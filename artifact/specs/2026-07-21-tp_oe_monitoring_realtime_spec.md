# SPECIFICATION: TP OE Monitoring Real-Time Data Source Transition

## 1. 개요 및 목적 (Background & Purpose)
TP 공장 2026년 이상 MP-GATE 대상 5대 규격 모니터 시스템(`tp_oe_monitoring`)의 실적 데이터 원천을 기존 로컬 SQLite의 선집계 캐시 뷰(`tp_oe_2026_target_metrics_agg`)에서 **실시간 Databricks 클라우드 데이터웨어하우스**로 완전히 전환합니다. 
이를 통해 데이터 정합성을 확보하고, 실적 조회가 페이지 로딩 시마다 원천 DB를 거쳐 최신 실시간 데이터로 표출될 수 있도록 리팩토링하는 것을 목표로 합니다.

---

## 2. 사용 데이터 원천 및 테이블 (Data Sources & Tables)
원천 Databricks에서 데이터를 취합하기 위해 다음 테이블들을 사용합니다:
1.  **규격 마스터 (SQLite `staging.db`)**:
    -   `iqm_plus_spec_master` 테이블: 5대 타깃 자재(`1033649`, `1033647`, `2022188`, `1034831`, `1034828`)의 기준 속성(스펙명, OEM, 양산시작일 등) 수집
2.  **생산량 (Databricks)**:
    -   `hkt_dw.production.wrk_f_lwrkts118` (`gmes_prd_production_volume`): 실시간 생산 실적 수량
3.  **공정 및 출하 부적합 (Databricks)**:
    -   `hkt_dw.quality.qlt_f_lqlttr107` (`gmes_ncf_finished_product_inspection_result`): 완제품 공정 검사 부적합
    -   `hkt_dw.quality.qlt_f_lqlttr120` (`gmes_ncf_shipment_inspection_result`): 완제품 출하 검사 부적합
4.  **중량 검사 (Databricks)**:
    -   `hkt_dw.quality.qlt_f_lqlttr127` (`gmes_build_manufacture_report`): 그린/가류 타이어 중량 계측 원천 데이터
5.  **Uniformity 검사 (Databricks)**:
    -   `hkt_quality.inspection.uniformity_result_raw` (`gmes_uf_result_raw`): 완제품 Uniformity 정밀 계측 및 합격 판정 원천 데이터

---

## 3. 통합 결합 Databricks SQL 쿼리 설계 (Unified SQL Query)
페이지 렌더링 성능을 저해하는 다중 데이터베이스 라운드트립을 최소화하기 위해, 단 한 번의 호출로 생산, 스크랩, 리워크, 중량, Uniformity 실적을 모두 집계하는 결합 쿼리를 사용합니다.

```sql
WITH spec_master AS (
    SELECT DISTINCT PLT_CD AS PLANT, PRD_CD AS MCODE, SPEC_CD
    FROM hkt_dw.specification.mas_d_lmastr101
    WHERE PLT_CD = 'TP' AND PRD_CD IN ('1033649', '1033647', '2022188', '1034831', '1034828')
),
prod AS (
    SELECT PRD_CD AS MCODE, SUM(PRDT_QTY) AS PRDT_QTY
    FROM hkt_dw.production.wrk_f_lwrkts118
    WHERE PLT_CD = 'TP'
      AND PRD_CD IN ('1033649', '1033647', '2022188', '1034831', '1034828')
      AND WRK_DATE >= '20260101'
    GROUP BY PRD_CD
),
ncf_proc AS (
    SELECT m.MCODE, ncf.INS_TP_CD, ncf.DFT_QTY
    FROM spec_master m
    INNER JOIN hkt_dw.quality.qlt_f_lqlttr107 ncf
       ON m.PLANT = ncf.PLT_CD AND m.SPEC_CD = ncf.SPEC_CD
    WHERE ncf.DFT_QTY > 0 AND ncf.INS_DATE >= '20260101'
),
ncf_ship AS (
    SELECT m.MCODE, '1' AS INS_TP_CD, s.DFT_QTY
    FROM spec_master m
    INNER JOIN hkt_dw.quality.qlt_f_lqlttr120 s
       ON m.PLANT = s.PLT_CD AND m.SPEC_CD = s.SPEC_CD
    WHERE s.DFT_QTY > 0 AND s.INS_DATE >= '20260101' AND s.DFT_OCCR_FG = '1'
),
ncf_all AS (
    SELECT MCODE, INS_TP_CD, DFT_QTY FROM ncf_proc
    UNION ALL
    SELECT MCODE, INS_TP_CD, DFT_QTY FROM ncf_ship
),
ncf_agg AS (
    SELECT 
        MCODE,
        SUM(CASE WHEN INS_TP_CD IN ('1', '2', '3', '5') THEN DFT_QTY ELSE 0 END) AS SCRAP_DFT_QTY,
        SUM(CASE WHEN INS_TP_CD IN ('4', '6', '8', 'C', 'D', 'H', 'V') THEN DFT_QTY ELSE 0 END) AS REWORK_DFT_QTY
    FROM ncf_all
    GROUP BY MCODE
),
wt AS (
    SELECT m.MCODE,
           CASE WHEN w.STD_WGT != 0 AND w.MRM_WGT >= (w.STD_WGT * 0.975) AND w.MRM_WGT <= (w.STD_WGT * 1.025) THEN 1 ELSE 0 END AS JDG
    FROM spec_master m
    INNER JOIN hkt_dw.quality.qlt_f_lqlttr127 w
       ON m.PLANT = w.PLT_CD AND m.SPEC_CD = w.SPEC_CD
    WHERE w.INS_DATE >= '20260101' AND w.MRM_WGT != 0
),
wt_agg AS (
    SELECT 
        MCODE,
        COUNT(*) AS GT_WT_INS_COUNT,
        SUM(JDG) AS GT_WT_PASS_COUNT
    FROM wt
    GROUP BY MCODE
),
uf AS (
    SELECT m.MCODE,
           CASE 
               WHEN m.PLANT IN ('JP','HP','CP') AND u.JDG_GR <= 3 THEN 1
               WHEN m.PLANT IN ('KP','DP','IP','MP','TP') AND u.JDG_GR <= 4 THEN 1
               ELSE 0
           END AS JDG
    FROM spec_master m
    INNER JOIN hkt_quality.inspection.uniformity_result_raw u
       ON m.PLANT = u.PLT_CD AND m.SPEC_CD = u.SPEC_CD
    WHERE u.INS_DATE >= '20260101' AND u.INS_FG = '1'
),
uf_agg AS (
    SELECT 
        MCODE,
        COUNT(*) AS UF_INS_COUNT,
        SUM(JDG) AS UF_PASS_COUNT
    FROM uf
    GROUP BY MCODE
)
SELECT 
    m.MCODE,
    COALESCE(p.PRDT_QTY, 0) AS PRDT_QTY,
    COALESCE(n.SCRAP_DFT_QTY, 0) AS SCRAP_DFT_QTY,
    COALESCE(n.REWORK_DFT_QTY, 0) AS REWORK_DFT_QTY,
    COALESCE(w.GT_WT_INS_COUNT, 0) AS GT_WT_INS_COUNT,
    COALESCE(w.GT_WT_PASS_COUNT, 0) AS GT_WT_PASS_COUNT,
    COALESCE(u.UF_INS_COUNT, 0) AS UF_INS_COUNT,
    COALESCE(u.UF_PASS_COUNT, 0) AS UF_PASS_COUNT
FROM (SELECT DISTINCT MCODE FROM spec_master) m
LEFT JOIN prod p ON m.MCODE = p.MCODE
LEFT JOIN ncf_agg n ON m.MCODE = n.MCODE
LEFT JOIN wt_agg w ON m.MCODE = w.MCODE
LEFT JOIN uf_agg u ON m.MCODE = u.MCODE
```

---

## 4. 서비스 레이어 리팩토링 설계 (Service Refactoring)
`app/service/tp_oe_2026_service.py` 내의 `get_tp_oe_2026_spec_data()` 함수를 다음과 같이 리팩토링합니다.

1.  **Staging DB 규격 마스터 쿼리**:
    -   `iqm_plus_spec_master` 테이블에서 타깃 연도가 2026년 이상이고 TP 공장인 5대 타깃 자재 메타 정보 조회.
2.  **실시간 Databricks 쿼리 실행**:
    -   `try...except` 가드로 래핑하여 Databricks 클라이언트(`get_client("databricks")`)를 통해 위 통합 쿼리를 실행.
    -   결과 데이터프레임의 모든 칼럼명을 대문자 처리하여 SQLite 메타데이터 칼럼 양식과 통일.
3.  **데이터 결합 및 파생 칼럼 계산**:
    -   SQLite에서 조회한 메타데이터와 Databricks에서 가져온 실시간 실측 수치 데이터프레임을 `MCODE` 기준으로 Left Join.
    -   `MASS_PERIOD`를 오늘 날짜 대비 양산시작일(`MIN_WRK_DATE`)의 경과 일수로 동적 계산 (`(today - min_wrk_date).days`).
    -   PPM 및 합격률 계산:
        -   `SCRAP_PPM` = `SCRAP_DFT_QTY / PRDT_QTY * 1,000,000` (PRDT_QTY > 0 일 때만)
        -   `REWORK_PPM` = `REWORK_DFT_QTY / PRDT_QTY * 1,000,000` (PRDT_QTY > 0 일 때만)
        -   `GT_WT_PASS_RATE` = `GT_WT_PASS_COUNT / GT_WT_INS_COUNT * 100` (GT_WT_INS_COUNT > 0 일 때만)
        -   `UF_PASS_RATE` = `UF_PASS_COUNT / UF_INS_COUNT * 100` (UF_INS_COUNT > 0 일 때만)
4.  **강력한 장애 극복 가드 (Robust Fallback)**:
    -   Databricks 연결이 유효하지 않거나 에러 발생 시, 모든 실적 수치를 0 또는 기본값으로 안전하게 바인딩한 데이터프레임을 만들어 반환. 페이지 전체에 5대 타깃 마스터는 온전히 노출될 수 있도록 완벽 방어.

---

## 5. 단위 테스트 설계 및 검증 계획 (Testing Strategy)
-   `tests/test_tp_oe_2026_service.py`에 작성된 기존 단위 테스트 검증 사양이 변경 후에도 무너지지 않고 정상적으로 작동(100% 통과)함을 검증.
-   Databricks 쿼리가 실행되는 상태와 연결 실패 시의 Mock 테스트를 추가로 수립하여 비상 극복 모드가 제대로 작동하는지 교차 확인.
