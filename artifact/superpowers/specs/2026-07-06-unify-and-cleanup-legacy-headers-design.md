---
id: spec.unify-and-cleanup-legacy-headers
title: "[Spec] Unify and Cleanup Legacy Headers Design"
type: specification
status: proposed
summary: >
  Streamlit 헤더 위젯들의 중복을 완전히 청소하고, section_header 단일 다이나믹 라우터로 완전히 일원화하여 기존 레거시 함수(dashboard_header, stats_header, subheader_title_panel, dashboard_section_header, subheader_title_stats_panel)를 제거하는 디자인 스펙입니다.
updated: 2026-07-06
---

# Unify and Cleanup Legacy Headers Design Spec (헤더 컴포넌트 일원화 및 잔재 제거 설계)

본 문서는 `app/core/design_system/streamlit_widgets.py` 내에 존재하는 다양한 소제목/스탯/대시보드 헤더의 중복 잔재들을 단일 인터페이스 `section_header`로 완전히 병합 및 라우팅하고, 기존 레거시 함수를 완벽히 소멸시키기 위한 설계 사양(SSOT)입니다.

---

## 1. 목적 및 배경
- **중복 최소화 및 인터페이스 단일화**: 현재 `streamlit_widgets.py`에는 `section_header`가 구현되어 부분적인 자동 분기(type1, type2, type3)를 지원하고 있지만, 여전히 `dashboard_header`나 `stats_header`와 같은 동등한 계층의 대형 헤더 컴포넌트가 별도 정의되어 중복 스타일 코드를 유발하고 있습니다.
- **호출 구조 슬림화**: 사용자의 명시적 요청에 맞춰 불필요한 구버전 래퍼 및 레거시 헤더 함수들을 전량 삭제하고, 프로덕션의 유일한 레거시 참조 지점을 최신 `section_header` 호출로 완벽하게 마이그레이션하여 유지보수성을 극대화합니다.

---

## 2. 핵심 변경 범위 및 설계

### ① app/core/design_system/streamlit_widgets.py 개정
`section_header`가 메인 진입점이 되며, `header_type` 매개변수를 통해 다이나믹하게 스타일(표준형, 대시보드형, 통계형)을 라우팅하도록 리팩토링합니다.

- **`section_header` 인터페이스 정의**
  ```python
  def section_header(
      title: str,
      subtitle: str | None = None,
      info_items: list[dict[str, str]] | None = None,
      icon_name: str | None = None,
      top_margin: str | None = None,
      bottom_margin: str | None = None,
      basic_info: dict[str, str] | None = None,
      header_type: Literal["standard", "dashboard", "stats"] = "standard",
      **kwargs,
  ) -> None:
  ```

- **타입별 스타일/레이아웃 매핑 스펙**
  1. `header_type == "standard"` (기본값)
     - 폰트 크기: `1.15rem`
     - 보더 하단: 얇은 border(`has_border=True`, 패딩 주입)
     - 아이콘 크기: `1.15rem` (클래스: `CSSClasses.MINIHEADER_TITLE_ICON`)
     - 마진: 상단 `spacing.space_5`, 하단 `spacing.space_3`
     - 우측 영역: `basic_info`가 존재할 시 Type 3(상세 스펙 카드), `info_items` 3개 이상 시 Type 2(스탯 카드 그리드), 2개 이하 시 Type 1(컴팩트 메트릭) 자동 라우팅
  2. `header_type == "dashboard"`
     - 폰트 크기: `1.35rem` (대시보드 메인 레이아웃용)
     - 보더 하단: 없음 (`has_border=False`)
     - 아이콘 크기: `1.6rem`
     - 마진: 상단 `spacing.space_6`, 하단 `spacing.space_5`
     - 우측 영역: `extra_info_html` (만약 `kwargs`나 파라미터로 제공될 경우 우측 렌더링 지원)
  3. `header_type == "stats"`
     - 폰트 크기: `1.35rem`
     - 보더 하단: 보더 있음 (`has_border=True`, 패딩 주입)
     - 아이콘 크기: `1.35rem` (클래스: `CSSClasses.DASHBOARD_TITLE_ICON`)
     - 마진: 상단 `spacing.space_6`, 하단 `spacing.space_5`
     - 우측 영역: 대시보드 통계 그리드(`_build_stats_html(info_items)`) 강제 적용

- **완전 삭제 대상 레거시 함수 (Deprecated 및 Residual 전수 제거)**
  - `dashboard_header`
  - `dashboard_section_header`
  - `stats_header`
  - `subheader_title_stats_panel`
  - `subheader_title_panel`

### ② app/pages/_40_collaboration/qrs_worksheet_monitoring_page.py 이관
- **임포트부 수정**
  - `from app.core.design_system.streamlit_widgets import stats_header` -> `from app.core.design_system.streamlit_widgets import section_header`
- **호출부 수정** (라인 407, 990 부근)
  - `stats_header(...)` 호출을 `section_header(..., header_type="stats")` 형태로 변환합니다.

---

## 3. 테스트 및 검증 전략
- **유닛 테스트 개정 (`tests/test_streamlit_widgets.py`)**
  - 기존 레거시 함수를 테스트하던 코드가 있을 경우 전면 청소합니다.
  - `test_smart_section_header_routing_and_svg` 내에 `header_type` 옵션들(`"standard"`, `"dashboard"`, `"stats"`)이 올바른 HTML 포맷과 스타일 토큰들을 문제없이 빌드하고 주석 처리 없이 렌더링하는지 세밀하게 검증하는 단계를 추가합니다.
- **통합 검증**
  - `pytest tests/test_streamlit_widgets.py` 명령을 실행해 어떠한 TypeError나 빌드 결함도 발생하지 않고 100% PASS함을 확인합니다.

---

## 4. 제약 및 준수 조항
- **이모지 전면 차단**: 주석, 코드 내 독스트링 등에 이모지 절대 금지.
- **한국어 독스트링**: 신규 및 수정된 코드 내부 주석과 문서화 블록은 한국어 표준 주석 규격을 엄격히 지킵니다.
- **WSL 링크 의무**: 모든 문서 연결은 상대 경로로만 관리합니다. 예: [app/core/design_system/streamlit_widgets.py](app/core/design_system/streamlit_widgets.py)
