# GT/WT 탭 리팩토링 및 오차 분석 고도화 구현 계획서 (NCF Look & Feel 완벽 동기화 버전)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** STD 데이터 대비 +/- 2.5% 오차 범위를 기준으로 중량 데이터(G/T, W/T)의 오차율 및 종합 합격률을 가공하고, Analysis Method(IQM_PLUS, PERIOD, BP)의 분기 조건에 따라 NCF 탭과 완전히 동일한 Look & Feel(섹션 타이틀, 수평 3분할 그리드 배치, 메트릭 카드 테마)로 대시보드 화면을 동적으로 리팩토링 및 렌더링합니다.

**Architecture:** 
1. `app/service/data_analysis_df.py`에 원시 중량 계측 데이터를 로드하고 개별 타이어별 오차율(`DEVIATION_PCT`) 및 합격 여부(`JDG`)를 연산하는 전처리 함수를 추가합니다.
2. `app/pages/_20_analysis/data_analysis_plots_dev.py`에 단일 분포 히스토그램 플롯 함수를 신설하여 일반 모드 및 BP 전후 구간 분할 분포 렌더링을 유연하게 지원하고, 기존 시계열 트렌드 차트에 BP 세로 점선을 추가합니다.
3. `app/pages/_20_analysis/data_analysis_page_dev.py`에서 기존의 단순한 트렌드 단독 렌더러를 리팩토링하여 메트릭 카드 행, NCF 대칭 레이아웃(일반 모드: 1:2 수평 배치 / BP 모드: 1:1:2 수평 3분할 배치), 그리고 PRE vs POST 중량 통계 비교 요약 테이블을 정밀하게 배치합니다.

**Tech Stack:** Python, Streamlit, Pandas, Plotly, Pytest

## Global Constraints

* **Safety Lock 준수**: 사용자의 명시적인 직접 승인을 받은 범위 내에서만 코드를 안전하게 가공 및 적용합니다.
* **유니코드 이모지 절대 금지**: 마크다운, 버튼, 라벨, UI 텍스트, 주석 전수에서 유니코드 이모지를 직접 기입하지 않으며, 아이콘은 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용합니다.
* **WSL 경로 제약 준수**: 파일 하이퍼링크 작성 시 절대 경로(`file:///home/...`) 대신 워크스페이스 기준 평문 상대 경로만을 기재합니다.
* **한국어 주석 표준 엄수**: 소스 코드 내부의 모든 모듈, 클래스, 함수에 작성되는 독스트링 및 주석은 기본적으로 가독성 높은 한국어로 정성스럽고 명확하게 기술합니다.
* **섹션 구분 장식 표준 엄수**: 주요 레이아웃이나 단계를 선언할 때 통일된 주석 장식 블록 양식을 사용합니다.

---

### Task 1: 중량 원시 데이터 전처리 및 편차 분석 서비스 구현

**Files:**
* Create: `tests/service/test_data_analysis_df_gt_wt.py`
* Modify: `app/service/data_analysis_df.py:384-386` (신규 함수 추가)

**Interfaces:**
* Consumes: `IqmPlusParams` (M-Code, Date Range, BP Date 등), `gmes_df.preprocessing_weight_rawdata`
* Produces: `preprocess_gt_weight_raw(params: IqmPlusParams) -> pd.DataFrame`
  - 반환형: `PLANT`, `M_CODE`, `SPEC_CD`, `INS_DATE`, `STD_WGT`, `MRM_WGT`, `DEVIATION_PCT`, `JDG` 컬럼이 보장되는 데이터프레임.

- [ ] **Step 1: Write the failing test**
  `tests/service/test_data_analysis_df_gt_wt.py`에 원시 중량 데이터를 모킹하여 오차율 연산 및 합격(JDG) 필드가 +/- 2.5% 기준으로 올바르게 판정되는지 검증하는 테스트를 작성합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import pandas as pd
  import pytest
  from app.core.data_models.parameters import IqmPlusParams
  from app.service.data_analysis_df import preprocess_gt_weight_raw

  # =========================================================================
  # SECTION 2. Test Cases (G/T, W/T 중량 편차 분석 유닛 테스트)
  # =========================================================================
  def test_preprocess_gt_weight_raw_deviation_and_jdg(monkeypatch):
      """G/T, W/T 원시 데이터의 오차율 연산 및 +/- 2.5% 기준 JDG 판정 정합성을 검증합니다."""
      # (1) 모킹 데이터 준비
      mock_df = pd.DataFrame([
          {"PLANT": "P1", "M_CODE": "M1", "SPEC_CD": "S1", "INS_DATE": "20260713", "STD_WGT": 10.0, "MRM_WGT": 10.1},  # 오차율 +1.0% (합격)
          {"PLANT": "P1", "M_CODE": "M1", "SPEC_CD": "S1", "INS_DATE": "20260713", "STD_WGT": 10.0, "MRM_WGT": 10.25}, # 오차율 +2.5% (합격 경계)
          {"PLANT": "P1", "M_CODE": "M1", "SPEC_CD": "S1", "INS_DATE": "20260713", "STD_WGT": 10.0, "MRM_WGT": 10.3},  # 오차율 +3.0% (불합격)
          {"PLANT": "P1", "M_CODE": "M1", "SPEC_CD": "S1", "INS_DATE": "20260713", "STD_WGT": 10.0, "MRM_WGT": 9.75},  # 오차율 -2.5% (합격 경계)
          {"PLANT": "P1", "M_CODE": "M1", "SPEC_CD": "S1", "INS_DATE": "20260713", "STD_WGT": 10.0, "MRM_WGT": 9.7},   # 오차율 -3.0% (불합격)
      ])
      
      # (2) gmes_df 모듈의 중량 데이터 쿼리 함수를 가로채 모킹 데이터 반환하도록 설정
      from app.service import gmes_df
      monkeypatch.setattr(gmes_df, "preprocessing_weight_rawdata", lambda params: mock_df)
      
      # (3) 파라미터 정의 및 함수 호출
      params = IqmPlusParams()
      params.step1_basic_mcode = "M1"
      params.step1_basic_start_date_str = "20260701"
      params.step1_basic_end_date_str = "20260713"
      
      res = preprocess_gt_weight_raw(params)
      
      # (4) 정량적 통계 및 판정 결과 검증
      assert "DEVIATION_PCT" in res.columns
      assert "JDG" in res.columns
      
      # 오차율 검증 (float 오차 방지하기 위한 근사치 대조)
      assert abs(res.loc[0, "DEVIATION_PCT"] - 1.0) < 1e-5
      assert abs(res.loc[1, "DEVIATION_PCT"] - 2.5) < 1e-5
      assert abs(res.loc[2, "DEVIATION_PCT"] - 3.0) < 1e-5
      assert abs(res.loc[3, "DEVIATION_PCT"] - (-2.5)) < 1e-5
      assert abs(res.loc[4, "DEVIATION_PCT"] - (-3.0)) < 1e-5
      
      # 합격 여부(JDG) 검증 (1: 합격, 0: 불합격)
      assert res.loc[0, "JDG"] == 1
      assert res.loc[1, "JDG"] == 1
      assert res.loc[2, "JDG"] == 0
      assert res.loc[3, "JDG"] == 1
      assert res.loc[4, "JDG"] == 0
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/service/test_data_analysis_df_gt_wt.py -v`
  Expected: FAIL with "ImportError: cannot import name 'preprocess_gt_weight_raw' from 'app.service.data_analysis_df'"

- [ ] **Step 3: Write minimal implementation**
  `app/service/data_analysis_df.py` 내의 적절한 위치(예: `preprocess_gt_weight` 함수 주변)에 `preprocess_gt_weight_raw` 함수를 정의합니다.

  ```python
  # * [SERVICE - GT/WT 그린중량/가류중량 원천 가공 데이터 수집]
  @st.cache_data(ttl=1800)
  def preprocess_gt_weight_raw(params: IqmPlusParams) -> pd.DataFrame:
      """
      그린 타이어 및 가류 타이어의 원시 계측 데이터를 로드하고,
      각 개체별 기준 중량 대비 측정 오차율(DEVIATION_PCT) 및 +/- 2.5% 기준 합격 여부(JDG)를 가공합니다.

      Parameters
      ----------
      params : IqmPlusParams
          대시보드 검색 조건 및 상태 파라미터.

      Returns
      -------
      pd.DataFrame
          오차율 및 합격 여부가 추가 가공된 원시 중량 데이터프레임.
      """
      from app.core.data_models.parameters import GTWeightParams
      from app.service import gmes_df
      import numpy as np

      # (1) 원시 중량 데이터 쿼리용 파라미터 변환
      wt_params = GTWeightParams(
          view_mode=params.step1_basic_view_by,
          mcode_list=[params.step1_basic_mcode],
          start_date=params.step1_basic_start_date_str,
          end_date=params.step1_basic_end_date_str,
      )

      # (2) 원천 데이터 수집
      df_raw = gmes_df.preprocessing_weight_rawdata(params=wt_params)
      if df_raw.empty:
          return pd.DataFrame(columns=["PLANT", "M_CODE", "SPEC_CD", "INS_DATE", "STD_WGT", "MRM_WGT", "DEVIATION_PCT", "JDG"])

      df_raw = df_raw.copy()

      # (3) 오차율 (Deviation %) 및 합격 여부 (JDG) 필드 연산 수립
      # STD_WGT 분모 0 방지 방어 코드 가동
      valid_mask = (df_raw["STD_WGT"] != 0) & (df_raw["STD_WGT"].notna()) & (df_raw["MRM_WGT"].notna())
      df_raw["DEVIATION_PCT"] = 0.0
      df_raw.loc[valid_mask, "DEVIATION_PCT"] = (
          (df_raw.loc[valid_mask, "MRM_WGT"] - df_raw.loc[valid_mask, "STD_WGT"])
          / df_raw.loc[valid_mask, "STD_WGT"]
          * 100
      )

      # +/- 2.5% 오차율 이내를 합격(1), 그 외를 불합격(0)으로 판정
      df_raw["JDG"] = np.where(
          (df_raw["DEVIATION_PCT"] >= -2.5) & (df_raw["DEVIATION_PCT"] <= 2.5), 1, 0
      )

      return df_raw
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/service/test_data_analysis_df_gt_wt.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add tests/service/test_data_analysis_df_gt_wt.py app/service/data_analysis_df.py
  git commit -m "[FEAT] G/T 및 W/T 중량 오차 분석 원시 데이터 가공 전처리 함수 추가"
  ```

---

### Task 2: 중량 오차 분포 히스토그램 및 트렌드 차트 고도화 (NCF 대칭 사양)

**Files:**
* Create: `tests/pages/test_data_analysis_plots_gt_wt.py`
* Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`

**Interfaces:**
* Consumes: G/T & W/T 가공 데이터프레임
* Produces:
  - `fig_gt_weight_deviation_histogram(df: pd.DataFrame, title: str = "Weight Deviation Distribution", color: str | None = None) -> go.Figure`
  - `fig_gt_weight_trend(params: IqmPlusParams, df: pd.DataFrame, bp_date_str: str | None = None) -> go.Figure`

- [ ] **Step 1: Write the failing test**
  `tests/pages/test_data_analysis_plots_gt_wt.py`에 `fig_gt_weight_deviation_histogram` 함수가 단일 Plotly Figure 객체를 컬러 옵션이 지정된 채 정상 생성하는지 검증하는 테스트를 작성합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import pandas as pd
  import plotly.graph_objs as go
  from app.pages._20_analysis.data_analysis_plots_dev import fig_gt_weight_deviation_histogram

  # =========================================================================
  # SECTION 2. Test Cases (시각화 유닛 테스트)
  # =========================================================================
  def test_fig_gt_weight_deviation_histogram_creation():
      """오차율 분포 히스토그램 생성 및 컬러 테마 지정을 검증합니다."""
      # (1) 테스트용 데이터프레임 구성
      df = pd.DataFrame([
          {"DEVIATION_PCT": -1.0},
          {"DEVIATION_PCT": 0.5},
          {"DEVIATION_PCT": 3.0},
      ])
      
      # (2) 기본 히스토그램 생성 검증
      fig = fig_gt_weight_deviation_histogram(df, title="Test Distribution", color="#3b82f6")
      assert isinstance(fig, go.Figure)
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/pages/test_data_analysis_plots_gt_wt.py -v`
  Expected: FAIL with "ImportError: cannot import name 'fig_gt_weight_deviation_histogram' from 'app.pages._20_analysis.data_analysis_plots_dev'"

- [ ] **Step 3: Write minimal implementation**
  `app/pages/_20_analysis/data_analysis_plots_dev.py` 내에 `fig_gt_weight_deviation_histogram` 함수를 추가하고, 기존 `fig_gt_weight_trend`에 `bp_date_str` 세로선 처리 로직을 이식합니다.

  ```python
  # * [PLOT - G/T & W/T 중량 오차율 분포 히스토그램 렌더러]
  def fig_gt_weight_deviation_histogram(df: pd.DataFrame, title: str = "Weight Deviation Distribution", color: str | None = None) -> go.Figure:
      """
      그린중량 및 가류중량 오차율 데이터의 분포 히스토그램을 생성합니다.

      Parameters
      ----------
      df : pd.DataFrame
          DEVIATION_PCT 컬럼을 포함하는 중량 전처리 데이터프레임.
      title : str, optional
          차트 상단 제목. 기본값은 "Weight Deviation Distribution".
      color : str | None, optional
          히스토그램 마커 채우기 색상. 지정되지 않으면 기본 브랜드 슬레이트 회색을 사용합니다.

      Returns
      -------
      go.Figure
          Plotly 히스토그램 피규어 객체.
      """
      import plotly.graph_objs as go
      from app.core.design_system.tokens import colors
      
      fig = go.Figure()
      fill_color = color if color else colors.slate_700
      
      # 분포 히스토그램 트레이스 추가
      fig.add_trace(go.Histogram(
          x=df["DEVIATION_PCT"],
          name="Weight Deviation",
          xbins=dict(start=-5.0, end=5.0, size=0.2),
          marker_color=fill_color,
          opacity=0.8,
      ))
      
      # +/- 2.5% 규격 범위를 표시하기 위한 수직 경계선 어노테이션 추가
      for limit_val in [-2.5, 2.5]:
          fig.add_vline(
              x=limit_val,
              line_width=1.5,
              line_dash="dash",
              line_color=colors.orange_500,
              annotation_text=f"{limit_val}%",
              annotation_position="top",
              annotation_font=dict(color=colors.orange_500, size=10)
          )
          
      apply_shadcn_style_to_figure(fig, title=title, height=260)
      
      fig.update_layout(
          xaxis=dict(title="Deviation (%)", range=[-5.0, 5.0], tickfont=dict(color=colors.slate_700)),
          yaxis=dict(title="Count", gridcolor=colors.slate_200, tickfont=dict(color=colors.slate_700)),
          margin=dict(l=60, r=40, t=60, b=60),
          legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5, font=dict(color=colors.slate_700)),
      )
      
      return fig
  ```

  동일 파일 내의 `fig_gt_weight_trend` 함수(Line 1481)를 다음과 같이 수정 및 업데이트합니다:

  ```python
  # StartLine: 1481, EndLine: 1545 타겟 치환
  def fig_gt_weight_trend(params: IqmPlusParams, df: pd.DataFrame, bp_date_str: str | None = None) -> go.Figure:
      # Sort by PERIOD_ID in ascending order to display X-axis chronologically
      df = df.sort_values(by="PERIOD_ID", ascending=True)

      # 95% 미만인 Anomaly(결격) 시점에만 고시인성 오렌지 Accent 적용, 정상 시는 slate_900
      marker_colors = [
          colors.orange_500 if rate < 95.0 else colors.slate_900
          for rate in df["PASS_RATE"]
      ]

      # plotly line chart
      trace1 = go.Bar(
          x=df["PERIOD_ID"],
          y=df["WT_INS_QTY"],
          name="Total",
          marker=dict(color=colors.slate_300),  # 전체 수량은 흐린 무채색
          text=df["WT_INS_QTY"],
      )
      trace2 = go.Bar(
          x=df["PERIOD_ID"],
          y=df["WT_PASS_QTY"],
          name="Pass",
          marker=dict(color=colors.slate_700),  # 합격 수량은 주 Slate_700 무채색
          text=df["WT_PASS_QTY"],
      )
      trace3 = go.Scatter(
          x=df["PERIOD_ID"],
          y=df["PASS_RATE"],
          name="Pass Rate",
          mode="lines+markers",
          line=dict(color=colors.slate_900, width=2),  # 합격률 라인은 차분한 slate_900
          marker=dict(size=8, color=marker_colors),
          yaxis="y2",
      )

      fig = go.Figure([trace1, trace2, trace3])
      apply_shadcn_style_to_figure(fig, title="GT/WT Trend", height=260)
      
      # BP 모드일 경우 변경점 날짜 세로 점선 추가 수립
      if bp_date_str:
          fig.add_vline(
              x=bp_date_str,
              line_width=1.5,
              line_dash="dash",
              line_color=colors.orange_500,
              annotation_text="BP Date",
              annotation_position="top left",
              annotation_font=dict(color=colors.orange_500, size=10)
          )
          
      fig.update_layout(
          xaxis=dict(title="Period", type="category", tickfont=dict(color=colors.slate_700)),
          yaxis=dict(
              title="Count",
              rangemode="tozero",
              gridcolor=colors.slate_200,
              tickfont=dict(color=colors.slate_700),
          ),
          yaxis2=dict(
              title="Pass Rate (%)",
              overlaying="y",
              side="right",
              range=[0, 105],
              gridcolor=colors.slate_100,
              tickfont=dict(color=colors.slate_700),
          ),
          bargap=0.2,
          legend=dict(
              orientation="h",
              yanchor="top",
              y=-0.3,
              xanchor="center",
              x=0.5,
              font=dict(color=colors.slate_700),
          ),
          margin=dict(l=60, r=60, t=60, b=80),
      )
      return fig
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/pages/test_data_analysis_plots_gt_wt.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add tests/pages/test_data_analysis_plots_gt_wt.py app/pages/_20_analysis/data_analysis_plots_dev.py
  git commit -m "[FEAT] G/T 및 W/T 중량 오차 히스토그램 및 트렌드 기준선 시각화 기능 추가"
  ```

---

### Task 3: GT/WT 탭 렌더러 리팩토링 및 NCF 대칭 레이아웃(1:1:2) 완성

**Files:**
* Modify: `app/pages/_20_analysis/data_analysis_page_dev.py:1272-1302`

**Interfaces:**
* Consumes: `IqmPlusParams`, `preprocess_gt_weight_raw` 및 신설된 플롯 객체들
* Produces:
  - `_render_tab_gt_wt(params: IqmPlusParams) -> None` (리팩토링)
  - `_render_gt_wt_bp_compare_table(df_gt_raw: pd.DataFrame, bp_date_str: str) -> None` (신설 헬퍼)

- [ ] **Step 1: Write the failing test**
  `tests/pages/test_data_analysis_page_gt_wt.py`를 신설하여 UI의 렌더링 시 내부적으로 모킹된 메트릭이나 테이블이 에러 없이 출력 흐름을 타는지 검증하는 코드를 작성합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import pandas as pd
  import streamlit as st
  from app.core.data_models.parameters import IqmPlusParams
  from app.pages._20_analysis.data_analysis_page_dev import _render_tab_gt_wt

  # =========================================================================
  # SECTION 2. Test Cases (UI 탭 유닛 테스트)
  # =========================================================================
  def test_render_tab_gt_wt_flow(monkeypatch):
      """GT/WT 탭 UI 호출 시 예외 발생 없이 흐름이 정상 관통하는지 테스트합니다."""
      # (1) 모킹 함수 설정
      mock_raw_df = pd.DataFrame([
          {"INS_DATE": pd.Timestamp("2026-07-01"), "STD_WGT": 10.0, "MRM_WGT": 10.1, "DEVIATION_PCT": 1.0, "JDG": 1},
          {"INS_DATE": pd.Timestamp("2026-07-13"), "STD_WGT": 10.0, "MRM_WGT": 10.3, "DEVIATION_PCT": 3.0, "JDG": 0},
      ])
      
      # streamlit layout component 모킹으로 실제 브라우저 없는 CLI 환경 보장
      monkeypatch.setattr(st, "columns", lambda *args, **kwargs: [st.container() for _ in range(max(args[0] if isinstance(args[0], list) else [args[0]]))])
      
      from app.pages._20_analysis import data_analysis_page_dev
      monkeypatch.setattr(data_analysis_page_dev, "preprocess_gt_weight_raw", lambda params: mock_df_raw_handler())
      
      def mock_df_raw_handler():
          return mock_raw_df

      # (2) 실행 및 흐름 검증 (오류 없이 통과해야 함)
      params = IqmPlusParams()
      params.step0_selected_menu = "IQM_PLUS"
      params.step1_basic_mcode = "M1"
      
      try:
          _render_tab_gt_wt(params)
          flow_success = True
      except Exception as e:
          flow_success = False
          print(f"UI Flow Failed with exception: {e}")
          
      assert flow_success is True
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/pages/test_data_analysis_page_gt_wt.py -v`
  Expected: FAIL (구현 중인 preprocess_gt_weight_raw 연계 누락이나, UI 내부에서 raw dataframe을 호출하지 않고 기존의 df_gt_weight(집계)만 사용하기 때문)

- [ ] **Step 3: Write minimal implementation**
  `app/pages/_20_analysis/data_analysis_page_dev.py`의 `_render_tab_gt_wt` 함수를 전면 리팩토링하고 통계 비교 테이블 출력 헬퍼 함수를 추가합니다.

  ```python
  # StartLine: 1272, EndLine: 1302 타겟 치환
  # * [UI - GT/WT 탭 렌더러]
  def _render_tab_gt_wt(params: IqmPlusParams) -> None:
      """
      GT/WT (그린중량 및 가류중량) 탭의 콘텐츠를 다차원적으로 렌더링합니다.
      
      NCF 탭의 레이아웃(Feel & Look)과 동일하게 섹션 타이틀, 수평 분할 비율,
      그리고 메트릭 요약 카드를 연동 배치하여 고도의 일관성을 보장합니다.

      Parameters
      ----------
      params : IqmPlusParams
          대시보드 검색 조건 및 상태 파라미터.

      Returns
      -------
      None
          Streamlit 컴포넌트 출력 전용.
      """
      from app.service.data_analysis_df import preprocess_gt_weight_raw, preprocess_gt_weight
      
      # (1) 분석 데이터 수집 (시계열 집계 데이터 및 개별 원시 편차 데이터 일괄 수집)
      df_gt_agg = preprocess_gt_weight(params)
      df_gt_raw = preprocess_gt_weight_raw(params)
      
      # (2) 기본 메타정보 계산
      meta_info = _resolve_product_metadata(params.step1_basic_mcode)
      plant_val = meta_info["plant"]
      mcode_val = meta_info["mcode"]
      oem_val = meta_info["oem"]
      vehicle_val = meta_info["vehicle"]
      sop_date_str = meta_info["sop_date_str"]
      prod_period_str = meta_info["prod_period_str"]

      # (3) 종합 통계 연산
      total_inspected = len(df_gt_raw)
      if total_inspected > 0:
          total_pass = int(df_gt_raw["JDG"].sum())
          overall_pass_rate = (total_pass / total_inspected) * 100
          mean_deviation = float(df_gt_raw["DEVIATION_PCT"].mean())
          std_deviation = float(df_gt_raw["DEVIATION_PCT"].std()) if total_inspected > 1 else 0.0
      else:
          overall_pass_rate = 0.0
          mean_deviation = 0.0
          std_deviation = 0.0

      # (4) KPI 요약 메트릭 카드 페이로드 조립
      metrics_payload = [
          {"title": "Total Inspected", "value": f"{total_inspected:,.0f}", "description": "Total weight test count"},
          {"title": "Overall Pass Rate", "value": f"{overall_pass_rate:.2f}%", "description": "Within +/- 2.5% spec limit", "value_style": f"color: {colors.blue_600} !important;"},
          {"title": "Average Deviation", "value": f"{mean_deviation:+.2f}%", "description": "Avg weight offset percentage"},
          {"title": "Standard Deviation", "value": f"{std_deviation:.3f} %", "description": "Deviation spread (σ)"}
      ]

      # 프리미엄 공통 수치 카드 로우 렌더링 (NCF 테마 구조 및 블루 브랜드 테마 연계)
      premium_dashboard_metric_row(
          plant=plant_val,
          mcode=mcode_val,
          oem=oem_val,
          vehicle=vehicle_val,
          sop_date_str=sop_date_str,
          prod_period_str=prod_period_str,
          badge_bg_color=colors.blue_600,
          metrics=metrics_payload,
          defects=[],
          rank_color=colors.blue_600
      )
      
      st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
      
      # (5) 분석 모드(Method)에 따른 동적 레이아웃 구성 (NCF 수평 배열 및 3분할 비율 동기화)
      is_bp_mode = (params.step0_selected_menu == MENU_SELECT_DICT["BP"] and params.step1_basic_bp)
      
      # 트렌드 플롯 객체 생성
      fig_trend = plots.fig_gt_weight_trend(
          params, 
          df_gt_agg, 
          bp_date_str=params.step1_basic_bp_str if is_bp_mode else None
      )
      fig_trend.update_layout(title="")
      
      if is_bp_mode:
          bp_date_str = params.step1_basic_bp_str
          bp_dt = pd.to_datetime(bp_date_str)
          
          # PRE / POST 원시 데이터 분류
          df_raw_copy = df_gt_raw.copy()
          df_raw_copy["INS_DATE_DT"] = pd.to_datetime(df_raw_copy["INS_DATE"])
          df_pre = df_raw_copy[df_raw_copy["INS_DATE_DT"] < bp_dt]
          df_post = df_raw_copy[df_raw_copy["INS_DATE_DT"] >= bp_dt]
          
          # NCF와 100% 동일하게 1:1로 쪼갠 분포 히스토그램 생성
          fig_hist_before = plots.fig_gt_weight_deviation_histogram(df_pre, title="", color=colors.slate_400)
          fig_hist_after = plots.fig_gt_weight_deviation_histogram(df_post, title="", color=colors.blue_600)
          
          # 타이틀 전용 로우 (NCF 50:50 분할 정렬 동기화)
          header_cols = st.columns([2, 2], vertical_alignment="bottom")
          with header_cols[0]:
              render_section_title("Weight Deviation Comparison by Break Point")
          with header_cols[1]:
              render_section_title("GT/WT Pass Rate Trend")
              
          # 실제 차트 렌더링 로우 (NCF 1:1:2 수평 3분할 그리드 배치 완벽 동기화)
          cols = st.columns([1, 1, 2], vertical_alignment="top")
          with cols[0]:
              st.markdown("<p style='font-size:13px; font-weight:600; color:#64748b; margin-bottom:8px; text-align:center;'>Before Break Point</p>", unsafe_allow_html=True)
              st.plotly_chart(fig_hist_before, use_container_width=True, key="gt_weight_hist_before_chart")
          with cols[1]:
              st.markdown("<p style='font-size:13px; font-weight:600; color:#64748b; margin-bottom:8px; text-align:center;'>After Break Point</p>", unsafe_allow_html=True)
              st.plotly_chart(fig_hist_after, use_container_width=True, key="gt_weight_hist_after_chart")
          with cols[2]:
              st.plotly_chart(fig_trend, use_container_width=True, key="gt_weight_trend_bp_chart")
              
          st.divider()
          
          # Row 1.5: G/T & W/T 중량 통계 비교 요약 테이블 노출 (NCF Row 1.5 요약 표 구조 동기화)
          render_section_title("Weight Performance Summary by Break Point")
          _render_gt_wt_bp_compare_table(df_gt_raw, bp_date_str)
          
      else:
          # 일반 IQM_PLUS / PERIOD 모드: NCF 1:2 가로 렌더링 대칭 수립
          # 좌측 분포 히스토그램 (비율 1) / 우측 시계열 트렌드 차트 (비율 2) 수평 배치
          cols = st.columns([1, 2], vertical_alignment="top")
          with cols[0]:
              render_section_title("Weight Deviation Distribution")
              fig_hist = plots.fig_gt_weight_deviation_histogram(df_gt_raw)
              st.plotly_chart(fig_hist, key="gt_weight_hist_normal_chart", use_container_width=True)
          with cols[1]:
              render_section_title("GT/WT Pass Rate Trend")
              st.plotly_chart(fig_trend, key="gt_weight_trend_normal_chart", use_container_width=True)

      st.divider()


  # * [UI - GT/WT 탭 BP 전후 통계 대조 비교 테이블 추가]
  def _render_gt_wt_bp_compare_table(df_gt_raw: pd.DataFrame, bp_date_str: str) -> None:
      """
      Break Point 변경점 날짜를 기준으로 PRE 구간과 POST 구간의 중량 통계(수량, 합격률, 오차율 등)를 비교 대조하는 표를 출력합니다.

      Parameters
      ----------
      df_gt_raw : pd.DataFrame
          원시 가공 중량 데이터프레임.
      bp_date_str : str
          Break Point 일자 문자열 (YYYY-MM-DD 포맷).

      Returns
      -------
      None
          Streamlit 테이블 출력 전용.
      """
      import streamlit as st
      import pandas as pd

      if df_gt_raw.empty:
          st.info("No comparison data available.", icon=":material/info:")
          return

      # (1) PRE / POST 데이터 분할
      df = df_gt_raw.copy()
      df["INS_DATE_DT"] = pd.to_datetime(df["INS_DATE"])
      bp_dt = pd.to_datetime(bp_date_str)
      
      df_pre = df[df["INS_DATE_DT"] < bp_dt]
      df_post = df[df["INS_DATE_DT"] >= bp_dt]
      
      # (2) 통계치 연산 헬퍼 정의
      def _calc_stats(sub_df):
          n = len(sub_df)
          if n == 0:
              return 0, 0.0, 0.0, 0.0
          pass_rate = (sub_df["JDG"].sum() / n) * 100
          mean_dev = sub_df["DEVIATION_PCT"].mean()
          std_dev = sub_df["DEVIATION_PCT"].std() if n > 1 else 0.0
          return n, pass_rate, mean_dev, std_dev

      pre_n, pre_pass, pre_mean, pre_std = _calc_stats(df_pre)
      post_n, post_pass, post_mean, post_std = _calc_stats(df_post)
      
      # (3) 결과 딕셔너리 리스트 정렬
      metrics_data = [
          {
              "Metric": "Total Inspected (ea)",
              "Prior": f"{pre_n:,.0f}",
              "After": f"{post_n:,.0f}",
              "Diff": f"{(post_n - pre_n):+,.0f}"
          },
          {
              "Metric": "Pass Rate (%)",
              "Prior": f"{pre_pass:.2f}%",
              "After": f"{post_pass:.2f}%",
              "Diff": f"{(post_pass - pre_pass):+.2f}%p"
          },
          {
              "Metric": "Average Deviation (%)",
              "Prior": f"{pre_mean:+.2f}%",
              "After": f"{post_mean:+.2f}%",
              "Diff": f"{(post_mean - pre_mean):+.2f}%p"
          },
          {
              "Metric": "Standard Deviation (σ)",
              "Prior": f"{pre_std:.3f}%",
              "After": f"{post_std:.3f}%",
              "Diff": f"{(post_std - pre_std):+.3f}%p"
          }
      ]
      
      # Pandas DataFrame 변환
      df_table = pd.DataFrame(metrics_data)
      
      # CSS 테마 및 미니멀 보더를 강제화하여 프리미엄 테이블 출력
      st.markdown(
          f"""
          <style>
          .gt-wt-premium-table-container {{
              background: {colors.app_background};
              border: 1px solid {colors.app_border};
              border-radius: 0.375rem;
              padding: {spacing.space_3};
              font-family: {get_font_family('primary')};
          }}
          </style>
          <div class="gt-wt-premium-table-container">
          """,
          unsafe_allow_html=True
      )
      
      st.table(df_table.set_index("Metric"))
      st.markdown("</div>", unsafe_allow_html=True)
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/pages/test_data_analysis_page_gt_wt.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add tests/pages/test_data_analysis_page_gt_wt.py app/pages/_20_analysis/data_analysis_page_dev.py
  git commit -m "[FEAT] G/T 및 W/T 탭 레이아웃 전면 리팩토링 및 NCF Look & Feel 완벽 대칭 동기화"
  ```

---

## Self-Review

1. **Spec coverage:** 
   - STD 데이터 +/- 2.5% 기준 MRM_WGT 합격률 지표 연산 및 오차율 계산 -> Task 1의 `preprocess_gt_weight_raw`에서 구현.
   - 단일 오차율 분포 및 PRE/POST 오버랩 분포 히스토그램 구현 -> Task 2의 `fig_gt_weight_deviation_histogram`에서 구현.
   - Analysis Method 분기(IQM_PLUS, PERIOD, BP)에 따른 동적 UI 렌더링 -> Task 3의 `_render_tab_gt_wt` 리팩토링으로 구현 완료.

2. **Placeholder scan:** "TBD", "TODO", 생략 기호 없이 모든 함수의 실제 실행 가능한 코드 블록 전수 명시 완료.

3. **Type consistency:** parameter 형태(`IqmPlusParams`), Plotly Figure 타입, Pandas DataFrame 구조 및 컬럼명 (`DEVIATION_PCT`, `JDG`) 전반의 호환성 정합성 수립 완료.
