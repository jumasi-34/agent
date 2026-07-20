# M-Code List Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** tp_oe_spec_managemnt 테이블과 UI 제어를 기존 다중 스펙 컬럼 구조에서 초단순 마스터 M-Code 리스트 단일 컬럼 구조로 정밀 리팩토링합니다.

**Architecture:** 
1. `ensure_table_exists` 데이터베이스 자가 치유 훅을 갱신하여 m_code와 remark 만으로 이루어진 새로운 단순 스키마 DDL을 구동합니다.
2. `save_spec_changes_transaction` 컨트롤러 로직을 개편하여 m_code의 공백 검증 및 중복 등록 예외(UNIQUE constraint) 상황을 안전하게 롤백(Rollback)하는 트랜잭션 동기화를 보장합니다.
3. `main` UI에서 `col_config`를 `id`, `m_code`, `remark`, `created_at`, `updated_at` 으로 간소화하고 직관적인 설명 툴팁을 마운트합니다.

**Tech Stack:** Streamlit (UI & data_editor), SQLite3 (ops.db), Pytest (TDD)

## Global Constraints
* **Safety Lock**: 기존 프로덕션 소스 코드(app.py 등)를 오염시키지 않으며, 오직 대상 파일([app/pages/_80_admin/tp_oe_monitoring_page.py](app/pages/_80_admin/tp_oe_monitoring_page.py), [tests/test_tp_oe_monitoring.py](tests/test_tp_oe_monitoring.py)) 내에서만 안전 수정을 전개합니다.
* **Emoji Restriction**: 모든 UI 텍스트, 버튼, 알림 및 마크다운 주석 전반에서 일반 유니코드 이모지 사용을 엄격히 배제하고, 오직 Streamlit 기본 Google Material 아이콘 구문 `:material/icon_name:`만 사용합니다.
* **Korean Docstrings**: 소스 코드 내 모든 신규/수정 함수 및 단위 테스트에 작성되는 독스트링 및 주석은 Google/NumPy 스타일의 한국어(Korean)로 일관성 있게 구성합니다.

---

### Task 1: 스키마 마이그레이션 및 자가 치유 훅 개편

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py` (ensure_table_exists 함수 수정)
- Modify: `tests/test_tp_oe_monitoring.py` (테스트 전수 스키마 세팅 수정)

**Interfaces:**
- Consumes: `SQLiteDDL("ops")` 인터페이스
- Produces: `ensure_table_exists()` (tp_oe_spec_managemnt 테이블이 존재하지 않으면 `m_code` UNIQUE 제약을 가진 초단순 스키마로 자동 생성)

- [ ] **Step 1: 테스트용 DDL 셋업 갱신**
  [tests/test_tp_oe_monitoring.py](tests/test_tp_oe_monitoring.py) 내 두 테스트 케이스의 테이블 생성 구문(`CREATE TABLE`)을 신규 스키마 규격으로 전수 갱신합니다.
  ```python
  # 변경 전 기존 다중 컬럼 스키마 대신 아래 신규 초단순 스키마 적용
  CREATE TABLE tp_oe_spec_managemnt (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      m_code TEXT NOT NULL UNIQUE,
      remark TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

- [ ] **Step 2: ensure_table_exists 훅 로직 갱신**
  [app/pages/_80_admin/tp_oe_monitoring_page.py](app/pages/_80_admin/tp_oe_monitoring_page.py) 하위의 DDL 스크립트를 신규 스키마로 대체합니다.
  ```python
  def ensure_table_exists() -> None:
      """tp_oe_spec_managemnt 테이블의 존재 여부를 감지하고, 부재 시 자동 생성합니다."""
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
          CREATE TABLE IF NOT EXISTS tp_oe_spec_managemnt (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              m_code TEXT NOT NULL UNIQUE,
              remark TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
      """)
  ```

- [ ] **Step 3: 테스트 실행하여 컴파일 오류 검증**
  Run: `pytest tests/test_tp_oe_monitoring.py`
  Expected: FAIL (컨트롤러 함수와 테스트 입력 간의 컬럼 개수 불일치 오류 발생)

- [ ] **Step 4: 기존 DB 스키마 리빌딩을 위해 임시 DROP 구동**
  로컬 sqlite 파일 `local.data/db/ops.db` 내에 이미 존재하던 기존 스펙 테이블을 일시 강제 삭제(DROP)하여, 런타임 재생성 훅이 새로운 스키마를 안전하게 바인딩하도록 유도합니다.
  Run: `sqlite3 local.data/db/ops.db "DROP TABLE IF EXISTS tp_oe_spec_managemnt;"`
  Expected: 정상 종료

- [ ] **Step 5: 변경 사항 로컬 커밋**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py tests/test_tp_oe_monitoring.py
  git commit -m "feat: refactor database schema to minimal M-Code list model"
  ```

---

### Task 2: 트랜잭션 동기화 비즈니스 컨트롤러 개편 및 단위 검증

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py` (save_spec_changes_transaction 함수 수정)
- Modify: `tests/test_tp_oe_monitoring.py` (전수 테스트 케이스 입력 데이터 단순화 및 단언문 갱신)

**Interfaces:**
- Consumes: `save_spec_changes_transaction(added_list: List[dict], edited_dict: Dict[str, dict], deleted_list: List[dict])`
- Produces: `Tuple[bool, str]` (트랜잭션 전체 성공 여부 및 결과 메시지 반환)

- [ ] **Step 1: save_spec_changes_transaction 함수 재구현**
  [app/pages/_80_admin/tp_oe_monitoring_page.py](app/pages/_80_admin/tp_oe_monitoring_page.py) 하위의 삽입/수정 쿼리 맵핑을 m_code 기반으로 리팩토링합니다.
  ```python
  def save_spec_changes_transaction(added_list: list, edited_dict: dict, deleted_list: list) -> tuple[bool, str]:
      """M-Code 추가, 수정, 삭제 일괄 변경사항을 단일 트랜잭션 하에서 수동으로 제어 및 보장합니다."""
      dml = SQLiteDML("ops")
      conn = sqlite3.connect(dml.db_path)
      conn.isolation_level = None  # 수동 트랜잭션 오케스트레이션 활성화
      cursor = conn.cursor()
      
      try:
          cursor.execute("BEGIN TRANSACTION;")
          
          # 1. 삭제 (Delete) 처리
          if deleted_list:
              placeholders = ", ".join(["?"] * len(deleted_list))
              delete_query = f"DELETE FROM tp_oe_spec_managemnt WHERE id IN ({placeholders});"
              cursor.execute(delete_query, deleted_list)
              
          # 2. 추가 (Insert) 처리
          for row in added_list:
              m_code = row.get("m_code")
              if not m_code or str(m_code).strip() == "":
                  raise ValueError("M-Code는 필수 입력 항목입니다.")
              
              insert_query = """
                  INSERT INTO tp_oe_spec_managemnt (m_code, remark)
                  VALUES (?, ?);
              """
              cursor.execute(insert_query, (str(m_code).strip(), row.get("remark")))
              
          # 3. 수정 (Update) 처리
          for row_id, changes in edited_dict.items():
              if not changes:
                  continue
              
              set_clauses = []
              params = []
              for col, val in changes.items():
                  if col == "m_code":
                      if not val or str(val).strip() == "":
                          raise ValueError("M-Code는 공백일 수 없습니다.")
                      set_clauses.append("m_code = ?")
                      params.append(str(val).strip())
                  elif col == "remark":
                      set_clauses.append("remark = ?")
                      params.append(val)
              
              if set_clauses:
                  set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                  update_query = f"UPDATE tp_oe_spec_managemnt SET {', '.join(set_clauses)} WHERE id = ?;"
                  params.append(int(row_id))
                  cursor.execute(update_query, tuple(params))
                  
          cursor.execute("COMMIT;")
          return True, "변경사항이 성공적으로 일괄 커밋되었습니다."
          
      except sqlite3.IntegrityError as ie:
          conn.rollback()
          return False, f"데이터 통합 제약 위배로 전체 롤백되었습니다. 중복된 M-Code 입력을 확인하세요."
      except Exception as e:
          conn.rollback()
          return False, f"트랜잭션 오류 발생으로 인해 전체 롤백되었습니다: {str(e)}"
      finally:
          cursor.close()
          conn.close()
  ```

- [ ] **Step 2: test_save_spec_changes_transaction_success 단위 테스트 갱신**
  [tests/test_tp_oe_monitoring.py](tests/test_tp_oe_monitoring.py)의 성공 케이스를 갱신합니다.
  ```python
  def test_save_spec_changes_transaction_success():
      """M-Code 추가, 수정, 삭제 변경사항이 단일 트랜잭션 하에서 무결히 반영되는지 검증합니다."""
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
          DROP TABLE IF EXISTS tp_oe_spec_managemnt;
          CREATE TABLE tp_oe_spec_managemnt (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              m_code TEXT NOT NULL UNIQUE,
              remark TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
          INSERT INTO tp_oe_spec_managemnt (m_code, remark)
          VALUES ('M_SEED_01', 'Initial Seed Code');
      """)
      
      dml = SQLiteDML("ops")
      init_df = dml.fetch_query("SELECT id FROM tp_oe_spec_managemnt LIMIT 1")
      init_id = int(init_df.iloc[0]["id"])
      
      added_list = [
          {"m_code": "M_ADD_99", "remark": "Newly added m-code"}
      ]
      edited_dict = {
          str(init_id): {"remark": "Updated seed description"}
      }
      deleted_list = []
      
      success, message = save_spec_changes_transaction(added_list, edited_dict, deleted_list)
      assert success is True
      
      updated_df = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt ORDER BY id")
      assert len(updated_df) == 2
      
      # 수정 데이터 검증
      seed_row = updated_df[updated_df["id"] == init_id].iloc[0]
      assert seed_row["remark"] == "Updated seed description"
      
      # 추가 데이터 검증
      new_row = updated_df[updated_df["m_code"] == "M_ADD_99"].iloc[0]
      assert new_row["remark"] == "Newly added m-code"
  ```

- [ ] **Step 3: test_save_spec_changes_transaction_rollback_on_failure 단위 테스트 갱신**
  롤백 실패 시나리오 및 중복 제약 테스트를 갱신합니다.
  ```python
  def test_save_spec_changes_transaction_rollback_on_failure():
      """필수 필드 유실 또는 중복된 M-Code 추가 시 일괄 롤백 기능이 성공 보장되는지 검증합니다."""
      ddl = SQLiteDDL("ops")
      ddl.execute_script("""
          DROP TABLE IF EXISTS tp_oe_spec_managemnt;
          CREATE TABLE tp_oe_spec_managemnt (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              m_code TEXT NOT NULL UNIQUE,
              remark TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
          INSERT INTO tp_oe_spec_managemnt (m_code, remark)
          VALUES ('M_SEED_01', 'Initial Seed Code');
      """)
      
      dml = SQLiteDML("ops")
      init_df = dml.fetch_query("SELECT id FROM tp_oe_spec_managemnt LIMIT 1")
      init_id = int(init_df.iloc[0]["id"])
      
      # M-Code가 이미 존재하는 'M_SEED_01'으로 중복 등록하려 하여 무결성 제약을 강제 트리거
      added_list = [
          {"m_code": "M_SEED_01", "remark": "Duplicate code try"}
      ]
      edited_dict = {
          str(init_id): {"remark": "This modification must be rolled back"}
      }
      deleted_list = []
      
      success, message = save_spec_changes_transaction(added_list, edited_dict, deleted_list)
      
      # 검증: 트랜잭션이 실패하고 롤백되어 이전 데이터 상태가 완전히 고수되었는지 확인
      assert success is False
      assert "중복" in message or "롤백" in message
      
      result_df = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt")
      assert len(result_df) == 1
      assert result_df.iloc[0]["m_code"] == "M_SEED_01"
      assert result_df.iloc[0]["remark"] == "Initial Seed Code"
  ```

- [ ] **Step 4: Pytest 테스트 패스 확인**
  Run: `pytest tests/test_tp_oe_monitoring.py -v`
  Expected: `2 passed` (테스트 100% 무결 GREEN 성공)

- [ ] **Step 5: 변경 사항 로컬 커밋**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py tests/test_tp_oe_monitoring.py
  git commit -m "feat: implement transactional M-Code synchronization and pass all integration tests"
  ```

---

### Task 3: Streamlit UI 컬럼 구성 및 설명문 리팩토링

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py` (main 함수 UI 로직 수정)

**Interfaces:**
- Consumes: `st.data_editor` UI 컴포넌트
- Produces: M-Code 데이터 에디팅 테이블 및 세션 가로채기 갱신 UI

- [ ] **Step 1: main() 내 컬럼 바인딩 및 col_config 간소화**
  [app/pages/_80_admin/tp_oe_monitoring_page.py](app/pages/_80_admin/tp_oe_monitoring_page.py) 의 `main()` 함수에서 `col_config` 변수를 M-Code 명세에 부합하도록 슬림하게 갱신하고, 사용자 가이드 마크다운 텍스트를 개선합니다.
  ```python
  # 변경 전의 복잡한 컬럼 스택 대신 아래의 단출한 구성 적용
  st.title("TP OE Monitoring")
  st.markdown("---")
  st.subheader("M-Code Master Dataset")
  st.markdown("관리할 대상 **M-Code 리스트**를 직접 추가, 변경, 삭제할 수 있습니다. 수정한 뒤 하단의 **변경사항 저장** 버튼을 반드시 클릭해 주세요.")

  col_config = {
      "id": st.column_config.NumberColumn("ID", disabled=True, format="%d"),
      "m_code": st.column_config.TextColumn("M-Code (자재코드)", required=True, help="중복되지 않는 고유 M-Code를 기재하십시오."),
      "remark": st.column_config.TextColumn("Remark (비고)", help="해당 M-Code에 대한 세부 메모를 명시하십시오."),
      "created_at": st.column_config.DatetimeColumn("Created At (최초 생성)", disabled=True),
      "updated_at": st.column_config.DatetimeColumn("Updated At (최종 수정)", disabled=True)
  }
  ```

- [ ] **Step 2: 파이썬 구문 이상 유무 컴파일 확인**
  Run: `python -m py_compile app/pages/_80_admin/tp_oe_monitoring_page.py`
  Expected: 정상 성공 (어떠한 Syntax Error도 없어야 함)

- [ ] **Step 3: 테스트 슈트 재구동 및 확인**
  Run: `pytest tests/test_tp_oe_monitoring.py`
  Expected: `2 passed`

- [ ] **Step 4: 변경 사항 최종 로컬 커밋**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py
  git commit -m "feat: simplify Streamlit UI data_editor layout for streamlined M-Code list"
  ```
