# [Spec] 창고재고 입고 현황 조회 (PRD_CD 기준) 기능 설계 명세서

## 1. 개요 및 목적
* **배경**: 기존에 SQL 쿼리로 수동 조회하던 '창고재고 입고 현황(M-Code 기준)' 데이터를 시스템 내부의 표준 아키텍처(L3-query, L3-service, L3-dashboard)에 맞추어 관리자 페이지에 연동하고, 한글 AS 하드코딩 안티패턴을 제거하여 프리미엄 UI로 표출합니다.
* **목표**: 
  * `inv_f_linvtr110` 테이블을 `DatabricksTables` 상수에 추가하여 비즈니스 정합성을 확보합니다.
  * SQL 한글 Alias 오염을 방지하고 `get_dynamic_column_configs`를 경유한 동적 한글 매핑 헬퍼를 결합합니다.
  * 기존 `DECODE` 구문을 표준 `CASE WHEN` 구문으로 온전히 전환하여 출하구분 매핑을 보완합니다.
  * Streamlit Admin 권한 제어를 탑재하여 오직 관리자 계정만 접근할 수 있는 전용 페이지를 구축합니다.

---

## 2. 아키텍처 설계 및 구성 요소 (Architecture & Components)

### ① 데이터 모델 및 파라미터 표준화
* **대상 파일**: `app/core/data_models/parameters.py`
* **추가 요소**: `WarehouseReceiptParams` 데이터클래스 정의
```python
@dataclass
class WarehouseReceiptParams:
    """창고재고 입고 현황 조회 처리 매개변수"""
    plant_list: str | list[str] | None = None
    mcode_list: str | list[str] | None = None
    start_date: str | None = None
    end_date: str | None = None
    view_mode: Literal["rawdata"] = "rawdata"
```

* **대상 파일**: `app/core/sql_builder/query_database.py`
* **추가 요소**: `DatabricksTables` 클래스 상수에 창고재고 입고 현황 테이블 등록
```python
gmes_inv_warehouse_receipt: ClassVar[str] = "hkt_dw.inventory.inv_f_linvtr110"  # [GMES] 창고재고 입고 현황 이력 정보
```

### ② 쿼리 레이어 (L3-query)
* **대상 파일**: `app/queries/q_warehouse_receipt.py` (신규 생성)
* **책임**: 오직 순수 SQL 문자열(`str`) 조립 및 반환. 직접 실행하지 않음.
* **규칙 준수**:
  * 한글 AS 별칭 사용을 전면 배제하고, 무조건 영문 물리 컬럼명을 반환합니다.
  * `DECODE`는 표준 `CASE WHEN` 구문으로 완전히 전환합니다.
  * `QueryFilter` 헬퍼를 활용해 동적 조건을 바인딩합니다.
  * 완성된 SQL 문자열을 `query` 지역 변수에 바인딩한 후 최종 줄에서 단일 반환합니다.
  * 함수 선언부 위에 대괄호 형태의 식별용 헤더 주석(`# * [WAREHOUSE - 요약 설명]`)을 작성합니다.

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
from app.core.sql_builder.query_database import DatabricksTables
from app.core.sql_builder.query_helper import QueryFilter, log_query_assembly

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
        FROM {{DatabricksTables.gmes_inv_warehouse_receipt}} t
        {{where_clause}}
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

### ③ 서비스 레이어 (L3-service)
* **대상 파일**: `app/service/warehouse_receipt_df.py` (신규 생성)
* **책임**: 데이터 타입 복구 및 결측치 대체 전처리 수행, 대시보드 렌더링에 적합한 데이터프레임 반환.
* **규칙 준수**:
  * 무거운 Databricks 쿼리 조회가 일어나므로 `@st.cache_data(ttl="1h")` 캐싱 데코레이터를 적용합니다.
  * 데이터프레임 가공 시 `inplace=True` 사용을 절대 금지합니다.
  * 파라미터는 낱개 변수가 아닌 `WarehouseReceiptParams` 데이터클래스로 수집합니다.
  * 표준 함수 명명 규칙인 `preprocessing_warehouse_receipt_rawdata`를 준수합니다.

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import pandas as pd
import streamlit as st
from app.core.infrastructure.databricks_client import DatabricksClient  # 혹은 표준 실행 라이브러리
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
    
    if df_raw.empty:
        return pd.DataFrame(columns=["PLANT_CODE", "MCODE", "SPEC_CD", "RCPT_DATE", "SHP_FG", "RCPT_FG_NM", "RCPT_QTY"])
        
    # 타입 교정 및 인플레이스 가공 금지 규칙 준수
    df = df_raw.copy()
    df["RCPT_QTY"] = pd.to_numeric(df["RCPT_QTY"], errors="coerce").fillna(0).astype(int)
    df["RCPT_DATE"] = df["RCPT_DATE"].astype(str)
    
    return df
```

### ④ 화면 레이어 (L3-dashboard UI)
* **대상 파일**: `app/pages/_80_admin/warehouse_receipt_page.py` (신규 생성)
* **책임**: 입력 필터를 제어하고, 사이드바를 연동하며, 프리미엄 테이블을 화면에 렌더링합니다.
* **규칙 준수**:
  * `st.session_state.get("role") != "Admin"` 인 경우 에러 메시지와 함께 실행을 완전히 중단(`st.stop()`)합니다.
  * 본문의 대제목은 프로젝트 표준 규격인 `page_header` 공통 H1 컴포넌트를 필수 활용합니다.
  * 일반 이모지 사용을 전면 배제하고 오직 Google Material Symbol만 활용합니다.
  * 화면에 표출할 때는 반드시 `get_dynamic_column_configs` 동적 헬퍼를 경유시켜 컬럼 레이블, 설명, 데이터 포맷이 정밀 결합되도록 합니다.
  * 표준 템플릿인 `standard_page_template.py`를 계승하여 일관성 있는 사이드바 필터를 구축합니다.

### ⑤ 메타데이터 바인딩 표준화
* **대상 파일**: `local.data/query/query_metadata.json`
* **추가 요소**: 신규 가상 테이블 `"gmes_inv_warehouse_receipt"` 스키마 정의를 추가하여, `get_dynamic_column_configs` 호출 시 한글 명칭과 툴팁이 자동으로 주입되도록 보완합니다.
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
        "description": "창고 입고 일자 (YYYYMMDD)",
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
        "description": "출하구분 코드가 한글/영문 설명으로 디코딩된 값 (예: OEM, REP, OE Fitment 등)",
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
  }
```

---

## 3. 테스트 및 품질 검증 계획 (Harnessing & QA Plan)
* **테스트 격리 원칙**: 실제 원격 Databricks DB 커넥션을 성립하지 않는 환경에서도 비즈니스 로직을 검증할 수 있도록 `tests/` 하위에 독립된 단위 테스트를 수행합니다.
* **Mocking 검증**: `DatabricksClient` 객체를 Mocking 하여 샘플 입고 이력 데이터프레임이 리턴되었을 때, `preprocessing_warehouse_receipt_rawdata` 함수가 인플레이스 변조 없이 자료형 정제와 결측치 처리를 완벽히 수행하는지 검증합니다.
* **코드 무결성 린터(Verify Code)**: 작업 완료 후 `verify_code.py` 등을 실행하여 금지된 이모지 혼입 여부, SQL 한글 Alias 하드코딩 여부, 린트 오류를 완전 검역(Quality Gate)할 것입니다.

---

## 4. 자가 진단 및 예외 대응 설계
* **데이터 부재 시 대응**: 지정된 M코드로 기간 내 조회 데이터가 없을 경우, 화면 파괴 현상 없이 "조회된 입고 데이터가 존재하지 않습니다." 라는 미려한 빈 경고창(`st.info` + 자동 이모지 바인딩 몽키패치)으로 예외를 우아하게 대체합니다.
* **성능 및 캐싱 조절**: 1시간(`ttl="1h"`) 만료 주기를 설정하여 Databricks 클러스터 부하 및 클라우드 과금을 원천 최소화합니다.
