# NCF Table Refactoring & Scrap-Rework Direct Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Staging DB의 불필요한 합성 테이블 product_audit_ncf를 제거하고, Scrap과 Rework 개별 도메인 테이블로 수집 및 캐싱 프로세스를 분리 정규화하며, 최종 집계 배치(run_iqm_aggregation) 및 관리자 대시보드 UI를 이에 맞춤형으로 개편합니다.

**Architecture:** 
1. `iqm_df.py` 내의 `get_ncf_by_unit_period` 함수를 제거하고, `get_scrap_by_unit_period`와 `get_rework_by_unit_period`로 분할하여 개별 수집하도록 변경합니다.
2. 집계 배치 실행 시 기존 `ncf` 테이블을 저장하지 않고 `product_audit_scrap`과 `product_audit_rework` 각각으로 SQLite에 적재한 뒤 `df_iqm_agg_cum`을 다이렉트로 결합합니다.
3. 관리자 대시보드 및 DB 메타데이터, 카탈로그 명세를 NCF가 아닌 개별 독립 테이블 구조로 전폭 전환합니다.

**Tech Stack:** Python 3.11, Pandas, Streamlit, SQLite

## Global Constraints

*   **이모지 사용 금지**: 소스 코드 주석, UI, 버튼, 텍스트 등에 유니코드 이모지 사용을 엄격히 금지합니다.
*   **WSL Markdown Link Constraint**: 모든 마크다운 링크 작성 시 절대 리눅스 경로 및 `file:///` 프로토콜을 배제하고 평문 상대 경로만을 사용하여 기재합니다.
*   **함수 및 주석 표준**: Google/NumPy 스타일의 한글 독스트링 구조 및 대분류 헤더 주석(`# * [대분류 - 요약]`) 표준을 엄격히 준수합니다.

---

### Task 1: iqm_df.py 서비스 레이어 분리 리팩토링

**Files:**
*   Modify: `app/service/iqm_df.py:133-204`, `app/service/iqm_df.py:1022-1097`
*   Test: `tests/test_iqm_aggregation_fallback.py`

**Interfaces:**
*   Consumes: `q_iqm_plus.get_query_scrap_from_mes`, `q_iqm_plus.get_query_rework_from_mes`
*   Produces: `get_scrap_by_unit_period`, `get_rework_by_unit_period`

- [ ] **Step 1: get_ncf_by_unit_period 함수 해체 및 개별 수집 함수 구현**
  기존의 `get_ncf_by_unit_period`를 들어내고, 아래와 같이 `get_scrap_by_unit_period`와 `get_rework_by_unit_period` 함수로 분할 선언합니다.
  ```python
  # * [SERVICE - SCRAP 품질 데이터 조회 및 지수 산출]
  def get_scrap_by_unit_period(mcode_list_for_query: str) -> pd.DataFrame:
      """단위 기간별 스크랩(Scrap) 품질 데이터 및 지수를 산출합니다.

      Parameters
      ----------
      mcode_list_for_query : str
          조회 대상 M-Code 목록 조건 문자열

      Returns
      -------
      pd.DataFrame
          스크랩 데이터프레임
      """
      prdt_df = get_client("sqlite", sqlite_db_path="staging").execute(
          q_iqm_plus.get_sqlite_production_volume_iqm_rawdata()
      )

      scrap_df = (
          get_client("databricks")
          .execute(q_iqm_plus.get_query_scrap_from_mes(mcode_list_for_query))
          .rename(columns={"PRD_CD": "MFG_MCODE"})
          .merge(prdt_df, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .assign(
              PPM=lambda df: (
                  df["DFT_QTY"].astype(float) / df["PRDT_QTY"].astype(float) * 1000000
              )
          )
      )
      
      scrap_ncf_df = (
          scrap_df.copy()
          .assign(
              INDEX=lambda df: calculate_quality_index(df["PPM"], "scrap", inverse=True)
          )
          .rename(
              columns={
                  "DFT_QTY": "SCRAP_DFT_QTY",
                  "PPM": "SCRAP_RATE",
                  "INDEX": "SCRAP_INDEX",
              }
          )
          .drop(columns=["CAT"])
      )
      
      return scrap_ncf_df.drop(
          columns=["PLT_CD", "SPEC_CD", "MIN_WRK_DATE", "MASS_PERIOD", "PRDT_QTY"]
      )


  # * [SERVICE - REWORK 품질 데이터 조회 및 지수 산출]
  def get_rework_by_unit_period(mcode_list_for_query: str) -> pd.DataFrame:
      """단위 기간별 재작업(Rework) 품질 데이터 및 지수를 산출합니다.

      Parameters
      ----------
      mcode_list_for_query : str
          조회 대상 M-Code 목록 조건 문자열

      Returns
      -------
      pd.DataFrame
          재작업 데이터프레임
      """
      prdt_df = get_client("sqlite", sqlite_db_path="staging").execute(
          q_iqm_plus.get_sqlite_production_volume_iqm_rawdata()
      )

      rework_df = (
          get_client("databricks")
          .execute(q_iqm_plus.get_query_rework_from_mes(mcode_list_for_query))
          .rename(columns={"PRD_CD": "MFG_MCODE"})
          .merge(prdt_df, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .assign(
              PPM=lambda df: (
                  df["DFT_QTY"].astype(float) / df["PRDT_QTY"].astype(float) * 1000000
              )
          )
      )
      
      rework_ncf_df = (
          rework_df.copy()
          .assign(
              INDEX=lambda df: calculate_quality_index(df["PPM"], "rework", inverse=True)
          )
          .rename(
              columns={
                  "DFT_QTY": "REWORK_DFT_QTY",
                  "PPM": "REWORK_RATE",
                  "INDEX": "REWORK_INDEX",
              }
          )
          .drop(columns=["CAT"])
      )
      
      return rework_ncf_df.drop(
          columns=["PLT_CD", "SPEC_CD", "MIN_WRK_DATE", "MASS_PERIOD", "PRDT_QTY"]
      )
  ```

- [ ] **Step 2: run_iqm_aggregation 집계 및 저장 로직 개편**
  `app/service/iqm_df.py` 파일의 `run_iqm_aggregation` 함수를 수정하여 기존 `df_ncf` 대신 `df_scrap`과 `df_rework`를 개별 획득 및 SQLite에 적재하며, 이를 직접 누적 결합하도록 변경합니다.
  ```python
      # 기존 NCF 적재 폐지 -> Scrap / Rework 각각 SQLite 캐싱 적재
      df_scrap = get_scrap_by_unit_period(mfg_mcode_list_for_query)
      _save_to_sqlite(df_scrap, SQLiteTables.sqlite_staging_iqm_scrap)

      df_rework = get_rework_by_unit_period(mfg_mcode_list_for_query)
      _save_to_sqlite(df_rework, SQLiteTables.sqlite_staging_iqm_rework)

      # 최종 누적 조립 병합부 개편
      df_iqm_agg_cum = (
          df_spec_master.merge(df_prdt, on=["MFG_MCODE"], how="left")
          .merge(df_scrap, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .merge(df_rework, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .merge(df_gt_wt, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .merge(df_uf, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
          .merge(df_rr_result, on=["RR_MCODE", "PERIOD_NAME"], how="left")
          .merge(df_ctl, on=["MFG_MCODE", "PERIOD_NAME"], how="left")
      )
  ```

- [ ] **Step 3: 테스트 및 무결성 검증**
  Staging DB에 적재를 유발하는 aggregate 배치가 문법 및 정적 바인딩 오류 없이 동작하는지 테스트합니다.


### Task 2: SQL 쿼리 클래스 속성 및 DB 메타데이터 동기화

**Files:**
*   Modify: `app/core/sql_builder/query_database.py:203`, `app/core/data_models/database_metadata.json`

**Interfaces:**
*   Consumes: `SQLiteTables`
*   Produces: `sqlite_staging_iqm_ncf` 제거, `sqlite_staging_iqm_scrap` & `sqlite_staging_iqm_rework` 정상화

- [ ] **Step 1: SQL 쿼리 빌더 정적 런타임 속성 제거**
  `app/core/sql_builder/query_database.py`에서 불필요해진 NCF 클래스 속성을 안전하게 제거합니다.
  ```python
  # 제거 대상
  # sqlite_staging_iqm_ncf: ClassVar[str] = "product_audit_ncf"
  ```

- [ ] **Step 2: JSON 메타데이터에서 NCF 제거 및 Scrap-Rework 활성화**
  `app/core/data_models/database_metadata.json` 파일에서 `product_audit_ncf` 테이블 명세 블록을 완전히 도려내어 제거합니다.
  이어서 `product_audit_scrap` 및 `product_audit_rework` 테이블 명세 블록에서 `"category": "! 삭제대기"`로 선언되어 있는 값을 `"category": "Staging Database"`로 변경하여 정상 가동 상태로 반영합니다.


### Task 3: 관리자 수동 집계 대시보드 렌더링 개편

**Files:**
*   Modify: `app/pages/_80_admin/manual_aggregator_page.py:115-125`, `app/pages/_80_admin/manual_aggregator_page.py:150-195`

- [ ] **Step 1: manual_aggregator_page.py 데이터 조회부 개편**
  집계 직후 SQLite staging DB의 원시 세부 테이블 조회 딕셔너리(`results`)를 생성하는 구문에서 `product_audit_ncf` 대신 개별 테이블을 안전하게 읽어오도록 매핑합니다.
  ```python
                  results = {
                      "iqm_plus_agg_cum": master_df,
                      "spec_master": safe_read_sql("product_audit_spec_master", conn),
                      "production": safe_read_sql("product_audit_pdrt", conn),
                      "scrap": safe_read_sql("product_audit_scrap", conn),
                      "rework": safe_read_sql("product_audit_rework", conn),
                      "gt_wt": safe_read_sql("product_audit_gt_wt", conn),
                      "uniformity": safe_read_sql("product_audit_uf", conn),
                      "rr": safe_read_sql("product_audit_rr", conn),
                      "ctl": safe_read_sql("product_audit_ctl", conn),
                  }
  ```

- [ ] **Step 2: UI 탭 세분화 및 데이터프레임 렌더링 세분화**
  결과 화면을 뿌려주는 탭 세그먼트 셀렉터(`tab_names`)에서 `"부적합"` 탭을 완전히 들어내고, `"스크랩 (Scrap)"` 과 `"재작업 (Rework)"` 두 개의 개별 탭으로 구성합니다.
  ```python
                  tab_names = [
                      "최종 집계 (IQM Plus Agg Cum)",
                      "Spec Master",
                      "생산 수량",
                      "스크랩 (Scrap)",
                      "재작업 (Rework)",
                      "GT/WT",
                      "Uniformity",
                      "RR",
                      "CTL",
                  ]
  ```
  그리고 이에 따른 세부 분기 렌더링 영역도 개별적으로 각각 분할 구성합니다.
  ```python
                  elif selected_result_tab == "스크랩 (Scrap)":
                      st.markdown("**단위 기간별 스크랩 수량 및 지수**")
                      st.dataframe(results["scrap"], use_container_width=True, height=500)
                      st.caption(f"총 {len(results['scrap']):,} rows")

                  elif selected_result_tab == "재작업 (Rework)":
                      st.markdown("**단위 기간별 재작업 수량 및 지수**")
                      st.dataframe(results["rework"], use_container_width=True, height=500)
                      st.caption(f"총 {len(results['rework']):,} rows")
  ```


### Task 3.5: 생산 실적(Production Volume) 테이블 '30D', '60D' 데이터 필터링

**Files:**
*   Modify: `app/service/iqm_df.py`

- [ ] **Step 1: get_prdt_by_unit_period 내 '30D', '60D' 데이터 필터링**
  `app/service/iqm_df.py` 파일의 `get_prdt_by_unit_period` 함수 내에서 가져온 생산 실적 DataFrame 중 `PERIOD_NAME` 컬럼의 값이 '30D', '60D'인 행을 소거하도록 필터링 조건을 추가합니다.
  ```python
  def get_prdt_by_unit_period(mcode_list_for_query: str) -> pd.DataFrame:
      df_prdt = (
          get_client("databricks")
          .execute(q_iqm_plus.get_query_prdt_by_unit_period(mcode_list_for_query))
          .rename(columns={"PRD_CD": "MFG_MCODE"})[
              ["MFG_MCODE", "PERIOD_NAME", "MASS_PERIOD", "PRDT_QTY"]
          ]
      )
      return df_prdt[~df_prdt["PERIOD_NAME"].isin(["30D", "60D"])]
  ```


### Task 4: 카탈로그 명세서 갱신 및 데이터베이스 물리 테이블 제거

**Files:**
*   Modify: `app/core/sql_builder/CATALOG.md`, `app/pages/_10_dashboard/iqm_plus_main_prd.md`

- [ ] **Step 1: 명세 문서 내 레거시 NCF 소거 및 Scrap-Rework 정상화**
  * `CATALOG.md` 내에서 `product_audit_ncf` 행을 삭제하고, `product_audit_scrap`과 `product_audit_rework` 행에 붙어 있던 `[주의] 삭제 대기` 문구를 소거하여 정식 활성 캐시 상태로 고쳐 적습니다.
  * `iqm_plus_main_prd.md` 내 SQLite 캐시 목록 중 `product_audit_ncf` 언급을 삭제하고, 개별 스크랩/재작업 수량 캐싱 테이블로 현행화합니다.

- [ ] **Step 2: SQLite staging.db에서 물리 NCF 테이블 드롭 및 pdrt 테이블 '30D', '60D' 데이터 소거**
  SQLite3를 이용하여 `staging.db` 내 불필요해진 `product_audit_ncf` 테이블을 드롭 처리하고, `product_audit_pdrt` 테이블에서 `PERIOD_NAME`이 '30D', '60D'인 물리 데이터를 일회성으로 소거합니다.
  Run command:
  ```bash
  python3 -c "import sqlite3; conn = sqlite3.connect('/home/jumasi/workstation/local.data/database/staging.db'); cursor = conn.cursor(); cursor.execute('DROP TABLE IF EXISTS product_audit_ncf;'); cursor.execute(\"DELETE FROM product_audit_pdrt WHERE PERIOD_NAME IN ('30D', '60D');\"); conn.commit(); conn.close()"
  ```
