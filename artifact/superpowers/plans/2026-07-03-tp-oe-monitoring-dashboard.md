# TP OE Monitoring 대시보드 신설 및 사이드바 통합 구현 계획서

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** TP OE Monitoring 페이지의 필터 제어 환경을 st.sidebar 로 통합하고, 첫 번째 탭에 생산 달성률, Scrap/Rework PPM 및 Uniformity 합격률을 요약한 실시간 KPI 카드 및 Plotly 혼합 추이 그래프를 렌더링하는 프리미엄 대시보드를 신설합니다.

**Architecture:** 
- 화면 뷰 레이어(Streamlit)인 `tp_oe_monitoring_page.py`와 순수 Plotly 드로잉 엔진인 `tp_oe_monitoring_plots.py`를 엄격히 물리 격리합니다.
- 데이터 렌더링 시 `app.core.design_system.tokens`의 컬러, 폰트 및 `light_theme`을 완전히 상속하여 배경을 투명화합니다.

**Tech Stack:** Streamlit, Plotly, Pandas, Pytest, Design System Tokens

## Global Constraints

- 모든 파이썬 소스 코드 주석 및 마크다운 파일 내에서는 유니코드 이모지(별, 로봇 등) 사용이 엄격히 금지됩니다. (아이콘 필요 시 오직 :material/icon_name: 만 허용)
- VS Code 터미널 및 채팅 마크다운 내 모든 하이퍼링크는 절대 경로가 아닌 평문 상대 경로(예: [.agents/AGENTS.md](../AGENTS.md))를 강제 엄수합니다.
- 모든 신규 생성/수정 모듈 및 함수는 한국어로 상세하고 가독성 높은 독스트링(Docstring)과 섹션 데코레이터를 구조화하여 명시해야 합니다.

---

### Task 1: 시각화 모듈 독립 및 기본 인터페이스 수립

**Files:**
- Create: `app/pages/_80_admin/tp_oe_monitoring_plots.py`
- Create: `tests/test_tp_oe_monitoring_plots.py`

**Interfaces:**
- Consumes: `app.core.design_system.plot.chart_helpers.create_empty_chart`
- Produces: 
  - `draw_production_trend_chart(df_daily: pd.DataFrame) -> go.Figure`
  - `draw_mcode_quality_chart(df_scrap: pd.DataFrame, df_rework: pd.DataFrame) -> go.Figure`

- [ ] **Step 1: 실패하는 TDD 테스트 코드 작성**
  빈 데이터 수신 시 어노테이션 메시지가 포함된 빈 차트(create_empty_chart)를 올바르게 생성해내는지 검증하는 단위 테스트를 선제 구현합니다.

  `tests/test_tp_oe_monitoring_plots.py` 작성:
  ```python
  import pandas as pd
  import plotly.graph_objects as go
  from app.pages._80_admin.tp_oe_monitoring_plots import (
      draw_production_trend_chart,
      draw_mcode_quality_chart,
  )

  def test_draw_production_trend_chart_empty():
      # 빈 데이터프레임 주입 시 빈 차트가 정상 반환되는가
      df = pd.DataFrame()
      fig = draw_production_trend_chart(df)
      assert isinstance(fig, go.Figure)
      assert len(fig.layout.annotations) > 0
      assert "No data" in fig.layout.annotations[0].text

  def test_draw_mcode_quality_chart_empty():
      # 빈 품질 데이터 주입 시 빈 차트가 정상 반환되는가
      df_scrap = pd.DataFrame()
      df_rework = pd.DataFrame()
      fig = draw_mcode_quality_chart(df_scrap, df_rework)
      assert isinstance(fig, go.Figure)
      assert len(fig.layout.annotations) > 0
      assert "No data" in fig.layout.annotations[0].text
  ```

- [ ] **Step 2: 테스트를 구동하여 실패하는지 정량적 검증**
  Run: `PYTHONPATH=. python -m pytest tests/test_tp_oe_monitoring_plots.py -v`
  Expected: FAIL (ModuleNotFoundError 또는 ImportError 발생)

- [ ] **Step 3: 최소 구현으로 모듈 인터페이스 및 빈 차트 대응 구조 안착**
  `app/pages/_80_admin/tp_oe_monitoring_plots.py` 작성:
  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import pandas as pd
  import plotly.graph_objects as go
  from app.core.design_system.plot.chart_helpers import create_empty_chart, validate_chart_data

  # * [대분류 - 일별 생산 실적 및 계획 대비 추이 차트 생성]
  def draw_production_trend_chart(df_daily: pd.DataFrame) -> go.Figure:
      """일별 생산 계획 대비 실적 추이를 비교 대조하는 혼합 차트를 빌드합니다.

      Parameters
      ----------
      df_daily : pd.DataFrame
          일별 생산 계획 및 실적 데이터프레임 (필수 컬럼: DATE, PLAN_QTY, ACTUAL_QTY)

      Returns
      -------
      go.Figure
          Plotly Figure 객체
      """
      if not validate_chart_data(df_daily, ["DATE", "PLAN_QTY", "ACTUAL_QTY"]):
          return create_empty_chart("Daily Production Trend", message="No data available for the selected week")
      
      # 임시 빈 차트
      return go.Figure()

  # * [대분류 - M-Code별 Scrap 및 Rework 품질 비교 차트 생성]
  def draw_mcode_quality_chart(df_scrap: pd.DataFrame, df_rework: pd.DataFrame) -> go.Figure:
      """M-Code별 Scrap 및 Rework 수량을 비교하는 누적 수평 막대 차트를 빌드합니다.

      Parameters
      ----------
      df_scrap : pd.DataFrame
          Scrap 불량 실시간 데이터프레임 (필수 컬럼: PRD_CD, DFT_QTY)
      df_rework : pd.DataFrame
          Rework 불량 실시간 데이터프레임 (필수 컬럼: PRD_CD, DFT_QTY)

      Returns
      -------
      go.Figure
          Plotly Figure 객체
      """
      has_scrap = validate_chart_data(df_scrap, ["PRD_CD", "DFT_QTY"])
      has_rework = validate_chart_data(df_rework, ["PRD_CD", "DFT_QTY"])
      
      if not has_scrap and not has_rework:
          return create_empty_chart("M-Code Quality PPM Comparison", message="No quality raw data available")
      
      # 임시 빈 차트
      return go.Figure()
  ```

- [ ] **Step 4: 테스트 재실행 및 완수 성공 확인**
  Run: `PYTHONPATH=. python -m pytest tests/test_tp_oe_monitoring_plots.py -v`
  Expected: PASS

- [ ] **Step 5: 원자적 로컬 깃 커밋 실행**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_plots.py tests/test_tp_oe_monitoring_plots.py
  git commit -m "[TEST] TP OE 시각화 plots 모듈 신설 및 빈 차트 TDD 구현"
  ```

---

### Task 2: Plotly 시각화 세부 구현 및 디자인 토큰 매핑

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_plots.py`
- Modify: `tests/test_tp_oe_monitoring_plots.py`

**Interfaces:**
- Consumes: 
  - `app.core.design_system.tokens.colors`
  - `app.core.design_system.tokens.carbon_categorical_list`
  - `app.core.design_system.plot.chart_helpers.create_hovertemplate`
- Produces: 완성형 `draw_production_trend_chart`, `draw_mcode_quality_chart` Figure 반환

- [ ] **Step 1: 실제 주입 데이터 가동 유효성 검증 테스트 케이스 보강**
  `tests/test_tp_oe_monitoring_plots.py`에 다음 테스트 추가:
  ```python
  def test_draw_production_trend_chart_with_data():
      df = pd.DataFrame([
          {"DATE": "2026-06-28", "PLAN_QTY": 1000, "ACTUAL_QTY": 900},
          {"DATE": "2026-06-29", "PLAN_QTY": 1200, "ACTUAL_QTY": 1150}
      ])
      fig = draw_production_trend_chart(df)
      assert isinstance(fig, go.Figure)
      # Trace가 2개 (Plan 바, Actual 라인) 생성되었는지 확인
      assert len(fig.data) == 2
      # 배경색이 투명(rgba) 처리되었는지 확인
      assert fig.layout.paper_bgcolor == "rgba(0,0,0,0)"

  def test_draw_mcode_quality_chart_with_data():
      df_scrap = pd.DataFrame([{"PRD_CD": "M1", "DFT_QTY": 10}])
      df_rework = pd.DataFrame([{"PRD_CD": "M1", "DFT_QTY": 5}])
      fig = draw_mcode_quality_chart(df_scrap, df_rework)
      assert isinstance(fig, go.Figure)
      assert fig.layout.plot_bgcolor == "rgba(0,0,0,0)"
  ```

- [ ] **Step 2: 테스트를 구동하여 실패 확인**
  Run: `PYTHONPATH=. python -m pytest tests/test_tp_oe_monitoring_plots.py -v`
  Expected: FAIL (AssertionError: fig.data 가 비어 있거나 배경색이 투명이 아님)

- [ ] **Step 3: Plotly 세부 데이터 드로잉 및 토큰 이식 구현 완료**
  `app/pages/_80_admin/tp_oe_monitoring_plots.py` 수정:
  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import pandas as pd
  import plotly.graph_objects as go
  from app.core.design_system.tokens import colors, carbon_categorical_list
  from app.core.design_system.plot.chart_helpers import (
      create_empty_chart, 
      validate_chart_data,
      create_hovertemplate
  )

  # * [대분류 - 일별 생산 실적 및 계획 대비 추이 차트 생성]
  def draw_production_trend_chart(df_daily: pd.DataFrame) -> go.Figure:
      """일별 생산 계획 대비 실적 추이를 비교 대조하는 혼합 차트를 빌드합니다."""
      if not validate_chart_data(df_daily, ["DATE", "PLAN_QTY", "ACTUAL_QTY"]):
          return create_empty_chart("Daily Production Trend", message="No data available for the selected week")
      
      fig = go.Figure()
      
      # 1. 계획수량 (Bar 차트 - 연한 slate 색상 적용)
      fig.add_trace(go.Bar(
          x=df_daily["DATE"],
          y=df_daily["PLAN_QTY"],
          name="Plan Qty (계획수량)",
          marker_color=colors.slate_200,
          hovertemplate=create_hovertemplate({"Plan Qty": ("y", "%{y:,.0f} EA")}, header="%{x}")
      ))
      
      # 2. 실제 생산량 (Line 차트 - 브랜드 주황색 적용)
      fig.add_trace(go.Scatter(
          x=df_daily["DATE"],
          y=df_daily["ACTUAL_QTY"],
          name="Actual Qty (실적수량)",
          mode="lines+markers",
          line=dict(color=colors.app_primary, width=3),
          marker=dict(size=8, color=colors.app_primary),
          hovertemplate=create_hovertemplate({"Actual Qty": ("y", "%{y:,.0f} EA")}, header="%{x}")
      ))
      
      # 레이아웃 세부 튜닝 및 배경 완전 투명화
      fig.update_layout(
          height=300,
          margin=dict(l=10, r=10, t=30, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          barmode="group",
          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
      )
      return fig

  # * [대분류 - M-Code별 Scrap 및 Rework 품질 비교 차트 생성]
  def draw_mcode_quality_chart(df_scrap: pd.DataFrame, df_rework: pd.DataFrame) -> go.Figure:
      """M-Code별 Scrap 및 Rework 수량을 비교하는 누적 수평 막대 차트를 빌드합니다."""
      has_scrap = validate_chart_data(df_scrap, ["PRD_CD", "DFT_QTY"])
      has_rework = validate_chart_data(df_rework, ["PRD_CD", "DFT_QTY"])
      
      if not has_scrap and not has_rework:
          return create_empty_chart("M-Code Quality (Defects)", message="No quality raw data available")
      
      # 데이터 취합 처리
      prd_list = []
      scrap_vals = {}
      rework_val = {}
      
      if has_scrap:
          df_s_grp = df_scrap.groupby("PRD_CD")["DFT_QTY"].sum()
          for prd, qty in df_s_grp.items():
              prd_list.append(prd)
              scrap_vals[prd] = qty
              
      if has_rework:
          df_r_grp = df_rework.groupby("PRD_CD")["DFT_QTY"].sum()
          for prd, qty in df_r_grp.items():
              if prd not in prd_list:
                  prd_list.append(prd)
              rework_val[prd] = qty
              
      prd_list = list(set(prd_list))
      
      y_data = prd_list
      x_scrap = [scrap_vals.get(p, 0) for p in prd_list]
      x_rework = [rework_val.get(p, 0) for p in prd_list]
      
      fig = go.Figure()
      
      # Scrap 수량 (Carbon 1순위 범주색: Purple-70)
      fig.add_trace(go.Bar(
          y=y_data,
          x=x_scrap,
          name="Scrap Qty",
          orientation="h",
          marker_color=carbon_categorical_list[0],
          hovertemplate=create_hovertemplate({"Scrap Qty": ("x", "%{x:,.0f} EA")}, header="%{y}")
      ))
      
      # Rework 수량 (Carbon 2순위 범주색: Cyan-50)
      fig.add_trace(go.Bar(
          y=y_data,
          x=x_rework,
          name="Rework Qty",
          orientation="h",
          marker_color=carbon_categorical_list[1],
          hovertemplate=create_hovertemplate({"Rework Qty": ("x", "%{x:,.0f} EA")}, header="%{y}")
      ))
      
      fig.update_layout(
          height=300,
          margin=dict(l=10, r=10, t=30, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          barmode="stack",
          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
      )
      return fig
  ```

- [ ] **Step 4: 테스트 재기동 및 통과 확인**
  Run: `PYTHONPATH=. python -m pytest tests/test_tp_oe_monitoring_plots.py -v`
  Expected: PASS

- [ ] **Step 5: 원자적 깃 커밋 실행**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_plots.py tests/test_tp_oe_monitoring_plots.py
  git commit -m "[FEAT] TP OE Plotly 데이터 추이 및 수평 막대 차트 구현 완수"
  ```

---

### Task 3: Streamlit 컨트롤러 사이드바 이전 통합 및 일별 생산 데이터 파이프라인 수립

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py`

**Interfaces:**
- Consumes: `app.service.gmes_df.preprocessing_gmes_production_plan_vs_actual`
- Produces: 사이드바 필터 및 세션 키 `df_prod_plan_daily` 데이터 영속화

- [ ] **Step 1: 기존 코드 및 사이드바 이전 부분 리팩토링 및 일별 적재 구현**
  - 기존 상단 컨테이너 필터 구문(`with st.container(border=True):` 및 일요일/토요일 계산 등)을 전면 제거합니다.
  - 이를 `st.sidebar` 하위 영역으로 이주시키고, `df_prod_plan_daily` 세션 상태가 조회 시점에 정상 업데이트되도록 주입합니다.

  `app/pages/_80_admin/tp_oe_monitoring_page.py` 내의 수정 영역 (L171-L308 부근 교체):
  ```python
  # =========================================================================
  # SECTION 5. Sidebar Filter Controller (사이드바 제어 컨트롤러)
  # =========================================================================
  with st.sidebar:
      st.markdown("### 조회 조건 설정")
      
      # 단일 날짜(Date)로 받아 그 날짜가 속한 주 전체를 계산
      target_date = st.date_input(
          "조회 기준 일자",
          value=datetime.date(2026, 6, 30),
          help="선택한 일자가 속해 있는 주간(일요일~토요일) 전체를 실적 조회 영역으로 자동 설정합니다."
      )
      
      spec_fg = st.selectbox(
          "스펙 구분 (Spec FG)",
          options=["KT", "HX"],
          index=0,
          help="조회 대상 규격 구분을 명시하십시오."
      )
      
      spec_types = st.multiselect(
          "스펙 타입 (Spec Type)",
          options=["X", "P", "V", "M", "S", "T"],
          default=["M", "S", "T"],
          help="조회할 규격 타입 범주를 다중 선택하십시오."
      )
      
      # 조회 실행 단추
      btn_query = st.button(
          "실시간 데이터 조회",
          type="primary",
          use_container_width=True,
          icon=":material/search:"
      )

  # 선택한 단일 날짜 기준 주간(일~토) 계산
  start_date_str = None
  end_date_str = None
  if target_date:
      sun_date = target_date - datetime.timedelta(days=(target_date.weekday() + 1) % 7)
      sat_date = sun_date + datetime.timedelta(days=6)
      start_date_str = sun_date.strftime("%Y%m%d")
      end_date_str = sat_date.strftime("%Y%m%d")

  # 세션 상태 사전 선언 (일별 데이터 세션 키 df_prod_plan_daily 추가)
  if "df_spec_rev" not in st.session_state:
      st.session_state["df_spec_rev"] = None
  if "df_prod_plan" not in st.session_state:
      st.session_state["df_prod_plan"] = None
  if "df_prod_plan_daily" not in st.session_state:
      st.session_state["df_prod_plan_daily"] = None
  if "df_scrap" not in st.session_state:
      st.session_state["df_scrap"] = None
  if "df_rework" not in st.session_state:
      st.session_state["df_rework"] = None
  if "df_uf" not in st.session_state:
      st.session_state["df_uf"] = None

  if btn_query:
      if not start_date_str or not end_date_str:
          st.error("조회 기준 일자를 올바르게 지정하여 주십시오.", icon=":material/error:")
      elif not spec_types:
          st.error("최소 하나 이상의 스펙 타입을 다중 선택 필터에 입력해 주십시오.", icon=":material/error:")
      else:
          with st.spinner("Databricks 실시간 데이터웨어하우스 연동 쿼리 수행 중..."):
              try:
                  # 1. 규격 개정 및 OE 매핑 적재
                  rev_params = GMESSpecMasterParams(
                      mcode_list=mcode_list,
                      spec_fg_list=spec_fg,
                      spec_type_list=spec_types
                  )
                  st.session_state["df_spec_rev"] = preprocessing_gmes_spec_oe_revision(rev_params)

                  # 2. 생산 파라미터 공통 생성
                  prod_params = ProductionParams(
                      mcode_list=mcode_list,
                      start_date=start_date_str,
                      end_date=end_date_str,
                      spec_fg_list=spec_fg,
                      spec_type_list=spec_types
                  )
                  
                  # [일별 원본 데이터 파이프라인 신설]
                  from app.service.gmes_df import preprocessing_gmes_production_plan_vs_actual
                  st.session_state["df_prod_plan_daily"] = preprocessing_gmes_production_plan_vs_actual(prod_params)
                  
                  # 3. 주별 계획 대비 실적 합산 및 적재
                  st.session_state["df_prod_plan"] = preprocessing_gmes_production_plan_vs_actual_weekly(prod_params)

                  # 4. Scrap 품질 데이터 적재
                  scrap_params = NonconformityParams(
                      mcode_list=mcode_list,
                      start_date=start_date_str,
                      end_date=end_date_str,
                      spec_fg_list=spec_fg,
                      spec_type_list=spec_types,
                      disposition_type="scrap",
                      view_mode="rawdata"
                  )
                  st.session_state["df_scrap"] = preprocessing_ncf_rawdata(scrap_params)

                  # 5. Rework 품질 데이터 적재
                  rework_params = NonconformityParams(
                      mcode_list=mcode_list,
                      start_date=start_date_str,
                      end_date=end_date_str,
                      spec_fg_list=spec_fg,
                      spec_type_list=spec_types,
                      disposition_type="rework",
                      view_mode="rawdata"
                  )
                  st.session_state["df_rework"] = preprocessing_ncf_rawdata(rework_params)

                  # 6. UF 품질 데이터 적재
                  uf_params = UniformityParams(
                      mcode_list=mcode_list,
                      start_date=start_date_str,
                      end_date=end_date_str,
                      spec_fg_list=spec_fg,
                      spec_type_list=spec_types,
                      view_mode="rawdata"
                  )
                  st.session_state["df_uf"] = preprocessing_uf_general_rawdata(uf_params)

              except Exception as e:
                  st.error(f"실시간 데이터 조회 중 오류가 발생했습니다: {str(e)}", icon=":material/error:")
                  st.session_state["df_spec_rev"] = None
                  st.session_state["df_prod_plan"] = None
                  st.session_state["df_prod_plan_daily"] = None
                  st.session_state["df_scrap"] = None
                  st.session_state["df_rework"] = None
                  st.session_state["df_uf"] = None
  ```

- [ ] **Step 2: 로컬 전체 통합 테스트 수행 및 이상 유무 점검**
  Run: `PYTHONPATH=. python -m pytest tests/test_tp_oe_monitoring.py -v`
  Expected: PASS (기존 통합 테스트가 에러 없이 잘 작동함)

- [ ] **Step 3: 원자적 깃 커밋 실행**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py
  git commit -m "[REFACTOR] 필터 컨트롤러 사이드바 이전 통합 및 일별 생산 데이터 수집 추가"
  ```

---

### Task 4: 첫 번째 대시보드 탭 (`tab0`) 종합 모니터링 대시보드 및 Plotly 위젯 연동

**Files:**
- Modify: `app/pages/_80_admin/tp_oe_monitoring_page.py`

**Interfaces:**
- Consumes: 
  - `app.pages._80_admin.tp_oe_monitoring_plots.draw_production_trend_chart`
  - `app.pages._80_admin.tp_oe_monitoring_plots.draw_mcode_quality_chart`
- Produces: 3개 탭 구성 및 "종합 모니터링 대시보드"의 KPI 메트릭 및 차트 연동 렌더링

- [ ] **Step 1: 3개 탭 리팩토링 및 tab0 대시보드 연동 구현**
  - 기존 `tab1, tab2 = st.tabs(["규격 및 실적 실시간 모니터링", "M-Code 관리 마스터"])` 라인을 3개 탭으로 수정하고 대시보드를 안착시킵니다.
  - 1층에 4개의 컬럼 구조 메트릭 카드 배치 및 수치(PPM, 달성률, 합격률) 계산식을 작성합니다.
  - 2층에 `draw_production_trend_chart`, `draw_mcode_quality_chart` 함수를 import하여 `st.plotly_chart`로 연동 렌더링합니다.

  `app/pages/_80_admin/tp_oe_monitoring_page.py` 수정 (탭 렌더링 영역 L150-L165 부근 교체):
  ```python
      # 3. 레이아웃 타이틀 렌더링 (이모지 전면 금지 규정 준수)
      st.title("TP OE Monitoring")
      st.markdown("---")
      
      # 탭 레이아웃 구성 (3개 탭으로 개편)
      tab0, tab1, tab2 = st.tabs(["종합 모니터링 대시보드", "규격 및 실적 실시간 모니터링", "M-Code 관리 마스터"])
      
      # 데이터베이스에서 실시간 데이터 로드 (공통 데이터 추출)
      dml = SQLiteDML("ops")
      df_specs_all = dml.fetch_query("SELECT * FROM tp_oe_spec_managemnt ORDER BY id DESC")
      mcode_list = [str(x).strip() for x in df_specs_all["m_code"].dropna().unique() if str(x).strip() != ""]

      # =========================================================================
      # TAB 0. 종합 모니터링 대시보드 (신설 시각화 탭)
      # =========================================================================
      with tab0:
          st.subheader("종합 실시간 모니터링 대시보드")
          st.markdown("생산 계획 달성 현황 및 종합 품질 지표(Scrap, Rework, Uniformity)를 시각적으로 요약 관측합니다.")
          
          df_plan = st.session_state.get("df_prod_plan")
          df_scrap = st.session_state.get("df_scrap")
          df_rework = st.session_state.get("df_rework")
          df_uf = st.session_state.get("df_uf")
          df_daily = st.session_state.get("df_prod_plan_daily")
          
          if df_plan is None or df_plan.empty:
              st.warning("등록된 M-Code 및 조회된 데이터가 존재하지 않습니다. 좌측 사이드바에서 '실시간 데이터 조회' 버튼을 먼저 클릭해 주십시오.", icon=":material/warning:")
          else:
              # --- [1층: Key KPI 메트릭 요약] ---
              # 수치 산출
              total_plan = df_plan["PLAN_QTY"].sum() if "PLAN_QTY" in df_plan.columns else 0.0
              total_act = df_plan["ACTUAL_QTY"].sum() if "ACTUAL_QTY" in df_plan.columns else 0.0
              achieve_rate = (100.0 * total_act / total_plan) if total_plan > 0 else 0.0
              
              total_scrap = df_scrap["DFT_QTY"].sum() if (df_scrap is not None and "DFT_QTY" in df_scrap.columns) else 0.0
              scrap_ppm = (total_scrap / total_act * 1000000.0) if total_act > 0 else 0.0
              
              total_rework = df_rework["DFT_QTY"].sum() if (df_rework is not None and "DFT_QTY" in df_rework.columns) else 0.0
              rework_ppm = (total_rework / total_act * 1000000.0) if total_act > 0 else 0.0
              
              total_uf = len(df_uf) if df_uf is not None else 0
              pass_uf = len(df_uf[df_uf["JDG"] == "OK"]) if (df_uf is not None and "JDG" in df_uf.columns) else 0
              uf_pass_rate = (100.0 * pass_uf / total_uf) if total_uf > 0 else 100.0
              
              # 메트릭 카드 4열 배치
              m_col1, m_col2, m_col3, m_col4 = st.columns(4)
              with m_col1:
                  st.metric(
                      label="생산 달성률",
                      value=f"{achieve_rate:.1f}%",
                      delta=f"{total_act:,.0f} / {total_plan:,.0f} EA"
                  )
              with m_col2:
                  st.metric(
                      label="Scrap 불량률",
                      value=f"{scrap_ppm:,.0f} PPM",
                      delta=f"{total_scrap:,.0f} EA",
                      delta_color="inverse"
                  )
              with m_col3:
                  st.metric(
                      label="Rework 불량률",
                      value=f"{rework_ppm:,.0f} PPM",
                      delta=f"{total_rework:,.0f} EA",
                      delta_color="inverse"
                  )
              with m_col4:
                  st.metric(
                      label="Uniformity 합격률",
                      value=f"{uf_pass_rate:.1f}%",
                      delta=f"{pass_uf:,.0f} / {total_uf:,.0f} 건"
                  )
                  
              st.markdown("---")
              
              # --- [2층: Plotly 차트 드로잉 및 이식] ---
              from app.pages._80_admin.tp_oe_monitoring_plots import (
                  draw_production_trend_chart,
                  draw_mcode_quality_chart,
              )
              
              c_col1, c_col2 = st.columns(2)
              with c_col1:
                  st.markdown("**주간 일별 계획 대비 실적 추이**")
                  fig_trend = draw_production_trend_chart(df_daily)
                  st.plotly_chart(fig_trend, use_container_width=True, key="dashboard_production_trend_plotly")
                  
              with c_col2:
                  st.markdown("**자재(M-Code)별 Scrap 및 Rework 품질 비교**")
                  fig_quality = draw_mcode_quality_chart(df_scrap, df_rework)
                  st.plotly_chart(fig_quality, use_container_width=True, key="dashboard_mcode_quality_plotly")
  ```

- [ ] **Step 2: 정량적 자가 검증 검사 (QA Quality Gate)**
  - `make verify` 또는 `python tests/verify_code.py`를 실행하여 아티팩트 마크다운 포맷 준수 및 소스 파일 내 이모지 완전 차단 여부 등 정적 정합성을 검증합니다.
  - `PYTHONPATH=. python -m pytest tests/`를 가동하여, 모든 전수 테스트 케이스가 무결하고 완벽하게 PASS 됨을 입증합니다.

- [ ] **Step 3: 원자적 깃 커밋 실행**
  ```bash
  git add app/pages/_80_admin/tp_oe_monitoring_page.py
  git commit -m "[FEAT] 대시보드 탭 KPI 메트릭 및 Plotly 시각화 연동 구현 완수"
  ```
