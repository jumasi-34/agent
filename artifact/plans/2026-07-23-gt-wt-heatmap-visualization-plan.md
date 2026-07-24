# GT/WT 복합 시각화 (히트맵 & 그룹 바 차트) 구현 계획서 (2026-07-23)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GT/WT 탭 하단에 기준 중량(`STD_WGT`) & 성형기(`BLDG_MC`) 복합 집계 데이터를 효과적으로 파악하기 위한 Plotly 히트맵(C안) 및 그룹형 바 차트(A안)를 탑재하고 화면 레이아웃에 연동합니다.

**Architecture:** 
1. `plots_data_analysis.py`에 원시 중량 데이터를 전달받아 히트맵 및 바 차트용 Plotly Figure 객체를 생성하는 함수 `fig_gt_weight_heatmap` 및 `fig_gt_weight_grouped_bar`를 정의합니다.
2. `renderer_gt_wt.py` 컨트롤러에서 이 함수들을 호출하고, `st.plotly_chart`를 사용해 하향 인지 분석 흐름에 따라 배치합니다.
3. 관련 단위 테스트들을 추가 및 보강하여 기능과 흐름의 무결성을 전수 검증합니다.

**Tech Stack:** Python 3.12, Pandas, Plotly, Streamlit, Pytest

## Global Constraints

* **이모지 사용 전면 금지**: 차트 타이틀, 버튼 라벨, 설명 등 모든 영역에 일반 유니코드 이모지 기입을 금지합니다.
* **디자인 토큰 엄수**: 차트 스타일링 시 `colors.orange_500`, `colors.blue_600` 등의 전역 색상 토큰을 준수하고, 반환 직전 `apply_shadcn_style_to_figure(fig)`를 반드시 실행합니다.
* **Streamlit 분리 정책**: 플롯 드로잉 모듈(`plots_data_analysis.py`) 내부에서는 어떠한 Streamlit 호출(`st.*`)도 금지합니다.

---

## File Structure

- Modify: `app/pages/_20_analysis/data_analysis/plots_data_analysis.py`
  - 플롯 드로잉 책임: 복합 히트맵 및 그룹 바 차트 빌드 및 스타일 주입.
- Modify: `app/pages/_20_analysis/data_analysis/renderer_gt_wt.py`
  - 레이아웃 및 렌더링 책임: 집계 뷰 최하단에 신규 두 차트(히트맵, 바 차트)와 집계 테이블 배치.
- Modify: `tests/pages/test_data_analysis_page_gt_wt.py`
  - 테스트 책임: 새로운 차트 렌더링 호출 흐름을 모킹하여 UI 렌더링 정상 관통 여부 검증.

---

### Task 1: Plotly 복합 차트 드로잉 구현 (`plots_data_analysis.py`)

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis/plots_data_analysis.py`
- Modify: `tests/pages/test_data_analysis_plots_gt_wt.py`

**Interfaces:**
- Produces: `fig_gt_weight_heatmap(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure`
- Produces: `fig_gt_weight_grouped_bar(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure`

- [ ] **Step 1: `test_data_analysis_plots_gt_wt.py` 에 실패하는 테스트 작성**
  ```python
  import pandas as pd
  import plotly.graph_objects as go
  from app.pages._20_analysis.data_analysis.plots_data_analysis import fig_gt_weight_heatmap, fig_gt_weight_grouped_bar

  def test_gt_weight_heatmap_and_bar_creation():
      mock_df = pd.DataFrame([
          {"INS_DATE": pd.Timestamp("2026-07-01"), "STD_WGT": 10.0, "BLDG_MC": "MC01", "MRM_WGT": 10.1, "JDG": 1},
          {"INS_DATE": pd.Timestamp("2026-07-13"), "STD_WGT": 10.0, "BLDG_MC": "MC01", "MRM_WGT": 10.3, "JDG": 0},
      ])
      fig_hm = fig_gt_weight_heatmap(mock_df, "NCF")
      fig_bar = fig_gt_weight_grouped_bar(mock_df, "NCF")
      assert isinstance(fig_hm, go.Figure)
      assert isinstance(fig_bar, go.Figure)
  ```

- [ ] **Step 2: 테스트를 수행하여 실패(ImportError 등) 확인**
  Run: `pytest tests/pages/test_data_analysis_plots_gt_wt.py -v`
  Expected: FAIL

- [ ] **Step 3: `plots_data_analysis.py` 내부에 두 차트 생성 핵심 로직 구현**
  ```python
  def fig_gt_weight_heatmap(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure:
      """성형기 x 규격(기준중량) 매트릭스를 그리는 히트맵을 생성합니다."""
      if df_gt_raw.empty or "BLDG_MC" not in df_gt_raw.columns:
          fig = go.Figure()
          return apply_shadcn_style_to_figure(fig)

      # 1. 집계 계산
      import numpy as np
      df = df_gt_raw.copy()
      df_agg = df.groupby(["STD_WGT", "BLDG_MC"], as_index=False).agg(
          Inspected_Qty=("JDG", "count"),
          Passed_Qty=("JDG", "sum")
      )
      df_agg["Pass_Rate"] = np.where(
          df_agg["Inspected_Qty"] > 0,
          (df_agg["Passed_Qty"] / df_agg["Inspected_Qty"]) * 100.0,
          0.0
      )
      
      # 2. Pivot 처리하여 2D Grid 형태로 가공
      # Y축(기준 중량)은 시인성을 위해 내림차순 정렬
      df_pivot = df_agg.pivot(index="STD_WGT", columns="BLDG_MC", values="Pass_Rate").sort_index(ascending=False)
      df_ins_pivot = df_agg.pivot(index="STD_WGT", columns="BLDG_MC", values="Inspected_Qty").sort_index(ascending=False)
      df_pass_pivot = df_agg.pivot(index="STD_WGT", columns="BLDG_MC", values="Passed_Qty").sort_index(ascending=False)
      
      x_vals = df_pivot.columns.astype(str).tolist()
      y_vals = [f"{v:.3f} kg" for v in df_pivot.index.tolist()]
      z_vals = df_pivot.values.tolist()
      
      # Cell Annotation Text 생성: "98.5% (985/1k)"
      annotation_text = []
      for r_idx in range(len(df_pivot)):
          row_text = []
          for c_idx in range(len(df_pivot.columns)):
              p_rate = z_vals[r_idx][c_idx]
              ins_q = df_ins_pivot.values[r_idx][c_idx]
              pass_q = df_pass_pivot.values[r_idx][c_idx]
              if np.isnan(p_rate):
                  row_text.append("")
              else:
                  row_text.append(f"{p_rate:.1f}%<br>({int(pass_q)}/{int(ins_q)})")
          annotation_text.append(row_text)

      # 3. Heatmap trace 생성
      # 경고 다홍색(colors.orange_500: #F97316)에서 안정 진청색(colors.blue_600: #2563EB) 그라데이션
      custom_colorscale = [
          [0.0, colors.orange_500],
          [0.5, colors.slate_400],
          [1.0, colors.blue_600]
      ]

      fig = go.Figure(data=go.Heatmap(
          x=x_vals,
          y=y_vals,
          z=z_vals,
          colorscale=custom_colorscale,
          zmin=90.0,
          zmax=100.0,
          showscale=True,
          text=annotation_text,
          texttemplate="%{text}",
          textfont={"family": get_font_family("primary"), "size": 10, "color": "white"},
          hoverongaps=False,
          hovertemplate="Machine: %{x}<br>Spec: %{y}<br>Pass Rate: %{z:.2f}%<extra></extra>"
      ))
      
      fig.update_layout(
          margin=dict(t=10, b=10, l=10, r=10),
          height=300,
          xaxis=dict(type="category", title="Building Machine"),
          yaxis=dict(type="category", title="Standard Weight"),
      )
      return apply_shadcn_style_to_figure(fig)

  def fig_gt_weight_grouped_bar(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure:
      """성형기 x 규격(기준중량)별 합격률 비교용 그룹 막대 차트를 생성합니다."""
      if df_gt_raw.empty or "BLDG_MC" not in df_gt_raw.columns:
          fig = go.Figure()
          return apply_shadcn_style_to_figure(fig)

      import numpy as np
      df = df_gt_raw.copy()
      df_agg = df.groupby(["STD_WGT", "BLDG_MC"], as_index=False).agg(
          Inspected_Qty=("JDG", "count"),
          Passed_Qty=("JDG", "sum")
      )
      df_agg["Pass_Rate"] = np.where(
          df_agg["Inspected_Qty"] > 0,
          (df_agg["Passed_Qty"] / df_agg["Inspected_Qty"]) * 100.0,
          0.0
      )
      
      df_agg["STD_WGT_str"] = df_agg["STD_WGT"].apply(lambda v: f"{v:.3f} kg")
      
      # Grouped Bar Plotly Express 로 빌드
      fig = px.bar(
          df_agg,
          x="BLDG_MC",
          y="Pass_Rate",
          color="STD_WGT_str",
          barmode="group",
          labels={
              "BLDG_MC": "Building Machine",
              "Pass_Rate": "Pass Rate (%)",
              "STD_WGT_str": "Standard Weight"
          },
          category_orders={"BLDG_MC": sorted(df_agg["BLDG_MC"].unique().tolist())},
          hover_data={"Pass_Rate": ":.2f%"}
      )
      
      fig.update_layout(
          margin=dict(t=20, b=10, l=10, r=10),
          height=350,
          yaxis=dict(range=[90, 100.5]), # 가독성 향상을 위해 Y축 범위 고정
      )
      return apply_shadcn_style_to_figure(fig)
  ```

- [ ] **Step 4: 테스트를 수행하여 성공 확인**
  Run: `pytest tests/pages/test_data_analysis_plots_gt_wt.py -v`
  Expected: PASS

- [ ] **Step 5: 변경점 커밋**
  ```bash
  git add app/pages/_20_analysis/data_analysis/plots_data_analysis.py tests/pages/test_data_analysis_plots_gt_wt.py
  git commit -m "feat(gt-wt): add heatmap and grouped bar plot functions in plots_data_analysis"
  ```

---

### Task 2: GT/WT 탭 UI 레이아웃 연동 및 배치 (`renderer_gt_wt.py`)

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis/renderer_gt_wt.py`

**Interfaces:**
- Consumes: `fig_gt_weight_heatmap(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure`
- Consumes: `fig_gt_weight_grouped_bar(df_gt_raw: pd.DataFrame, category_label: str) -> go.Figure`

- [ ] **Step 1: `renderer_gt_wt.py` 최하단에 시각화 차트 두 개 및 공백 배치 적용**
  Modify: `app/pages/_20_analysis/data_analysis/renderer_gt_wt.py`
  
  ```python
  # (이하 170-180라인 근방의 replace 적용)
      st.divider()

      # 1. 품질 매트릭스 히트맵 렌더링
      fig_hm = plots.fig_gt_weight_heatmap(df_gt_raw, category="NCF" if params.step1_basic_view_by == "Scrap" else "REWORK") # 또는 category_val
      render_section_title("Weight Quality Matrix by Machine & Spec")
      st.plotly_chart(fig_hm, use_container_width=True, key="gt_weight_heatmap_chart")

      st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

      # 2. 상세 합격률 비교 그룹 바 차트 렌더링
      fig_bar = plots.fig_gt_weight_grouped_bar(df_gt_raw, category="NCF" if params.step1_basic_view_by == "Scrap" else "REWORK")
      render_section_title("Weight Pass Rate Comparison by Machine & Spec")
      st.plotly_chart(fig_bar, use_container_width=True, key="gt_weight_grouped_bar_chart")

      st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

      # 3. 기존 집계 요약 테이블 배치
      render_section_title("Weight Performance Summary by Standard Weight & Building Machine")
      _render_gt_wt_combined_agg_table(df_gt_raw)
  ```
  *(주의: category_label 구분은 NCF 탭의 category 매핑 규칙과 일치하도록 적절히 분류)*

- [ ] **Step 2: 로컬 unit test를 수행하여 레이아웃 연동의 흐름 유효성 검증**
  Run: `pytest tests/pages/test_data_analysis_page_gt_wt.py -v`
  Expected: FAIL (새로 추가한 Plots 모킹 처리가 아직 test에 이루어지지 않아, mock_df의 렌더링 단에서 plots 모킹 객체를 못 찾아 에러 발생할 수 있음)

- [ ] **Step 3: 테스트 파일 `test_data_analysis_page_gt_wt.py` 수정**
  - `plots.fig_gt_weight_heatmap` 및 `plots.fig_gt_weight_grouped_bar` 호출을 Mocking 객체로 우회하도록 몽키패치 추가.
  Modify: `tests/pages/test_data_analysis_page_gt_wt.py`
  
  ```python
  # render_tab_gt_wt_flow 테스트 내부 모킹에 아래 패치 추가
  monkeypatch.setattr(data_analysis_page_dev.plots, "fig_gt_weight_heatmap", lambda *args, **kwargs: go.Figure())
  monkeypatch.setattr(data_analysis_page_dev.plots, "fig_gt_weight_grouped_bar", lambda *args, **kwargs: go.Figure())
  ```

- [ ] **Step 4: 테스트를 재실행하여 흐름 통과 확인**
  Run: `pytest tests/pages/test_data_analysis_page_gt_wt.py -v`
  Expected: PASS

- [ ] **Step 5: 변경점 커밋**
  ```bash
  git add app/pages/_20_analysis/data_analysis/renderer_gt_wt.py tests/pages/test_data_analysis_page_gt_wt.py
  git commit -m "feat(gt-wt): render heatmap and bar plot components in GT/WT layout and mock in tests"
  ```
