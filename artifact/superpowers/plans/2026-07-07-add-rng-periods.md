# Add RNG range periods to IQM Plus queries and services Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 5대 핵심 Databricks SQL 쿼리에 RNG_91_180D, RNG_181_270D, RNG_271_365D 범위를 집계 및 Unpivot 로직으로 완벽 수용하고, 서비스 정제 헬퍼 및 비즈니스 상수와 UI 대시보드 전 영역에 누수 없이 전파하여 시각화 및 추세 분석 정합성을 구현합니다.

**Architecture:** 
1. Databricks SQL 5대 쿼리 함수 내에서 CTE(`_aggregated`, `periods`) 및 최종 Unpivot SELECT `CASE` 문에 3대 RNG 구간 수식을 추가 이식합니다.
2. `app/service/iqm_df.py` 내의 `_filter_and_map_period_names` 헬퍼 함수가 RNG 구간을 필터링 없이 투명하게 통과시키도록 보증하고, 모든 핵심 데이터 수집 함수의 반환부가 이 헬퍼를 무조건 거치도록 점검합니다.
3. `business_constants.json` 파일의 `PERIOD_LABELS`와 `PERIOD_ORDER` 목록에서 `"30D"`, `"60D"`를 완벽 분리하고, 7대 타겟 기간(`CUM_1_90D`~`CUM_1_365D`, `RNG_91_180D`~`RNG_271_365D`)을 정합 순서로 정의합니다.
4. Streamlit UI 렌더링 코드들을 점검하여 하드코딩된 기간명 누락 여부 확인 및 최종 정합성을 검증합니다.

**Tech Stack:** Python, Pandas, Streamlit, Databricks SQL, JSON

## Global Constraints
- safety-lock: 사용자의 명시적인 승인 없이 `app/` 하위 소스 코드를 수정할 수 없으나, 본 작업은 직접 요청된 Task 3.5 구현 사항이므로 동의 획득 및 수정을 동시 수행합니다.
- WSL-markdown-link-constraint: 모든 마크다운 내 링크는 절대 리눅스 경로(`file:///...`)를 배제하고 루트 기준의 평문 상대 경로(예: `docs/superpowers/plans/...md`)만을 작성합니다.
- emoji-ban: UI 텍스트, 코드 주석, 마크다운 텍스트, 커밋 메시지 등 모든 영역에서 유니코드 이모지 사용을 엄격히 금지합니다. (오직 Streamlit `:material/icon:` 구문만 허용)
- 한국어 독스트링 원칙: 소스 코드 주석 및 독스트링은 기본적으로 명확한 타입 힌팅과 함께 한국어(Korean)로 상세히 기술합니다.

---

### Task 1: `app/queries/q_iqm_plus.py` 5대 핵심 SQL 쿼리 개편

**Files:**
- Modify: `app/queries/q_iqm_plus.py`
- Test: `tests/queries/test_q_iqm_plus.py` (또는 인메모리 파싱 테스트)

**Interfaces:**
- Consumes: GMES 원천 Databricks 테이블 구조 및 DATEDIFF 함수
- Produces: 7대 기간(CUM_1_90D~CUM_1_365D, RNG_91_180D~RNG_271_365D)이 완벽히 Unpivot된 Databricks SQL 쿼리 스트링

- [ ] **Step 1.1: `get_query_prdt_by_unit_period` 생산 실적 쿼리 수정**
  - `prdt_aggregated` CTE 내에 `PRDT_QTY_RNG_91_180D`, `PRDT_QTY_RNG_181_270D`, `PRDT_QTY_RNG_271_365D` 집계 SUM 식 추가.
  - `periods` CTE 내에 UNION ALL 3대 RNG 구간 추가.
  - 최종 SELECT Unpivot CASE 문 내에 RNG 구간과 대응 집계 컬럼 매핑 추가.

- [ ] **Step 1.2: `get_query_gt_wt_by_unit_period` 중량 검사 쿼리 수정**
  - `period_aggregation` CTE 내에 pass 수 및 total 수 3대 RNG 구간 집계식 추가 (`pass_rng_91_180d`, `total_rng_91_180d` 등).
  - `periods` CTE 내에 동일하게 UNION ALL 3대 RNG 구간 추가.
  - 최종 SELECT CASE 내 `GT_WT_PASS_COUNT`, `GT_WT_INS_COUNT` 각각에 RNG 구간 매핑 및 `GT_WT_PASS_RATE` 수식 대응 추가.

- [ ] **Step 1.3: `get_query_uniformity_by_unit_period` 균일성 검사 쿼리 수정**
  - `period_aggregation` CTE 내에 pass 수 및 count 수 3대 RNG 구간 집계식 추가 (`PASS_rng_91_180d`, `COUNT_rng_91_180d` 등).
  - `periods` CTE 내에 UNION ALL 3대 RNG 구간 추가.
  - 최종 SELECT CASE 내 `UF_PASS_COUNT`, `UF_INS_COUNT` 각각에 RNG 구간 매핑 및 `UF_PASS_RATE` 수식 대응 추가.

- [ ] **Step 1.4: `get_query_scrap_from_mes` 및 `get_query_rework_from_mes` 불량 쿼리 수정**
  - `table_aggregated` CTE 내에 `DFT_QTY_RNG_91_180D`, `DFT_QTY_RNG_181_270D`, `DFT_QTY_RNG_271_365D` 집계 식 추가.
  - `periods` CTE 내에 UNION ALL 3대 RNG 구간 추가.
  - 최종 SELECT CASE 내 `DFT_QTY` Unpivot에 RNG 구간 매핑 추가.

---

### Task 2: `app/service/iqm_df.py` 수집 데이터 전처리 정제 헬퍼 보장 및 리턴 점검

**Files:**
- Modify: `app/service/iqm_df.py`
- Test: `tests/service/test_iqm_df.py` (필요 시 단위 검증 코드)

**Interfaces:**
- Consumes: Databricks 원천 반환 데이터프레임
- Produces: 30D/60D가 필터링되고 90D~365D는 CUM_1_90D~CUM_1_365D로 변경되며, RNG 구간은 그대로 통과된 전처리 완료 데이터프레임

- [ ] **Step 2.1: `_filter_and_map_period_names` 헬퍼 함수 점검 및 독스트링 갱신**
  - `_filter_and_map_period_names` 함수가 RNG 구간 컬럼들을 필터링 없이 투명하게 통과시키는지 코드 분석 및 정합성 보강.
  - 모듈 가이드라인 주석 형식(`# * [SERVICE - ...]`) 및 Google 스타일 한국어 독스트링 정비.

- [ ] **Step 2.2: 5대 핵심 데이터 수집 함수의 반환구 정합성 확인**
  - `get_prdt_by_unit_period`, `get_scrap_by_unit_period`, `get_rework_by_unit_period`, `get_gt_wt_by_unit_period`, `get_uniformity_by_unit_period` 함수 모두 최종 리턴 시 `_filter_and_map_period_names`가 올바르게 적용되어 누수 없이 데이터 정제가 동작하는지 재확인.

---

### Task 3: `app/core/data_models/business_constants.json` 기간 상수 추가 및 동기화

**Files:**
- Modify: `app/core/data_models/business_constants.json`

**Interfaces:**
- Consumes: 없음 (정적 상수 JSON)
- Produces: 30D/60D가 탈거되고 CUM 4대 구간과 RNG 3대 구간이 순서대로 정비된 `PERIOD_LABELS` 및 `PERIOD_ORDER` 리스트

- [ ] **Step 3.1: JSON 내 PERIOD_LABELS와 PERIOD_ORDER 리스트 갱신**
  - 기존 `"30D"`, `"60D"` 목록 완벽 제거.
  - 7대 기간 명시적 추가: `["CUM_1_90D", "CUM_1_180D", "CUM_1_270D", "CUM_1_365D", "RNG_91_180D", "RNG_181_270D", "RNG_271_365D"]`.

---

### Task 4: 대시보드 렌더링 코드 내 하드코딩 명칭 치환 및 최종 검증

**Files:**
- Modify/Verify: `app/pages/_10_dashboard/iqm_plus_main_page.py`, `app/pages/_10_dashboard/iqm_plus_main_plots.py`, `app/pages/_10_dashboard/iqm_quality_trend_analysis_page.py`
- Test: 전체 streamlit 코드 정적 컴파일 및 실행 검증

- [ ] **Step 4.1: 대시보드 UI 파일들의 CUM_1_ 접두어 정합성 전수 조사 및 하드코딩 보정**
  - `iqm_plus_main_page.py` 내부 `periods = ["CUM_1_90D", "CUM_1_180D", "CUM_1_270D", "CUM_1_365D"]`가 정합하게 유지되고 있는지 확인.
  - `iqm_plus_main_plots.py` 내부 `create_m_level_trend_gauge_charts`의 `title_dict` 키가 올바르게 `CUM_1_90D` 등으로 동작하는지 확인.
  - `iqm_quality_trend_analysis_page.py` 내부 피벗 연산 수동 생성 방어벽(`periods`), `get_latest_active_period` 최신 가용 구간 탐색 로직 등에서 `"90D"`~`"365D"` 하드코딩 문자열들이 누수 없이 `"CUM_1_90D"`~`"CUM_1_365D"`로 정돈되었는지 이중 체크.

- [ ] **Step 4.2: 배포 전 자가 컴파일 및 검증 수행**
  - 정적 린트 체크 또는 `python -m py_compile` 명령을 통해 수정된 Python 파일들의 구문 오류 전수 차단.
  - 검증 단계가 성공적으로 완결되면 `verification-before-completion` 사양을 만족하는 무결함 보고서를 빌드하여 저장.
