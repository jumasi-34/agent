# Unify and Cleanup Legacy Headers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `app/core/design_system/streamlit_widgets.py`에서 불필요한 기존 잔재 헤더 함수들을 완전히 소멸시키고, `section_header` 하나만으로 세 가지 변형(Standard, Dashboard, Stats) 레이아웃을 다이나믹하게 렌더링하도록 일원화합니다.

**Architecture:** 
`section_header`에 `header_type: Literal["standard", "dashboard", "stats"] = "standard"` 파라미터를 도입하여 단일 인터페이스 안에서 마진, 보더라인 유무, 폰트 크기 및 우측 스탯/HTML 정보 빌드 영역을 분기합니다. 기존의 프로덕션 호출 지점([app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py](app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py))을 신형 `section_header` 호출로 완벽히 리다이렉션하고 레거시 함수 정의를 완전히 제거합니다.

**Tech Stack:** Python 3.11, Streamlit 1.35+, Pytest

## Global Constraints

- **유니코드 이모지 완전 금지**: 모든 주석, 소스 코드 및 독스트링 문서 내에 어떠한 일반 유니코드 이모지(예: 🌟, 🚀, 🛠️ 등)도 사용하지 않습니다. (구글 머티리얼 벡터 구문 `:material/icon_name:`만 사용 가능)
- **WSL Markdown Link Constraint**: 절대 리눅스 파일 경로나 `file:///` 프로토콜을 사용하지 않고, 워크스페이스 루트 기준의 평문 상대 경로만을 사용하여 하이퍼링크를 제공합니다.
- **한국어 독스트링**: 신규 및 보완 모듈, 함수에 작성되는 모든 설명과 주석은 고가독성의 한국어로 정교하게 기술합니다.

---

### Task 1: `section_header` 만능 다이나믹 라우터 구현 및 레거시 함수 제거

**Files:**
- Modify: [app/core/design_system/streamlit_widgets.py](app/core/design_system/streamlit_widgets.py)
- Test: [tests/test_streamlit_widgets.py](tests/test_streamlit_widgets.py)

**Interfaces:**
- Consumes: `_build_header_icon_html`, `_build_stats_html`, `_build_info_items_html`, `_build_container_style`, `_minify_html`, `colors`, `spacing`, `CSSClasses`
- Produces: `section_header` 함수 하나로 3가지 타입 렌더링 지원
  - `def section_header(title: str, subtitle: str | None = None, info_items: list[dict[str, str]] | None = None, icon_name: str | None = None, top_margin: str | None = None, bottom_margin: str | None = None, basic_info: dict[str, str] | None = None, header_type: Literal["standard", "dashboard", "stats"] = "standard", **kwargs) -> None:`

- [ ] **Step 1: 실패하는 통합 유닛 테스트 작성**
  [tests/test_streamlit_widgets.py](tests/test_streamlit_widgets.py)의 `test_smart_section_header_routing_and_svg` 함수 내부에 `header_type="dashboard"` 및 `header_type="stats"` 옵션의 렌더링 구조와 적용 스타일 토큰을 정밀하게 단정(Assert)하는 실패할 테스트 코드를 먼저 추가합니다.

  ```python
  # (tests/test_streamlit_widgets.py 내 test_smart_section_header_routing_and_svg 함수 하단에 추가할 내용)
  # --- 5. header_type="dashboard" 분기 및 레이아웃 검증 ---
  section_header(
      title="Dashboard Spec Title",
      subtitle="Dashboard Sub",
      icon_name="grid_view",
      header_type="dashboard",
  )
  call_args_dash = mock_markdown.call_args[0][0]
  assert "Dashboard Spec Title" in call_args_dash
  assert "grid_view" in call_args_dash
  assert "margin-top: 1.5rem;" in call_args_dash  # spacing.space_6 렌더링 확인 (has_border=False 이므로 하단 보더라인 스타일이 없어야 함)
  assert "border-bottom" not in call_args_dash

  mock_markdown.reset_mock()

  # --- 6. header_type="stats" 분기 및 레이아웃 검증 ---
  section_header(
      title="Stats Spec Title",
      subtitle="Stats Sub",
      info_items=[{"label": "Metric", "value": "100"}],
      icon_name="show_chart",
      header_type="stats",
  )
  call_args_stats = mock_markdown.call_args[0][0]
  assert "Stats Spec Title" in call_args_stats
  assert "Metric" in call_args_stats
  assert "100" in call_args_stats
  assert "border-bottom: 1px solid" in call_args_stats  # has_border=True 렌더링 확인
  ```

- [ ] **Step 2: Pytest 구동하여 테스트 실패 확인**
  Run: `pytest tests/test_streamlit_widgets.py -k test_smart_section_header_routing_and_svg -v`
  Expected: FAIL (TypeError: `section_header() got an unexpected keyword argument 'header_type'` 혹은 분기 검증 단정 실패)

- [ ] **Step 3: `section_header`에 다이나믹 라우팅 구현 및 레거시 함수 영구 제거**
  [app/core/design_system/streamlit_widgets.py](app/core/design_system/streamlit_widgets.py)에서 `section_header` 시그니처를 수정하고, `header_type` 기반 분기 로직을 주입합니다. 또한 불필요해진 레거시 함수들을 파일에서 흔적 없이 완전히 지웁니다.

  ```python
  # app/core/design_system/streamlit_widgets.py 수정 내용
  def section_header(
      title: str,
      subtitle: str | None = None,
      info_items: list[dict[str, str]] | None = None,
      icon_name: str | None = None,
      top_margin: str | None = None,
      bottom_margin: str | None = None,
      basic_info: dict[str, str] | None = None,
      header_type: str = "standard",  # Literal["standard", "dashboard", "stats"]
      **kwargs,
  ) -> None:
      """만능 다이나믹 라우팅을 지원하는 소제목 및 섹션 구분 헤더 위젯입니다.

      Parameters
      ----------
      title : str
          제목 텍스트.
      subtitle : str, optional
          부제목 텍스트. 기본값은 None.
      info_items : list[dict[str, str]], optional
          우측 정보 패널 및 통계 그리드에 표시할 데이터. 기본값은 None.
      icon_name : str, optional
          제목 옆에 노출할 Material 아이콘명. 기본값은 None.
      top_margin : str, optional
          상단 여백. 지정하지 않을 시 타입별 기본 토큰이 주입됩니다.
      bottom_margin : str, optional
          하단 여백. 지정하지 않을 시 타입별 기본 토큰이 주입됩니다.
      basic_info : dict[str, str], optional
          타이어 기본 정보 딕셔너리 (Type 3 Spec에 활용). 기본값은 None.
      header_type : str, optional
          렌더링할 헤더 스타일 타입 ('standard', 'dashboard', 'stats'). 기본값은 'standard'.
      """
      import html
      from app.core.design_system.tokens import get_font_family, spacing

      # 0. 하위 호환성 (레거시 title_icon, icon_config 수용 및 자동 매핑)
      final_icon_name = icon_name
      if "title_icon" in kwargs:
          final_icon_name = kwargs["title_icon"]
      if "icon" in kwargs:
          final_icon_name = kwargs["icon"]

      final_basic_info = basic_info
      if "basic_info" in kwargs:
          final_basic_info = kwargs["basic_info"]

      # 1. 타입별 마진 및 보더 설정
      if header_type == "dashboard":
          t_margin = top_margin if top_margin else spacing.space_6
          b_margin = bottom_margin if bottom_margin else spacing.space_5
          has_border = False
          font_size_val = "1.35rem"
          icon_size_val = "1.6rem"
          padding_b = "0px"
          icon_css = "dashboard-title-icon-svg"  # 대시보드 대형 아이콘 클래스
      elif header_type == "stats":
          t_margin = top_margin if top_margin else spacing.space_6
          b_margin = bottom_margin if bottom_margin else spacing.space_5
          has_border = True
          font_size_val = "1.35rem"
          icon_size_val = "1.35rem"
          padding_b = spacing.space_3
          icon_css = CSSClasses.DASHBOARD_TITLE_ICON
      else:  # standard
          t_margin = top_margin if top_margin else spacing.space_5
          b_margin = bottom_margin if bottom_margin else spacing.space_3
          has_border = True
          font_size_val = "1.15rem"
          icon_size_val = "1.15rem"
          padding_b = spacing.space_2
          icon_css = CSSClasses.MINIHEADER_TITLE_ICON

      # 2. 아이콘 HTML 렌더링
      icon_html = _build_header_icon_html(final_icon_name, font_size=icon_size_val, css_class=icon_css)

      # 3. 서브타이틀 HTML 렌더링
      subtitle_html = ""
      if subtitle:
          subtitle_escaped = html.escape(str(subtitle))
          subtitle_font_size = "0.8rem" if header_type in ["dashboard", "stats"] else "0.75rem"
          subtitle_html = f"""
          <p style="font-family: {get_font_family('primary')}; font-size: {subtitle_font_size}; color: {colors.app_text_muted}; margin: {spacing.space_1} 0 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              {subtitle_escaped}
          </p>
          """

      # 4. 우측 정보 영역 HTML 빌드 및 라우팅
      info_html = ""
      if header_type == "dashboard":
          if "extra_info_html" in kwargs and kwargs["extra_info_html"]:
              info_html = kwargs["extra_info_html"]
      elif header_type == "stats":
          # stats 타입은 무조건 _build_stats_html 연동
          if info_items is not None:
              _validate_inputs(title, info_items)
              info_html = _build_stats_html(info_items)
      else:  # standard
          if final_basic_info:
              items_html = ""
              for key, val in final_basic_info.items():
                  k_esc = html.escape(str(key))
                  v_esc = html.escape(str(val))
                  items_html += f'<div class="{CSSClasses.TIRE_INFO_BASIC_ITEM}"><span class="{CSSClasses.TIRE_INFO_BASIC_LABEL}">{k_esc}</span><span class="{CSSClasses.TIRE_INFO_BASIC_VALUE}">{v_esc}</span></div>'
              info_html = f'<div class="{CSSClasses.TIRE_INFO_BASIC}">{items_html}</div>'
          elif info_items:
              if len(info_items) >= 3:
                  info_html = _build_stats_html(info_items)
              else:
                  info_html = _build_info_items_html(info_items)

      title_escaped = html.escape(str(title))
      container_style = _build_container_style(t_margin, b_margin, has_border=has_border, padding_bottom=padding_b)

      # 5. 최종 레이아웃 합성 및 Streamlit 주입
      html_content = f"""
      <div style="{container_style}">
          <div style="overflow: hidden; flex: 1;">
              <div style="display: flex; align-items: center; gap: {spacing.space_1}; margin: 0; line-height: 1;" translate="no">
                  {icon_html}
                  <div style="font-family: {get_font_family('display')}; font-size: {font_size_val}; font-weight: 600; color: {colors.app_text_primary}; margin: 0; line-height: 1; display: inline-flex; align-items: center; white-space: nowrap;" translate="no">
                      {title_escaped}
                  </div>
              </div>
              {subtitle_html}
          </div>
          {info_html}
      </div>
      """

      flat_html = _minify_html(html_content)
      st.markdown(flat_html, unsafe_allow_html=True)
  ```

  동시에 아래의 기존 레거시 코드 구간을 파일에서 깨끗하게 지웁니다:
  - `def subheader_title_panel(...)` (라인 664 ~ 705 근처)
  - `def dashboard_header(...)` (라인 710 ~ 790 근처)
  - `def dashboard_section_header(...)` (라인 791 ~ 827 근처)
  - `def stats_header(...)` (라인 830 ~ 911 근처)
  - `def subheader_title_stats_panel(...)` (라인 912 ~ 953 근처)

- [ ] **Step 4: Pytest 구동하여 테스트 성공 확인**
  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: PASS

- [ ] **Step 5: 변경 사항 커밋**
  ```bash
  git add app/core/design_system/streamlit_widgets.py tests/test_streamlit_widgets.py
  git commit -m "refactor(widgets): unify all legacy headers into section_header dynamic router"
  ```

---

### Task 2: 프로덕션 호출처 `qrs_worksheet_monitoring_page.py` 마이그레이션

**Files:**
- Modify: [app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py](app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py)

**Interfaces:**
- Consumes: `section_header`
- Produces: `section_header(..., header_type="stats")` 호출을 통한 통계 헤더 출력

- [ ] **Step 1: 임포트 및 호출부 수정**
  [app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py](app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py)를 열어, `stats_header` 임포트를 `section_header`로 전면 교체합니다.

  ```python
  # app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py 수정 부분 (L26-L30 근처)
  from app.core.design_system.streamlit_widgets import (
      header_main_title_info_panel,
      shadcn_data_table,
      section_header,  # stats_header -> section_header 로 전환
  )
  ```

  동시에 파일 내부의 두 군데 `stats_header(...)` 호출을 `section_header(..., header_type="stats")` 로 안전하게 전환합니다.

  ```python
  # 첫 번째 호출처 수정 (L407 근처)
  def display_qrs_section(
      title: str, df: pd.DataFrame, team_pivot_df: pd.DataFrame, key_prefix: str
  ) -> None:
      ...
      # 섹션 헤더 (shadcn 스타일)
      section_header(
          title=title,
          subtitle="작업일지 작성 현황",
          info_items=[],
          header_type="stats",  # 추가
      )
  ```

  ```python
  # 두 번째 호출처 수정 (L990 근처)
  def _render_subteam_stats_and_tables(
      subteam: str,
      team: str,
      sub_team_agg_df: pd.DataFrame,
      machine_agg_df: pd.DataFrame,
  ) -> None:
      ...
      section_header(
          title=subteam,
          subtitle=team,
          info_items=[
              {
                  "label": "작성률",
                  "value": sub_team_agg_df[sub_team_agg_df["SUB_TEAM"] == subteam][
                      "작성률"
                  ].values[0],
              },
              {
                  "label": "합격률",
                  "value": sub_team_agg_df[sub_team_agg_df["SUB_TEAM"] == subteam][
                      "합격률"
                  ].values[0],
              },
          ],
          header_type="stats",  # 추가
      )
  ```

- [ ] **Step 2: 전체 Pytest 구동 및 정적 린트 검증**
  전체 테스트를 다시 한번 점검하고, 혹시 존재할지 모르는 구문 오류나 임포트 오류를 검증합니다.
  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: PASS

- [ ] **Step 3: 변경 사항 커밋**
  ```bash
  git add app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py
  git commit -m "refactor(qrs-page): migrate legacy stats_header to section_header stats variant"
  ```
