# Componentize Data Analysis Metrics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `app/pages/_20_analysis/data_analysis_page.py` 및 대시보드 화면에 하드코딩되어 있던 HTML 기반 프리미엄 메트릭 카드 및 주요 부적합 TOP 3 결합 카드를 전역 컴포넌트 모듈(`app/core/design_system/components/metrics.py`)로 추출하고, 이를 각 분석 화면에서 범용 임포트하여 클린 코드를 완성합니다.

**Architecture:** 
- 디자인 시스템 패키지 하위에 `components` 디렉토리를 마련하고 `metrics.py` 컴포넌트 모듈을 구축합니다.
- 복잡한 2열 분리형 TOP 3 카드 및 SOP 메타데이터 카드 생성 함수를 명확한 파라미터 타입 힌팅과 Google/NumPy 스타일 한글 독스트링(Docstring)으로 구현합니다.
- `data_analysis_page.py` 내의 중복 보일러플레이트 HTML 코드를 완전 걷어내고 컴포넌트로 일괄 전환합니다.

**Tech Stack:** Python 3, Streamlit, HTML5, CSS3, Design System Tokens

## Global Constraints

- Streamlit UI, 마크다운 문서, 소스 코드 주석 등 어떠한 곳에서도 일반 유니코드 이모지(별, 느낌표, 전구 등)를 절대 사용할 수 없습니다.
- 모든 파일 하이퍼링크는 반드시 프로토콜을 제외하고 워크스페이스 루트 기준의 평문 상대 경로만을 사용하여 작성해야 합니다.
- 새로 작성되는 모든 모듈, 클래스, 함수에는 반드시 한글(Korean)로 작성된 명확한 독스트링(Docstring)과 섹션 구분 주석 장식이 포함되어야 합니다.

---

## Task 1: 전역 UI 메트릭 컴포넌트 모듈 설계 및 구현

**Files:**
- Create: `app/core/design_system/components/metrics.py`
- Create: `app/core/design_system/components/__init__.py`

**Interfaces:**
- Produces: 
  - `render_premium_metric_card(title: str, value: str, description: str, value_style: str = "") -> str`
  - `render_metadata_card(plant: str, mcode: str, oem: str, vehicle: str, sop_date_str: str, prod_period_str: str, badge_bg_color: str) -> str`
  - `render_top3_defect_card(defects: list[dict], title: str = "주요 부적합<br>TOP 3", rank_color: str = "#f97316") -> str`
  - `render_unified_metric_row(metadata_html: str, metrics_html_list: list[str], unified_defect_html: str) -> str`

- [ ] **Step 1: `components/__init__.py` 포워더 파일 생성**
  - 패키지 네임스페이스 정의 및 컴포넌트 임포트 단순화 포워딩 구문을 작성합니다.

- [ ] **Step 2: `components/metrics.py` 컴포넌트 모듈 구현**
  - Google/NumPy 스타일의 명확한 한글 독스트링을 작성합니다.
  - 마크다운 복사 버그 우회용 프리미엄 메트릭 카드 및 2열 분리 레이아웃의 TOP 3 카드 템플릿 로직을 고가용성 컴포넌트로 안전하게 이식합니다.
  - 색상 코드와 같은 스타일링 속성에 디자인 토큰을 활용할 수 있도록 유연한 인자(Parameter) 설계를 적용합니다.

---

## Task 2: Data Analysis 화면에 컴포넌트 이식 및 렌더러 리팩토링

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page.py`

**Interfaces:**
- Consumes: `app.core.design_system.components.metrics` 컴포넌트 기능들

- [ ] **Step 1: 보일러플레이트 코드 제거 및 임포트 구문 교체**
  - `data_analysis_page.py` 내부의 기존 인라인 HTML 메트릭 카드 렌더링 코드(`render_custom_metric_card`, `unified_defect_card_html` 조립부 등)를 모두 제거합니다.
  - 상단에 신규 컴포넌트 임포트 구문을 선언합니다.

- [ ] **Step 2: 컴포넌트 적용 및 데이터 매핑**
  - 연산된 생산량, NCF 발생 수량, PPM 수치 및 상위 3개 불량 목록을 컴포넌트에 주입합니다.
  - `render_unified_metric_row`를 이용해 최종 UI 단일 컨테이너를 안전하게 렌더링합니다.

- [ ] **Step 3: 로컬 런타임 및 예외 방어 게이트 검증**
  - 수정 완료 후 정적 검증(`python -m py_compile app/pages/_20_analysis/data_analysis_page.py`)을 실행하여 구문 에러를 차단합니다.
  - 유니코드 이모지가 주석이나 텍스트 내에 묻어 들어갔는지 텍스트 스캔으로 검증합니다.
