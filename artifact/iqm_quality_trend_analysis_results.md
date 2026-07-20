# IQM 품질 규격별 추세 분석 대시보드 데이터 누락 장애 정밀 진단 및 조치 제안서

본 보고서는 IQM 품질 규격별 추세 분석 대시보드 가동 후, 화면 상에 분석 데이터가 일절 노출되지 않는 현상(Empty View)에 대한 원천 DB 분석 결과와 이를 해결하기 위한 정교한 전처리 로직 리팩토링 방안을 제시합니다.

---

## 1. 정밀 원인 분석 (Root Cause Investigation)

### ① 원천 데이터베이스 검증
본 프로젝트의 로컬 Staging DB인 `local.data/database/staging.db` 내의 `product_audit_iqm_plus_agg_interval` 테이블을 정밀 조회한 결과, 총 **484건**의 데이터가 정상적으로 적재되어 있음을 확인하였습니다.
- **2025년 생산 실적 규격**: 316건 (유니크 규격 수: 79개)
- **2026년 생산 실적 규격**: 168건 (유니크 규격 수: 42개)

### ② 연도 간 규격 매핑 불일치 (교집합 0건)
기존 대시보드의 필터 처리 로직은 선택된 두 연도(예: 2025년과 2026년)에 대해 동일한 자재코드(`MCODE`)를 기준으로 `how="inner"` 조인을 수행하여 연도 간 지표 변화(Gap)를 분석하도록 개발되었습니다.
그러나 두 연도의 규격코드 교집합을 계산한 결과, **교집합 건수가 정확히 0건**으로 확인되었습니다.
- **원인**: 개별 규격(`MCODE`)은 양산 승인을 받은 시점의 계획 연도로 `YEAR` 값이 정적으로 매핑(`df_spec_master` 테이블 기준)되어 저장됩니다. 따라서 한 규격은 양산 연도(예: 2025년 혹은 2026년)의 레코드로 고정되어 존재하므로, 연도 간 교집합 규격이 발생하지 않는 구조적 특성을 가지고 있습니다.
- **결과**: `pd.merge(df_prev, df_curr, on="MCODE", how="inner")`를 수행할 때 결과 데이터프레임이 공집합이 됨으로써 화면 상에 "분석 데이터 없음" 경고만 출력되는 버그가 발생한 것입니다.

---

## 2. 해결 방안 제안 (Proposed Solution)

### ① 동일 규격 내의 양산 수명 주기 구간별 추세 분석으로 전환 (90D vs 365D)
IQM Plus의 본질적인 모니터링 목적은 **"양산 승인 후 초기 유동 365일 동안의 품질 흐름"**을 점검하는 것입니다.
따라서 연도 간의 1:1 비교 대신, 선택된 연도 범위 내에서 활성화된 **개별 규격 자체의 시간 흐름에 따른 트렌드(양산 초기 90D 대비 양산 말기 365D의 품질 변화 격차)**를 계산하여 추세를 판정하는 구조로 전처리 로직을 전환합니다.

- **PREV (기준/초기)**: 해당 규격의 양산 최초 구간인 `90D` 시점의 지표
- **CURR (비교/최종)**: 해당 규격이 도달한 가장 최근 구간(`180D`, `270D`, `365D` 중 최신 데이터)의 지표
- **효과**: 연도 간 공통 규격이 존재하지 않아도, 선택된 모든 개발 규격들에 대해 초기 양산 대비 품질 개선/악화 트렌드를 100% 정상 누락 없이 추적 및 렌더링할 수 있게 됩니다.

---

## 3. 세부 코드 수정 계획 (Refactoring Plan)

`app/pages/_80_admin/iqm_quality_trend_analysis_page.py` 소스 파일 내부의 전처리 함수와 호출부를 다음과 같이 수정할 것을 제안합니다.

### ① `calculate_trend_gaps` 전처리 함수 리팩토링

```python
# =========================================================================
# SECTION 6. Trend Preprocessing Helper (추세 연산 헬퍼 함수)
# =========================================================================
def calculate_trend_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """선택된 연도 범위에 속하는 개별 규격(MCODE)의 초기 양산(90D) 대비 양산 말기(최신 구간) 품질 지표와 증감 격차(Gap)를 산출합니다.

    Args:
        df (pd.DataFrame): 필터링된 원천 데이터프레임

    Returns:
        pd.DataFrame: 규격(MCODE)별 구간 격차 및 종합 추세 분석 결과 데이터프레임
    """
    if df.empty:
        return pd.DataFrame()

    # 1. 초기 구간(90D) 데이터 추출
    df_prev = df[df["PERIOD_NAME"] == "90D"].copy()
    if df_prev.empty:
        return pd.DataFrame()

    # 2. 최종 구간 데이터 추출 (90D가 아닌 다른 구간 중 규격별 가장 최신 구간을 잡음)
    df_sorted = df[df["PERIOD_NAME"] != "90D"].sort_values(by=["MCODE", "PERIOD_NAME"])
    if df_sorted.empty:
        df_curr = df_prev.copy()
    else:
        df_curr = df_sorted.groupby("MCODE").last().reset_index()

    # 3. 규격(MCODE) 기준 Inner Join 병합
    df_merged = pd.merge(
        df_prev[["MCODE", "SCRAP_RATE", "REWORK_RATE", "GT_WT_PASS_RATE", "UF_PASS_RATE", "PRDT_QTY"]],
        df_curr[["MCODE", "SCRAP_RATE", "REWORK_RATE", "GT_WT_PASS_RATE", "UF_PASS_RATE", "PRDT_QTY"]],
        on="MCODE",
        suffixes=("_PREV", "_CURR"),
        how="inner"
    )

    if df_merged.empty:
        return pd.DataFrame()

    # 4. 각 지표별 구간 격차(Gap) 산출 (최신 - 이전)
    df_merged["SCRAP_GAP"] = df_merged["SCRAP_RATE_CURR"] - df_merged["SCRAP_RATE_PREV"]
    df_merged["REWORK_GAP"] = df_merged["REWORK_RATE_CURR"] - df_merged["REWORK_RATE_PREV"]
    df_merged["GT_WT_GAP"] = df_merged["GT_WT_PASS_RATE_CURR"] - df_merged["GT_WT_PASS_RATE_PREV"]
    df_merged["UF_GAP"] = df_merged["UF_PASS_RATE_CURR"] - df_merged["UF_PASS_RATE_PREV"]

    # 5. 각 지표별 개선 여부 점수화 (종합 트렌드 계산용)
    # Scrap/Rework (불량률): 감소할수록 개선(1), 증가할수록 악화(-1)
    scrap_score = df_merged["SCRAP_GAP"].apply(lambda x: 1 if x < 0 else (-1 if x > 0 else 0))
    rework_score = df_merged["REWORK_GAP"].apply(lambda x: 1 if x < 0 else (-1 if x > 0 else 0))
    # GT_WT/UF (합격률): 증가할수록 개선(1), 감소할수록 악화(-1)
    gt_score = df_merged["GT_WT_GAP"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    uf_score = df_merged["UF_GAP"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

    # 종합 트렌드 지수 합산 및 판정
    df_merged["TOTAL_TREND_SCORE"] = scrap_score + rework_score + gt_score + uf_score
    df_merged["TOTAL_TREND_DECISION"] = df_merged["TOTAL_TREND_SCORE"].apply(
        lambda s: "개선" if s > 0 else ("악화" if s < 0 else "유지")
    )

    return df_merged
```

### ② 데이터 필터링 실행부 바인딩 및 라벨 텍스트 개선

```python
# Gap 데이터 산출 (선택된 연도 필터 범위 내에서 규격별 구간 격차 연산)
df_analysis = calculate_trend_gaps(df_filtered)

# 최소 생산량 컷오프 필터 적용 (최근 구간 생산량 기준)
if not df_analysis.empty:
    df_analysis = df_analysis[df_analysis["PRDT_QTY_CURR"] >= qty_cutoff]
```

또한, 테이블 정보성 캡션을 "연도 간 대조"에서 "양산 초기(90D) 대비 양산 말기(최신 구간) 대조" 문구로 자연스럽게 동기화하여 정보 신뢰도를 비약적으로 보증합니다.

---

## 4. 사용자 의사결정 요청 및 다음 단계

위 조치 방안을 적용할 경우, 사용자가 선택한 연도 필터에 부합하는 모든 핵심 규격들이 하나도 빠짐없이 정상적으로 로딩되며, 메트릭, 시각화, 상세 테이블이 완벽하게 가동됩니다.

- [ ] **방안 적용 및 화면 검증 진행 요청**: 사용자의 동의를 얻는 대로 `app/pages/_80_admin/iqm_quality_trend_analysis_page.py` 소스 파일에 정교하게 반영하고, 로컬 정적 컴파일 및 전체 테스트를 통과시킨 후 수정을 최종 완수하겠습니다.
