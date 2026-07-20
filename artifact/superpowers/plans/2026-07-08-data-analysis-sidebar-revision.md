# Data Analysis Page Sidebar Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 데이터 분석 페이지의 사이드 패널(사이드바) 최상단에 `st.sidebar.segmented_control`을 배치하여 분석 기법을 결정하고, 선택된 분석 모드에 부합하는 필터 및 기간 제약 사항만 동적으로 유기적으로 표출하여 UI 인지 맥락을 깔끔하게 개편합니다.

**Architecture:** 
- 최상단 `st.sidebar.segmented_control`에서 선택된 ID(`IQM_PLUS`, `PERIOD`, `BP`)를 `MENU_SELECT_DICT`와 역매핑하여 `params.step0_selected_menu` 상태에 실시간 동기화합니다.
- 사이드바 내부 폼(`with st.sidebar.form`)에서는 각 분석 모드별 맞춤형 인풋 필드만 분기 렌더링되도록 격리 및 동적 리팩토링을 가해, 백엔드 연산 및 Plotly 시각화 쿼리 로직의 무결성을 100% 보존합니다.

**Tech Stack:** Streamlit (Layout, Segmented Control, Conditional Forms), Python, Pytest

## Global Constraints
- **Safety Lock**: 본 구현 계획은 사용자의 최종 승인 동의에 입각하여 가동되며, `app/pages/_20_analysis/data_analysis_page_dev.py`와 `tests/pages/test_data_analysis_page_dev.py`를 정밀하게 격리 가공합니다.
- **Emoji Restriction**: Streamlit UI, 주석, 소스 코드 내에 유니코드 이모지 작성을 완전히 배제하고 오직 Streamlit 기본 머티리얼 아이콘 구문(`:material/icon_name:`)만을 허용합니다.
- **WSL Markdown Link Constraint**: 모든 내부 파일 하이퍼링크는 프로토콜 없이 워크스페이스 기준 평문 상대 경로만을 정밀 적용합니다.

---

### Task 1: user_input_section 정적 로직 검증 및 붕괴 테스트 수립

**Files:**
- Modify: `tests/pages/test_data_analysis_page_dev.py:12-130`

**Interfaces:**
- Consumes: `app.pages._20_analysis.data_analysis_page_dev.user_input_section`
- Produces: `test_user_input_section_segmented_control_logic` (신규 단위 테스트 검증 메서드)

- [ ] **Step 1: user_input_section 로직을 격리 검증하는 실패하는 테스트 코드 작성**
  `tests/pages/test_data_analysis_page_dev.py` 하단에 `st.sidebar.segmented_control` 기반의 신규 동적 제어 흐름이 정상적으로 파싱되고 바인딩되는지 확인하는 실패 테스트를 추가합니다.

  ```python
  # (tests/pages/test_data_analysis_page_dev.py 끝부분에 추가할 코드 조각)
      @patch("app.pages._20_analysis.data_analysis_page_dev.st")
      @patch("app.pages._20_analysis.data_analysis_page_dev.generate_iqm_plus_master_df")
      def test_user_input_section_segmented_control_logic(
          self,
          mock_generate_master,
          mock_st,
      ) -> None:
          """사이드바 user_input_section이 segmented_control 선택에 따라 올바른 params 상태를 반환하는지 테스트합니다."""
          from app.pages._20_analysis.data_analysis_page_dev import user_input_section
          
          # 1. IQM Plus 마스터 데이터 모킹
          mock_master_df = pd.DataFrame({
              "MFG_MCODE": ["M001"],
              "MIN_WRK_DATE": [pd.to_datetime("2026-01-01")]
          })
          mock_generate_master.return_value = mock_master_df
          
          # 2. Streamlit 위젯 반환 값 모킹
          # (1) segmented_control이 'IQM_PLUS' 모드를 선택한 시나리오
          mock_st.sidebar.segmented_control.return_value = "IQM_PLUS"
          mock_st.selectbox.return_value = "M001"
          mock_st.segmented_control.return_value = "Weekly"
          mock_st.form_submit_button.return_value = True
          
          # 3. 파라미터 초기화 및 실행
          params = IqmPlusParams()
          params.step0_selected_menu = "" # 초기값 공백
          
          # UI 함수 실행
          updated_params = user_input_section(params)
          
          # 4. 정량 단언 검증 (Assert)
          # segmented_control 'IQM_PLUS' 선택 시 params.step0_selected_menu가 "IQM Plus Only"로 정상 매핑되는지 체크
          self.assertEqual(updated_params.step0_selected_menu, MENU_SELECT_DICT["IQM_PLUS"])
          
          # st.sidebar.segmented_control이 올바른 매개변수로 호출되었는지 정적 체이싱
          mock_st.sidebar.segmented_control.assert_called_once()
  ```

- [ ] **Step 2: 테스트를 수행하여 기대대로 실패(Fail)하는지 확인**
  Run: `pytest tests/pages/test_data_analysis_page_dev.py -k test_user_input_section_segmented_control_logic -v`
  Expected: FAIL (이유: 아직 `data_analysis_page_dev.py` 내부에 `st.sidebar.segmented_control` 로직이 미구현 상태이므로)

- [ ] **Step 3: Commit**
  ```bash
  git add tests/pages/test_data_analysis_page_dev.py
  git commit -m "test: add failing unit test for dynamic sidebar user input panel"
  ```

---

### Task 2: dynamic_sidebar_segmented_control 도입 및 분기 리팩토링

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page_dev.py:118-350`

**Interfaces:**
- Consumes: `IqmPlusParams`
- Produces: `user_input_section` (리팩토링된 신규 동적 렌더링 모듈)

- [ ] **Step 1: app/pages/_20_analysis/data_analysis_page_dev.py 의 user_input_section 리팩토링 이행**
  구현 사양서에 의거하여, 거대 버튼 루프를 제거하고 최상단 `st.sidebar.segmented_control`을 활용한 세션 동기화 및 폼 분기 렌더링 코드를 이식합니다.

  ```python
  # (app/pages/_20_analysis/data_analysis_page_dev.py의 user_input_section 구현부 치환 코드 조각)
  def user_input_section(params: IqmPlusParams) -> IqmPlusParams:
      """
      고도화된 대시보드 사이드바 패널의 입력 UI 필터를 렌더링하고 사용자가 입력한 필터 상태를 반환합니다.
      """
      import datetime as dt

      # -- [1] ANALYSIS MODE 섹션 (최상단 수평 정돈)
      st.sidebar.markdown("### :material/settings: **[1] ANALYSIS MODE**")
      
      # 기존 step0_selected_menu 텍스트를 key-ID 값으로 역매핑하여 기본값 정렬
      rev_menu_dict = {v: k for k, v in MENU_SELECT_DICT.items()}
      current_default_id = rev_menu_dict.get(params.step0_selected_menu, "IQM_PLUS")
      
      # st.sidebar.segmented_control을 활용하여 3개의 모드를 명확히 노출
      selected_mode_id = st.sidebar.segmented_control(
          "Analysis Mode Selector",
          options=["IQM_PLUS", "PERIOD", "BP"],
          format_func=lambda x: {
              "IQM_PLUS": "IQM Plus Only",
              "PERIOD": "Period Analysis",
              "BP": "Break Point"
          }[x],
          selection_mode="single",
          default=current_default_id,
          key="analysis_mode_selector",
          label_visibility="collapsed" # 레이블 감춤으로 슬림함 극대화
      )
      
      # 사용자가 조작한 모드 식별자를 비즈니스 텍스트 필드로 전환하여 세션 상태 즉시 갱신
      params.step0_selected_menu = MENU_SELECT_DICT[selected_mode_id]

      st.sidebar.divider()

      # -- [2] SEARCH SPECIFICATION 섹션
      st.sidebar.markdown("### :material/calendar_today: **[2] SEARCH SPECIFICATION**")

      # * [UI - IQM Plus M-Code 선택 및 일자 동기화]
      def _render_iqm_plus_mcode_and_dates(params: IqmPlusParams) -> IqmPlusParams:
          iqm_plus_master_df = generate_iqm_plus_master_df()
          iqm_mcode_list = sorted(iqm_plus_master_df["MFG_MCODE"].unique().tolist())

          params.step1_basic_mcode = st.selectbox(
              "M-Code Select",
              iqm_mcode_list,
              index=iqm_mcode_list.index(
                  params.step1_basic_mcode
                  if params and params.step1_basic_mcode in iqm_mcode_list
                  else iqm_mcode_list[0]
              ),
              key="mcode_input",
              help="IQM Plus 마스터 DB에서 감지된 M-Code 목록입니다."
          )

          condition = iqm_plus_master_df["MFG_MCODE"] == params.step1_basic_mcode
          selected_mcode_info_dict = iqm_plus_master_df.loc[condition].to_dict(
              orient="records"
          )[0]
          
          # start date 수집
          params.step1_basic_start_date = selected_mcode_info_dict["MIN_WRK_DATE"]
          end_date_candidate = selected_mcode_info_dict["MIN_WRK_DATE"] + timedelta(days=364)
          today = pd.to_datetime(dt.datetime.now().date())
          params.step1_basic_end_date = min(pd.to_datetime(end_date_candidate), today)
          
          params.step1_basic_start_date_str = _format_date_yyyymmdd(params.step1_basic_start_date)
          params.step1_basic_end_date_str = _format_date_yyyymmdd(params.step1_basic_end_date)
          
          # IQM_PLUS 모드 전용 : 조회 범위 1년 자동 지정을 시각적으로 안내 (읽기 전용 st.info 구성)
          st.info(
              f"조회 기간 범위 자동 지정 완료\n\n"
              f":material/calendar_today: {params.step1_basic_start_date_str} ~ {params.step1_basic_end_date_str}",
              icon=":material/info:"
          )

          return params

      # (이하 헬퍼 _render_normal_mcode_and_dates 및 _render_bp_date는 기존 소스 일관성 유지)
      ...
  ```

- [ ] **Step 2: 폼(Form) 내부 분기 필터 렌더링 로직 교체**
  선택된 `params.step0_selected_menu` 텍스트값과 일관성을 유지하도록 폼 렌더링 파트를 리팩토링합니다.

  ```python
  # (data_analysis_page_dev.py의 user_input_section 내 st.sidebar.form 구획)
      with st.sidebar.form("product_history_revision_form", border=False):
          if params.step0_selected_menu == MENU_SELECT_DICT["IQM_PLUS"]:
              params = _render_iqm_plus_mcode_and_dates(params)
          else:
              params = _render_normal_mcode_and_dates(params)

          # 변경점 메뉴 로직 : BP Date 입력 상자 추가 노출
          if params.step0_selected_menu == MENU_SELECT_DICT["BP"]:
              params = _render_bp_date(params)

          st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
          st.markdown("### :material/tune: **[3] VIEW PREFERENCE**")

          view_by = st.segmented_control(
              "View Period Unit",
              ["Weekly", "Monthly"],
              selection_mode="single",
              key="view_by_selector",
              default="Weekly",
              width="stretch",
          )

          st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

          user_form_submit_btn = st.form_submit_button(
              " Run Query & Analysis",
              type="primary",
              key="user_submit",
              use_container_width=True,
          )
  ```

- [ ] **Step 3: 단위 테스트를 수행하여 PASS 확인**
  Run: `pytest tests/pages/test_data_analysis_page_dev.py -v`
  Expected: 모든 단위 테스트 통과 (PASS)

- [ ] **Step 4: Commit**
  ```bash
  git add app/pages/_20_analysis/data_analysis_page_dev.py
  git commit -m "feat: implement dynamic sidebar segmented control and conditional inputs"
  ```
