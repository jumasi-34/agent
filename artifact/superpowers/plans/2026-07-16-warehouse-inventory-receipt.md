# Warehouse Inventory Receipt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 창고재고 입고 현황 조회(M-Code 기준) 기능을 추가하여 Admin 권한을 가진 사용자가 특정 기간의 입고 현황을 한글 메타데이터와 함께 세련되게 조회할 수 있는 신규 화면 및 데이터 파이프라인을 구축합니다.

**Architecture:** M-Code 기반의 창고재고 입고 현황을 Databricks SQL 쿼리를 통해 효율적으로 집계하고, Pandas 서비스 전처리 및 Streamlit UI 페이지로 연결하는 고성능 격리 아키텍처(L3-query, L3-service, L3-dashboard)를 따릅니다.

**Tech Stack:** Python 3.10+, Pandas, Streamlit, Databricks SQL, Pytest (Unit Testing)

## Global Constraints

* **Safety Lock (기존 소스 코드 변경 최소화)**: 기존 파일의 변경은 상수 및 파라미터 등록에 국한하며, 신규 로직은 격리된 독립 신규 모듈(`q_warehouse_receipt.py`, `warehouse_receipt_df.py`, `warehouse_receipt_page.py`)에 안전하게 전담 구현합니다.
* **UI 규칙 및 이모지 사용 전면 금지**: Streamlit UI 페이지, 마크다운 텍스트, 버튼, 토스트, 주석 등 어떠한 곳에서도 일반 유니코드 이모지(별, 느낌표 등)를 사용할 수 없습니다. 오직 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용합니다.
* **한글 AS Alias 사용 전면 금지**: SQL 내부에서 디스플레이용 한글 `AS "별칭"` 선언을 엄격히 금지하며, 한글 레이블 매핑은 UI 단의 동적 메타데이터 헬퍼(`get_dynamic_column_configs`)에 위임합니다.
* **WSL Markdown Link Constraint**: 모든 파일 하이퍼링크는 프로토콜(`file:///`)을 제외하고 워크스페이스 루트 기준의 평문 상대 경로만을 사용하여 작성해야 합니다.

---

### Task 1: Databricks 테이블 상수 등록 및 SQL 필터 파라미터 데이터클래스 생성

**Files:**
* Modify: `app/core/sql_builder/query_database.py` (라인 56-100 부근, `DatabricksTables` 클래스 내에 테이블 등록)
* Modify: `app/core/data_models/parameters.py` (파일 끝에 `WarehouseReceiptParams` 클래스 등록)
* Test: `tests/test_parameters_and_tables.py` (신규 독립 테스트 파일 생성)

**Interfaces:**
* Consumes: None (기초 모듈)
* Produces:
  * `DatabricksTables.gmes_inv_warehouse_receipt` -> `str`
  * `WarehouseReceiptParams` -> Dataclass

- [ ] **Step 1: Write the failing test**

`tests/test_parameters_and_tables.py` 파일을 생성하여 `WarehouseReceiptParams`와 `DatabricksTables.gmes_inv_warehouse_receipt`가 정의되었는지와 구조를 검증하는 테스트를 작성합니다.

```python
# -*- coding: utf-8 -*-
import pytest
from app.core.sql_builder.query_database import DatabricksTables

def test_gmes_inv_warehouse_receipt_table_registered():
    # DatabricksTables 클래스에 gmes_inv_warehouse_receipt 상수가 올바르게 정의되어 있는지 검증합니다.
    assert hasattr(DatabricksTables, "gmes_inv_warehouse_receipt")
    assert DatabricksTables.gmes_inv_warehouse_receipt == "hkt_dw.inventory.inv_f_linvtr110"

def test_warehouse_receipt_params_structure():
    # WarehouseReceiptParams 데이터클래스가 정상적으로 정의되어 있고 올바른 필드를 가졌는지 검증합니다.
    from app.core.data_models.parameters import WarehouseReceiptParams
    params = WarehouseReceiptParams(
        plant_list=["TP"],
        mcode_list=["1033649"],
        start_date="2026-01-01",
        end_date="2026-01-31"
    )
    assert params.plant_list == ["TP"]
    assert params.mcode_list == ["1033649"]
    assert params.start_date == "2026-01-01"
    assert params.end_date == "2026-01-31"
    assert params.view_mode == "rawdata"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_parameters_and_tables.py -v`
Expected: FAIL (ImportError 혹은 AttributeError 발생)

- [ ] **Step 3: Write minimal implementation**

`app/core/sql_builder/query_database.py` 파일의 `DatabricksTables` 클래스 내부에 다음 코드를 추가합니다:
```python
    gmes_inv_warehouse_receipt: ClassVar[str] = "hkt_dw.inventory.inv_f_linvtr110"  # [GMES] 창고재고 입고 현황 이력 정보
```

`app/core/data_models/parameters.py` 파일 하단에 다음 코드를 추가합니다:
```python
@dataclass
class WarehouseReceiptParams:
    """[GMES] 창고재고 입고 현황 조회 처리용 필터 파라미터 구조체"""
    plant_list: str | list[str] | None = None
    mcode_list: str | list[str] | None = None
    start_date: str | None = None
    end_date: str | None = None
    view_mode: Literal["rawdata"] = "rawdata"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_parameters_and_tables.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/core/sql_builder/query_database.py app/core/data_models/parameters.py tests/test_parameters_and_tables.py
git commit -m "feat: register databricks table constant and parameter dataclass for warehouse inventory receipt"
```

---

### Task 2: 쿼리 어셈블러 레이어 개발

**Files:**
* Create: `app/queries/q_warehouse_receipt.py` (신규 생성)
* Test: `tests/test_q_warehouse_receipt.py` (신규 생성)

**Interfaces:**
* Consumes:
  * `WarehouseReceiptParams` (from `app.core.data_models.parameters`)
  * `DatabricksTables` (from `app.core.sql_builder.query_database`)
* Produces:
  * `get_warehouse_receipt_query(params: WarehouseReceiptParams) -> str`

- [ ] **Step 1: Write the failing test**

`tests/test_q_warehouse_receipt.py` 파일을 생성하여 `get_warehouse_receipt_query` 함수의 쿼리 빌드 결과가 조건 필터에 맞춰 정상 작동하는지 검증하는 테스트를 작성합니다.

```python
# -*- coding: utf-8 -*-
import pytest
from app.core.data_models.parameters import WarehouseReceiptParams

def test_get_warehouse_receipt_query_generation_and_filters():
    # get_warehouse_receipt_query가 파라미터에 따라 적절한 SQL 쿼리 문자열을 조립해 내는지 검증합니다.
    from app.queries.q_warehouse_receipt import get_warehouse_receipt_query
    
    params = WarehouseReceiptParams(
        plant_list=["TP"],
        mcode_list=["1033649", "1033647"],
        start_date="2026-05-01",
        end_date="2026-05-31"
    )
    
    query = get_warehouse_receipt_query(params)
    
    # 1. 반환 타입 검증
    assert isinstance(query, str)
    
    # 2. 필수 테이블명 바인딩 검증
    assert "hkt_dw.inventory.inv_f_linvtr110" in query
    
    # 3. CASE WHEN 출하구분 변환 로직 탑재 검증 (한글 이모지 배제)
    assert "CASE t.SHP_FG" in query
    assert "WHEN 'O' THEN 'OEM'" in query
    assert "WHEN 'R' THEN 'REP'" in query
    assert "WHEN 'T' THEN 'OE Fitment'" in query
    assert "ELSE 'etc'" in query
    assert "AS RCPT_FG_NM" in query
    
    # 4. 동적 Where 조건 생성 검증
    assert "t.PLT_CD IN ('TP')" in query
    assert "t.PRD_CD IN ('1033649', '1033647')" in query
    assert "t.RCPT_DATE BETWEEN '2026-05-01' AND '2026-05-31'" in query
    
    # 5. 한글 AS Alias 사용 전면 금지 규칙 검증 (한글 별칭 문자열 "AS `별칭`" 등 차단)
    import re
    assert not re.search(r"AS\s+[`'\"][\uac00-\ud7a3]+", query, re.IGNORECASE)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_q_warehouse_receipt.py -v`
Expected: FAIL (ModuleNotFoundError 혹은 ImportError)

- [ ] **Step 3: Write minimal implementation**

`app/queries/q_warehouse_receipt.py` 파일을 생성하여 다음과 같이 쿼리 조립 코드를 작성합니다:

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
from app.core.data_models.parameters import WarehouseReceiptParams
from app.core.sql_builder.query_database import DatabricksTables
from app.core.sql_builder.filters import QueryFilter
from app.core.sql_builder.query_helper import log_query_assembly

# =========================================================================
# SECTION 2. Query Builders (SQL 쿼리 동적 조립 함수)
# =========================================================================

# * [WAREHOUSE - 창고재고 입고 현황 조회 쿼리 조립]
@log_query_assembly
def get_warehouse_receipt_query(params: WarehouseReceiptParams) -> str:
    """Databricks DWH 환경에서 M-Code 기준의 창고재고 입고 현황 데이터를 조회하는 순수 SQL을 생성합니다.

    Parameters
    ----------
    params : WarehouseReceiptParams
        공장, M-Code, 날짜 범위가 바인딩된 파라미터 객체

    Returns
    -------
    str
        동적으로 조립된 Databricks SQL 쿼리 문자열
    """
    where_clause = QueryFilter.build_where([
        QueryFilter.where_in("t.PLT_CD", params.plant_list),
        QueryFilter.where_in("t.PRD_CD", params.mcode_list),
        QueryFilter.where_date_between(params.start_date, params.end_date, "t.RCPT_DATE")
    ])

    query = f"""--sql
        SELECT
            t.PLT_CD                                       AS PLANT_CODE
          , t.PRD_CD                                       AS MCODE
          , t.SPEC_CD                                      AS SPEC_CD
          , t.RCPT_DATE                                    AS RCPT_DATE
          , t.SHP_FG                                       AS SHP_FG
          , CASE t.SHP_FG
                WHEN 'O' THEN 'OEM'
                WHEN 'R' THEN 'REP'
                WHEN 'T' THEN 'OE Fitment'
                WHEN 'F' THEN 'EXP OE'
                WHEN 'E' THEN 'EXP RE'
                WHEN 'S' THEN 'Special'
                WHEN 'P' THEN '미정의'
                WHEN 'X' THEN '미정의'
                ELSE 'etc'
            END                                            AS RCPT_FG_NM
          , SUM(t.RCPT_QTY)                                AS RCPT_QTY
        FROM {DatabricksTables.gmes_inv_warehouse_receipt} t
        {where_clause}
        GROUP BY 
            t.PLT_CD, 
            t.PRD_CD, 
            t.SPEC_CD, 
            t.RCPT_DATE, 
            t.SHP_FG,
            CASE t.SHP_FG
                WHEN 'O' THEN 'OEM'
                WHEN 'R' THEN 'REP'
                WHEN 'T' THEN 'OE Fitment'
                WHEN 'F' THEN 'EXP OE'
                WHEN 'E' THEN 'EXP RE'
                WHEN 'S' THEN 'Special'
                WHEN 'P' THEN '미정의'
                WHEN 'X' THEN '미정의'
                ELSE 'etc'
            END
    """
    return query
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_q_warehouse_receipt.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/queries/q_warehouse_receipt.py tests/test_q_warehouse_receipt.py
git commit -m "feat: add warehouse inventory receipt sql assembly layer"
```

---

### Task 3: 비즈니스 서비스 레이어 개발 (전처리 & 캐싱)

**Files:**
* Create: `app/service/warehouse_receipt_df.py` (신규 생성)
* Test: `tests/test_warehouse_receipt_service.py` (신규 생성)

**Interfaces:**
* Consumes:
  * `WarehouseReceiptParams` (from `app.core.data_models.parameters`)
  * `get_warehouse_receipt_query` (from `app.queries.q_warehouse_receipt`)
* Produces:
  * `preprocessing_warehouse_receipt_rawdata(params: WarehouseReceiptParams) -> pd.DataFrame`

- [ ] **Step 1: Write the failing test**

`tests/test_warehouse_receipt_service.py` 파일을 생성하여 `preprocessing_warehouse_receipt_rawdata` 함수가 실제 DB 커넥션을 성립하지 않는 Mocking 환경에서 데이터를 정상 처리(타입 변환 및 캐싱 검증)하는지 테스트를 작성합니다.

```python
# -*- coding: utf-8 -*-
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from app.core.data_models.parameters import WarehouseReceiptParams

def test_preprocessing_warehouse_receipt_service_flow():
    # DB 쿼리 실행 후 Pandas 데이터를 정제하고, inplace 변조가 없는지 검증합니다.
    from app.service.warehouse_receipt_df import preprocessing_warehouse_receipt_rawdata
    
    mock_df_raw = pd.DataFrame([
        {"PLANT_CODE": "TP", "MCODE": "1033649", "SPEC_CD": "205/55R16", "RCPT_DATE": "20260515", "SHP_FG": "O", "RCPT_FG_NM": "OEM", "RCPT_QTY": "150"},
        {"PLANT_CODE": "TP", "MCODE": "1033647", "SPEC_CD": "215/60R17", "RCPT_DATE": "20260516", "SHP_FG": "R", "RCPT_FG_NM": "REP", "RCPT_QTY": None}
    ])
    
    params = WarehouseReceiptParams(
        plant_list=["TP"],
        mcode_list=["1033649"],
        start_date="2026-05-01",
        end_date="2026-05-31"
    )
    
    # DatabricksClient 객체를 모킹하여 쿼리 결과를 바인딩합니다.
    with patch("app.service.warehouse_receipt_df.DatabricksClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.execute_query.return_value = mock_df_raw
        
        df_processed = preprocessing_warehouse_receipt_rawdata(params)
        
        # 1. 빈 데이터프레임이 아님을 검증
        assert not df_processed.empty
        
        # 2. 데이터 타입 복구 및 결측치 대체(0) 검증
        assert df_processed.loc[0, "RCPT_QTY"] == 150
        assert df_processed.loc[1, "RCPT_QTY"] == 0  # None -> 0
        assert df_processed["RCPT_QTY"].dtype == "int64" or df_processed["RCPT_QTY"].dtype == "int32"
        
        # 3. 입고일자(RCPT_DATE)의 string 타입 정화 검증
        assert df_processed["RCPT_DATE"].dtype == object or df_processed["RCPT_DATE"].dtype == "O"
        
        # 4. 원시 모킹 데이터프레임이 훼손(변조)되지 않았는지 검증 (inplace 변조 전면 방지)
        assert mock_df_raw.loc[1, "RCPT_QTY"] is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_warehouse_receipt_service.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

`app/service/warehouse_receipt_df.py` 파일을 생성하고 다음과 같이 데이터 서비스 코드를 작성합니다:

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import pandas as pd
import streamlit as st
from app.core.infrastructure.databricks_client import DatabricksClient
from app.core.data_models.parameters import WarehouseReceiptParams
from app.queries.q_warehouse_receipt import get_warehouse_receipt_query

# =========================================================================
# SECTION 2. Preprocessing Services (비즈니스 데이터 전처리 서비스)
# =========================================================================

# * [WAREHOUSE - 창고재고 입고 현황 원시 데이터 수집 및 1차 전처리]
@st.cache_data(ttl="1h")
def preprocessing_warehouse_receipt_rawdata(params: WarehouseReceiptParams) -> pd.DataFrame:
    """Databricks Client를 사용해 창고재고 입고 현황을 쿼리하고, 
    인플레이스 변조 없이 Pandas 데이터프레임 타입 정제 및 결측치 처리를 수행합니다.

    Parameters
    ----------
    params : WarehouseReceiptParams
        조회 검색 필터 조건 파라미터

    Returns
    -------
    pd.DataFrame
        정제된 입고 현황 데이터프레임
    """
    query = get_warehouse_receipt_query(params)
    
    # Databricks DB 실행 및 원시 DataFrame 수집
    client = DatabricksClient()
    df_raw = client.execute_query(query)
    
    if df_raw is None or df_raw.empty:
        return pd.DataFrame(columns=["PLANT_CODE", "MCODE", "SPEC_CD", "RCPT_DATE", "SHP_FG", "RCPT_FG_NM", "RCPT_QTY"])
        
    # 타입 교정 및 인플레이스 가공 금지 규칙 준수
    df = df_raw.copy()
    df["RCPT_QTY"] = pd.to_numeric(df["RCPT_QTY"], errors="coerce").fillna(0).astype("int64")
    df["RCPT_DATE"] = df["RCPT_DATE"].astype(str)
    
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_warehouse_receipt_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/service/warehouse_receipt_df.py tests/test_warehouse_receipt_service.py
git commit -m "feat: add business service layer with caching and dataframe cleansing for warehouse inventory receipt"
```

---

### Task 4: 동적 한글 매핑 메타데이터 등록

**Files:**
* Modify: `local.data/query/query_metadata.json` (가상 테이블 `"gmes_inv_warehouse_receipt"` 정의 추가)
* Test: `tests/test_query_metadata.py` (신규 생성)

**Interfaces:**
* Consumes: None (정적 메타데이터 파일)
* Produces:
  * `get_dynamic_column_configs("gmes_inv_warehouse_receipt")` -> dict with Column Configs

- [ ] **Step 1: Write the failing test**

`tests/test_query_metadata.py` 파일을 생성하여 `get_dynamic_column_configs` 모듈을 통과했을 때 신규 등록한 가상 테이블 명세서에 의거해 한글 디스플레이 레이블과 도움말이 정상 매핑되는지 검증하는 테스트를 작성합니다.

```python
# -*- coding: utf-8 -*-
import pytest
import streamlit as st
from app.core.design_system.column_config import get_dynamic_column_configs

def test_warehouse_receipt_dynamic_column_configs_mapping():
    # get_dynamic_column_configs가 gmes_inv_warehouse_receipt 키를 정확히 읽어 한글 헤더를 빌드하는지 검증합니다.
    df_columns = ["PLANT_CODE", "MCODE", "SPEC_CD", "RCPT_DATE", "SHP_FG", "RCPT_FG_NM", "RCPT_QTY"]
    
    configs = get_dynamic_column_configs("gmes_inv_warehouse_receipt", df_columns=df_columns)
    
    # 1. 딕셔너리가 정상 조립되었는지 검증
    assert isinstance(configs, dict)
    assert "PLANT_CODE" in configs
    assert "MCODE" in configs
    assert "RCPT_FG_NM" in configs
    assert "RCPT_QTY" in configs
    
    # 2. 한글 헤더 매핑 검증
    # Streamlit Column Config 인스턴스의 1번째 프로퍼티(_label 혹은 label)가 지정한 한글 헤더에 상응하는지 간접 검증
    assert getattr(configs["PLANT_CODE"], "label", None) == "사업장"
    assert getattr(configs["MCODE"], "label", None) == "M코드"
    assert getattr(configs["SPEC_CD"], "label", None) == "규격코드"
    assert getattr(configs["RCPT_DATE"], "label", None) == "입고일자"
    assert getattr(configs["RCPT_FG_NM"], "label", None) == "입고구분"
    assert getattr(configs["RCPT_QTY"], "label", None) == "입고수량"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_query_metadata.py -v`
Expected: FAIL (AssertionError: 한글 헤더가 매핑되지 않았거나 None 반환)

- [ ] **Step 3: Write minimal implementation**

`local.data/query/query_metadata.json` 파일의 시작 괄호 바로 밑(예: 2라인) 또는 기존 JSON 마지막에 `"gmes_inv_warehouse_receipt"` 설정을 삽입합니다. 여기서는 2라인에 삽입하겠습니다.
(기존 키 중 하나인 `cqms_4m_main` 바로 직전에 구조를 깨지 않고 삽입합니다)

```json
  "gmes_inv_warehouse_receipt": {
    "table_path": "hkt_dw.inventory.inv_f_linvtr110",
    "description": "창고재고 입고 현황 이력 정보",
    "columns": {
      "PLANT_CODE": {
        "type": "VARCHAR",
        "description": "사업장 코드 (예: TP)",
        "display_header": "사업장",
        "is_essential": true
      },
      "MCODE": {
        "type": "VARCHAR",
        "description": "자재 코드 (M-Code)",
        "display_header": "M코드",
        "is_essential": true
      },
      "SPEC_CD": {
        "type": "VARCHAR",
        "description": "타이어 규격 코드",
        "display_header": "규격코드",
        "is_essential": true
      },
      "RCPT_DATE": {
        "type": "DATE",
        "description": "창고 입고 일자",
        "display_header": "입고일자",
        "is_essential": true
      },
      "SHP_FG": {
        "type": "VARCHAR",
        "description": "출하 구분 원천 코드 (O, R, T, F, E, S, P, X 등)",
        "display_header": "출하구분코드",
        "is_essential": true
      },
      "RCPT_FG_NM": {
        "type": "VARCHAR",
        "description": "출하구분이 사람이 인지 가능한 형태명으로 변환된 값",
        "display_header": "입고구분",
        "is_essential": true
      },
      "RCPT_QTY": {
        "type": "INT",
        "description": "창고 입고 수량",
        "display_header": "입고수량",
        "is_essential": true
      }
    }
  },
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_query_metadata.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add local.data/query/query_metadata.json tests/test_query_metadata.py
git commit -m "feat: add gmes_inv_warehouse_receipt metadata for dynamic column mapping"
```

---

### Task 5: UI 화면 레이어 및 관리자 세션 제어 개발

**Files:**
* Create: `app/pages/_80_admin/warehouse_receipt_page.py` (신규 생성)
* Test: `tests/test_warehouse_receipt_page.py` (신규 생성)

**Interfaces:**
* Consumes:
  * `WarehouseReceiptParams` (from `app.core.data_models.parameters`)
  * `preprocessing_warehouse_receipt_rawdata` (from `app.service.warehouse_receipt_df`)
  * `get_dynamic_column_configs` (from `app.core.design_system.column_config`)
* Produces:
  * Streamlit Page rendering (Admin auth protected)

- [ ] **Step 1: Write the failing test**

`tests/test_warehouse_receipt_page.py` 파일을 생성하여, 세션 상태에 `role` 정보가 비어 있거나 `Admin`이 아닌 경우 이 페이지가 `st.stop()`을 호출해 정상 격리 차단되는지 검증하는 테스트를 작성합니다.

```python
# -*- coding: utf-8 -*-
import pytest
import streamlit as st
from unittest.mock import patch, MagicMock

def test_warehouse_receipt_page_auth_protection():
    # st.session_state["role"]가 Admin이 아닐 때 error가 호출되고 자가 중단(stop)되는지 검증합니다.
    with patch("streamlit.session_state", {"role": "Viewer"}) as mock_session, \
         patch("streamlit.error") as mock_error, \
         patch("streamlit.stop") as mock_stop:
         
        # Import하는 시점에 모듈 시작부의 권한 필터가 작동합니다.
        try:
            import app.pages._80_admin.warehouse_receipt_page
        except SystemExit:
            pass # st.stop() 내부의 SystemExit 예외 무마
            
        mock_error.assert_called_with("이 페이지는 관리자(Admin) 권한을 가진 사용자만 접근할 수 있습니다.")
        mock_stop.assert_called_once()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_warehouse_receipt_page.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

`app/pages/_80_admin/warehouse_receipt_page.py` 파일을 생성하고 다음과 같이 프리미엄 UI 코드를 작성합니다:

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
from datetime import date
import streamlit as st
import pandas as pd

from app.core.design_system.css_injector import load_css
from app.core.design_system.streamlit_widgets import page_header
from app.core.design_system.column_config import get_dynamic_column_configs
from app.core.data_models.parameters import WarehouseReceiptParams
from app.service.warehouse_receipt_df import preprocessing_warehouse_receipt_rawdata

# =========================================================================
# SECTION 2. Security & Initialization (권한 검증 및 세션 상태 초기화)
# =========================================================================
load_css()

if "role" not in st.session_state:
    st.session_state["role"] = None

if st.session_state.get("role") not in ["Admin"]:
    st.error("이 페이지는 관리자(Admin) 권한을 가진 사용자만 접근할 수 있습니다.")
    st.stop()

# =========================================================================
# SECTION 3. Main Header (프리미엄 메인 헤더 보드)
# =========================================================================
page_header(
    title="Warehouse Inventory Receipts",
    title_icon=":material/warehouse:",
    subtitle="M-Code 기준의 공장 창고재고 입고 현황 데이터를 조회하고 집계합니다."
)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# =========================================================================
# SECTION 4. Sidebar Filter Controller (사이드바 입력 필터 세팅)
# =========================================================================
st.sidebar.markdown("### :material/filter_list: 조회 조건 필터")

# 1) 사업장 멀티 선택 (기본 TP 지정)
selected_plants = st.sidebar.multiselect(
    "사업장 (Plant)",
    options=["TP", "DP", "KP", "JP"],
    default=["TP"],
    help="조회하고자 하는 공장 코드를 선택하십시오."
)

# 2) M코드 조건 (기본 대상 M-Code 세팅)
# 텍스트 에어리어로 대량 M코드를 줄바꿈/콤마로 입력받도록 유도
mcode_input = st.sidebar.text_area(
    "M코드 (PRD_CD)",
    value="1033649\n1033647\n2022188",
    help="조회할 M코드 목록을 줄바꿈 또는 쉼표(,)로 구분하여 입력하십시오."
)

# M코드 전처리
mcode_list = []
if mcode_input:
    mcode_list = [code.strip() for code in mcode_input.replace(",", "\n").split("\n") if code.strip()]

# 3) 입고일자 날짜 범위
today = date.today()
start_of_year = date(today.year, 1, 1)

col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    start_date = st.date_input("시작 일자", value=start_of_year)
with col_d2:
    end_date = st.date_input("종료 일자", value=today)

# =========================================================================
# SECTION 5. Main Content Renderer (데이터 수집 및 메인 콘텐츠 렌더링)
# =========================================================================
if not selected_plants:
    st.warning("최소 하나 이상의 사업장을 선택해 주십시오.")
    st.stop()

if not mcode_list:
    st.warning("최소 하나 이상의 M코드를 입력해 주십시오.")
    st.stop()

# 파라미터 수집 및 빌딩
params = WarehouseReceiptParams(
    plant_list=selected_plants,
    mcode_list=mcode_list,
    start_date=start_date.strftime("%Y%m%d"),
    end_date=end_date.strftime("%Y%m%d")
)

# 데이터 가공 서비스 호출
with st.spinner("Databricks DW 입고 현황 데이터를 조회 중입니다..."):
    df_receipt = preprocessing_warehouse_receipt_rawdata(params)

# 데이터 렌더링
if df_receipt.empty:
    st.info("선택된 조회 필터 범위 내에 존재하는 창고 입고 이력 데이터가 없습니다.")
else:
    # 데이터 총량 및 지표 미니보드
    total_qty = df_receipt["RCPT_QTY"].sum()
    total_rows = len(df_receipt)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("총 입고 건수", f"{total_rows:,} 건")
    with col_m2:
        st.metric("총 입고 수량", f"{total_qty:,} EA")
        
    st.markdown("<div style='margin-bottom: 1.0rem;'></div>", unsafe_allow_html=True)
    
    # 동적 한글 메타데이터 바인딩 테이블 표출 (한글 AS 하드코딩 영구 방지)
    column_config = get_dynamic_column_configs("gmes_inv_warehouse_receipt", list(df_receipt.columns))
    
    st.dataframe(
        df_receipt,
        use_container_width=True,
        column_config=column_config,
        hide_index=True
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_warehouse_receipt_page.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/pages/_80_admin/warehouse_receipt_page.py tests/test_warehouse_receipt_page.py
git commit -m "feat: complete warehouse receipt page with admin session guard and dynamic table"
```
