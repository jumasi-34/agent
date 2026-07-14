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

## 5. 월간 차트의 X축 문자열 매칭 정렬 버그 방지 표준 (X-axis Tick Alignment Standard)
- **문자열 월 데이터와 정수형 틱매칭 간극 현상**:
  - Plotly에서 데이터 소스의 월 'MM' 필드가 문자열(예: `"01"`, `"02"`, ...)이고, 레이아웃의 `tickvals`가 정수 배열(예: `[1, 2, ..., 12]`)로 인가되는 경우, Plotly는 x축을 카테고리 축(`category`)으로 자동 오판하게 됩니다.
  - 이 경우 데이터 포인트는 인덱스인 `0, 1, ..., 11` 상에 배치되는 반면, 월별 틱 라벨은 지정된 `tickvals` 위치인 `1, 2, ..., 12` 에 매핑되어, 실제 표시 시 차트 데이터와 축 눈금이 한 달씩 좌측으로 어긋나며 12월 틱이 비어 있게 되는 정렬 크래시가 발생합니다.
- **예방 및 방어 설계 수칙**:
  - 월 단위 시계열을 수치 축(`linear`)으로 완벽하게 수평 정렬하기 위해, 프론트엔드로 전달 전 데이터 프레임의 월(MM) 필드를 반드시 **정수형(`int`)으로 변환**하여 차트에 바인딩해야 합니다.
  - 이를 통해 수치 좌표 `1~12`와 `tickvals`의 `1~12` 좌표가 1:1 대응하여 시각화 정합성이 완벽하게 보장됩니다. 관련 시뮬레이션 및 사전 입증 테스트 하네스는 `tests/test_monthly_chart_bug.py`를 통해 구조적으로 영구 보존됩니다.

## 6. 타임스탬프 축 세로 가이드라인 및 실측 불량율(NG Rate) 계산 정합성 수칙 (Guideline & Stats Sync)
- **Plotly add_vline 내장 어노테이션의 pd.Timestamp sum() 타입 버그 극복**:
  - Plotly의 `add_vline` 함수에 `pd.Timestamp` 객체를 전달하면서 동시에 `annotation_text` 를 사용하면 Plotly 내부적으로 가로축 중심 평균을 구하기 위해 `_mean(X)` $\rightarrow$ `sum(x)` 가 호출됩니다.
  - 파이썬 내장 `sum` 은 초기값 `0` 에서 루프를 시작하여 `0 + Timestamp` 가 가동되고, Pandas 표준에 따라 `TypeError: Addition/subtraction of integers and integer-arrays with Timestamp is no longer supported` 에러가 나며 대시보드가 크래시됩니다.
  - **해결 방안 (Workaround)**: 이 에러를 차단하기 위해 세로 기준선(`add_vline`) 자체는 어노테이션 관련 매개변수 없이 독립 렌더링하고, 텍스트 라벨(예: `"BP Date"`)은 상대 좌표계(`yref="paper"`) 상에서 `fig.add_annotation` 을 사용해 직접 수동 배치하는 설계가 가장 완벽하고 안전합니다.
- **실측 불량율(NG Rate)과 가이드라인의 100% 물리적 동조화 (Single Source of Truth)**:
  - 대시보드 속 정보 카드의 `Lower / Upper NG %` 실측 계산 시, 원시 제품 규격이 아니라 **차트에 실제로 드로잉되어 눈에 보이는 Limit 점선(예: Both 상태 시 lcl/ucl, Max Limit 상태 시 idx - 0.3 등)**을 그대로 불량율 연산의 한계치로 사용해야 합니다.
  - 가이드라인 드로잉 분기 조건과 불량율 연산 기준선 추출 조건을 단일 조건 변수(`is_both_spec` 플래그) 하에서 완벽하게 상호 동조화시킴으로써, 화면 속 점선 밖의 실제 측정 도트들과 정보 카드의 수치 정보가 한 치의 단수 오차도 없이 논리적으로 완전하게 수렴하는 최상의 정합성을 보장합니다.


