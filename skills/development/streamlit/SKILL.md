---
name: "developing-with-streamlit"
description: "Use for ALL Streamlit tasks: creating, editing, debugging, beautifying, styling, theming, optimizing, or deploying Streamlit apps. Also custom components, st.components.v2, HTML/JS/CSS work. Discovers and loads version-matched reference docs from the user's installed Streamlit (>=1.57). Triggers: streamlit, st., dashboard, app.py, beautify, style, CSS, color, background, theme, button, widget styling, custom component, st.components, CCv2, session state, performance, cache, fragment, slow rerun, deploy."
id: skill.development.streamlit
title: "Skill: DEVELOPMENT > STREAMLIT"
type: skill
status: active

parent: "[[skills/index.md]]"

related:
  - "[[skills/index.md]]"
  - rule.streamlit.widget_key

consumers:
  - agent.all

updated: 2026-06-28
---

# Developing with Streamlit

## Overview / Connections
* **Parent (상위 개념)**: [[skills/index.md]]


Streamlit (>=1.57) ships detailed reference documentation for building Streamlit apps inside its pip package. The bundled skill is a routing `SKILL.md` plus a `references/` folder of topic-specific reference docs (dashboards, themes, layouts, session state, custom components, etc.).

## Usage

Run the discovery script with the user's project directory:

```bash
python <SKILL_DIR>/scripts/discover.py --project-dir <USER_PROJECT_DIR>
```

The script prints either:

- **A path on stdout** (exit 0) — the bundled `SKILL.md`. Read it; it points into `references/`.
- **An `ERROR:` block on stderr** (non-zero exit). Follow the printed instructions and re-run.

`<SKILL_DIR>` is the directory containing this file; `<USER_PROJECT_DIR>` is the absolute path to the user's project. Passing `--project-dir` matters because the script resolves `.venv`, `../.venv`, `Pipfile`, `poetry.lock`, `pdm.lock`, and `uv.lock` relative to it.

---

## 3. 프리미엄 Plotly 컴포넌트 위임 개발 및 디자인 가이드라인

향후 에이전트 및 개발자가 대시보드 내의 다양한 시각화(Plotly 등) 개선 요청을 수신하였을 때, 본 프로젝트의 정합성과 최고 수준의 룩앤필을 보증하기 위해 반드시 아래의 위임 설계 및 디자인 표준을 이행해야 합니다.

### ① 공용 컴포넌트 격리화 및 위임 설계 패턴 (Safety Lock 준수)
- 각 화면 페이지 컨트롤러(`*_page.py`)나 개별 플롯 파일(`*_plots.py`) 내에 차트 드로잉 및 상세 스타일 코드가 직접 하드코딩 및 노출되는 것은 엄격히 통제합니다.
- 대신, `app/core/plot/components.py` 내에 공용 프리미엄 시각화 컴포넌트 클래스(예: `PremiumDonutPlot`, `PremiumParetoPlot` 등)로 캡슐화하여 일원화하여 개발 및 유지 관리합니다.
- 기존의 레거시 시각화 함수 인터페이스(예: `fig_scrap_rate`, `fig_pareto` 등)의 내부 구현부만 해당 공용 컴포넌트의 인스턴스를 선언하고 `.render()` 결과를 반환하는 구조로 Surgical Edit(수술식 변경)을 이행합니다. 
- 이로 인해 화면 페이지의 직접적인 비즈니스 렌더링 로직의 오작동 및 충돌을 완벽히 격리(Safety Lock)하며, 동시에 호출만으로 프리미엄 룩앤필이 대시보드 전반에 자동 확산 및 적용되는 강력한 확장성을 획득합니다.

### ② 디자인 시스템의 3단계 위계 컬러 및 폰트 토큰 바인딩 
- 모든 Plotly 레이아웃, 트레이스, 범례, 수평/수직 기준 가이드선 및 shading 영역 등에 사용되는 색상은 직접 실물 HEX/RGBA 값(예: `#ef4444`, `#cbd5e1` 등)을 하드코딩하지 않습니다.
- 반드시 `app/core/design_system/tokens/colors.py` 내에 정의된 물리 토큰(Primitive)과 이를 의미적으로 바인딩한 의미 토큰(Semantic - 예: `colors.green_500`, `colors.slate_300`) 위계를 충실히 경유하여 호출 및 적용해야 합니다.
- 다크/라이트 테마의 유연성을 위해 그리드선, 가이드선, Shading 투과 레이어 등은 은은한 반투명 투과 값(예: `rgba(128, 128, 128, 0.15)`)을 영리하게 결합해 상호 대비도를 가시적으로 보정합니다.
- 폰트 적용 시 브라우저 기본 폰트를 배제하고, `get_font_family("display")` (제목군) 또는 `get_font_family("primary")` (본문/라벨군) 폰트 토큰 호출을 레이아웃 딕셔너리에 필수 매핑합니다.

### ③ 고가용성 공용 툴팁(Tooltip) 어댑터 100% 장착 수칙
- 모든 Plotly 마우스 호버 장치(`hovertemplate`) 내에 하드코딩되거나 산만한 텍스트 정보가 임의로 기재되지 않도록 철저히 차단합니다.
- 반드시 `app/core/design_system/plot/tooltip/adapters.py`에 마련된 표준형 툴팁 어댑터(`create_donut_tooltip`, `create_bar_tooltip`, `create_line_tooltip` 등)를 최종 trace의 `hovertemplate` 인자에 필히 결합하여 정돈되고 고급스러운 툴팁 룩앤필을 균일하게 보증합니다.

### ④ 수치 가독성 및 가시적 관리선 레이아웃 정합성
- 대형 차트(예: 파레토, p-관리도) 렌더링 시, 80% 누적 한계선(UCL, LCL 쉐이딩 밴드 가이드) 등 비즈니스 제약 가이드라인을 은은한 점선과 레이어 Shading으로 영리하게 제공하여 해석 편의를 도모합니다.
- 또한 우상단 구석 등에 가시적인 KPI Summary Annotation Box(예: "평균 불량률 (pbar) = 0.25%")를 매끄러운 반투명 카드 배너 형태로 가산하여 현장 관리 정합성을 극대화합니다.

## Related

[[Streamlit UI Development]]
[[Plotly Visualization System]]
