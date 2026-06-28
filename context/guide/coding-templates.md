---
id: guide.coding_templates
type: reference
status: active

summary: >
  UI 페이지, 서비스, plots, 쿼리 각 계층별로 준수해야 하는 파이썬 표준 소스 코드 및 주석 템플릿 가이드라인.

keywords:
  - templates
  - coding-standard
  - boilerplate
  - comments

parent: "[[context/guide/guide-index]]"

related:
  - "[[rules/L2-naming-convention]]"
  - "[[context/guide/3layer-development-process]]"
  - "[[context/guide/page-template-standard]]"

consumers:
  - "[[agents/roles/planner-orchestrator]]"
  - agent.ui_builder
  - agent.service_builder

updated: 2026-06-28
---


# 3-Layer Architecture 구조적 주석 템플릿 가이드

## Overview
* **왜 존재하는가 (Why)**: 개발자 및 AI 에이전트가 코드를 작성할 때 일관되고 통일된 주석 구조와 포맷을 보장하여 소스코드의 가독성을 최상으로 유지하기 위함입니다.
* **언제 사용하는가 (When)**: 신규 페이지 모듈, 서비스 함수, SQL 쿼리 모듈을 신설하거나 기존 코드를 전면 리팩토링할 때 뼈대로 복사하여 사용합니다.
* **연계 실행 (Next Action)**: 구체적인 Streamlit 표준 페이지 템플릿 상세 명세를 확인하려면 [guide.page_template_standard](.agents/context/guide/page-template-standard.md)를 참조하십시오.

## Connections
* **상위 개념**: [guide.readme](.agents/context/guide/guide-index.md)
* **연관 자산**:
  - [.agents/context/guide/page-template-standard.md](.agents/context/guide/page-template-standard.md)
  - [.agents/context/guide/page_template_standard.py](.agents/context/guide/page_template_standard.py)
  - [.agents/context/guide/query_module_template.py](.agents/context/guide/query_module_template.py)

---

이 문서는 모든 개발자가 동일한 주석 블록과 정렬 구조를 표준으로 삼아 일관성 있는 소스코드를 작성하도록 유도하는 **구조적 주석 섹션(Comment Sections) 템플릿**을 정의합니다.

새로운 파일을 생성할 때는 아래 정의된 레이어별 주석 구조를 복사하여 뼈대로 삼고, 각 영역의 가이드라인에 맞추어 코드를 구현하십시오.

---

## ❶ 대시보드 UI 레이어 템플릿 (`app/pages/*_page.py`)

- **목적**: 사용자의 필터 선택을 입력받아 파라미터를 제어하고, 레이아웃을 구성하며, 최종 차트와 지표 카드를 화면에 렌더링합니다.
- **주석 및 구조 템플릿**:
  대시보드 화면 컨트롤러는 일관된 작업 순서(7단계 표준 구조)와 탭/섹션 분할 렌더링 가독성 규칙을 준수하여 작성해야 합니다. 
  자세한 설계 규칙은 [.agents/context/guide/page-template-standard.md](.agents/context/guide/page-template-standard.md) 문서를 준수하십시오.

  실제 신규 개발 및 리팩토링 시 즉시 복사하여 사용할 수 있는 완전한 파이썬 소스 코드 템플릿은 [.agents/context/guide/page_template_standard.py](.agents/context/guide/page_template_standard.py)를 복사하여 뼈대로 삼으십시오.

- **요약된 7단계 구조 개요**:
  1. **Imports**: 외부 라이브러리, 코어 UI, 비즈니스 서비스, 1:1 plots 순 배치
  2. **Page Config**: st.set_page_config() 선언 및 load_css() 호출
  3. **Session Interception**: 위젯 렌더링 전 st.session_state 키 백업 및 클리어 처리로 에러 차단
  4. **Sidebar Inputs**: 사이드바 필터 제어 및 *Params 데이터클래스 조립 패킹
  5. **Data Loading**: st.spinner() 기동 하에 서비스 레이어 호출 및 빈 데이터 방어막(st.stop()) 수립
  6. **Modular Rendering Functions**: 탭별/섹션별 렌더링 함수군 선언 (st.fragment 적용)
  7. **Main Render Loop**: 타이틀 정보 패널 렌더링 후 st.tabs() 객체와 렌더링 함수 바인딩 전개

---

## ❷ 서비스 레이어 템플릿 (`app/service/*_df.py`)

- **목적**: DB 클라이언트를 통해 조회된 원시 데이터를 1차 전처리(타입 교정, 결측치 처리) 및 2차 가공(비즈니스 수식 적용), 3차 집계 연산(그룹화)을 통해 정제된 Pandas DataFrame으로 가공합니다.
- **주석 섹션 구성**:

```python
"""
<도메인명> 데이터 처리 및 비즈니스 서비스 모듈
- 작성일: 2026-06-09
- 설명: <도메인/기능 설명> 데이터를 수집, 전처리, 통계/그룹 집계하는 서비스 레이어입니다.
"""

# =========================================================================
# SECTION 1. Imports (라이브러리, DB 클라이언트 및 쿼리 빌더 임포트)
# =========================================================================
# 1) 외부 패키지 (pandas, streamlit 등)
# 2) DB 클라이언트 및 설정 (get_client)
# 3) params 데이터클래스
# 4) 연계 쿼리 조립 모듈 (*_query.py)


# =========================================================================
# SECTION 2. Primary Preprocessing & Caching (1차 원시 데이터 조회 및 캐싱 처리)
# =========================================================================
# - @st.cache_data(ttl=3600) 데코레이터 적용
# - sql = get_*_rawdata(params) 쿼리 문자열 조립 호출
# - db_client.execute(sql) 쿼리 수행
# - 데이터 타입 복구(pd.to_datetime 등), 결측치 기본값 대체 가공 (Inplace Mutation 사용 금지)


# =========================================================================
# SECTION 3. Business Data Transformations (2차 형태 변형 및 비즈니스 공식 가공)
# =========================================================================
# - 1차 가공 완료된 데이터프레임을 기반으로 피벗, 파생 변수 생성, 비즈니스 계산 수행
# - 판다스 메소드 체이닝(.assign, .query 등)을 활용해 정돈된 연산 흐름 확보


# =========================================================================
# SECTION 4. Statistical Group Aggregations (3차 통계 및 그룹 집계 연산)
# =========================================================================
# - 일별, 월별, 공장별, 제품별 등 특정 차원을 기준으로 그룹 연산(.groupby) 수행
# - 집계 요약 및 정렬 작업을 완료한 최종 차트 드로잉용 데이터프레임 반환


# =========================================================================
# SECTION 5. Private Helpers (모듈 내부 전용 비공개 헬퍼 함수)
# =========================================================================
# - 모듈 외부로 노출하지 않는 서브 루틴 함수들을 언더바 접두사(_fetch_*, _apply_*) 형태로 정의
```

---

## ❸ 시각화 플롯 레이어 템플릿 (`app/pages/*_plots.py`)

- **목적**: 넘겨받은 정제 완료된 DataFrame을 활용해 hover 텍스트 가공, 차트 디자인 세부 옵션을 설정하고 최적화된 **Plotly Figure 객체**를 반환합니다.
- **주석 섹션 구성**:

```python
"""
<도메인명> 시각화 드로잉 모듈
- 작성일: 2026-06-09
- 설명: <도메인/기능 설명> 데이터 시각화를 위한 Plotly 차트 빌더 세트입니다.
"""

# =========================================================================
# SECTION 1. Imports (라이브러리 및 공통 디자인 테마 컬러 임포트)
# =========================================================================
# 1) 외부 패키지 (plotly.graph_objects, plotly.express 등)
# 2) 중앙화 디자인 테마 컬러 (app.core.constants.ui 등)
# - [주의] streamlit 이나 비즈니스 서비스 레이어 모듈을 절대 이곳에서 임포트하지 마십시오.


# =========================================================================
# SECTION 2. Visual-Specific Preprocessing (시각화 종속 데이터 포맷 가공)
# =========================================================================
# - 데이터가 비어있을 경우 미려한 안내용 빈 go.Figure() 즉시 가공 반환
# - hovertemplate용 마우스 오버 툴팁 f-string 조립 및 컬럼 할당
# - 시각화 전용 Top-N 자르기 및 "Others" 그룹화, 축 포맷 가공


# =========================================================================
# SECTION 3. Plotly Traces Drawing (Plotly 트레이스 및 데이터 시각화 구성)
# =========================================================================
# - go.Figure() 객체 생성 및 Trace 추가 (go.Bar, go.Scatter, go.Pie 등)
# - 중앙화 테마에서 정의된 프리미엄 컬러 파레트(colors.get("primary") 등) 바인딩


# =========================================================================
# SECTION 4. Figure Layout Customization (레이아웃, 축, 범례 디테일 커스텀)
# =========================================================================
# - fig.update_layout() 설정: 투명한 배경(paper_bgcolor="rgba(0,0,0,0)"), 마진 조율, 마우스 호버 모드 최적화
# - fig.update_xaxes(), fig.update_yaxes() 설정: 가느다란 그리드 실선(gridcolor="rgba(200,200,200,0.2)"), 축 정렬
# - 범례(Legend) 가로형 일괄 배치 최적화 및 조율 완료된 fig 최종 반환
```

---

## ❹ 쿼리 레이어 템플릿 (`app/queries/*_query.py` 또는 `q_*.py`)

- **목적**: 데이터베이스 실행은 하지 않고, 입력 파라미터를 받아 **순수 SQL 문자열(`str`)**을 동적으로 생성 및 조립합니다.
- **주석 및 함수 명명 규칙 구성**:
  - **대통합 공식**: `get_{system}_{domain}_{조건/설명/특별한 내용이 없으면 general}_{agg/rawdata}`
  - 실사용 파이썬 템플릿 코드는 [query_module_template.py](query_module_template.py) 파일을 바로 복사하여 뼈대로 사용할 수 있습니다.

```python
"""
<도메인명> 쿼리 조립 모듈
- 작성일: 2026-06-12
- 설명: <도메인/기능 설명> 관련 데이터베이스 조회용 순수 SQL 쿼리를 생성합니다.
"""

# =========================================================================
# SECTION 1. Imports & Constants (파라미터 및 중앙 테이블 상수 임포트)
# =========================================================================
# 1) params 데이터클래스
# 2) 중앙화 테이블 상수 변수 (DatabricksTables, OracleTables 등)
# 3) SQL 조립 헬퍼 클래스 (QueryFilter, SQLConverter)


# =========================================================================
# SECTION 2. Style A: 단순 조회 및 단일 테이블 마스터형 (Simple Master Target)
# =========================================================================
# - JOIN이 없고 조건이 단순한 기준 마스터 테이블 조회용
# - 예: get_gmes_spec_product_master(params)
def get_{system}_{domain}_{조건/설명}_master(params: ParamsClass) -> str:
    conditions = [QueryFilter.where_in("COL", params.values)]
    where_clause = QueryFilter.build_where(conditions)
    
    query = f"""--sql
    SELECT * FROM {DatabricksTables.table_name}
    {where_clause};
    """
    return query


# =========================================================================
# SECTION 3. Style B: 다중 조인 및 가변 필터형 (Dynamic Multi-Join Target)
# =========================================================================
# - 다중 JOIN 및 동적 조건절 결합
# - 예: get_cqms_qi_mttc_defect_rawdata(params)
def get_{system}_{domain}_{조건/설명}_{agg/rawdata}(params: ParamsClass) -> str:
    conditions = [
        QueryFilter.where_in("QI.PLANT", params.plant_list),
        QueryFilter.where_date_between(params.start_date, params.end_date, "QI.REG_DATE")
    ]
    where_clause = QueryFilter.build_where(conditions)
    
    query = f"""--sql
    SELECT QI.*, M.M_CODE
    FROM {DatabricksTables.cqms_quality_main} QI
    INNER JOIN {DatabricksTables.cqms_quality_mcode} M ON QI.SEQ = M.CQMS_QUALITY_ISSUE_SEQ
    {where_clause};
    """
    return query


# =========================================================================
# SECTION 4. Style C: 대규모 CTE 구조화형 (Complex CTE-Structured Target)
# =========================================================================
# - 초복잡 쿼리용, CTE(WITH 문)를 메인 함수 안에 계층적으로 단일 조립 (쪼개기 절대 금지)
# - 예: get_ctms_ctl_daily_window_agg(params)
def get_{system}_{domain}_{조건/설명}_{agg/rawdata}(params: ParamsClass) -> str:
    where_clause = QueryFilter.build_where([QueryFilter.where_in("PLANT", params.plant_list)])
    
    query = f"""--sql
    WITH base AS (
        SELECT DOC_NO, PLANT FROM {DatabricksTables.ctms_result_data} {where_clause}
    ),
    agg_data AS (
        SELECT PLANT, COUNT(DOC_NO) AS CNT FROM base GROUP BY PLANT
    )
    SELECT * FROM agg_data;
    """
    return query
```

---

## 💡 개발 가이드라인 수칙 요약

1. **템플릿 준수 의무**: 신규 파일 생성 시 해당 레이어의 **SECTION 1 ~ 5 주석 구문**을 맨 위에 복사하여 붙여넣은 뒤 작업을 시작하십시오.
2. **섹션 준수 체크**: 다른 개발자가 파일을 보더라도 주석 섹션을 보고 필요한 로직(예: UI 필터 추가는 SECTION 3, 차트 옵션 변경은 SECTION 4)의 위치를 즉각 파악할 수 있어야 합니다.
3. **격벽 무결성**: 각 섹션 내 가이드라인에 맞지 않는 로직(예: 서비스 레이어 내에서 Plotly 임포트하기, UI 파일 내에서 SQL 직접 선언하기 등)은 어떠한 상황에서도 엄격히 금지됩니다.
