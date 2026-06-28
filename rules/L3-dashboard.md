---
id: rule.l3.dashboard
type: rule
status: active

summary: >
  L3 대시보드 UI 개발 규칙.
  Streamlit 화면 컨트롤러(page)의 역할과 제약(Plotly 인라인 금지, 시맨틱 컬러 매핑, 이모지 금지, 동적 컬럼 설정기 사용 등)을 정의한다.

keywords:
  - streamlit
  - dashboard
  - ui
  - layout
  - page

parent: "[[rules/rules-index]]"

related:
  - "[[rules/L2-architecture]]"
  - "[[rules/L2-color-system]]"
  - "[[rules/L3-plot]]"

consumers:
  - "[[agents/roles/planner-orchestrator]]"
  - "[[agents/roles/dashboard-layer-builder]]"
  - agent.ui_reviewer

updated: 2026-06-28---

# L3-dashboard.md (L3 대시보드 UI 개발 규칙)

## Overview
* **왜 존재하는가 (Why)**: Streamlit 화면 개발 시 UI 컨트롤러 레이어에 데이터 가공 및 차트 렌더링 세부 구현이 혼재되는 것을 방지하고, 일관된 디자인 시스템(ShadCN 스타일, 프리미엄 플랫 CSS)을 일괄 이식하여 고품질의 UX를 단일하게 보장하기 위함입니다.
* **언제 사용하는가 (When)**: `app/pages/` 내의 `*_page.py` 컨트롤러를 신규 작성하거나 기존 대시보드 UI를 리팩토링할 때 상시 준수합니다.
* **연계 실행 (Next Action)**: 이 레이아웃에서 렌더링할 고품질 Plotly 차트 세부 명세를 정의하려면 [.agents/rules/L3-plot.md](.agents/rules/L3-plot.md)를 연이어 연계 참조하십시오.

## Connections
* **상위 개념**: [.agents/rules/L2-architecture.md](.agents/rules/L2-architecture.md)
* **연관 자산**: 
  - [.agents/rules/L3-plot.md](.agents/rules/L3-plot.md)
  - [.agents/rules/L2-color-system.md](.agents/rules/L2-color-system.md)
---

## 1. 대시보드 UI 레이어의 핵심 역할 및 위치
- **위치**: `app/pages/` 아래 메뉴 번호 접두사가 붙은 폴더(예: `_10_dashboard/`)에 배치
- **파일명**: `*_page.py` 명명 규칙 준수
- **책임**: 사용자의 필터 선택을 입력받아 파라미터를 제어하고, 레이아웃을 구성하며, 최종 차트와 지표 카드를 화면에 렌더링(Control & Render)합니다.

---

## 2. 금지 규칙 (Strict Guardrails)
> [!IMPORTANT]
> 레이어 간 상호 작용 및 고수준 의존성 격벽 제약 조건은 단일 진실 공급원(SSOT)인 **[L2-architecture.md](.agents/rules/L2-architecture.md)**의 규칙을 엄격히 준수합니다.

1. **인라인 시각화 드로잉 금지 (No Inline Plotly)**:
   - UI 메인 파일(`*_page.py`) 내부에 수백 줄의 Plotly 차트 드로잉 코드를 작성하지 않습니다. 차트 작성 책임은 1:1 대칭 매핑 관계인 시각화 파일(`*_plots.py`)로 온전히 위임합니다.
2. **인라인 스타일 하드코딩 및 시맨틱 컬러 매핑 의무화**:
   - 페이지 내부에서 원시 CSS나 HTML 태그를 사용해 개별 요소를 스타일링하는 행위를 전면 금지합니다.
   - 모든 색상 사용 표준은 최상위 디자인 표준인 **[L2-color-system.md](.agents/rules/L2-color-system.md)**를 단일 진실 공급원(SSOT)으로 삼아 준수합니다.
   - UI 페이지 내의 표 배경, 통계 카드, 경고 표시 등에 색상을 바인딩할 때, 개별 Hex 코드를 하드코딩하거나 프리미티브 토큰(`colors.light_gray` 등)을 임의 대입하지 않고, 반드시 아키텍처에 맞게 추상화된 **Streamlit UI 시맨틱 계층**을 엄격히 준수합니다. (예: 테이블 배경은 `colors.app_surface_muted` 적용, 경고는 `colors.status_warning` 연동)
   - **Primary 주황색 고정 및 용도 엄격 제약**: 앱 브랜드 및 주요 액션 컬러는 주황색 계열(`app_primary`, `app_primary_hover` 등)로 고정되며, 이는 오직 주요 조작 버튼, 메뉴의 활성(Active) 선택 상태, 주요 수치 강조 등으로 제한되어 적용되어야 합니다.
3. **이모지 사용 전면 금지 및 Google Material Symbols 제한적 허용 (Strict Emoji-Free Design)**:
   - UI 페이지, 탭 라벨, 마크다운 텍스트, 버튼, 토스트, 에러/경고 메시지 및 소스 코드 내 주석을 포함한 모든 영역에서 일반 유니코드 이모지(Emoji)의 직접 사용을 엄격히 금지합니다.
   - 화면 디자인 상 반드시 아이콘을 사용해야 하는 경우에는 오직 Streamlit이 기본 지원하는 Google Material 아이콘 구문 (`:material/icon_name:`)만 사용해야 합니다.
   - 단, `st.success`, `st.error`, `st.warning`, `st.info`와 같이 자체 아이콘을 내장한 Streamlit 컴포넌트의 메시지 텍스트 안에는 불필요한 아이콘 구문을 추가하지 않고 순수 텍스트만 작성하여 가독성을 높입니다.

---

## 3. UI 개발 5대 표준
1. **1:1 대칭 매핑 아키텍처**:
   - 모든 화면은 **화면 컨트롤러(`*_page.py`)**와 **시각화 드로잉(`*_plots.py`)** 파일이 1:1 매핑되어 한 쌍으로 작동해야 합니다.
2. **공통 UI 모듈 (`app/core/ui/`) 최우선 참조**:
   - 일관성 있는 디자인을 위해 `components.py` 및 `styles.py`에서 제공하는 공통 컴포넌트(ShadCN 스타일 UI, 카드형 지표, mini_header 등)를 최우선으로 사용하여 화면을 구성합니다.
3. **입력 필터 파라미터 데이터클래스 조립**:
   - 사용자가 UI 필터(기간, 공장, 제품 등)로 선택한 값은 낱개 변수로 뿌리지 않고, 반드시 `app/core/params/parameters.py`의 전용 데이터클래스(`*Params`) 객체로 조립하여 서비스 함수로 전달합니다.
4. **세션 상태(Session State) 네임스페이스 통제**:
   - 임의의 문자열을 키로 사용하지 말고, `core/constants/` 또는 `core/page/` 등에 미리 정의된 표준 세션 상태 키 목록만을 바인딩하여 세션을 추적 및 관리합니다.
5. **동적 메타데이터 기반 컬럼 설정기 (`get_dynamic_column_configs`) 필수 연동**:
   - 화면 단에서 데이터프레임을 표출(`st.dataframe`, `st.data_editor` 등)하거나 차트에 바인딩할 때, SQL 쿼리 상에서 한글 AS 별칭을 임의 코딩하는 대신 반드시 `get_dynamic_column_configs` 동적 헬퍼를 활용해야 합니다.
   - 해당 헬퍼 함수는 테이블별 메타데이터(`local.data/query/metadata_*.json`)와 글로벌 공통 사전(`local.data/query/global_metadata.json`)을 동적으로 연동하여 한글 레이블, 소수점 자릿수 포맷, 컬럼 도움말(툴팁) 등을 일관성 있고 완벽하게 조립해 줍니다.
   - **사용 코드 표준 예시**:
     ```python
     from app.core.boilerplate_column_config import get_dynamic_column_configs

     # 'cqms_qi_mttc' 테이블의 메타데이터와 현재 데이터프레임 컬럼을 바인딩
     column_config = get_dynamic_column_configs("cqms_qi_mttc", df.columns)
     st.dataframe(df, column_config=column_config, use_container_width=True)
     ```

---

## 4. 표준 폴더 명명 규칙 (Directory Naming)
* **메뉴 정렬 제어 폴더**: `_<번호>_<카테고리명>/`
  - 예: `_10_dashboard/`, `_20_analysis/`, `_30_monitoring/`
* **메인 화면 페이지**: `*_page.py`
  - 예: `cqms_dashboard_page.py`

---

## 5. 프리미엄 플랫 디자인 및 타이틀 테두리 제거 표준 (Border-Free Header Standard)
> [!NOTE]
> Shadcn UI 연출을 극대화하기 위해 대시보드 내부 섹션 타이틀 및 통계 보드 주변에 불필요한 외곽선 상자(Border box)가 노출되는 것을 지양합니다.

1. **대시보드 통계 패널 테두리 오버라이드**:
   - `subheader_title_stats_panel` 컴포넌트 등으로 통계 지표 정보 패널을 생성할 때, 기본 테두리선과 배경색을 제어하기 위해 대시보드 메인 페이지의 `<style>` 태그 내부에 반드시 아래의 CSS 오버라이드 코드를 바인딩하여 플랫 디자인을 유지합니다.
   ```css
   /* subheader_title_stats_panel의 보더 및 배경 제거하여 border-free 플랫화 실현 */
   div[data-testid="stMarkdownContainer"] .shadcn-dashboard-info-panel,
   .shadcn-dashboard-info-panel {
       border: none !important;
       background-color: transparent !important;
       box-shadow: none !important;
       padding: 0.5rem 0rem !important;
   }
   ```
2. **미니멀 타이포그래피 일치화**:
   - 화면 내 소제목, 섹션 헤더 등은 디자인 시스템의 `colors.slate_800` 주조색과 `get_font_family('display')` 서체 패밀리를 바인딩해 고급스럽고 균형 잡힌 서체 가독성을 구현합니다.


## Related

[[Streamlit UI Development]]

