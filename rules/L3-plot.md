---
id: rule.l3.plot
type: rule
status: active

summary: >
  L3 시각화/차트 개발 규칙.
  Plotly 기반 플롯 레이어(plots)의 역할과 제약(Streamlit 레이아웃 호출 금지, 비즈니스 가공 금지, 호버 옵션 최적화, Carbon DV 준수 등)을 정의한다.

keywords:
  - plotly
  - plot
  - chart
  - visualization
  - typography

parent: rule.readme

related:
  - rule.l2.color_system
  - rule.l3.dashboard

consumers:
  - agent.planner_orchestrator
  - agent.dashboard_layer_builder
  - agent.ui_reviewer

updated: 2026-06-28
---

# L3-plot.md (L3 시각화/차트 개발 규칙)

## Overview
* **왜 존재하는가 (Why)**: Plotly 차트 드로잉에 필요한 복잡한 시각적 설정(서체, 축, 범례, 색상)과 핵심 비즈니스 로직을 분리하고, IBM Carbon DV 및 디자인 시스템 표준을 보장하여 고도로 전문화되고 통일된 데이터 시각화를 제공하기 위함입니다.
* **언제 사용하는가 (When)**: `app/pages/` 하위에서 `*_plots.py` 파일을 작성하거나 차트 컴포넌트를 리팩토링할 때 상시 준수합니다.
* **연계 실행 (Next Action)**: 차트에 들어갈 정제된 데이터프레임을 생성하기 위해 [L3-service.md](.agents/rules/L3-service.md)의 서비스 레이어 연산 및 캐싱 규칙을 따르십시오.

## Connections
* **상위 개념**: [.agents/rules/L2-architecture.md](.agents/rules/L2-architecture.md)
* **연관 자산**: 
  - [.agents/rules/L3-dashboard.md](.agents/rules/L3-dashboard.md)
  - [.agents/rules/L2-color-system.md](.agents/rules/L2-color-system.md)
---

## 1. 플롯 레이어의 핵심 역할 및 위치
- **위치**: `app/pages/` 산하 각 페이지 폴더(예: `_10_dashboard/`)에 page 파일과 함께 동거
- **파일명**: `*_plots.py` 명명 규칙 준수
- **책임**: 넘겨받은 정제된 Pandas DataFrame을 활용하여 호버 텍스트 가공, 차트 디자인 세부 옵션을 설정하고 최적화된 **Plotly Figure 객체**를 드로잉 및 반환합니다.

---

## 2. 금지 규칙 (Strict Guardrails)
> [!IMPORTANT]
> 레이어 간 상호 작용 및 고수준 의존성 격벽 제약 조건은 단일 진실 공급원(SSOT)인 **[L2-architecture.md](.agents/rules/L2-architecture.md)**의 규칙을 엄격히 준수합니다.

1. **Streamlit 레이아웃 요소 호출 금지 (No Streamlit Layout in Plots)**:
   - `*_plots.py` 내부에서는 `st.write`, `st.columns`, `st.sidebar`, `st.metric` 등 화면 레이아웃 및 UI 요소를 렌더링하는 함수를 절대 호출할 수 없습니다. 오직 순수 시각화 차트 객체만을 생성하여 반환해야 합니다.
2. **비즈니스 가공 금지 (No Business Logic)**:
   - 플롯 파일 내부에서 데이터 원본 필터링, 복잡한 통계 수식 적용, 결측값 전처리 등 비즈니스 서비스 레이어의 역할을 침범하지 않습니다.
3. **Plotly 스펙 검증 규칙 준수 및 spikemode 하드코딩 금지 (Plotly Schema Compliance)**:
   - layout의 `xaxis` 또는 `yaxis` 객체 설정 시, `spikemode`에 `'vertical'` 또는 `'horizontal'`과 같이 표준 사양에 정의되지 않은 문자열을 임의 대입하는 것을 엄격히 금지합니다.
   - Plotly의 `spikemode` 속성은 오직 `'toaxis'`, `'across'`, `'marker'`의 단일 플래그 혹은 플러스로 조합된 값(예: `'toaxis+across'`)만을 허용합니다.
   - 축별로 마우스 hover 선이 생성되는 기본 방향은 Plotly 엔진이 네이티브하게 최적 처리하므로, 가급적 `spikemode` 속성은 생략하는 것을 권장합니다.

---

## 3. 시각화 개발 3대 표준
1. **시각화 전처리 샌드박스 경계 (Preprocessing Boundary)**:
   - 마우스 호버(Hover)용 툴팁 텍스트 조립, 플롯 디자인에 맞춘 Top-N 자르기 및 `Others` 그룹화, 그래프 축 포맷팅(Tickformat) 등 **시각화 레이아웃에 직접 결속된 포맷팅 가공**만 플롯 레이어 내에서 수행합니다.
2. **의미 중심의 차트 시맨틱 토큰 의무화 및 Carbon DV 철학 준수**:
   - 차트 마커나 라인 색상 지정 시 하드코딩된 임의의 헥사(Hex) 코드를 사용하는 것을 절대 금지하며, 단순 물리 컬러 토큰의 무분별한 직접 참조 또한 배제합니다.
   - 데이터 시각화의 모든 색상 사용 표준은 최상위 디자인 표준인 **[L2-color-system.md](.agents/rules/L2-color-system.md)**를 단일 진실 공급원(SSOT)으로 삼아 준수합니다.
   - 연도별 트렌드 분석 등 데이터 위계가 존재하는 차트는 계층형 시맨틱 차트 토큰(`chart_series_primary`, `chart_series_secondary`, `chart_series_tertiary`)을 반드시 대입하여 IBM Carbon Data Visualization의 계층화 철학을 따릅니다.
   - 규격선 및 임계선은 도메인 전용 토큰(`spec_limit`, `control_limit`, `target_line` 등)을 매핑하여 비즈니스 의미론을 명확히 전달합니다.
3. **인터랙티브 호버 옵션 최적화**:
   - 정적 이미지 차트가 아닌, 사용자 마우스 오버 시 풍부하고 직관적인 데이터를 제공하도록 `hover_data` 혹은 `hovertemplate` 옵션을 미려하게 커스텀 구성합니다.
   - 이때 가독성과 유지보수 편의성을 수호하기 위해 호버(Tooltip) 템플릿 명세는 외부 공통 설정을 참조하지 않고, 개별 시각화 함수 내에 직접 하드코딩(f-string 및 HTML 태그 사용)하여 명시적으로 제어합니다.

---

## 4. 표준 파일 명명 규칙 (Naming Standard)
- **차트 드로잉 파일**: `*_plots.py`
  - 반드시 화면 메인 컨트롤러(`*_page.py`)와 동일 디렉터리 내에서 1:1 대치 구조를 유지합니다.
  - 예: `cqms_dashboard_page.py`와 `cqms_dashboard_plots.py`

---

## 5. UI 및 시각화 리팩토링 제약 6대 수칙
에이전트가 Streamlit UI 및 Plotly 시각화 리팩토링을 수행할 때 반드시 다음 6대 수칙을 철저히 준수해야 합니다.
1. **컬러는 무조건 토큰화**: 모든 하드코딩된 HEX 코드, 색상 문자열 및 빌트인 컬러스케일은 반드시 `app/core/constants/ui.py` 내의 디자인 시스템 토큰(Colors)으로 일원화하여 참조합니다.
2. **Plotly는 컴포넌트화**: 개별 플롯 파일(`*_plots.py`) 내에 차트 드로잉 코드가 직접 노출되지 않도록 `app/core/plot/components.py` 등에 컴포넌트 클래스(Factory 패턴 등)로 캡슐화하여 공통 관리합니다.
3. **필요한 컬러가 없을 경우 토큰화 후 사용**: 디자인 시스템 상에 구현되어 있지 않은 신규 컬러가 필요할 경우, 코드 내에 직접 상수를 정의하지 말고 `app/core/constants/ui.py`에 물리 및 시맨틱 토큰으로 등록 후 간접 참조하여 사용해야 합니다.
4. **재사용할 컴포넌트가 없을 경우 기존 컴포넌트 기능 확장**: 완전히 동일한 컴포넌트가 없더라도 기존에 개발된 컴포넌트의 파라미터나 분기 처리를 개선(기능 확장)하여 해결할 수 있는지 최우선적으로 검토합니다.
5. **기능 확장이 안될 경우 컴포넌트 추가**: 기존 컴포넌트의 단순 확장으로 수용하기 힘든 완전히 다른 데이터 유형이나 프레젠테이션 스펙인 경우에 한해, 신규 컴포넌트 클래스를 추가 작성합니다.
6. **Layout 공통 요소는 요소별 컴포넌트 생성**: 타이틀, 범례, 그리드선, 축 스타일 등 Plotly 레이아웃을 구성하는 중복 제어 속성들은 개별 레이아웃 헬퍼 혹은 요소별 공통 컴포넌트 메서드로 분리 정의하여 재사용합니다.

---

## 6. 대시보드 플롯 서체 및 타이포그래피 정합 가이드 (Plotly Typography Harmony Guideline)
> [!IMPORTANT]
> 대시보드 내부의 모든 데이터 시각화 차트는 브랜드 디자인 일관성을 위해 반드시 폰트 종류, 크기, 색상이 사전에 정의된 표준 디자인 토큰 규격을 준수하여 렌더링되어야 합니다.

1. **차트 전용 스타일 헬퍼 (`apply_custom_chart_style`) 적용 필수**:
   - `*_plots.py` 내부에서 Plotly Figure 객체를 반환하기 직전에, 표준 타이포그래피 사양이 이식된 스타일 헬퍼를 무조건 호출해 피규어 객체의 테마를 갱신합니다.
   - **표준 폰트 스펙**:
     - **차트 대제목 (Title)**: 16px, `colors.slate_800`, Bold 스타일 (`get_font_family('display')` 연계)
     - **범례 항목 (Legend)**: 13px, `colors.slate_600`
     - **축 제목 (Axis Title)**: 13px, `colors.slate_500`
     - **축 데이터 눈금 라벨 (Tick Font)**: 12px, `colors.slate_400`
     - **내부 데이터 값 라벨 (Text Font)**: 13px, 표준 서체 패밀리 강제 동기화
   - **배경 처리 투명화 필수**:
     - 차트 카드가 배치되는 st.container 박스나 배경 패널과의 유연한 조화를 이루기 위해, `paper_bgcolor` 및 `plot_bgcolor` 속성은 항상 투명(`rgba(0,0,0,0)`)으로 강제 지정합니다.
2. **기존 플롯 함수의 간접 스타일 래핑 패턴(Decorator/Wrapper Pattern)**:
   - 외부 라이브러리나 다른 디렉터리에 배정된 플롯 모듈을 참조하여 재내보내기할 경우, 원본 파일의 소스 코드를 무분별하게 훼손하지 않기 위해 개별 호출 지점에서 데코레이터나 래핑 함수를 경유하여 반환하는 정합 패턴을 지향합니다.


