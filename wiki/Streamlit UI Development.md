---
title: "[Wiki] Streamlit UI 개발"
id: "wiki.streamlit ui development"
type: wiki
status: active
parent: "Architecture Guide.md"
related: ["Plotly Visualization System.md"]
consumers: ["../agents/roles/dashboard-layer-builder.md"]
updated: 2026-06-29
---
# Streamlit UI Development (Streamlit 화면 개발 및 제어 표준)

## 1. 왜 존재하는가 (Why)
이 가이드는 Streamlit 위젯의 생명 주기 관리 및 세션 상태 제어 시 빈번히 발생하는 런타임 충돌과, 사용자 테마 및 브라우저 환경에 따른 다크/라이트 모드 스타일 엇박자를 방지하기 위해 존재합니다. 엄격한 UI 제어 규칙을 통해 화면 깜빡임이 없고 로딩 성능이 최적화된 프리미엄 비주얼 대시보드를 유지할 수 있습니다.

## 2. 어디와 연결되는가 (Connections)
- **3-Layer 계층 정합성**: UI 컴포넌트의 물리적 설계 원칙은 [Architecture Guide](Architecture Guide.md)에 전적으로 바인딩됩니다.
- **차트 및 인라인 요소 렌더링**: 화면 내부의 Plotly 차트 및 아이콘 시스템은 [Plotly Visualization System](Plotly Visualization System.md)의 컴포넌트 사양을 참조합니다.
- **기획 및 탭 화면 레이아웃**: 대시보드의 화면 구성 및 분기 탭 기획 표준은 [PRD Planning Workflow](PRD Planning Workflow.md)와 직접 연계됩니다.

## 3. 무엇을 이해해야 하는가 (What)
- **세션 상태 가로채기(Session Interception) 기법**:
  - Streamlit의 고유 제약에 따라 `key`가 할당되어 화면에 이미 인스턴스화된 위젯에 `st.session_state[key] = value` 형태로 동적으로 값을 직접 할당해 수정하려 하면 `StreamlitAPIException`이 유발됩니다.
  - 이를 방지하기 위해 위젯이 선언되기 바로 직전 단계에서 해당 세션 키의 값을 검사하고 청소하거나 선행 주입하는 가로채기(Interception)를 활용해야 합니다.
- **다크 & 라이트 하이브리드 CSS 표준**:
  - 사용자의 OS 미디어나 강제 다크 모드 속성에 의존하지 않고, Streamlit 빌트인 CSS 커스텀 변수(예: `--text-color`, `--background-color`, `--secondary-background-color`)를 SSOT로 상시 적용하여 가독성 가림 현상을 방지합니다.
- **로딩 최적화**: 
  - 불필요한 전체 렌더링을 방지하기 위해 부분 갱신 조각(Fragment)과 스마트 캐싱을 적절히 구성합니다.

## 4. 단독 기동 세이프가드 및 ECharts 컴포넌트 통합 표준 (Standalone Safeguard & ECharts Integration)
- **독립 페이지 단독 구동 시 레이아웃 쏠림 해결 (`layout="wide"`)**:
  - 메인 `app.py` 프레임워크를 통하지 않고 각 서브 대시보드 화면(`app/pages/` 하위)을 단독으로 다이렉트 실행 시, Streamlit 기본값이 `layout="centered"`로 작동하여 전체 UI 및 제목 타이틀이 정중앙으로 강제 수축·밀리는 시각적 불균형이 유발됩니다.
  - 이를 예방하기 위해, 모든 개별 화면 페이지의 진입 초입부(`SECTION 2`)에 아래와 같은 글로벌 세이프가드를 탑재하여 항상 `wide` 화면 폭을 보증함으로써 좌측 상단 좌우 대칭 타이틀 레이아웃을 엄수합니다:
    ```python
    try:
        st.set_page_config(layout="wide", page_title="Data Analysis")
    except Exception:
        # app.py 메인에서 기 지정된 set_page_config가 이미 실행 중일 경우의 이중 호출 예외 방어
        pass
    ```
- **범용 ECharts 레이더 차트 고도화 (Multi-Series & JsCode Formatter)**:
  - 레이더 차트의 수평 시각적 균형과 정밀 렌더링을 위해 최대 축 범위를 고정(`max_val=15.0`)하고, 반지름(`radius: "70%"`) 및 중심 정렬(`center: ["50%", "46%"]`)을 최적화하여 인접 컴포넌트들과의 수직 정렬을 완전하게 일치시킵니다.
  - 다중 데이터 비교 시각화 지원을 위해 `values` 리스트와 `series_colors`, `series_symbols`의 유연한 확장을 수용하며, 특정 연간 평균(Average) 데이터의 불필요한 마커('dot')를 제거하는 포맷팅(`series_symbols=["circle", "none"]`)을 동적으로 적용합니다.
  - 데이터 오버 시 툴팁 내 수치가 날것으로 출력되거나 일그러지는 현상을 차단하기 위해 `streamlit_echarts.JsCode` 기반의 동적 툴팁 포매터를 활용하여, 소수점 첫째자리(`.1f`) 및 한글 축 설명을 이모지 배제 규칙 하에 품격 있게 빌드합니다.

