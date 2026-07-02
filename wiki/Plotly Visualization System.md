---
title: "[Wiki] 시각화 시스템 설계"
id: "wiki.plotly visualization system"
type: wiki
status: active
parent: "Architecture Guide.md"
related: ["Streamlit UI Development.md"]
consumers: ["../agents/roles/data-insights-analyst.md"]
updated: 2026-07-02
---
# Plotly Visualization System (Plotly 시각화 및 컴포넌트화 지침)

## 1. 왜 존재하는가 (Why)
이 가이드는 대시보드의 비주얼 핵심인 차트 및 시각 요소들이 개별 화면 모듈 내에 스파게티 형태로 혼재되어 노출되는 것을 차단하고, IBM Carbon 테마 기반의 고급스러운 디자인을 일관성 있게 구현하기 위해 존재합니다. 시각화를 컴포넌트화하고 레이아웃 및 디자인 컬러 시스템을 정적 격리함으로써 프리미엄 UI 미학을 달성합니다.

## 2. 어디와 연결되는가 (Connections)
- **UI 화면 레이아웃 및 렌더링**: 개별 차트 컴포넌트의 화면 배치는 [Streamlit UI Development](Streamlit UI Development.md)를 통해 동적으로 주입됩니다.
- **데이터 공급 및 전처리 정합성**: 차트가 소비하는 데이터의 3-Layer 정합성은 [Architecture Guide](Architecture Guide.md)의 명세를 이행합니다.
- **비즈니스 지표 가독성**: 데이터 시각화의 수식 조건부 강조 및 다국어 축 설명은 [Quality Metric & Business Rules](Quality Metric & Business Rules.md)를 기반으로 가공됩니다.

## 3. 무엇을 이해해야 하는가 (What)
- **Plotly의 철저한 컴포넌트화**:
  - 차트 개별 파일(`*_plots.py` 등) 내부에 생짜 차트 드로잉 코드가 직접 노출되거나 중복 생성되어서는 안 됩니다. 공통 컴포넌트 클래스(Factory 패턴)로 철저히 캡슐화하여 단일 관리해야 합니다.
- **디자인 컬러의 3단계 위계 준수**:
  - 실물 HEX/RGBA 값을 코드 내에 하드코딩해서는 절대 안 됩니다. 
  - `PrimitiveColors` (원천 값 선언) $\rightarrow$ `SemanticColors` (의미 기반 매핑) $\rightarrow$ 최종 Plot/CSS 컴포넌트 호출의 3단계 위계를 관철하여 일관된 채도와 배색을 완성합니다.
- **인라인 아이콘의 Lucide SVG 단일화**:
  - 일반 유니코드 이모지 사용을 엄격히 차단하며, 인라인 SVG 아이콘의 렌더링은 Lucide 표준을 단일 SSOT로 활용하여 렌더링합니다.

## 4. 프리미엄 툴팁 직렬화 및 결측치 방어 설계 (Robust Tooltip Design)
- **Numpy 3D Array JSON 직렬화 한계 극복**:
  - Plotly Python SDK에서 `customdata`에 넘파이 3차원 배열(`np.stack` 결과 등)을 대입해 프론트엔드의 Plotly.js 엔진으로 직렬화할 때, 구조 왜곡으로 인해 템플릿의 셀 단위 인덱싱(`%{customdata[0]}`)이 원천 무력화되어 툴팁이 일그러지는 한계가 존재합니다.
  - 이를 원천 방지하기 위해 다차원 구조 끝단에 반드시 **`.tolist()`**를 가동하여 완벽한 순수 파이썬 중첩 리스트(`list of lists of lists`) 구조로 형변환한 뒤 전달해야 합니다.
- **결측치(NaN) 포맷팅 템플릿 크래시 차단**:
  - 조회 기간 내 실적이 없는 결측치 셀(`NaN`)의 경우, Plotly 템플릿 엔진(`hovertemplate`) 내에서 실수 포맷팅(`%{z:.1f}%`)을 가동하는 과정에서 렌더링 파이프라인 전체가 파쇄되는 크래시가 발생할 수 있습니다.
  - 이를 위해 결측치를 포괄한 합격률 문자열 2차원 리스트(`pass_rate_str_matrix`)를 파이썬 서비스단에서 직접 가공(예: `NaN` 시 `"- "`, 정상 시 `"95.3%"`)하여 `customdata`에 바인딩하고, 템플릿 내에서는 실수 연산 없이 단지 문자열 **`%{customdata[2]}`** 형태로 바로 표시하는 설계가 가장 견고합니다.
