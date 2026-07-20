# G/T Weight Recalculation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** G/T Weight(완제품 중량) 합격 판정 기준을 기존 고정형 상하한(UPM_STD_WGT, LWM_STD_WGT)에서 기준 중량(STD_WGT) 대비 +/- 2.5% 범위 내 가변 판정하도록 SQL 수식을 수정하고, SQLite 캐시 동기화를 실행하여 무결하게 변경 완료합니다.

**Architecture:** 
DWH 원천 데이터를 집계하여 SQLite Staging DB에 캐싱하는 SQL 쿼리 어셈블러 레이어의 `JDG` 수식을 직접 수정합니다. 이렇게 함으로써 SQLite Staging DB 스키마는 원본 그대로 유지하되, 집계되는 무결성 데이터 내용만 가변 룰에 맞춰 정교하게 갱신되도록 보장합니다.

**Tech Stack:** Python 3.10+, SQLite3, pytest, Databricks SQL Engine (via Python DB Client)

## Global Constraints

- **Safety Lock**: 사용자의 직접 승인 없이 프로덕션 소스 코드(`app/` 및 `app.py`)를 임의로 수정하여 배포할 수 없습니다. 본 구현 계획의 Task 2 실행 시에만 코드 수정이 승인됩니다.
- **No Unicode Emojis**: Streamlit UI, 소스 코드 주석, 마크다운 텍스트 및 주석 어디에서도 일반 유니코드 이모지(예: 별, 느낌표, 가위표 등)를 절대로 사용하지 않습니다.
- **Korean Comments Principle**: 작성되는 유닛 테스트 및 수정되는 소스 코드 주석, 독스트링(Docstring)은 가독성과 협업 정합성을 극대화하기 위해 한국어(Korean)로 작성하는 것을 원칙으로 합니다.
- **WSL Path Protocol Exclusion**: 마크다운 내 모든 파일 링크는 절대 리눅스 경로 및 `file:///` 프로토콜을 사용하지 않고, 오직 평문 상대 경로만을 이용해 작성합니다.

---

### Task 1: G/T Weight 판정 기준 변경 유닛 테스트 작성 (TDD 실패 단계)

G/T Weight 판정 기준이 +/- 2.5% (`STD_WGT * 0.975`에서 `STD_WGT * 1.025` 사이) 수식으로 생성되는지 정적으로 검증하는 독립 유닛 테스트를 생성하고, 실패함을 확인합니다.

**Files:**
- Create: `tests/test_gt_weight_spec.py`

**Interfaces:**
- Consumes: `app.queries.q_iqm_plus.get_query_gt_wt_by_unit_period`, `app.queries.gmes_query.get_gmes_gt_wt_rawdata`, `app.queries.gmes_query.get_gmes_gt_wt_by_period`
- Produces: `test_gt_weight_sql_generation_recalculation` 유닛 테스트 스펙

- [ ] **Step 1: 실패하는 유닛 테스트 코드 작성**
  `tests/test_gt_weight_spec.py` 파일을 새로 생성하고 아래의 코드를 작성합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports
  # =========================================================================
  import pytest
  from app.queries import q_iqm_plus
  from app.queries import gmes_query
  from app.core.data_models.parameters import GTWeightParams

  # =========================================================================
  # SECTION 2. Unit Tests for G/T Weight Recalculation SQL
  # =========================================================================

  def test_q_iqm_plus_query_contains_new_recalculation_formula():
      """q_iqm_plus의 완제품 중량 집계 쿼리가 +/- 2.5% 기준 수식으로 생성되는지 검증합니다."""
      # Given
      mcode_list = ["M12345"]
      year = 2026
      month = 6

      # When
      query_str = q_iqm_plus.get_query_gt_wt_by_unit_period(mcode_list, year=year, month=month)

      # Then
      # 새 판정 비율 상수(0.975, 1.025) 및 STD_WGT 가 쿼리에 포함되었는지 검증
      assert "0.975" in query_str, "집계 쿼리 내 하한 비율 상수 0.975가 누락되었습니다."
      assert "1.025" in query_str, "집계 쿼리 내 상한 비율 상수 1.025가 누락되었습니다."
      assert "STD_WGT" in query_str, "집계 쿼리 내 기준 중량 컬럼 STD_WGT 참조가 누락되었습니다."
      assert "UPM_STD_WGT" not in query_str, "집계 쿼리 내 레거시 상한 컬럼 UPM_STD_WGT가 남아있습니다."
      assert "LWM_STD_WGT" not in query_str, "집계 쿼리 내 레거시 하한 컬럼 LWM_STD_WGT가 남아있습니다."


  def test_gmes_query_rawdata_contains_new_recalculation_formula():
      """gmes_query의 완제품 중량 원시 데이터 쿼리가 +/- 2.5% 기준 수식으로 생성되는지 검증합니다."""
      # Given
      params = GTWeightParams(
          plant_list=["P1"],
          spec_fg_list=["KT"],
          spec_type_list=["S"],
          mcode_list=["M12345"],
          start_date="2026-06-01",
          end_date="2026-06-30"
      )

      # When
      query_str_raw = gmes_query.get_gmes_gt_wt_rawdata(params)
      query_str_period = gmes_query.get_gmes_gt_wt_by_period(params)

      # Then (Raw query)
      assert "0.975" in query_str_raw, "원시 데이터 쿼리 내 하한 비율 상수 0.975가 누락되었습니다."
      assert "1.025" in query_str_raw, "원시 데이터 쿼리 내 상한 비율 상수 1.025가 누락되었습니다."
      assert "UPM_STD_WGT" not in query_str_raw, "원시 데이터 쿼리 내 레거시 상한 컬럼 UPM_STD_WGT가 남아있습니다."

      # Then (Period query)
      assert "0.975" in query_str_period, "기간별 쿼리 내 하한 비율 상수 0.975가 누락되었습니다."
      assert "1.025" in query_str_period, "기간별 쿼리 내 상한 비율 상수 1.025가 누락되었습니다."
      assert "UPM_STD_WGT" not in query_str_period, "기간별 쿼리 내 레거시 상한 컬럼 UPM_STD_WGT가 남아있습니다."
  ```

- [ ] **Step 2: 테스트를 실행하여 실패하는지 검증**
  터미널에서 새로 작성한 테스트를 수행하여 레거시 상한 컬럼 참조 및 새 수식 상수가 누락되어 실패하는지 확인합니다.

  Run: `pytest tests/test_gt_weight_spec.py -v`
  Expected: FAIL (AssertionError: "집계 쿼리 내 하한 비율 상수 0.975가 누락되었습니다." 또는 "UPM_STD_WGT가 남아있습니다." 등의 에러 메시지 발생)

- [ ] **Step 3: 테스트 실패 형상 기록 및 커밋**
  실패 테스트가 등록되었으므로 형상 변경을 기록합니다.

  ```bash
  git add tests/test_gt_weight_spec.py
  git commit -m "test: add failing TDD test for G/T Weight recalculation logic"
  ```

---

### Task 2: G/T Weight SQL 판정 수식 수정 및 테스트 통과 단계 (TDD 통과 단계)

쿼리 생성 모듈 내의 G/T Weight 판정 SQL 수식을 수정하여 +/- 2.5% 가변 범위를 적용하고, 작성한 유닛 테스트를 성공시킵니다.

**Files:**
- Modify: `app/queries/q_iqm_plus.py:360-374`
- Modify: `app/queries/gmes_query.py:2108-2122`
- Modify: `app/queries/gmes_query.py:2180-2194`

**Interfaces:**
- Consumes: None
- Produces: 수정 완료된 `get_query_gt_wt_by_unit_period`, `get_gmes_gt_wt_rawdata`, `get_gmes_gt_wt_by_period`

- [ ] **Step 1: `app/queries/q_iqm_plus.py`의 `get_query_gt_wt_by_unit_period` 수정**
  `app/queries/q_iqm_plus.py` 파일의 Line 363 부근을 아래와 같이 수정합니다.

  AS-IS:
  ```sql
              CASE WHEN bmr.MRM_WGT <= bmr.UPM_STD_WGT AND bmr.MRM_WGT >= bmr.LWM_STD_WGT THEN 1 ELSE 0 END AS JDG
  ```

  TO-BE:
  ```sql
              CASE WHEN bmr.STD_WGT != 0 AND bmr.MRM_WGT >= (bmr.STD_WGT * 0.975) AND bmr.MRM_WGT <= (bmr.STD_WGT * 1.025) THEN 1 ELSE 0 END AS JDG
  ```

- [ ] **Step 2: `app/queries/gmes_query.py`의 `get_gmes_gt_wt_rawdata` 및 `get_gmes_gt_wt_by_period` 수정**
  `app/queries/gmes_query.py` 파일의 Line 2115 및 Line 2187 부근을 아래와 같이 수정합니다.

  AS-IS (Line 2115 부근):
  ```sql
                      CASE
                          WHEN MRM_WGT <= UPM_STD_WGT AND MRM_WGT >= LWM_STD_WGT THEN 1
                          ELSE 0
                      END AS JDG
  ```

  TO-BE (Line 2115 부근):
  ```sql
                      CASE
                          WHEN STD_WGT != 0 AND MRM_WGT >= (STD_WGT * 0.975) AND MRM_WGT <= (STD_WGT * 1.025) THEN 1
                          ELSE 0
                      END AS JDG
  ```

  AS-IS (Line 2187 부근):
  ```sql
                      CASE
                          WHEN MRM_WGT <= UPM_STD_WGT AND MRM_WGT >= LWM_STD_WGT THEN 1
                          ELSE 0
                      END AS JDG
  ```

  TO-BE (Line 2187 부근):
  ```sql
                      CASE
                          WHEN STD_WGT != 0 AND MRM_WGT >= (STD_WGT * 0.975) AND MRM_WGT <= (STD_WGT * 1.025) THEN 1
                          ELSE 0
                      END AS JDG
  ```

- [ ] **Step 3: 테스트를 실행하여 성공하는지 검증**
  수정 완료된 SQL 어셈블러 함수들이 유닛 테스트 단언문(Assert)을 성공적으로 통과하는지 확인합니다.

  Run: `pytest tests/test_gt_weight_spec.py -v`
  Expected: PASS

- [ ] **Step 4: 무결성 통과 형상 기록 및 커밋**
  수정이 완벽히 완료되었으므로 형상 변경을 커밋합니다.

  ```bash
  git add app/queries/q_iqm_plus.py app/queries/gmes_query.py
  git commit -m "feat: recalculate G/T Weight pass rate based on STD_WGT +/- 2.5%"
  ```

---

### Task 3: SQLite Staging DB 캐시 데이터 강제 동기화 갱신 및 대시보드 무결성 확인

변경된 판정 수식을 토대로 SQLite Staging DB of 집계 데이터를 실제로 재생성 및 갱신하고, 데이터 정합성에 문제가 없는지 확인합니다.

**Files:**
- Create: `tests/test_gt_weight_db_refresh.py` (임시 검증 및 갱신 스크립트)

**Interfaces:**
- Consumes: `app.service.iqm_df.run_iqm_aggregation`
- Produces: 갱신된 SQLite Staging DB `prd_audit_iqm_plus_monthly_agg` 테이블 데이터

- [ ] **Step 1: Staging DB 데이터 갱신 및 무결성 검증 스크립트 작성**
  `tests/test_gt_weight_db_refresh.py` 파일을 작성하여, 최근 주요 연월 데이터(예: 2026년 6월 등)를 신규 규칙으로 집계 갱신 및 SQLite에 정상 적재되었는지 레코드 카운트를 정량 확인합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports
  # =========================================================================
  import sqlite3
  import pytest
  from app.service.iqm_df import run_iqm_aggregation, SQLiteTables

  # =========================================================================
  # SECTION 2. Staging DB Recaching and Verification
  # =========================================================================

  def test_run_aggregation_recaches_new_standards_successfully():
      """변경된 룰을 토대로 대상 연월의 SQLite Staging 캐시를 강제 동기화하고 정합성을 검증합니다."""
      # Given
      target_year = 2026
      target_month = 6
      db_path = "/home/jumasi/workstation/local.data/database/staging.db"

      # When - 데이터 파이프라인 강제 재생성 트리거 (Mocking 없이 실제 데이터 적재 흐름 실행)
      master_df = run_iqm_aggregation(save_db=True, target_year=target_year, target_month=target_month)

      # Then 1. 반환된 데이터프레임 무결성 체크
      assert master_df is not None, "동기화 후 결과 데이터프레임이 생성되지 않았습니다."
      assert not master_df.empty, "동기화된 데이터프레임이 완전히 비어있습니다."

      # Then 2. SQLite Staging DB의 실제 적재 상태 직접 확인
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()
      cursor.execute(
          f"SELECT COUNT(1) FROM {SQLiteTables.prd_audit_iqm_plus_monthly_agg} WHERE YEAR = ? AND MONTH = ?",
          (target_year, target_month)
      )
      count = cursor.fetchone()[0]
      conn.close()

      print(f"동기화 완료 레코드 수: {count}건")
      assert count > 0, "SQLite Staging DB에 캐시 데이터가 비정상적으로 적재되지 않았습니다."
  ```

- [ ] **Step 2: 동기화 및 검증 테스트 실행**
  DWH 연결이 정상적으로 수행되어 2026년 6월 데이터를 SQLite에 무사히 갱신 완료하는지 확인합니다.

  Run: `pytest tests/test_gt_weight_db_refresh.py -s -v`
  Expected: PASS 및 "동기화 완료 레코드 수: N건" 정상 콘솔 출력

- [ ] **Step 3: Staging DB 갱신 검증 완료 형상 기록 및 최종 마무리**
  모든 캐시 데이터 동기화 및 검증이 완료되었으므로 최종 테스트 및 헬퍼 파일들을 커밋합니다.

  ```bash
  git add tests/test_gt_weight_db_refresh.py
  git commit -m "test: add integration test to refresh SQLite staging DB for G/T weight recalculation"
  ```
