# [Feature Name] Implementation Plan: Dashboard Section Header Componentization

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 대시보드 내에 하드코딩되어 반복 사용 중인 소제목(H3 섹션 구분 제목)의 마크다운 코드를 단일 공통 위젯 컴포넌트(`dashboard_section_header`)로 추상화하여, 유지보수성과 시각적 통일성을 극대화합니다.

**Architecture:** `app/core/design_system/streamlit_widgets.py` 내에 독립 함수형 UI 컴포넌트를 선언하고, `unittest.mock.patch` 기반의 Streamlit 렌더링 검증용 TDD 테스트 스위트를 구축한 후, 각 페이지의 하드코딩 영역을 순차적으로 안전 교체합니다.

**Tech Stack:** Python 3.x, Streamlit, Pytest, Mocking

## Global Constraints

- Safety Lock: 사용자의 명시적인 직접 승인 및 요청이 있기 전까지 기존 프로덕션 소스 코드 변경 금지 (본 작업은 승인을 득함).
- UI 규칙 및 이모지 사용 전면 금지: 어떠한 텍스트 주석 및 UI 문자열 영역에서도 일반 유니코드 이모지를 사용할 수 없음.
- WSL Markdown Link Constraint: 클릭 동작 호환성을 위해 모든 하이퍼링크는 프로토콜을 제외한 워크스페이스 기준 평문 상대 경로 사용.
- 함수 생성, 독스트링 및 코드 구조 표준: 신규 함수 추가 시 Google/NumPy 스타일 한글 독스트링 및 표준 주석 장식 블록 적용 필수.

---

### Task 1: 공통 위젯 컴포넌트 추가 및 TDD 테스트 검증

**Files:**
- Create: `tests/test_streamlit_widgets.py`
- Modify: `app/core/design_system/streamlit_widgets.py:388-388` (subheader_title_stats_panel 바로 위에 삽입)

**Interfaces:**
- Consumes:
  - `from app.core.design_system.tokens import colors, get_font_family, spacing`
  - `from app.core.design_system.tokens.icons import get_svg_icon`
- Produces:
  - `def dashboard_section_header(title: str, subtitle: str | None = None, icon_name: str | None = None, extra_info_html: str | None = None, top_margin: str | None = None, bottom_margin: str | None = None) -> None`

- [ ] **Step 1: Write the failing test**
  
  `tests/test_streamlit_widgets.py` 파일을 생성하고 컴포넌트 렌더링에 대한 모의 테스트를 선언합니다.

  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  import unittest
  from unittest.mock import patch
  import streamlit as st

  # =========================================================================
  # SECTION 2. Test Case Definition (테스트 케이스 정의)
  # =========================================================================
  def test_dashboard_section_header_rendering():
      """dashboard_section_header 컴포넌트가 올바른 HTML 포맷으로 렌더링되는지 검증합니다."""
      # 아직 존재하지 않는 모듈이므로 임포트 시 실패 예상 또는 NameError 유발
      from app.core.design_system.streamlit_widgets import dashboard_section_header

      with patch("streamlit.markdown") as mock_markdown:
          dashboard_section_header(
              title="Test Section Title",
              subtitle="Test Section Subtitle Desc",
              icon_name="trending_up",
          )
          
          # markdown이 호출되었는지 확인
          assert mock_markdown.called
          call_args = mock_markdown.call_args[0][0]
          
          # 핵심 HTML 클래스 및 텍스트 렌더링 구조 보장 검증
          assert "Test Section Title" in call_args
          assert "Test Section Subtitle Desc" in call_args
          assert "trending_up" in call_args
          assert "display: flex" in call_args
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: FAIL with `ImportError: cannot import name 'dashboard_section_header'`

- [ ] **Step 3: Write minimal implementation**

  [app/core/design_system/streamlit_widgets.py](app/core/design_system/streamlit_widgets.py)의 적절한 위치(L388 부근, `subheader_title_stats_panel` 직전)에 한글 독스트링 표준 주석 규격을 철저히 준수한 `dashboard_section_header()` 함수를 추가합니다.

  ```python
  # =========================================================================
  # SECTION 3.5. Dashboard Section Header (소제목 섹션 구분 헤더 컴포넌트)
  # =========================================================================
  # * [UI 컴포넌트 - 대시보드 소제목 섹션 구분 헤더 렌더링]
  def dashboard_section_header(
      title: str,
      subtitle: str | None = None,
      icon_name: str | None = None,
      extra_info_html: str | None = None,
      top_margin: str | None = None,
      bottom_margin: str | None = None,
  ) -> None:
      """대시보드 페이지 내부에서 일관된 스타일의 소제목 및 섹션 구분 헤더를 빌드하고 렌더링합니다.

      Parameters
      ----------
      title : str
          섹션 제목 텍스트 (예: 'M-Level Index Trend').
      subtitle : str, optional
          설명 및 서브제목 텍스트. 기본값은 None.
      icon_name : str, optional
          제목 좌측에 렌더링할 SVG 아이콘명. 기본값은 None.
      extra_info_html : str, optional
          우측 영역에 배치될 추가 통계 뱃지 및 설명 정보 HTML 문자열. 기본값은 None.
      top_margin : str, optional
          상단 여백 (예: spacing.space_6). 지정하지 않을 시 기본 토큰 값이 주입됩니다.
      bottom_margin : str, optional
          하단 여백 (예: spacing.space_5). 지정하지 않을 시 기본 토큰 값이 주입됩니다.
      """
      import html
      from app.core.design_system.tokens import colors, get_font_family, spacing
      from app.core.design_system.tokens.icons import get_svg_icon

      # 1. 마진 기본값 보정
      t_margin = top_margin if top_margin else spacing.space_6
      b_margin = bottom_margin if bottom_margin else spacing.space_5

      # 2. 아이콘 HTML 렌더링
      icon_html = ""
      if icon_name:
          icon_svg = get_svg_icon(icon_name, "1.6rem", colors.app_text_primary)
          icon_html = f'''
          <div style="display: inline-flex; align-items: center; justify-content: center; user-select: none; -webkit-user-select: none;" translate="no">
              {icon_svg}
          </div>
          '''

      # 3. 서브타이틀 HTML 렌더링
      subtitle_html = ""
      if subtitle:
          subtitle_escaped = html.escape(str(subtitle))
          subtitle_html = f'''
          <p style="font-family: {get_font_family('primary')}; font-size: 0.8rem; color: {colors.app_text_muted}; margin: {spacing.space_1} 0 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              {subtitle_escaped}
          </p>
          '''

      # 4. 우측 추가 정보 패널 HTML 렌더링
      extra_html = ""
      if extra_info_html:
          extra_html = extra_info_html

      title_escaped = html.escape(str(title))

      # 5. 최종 레이아웃 합성 및 Streamlit 주입 (유니코드 이모지 배제 규칙 준수)
      html_content = f"""
      <div style="margin-top: {t_margin}; margin-bottom: {b_margin}; display: flex; justify-content: space-between; align-items: center; flex-wrap: nowrap; gap: {spacing.space_4};">
          <div style="overflow: hidden; flex: 1;">
              <div style="display: flex; align-items: center; gap: {spacing.space_2}; margin: 0; line-height: 1;" translate="no">
                  {icon_html}
                  <div style="font-family: {get_font_family('display')}; font-size: 1.35rem; font-weight: 600; color: {colors.app_text_primary}; margin: 0; line-height: 1; display: inline-flex; align-items: center; white-space: nowrap;" translate="no">
                      {title_escaped}
                  </div>
              </div>
              {subtitle_html}
          </div>
          {extra_html}
      </div>
      """
      st.markdown(html_content, unsafe_allow_html=True)
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**

  ```bash
  git add tests/test_streamlit_widgets.py app/core/design_system/streamlit_widgets.py
  git commit -m "feat(widget): add common dashboard_section_header component"
  ```

---

### Task 2: IQM Plus 메인 대시보드 리팩토링 이행

**Files:**
- Modify: `app/pages/_10_dashboard/iqm_plus_main_page.py` (임포트 보강 및 9개 섹션 타이틀 컴포넌트화)

**Interfaces:**
- Consumes:
  - `from app.core.design_system.streamlit_widgets import dashboard_section_header`

- [ ] **Step 1: 임포트 최적화 및 로컬 get_svg_icon 연관성 정리**
  
  `app/pages/_10_dashboard/iqm_plus_main_page.py` 상단 임포트 구문에 `dashboard_section_header`를 추가합니다.

- [ ] **Step 2: 9개 섹션 헤더 일괄 수정**

  각 하드코딩 구역을 찾아서 `dashboard_section_header` 호출문으로 순차 치환합니다.
  
  * *M-Level Index Trend* (L1017 부근)
  * *CQMS Events Monitoring* (L1084 부근)
  * *Plant & OEM Distribution* (L1251 부근)
  * *Advanced Maturity Analytics* (L1307 부근)
  * *OEQI Monthly Heatmap Matrix* (L1425 부근)
  * *CQMS Integration Monitor* (L1543 부근)
  * *Product Assessment Data Table* (L1625 부근)
  * *Maturity Progression Log* (L1679 부근)
  * *IQM Operations Guide* (L1731 부근)

- [ ] **Step 3: 동작 테스트 및 커밋**

  전체 구동 테스트 후 스테이징하여 커밋합니다.
  ```bash
  git add app/pages/_10_dashboard/iqm_plus_main_page.py
  git commit -m "refactor(iqm-dashboard): replace hardcoded headers with dashboard_section_header"
  ```

---

### Task 3: OE Quality Dashboard 리팩토링 이행

**Files:**
- Modify: `app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py` (임포트 보강 및 12개 섹션 타이틀 컴포넌트화)

- [ ] **Step 1: 임포트 최적화**

  상단 임포트 구문에 `dashboard_section_header`를 추가합니다.

- [ ] **Step 2: 12개 섹션 헤더 일괄 수정 (extra_info_html 파라미터 연동 적용)**

  우측에 `Trend Period`, `Unit: Score`, `Unit: Events` 등 가변 뱃지가 들어갔던 특별 소제목 사양까지 완벽 수용하도록 치환합니다.
  
  * *Global OE Quality Index Trend* (L514 부근)
  * *Regional Performance* (L561 부근)
  * *Quality Issue Distribution* (L597 부근)
  * *Mass Production Progression Tracker* (L624 부근)
  * *OEQI by Plant & OEM* (L751 부근)
  * *CQMS Trend Overview* (L826 부근)
  * *OEM Raw Data Logger* (L873 부근)
  * *Global OE Quality Grid* (L940 부근)
  * *OEQI Score Trend* (L962 부근)
  * *OEM Issue Share* (L984 부근)
  * *Timeline Progression* (L1006 부근)
  * *Plant Topology Network* (L1034 부근)
  * *Claims & Returns Log* (L1087 부근)

- [ ] **Step 3: 테스트 및 커밋**

  ```bash
  git add app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py
  git commit -m "refactor(oe-dashboard): replace hardcoded headers with dashboard_section_header"
  ```

---

### Task 4: 무결성 무결 검증 및 지식 그래프 업데이트

- [ ] **Step 1: 전체 Pytest 스위트 구동 검증**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: All tests PASS

- [ ] **Step 2: Graphify 지식 그래프 최신화**

  Run: `graphify update .`
  Expected: Successful node & edge compilation
