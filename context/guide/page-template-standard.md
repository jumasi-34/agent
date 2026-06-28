---
id: guide.page_template_standard
type: reference
status: active

summary: >
  Streamlit 화면 컨트롤러 파일(*_page.py) 작성 시 준수해야 하는 7단계 표준 구조(Page Config, Load State, Sidebar, Main tabs, Render) 및 디자인/아키텍처 가이드라인.

keywords:
  - streamlit
  - ui-standard
  - layout
  - template
  - page-controller

parent: "[[context/guide/guide-index.md]]"

related:
  - "[[rules/L3-dashboard.md]]"
  - "[[context/guide/coding-templates.md]]"
  - "[[context/guide/new_page_development_workflow.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"
  - agent.ui_builder

updated: 2026-06-28
---


# Streamlit UI Page Naming & Architectural Template Standard

## Overview
* **왜 존재하는가 (Why)**: 모든 대시보드 화면 컨트롤러가 정립된 7단계 개발 표준 순서와 3레이어 물리 격리 규칙을 만족하도록 함으로써 UI 계층의 구조적 일관성과 최상의 유지보수 가독성을 확보하기 위함입니다.
* **언제 사용하는가 (When)**: 신규 Streamlit 페이지 모듈(`*_page.py`)을 설계하거나, 복잡해진 화면의 컴포넌트 렌더링 순서 및 필터 구조를 리팩토링할 때 준수합니다.
* **연계 실행 (Next Action)**: 즉시 복사하여 사용할 수 있는 실물 파이썬 템플릿을 확인하려면 [guide.page_template_standard_py](.agents/context/guide/page_template_standard.py) 코드를 확인하십시오. (상대 경로: [page_template_standard.py](.agents/context/guide/page_template_standard.py))

## Connections
* **상위 개념**: [guide.readme](.agents/context/guide/guide-index.md)
* **연관 자산**:
  - [.agents/rules/L3-dashboard.md](.agents/rules/L3-dashboard.md)
  - [.agents/context/guide/coding-templates.md](.agents/context/guide/coding-templates.md)
  - [.agents/context/guide/page_template_standard.py](.agents/context/guide/page_template_standard.py)

---

이 가이드는 모든 대시보드 화면 컨트롤러 파일(`*_page.py`)이 일관된 품질을 확보하고 높은 가독성과 유지보수성을 가질 수 있도록 개발 표준과 구조적 코드 템클릿을 정의합니다.

이 문서는 프로젝트의 UI 설계 단일 진실 공급원(SSOT)의 일부이며, 개발을 시작하기 전에 반드시 탐독하고 준수해야 합니다.

---

## 1. 핵심 3대 설계 철학 (Core Design Philosophy)

### ① 단일 책임 및 물리 격리 (Single Responsibility & Isolation)
- `*_page.py` 파일은 화면의 레이아웃을 잡고 필터를 제어하며 위젯을 화면에 표출하는 **화면 컨트롤러(Controller & Layout)** 역할만 전담합니다.
- 데이터베이스 조회 및 Pandas 전처리는 **서비스 레이어([.agents/rules/L3-service.md](.agents/rules/L3-service.md))**에 위임합니다.
- 복잡한 Plotly 피규어 구성 및 스타일 차트 그리기는 **시각화 레이어([.agents/rules/L3-plot.md](.agents/rules/L3-plot.md))**에 위임합니다.

### ② 이모지 전면 사용 금지 및 Material Icons 표준화 (Strict Emoji-Free Policy)
- 탭 라벨, 마크다운 텍스트, 버튼, 로그 및 소스 코드 내 주석을 포함한 대시보드 전 영역에서 유니코드 이모지(예: 💡, 🚀, 📋, ⚠️, ❌)의 사용을 금지합니다.
- 아이콘이 필요한 영역에는 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`) 또는 UI 컴포넌트의 전용 파라미터(`material_icon:icon_name`)만을 사용합니다.

### ③ 일방향 의존성 흐름 수호 (Unidirectional Dependency Flow)
- 의존성의 흐름은 항상 **[UI Page -> Service -> Query]** 순서로 흘러야 합니다. 
- UI 레이어가 데이터베이스에 직접 접근하거나 쿼리를 단독 실행하는 역방향 혹은 격벽 파괴 흐름은 엄격히 규제됩니다.

---

## 2. 렌더링 함수 생성 기준 (Rendering Function Criteria)

가독성과 성능 향상을 위해 화면 드로잉 코드는 단일 진입점에 몰아넣지 않고, 명확한 가상 계층 구조로 모듈화하여 쪼개어 구현합니다.

```
Main Render Loop (메인 렌더링 진입점)
   │
   ├── render_header_section()   # 1. 상단 공통 헤더/서머리 보드
   │
   └── st.tabs() (탭 라우터)
         │
         ├── render_overview_tab()     # 2. 탭 레벨 렌더러 (Overview)
         │     ├── _render_kpi_cards()      # 2-1. 복잡할 경우 세부 섹션 분리
         │     └── _render_main_plots()     # 2-2. 복잡할 경우 세부 섹션 분리
         │
         └── render_details_tab()      # 3. 탭 레벨 렌더러 (Details) -> @st.fragment 격리
               └── _render_raw_table()
```

### ① 탭 단위 분할 렌더링 (Tab-based Rendering)
- 대시보드의 개별 메인 탭에 대응하는 별도의 탭 레벨 렌더링 함수(`render_overview_tab`, `render_trend_tab` 등)를 반드시 단독 선언합니다.
- 메인 루프에서는 탭을 생성하고 선택된 탭 컨테이너 내부에서 각 탭 레벨 함수를 호출하는 역할만 부여합니다.

### ② 세부 섹션 분할 렌더링 (Section-based Rendering)
- 하나의 탭 내부가 200줄 이상으로 길어지거나 복잡한 그리드 배치, 다중 카드가 존재하는 경우, 해당 탭 렌더러 안에서 하위 섹션 함수군(예: `_render_kpi_cards`, `_render_trend_plots`)으로 추가 세분화하여 호출합니다.
- 세부 섹션 함수는 모듈 외부 노출을 막기 위해 반드시 언더바 접두사(`_`)를 붙여 프라이빗 헬퍼 형태로 선언합니다.

### ③ 프래그먼트 독립 렌더링 (@st.fragment)
- 특정 섹션 내의 인터랙티브 위젯(필터, 멀티셀렉트, 정렬 버튼 등) 조작 시, 페이지 전체를 Rerun 하지 않고 해당 섹션만 초고속 로컬 렌더링하도록 탭 또는 세부 섹션 함수 단위에 `@st.fragment` 데코레이터를 적용합니다.
- 데이터 로드 비용과 네트워크 과금을 비약적으로 절감하고 데스크톱 앱과 같은 즉각적이고 매끄러운 UX를 선호합니다.

---

## 3. 화면 처리 표준 7단계 순서 (Execution Order Standards)

모든 `*_page.py` 파일은 일관된 작업 흐름을 갖추기 위해 다음 7단계의 코드 빌드 순서를 엄격히 준수하여 순차적으로 작성해야 합니다. 
특히, 각 단계 및 주요 기능적 구역의 시작점은 코드의 가독성과 탐색 효율을 비약적으로 높이기 위해 **반드시 통일된 주석 장식 블록(섹션 타이틀 하이라이트) 양식을 사용하여 시각적으로 강조**해야 합니다.

* **표준 섹션 주석 예시**:
  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  ```

### **[1단계] imports (라이브러리 및 종속성 배치)**
- 외부 패키지 ➔ 공통 디자인/코어 UI ➔ 비즈니스 서비스 ➔ 1:1 플롯 레이어 순서로 질서 있게 수입합니다.

### **[2단계] Page Config & Styles (초기화)**
- `st.set_page_config()`를 가장 먼저 선언한 뒤 `load_css()` 공통 테마 스타일시트를 호출합니다.

### **[3단계] Session State Interception (세션 가로채기)**
- Streamlit에서 동적으로 위젯 키의 값을 코드 상에서 초기화하거나 수정할 때 `StreamlitAPIException`이 발생하는 것을 방지하는 핵심 가드 레일입니다.
- 위젯이 화면에 기동(인스턴스화)되기 직전 영역에서, `st.session_state` 키의 존재 여부를 파악하여 백업 변수에 할당하고 해당 키를 임시로 삭제하거나 사전 설정하는 기법을 일관되게 활용합니다.

### **[4단계] Sidebar Inputs & Params Assembly (입력 및 규격화)**
- 사용자가 조작하는 필터를 사이드바(`st.sidebar`) 내부에 배치합니다.
- 입력값들은 서비스 레이어로 낱개로 흩뿌려 전달하지 않고, 반드시 `core/params/parameters.py` 내의 도메인 전용 파라미터 데이터클래스(`*Params`) 객체로 패킹 및 조립합니다.

### **[5단계] Data Loading & Defenses (데이터 호출 및 방어막)**
- 데이터 조회 중 대기 시간을 가시화하기 위해 반드시 `st.spinner()` 구조 아래에서 서비스 레이어 전처리 함수를 호출합니다.
- 서비스 함수는 과금 폭증을 제어하기 위해 반드시 백엔드 캐싱(`@st.cache_data`)이 적용되어 있어야 합니다.
- **[방어막 수립]** 데이터가 존재하지 않거나 빈 데이터프레임이 리턴된 경우, 화면이 깨지는 것을 차단하기 위해 `st.warning("데이터가 없습니다.")` 안내 메시지와 함께 `st.stop()`을 실행시켜 뒤의 UI 렌더러 기동을 즉각 중지(Short-Circuit)합니다.

### **[6단계] Modular Rendering Functions (비주얼 컴포넌트 선언)**
- 상단 정의된 렌더링 함수 생성 기준에 맞춰 탭 및 섹션별 렌더링 함수를 정형적으로 작성합니다.
- `app/core/ui/components.py` 내의 검증된 공통 컴포넌트(`header_main_title_info_panel`, `subheader_title_stats_panel`, `metric_card_vertical`)를 적극 활용합니다.

### **[7단계] Main Render Loop (라우터 가동 및 조립)**
- 최종 메인 렌더링 루프를 구성합니다. 타이틀 헤더를 호출하고, `st.tabs()` 객체를 연동하여 위에서 선언한 렌더러 함수들을 각각의 탭 영역에 매핑하고 앱을 최종 전개합니다.

---

## 4. 재사용 유틸 및 핵심 도구 활용 규칙

### ① 동적 컬럼 설정기 (`get_dynamic_column_configs` 필수 연동)
- 화면에서 데이터 테이블을 표출(`st.dataframe`)할 때 영문 물리 컬럼명을 수동으로 하나하나 한글 별칭으로 AS 하드코딩하거나 딕셔너리를 인라인으로 쓰지 마십시오.
- 공통 헬퍼인 `get_dynamic_column_configs("테이블키", df.columns)`를 바인딩하면, 로컬 JSON 데이터 사전과 연동하여 정밀한 한글 표시명, 소숫점 표시 자리수, 도움말 툴팁까지 완벽히 포맷팅된 `column_config`를 자동 반환합니다.
- 적용 수칙 예시:
  ```python
  from app.core.boilerplate_column_config import get_dynamic_column_configs

  # 'cqms_qi_mttc' 테이블의 메타데이터와 연동
  configs = get_dynamic_column_configs("cqms_qi_mttc", df.columns)
  st.dataframe(df, column_config=configs, use_container_width=True, hide_index=True)
  ```

### ② Plotly 시각화 격리 규칙
- `*_page.py` 내에서 Plotly 차트 드로잉 및 디테일 레이아웃 조율을 하드코딩하지 않습니다.
- 차트 드로잉은 무조건 1:1 대칭 매핑인 `*_plots.py` 내부의 드로잉 함수(예: `viz.draw_*_chart()`)를 기동하여 Figure 객체를 반환받아 화면 단에서는 `st.plotly_chart(fig)` 호출만 진행합니다.

---

## 5. 표준 소스 코드 템플릿 (Template File)

실제 프로덕션 화면을 개발할 때 복사하여 뼈대로 즉시 사용할 수 있는 표준화된 고품질 파일 템플릿 소스는 아래 상대 경로 링크에서 직접 다운로드하거나 참조할 수 있습니다.

- **완성된 파이썬 코드 소스**: [.agents/context/guide/page_template_standard.py](page_template_standard.py)
