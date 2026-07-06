# [Product History] Spec Revision 이력 타임라인 차트 개선 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `Overview` 탭 상단에 Spec Revision 이력(개발/양산 등)의 기간과 변천을 보여주는 단일 행의 수평 타임라인 차트를 이미지 사양에 맞춰 렌더링하고, 기존 Lifecycle 차트는 유지합니다.

**Architecture:** Databricks에서 GMES 스펙 리비전 이력(`get_gmes_spec_revision_general`)을 조회하고, 이를 시작 시점과 종료 시점(다음 변경건 - 1일, 마지막 건은 오늘날짜)으로 가공한 후, Plotly `px.timeline` 또는 수평 막대 차트로 수평 정렬하여 렌더링합니다. 변경 날짜 지시선과 날짜 텍스트, 맞춤 툴팁을 완벽히 수립합니다.

**Tech Stack:** Python, Pandas, Streamlit, Plotly Express / Graph Objects

## Global Constraints

- **Safety Lock**: 사용자의 승인 없이 원천 프로덕션 소스 코드를 수정하지 않으며, 이 계획이 승인된 이후에 수정을 수행합니다.
- **WSL Markdown Link Constraint**: 모든 파일 링크는 상대 경로를 사용하고 `file:///`을 포함하지 않습니다.
- **이모지 사용 금지**: UI 상에 이모지를 노출하지 않으며 머티리얼 벡터 아이콘(`:material/...`)만 활용합니다.
- **한국어 주석/독스트링**: 새로 생성하는 모든 서비스 함수와 플롯 함수에는 Google/NumPy 스타일의 명확한 타입 힌팅과 한국어 독스트링 및 표준 주석 장식 블록을 적용합니다.

---

## File Structure

- **Modify**:
  - `app/service/data_analysis_df.py` : Spec Revision 데이터 조회 및 유효기간 전처리 서비스 함수 구현
  - `app/pages/_20_analysis/data_analysis_plots_dev.py` : 한 줄 스펙 리비전 수평 타임라인 차트 플롯 함수 구현
  - `app/pages/_20_analysis/data_analysis_page_dev.py` : Overview 탭에 신규 차트를 렌더링하는 UI 배치 추가

---

## Tasks

### Task 1: Spec Revision 데이터 가공 서비스 구현

**Files:**
- Modify: `app/service/data_analysis_df.py`
- Test: `tests/service/test_spec_revision_service.py`

**Interfaces:**
- Consumes: `IqmPlusParams` 및 GMES Databricks 클라이언트
- Produces: `preprocess_spec_revision_df(params: IqmPlusParams) -> pd.DataFrame`
  - 리턴 컬럼: `['Start', 'End', 'STXC', 'RCPE_VER', 'Text', 'Duration']`

- [ ] **Step 1: 실패 테스트 작성**
  - M-Code를 파라미터로 주었을 때 mock Databricks 클라이언트가 리턴하는 스펙 리비전 정보를 올바른 수평 기간(Start~End) 및 3자리 포맷팅 텍스트(예: `V-001`, `S-002`)로 정교하게 변환하는지 검증하는 단위 테스트를 생성합니다.

  Create: `tests/service/test_spec_revision_service.py`
  ```python
  import unittest
  from unittest.mock import MagicMock, patch
  import pandas as pd
  from datetime import datetime
  from app.core.data_models.parameters import IqmPlusParams

  class TestSpecRevisionService(unittest.TestCase):
      @patch("app.service.data_analysis_df.get_client")
      def test_preprocess_spec_revision_df(self, mock_get_client):
          # Mock databricks client 및 데이터 프레임 정의
          mock_db = MagicMock()
          mock_get_client.return_value = mock_db
          
          mock_data = pd.DataFrame({
              "STXC": ["V", "S", "S"],
              "RCPE_VER": ["1", "2.0", "3.0"],
              "VLDT_SRT_DATE": ["2026-01-14", "2026-02-02", "2026-06-04"],
              "SPEC_CD": ["KT100", "KT100", "KT100"]
          })
          mock_db.execute.return_value = mock_data
          
          params = IqmPlusParams(
              step0_selected_menu="IQM_PLUS",
              step1_basic_mcode="1035774",
              step1_basic_start_date_str="2026-01-01",
              step1_basic_view_by="90D"
          )
          
          # app.service.data_analysis_df 모듈은 추후 구현될 것이므로 실패 예상
          from app.service.data_analysis_df import preprocess_spec_revision_df
          df = preprocess_spec_revision_df(params)
          
          self.assertEqual(len(df), 3)
          self.assertEqual(df.iloc[0]["Text"], "V-001")
          self.assertEqual(df.iloc[1]["Text"], "S-002")
          self.assertEqual(df.iloc[2]["Text"], "S-003")
          
          # 날짜 형식 및 계산 검증
          self.assertEqual(df.iloc[0]["Start"], pd.to_datetime("2026-01-14"))
          self.assertEqual(df.iloc[0]["End"], pd.to_datetime("2026-02-01")) # 2026-02-02 - 1일
          self.assertEqual(df.iloc[2]["End"].date(), datetime.now().date()) # 오늘날짜
  ```

- [ ] **Step 2: 테스트를 수행하여 실패 여부 확인**
  - `pytest tests/service/test_spec_revision_service.py` 실행하여 모듈이 없거나 함수가 정의되지 않아 실패하는 것을 확인합니다.

- [ ] **Step 3: `app/service/data_analysis_df.py`에 `preprocess_spec_revision_df` 서비스 구현**
  - `app/service/data_analysis_df.py` 에 아래의 함수를 정례 주석과 함께 삽입합니다.

  Modify: `app/service/data_analysis_df.py`
  ```python
  # =========================================================================
  # SECTION 4. Spec Revision Preprocessing (스펙 리비전 이력 가공 서비스)
  # =========================================================================

  # * [SERVICE - 스펙 리비전 이력 단독 전처리]
  @st.cache_data(ttl=3600)
  def preprocess_spec_revision_df(params: IqmPlusParams) -> pd.DataFrame:
      """
      선택된 M-Code와 연동되는 GMES 스펙 리비전 목록을 가져와, 수평 타임라인 구현을 위한
      시작일(Start), 종료일(End, 다음 변경일 - 1일, 최종건은 오늘), 3자리 Revision 텍스트 컬럼을 가공합니다.

      Parameters
      ----------
      params : IqmPlusParams
          대시보드 검색 조건 및 자재코드 파라미터.

      Returns
      -------
      pd.DataFrame
          수평 타임라인 및 툴팁 시각화가 완비된 스펙 리비전 가공 데이터프레임.
      """
      query = gmes_query.get_gmes_spec_revision_general(
          mcode_list=[params.step1_basic_mcode]
      )
      df = databricks_client.execute(query)
      if df.empty:
          return pd.DataFrame(columns=["Start", "End", "STXC", "RCPE_VER", "Text", "Duration"])

      # 1. 날짜 및 타입 정제
      df["Start"] = pd.to_datetime(df["VLDT_SRT_DATE"], errors="coerce")
      df = df.dropna(subset=["Start"]).sort_values("Start").reset_index(drop=True)

      # 2. Revision No. 3자리 문자열 및 표시 텍스트 포맷팅 (V-001, S-002)
      def format_revision(row):
          stxc = str(row.get("STXC", "")).strip()
          rcpe_ver_raw = row.get("RCPE_VER", "0")
          try:
              rcpe_ver_num = int(float(rcpe_ver_raw))
              rcpe_ver_str = f"{rcpe_ver_num:03d}"
          except ValueError:
              rcpe_ver_str = str(rcpe_ver_raw).zfill(3)[:3]
          return f"{stxc}-{rcpe_ver_str}"

      df["Text"] = df.apply(format_revision, axis=1)

      # 3. 종료일(End) 연산: 다음 변경 지점의 Start - 1일, 마지막은 오늘날짜
      ends = []
      now_ts = pd.Timestamp(datetime.now().date())
      for i in range(len(df)):
          if i < len(df) - 1:
              next_start = df.loc[i + 1, "Start"]
              end_date = next_start - pd.Timedelta(days=1)
              # 방어 코드: 만약 end_date가 start보다 이전이면 start로 고정
              if end_date < df.loc[i, "Start"]:
                  end_date = df.loc[i, "Start"]
              ends.append(end_date)
          else:
              # 마지막 끝점은 오늘날짜
              end_date = now_ts
              if end_date < df.loc[i, "Start"]:
                  end_date = df.loc[i, "Start"]
              ends.append(end_date)
      df["End"] = ends

      # 4. 소요 기간(Duration) 연산
      df["Duration"] = (df["End"] - df["Start"]).dt.days + 1

      return df[["Start", "End", "STXC", "RCPE_VER", "Text", "Duration"]]
  ```

- [ ] **Step 4: 테스트를 수행하여 성공 확인**
  - `pytest tests/service/test_spec_revision_service.py`를 실행하여 작성한 테스트가 통과하는지 증명합니다.


### Task 2: Spec Revision Timeline 플롯 함수 구현

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`
- Test: `tests/pages/test_spec_revision_plot.py`

**Interfaces:**
- Consumes: `preprocess_spec_revision_df` 에서 가공된 `pd.DataFrame`
- Produces: `fig_spec_revision_timeline(df: pd.DataFrame) -> go.Figure`

- [ ] **Step 1: 플롯 함수 테스트 코드 작성**
  - 임의의 데이터프레임이 주어졌을 때, 올바른 Plotly figure가 생성되고 이미지처럼 한 줄 표시(Y축 고정), X축 날짜 틱 배치, 색상 맵 등이 반영되는지 확인합니다.

  Create: `tests/pages/test_spec_revision_plot.py`
  ```python
  import unittest
  import pandas as pd
  import plotly.graph_objects as go
  from app.pages._20_analysis.data_analysis_plots_dev import fig_spec_revision_timeline

  class TestSpecRevisionPlot(unittest.TestCase):
      def test_fig_spec_revision_timeline(self):
          df = pd.DataFrame({
              "Start": pd.to_datetime(["2026-01-14", "2026-02-02", "2026-06-04"]),
              "End": pd.to_datetime(["2026-02-01", "2026-06-03", "2026-07-06"]),
              "STXC": ["V", "S", "S"],
              "RCPE_VER": ["1", "2.0", "3.0"],
              "Text": ["V-001", "S-002", "S-003"],
              "Duration": [19, 122, 33]
          })
          
          fig = fig_spec_revision_timeline(df)
          self.assertIsInstance(fig, go.Figure)
          
          # Y축이 단일 상수값 범주로 지정되었는지 확인 (한줄 표시)
          y_vals = [t.y for t in fig.data]
          for y in y_vals:
              self.assertTrue(all(val == "Spec Revision" for val in y))
  ```

- [ ] **Step 2: 테스트를 수행하여 실패 여부 확인**
  - `pytest tests/pages/test_spec_revision_plot.py` 실행하여 함수 부재로 실패함을 확인합니다.

- [ ] **Step 3: `app/pages/_20_analysis/data_analysis_plots_dev.py`에 플롯 함수 추가**
  - Plotly Express를 활용해 `px.timeline`으로 깔끔하게 그리거나, 세로 지시선 및 맞춤 테두리 둥글게 처리를 한 후 `apply_shadcn_style_to_figure` 스타일로 최종 연계해 반환하는 함수를 구현합니다.

  Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`
  ```python
  # =========================================================================
  # SECTION 1. Imports 보정 및 신규 플롯 함수 정의
  # =========================================================================
  import plotly.express as px
  import plotly.graph_objects as go

  # * [PLOT - Spec Revision 단일 행 수평 타임라인 차트]
  def fig_spec_revision_timeline(df: pd.DataFrame) -> go.Figure:
      """
      가공된 Spec Revision 데이터를 바탕으로 이미지와 동일한 한 줄(단일 행)의
      수평 타임라인 Gantt 차트를 렌더링합니다.

      Parameters
      ----------
      df : pd.DataFrame
          ['Start', 'End', 'STXC', 'RCPE_VER', 'Text', 'Duration'] 이 포함된 데이터프레임.

      Returns
      -------
      go.Figure
          디자인 테마가 적용된 수평 타임라인 Plotly 객체.
      """
      if df.empty:
          fig = go.Figure()
          apply_shadcn_style_to_figure(fig, title="Spec Revision History", height=150)
          return fig

      # 단일 행 표시를 위해 Y축 값을 하나의 문자열 상수로 통일
      plot_df = df.copy()
      plot_df["Category"] = "Spec Revision"

      # 이미지의 Spec 타입별 최적 디자인 색상 매핑
      # V Spec: 짙은 청색계열 (#1b638a), S/T Spec: 주황색계열 (#e07a34)
      color_map = {
          "V": "#1b638a",
          "S": "#e07a34",
          "P": "#9b59b6",
          "M": "#2ecc71",
          "T": "#e67e22"
      }
      
      # Plotly Express timeline 기동
      fig = px.timeline(
          plot_df,
          x_start="Start",
          x_end="End",
          y="Category",
          color="STXC",
          text="Text",
          color_discrete_map=color_map,
          hover_data=["Start", "End", "Duration", "Text"]
      )

      # 툴팁(Tooltip) 전면 리폼 및 마커 디테일 보정
      hover_text = []
      for _, row in plot_df.iterrows():
          srt_str = row["Start"].strftime("%Y-%m-%d")
          end_str = row["End"].strftime("%Y-%m-%d")
          hover_text.append(
              f"<b>Revision: {row['Text']}</b><br>"
              f"Period: {srt_str} ~ {end_str}<br>"
              f"Duration: {row['Duration']} days"
              f"<extra></extra>"
          )

      fig.update_traces(
          textposition="inside",
          insidetextanchor="middle",
          textfont=dict(color="white", size=13, family="sans-serif", weight="bold"),
          marker=dict(
              line=dict(color="#2c3e50", width=1),
              # 둥근 모서리가 플로팅 엔진 환경에 따라 미지원될 수 있어 깔끔한 테두리로 정리
          ),
          hovertemplate=hover_text
      )

      # Shadcn 테마 뼈대 적용 (높이를 180px로 아담하게 슬림 패키징)
      apply_shadcn_style_to_figure(fig, title="", height=180)

      # X축 눈금(Tick)을 스펙 변경 시점(Start 날짜들)으로만 정확하게 강제 조정
      tick_vals = plot_df["Start"].tolist()
      tick_text = plot_df["Start"].dt.strftime("%Y-%m-%d").tolist()

      fig.update_layout(
          showlegend=False,
          margin=dict(t=10, b=20, l=10, r=10),
          xaxis=dict(
              type="date",
              tickvals=tick_vals,
              ticktext=tick_text,
              tickfont=dict(color=colors.slate_700, size=11, family="sans-serif"),
              showgrid=True,
              gridcolor="#cbd5e1", # 세로 지시선 가이드라인을 위해 grid 활성화 및 연한 색상 지정
              gridwidth=1.5,
              layer="below traces"
          ),
          yaxis=dict(
              visible=False, # 단일 라인이므로 카테고리 텍스트는 숨겨서 바를 넓게 활용
              showgrid=False
          )
      )

      # 이미지의 수직 지시선(Vertical lines) 강조를 위해 Start 날짜별로 명시적인 세로선 오버레이 추가
      for start_date in tick_vals:
          fig.add_vline(
              x=start_date.timestamp() * 1000, # datetime을 plotly timestamp ms로 연동
              line=dict(color="#1b638a", width=1.5),
              layer="below"
          )

      return fig
  ```

- [ ] **Step 4: 테스트를 수행하여 성공 확인**
  - `pytest tests/pages/test_spec_revision_plot.py`를 실행하여 작성한 테스트가 통과하는지 확인합니다.


### Task 3: Streamlit UI 연계 및 기존 Lifecycle 통합 렌더링

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page_dev.py`

- [ ] **Step 1: `_render_tab_overview` 내에 신규 차트 적용**
  - `data_analysis_page_dev.py` 내의 `_render_tab_overview` 함수에서, 기존 Lifecycle 차트 위에 새로운 Spec Revision Timeline 차트 영역을 가로 막대 형태로 얹어 렌더링하도록 몽킹 및 보강합니다.

  Modify: `app/pages/_20_analysis/data_analysis_page_dev.py:481-489`
  ```python
          # -- Spec Revision 이력 타임라인 렌더링
          st.subheader(
              "Product History",
              help="PLM/GMES 기반의 스펙 변경 revision 이력 수평 타임라인",
          )
          
          df_spec_rev = preprocess_spec_revision_df(params)
          if not df_spec_rev.empty:
              fig_spec_rev = plots.fig_spec_revision_timeline(df_spec_rev)
              st.plotly_chart(fig_spec_rev, key="spec_revision_timeline_chart")
          else:
              st.info("No Spec Revision history available.", icon=":material/info:")

          # -- Lifecycle 타임라인 렌더링 (기존 차트는 원천 그대로 완벽 유지)
          st.subheader(
              "Lifecycle",
              help="CQMS & PLM으로 수집된 정보를 기반으로 스펙변경 및 품질이슈 이력 조회",
          )

          df_life_cycle = preprocess_lifecycle_df(params)
          fig_life_cycle = plots.fig_life_cycle(df_life_cycle)
          st.plotly_chart(fig_life_cycle, key="life_cycle_chart")
  ```

- [ ] **Step 2: Streamlit 렌더러 동작 연동 테스트 검증**
  - `tests/pages/test_data_analysis_page_dev.py` 등의 검증 테스트를 활용해 신규 페이지 코드가 임포트 시 예외나 KeyError를 일으키지 않고 성공적으로 실행되는지 점검합니다.
