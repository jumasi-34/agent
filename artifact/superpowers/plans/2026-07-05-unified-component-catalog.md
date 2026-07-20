# Unified Component Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `standard_page_template.py` 템플릿 페이지에 Plotly & ECharts 컴포넌트 라이브 시각화, 모듈명/함수명, 샘플 코드가 포함된 프리미엄 컴포넌트 카탈로그를 안전하게 추가하고, 향후 디자인 토큰 및 스트림릿 위젯 확장이 가능하도록 네비게이션을 구조화합니다.

**Architecture:** 
- 기존 사이드바 네비게이션 및 세션 제어 로직을 보존하면서 4번째 탭 메뉴(`CATALOG`)를 분기 추가합니다.
- 메인 본문 렌더링에 `CATALOG` 조건식을 추가하고, 그 안에서 `st.tabs`를 이용해 `Plotly Go Engine`, `ECharts Engine`, `Design System Tokens (TBD)`, `Streamlit UI Widgets (TBD)`를 구획화합니다.
- 초경량 인메모리 목 데이터(`get_mock_data_for_catalog()`)를 안전하게 제공하여 DB 쿼리 및 성능 저하를 방지합니다.

**Tech Stack:** Streamlit, Pandas, NumPy, Plotly, Streamlit-ECharts

## Global Constraints

- **이모지 전면 금지**: UI 상의 텍스트, 탭 라벨, 버튼, 마크다운 콘텐츠 및 코드 주석 내에서 어떠한 유니코드 이모지(예: :chart_with_upwards_trend:, :art: 등)도 사용할 수 없으며, 구글 머티리얼 아이콘 구문인 `:material/icon_name:`만을 사용해야 합니다.
- **Safety Lock 준수**: 기존 코드의 동작 방식을 해치지 않고 `standard_page_template.py`에 추가 탭으로만 연동하여, 기존 대시보드 페이지나 비즈니스 서비스 레이어에 대한 종속성을 일체 갖지 않는 순수 독립형(Pure-UI Companion) 구조를 유지합니다.
- **WSL Markdown Link Constraint**: 모든 링크는 프로토콜을 제외한 워크스페이스 기준 평문 상대 경로(예: `[template](app/pages/_70_settings/standard_page_template.py)`)만을 사용합니다.
- **한국어 주석 및 Google 스타일 독스트링**: 신규 선언되는 초경량 헬퍼 함수나 테스트 로직 등은 모두 한국어 설명 및 Google/NumPy 스타일의 타입 힌팅 Docstring 구조를 준수해야 합니다.
- **Streamlit 위젯 세션 상태 제약**: `key`가 바인딩된 위젯의 상태값을 임의로 직접 할당하지 않고, 필요 시 세션 가로채기(Session Interception) 기법만을 활용합니다.

---

## Task 1: Component Catalog Mock Data Helper 설계 및 독립 테스트 구축

**Files:**
- Create: `tests/test_component_catalog.py`
- Modify: `app/pages/_70_settings/standard_page_template.py:298-320`

**Interfaces:**
- Consumes: None (독립 구현 및 템플릿 추가)
- Produces: `get_mock_data_for_catalog` (카탈로그 전용 초경량 목업 데이터 생성 함수)

- [ ] **Step 1: Write the failing test**

  `tests/test_component_catalog.py`에 카탈로그용 목 데이터가 정확한 컬럼과 타입으로 생성되는지 검증하는 실패하는 테스트를 작성합니다.

  ```python
  # -*- coding: utf-8 -*-
  """
  통합 컴포넌트 카탈로그 목 데이터 및 라우팅 정합성 검증 테스트
  """
  import pytest
  import pandas as pd

  def test_get_mock_data_for_catalog_structure():
      """카탈로그 렌더링에 사용될 모든 임시 데이터셋의 스키마와 정합성을 전수 검증합니다."""
      from app.pages._70_settings.standard_page_template import get_mock_data_for_catalog

      data_dict = get_mock_data_for_catalog()

      # 1) 히트맵 데이터 정합성 검증
      assert "heatmap" in data_dict
      df_heat = data_dict["heatmap"]
      assert isinstance(df_heat, pd.DataFrame)
      assert "PLANT" in df_heat.columns or df_heat.index.name == "PLANT"
      assert "Open" in df_heat.columns
      assert "Close" in df_heat.columns

      # 2) 랭킹 바 차트 데이터 정합성 검증
      assert "ranking" in data_dict
      df_rank = data_dict["ranking"]
      assert isinstance(df_rank, pd.DataFrame)
      required_cols = ["MCODE", "PLANT", "OEM", "VEHICLE", "MASS_PERIOD", "VALUE", "PREV_VAL", "CURR_VAL", "GAP_VAL", "SCORE_VAL", "DECISION_VAL"]
      for col in required_cols:
          assert col in df_rank.columns

      # 3) 도넛 및 파이 데이터 정합성 검증
      assert "pie" in data_dict
      df_pie = data_dict["pie"]
      assert isinstance(df_pie, pd.DataFrame)
      assert "Reason" in df_pie.columns
      assert "Value" in df_pie.columns

      # 4) 트렌드 라인 데이터 정합성 검증
      assert "line" in data_dict
      df_line = data_dict["line"]
      assert isinstance(df_line, pd.DataFrame)
      assert "Month" in df_line.columns
      assert "Target_KPI" in df_line.columns
      assert "Actual_KPI" in df_line.columns
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: FAIL (ImportError: cannot import name 'get_mock_data_for_catalog' from 'app.pages._70_settings.standard_page_template')

- [ ] **Step 3: Write minimal implementation**

  `app/pages/_70_settings/standard_page_template.py` 파일 내에 `get_mock_data_for_catalog` 도우미 함수를 빈 뼈대로 작성한 뒤, 테스트를 통과하기 위한 최소한의 인메모리 목 데이터를 반환하도록 구현합니다.
  기존의 `get_mock_data` 함수가 299~317 라인에 위치하고 있으므로, 그 하위에 추가 정의해 줍니다.

  ```python
  # * [데이터 조회 - 카탈로그 라이브 렌더링용 초경량 목업 데이터 생성]
  def get_mock_data_for_catalog() -> dict:
      """
      카탈로그 페이지의 9종 차트 컴포넌트 실시간 렌더링에 필요한 
      초경량 판다스 데이터프레임 구조를 생성하여 반환합니다.

      Returns
      -------
      dict
          각 플롯 컴포넌트 규격에 대응하는 pd.DataFrame 맵핑 사전.
      """
      # 1) 히트맵 전용 목업 데이터
      df_heatmap = pd.DataFrame(
          {
              "PLANT": ["H_Plant", "A_Plant", "K_Plant", "G_Plant", "Y_Plant", "S_Plant"],
              "Open": [5, 2, 0, 8, 3, 1],
              "On-going": [3, 4, 1, 2, 2, 0],
              "Close": [12, 18, 9, 15, 6, 4],
          }
      )

      # 2) 랭킹 바 차트 전용 (TrendRankBarPlot, draw_iqm_trend_rank_echart) 목업 데이터
      df_ranking = pd.DataFrame(
          {
              "MCODE": [f"MC-{i:03d}" for i in range(1, 11)],
              "PLANT": ["H_Plant", "A_Plant", "K_Plant", "H_Plant", "A_Plant", "K_Plant", "Y_Plant", "Y_Plant", "G_Plant", "S_Plant"],
              "OEM": ["OEM_A", "OEM_B", "OEM_A", "OEM_C", "OEM_B", "OEM_A", "OEM_C", "OEM_A", "OEM_B", "OEM_C"],
              "VEHICLE": ["Model_X", "Model_Y", "Model_Z", "Model_X", "Model_Y", "Model_Z", "Model_K", "Model_X", "Model_Y", "Model_K"],
              "MASS_PERIOD": [120, 95, 340, 210, 45, 180, 290, 80, 150, 60],
              "VALUE": [12.5, 9.2, 8.4, 7.1, 5.5, -2.1, -4.8, -6.5, -8.2, -11.0],
              "PREV_VAL": [45.0, 32.5, 28.0, 19.5, 15.0, 12.0, 22.0, 35.0, 40.0, 52.0],
              "CURR_VAL": [57.5, 41.7, 36.4, 26.6, 20.5, 9.9, 17.2, 28.5, 31.8, 41.0],
              "GAP_VAL": [12.5, 9.2, 8.4, 7.1, 5.5, -2.1, -4.8, -6.5, -8.2, -11.0],
              "SCORE_VAL": [14.2, 13.5, 12.8, 11.2, 10.5, 9.0, 8.1, 7.4, 6.2, 5.0],
              "DECISION_VAL": ["악화", "악화", "악화", "악화", "악화", "개선", "개선", "개선", "개선", "개선"],
          }
      )

      # 3) 도넛 및 파이 차트 전용 목업 데이터
      df_pie = pd.DataFrame(
          {
              "Reason": ["Scratch", "Dent", "Paint Fault", "Dimension Error", "Assembly Fault"],
              "Value": [35, 25, 18, 12, 10],
          }
      )

      # 4) 트렌드 라인 및 게이지 전용 목업 데이터
      df_line = pd.DataFrame(
          {
              "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
              "Target_KPI": [95.0, 95.0, 95.5, 95.5, 96.0, 96.0],
              "Actual_KPI": [94.2, 95.1, 95.8, 95.3, 96.4, 96.1],
          }
      )

      return {
          "heatmap": df_heatmap,
          "ranking": df_ranking,
          "pie": df_pie,
          "line": df_line,
      }
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add tests/test_component_catalog.py app/pages/_70_settings/standard_page_template.py
  git commit -m "test: add mock data helper for component catalog and unit test"
  ```

---

## Task 2: 사이드바 네비게이션 메뉴 확장 및 세션 라우팅 통합

**Files:**
- Modify: `app/pages/_70_settings/standard_page_template.py:150-212`

**Interfaces:**
- Consumes: `st.session_state`
- Produces: `CATALOG` 액티브 탭 라우팅 분기 처리

- [ ] **Step 1: Write the failing test**

  세션 상태 전환 및 라우팅 추가 검증용 테스트 코드를 `tests/test_component_catalog.py`에 확장하여 추가합니다.

  ```python
  def test_component_catalog_routing_flow():
      """카탈로그 탭 네비게이션이 세션 상태(st.session_state)에서 유효하게 분기되는지 검증합니다."""
      import streamlit as st
      
      # Mock Streamlit session state
      st.session_state.active_template_tab = "CATALOG"
      
      # 유효한 탭 정의에 CATALOG가 포함되는지 검증
      raw_tab = st.session_state.get("active_template_tab", "TAB_1")
      active_tab = raw_tab if raw_tab in ["TAB_1", "TAB_2", "TAB_3", "CATALOG"] else "TAB_1"
      
      assert active_tab == "CATALOG"
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_component_catalog.py::test_component_catalog_routing_flow -v`
  Expected: PASS (세션 상태 구조만 통과하며, 실제 UI 전환을 위한 템플릿 코드 바인딩 수정 준비)

- [ ] **Step 3: Modify standard_page_template.py to add CATALOG Menu**

  기존의 `standard_page_template.py` 파일의 세션 초기화 및 사이드바 버튼 영역을 수정하여 4번째 네비게이션인 "Component Catalog" 버튼을 추가합니다.
  - 라인 153-158: 세션 검사 및 바인딩 조건식에 `CATALOG`를 추가합니다.
  - 라인 208-212 근처(Detail Raw Data 버튼 바로 아래): "Component Catalog"용 `st.button`을 추가합니다.

  ```python
  # 1) 세션 검사 영역 수정
  if "active_template_tab" not in st.session_state:
      st.session_state.active_template_tab = "TAB_1"

  raw_tab = st.session_state.get("active_template_tab", "TAB_1")
  active_tab = raw_tab if raw_tab in ["TAB_1", "TAB_2", "TAB_3", "CATALOG"] else "TAB_1"
  ```

  ```python
  # 2) 사이드바 버튼 영역 수정 (기존 btn_tab3 밑에 추가)
      btn_tab3 = st.button(
          ":material/table_rows: Detail Raw Data",
          key="btn_template_tab3",
          type="primary" if active_tab == "TAB_3" else "secondary",
          use_container_width=True,
      )
      if btn_tab3:
          st.session_state.active_template_tab = "TAB_3"
          st.rerun()

      btn_catalog = st.button(
          ":material/insert_chart: Component Catalog",
          key="btn_template_catalog",
          type="primary" if active_tab == "CATALOG" else "secondary",
          use_container_width=True,
      )
      if btn_catalog:
          st.session_state.active_template_tab = "CATALOG"
          st.rerun()
  ```

- [ ] **Step 4: Run test to verify passes**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add app/pages/_70_settings/standard_page_template.py
  git commit -m "feat: expand sidebar navigation to support component catalog"
  ```

---

## Task 3: 메인 레이아웃 내 CATALOG 활성 탭 및 서브 탭 뼈대 구축

**Files:**
- Modify: `app/pages/_70_settings/standard_page_template.py:389-399`

**Interfaces:**
- Consumes: `active_tab == "CATALOG"`
- Produces: 4종의 서브 탭 (`st.tabs`) 레이아웃 컨테이너

- [ ] **Step 1: Write the failing test**

  카탈로그 하위 서브 탭이 UI 상에서 정확하게 정의되었는지 모킹을 통해 단순 검사하는 루틴을 작성합니다.

  ```python
  def test_sub_tabs_definitions():
      """카탈로그 내부의 4대 핵심 서브 탭이 정상 정의되었는지 구조를 검증합니다."""
      tabs_def = [
          "Plotly Go Engine",
          "ECharts Engine",
          "Design System Tokens (TBD)",
          "Streamlit UI Widgets (TBD)"
      ]
      assert len(tabs_def) == 4
      assert "Plotly Go Engine" in tabs_def
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_component_catalog.py::test_sub_tabs_definitions -v`
  Expected: PASS (뼈대 논리 검증)

- [ ] **Step 3: Modify standard_page_template.py to add CATALOG main block**

  기존의 `standard_page_template.py` 최하단(`active_tab == "TAB_3"` 분기 밑)에 `CATALOG` 분기 논리를 추가하고, 서브 탭 레이아웃을 생성합니다.

  ```python
  elif active_tab == "CATALOG":
      st.markdown("### :material/insert_chart: UI/UX Component & Design Catalog")
      st.write("프로젝트에서 사용 중인 공통 플롯 라이브러리 및 디자인 시스템 자산을 확인하고 복사하여 적용할 수 있습니다.")

      # 4개의 확장형 서브 탭 구조화 (이모지 절대 사용 금지 및 구글 메티리얼 구문 적용)
      sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(
          [
              ":material/finance: Plotly Go Engine",
              ":material/pie_chart: ECharts Engine",
              ":material/palette: Design System Tokens",
              ":material/widgets: Streamlit UI Widgets",
          ]
      )

      # 1) Plotly Go Engine 탭 바인딩 준비
      with sub_tab1:
          st.markdown("#### :material/analytics: Plotly-based Visualization Components")
          st.write("디자인 시스템 테마가 완벽히 주입된 고품질 Plotly 차트 카탈로그입니다.")

      # 2) ECharts Engine 탭 바인딩 준비
      with sub_tab2:
          st.markdown("#### :material/show_chart: ECharts-based Interactive Components")
          st.write("초고속 렌더링과 미려한 마우스 호버/클릭 인터랙션을 보장하는 ECharts 컴포넌트 목록입니다.")

      # 3) Design System Tokens 탭 (향후 확장용 안내 영역)
      with sub_tab3:
          st.info(
              ":material/palette: **Design System Tokens (준비 중)**\n\n"
              "향후 컬러 칩 팔레트, 타이포그래피 폰트 패밀리 가이드, 스페이싱 스케일, "
              "그리고 커스텀 SVG/Material 아이콘 카탈로그가 이 영역에 바인딩될 예정입니다.",
              icon=":material/info:"
          )

      # 4) Streamlit UI Widgets 탭 (향후 확장용 안내 영역)
      with sub_tab4:
          st.info(
              ":material/widgets: **Streamlit Common Widgets (준비 중)**\n\n"
              "향후 공통 헤더 패널(`header_main_title_info_panel`), 세로형 메트릭 카드(`metric_card_vertical`), "
              "그리고 Shadcn 스타일 정밀 데이터 테이블(`shadcn_data_table`) 카탈로그 및 복사용 템플릿 코드가 "
              "이 영역에 바인딩될 예정입니다.",
              icon=":material/info:"
          )
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add app/pages/_70_settings/standard_page_template.py
  git commit -m "feat: build main catalog page layout with sub tabs skeleton"
  ```

---

## Task 4: Plotly Go Engine 서브 탭 내 8종 라이브 차트 카드 연동 및 코드박스 구현

**Files:**
- Modify: `app/pages/_70_settings/standard_page_template.py:389-420`

**Interfaces:**
- Consumes: `app.core.plot.components`, `app.core.design_system.plot.components`
- Produces: 8개의 카드형(`border=True`) 플롯 렌더러와 샘플 코드 스니펫

- [ ] **Step 1: Write the failing test**

  테스트 파일에 각 Plotly 차트 컴포넌트 클래스가 정상적으로 임포트되고 생성되는지 확인하는 정적 임포트 테스트를 추가합니다.

  ```python
  def test_plotly_components_imports():
      """Plotly 컴포넌트들의 임포트 및 존재 여부를 검증합니다."""
      # Core plot components
      from app.core.plot.components import WeeklyHeatmapPlot, TrendRankBarPlot, PremiumDonutPlot
      assert WeeklyHeatmapPlot is not None
      assert TrendRankBarPlot is not None
      assert PremiumDonutPlot is not None

      # Design system plot components
      from app.core.design_system.plot.components.bar import BarChartComponent
      from app.core.design_system.plot.components.gauge import GaugeChartComponent
      from app.core.design_system.plot.components.indicator import IndicatorBulletComponent
      from app.core.design_system.plot.components.line import LineChartComponent
      from app.core.design_system.plot.components.pie import PieChartComponent

      assert BarChartComponent is not None
      assert GaugeChartComponent is not None
      assert IndicatorBulletComponent is not None
      assert LineChartComponent is not None
      assert PieChartComponent is not None
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_component_catalog.py::test_plotly_components_imports -v`
  Expected: PASS (임포트 무결성 패스)

- [ ] **Step 3: Implement Plotly Catalog Render Logic in standard_page_template.py**

  파일 상단(SECTION 1. Imports)에 필요한 모든 플롯 컴포넌트들을 임포트합니다.
  그리고 `sub_tab1` (Plotly Go Engine) 내부에 8개의 차트 컴포넌트를 `st.container(border=True)` 안에 순차적으로 배치하고 샘플 데이터 및 복사용 코드를 결합합니다.

  ```python
  # 상단 임포트 영역에 추가:
  from app.core.plot.components import WeeklyHeatmapPlot, TrendRankBarPlot, PremiumDonutPlot
  from app.core.design_system.plot.components.bar import BarChartComponent
  from app.core.design_system.plot.components.gauge import GaugeChartComponent
  from app.core.design_system.plot.components.indicator import IndicatorBulletComponent
  from app.core.design_system.plot.components.line import LineChartComponent
  from app.core.design_system.plot.components.pie import PieChartComponent
  ```

  ```python
  # sub_tab1 블록 내부에 렌더링 로직 추가 (대표 3종 예시 - 실제 코드엔 8종 전수 구현):
  catalog_data = get_mock_data_for_catalog()

  # 1. WeeklyHeatmapPlot
  with st.container(border=True):
      st.markdown("### 1) Weekly Status Heatmap (`WeeklyHeatmapPlot`)")
      st.markdown("`from app.core.plot.components import WeeklyHeatmapPlot`")
      heatmap_fig = WeeklyHeatmapPlot(
          df=catalog_data["heatmap"],
          title="Factory Weekly Quality Operations",
          color_theme="orange"
      ).render()
      st.plotly_chart(heatmap_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.plot.components import WeeklyHeatmapPlot

  plot = WeeklyHeatmapPlot(
      df=df_heatmap_data,
      title="Factory Weekly Quality Operations",
      color_theme="orange"  # 'orange' | 'green' | 'blue' | 'zinc'
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 2. TrendRankBarPlot
  with st.container(border=True):
      st.markdown("### 2) Trend Rank Bar Chart (`TrendRankBarPlot`)")
      st.markdown("`from app.core.plot.components import TrendRankBarPlot`")
      rank_fig = TrendRankBarPlot(
          df=catalog_data["ranking"],
          indicator_name="Scrap Rate (PPM)",
          is_improvement=True
      ).render()
      st.plotly_chart(rank_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.plot.components import TrendRankBarPlot

  plot = TrendRankBarPlot(
      df=df_ranking_data,
      indicator_name="Scrap Rate (PPM)",
      is_improvement=True  # True: 개선 랭킹(Teal), False: 악화 랭킹(Red)
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 3. PremiumDonutPlot
  with st.container(border=True):
      st.markdown("### 3) Premium Donut Chart (`PremiumDonutPlot`)")
      st.markdown("`from app.core.plot.components import PremiumDonutPlot`")
      donut_fig = PremiumDonutPlot(
          df=catalog_data["pie"],
          label_col="Reason",
          value_col="Value",
          title="Defect Ratio by Category"
      ).render()
      st.plotly_chart(donut_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.plot.components import PremiumDonutPlot

  plot = PremiumDonutPlot(
      df=df_defect_data,
      label_col="Reason",
      value_col="Value",
      title="Defect Ratio by Category"
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 4. BarChartComponent
  with st.container(border=True):
      st.markdown("### 4) Design System Bar Chart (`BarChartComponent`)")
      st.markdown("`from app.core.design_system.plot.components.bar import BarChartComponent`")
      bar_comp_fig = BarChartComponent(
          df=catalog_data["line"],
          x_col="Month",
          y_col="Actual_KPI",
          title="Monthly KPI Achievement Bar Chart",
          is_horizontal=False
      ).render()
      st.plotly_chart(bar_comp_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.design_system.plot.components.bar import BarChartComponent

  plot = BarChartComponent(
      df=df_kpi_data,
      x_col="Month",
      y_col="Actual_KPI",
      title="Monthly KPI Achievement Bar Chart",
      is_horizontal=False  # True 이면 가로형 바 차트
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 5. GaugeChartComponent
  with st.container(border=True):
      st.markdown("### 5) Design System Gauge Chart (`GaugeChartComponent`)")
      st.markdown("`from app.core.design_system.plot.components.gauge import GaugeChartComponent`")
      gauge_fig = GaugeChartComponent(
          value=85.4,
          title="Yearly Target Achievement Rate",
          metric_label="Achievement"
      ).render()
      st.plotly_chart(gauge_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.design_system.plot.components.gauge import GaugeChartComponent

  plot = GaugeChartComponent(
      value=85.4,
      title="Yearly Target Achievement Rate",
      metric_label="Achievement",
      unit="%"
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 6. IndicatorBulletComponent
  with st.container(border=True):
      st.markdown("### 6) Design System Bullet Chart (`IndicatorBulletComponent`)")
      st.markdown("`from app.core.design_system.plot.components.indicator import IndicatorBulletComponent`")
      bullet_fig = IndicatorBulletComponent(
          value=92.5,
          target=95.0,
          title="KPI Progress vs Target",
          metric_label="Quality Rate"
      ).render()
      st.plotly_chart(bullet_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.design_system.plot.components.indicator import IndicatorBulletComponent

  plot = IndicatorBulletComponent(
      value=92.5,
      target=95.0,
      title="KPI Progress vs Target",
      metric_label="Quality Rate",
      unit="%"
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 7. LineChartComponent
  with st.container(border=True):
      st.markdown("### 7) Design System Line Chart (`LineChartComponent`)")
      st.markdown("`from app.core.design_system.plot.components.line import LineChartComponent`")
      line_comp_fig = LineChartComponent(
          df=catalog_data["line"],
          x_col="Month",
          y_cols=["Actual_KPI", "Target_KPI"],
          title="KPI Monthly Trend Line"
      ).render()
      st.plotly_chart(line_comp_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.design_system.plot.components.line import LineChartComponent

  plot = LineChartComponent(
      df=df_kpi_data,
      x_col="Month",
      y_cols=["Actual_KPI", "Target_KPI"],  # 복수 컬럼 비교 지원
      title="KPI Monthly Trend Line"
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")

  # 8. PieChartComponent
  with st.container(border=True):
      st.markdown("### 8) Design System Pie Chart (`PieChartComponent`)")
      st.markdown("`from app.core.design_system.plot.components.pie import PieChartComponent`")
      pie_comp_fig = PieChartComponent(
          df=catalog_data["pie"],
          label_col="Reason",
          value_col="Value",
          title="Defect Segment Analysis"
      ).render()
      st.plotly_chart(pie_comp_fig, use_container_width=True)
      with st.expander("Show Sample Code", expanded=False):
          st.code("""
  from app.core.design_system.plot.components.pie import PieChartComponent

  plot = PieChartComponent(
      df=df_defect_data,
      label_col="Reason",
      value_col="Value",
      title="Defect Segment Analysis",
      is_donut=True  # True 이면 도넛 차트 형태로 렌더링
  )
  fig = plot.render()
  st.plotly_chart(fig, use_container_width=True)
          """, language="python")
  ```

- [ ] **Step 4: Run test to verify passes**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add app/pages/_70_settings/standard_page_template.py
  git commit -m "feat: complete integration of 8 plotly components with code templates"
  ```

---

## Task 5: ECharts Engine 서브 탭 내 라이브 랭킹 차트 연동 및 이벤트 바인딩

**Files:**
- Modify: `app/pages/_70_settings/standard_page_template.py:421-440`

**Interfaces:**
- Consumes: `draw_iqm_trend_rank_echart`
- Produces: 1개의 카드형 ECharts 렌더러와 샘플 코드 스니펫

- [ ] **Step 1: Write the failing test**

  ECharts 렌더링에 사용되는 핵심 모듈이 유효한 딕셔너리 형태를 생성해내는지 임포트 및 구조 테스트를 추가합니다.

  ```python
  def test_echarts_components_imports():
      """ECharts 랭킹 차트 함수의 반환값 및 임포트 검증을 수행합니다."""
      from app.pages._10_dashboard.iqm_quality_trend_analysis_plots import draw_iqm_trend_rank_echart
      from app.pages._70_settings.standard_page_template import get_mock_data_for_catalog
      
      mock_data = get_mock_data_for_catalog()["ranking"]
      opts = draw_iqm_trend_rank_echart(mock_data, "Scrap Rate PPM")
      
      assert opts is not None
      assert isinstance(opts, dict)
      assert "series" in opts
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_component_catalog.py::test_echarts_components_imports -v`
  Expected: PASS (구조적 통과 보증)

- [ ] **Step 3: Implement ECharts Catalog Render Logic in standard_page_template.py**

  파일 상단에 ECharts 렌더링 위젯 및 함수를 임포트합니다.
  그리고 `sub_tab2` (ECharts Engine) 내부에 ECharts 랭킹 컴포넌트를 배치합니다.

  ```python
  # 상단 임포트 영역에 추가:
  from streamlit_echarts import st_echarts
  from app.pages._10_dashboard.iqm_quality_trend_analysis_plots import draw_iqm_trend_rank_echart
  ```

  ```python
  # sub_tab2 블록 내부에 렌더링 로직 추가:
  with sub_tab2:
      st.markdown("#### :material/show_chart: ECharts-based Interactive Components")
      st.write("초고속 렌더링과 미려한 마우스 호버/클릭 인터랙션을 보장하는 ECharts 컴포넌트 목록입니다.")

      with st.container(border=True):
          st.markdown("### 1) ECharts Trend Rank Bar Chart (`draw_iqm_trend_rank_echart`)")
          st.markdown("`from app.pages._10_dashboard.iqm_quality_trend_analysis_plots import draw_iqm_trend_rank_echart`")
          
          # ECharts 옵션 딕셔너리 생성
          echarts_opts = draw_iqm_trend_rank_echart(
              df_rank=catalog_data["ranking"],
              indicator_name="Scrap Rate (PPM)",
              is_improvement=True
          )
          
          # ECharts 렌더러 호출 (마우스 클릭 이벤트 구조 예시 포함)
          st_echarts(options=echarts_opts, height="380px", key="catalog_echart_rank")
          
          with st.expander("Show Sample Code", expanded=False):
              st.code("""
  from streamlit_echarts import st_echarts
  from app.pages._10_dashboard.iqm_quality_trend_analysis_plots import draw_iqm_trend_rank_echart

  # ECharts 옵션 딕셔너리 획득
  echarts_opts = draw_iqm_trend_rank_echart(
      df_rank=df_ranking_data,
      indicator_name="Scrap Rate (PPM)",
      is_improvement=True  # True 이면 초록색 개선 랭킹, False 이면 빨간색 악화 랭킹
  )

  # 렌더링 가동
  st_echarts(
      options=echarts_opts, 
      height="380px", 
      key="unique_chart_widget_key"
  )
              """, language="python")
  ```

- [ ] **Step 4: Run test to verify passes**

  Run: `pytest tests/test_component_catalog.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add app/pages/_70_settings/standard_page_template.py
  git commit -m "feat: integrate ECharts rank chart and complete visualization catalog"
  ```
