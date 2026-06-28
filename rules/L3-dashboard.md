---
id: rule.l3.dashboard
title: "[Rule] Streamlit UI 구성"
type: rule
status: active

summary: >
  L3 대시보드 UI 개발 규칙.
  Streamlit 화면 컨트롤러(page)의 역할과 제약(Plotly 인라인 금지, 이모지 금지, 동적 컬럼 설정기 사용 등)을 정의한다.

keywords:
  - streamlit
  - dashboard
  - ui

parent: "[[rules/rules-index.md]]"

related:
  - "[[rules/L2-architecture.md]]"
  - "[[rules/L2-color-system.md]]"
  - "[[rules/L3-plot.md]]"

consumers:
  - agent.all

updated: 2026-06-29
---


# L3-dashboard.md (L3 대시보드 UI 개발 규칙)

본 문서는 일관되고 균형 잡힌 사용자 경험(UX)과 프리미엄 디자인 일관성을 사수하기 위해 Streamlit UI 렌더링 명세를 정의한 **단일 진실 공급원(SSOT) 규칙**입니다.

---

## 1. 대시보드 UI 레이어의 핵심 역할 및 위치
* **위치**: `app/pages/` 하위 메뉴 번호 접두사 폴더(예: `_10_dashboard/`)에 격리 배치
* **파일명**: `*_page.py` 명명 규칙 준수 (예: `cqms_dashboard_page.py`)
* **책임**: 사용자의 필터 선택을 입력받아 파라미터를 제어하고, 레이아웃을 구성하며, 최종 차트와 지표 카드를 화면에 배치(Control & Render)합니다.

---

## 2. 금지 및 제약 수칙 (Strict Guardrails)

1. **인라인 시각화 드로잉 금지**: UI 컨트롤러 파일 내부에서 복잡한 차트 드로잉 코드를 직접 기술하지 않습니다. 차트 레이아웃 구성 및 세부 드로잉 책임은 무조건 1:1 대칭 매핑인 `*_plots.py` 파일로 완전히 전담시킵니다.
2. **이모지 사용 전면 금지**: UI 페이지, 탭 라벨, 마크다운 텍스트, 버튼, 토스트 및 주석을 포함한 어떠한 영역에서도 일반 유니코드 이모지(별, 경고 등)를 사용할 수 없습니다. 아이콘이 필수적인 물리 영역은 오직 구글 머티리얼 심볼(`:material/icon_name:`)만을 활용합니다.
3. **용도 기반 시맨틱 컬러 매핑**: 개별 HEX 코드를 하드코딩하거나 1단계 프리미티브 컬러 상수를 임의 대입하는 것을 금지하며, 반드시 의미론적으로 추상화된 Streamlit UI 컬러 토큰(`colors.app_surface_muted` 등)을 바인딩합니다. 주 브랜드 주황색 계열(`app_primary`)은 버튼, 활성 탭 등 주요 조작 상태 및 수치 강조용으로 엄격히 한정 적용합니다.

---

## 3. 대시보드 UI 개발 4대 표준

1. **공통 UI 모듈 (`app/core/ui/`) 활용**: 페이지 내부에서 자체 HTML/CSS 인라인 스타일을 구구절절 기입하지 않고, 공통 컴포넌트인 `components.py` 및 `styles.py`에서 제공하는 규격 컴포넌트(ShadCN 스타일 UI, 카드형 지표 등)를 임포트하여 활용합니다.
2. **입력 필터 파라미터 캡슐화**: 화면 필터로부터 수집된 선택 데이터는 반드시 `app/core/params/parameters.py`의 전용 데이터클래스(`*Params`) 객체로 조립해 서비스 레이어의 인풋으로만 전달합니다.
3. **세션 상태(Session State) 통제**: 임의 변수명을 키로 쓰지 말고 `core/constants/` 또는 `core/page/` 등에 사전 선언된 세션 상태 키 목록을 엄격히 바인딩합니다.
4. **동적 메타데이터 컬럼 설정기 (`get_dynamic_column_configs`) 필수 연동**: 화면 단에서 데이터프레임을 표출할 때, 쿼리 내의 한글 AS 별칭 대신 반드시 `get_dynamic_column_configs` 헬퍼를 경유시켜 컬럼 레이블, 소수점 포맷, 도움말(툴팁)이 유기적 결합되게 합니다.

---

## 4. 대시보드 UI 레이어 4대 정합성 체크리스트

1. 차트 드로잉(Plotly) 소스 코드가 인라인에 작성되지 않고 `*_plots.py`로 완벽히 분리 전담되어 있는가?
2. 마크다운 본문, 버튼, 탭 제목 내에 유니코드 이모지가 철저히 차단되고, 아이콘이 필요한 곳에 Google Material Symbols를 대입했는가?
3. 표(dataframe) 렌더링 지점에서 한글 AS 오염 대신 `get_dynamic_column_configs` 동적 헬퍼를 경유시켜 결합을 완료했는가?
4. 스타일 처리를 위해 `app/core/ui/` 공통 라이브러리를 최우선적으로 참조하여 화면 간 일관성을 확보했는가?
