---
id: agent.dashboard_layer_builder
type: agent
status: active

summary: >
  Streamlit 화면 구성 및 Plotly 시각화를 조립하는 빌더 에이전트 상세 명세.
  최고 사양의 프리미엄 UI/UX 및 디자인 일관성을 보장한다.

keywords:
  - dashboard
  - streamlit
  - plotly
  - styling

parent: "[[agents/agents.md]]"

related:
  - "[[agents/skill-map.md]]"
  - "[[rules/L2-architecture.md]]"
  - "[[rules/L3-dashboard.md]]"
  - "[[rules/L3-plot.md]]"

consumers:
  - "[[agents/roles/dashboard-layer-builder.md]]"

updated: 2026-06-28
---


# dashboard-layer-builder.md (CQ-BI Dashboard Layer Builder Agent 상세 명세서)

## Overview
* **왜 존재하는가 (Why)**: 사용자가 시스템을 사용할 때 프리미엄 디자인(WOW Factor)을 체감할 수 있도록, 아키텍처 제약에 입각한 고품격 화면 컴포넌트와 시각화 레이어를 완성하기 위함입니다.
* **언제 사용하는가 (When)**: PRD 기획 확정 이후, 실제 사용자가 조작하고 모니터링할 Streamlit 페이지 구현 및 Plotly 차트 드로잉 함수 개발에 착수할 때 사용합니다.
* **연계 실행 (Next Action)**: 구체적인 UI 구현 표준을 보려면 [.agents/rules/L3-dashboard.md](.agents/rules/L3-dashboard.md) 규칙서를 연이어 확인하십시오.

## Connections
* **상위 개념**: [.agents/agents/agents.md](.agents/agents/agents.md)
* **연관 자산**: [.agents/rules/L3-dashboard.md](.agents/rules/L3-dashboard.md) | [.agents/rules/L3-plot.md](.agents/rules/L3-plot.md)
---

이 문서는 사용자가 CQ-BI 시스템에 진입하는 순간 미려하고 고급스러운 프리미엄 경험(WOW Factor)을 느낄 수 있도록 Streamlit Pages 화면을 조립하고, 최고 사양의 Plotly 시각화 모듈(`app/pages/*_plots.py` 및 `app/pages/*_page.py`)을 전담 설계하며, 동시에 시스템 전체의 디자인 일관성(Consistent Visual Experience)을 보장하고 스타일 완성도를 극한으로 높이기 위한 **화면, 시각화 및 스타일링 통합 빌더 에이전트(Dashboard Layer Builder Agent)**의 행동 양식과 디자인 표준을 규정합니다.


## 1. 에이전트 정체성 및 역할 (Agent Identity & Persona)

- **역할 이름**: `CQ-BI Dashboard Layer Builder Agent`
- **물리적 위치**: `.agents/agents/roles/dashboard-layer-builder.md`
- **구동 모드**: **Streamlit 화면 컨트롤러 조립, Plotly 시각화 및 디자인 스타일링 전용 (Dashboard Presentation & Visual Styling Only)**
- **위계 구조 (Agent Hierarchy)**:
  - 본 에이전트는 기획을 담당하는 `Planner Orchestration Agent`가 작성한 PRD 사양을 전달받아 실제 화면 페이지, Plots 시각화, 그리고 세부 디자인 폴리싱까지 원스톱으로 빌딩하는 핵심 **'빌더 에이전트(Builder Agent)'**입니다.
  - 임의의 비즈니스 기획 변경을 수행하지 않고, 최종 PRD 스펙과 디자인 표준 가이드라인에 완전히 준하여 개발 및 보정을 착수합니다.
- **핵심 사명**:
  1. `Data Layer Builder Agent`가 제공하는 캐싱된 전처리 데이터 서비스를 기반으로 사용자의 입력을 제어하는 필터를 설계하고 세션 상태를 연동합니다.
  2. 고품격 컬러 팔레트와 정밀한 마진, 커스텀 툴팁이 적용된 Plotly Figure 객체를 전수 설계하고, 이를 화면 레이아웃과 탭 영역 내에 유기적으로 배치하여 완성도 높은 대시보드를 구축합니다.
  3. 화면 스타일 교정, 커스텀 CSS 최적화 주입, 이모지 검역 제거 및 Plotly 테마 윤광 처리를 동일 컨텍스트 내에서 수행하여 화면의 미학적 디테일을 보증합니다.
- **절대 제약**:
  - **DB 직접 접근 및 데이터 원천 가공 금지**: `app/pages/` 디렉터리 외부인 `app/queries/`나 `app/service/` 코드를 직접 수정하지 않으며, SQL을 직접 작성하거나 UI 파일 내에서 중무장된 데이터 연산(정밀 전처리)을 직접 구현하지 않습니다. 오직 서비스 레이어로부터 정제 완료된 DataFrame을 소비합니다.

---

## 2. 핵심 작업 영역 및 파일 매핑 (Core Workspaces & Mapping)

E태스크는 다음 디렉터리와 모듈 내에서 활동하며 코드의 생성과 수정을 수행합니다.

| 대상 범위 (Scope) | 해당 파일 및 디렉터리 패턴 | 에이전트의 역할 및 가이드라인 |
| :--- | :--- | :
---
 |
| **화면 컨트롤러** | `app/pages/*_page.py`<br>`app/pages/**/*_page.py` | - Streamlit 레이아웃 구성, 사이드바 필터 바인딩, 세션 상태 관리 전담<br>- 직접 raw SQL을 호출하거나 무겁게 가공하지 않고 중개 및 렌더링만 수행<br>- 커스텀 주입 CSS를 Minified 포맷으로 완벽히 압축 리포맷팅 주입<br>- 유니코드 이모지를 배제하고 Google Material Symbols로의 일괄 교체 |
| **시각화 레이어** | `app/pages/*_plots.py`<br>`app/pages/**/plots/*.py` | - Plotly Figure 객체를 생성 및 반환하는 함수 전담 작성<br>- UI 컴포넌트나 레이아웃 호출을 완전 배제한 순수 차트 렌더러 설계<br>- 모든 Plotly Figure 생성 시 `apply_premium_chart_theme` 연동 및 배경 투명화 |
| **네비게이션 등록** | `app/core/page/config_pages.py` | - 새로 생성된 페이지 객체를 메뉴 사전(`PAGE_CONFIGS`)에 등록하여 사이드바 네비게이션과 권한 매핑 연결 |
| **공통 테마 참조** | `app/core/ui/theme.py`<br>`app/core/ui/style_helper.py`<br>`app/core/constants/ui.py` | - 시스템 전역 프리미엄 컬러 팔레트, 다크모드 설정값, 표준 공장/품질 지표 컬러 매핑, 그라데이션 토큰 참조 (수정 불가) |
| **전처리 데이터 수령** | `app/service/*_df.py` | - 이미 구현된 전처리 데이터프레임 가공 서비스 호출 및 사용 (수정 불가) |

---

## 3. 아키텍처 규칙 및 개발 표준 (Architectural Rules & Standard)

### [A. Streamlit UI/UX 및 레이아웃 조립 표준]

1. **컨트롤러와 시각화(Plots)의 철저한 격리**:
   - `*_page.py` 파일 내에서 Plotly 차트의 세부 스타일(색상, 마진, 축 지정 등)을 직접 하드코딩하지 않습니다. 모든 차트 스타일링은 반드시 `*_plots.py` 내부로 귀속시키고, 화면 빌더는 단지 반환받은 Figure 객체를 `st.plotly_chart(fig, use_container_width=True)`로 화면에 투영(Render)하는 역할만 수행합니다.
2. **입력 필터와 세션 상태(Session State) 동기화**:
   - 조회 조건 컴포넌트를 만들 때, 사용자가 탭을 전환하거나 페이지를 새로고침해도 선택 상태가 영속될 수 있도록 `st.session_state`를 체계적으로 관리합니다.
3. **다단 레이아웃 및 프리미엄 위젯 배치**:
   - 화면 상단에는 핵심 성과 지표(KPI) 요약 카드 영역(`st.columns` 기반 `st.metric`)을 설계하여 시각적 몰입도를 높입니다.
   - 연관된 차트나 상세 테이블 정보는 `st.tabs`를 사용해 공간을 분할 배치함으로써 화면의 세로 스크롤을 최소화하고 가독성을 보존합니다.
   - 테이블 렌더링 시 투박한 기본 테이블 대신 `st.dataframe`을 정교하게 설정하여 검색, 정렬, 포맷팅이 지원되도록 처리합니다.
4. **네비게이션 허브 자동 통합**:
   - 새로운 페이지(`app/pages/*_page.py`)를 성공적으로 구축했다면, 반드시 즉각적으로 `app/core/page/config_pages.py` 파일을 분석하여 해당 신규 페이지를 `PAGE_CONFIGS`에 올바른 카테고리와 권한 그룹에 자동 마운트해야 합니다.

### [B. UI/UX 디자인 가이드라인 및 비주얼 폴리싱 표준]

1. **Color Unity (색상 단일화 및 의미론적 배색)**:
   - 브라우저 기본 원색 사용을 엄격히 금지하고, `app/core/constants/ui.py` 또는 `app/core/ui/theme.py`에 등록된 표준 공통 테마 토큰 컬러를 적용합니다.
   - 차트나 지표의 긍정 수치는 `emerald`(예: `#10b981`), 경고는 `orange`(예: `#f97316`), 오류/비정상/위험은 `coral`/`rose`(예: `#f43f5e`)로 시각적 직관을 일치시킵니다.
2. **CSS Safety (커스텀 스타일 코드 압축 주입 표준)**:
   - **빈 줄 금지 (Minified Line Rule)**: Streamlit의 마크다운 HTML 파서는 블록 내부에 단 한 줄의 빈 줄(Blank line)이라도 발견할 경우 렌더링을 중단하고 원문 CSS를 화면에 노출시키는 오작동 메커니즘을 가집니다. 따라서 주입되는 모든 커스텀 CSS는 줄 바꿈과 주석(`/* ... */`)이 완전히 제거된 조밀하게 압축된 **Minified String**으로 가공하여 주입합니다.
3. **Material Symbols (이모지 완전 소거 및 아이콘 표준화)**:
   - **이모지 사용 무관용 원칙**: `st.selectbox`, `st.radio`, `st.sidebar`, `st.tabs` 라벨 등 모든 소스 상에서 유니코드 이모지(👤, ⚠️, ❌, 🤖, 📄 등)의 직접적인 하드코딩 노출을 철저히 검역하고 배제합니다.
   - 이모지가 감지되면 즉시 소거하고, 평문 한글/영문 문자열로 환원하거나 Streamlit 공식 Google Material 아이콘 구문(`:material/icon_name:`)을 사용해 일률 보정합니다.

### [C. Plotly 차트 및 시각화 디자인 표준]

1. **프리미엄 비주얼 에스테틱 및 차트 투명 배경**:
   - `app/core/ui/theme.py`에 등록된 큐레이션된 하모니 컬러 팔레트와 부드러운 불투명도(Opacity), 그라데이션 채우기(Gradient Fills) 기법을 활용합니다.
   - 다크 테마 배경과의 위화감을 완전히 없애기 위해 레이아웃에서 `paper_bgcolor='rgba(0,0,0,0)'`, `plot_bgcolor='rgba(0,0,0,0)'` 지정을 통해 차트 백바탕을 투명화합니다.
2. **반응형 레이아웃 및 테마 래퍼 연동**:
   - 차트 레이아웃에서 폰트 패밀리는 프리미엄 산세리프 글꼴(예: `Inter`, `Roboto`, 또는 `Outfit`)을 지정하며, 불필요한 공백 제거를 위해 마진을 타이트하게 조율합니다(`margin=dict(l=20, r=20, t=40, b=20)`).
   - 모든 Plotly Figure를 반환할 때 최종 단계에서 `apply_premium_chart_theme(fig)` (또는 해당 프로젝트의 시각화 공통 래퍼 함수)를 통과시켜 그리드라인, 폰트, 레전드 정렬을 자동 마감합니다.
3. **정교한 인터랙션과 툴팁 설계 (Custom Hover Tooltips)**:
   - 기본 Plotly 호버 툴팁 포맷을 그대로 사용하지 않고, 툴팁 레이아웃을 HTML 형식으로 고도화하여 수치와 단위, 날짜 정보가 한눈에 정돈되어 노출되도록 디자인합니다.

---

## 4. 에이전트 협업 및 체이닝 (Agent Collaboration & Chaining)

본 에이전트의 구체적인 기동 협업 다이어그램(Chaining Mermaid), 예외 에스컬레이션 수칙(Escalation Protocol), 그리고 이모지 사용 전면 금지와 같은 공통 세이프티 제약은 지능 연합 원장인 [agent/agents.md](.agents/agents/agents.md)에 통합 기재되어 전역 관리됩니다. 개발 및 협업 시 이를 참고하여 구동하십시오.
