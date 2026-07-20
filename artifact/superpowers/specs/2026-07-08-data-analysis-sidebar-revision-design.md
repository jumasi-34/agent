# Data Analysis Page Sidebar Revision Design

## 1. 개요 (Overview)
본 문서는 데이터 분석 페이지(`app/pages/_20_analysis/data_analysis_page_dev.py`)의 사이드 패널(사이드바) UI/UX를 개선하기 위한 상세 설계 문서입니다. 기존에 대메뉴 전환 버튼처럼 작용하여 혼란을 주던 **ANALYTIC MENU** 영역을 세련된 **Analysis Mode** 선택기로 단일 페이지 내의 기능적 흐름으로 재통합하고, 각 분석 기법에 부합하는 필터만 동적(Dynamic)으로 노출하여 깔끔하고 몰입감 있는 분석 경험을 제공하는 것을 목표로 합니다.

---

## 2. 해결하고자 하는 문제 (Problem Statement)
- **메뉴 진입의 물리적 격리감**: "IQM Plus Only", "Period", "Break Point"가 사이드바 최상단에서 크고 볼드한 버튼 형태로 제공되어, 사용자로 하여금 "데이터 분석"이라는 하나의 맥락 아래에 존재하는 세부 조회 옵션이 아니라 아예 독립된 3개의 다른 페이지로 화면이 바뀐다는 인상을 줍니다.
- **불필요한 인풋 상시 노출**: 분석 방식에 따라 필요한 인풋 항목이 다른데(예: IQM Plus는 날짜 선택이 불필요하고 M-Code를 Selectbox로 선택하지만, Period/BP는 날짜 지정 및 M-Code 직접 입력이 필요), 이들이 명확히 구분되지 않고 복잡한 조건식으로 사이드바 렌더러에 어수선하게 얽혀 있습니다.

---

## 3. 개선 상세 설계 (Detailed Design)

### ① UI 레이아웃 구조 (Layout & Hierarchy)
사이드바는 아래의 3대 구획으로 재구조화됩니다.

#### [A] SECTION 1. ANALYSIS MODE (분석 모드 정의) - 최상단 배치
기존의 세로형 거대 버튼을 제거하고, 세련된 가로 슬라이딩 카드 토글 형태의 `st.segmented_control`을 배치합니다.
- **기동 옵션**: `IQM_PLUS`, `PERIOD`, `BP`
- **라벨 매핑**:
  - `IQM_PLUS` -> `IQM Plus Only`
  - `PERIOD` -> `Period Analysis`
  - `BP` -> `Break Point`

#### [B] SECTION 2. DYNAMIC SEARCH FILTERS (동적 필터 입력 영역)
선택된 분석 모드 세션 상태에 근거하여, 사용자 인풋 필드가 유기적으로 빌드 및 전환됩니다.

| 분석 모드 (Selected Mode) | M-Code 입력 방식 | 날짜 범위 (Date Range) 입력 | 추가 필터 (Extra Filter) |
| :--- | :--- | :--- | :--- |
| **IQM Plus Only** (`IQM_PLUS`) | `st.selectbox` (마스터 목록에서 안전한 선택) | `st.info` (마스터 DB 기준 자동 계산된 1개년 범위를 읽기 전용 텍스트 알림창으로 표시) | 없음 |
| **Period Analysis** (`PERIOD`) | `st.text_input` (7자리 규격 직접 입력) | `st.date_input` (사용자 수동 범위 선택) | 없음 |
| **Break Point** (`BP`) | `st.text_input` (7자리 규격 직접 입력) | `st.date_input` (사용자 수동 범위 선택) | `Break Point Date` (`st.date_input` 단일 날짜 선택기 추가 노출) |

#### [C] SECTION 3. VIEW PREFERENCE & RUN (결과 조회 조건 및 제출)
- **집계 단위** (`st.segmented_control`): 주 단위(Weekly) / 월 단위(Monthly) 단일 선택.
- **Run Query & Analysis** (`st.form_submit_button`): 폼 조회를 시작하는 전체 가로폭 규격의 주 액션 버튼.

---

## 4. 데이터 흐름 및 상태 보존 (Data Flow & State Management)
- **세션 상태 가로채기(Interception)**: `st.segmented_control`이 변경될 때마다 화면이 리런(st.rerun)되며, 기존 `params` 데이터 모델 객체의 `step0_selected_menu` 필드에 상응하는 비즈니스 한글/영어 텍스트(`MENU_SELECT_DICT` 매핑 값)가 즉시 가로채어져 자동 바인딩됩니다.
- **일관성 보장**: 이 통합 변환 레이어를 통해, 탭별 연산 로직(`_render_tab_overview`, `_render_tab_ncf` 등)과 시각화 쿼리 백엔드 모듈(`app/service/data_analysis_df.py`)은 단 한 줄의 손상이나 수정 없이 안전하게 그대로 재사용됩니다.

---

## 5. 검증 및 수동 테스트 시나리오 (Verification & Test Plan)
1. **화면 부트스트랩 검증**: 화면 최초 진입 시 최상단에 `Analysis Mode` 가로형 토글이 "IQM Plus Only" 기본 상태로 안전하게 노출되는지 확인합니다.
2. **동적 렌더링 검증**:
   - `Period Analysis` 클릭 시 M-Code 입력창이 텍스트 필드로 전환되며, 날짜 입력 범위 위젯이 등장하는지 확인합니다.
   - `Break Point` 클릭 시 `Break Point Date` 위젯이 추가로 하단에 생성되는지 확인합니다.
   - `IQM Plus Only` 재클릭 시 다시 M-Code 선택 상자가 활성화되며 날짜 범위가 정보 알림창 형태로 비활성화되는지 확인합니다.
3. **분석 쿼리 정상 작동 검증**: 각 모드에서 `Run Query & Analysis` 버튼 클릭 시, 하단의 Overview 탭 및 NCF, Rework 등 서브 탭의 Plotly 시각화 차트와 프리미엄 메트릭 행들이 실시간으로 데이터를 성공적으로 수집하여 렌더링하는지 정량 체크합니다.
