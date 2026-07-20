# IQM 2024 Aggregation Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 제품 완성도 관리(IQM Plus) 대시보드에서 2024년 데이터가 누락되는 현상을 방지하기 위해 마스터 사양 데이터 수집 범위를 MP Gate BP. End가 2024년 이상인 기준으로 설정하고, 데이터의 귀속 연도(YEAR)를 MP Gate Act. End 기준으로 매핑되도록 보정합니다.

**Architecture:** `app/service/iqm_df.py` 내 `_get_master_table()` 함수에서 SQLite `ops.db`로부터 수집하는 정규 개발 사양 마스터 데이터 중, `MP Gate BP. End` 기준 연도(`BP_YEAR`)가 2024년 이상(`>= 2024`)인 대상만 선별(Filter)하고, `YEAR` 컬럼 값은 실제 완료 연도인 `MP Gate Act. End` 연도로 할당하여 실제 조회 연도에 정상 귀속되도록 수정합니다.

**Tech Stack:** Python 3.10+, Pandas, SQLite3, Pytest

## Global Constraints

- Safety Lock 준수: 사용자의 명시적인 승인 및 동의 없이 프로덕션 소스 코드를 즉각 수정하지 않습니다.
- 이모지 사용 금지: UI 및 소스 코드 내 모든 주석이나 마크다운에 유니코드 이모지를 배제하고 한국어로 통일하여 기술합니다.
- WSL 환경 상대 경로 사용: 하이퍼링크 작성 시 `file:///` 형식을 배제하고 평문 상대 경로 형식을 준수합니다.

---

### Task 1: 마스터 테이블 전처리 및 연도 귀속 규칙 보정

**Files:**
- Modify: `app/service/iqm_df.py:714-740`
- Test: `tests/test_iqm_2024_aggregation_fix.py`

**Interfaces:**
- Consumes: `get_client("sqlite", sqlite_db_path="ops").execute(q_iqm_plus.get_sqlite_regular_development_iqm_rawdata())`
- Produces: `_get_master_table()` 함수가 반환하는 `master_table` DataFrame (정상 필터링되고 YEAR가 보정된 형태)

- [ ] **Step 1: 검증용 신규 단위 테스트 작성**

  `tests/` 디렉터리 내에 독립적인 테스트 파일 `tests/test_iqm_2024_aggregation_fix.py`를 작성합니다.
  이 테스트는 실제 SQLite `ops.db`를 연동하거나 Mocking하여 `_get_master_table`이 `MP Gate BP. End >= 2024`인 대상을 모두 포함하면서, `YEAR`가 `MP Gate Act. End` 기준으로 설정되어 2024년에 완료된 사양(예: 1032599 등)의 `YEAR`가 2024로 안전하게 귀속되는지 검증합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (테스트 라이브러리 및 모듈 임포트)
  # =========================================================================
  import pytest
  import pandas as pd
  from app.service.iqm_df import _get_master_table

  # * [테스트 - 2024 IQM 데이터 수집 및 연도 귀속 규칙 검증]
  def test_get_master_table_aggregation_logic():
      """
      _get_master_table이 BP_YEAR >= 2024를 안전하게 필터링하고
      귀속 연도(YEAR)를 MP Gate Act. End의 년도로 매핑하는지 정적 검증합니다.
      """
      # 1. 마스터 데이터 로드 실행
      master_table, _, _, _, _, _ = _get_master_table()
      
      # 2. 기본 결과 무결성 검증
      assert isinstance(master_table, pd.DataFrame), "master_table은 DataFrame이어야 합니다."
      assert not master_table.empty, "master_table이 비어 있지 않아야 합니다."
      assert "YEAR" in master_table.columns, "YEAR 컬럼이 존재해야 합니다."
      assert "MCODE" in master_table.columns, "MCODE 컬럼이 존재해야 합니다."
      
      # 3. 최소 연도 제약조건 검증 (BP_YEAR가 2024 이상인 것만 필터링되더라도 실제 귀속 연도는 2024 이상이어야 함)
      # 실제 2024년에 Act. End가 발생한 데이터의 YEAR가 2024로 안전하게 할당되었는지 확인
      assert (master_table["YEAR"] >= 2024).all(), "모든 마스터 사양의 귀속 YEAR는 2024년 이상이어야 합니다."
      
      # 4. 특정 사례(MCODE='1032599')에 대한 귀속 연도 검증
      target_spec = master_table[master_table["MCODE"] == "1032599"]
      if not target_spec.empty:
          # MP Gate Act. End = 2024-12-05 이므로 YEAR는 2024여야 함 (BP. End = 2026-07-02 와 무관하게)
          assert (target_spec["YEAR"] == 2024).all(), "1032599의 귀속 YEAR는 2024여야 합니다."
  ```

- [ ] **Step 2: 작성한 테스트를 기동하여 실패(혹은 AS-IS 정합성 어긋남) 확인**

  Run: `pytest tests/test_iqm_2024_aggregation_fix.py -v`
  Expected: 기존 코드에서는 1032599의 `YEAR`가 `2026`으로 지정되거나, 2024년 이하의 일부 데이터 유실로 인해 단언문(assert)이 실패해야 합니다.

- [ ] **Step 3: 프로덕션 코드 `app/service/iqm_df.py` 수정**

  `_get_master_table` 함수 내부의 `sqliteOps_iqm_devSpecList` 생성 부분을 다음과 같이 수정합니다.

  ```python
  # =========================================================================
  # SECTION 2. Modified Master Data Collection
  # =========================================================================
  # AS-IS (Line 715-740 근처):
  # sqliteOps_iqm_devSpecList = (
  #     get_client("sqlite", sqlite_db_path="ops")
  #     .execute(q_iqm_plus.get_sqlite_regular_development_iqm_rawdata())
  #     .dropna(subset=["MP Gate Act. End"])
  #     .reset_index(drop=True)
  #     .assign(
  #         **{
  #             "M-code": lambda df: df["M-code"].astype(str),
  #             "MP Gate BP. End": lambda df: pd.to_datetime(
  #                 df["MP Gate BP. End"], errors="coerce"
  #             ),
  #             "YEAR": lambda df: pd.to_datetime(
  #                 df["MP Gate BP. End"], errors="coerce"
  #             ).dt.year,
  #         },
  #     )
  #     .rename(
  #         columns={
  #             "M-code": "MCODE",
  #             "MP Gate Act. End": "MP_GATE_DT",
  #             "Plant": "PLANT",
  #         }
  #     )[["MCODE", "YEAR", "PLANT", "MP_GATE_DT"]]
  #     .assign(PLANT=lambda df: df["PLANT"].map(MAPPING_PLANT_CODE))
  # )

  # TO-BE:
  sqliteOps_iqm_devSpecList = (
      get_client("sqlite", sqlite_db_path="ops")
      .execute(q_iqm_plus.get_sqlite_regular_development_iqm_rawdata())
      .dropna(subset=["MP Gate Act. End"])
      .reset_index(drop=True)
      .assign(
          **{
              "M-code": lambda df: df["M-code"].astype(str),
              "MP Gate BP. End": lambda df: pd.to_datetime(
                  df["MP Gate BP. End"], errors="coerce"
              ),
              "BP_YEAR": lambda df: pd.to_datetime(
                  df["MP Gate BP. End"], errors="coerce"
              ).dt.year,
              "YEAR": lambda df: pd.to_datetime(
                  df["MP Gate Act. End"], errors="coerce"
                ).dt.year,
          },
      )
      .loc[lambda df: df["BP_YEAR"] >= 2024]
      .rename(
          columns={
              "M-code": "MCODE",
              "MP Gate Act. End": "MP_GATE_DT",
              "Plant": "PLANT",
          }
      )[["MCODE", "YEAR", "PLANT", "MP_GATE_DT"]]
      .assign(PLANT=lambda df: df["PLANT"].map(MAPPING_PLANT_CODE))
  )
  ```

- [ ] **Step 4: 테스트 재기동 및 통과 확인**

  Run: `pytest tests/test_iqm_2024_aggregation_fix.py -v`
  Expected: 모든 단언문(assert) 성공 및 통과(PASS).

- [ ] **Step 5: 기존 전체 테스트 영향도(Regression) 확인**

  Run: `pytest tests/test_iqm_e2e_accumulation.py tests/test_iqm_self_healing.py -v`
  Expected: 기존 단위/통합 테스트 모두 100% 통과하여 사이드 이펙트가 없음을 실증합니다.
