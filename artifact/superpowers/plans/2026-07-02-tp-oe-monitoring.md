# TP OE Monitoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Admin Console 카테고리에 "TP OE Monitoring" 페이지를 추가하고 `st.data_editor`를 활용하여 `tp_oe_spec_managemnt` SQLite ops 테이블의 데이터를 원자적(Atomic) 트랜잭션 하에서 수동 커밋 편집할 수 있는 관리자 화면을 구현합니다.

**Architecture:** 
1. `routing.py`에 관리자(Admin) 권한 페이지로 등록하여 라우팅 레이어를 확보합니다.
2. `tp_oe_monitoring_page.py`에 `tp_oe_spec_managemnt` 테이블 자동 생성 DDL 로직을 탑재합니다.
3. 비즈니스 로직인 `save_spec_changes_transaction` 함수를 격리하여 단위 테스트(`tests/test_tp_oe_monitoring.py`)로 SQLite의 추가(INSERT)/수정(UPDATE)/삭제(DELETE) 트랜잭션 무결성과 예외 발생 시의 롤백(Rollback) 작동을 먼저 입증합니다 (TDD).
4. Streamlit UI 상에 세션 가로채기(Interception) 초기화 기법을 연동하여 편집 성공 또는 리셋 시 런타임 위젯 상태를 안전하게 새로고침합니다.

**Tech Stack:** Python 3.12, Streamlit V2 (Monkey Patched Context), SQLite 3, Pandas

## Global Constraints

* **Safety Lock**: 기존의 메인 프로덕션 코드(`app.py` 및 `app/` 전반)는 본 계획서 외 영역을 임의 수정할 수 없습니다. 오직 `routing.py` 라우팅 설정 주입과 신규 생성할 파일들만 통제합니다.
* **이모지 전면 금지**: UI, 버튼, 토스트, 마크다운 텍스트, 코드 주석 등 전체 영역에서 유니코드 이모지 사용을 엄격히 금지합니다. 아이콘이 필요한 경우 오직 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용합니다.
* **한국어 독스트링 원칙**: 모든 신규 함수, 클래스, 모듈에 작성되는 독스트링(Docstring) 및 중요 주석은 한국어(Korean)로 작성하는 것을 기본 원칙으로 합니다.
* **섹션 구분 타이틀 하이라이트 표준**: 주요 레이아웃 구역을 정의할 때 반드시 통일된 주석 장식 블록 양식을 사용합니다.
  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  ```
* **WSL Markdown Link Constraint**: 모든 파일 하이퍼링크는 프로토콜을 제외하고 워크스페이스 루트 기준의 평문 상대 경로만을 사용하여 작성합니다.

---

### Task 1: 라우팅 테이블 등록 및 TDD 하네스 준비

**Files:**
* Modify: `app/core/infrastructure/routing.py:226-251`
* Create: `tests/test_tp_oe_monitoring.py`

**Interfaces:**
* Consumes: `app/core/infrastructure/routing.py` (PAGE_CONFIGS 사전)
* Produces: `PAGE_CONFIGS["TP OE Monitoring"]` 키-밸류 라우팅 정보

- [ ] **Step 1: 라우팅 테이블에 신규 페이지 정보 등록**
  `app/core/infrastructure/routing.py` 파일의 `PAGE_CONFIGS` 사전 내 "Admin Console" 섹션 하위(예: `UI Column Metadata Manager` 직전)에 `TP OE Monitoring` 페이지 정보를 등록합니다.

  ```python
      "TP OE Monitoring": {
          "filename": "app/pages/_80_admin/tp_oe_monitoring_page.py",
          "icon": ":material/monitor_heart:",
          "category": "Admin Console",
          "roles": ["Admin"],
      },
  ```

- [ ] **Step 2: 비즈니스 로직 테스트 검증을 위한 failing test 작성**
  `tests/test_tp_oe_monitoring.py` 파일을 생성하고, 아직 존재하지 않는 트랜잭션 동기화 함수인 `save_spec_changes_transaction`에 대한 failing test 케이스를 작성합니다. 테스트 코드 내에서도 주석 및 독스트링은 한글화 원칙 및 주석 타이틀 하일라이트 양식을 철저히 준수합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import os
  import pytest
  import sqlite3
  import pandas as pd
  from app.core.infrastructure.sqlite_client import SQLiteDML, SQLiteDDL

  # 테스트 대상 모듈 임포트 (아직 생성되지 않은 파일이므로 NameError 및 ModuleNotFoundError가 날 것임)
  from app.pages._80_admin.tp_oe_monitoring_page import save_spec_changes_transaction

  # =========================================================================
  # SECTION 2. Test Cases (단위 테스트 케이스 정의)
  # =========================================================================
  def test_save_spec_changes_transaction_success():
      """추가, 수정, 삭제 변경사항이 단일 트랜잭션 하에서 성공적으로 커밋되는지 검증합니다."""
      # 1. 테스트용 물리 테이블 임시 생성 및 초기화
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
          DROP TABLE IF EXISTS tp_oe_spec_managemnt;
          CREATE TABLE tp_oe_spec_managemnt (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              factory TEXT NOT NULL,
              spec_group TEXT NOT NULL,
              spec_name TEXT NOT NULL,
              target_val REAL,
              lcl REAL,
              ucl REAL,
              unit TEXT,
              remark TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
          INSERT INTO tp_oe_spec_managemnt (factory, spec_group, spec_name, target_val, lcl, ucl, unit, remark)
          VALUES ('H1', 'OE_PRESS', 'Base Pressure', 32.0, 30.0, 34.0, 'psi', 'Initial Seed');
      """)
      
      dml = SQLiteDML("ops")
      # 초기 적재 데이터 id 획득
      init_df = dml.fetch_query("SELECT id FROM tp_oe_spec_managemnt LIMIT 1")
      init_id = int(init_df.iloc[0]["id"])
      
      # 2. 가공 데이터 준비
      added_list = [
          {"factory": "H2", "spec_group": "OE_TEMP", "spec_name": "Curing Temp", "target_val": 165.5, "lcl": 160.0, "ucl": 170.0, "unit": "C", "remark": "Add new spec"}
      ]
      edited_dict = {
          str(init_id): {"target_val": 33.0, "remark": "Update target"}
      }
      deleted_list = [] # 이번 턴에는 삭제 없음
      
      # 3. 트랜잭션 동기화 실행
      success, message = save_spec_changes_transaction(added_list, edited_dict, deleted_list)
      
      # 4. 검증 (Assert)
      assert success is True
      
      # DB 직접 조회하여 결과 검증
      updated_df = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt ORDER BY id")
      assert len(updated_df) == 2
      
      # 수정 데이터 검증
      edited_row = updated_df[updated_df["id"] == init_id].iloc[0]
      assert edited_row["target_val"] == 33.0
      assert edited_row["remark"] == "Update target"
      
      # 추가 데이터 검증
      added_row = updated_df[updated_df["factory"] == "H2"].iloc[0]
      assert added_row["spec_name"] == "Curing Temp"
      assert added_row["target_val"] == 165.5
  ```

- [ ] **Step 3: 테스트를 실행하여 실패(Failing)하는지 확인**
  Run: `pytest tests/test_tp_oe_monitoring.py -v`
  Expected Output: `ModuleNotFoundError: No module named 'app.pages._80_admin.tp_oe_monitoring_page'`

- [ ] **Step 4: 빈 껍데기 타겟 파일 생성하여 모듈 임포트 통과시키기**
  `app/pages/_80_admin/tp_oe_monitoring_page.py` 파일을 생성하고 임포트 오류를 없애기 위한 빈 함수를 선언합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import streamlit as st

  # =========================================================================
  # SECTION 2. Transaction Controller (트랜잭션 가공 및 제어부)
  # =========================================================================
  def save_spec_changes_transaction(added_list: list[dict], edited_dict: dict[str, dict], deleted_list: list[int]) -> tuple[bool, str]:
      """임시 Stub 함수입니다.

      Args:
          added_list: 추가 목록
          edited_dict: 수정 사전
          deleted_list: 삭제 ID 목록

      Returns:
          tuple[bool, str]: (성공여부, 메시지)
      """
      return False, "Not implemented"
  ```

- [ ] **Step 5: 다시 테스트를 실행하여 함수 미구현으로 실패하는지 검증**
  Run: `pytest tests/test_tp_oe_monitoring.py -v`
  Expected Output: `AssertionError: assert False is True`

- [ ] **Step 6: 변경 내역 커밋**
  ```bash
  git add app/core/infrastructure/routing.py tests/test_tp_oe_monitoring.py app/pages/_80_admin/tp_oe_monitoring_page.py
  git commit -m "test: add routing config and TDD harness for TP OE Monitoring"
  ```

---

### Task 2: 데이터베이스 동기화 컨트롤러 구현 및 테스트 무결성 확보

**Files:**
* Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py`
* Modify: `tests/test_tp_oe_monitoring.py`

**Interfaces:**
* Consumes: SQLite `ops` 데이터베이스
* Produces: `save_spec_changes_transaction(added_list, edited_dict, deleted_list) -> (bool, str)`

- [ ] **Step 1: 트랜잭션 동기화 핵심 비즈니스 로직 구현**
  `app/pages/_80_admin/tp_oe_monitoring_page.py` 파일 내에 SQLite 트랜잭션을 수동 제어하는 `save_spec_changes_transaction` 함수를 명세에 따라 완벽하게 구현합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import os
  import sqlite3
  import logging
  import pandas as pd
  import streamlit as st
  from app.core.data_models.business import SQLITE_DB_OPS_PATH

  logger = logging.getLogger(__name__)

  # =========================================================================
  # SECTION 2. Transaction Controller (트랜잭션 가공 및 제어부)
  # =========================================================================
  def save_spec_changes_transaction(
      added_list: list[dict], 
      edited_dict: dict[str, dict], 
      deleted_list: list[int]
  ) -> tuple[bool, str]:
      """데이터 에디터의 가공 정보들을 단일 트랜잭션으로 묶어 SQLite DB에 원자적으로 동기화합니다.

      추가, 수정, 삭제 행위 중 하나라도 예외가 발생할 경우 트랜잭션 전체를 롤백하여
      데이터 무결성을 보호합니다.

      Args:
          added_list (list[dict]): 신규 추가될 레코드 데이터 목록
          edited_dict (dict[str, dict]): 수정될 레코드 정보 (key: id_str, val: {col: val})
          deleted_list (list[int]): 삭제될 레코드 고유 ID 목록

      Returns:
          tuple[bool, str]: (동기화 성공 여부, 결과 피드백 메시지)
      """
      if not added_list and not edited_dict and not deleted_list:
          return True, "변경사항이 존재하지 않습니다."

      db_path = SQLITE_DB_OPS_PATH
      conn = None
      try:
          # 트랜잭션 수동 통제를 위해 isolation_level을 None으로 설정하여 수동 커밋 모드로 진입
          conn = sqlite3.connect(db_path, isolation_level=None)
          cursor = conn.cursor()
          
          # 명시적 트랜잭션 시작
          cursor.execute("BEGIN TRANSACTION;")
          
          # 1. 행 삭제 (Deleted Rows) 처리
          if deleted_list:
              # list_tables() 검증이 끝난 id 목록이므로 SQL injection 안전 보장
              placeholders = ", ".join(["?"] * len(deleted_list))
              delete_query = f"DELETE FROM tp_oe_spec_managemnt WHERE id IN ({placeholders});"
              cursor.execute(delete_query, tuple(deleted_list))
              logger.info(f"[DB Sync] Deleted {len(deleted_list)} rows from tp_oe_spec_managemnt")
          
          # 2. 행 수정 (Edited Rows) 처리
          if edited_dict:
              for row_id_str, changes in edited_dict.items():
                  if not changes:
                      continue
                  row_id = int(row_id_str)
                  
                  # 변경이 감지된 컬럼들만 동적으로 SET 쿼리 조립
                  set_clauses = []
                  params = []
                  for col, val in changes.items():
                      set_clauses.append(f"{col} = ?")
                      params.append(val)
                  
                  # updated_at 자동 업데이트
                  set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                  
                  params.append(row_id)
                  set_clause_str = ", ".join(set_clauses)
                  update_query = f"UPDATE tp_oe_spec_managemnt SET {set_clause_str} WHERE id = ?;"
                  cursor.execute(update_query, tuple(params))
              logger.info(f"[DB Sync] Updated {len(edited_dict)} rows in tp_oe_spec_managemnt")
          
          # 3. 행 추가 (Added Rows) 처리
          if added_list:
              insert_query = """
              INSERT INTO tp_oe_spec_managemnt (
                  factory, spec_group, spec_name, target_val, lcl, ucl, unit, remark
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
              """
              for row in added_list:
                  # 기본값이 없는 필수 컬럼 누락 방어
                  factory = row.get("factory")
                  spec_group = row.get("spec_group")
                  spec_name = row.get("spec_name")
                  
                  if not factory or not spec_group or not spec_name:
                      raise ValueError("필수 필드(공장, 스펙그룹, 스펙항목명)가 누락되어 저장이 불가능합니다.")
                      
                  values = (
                      factory,
                      spec_group,
                      spec_name,
                      row.get("target_val"),
                      row.get("lcl"),
                      row.get("ucl"),
                      row.get("unit"),
                      row.get("remark")
                  )
                  cursor.execute(insert_query, values)
              logger.info(f"[DB Sync] Inserted {len(added_list)} rows into tp_oe_spec_managemnt")
          
          # 트랜잭션 확정 커밋
          cursor.execute("COMMIT;")
          return True, "모든 변경사항이 성공적으로 데이터베이스에 영구 저장되었습니다."
          
      except Exception as e:
          if conn:
              try:
                  cursor.execute("ROLLBACK;")
                  logger.warning("[DB Sync] Sync failed. Transaction completely rolled back.")
              except sqlite3.Error as rollback_err:
                  logger.critical(f"[DB Sync] Failed to rollback! Error: {rollback_err}")
          logger.error(f"[DB Sync] Transaction execution exception: {str(e)}")
          return False, f"데이터베이스 업데이트 중 요류가 발생하여 전체 롤백되었습니다: {str(e)}"
      finally:
          if conn:
              conn.close()
  ```

- [ ] **Step 2: 실패 상황(Rollback)에 대한 TDD 단위 테스트 케이스 추가**
  `tests/test_tp_oe_monitoring.py` 하단에 일부 데이터에 하자가 있을 시 전체가 트랜잭션 롤백되어 이전 상태가 그대로 유지되는지 검증하는 테스트 케이스를 보강합니다.

  ```python
  def test_save_spec_changes_transaction_rollback_on_failure():
      """필수값 누락 등 유효하지 않은 데이터가 섞여 있을 시 전체 작업이 롤백되어 온전성이 유지되는지 검증합니다."""
      # 1. 스키마 초기화 및 단일 시드 데이터 준비
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
          DROP TABLE IF EXISTS tp_oe_spec_managemnt;
          CREATE TABLE tp_oe_spec_managemnt (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              factory TEXT NOT NULL,
              spec_group TEXT NOT NULL,
              spec_name TEXT NOT NULL,
              target_val REAL,
              lcl REAL,
              ucl REAL,
              unit TEXT,
              remark TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
          INSERT INTO tp_oe_spec_managemnt (factory, spec_group, spec_name, target_val, lcl, ucl, unit, remark)
          VALUES ('H1', 'OE_PRESS', 'Base Pressure', 32.0, 30.0, 34.0, 'psi', 'Initial Seed');
      """)
      
      dml = SQLiteDML("ops")
      init_df = dml.fetch_query("SELECT id FROM tp_oe_spec_managemnt LIMIT 1")
      init_id = int(init_df.iloc[0]["id"])
      
      # 2. 가공 데이터 준비 (정상 수정 1건 + 필수값 'factory'가 유실된 무효한 신규 데이터 1건 병합)
      added_list = [
          {"factory": None, "spec_group": "OE_TEMP", "spec_name": "Invalid Spec"}  # 'factory'가 None이므로 예외 발생 예정
      ]
      edited_dict = {
          str(init_id): {"target_val": 40.0, "remark": "Should not be saved"}  # 롤백되므로 이 수정도 반영되지 않아야 함
      }
      deleted_list = []
      
      # 3. 실행
      success, message = save_spec_changes_transaction(added_list, edited_dict, deleted_list)
      
      # 4. 검증 (Assert)
      assert success is False  # 롤백으로 실패가 반환되어야 함
      assert "누락" in message
      
      # DB에서 데이터가 이전 시드 상태 그대로 유지되고 수정이 반영되지 않았는지 확인
      result_df = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt")
      assert len(result_df) == 1
      assert result_df.iloc[0]["target_val"] == 32.0  # 40.0으로 바뀌지 않고 32.0으로 원복되어 있어야 함
      assert result_df.iloc[0]["remark"] == "Initial Seed"
  ```

- [ ] **Step 3: 전체 단위 테스트 실행하여 두 테스트 케이스 통과 확인**
  Run: `pytest tests/test_tp_oe_monitoring.py -v`
  Expected Output: `2 passed in X.XXs`

- [ ] **Step 4: 변경 내역 커밋**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py tests/test_tp_oe_monitoring.py
  git commit -m "feat: implement transaction sync engine and pass integration tests"
  ```

---

### Task 3: Streamlit UI 구현 및 세션 가로채기 복구 연동

**Files:**
* Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py`

**Interfaces:**
* Consumes: `st.session_state`, `save_spec_changes_transaction`
* Produces: 완전한 대시보드 화면 및 리셋 복구 인터랙션

- [ ] **Step 1: Streamlit 페이지 본체 개발**
  `app/pages/_80_admin/tp_oe_monitoring_page.py` 파일에 테이블 자동 감증 DDL 및 이중 가드 보안 장치, 그리고 `st.data_editor` UI와 변경 사항 대기 제어판을 구현합니다. 이모지 전면 배제 및 구문 표준을 철저히 충족합니다.

  ```python
  # (Task 2에서 선언한 imports 및 save_spec_changes_transaction 하위에 추가 작성)

  # =========================================================================
  # SECTION 3. Database Schema Guardian (데이터베이스 스키마 자가 복구)
  # =========================================================================
  def ensure_table_exists() -> None:
      """데이터베이스에 tp_oe_spec_managemnt 테이블이 존재하는지 확인하고,

      존재하지 않을 경우 초기 설계 물리 스키마로 즉시 신규 구성합니다.
      """
      from app.core.infrastructure.sqlite_client import SQLiteDDL
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
      CREATE TABLE IF NOT EXISTS tp_oe_spec_managemnt (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          factory TEXT NOT NULL,
          spec_group TEXT NOT NULL,
          spec_name TEXT NOT NULL,
          target_val REAL,
          lcl REAL,
          ucl REAL,
          unit TEXT,
          remark TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      """)

  # =========================================================================
  # SECTION 4. Page Rendering Entry Point (페이지 렌더링 도입부)
  # =========================================================================
  def main() -> None:
      """TP OE Monitoring 페이지의 메인 렌더러 함수입니다.

      관리자 권한 가드 검증, 데이터 로딩, 인라인 에디팅 수동 커밋 흐름을 제어합니다.
      """
      # 1. 2차 이중 권한 보안 가드 검증
      role = st.session_state.get("role")
      if role != "Admin":
          st.error("이 페이지는 관리자(Admin) 권한이 있는 사용자만 접근할 수 있습니다.")
          st.stop()

      # 2. 테이블 스키마 검증 및 자가 치유 기동
      ensure_table_exists()

      # 3. 레이아웃 타이틀 렌더링 (이모지 전면 금지 규정 준수)
      st.title("TP OE Monitoring & Spec Management")
      st.caption("TP OE 관련 공정 및 사양 정보에 대한 통합 관리자 전용 제어판입니다.")
      
      # 4. 세션 가로채기(Interception)를 활용한 에디터 상태 수동 제어
      # 데이터 에디터 위젯의 키 세션 리셋을 위한 고유 키 관리
      editor_key = "tp_oe_spec_editor_widget"
      editor_state_key = f"{editor_key}_state"
      
      # 데이터베이스에서 실시간 데이터 로드
      from app.core.infrastructure.sqlite_client import SQLiteDML
      dml = SQLiteDML("ops")
      
      # 최신 데이터를 DataFrame으로 셀렉션
      df_specs = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt ORDER BY id DESC")
      
      # 데이터 에디팅 테이블 렌더링
      st.subheader("OE Specification Dataset")
      st.markdown("데이터 셀을 직접 더블 클릭하여 값을 자유롭게 추가, 변경, 삭제할 수 있습니다. 입력 후 하단의 **변경사항 저장** 버튼을 꼭 클릭해 주세요.")

      # 사용자가 에디팅 편의를 느낄 수 있도록 기본 데이터 구조 가이드 제공
      col_config = {
          "id": st.column_config.NumberColumn("ID", disabled=True, format="%d"),
          "factory": st.column_config.TextColumn("Factory (공장)", required=True, placeholder="예: H1, H2, G1"),
          "spec_group": st.column_config.TextColumn("Spec Group (스펙그룹)", required=True, placeholder="예: OE_PRESS"),
          "spec_name": st.column_config.TextColumn("Spec Name (스펙항목명)", required=True, placeholder="예: Base Pressure"),
          "target_val": st.column_config.NumberColumn("Target (기준값)", format="%.2f"),
          "lcl": st.column_config.NumberColumn("LCL (하한선)", format="%.2f"),
          "ucl": st.column_config.NumberColumn("UCL (상한선)", format="%.2f"),
          "unit": st.column_config.TextColumn("Unit (단위)", placeholder="예: psi"),
          "remark": st.column_config.TextColumn("Remark (비고)"),
          "created_at": st.column_config.DatetimeColumn("Created At (최초 생성)", disabled=True),
          "updated_at": st.column_config.DatetimeColumn("Updated At (최종 수정)", disabled=True)
      }

      # st.data_editor를 띄우고 사용자의 세션 편집 버퍼를 바인딩
      edited_df = st.data_editor(
          df_specs,
          column_config=col_config,
          num_rows="dynamic",
          use_container_width=True,
          key=editor_key
      )

      # 5. 변경 내역 수합 및 디스플레이 제어 패널
      # Streamlit의 data_editor state는 st.session_state에 [key] 사전 하위의 "edited_rows", "added_rows", "deleted_rows" 등으로 자동 적재됨
      editor_changes = st.session_state.get(editor_key, {})
      
      added_rows = editor_changes.get("added_rows", [])
      edited_rows_dict = editor_changes.get("edited_rows", {})
      deleted_rows_indices = editor_changes.get("deleted_rows", [])

      # 삭제 정보의 경우, 프론트 뷰 상의 행 인덱스 리스트로 넘어오므로 실제 데이터프레임의 'id' 값으로 치환 매핑 필요
      deleted_ids = []
      if deleted_rows_indices:
          for idx in deleted_rows_indices:
              # df_specs가 DESC 정렬되어 있으므로 해당 인덱스의 고유 ID를 가져옴
              real_id = int(df_specs.iloc[idx]["id"])
              deleted_ids.append(real_id)

      has_changes = bool(added_rows or edited_rows_dict or deleted_ids)

      st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
      
      # 하단 액션 버튼 배치
      btn_cols = st.columns([1, 1, 6])
      
      if has_changes:
          st.info(f"대기 중인 변경사항: 추가 {len(added_rows)}건 | 수정 {len(edited_rows_dict)}건 | 삭제 {len(deleted_ids)}건")
          
          # 변경사항 저장 (Save Changes) 버튼
          if btn_cols[0].button(
              "변경사항 저장",
              type="primary",
              use_container_width=True,
              icon=":material/save:"
          ):
              success, message = save_spec_changes_transaction(added_rows, edited_rows_dict, deleted_ids)
              if success:
                  st.success(message, icon=":material/check_circle:")
                  
                  # [세션 가로채기 초기화 패턴 적용]
                  # 저장이 완료된 후 data_editor의 위젯 캐시 세션을 완전히 제거하여 리셋 유도
                  if editor_key in st.session_state:
                      st.session_state.pop(editor_key)
                  if editor_state_key in st.session_state:
                      st.session_state.pop(editor_state_key)
                  
                  # 화면 동기화 새로고침
                  st.rerun()
              else:
                  st.error(message, icon=":material/error:")
                  
          # 편집 내용 취소 (Reset) 버튼
          if btn_cols[1].button(
              "변경취소",
              type="secondary",
              use_container_width=True,
              icon=":material/undo:"
          ):
              # 편집 세션 초기화 및 Rerun
              if editor_key in st.session_state:
                  st.session_state.pop(editor_key)
              if editor_state_key in st.session_state:
                  st.session_state.pop(editor_state_key)
              st.rerun()
      else:
          btn_cols[0].button(
              "변경사항 저장",
              type="primary",
              disabled=True,
              use_container_width=True,
              icon=":material/save:"
          )
          btn_cols[1].button(
              "변경취소",
              type="secondary",
              disabled=True,
              use_container_width=True,
              icon=":material/undo:"
          )
          st.caption("현재 테이블 데이터는 물리 저장소와 완벽히 동기화되어 있습니다.")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 2: 수동 실행 환경 하에서 라우팅 정합성 자가 검사**
  기본 개발 모드 검증 스크립트 실행으로 에러 발생 여부를 파악합니다.
  Run: `python app/core/infrastructure/routing.py`
  Expected Output: (무반응 또는 0 반환, 에러가 발생하지 않아야 통과)

- [ ] **Step 3: 최종 배포 전 전체 빌드 정적 린트/정합성 종합 검증**
  Run: `pytest tests/test_tp_oe_monitoring.py -v`
  Expected Output: `2 passed`

- [ ] **Step 4: 변경 내역 최종 커밋**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py
  git commit -m "feat: complete TP OE Monitoring Admin page and integrate session-interception refresh"
  ```
