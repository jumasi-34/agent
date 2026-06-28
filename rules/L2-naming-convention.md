---
id: rule.l2.naming_convention
title: "[Rule] 코드 명명 규칙"
type: rule
status: active

summary: >
  L2 코드베이스 명명 규칙 표준.
  소스 코드 파일, 클래스, 함수(3-Layer 공식), 변수, DB 컬럼 및 CSS 클래스의 명명 규칙을 통일한다.

keywords:
  - naming-convention
  - standards
  - refactoring

parent: "[[rules/rules-index.md]]"

related:
  - "[[rules/L2-architecture.md]]"
  - "[[rules/L3-query.md]]"
  - "[[rules/L3-service.md]]"

consumers:
  - agent.all

updated: 2026-06-29
---


# L2-naming-convention.md (L2 코드베이스 명명 규칙 표준)

본 문서는 다차원 계층 구조(UI-Service-Query)를 유지하고 다수의 AI 에이전트와 인간 개발자가 생성하는 코드의 유지보수성을 극대화하기 위해 명명 및 서식 표준을 정의하는 **단일 진실 공급원(SSOT) 규칙**입니다.

---

## 1. 3-레이어 파일 및 디렉터리 명명 규칙 (File Naming)

모든 파일과 폴더의 이름은 소문자 스네이크 케이스(`snake_case`)를 사용합니다.

| 레이어 | 역할 | 파일명 규칙 | 올바른 예시 |
| :--- | :--- | :--- | :--- |
| **UI 메인** | Streamlit 화면 구성 및 입력 필터 제어 | `*_page.py` | `cqms_dashboard_page.py` |
| **UI 시각화** | Plotly 차트 드로잉 및 Hover 포맷팅 | `*_plots.py` | `cqms_dashboard_plots.py` |
| **Service** | Pandas 전처리, 비즈니스 계산 및 캐싱 | `*_df.py` | `cqms_df.py` |
| **Query** | SQL 문자열 조립 및 반환 | `*_query.py` 또는 `q_*.py` | `cqms_query.py`, `q_iqm_plus.py` |
| **기획 명세** | PRD 기획서 및 요구사항 정의서 | `*_prd.md` | `oe_quality_issue_dashboard_prd.md` |

* **에이전트 규칙 규칙 (`.agents/rules/`)**: 룰 계층 관리를 위해 반드시 분류 접두사(`L1-`, `L2-`, `L3-`)를 부여합니다.
* **상대 경로 의무화**: 모든 마크다운 자산 내 하이퍼링크는 절대 리눅스 경로나 `file:///` 프로토콜을 전면 배제하고, 워크스페이스 기준 평문 상대 경로(예: `[L2-architecture.md](.agents/rules/L2-architecture.md)`)만을 기입해야 합니다.

---

## 2. 소스 코드 요소 명명 공식 (Code Level Naming)

파이썬 PEP 8 스타일 가이드를 준수하며 아래 규칙을 엄격히 강제합니다.

### ① 클래스 및 변수 명명 (Classes & Variables)
* **클래스명**: 파스칼 케이스(`PascalCase`)를 사용하며, 필터 파라미터 데이터클래스는 반드시 `*Params` 접미사로 통일합니다. (예: `BaseFilterParams`, `OeQualityIssueParams`)
* **변수명**: 소문자 스네이크 케이스(`snake_case`)를 적용하며, Pandas DataFrame 변수는 반드시 `_df` 접미사를 적극 적용합니다. (예: `raw_df`, `filtered_df`)
* **SQLite 데이터베이스 로드 변수**: 로컬 SQLite로부터 데이터프레임을 조회해 적재할 시 원천 DB를 식별하기 위해 `sqlite<물리DB명>_<도메인약어>_<CamelCase비즈니스명>` 공식을 사용합니다.
  * `ops.db` 로드 예시: `sqliteOps_iqm_devSpecList`, `sqliteOps_iqm_mcodeMapping`
  * `staging.db` 로드 예시: `sqliteStaging_iqm_aggregateCum`
* **데이터프레임 컬럼명**: 데이터베이스 물리 스키마로부터 기인한 컬럼은 대문자 스네이크 케이스(`UPPER_SNAKE_CASE`)를 사용합니다. (예: `PLANT`, `NCF_RATE`)

### ② 함수 명명 공식 (get_{system}_{domain}_{조건/설명/general}_{agg/rawdata})
모든 함수명은 소문자 스네이크 케이스를 준수하며, 다음 공식을 기반으로 한눈에 계층과 출처가 정렬되도록 명명합니다.

1. **쿼리 레이어 (`app/queries/`)**: 오직 SQL 문자열 조립과 텍스트 반환만 담당하므로 `get_` 접두사와 데이터 종류를 접미사로 명명합니다.
   * 원시 데이터 조회 쿼리: `get_cqms_qi_mttc_rawdata(...)`, `get_ctms_ctl_general_rawdata(...)`
   * 조건 및 축별 조회: `get_gmes_production_by_plant(...)`, `get_gmes_ncf_by_dft_cd(...)`
2. **서비스 레이어 (`app/service/`)**: 데이터프레임 가공과 연산을 처리합니다.
   * 원시 데이터 수집 및 1차 전처리: `preprocessing_<도메인>_*_rawdata` (예: `preprocessing_qi_general_rawdata(...)`)
   * 대시보드 2차 가공 및 형태 변환: `transform_<업무/차트>_df` (예: `transform_qi_dashboard_df(...)`)
   * 통계 및 그룹 집계: `preprocessing_<업무>_*_agg` (예: `preprocessing_ncf_daily_agg(...)`)

---

## 3. 함수 생성 및 독스트링 필수 서식 (Function & Docstring Standards)

신규 또는 리팩토링 함수를 선언할 때, 가독성과 정합성 자동 검증을 위해 아래 5대 서식을 무조건 적용합니다.

1. **식별용 헤더 주석**: 함수 선언 직전 라인에 `# * [대분류 - 요약 설명]` 주석을 작성합니다.
   * 예시: `# * [SQL - IN 또는 NOT IN 조건절 생성]`
2. **명확한 타입 힌팅**: 파라미터와 반환값에 엄격한 Python 타입 힌트(`str | list[str] | None` 등)를 지정합니다.
3. **구조화된 독스트링**: Google/NumPy 독스트링 규격을 따르며, 함수의 목적 요약, Parameters(인자명, 타입, 상세 의미), Returns(반환 타입)를 작성합니다.
4. **한국어 독스트링 원칙**: 소스 코드 내 모든 독스트링 및 주석은 협업 가독성을 위해 **가능하면 한국어(Korean)로 작성**하는 것을 기본 원칙으로 삼습니다.
5. **섹션 구분 타이틀 하이라이트 표준**: 주요 레이아웃 구역을 정의할 때 반드시 장식 라인이 포함된 일관된 주석 블록을 사용해야 합니다.
   ```python
   # =========================================================================
   # SECTION 1. Imports (라이브러리 및 모듈 임포트)
   # =========================================================================
   ```

### 올바른 구현 표준 템플릿
```python
# * [SQL - IN 또는 NOT IN 조건절 생성]
def where_in(
    field_name: str, values: str | list[str] | None = None, include: bool = True
) -> str:
    """
    필드의 IN 또는 NOT IN 조건 SQL 문자열을 생성합니다.

    Parameters
    ----------
    field_name : str
        조건을 적용할 SQL 필드명.
    values : str | list[str] | None, optional
        필터링할 값 또는 값 리스트. 기본값은 None.
    include : bool, default=True
        True이면 IN, False이면 NOT IN 조건을 생성.

    Returns
    -------
    str
        생성된 SQL 조건문 문자열.
    """
    if not values:
        return ""
    if isinstance(values, str):
        operator = "=" if include else "!="
        return f"{field_name} {operator} '{values}'"
    if isinstance(values, list) and len(values) > 0:
        operator = "IN" if include else "NOT IN"
        values_str = "', '".join(str(v) for v in values)
        return f"{field_name} {operator} ('{values_str}')"
    return ""
```
