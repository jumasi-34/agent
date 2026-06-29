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
