# [Design Spec] GT/WT 기준 중량 & 성형기 복합 시각화 대시보드 설계서 (2026-07-23)

본 문서는 GT/WT(그린중량 및 가류중량) 탭 하단에 새롭게 연동한 **기준 중량(`STD_WGT`) & 성형기(`BLDG_MC`) 복합 집계 데이터**를 효과적으로 시각화하기 위해 수립한 디자인 명세서 및 구현 명세서입니다.

---

## 1. 개요 및 목적 (Overview & Goal)

* **배경**: 기존에 단일 기준으로 분리되어 있던 성형기별, 규격별 품질 지표를 통합하여 **성형기 x 규격(기준중량)** 2차원 매트릭스 형태로 복합 집계했습니다.
* **목적**: 대형 다중 차트를 상하 인지 흐름(Top-Down Flow)에 맞게 배치하여 다음 두 핵심 가치를 달성합니다:
  1. **조감(C안 - 히트맵)**: 어떤 성형기가 어떤 규격 중량에서 불량이 많이 나는지 한눈에 색상 농도로 포착합니다.
  2. **대조(A안 - 그룹 바 차트)**: 발굴된 품질 취약 영역의 구체적인 합격률을 정량적으로 상세 비교합니다.

---

## 2. 시각화 컴포넌트 세부 디자인 (Visual Component Details)

### 컴포넌트 ①: 복합 품질 매트릭스 히트맵 (Heatmap - C안)

* **차트 유형**: `plotly.graph_objects.Heatmap`
* **축 및 지표 매핑**:
  * **X축**: **성형기 (`Building Machine`, `BLDG_MC`)**
  * **Y축**: **기준 중량 (`Standard Weight`, `STD_WGT`)** (직관적 인지를 위해 내림차순 정렬)
  * **Z축 (색상)**: **합격률 (`Pass Rate`, %)**
* **비주얼 세부 사양**:
  * **컬러 스케일 (Color Scale)**: 경고색(낮은 합격률, 예: `< 95%`)에서 브랜드 안정색(높은 합격률, `100%`)으로 매끄럽게 그라데이션 전환되는 다이내믹 맵 구성.
    - 최소값: 다홍/주황 계열 (`colors.orange_500` 활용)
    - 최대값: 차분한 진청/청록 계열 (`colors.blue_600` 및 `colors.slate_800` 활용)
  * **세포 내 글자 표기 (Cell Text Annotation)**: 
    - 각 히트맵 세포 내부에 **`합격률% (합격수량 / 검사수량)`** 텍스트 라벨을 직접 표기하여 정량적인 생산량 규모와 합격률을 더블클릭 없이 전수 조감합니다.
    - 예시: `98.5% (985/1k)` 또는 `98.50% (985/1,000)`

### 컴포넌트 ②: 성형기 x 규격 그룹 바 차트 (Grouped Bar Chart - A안)

* **차트 유형**: `plotly.express.bar(barmode='group')` 또는 `plotly.graph_objects.Bar`
* **축 및 지표 매핑**:
  * **X축**: **성형기 (`Building Machine`, `BLDG_MC`)**
  * **Y축**: **합격률 (`Pass Rate`, %)**
  * **색상 구분 (Legend)**: **기준 중량 (`Standard Weight`, `STD_WGT`)**
* **비주얼 세부 사양**:
  * 성형기별 기둥 그룹 내부에서 각 기준 중량의 합격률 높이를 정량적으로 즉각 비교할 수 있도록 설계합니다.
  * Y축 범위는 합격률 편차를 정밀히 포착할 수 있도록 `[90.0, 100.0]` 또는 데이터 최소값 기준 동적 하한선(Y-axis Auto-range with buffer)을 부여하여 미세 변동성을 보장합니다.

---

## 3. 데이터 흐름 및 가공 (Data Flow & Formatting)

### 전처리 가공 표준 (`plots_data_analysis.py` 내 처리)

1. **데이트-설비-수량 데이터 프레임 획득**:
   - `renderer_gt_wt.py`로부터 `df_gt_raw`를 전달받아, 플롯 드로잉 내부에서 다차원 Pivot 또는 Groupby 연산을 적용해 히트맵에 필요한 2D 매트릭스 및 어노테이션 텍스트 행렬을 가공합니다.
2. **수치 포맷팅 일치**:
   - 검사수량이 많아 텍스트가 겹치는 것을 완벽히 예방하기 위해 수량은 천 단위 컴마 `,` 포맷을 강제 적용합니다.
3. **공통 디자인 시스템 적용**:
   - 두 플롯 모두 리턴 직전 `apply_shadcn_style_to_figure(fig)`를 무조건 통과시켜 일관된 한글 폰트(`Pretendard, Inter`) 및 투명 캔버스 레이아웃(`rgba(0,0,0,0)`)을 적용합니다.

---

## 4. UI 배치 레이아웃 (Layout Design)

`renderer_gt_wt.py` 최하단에 다음과 같이 순차적으로 렌더링되도록 물리적 배치 구조를 구성합니다:

```python
st.divider()

# 1. 복합 현황 조감 - 히트맵
render_section_title("Weight Quality Matrix by Machine & Spec")
st.plotly_chart(fig_heatmap, use_container_width=True, key="gt_weight_heatmap_chart")

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# 2. 상세 정량 비교 - 바 차트
render_section_title("Weight Pass Rate Comparison by Machine & Spec")
st.plotly_chart(fig_bar, use_container_width=True, key="gt_weight_grouped_bar_chart")

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# 3. 집계 데이터 테이블 (복합형)
render_section_title("Weight Performance Summary by Standard Weight & Building Machine")
_render_gt_wt_combined_agg_table(df_gt_raw)
```

이 배치 구조는 **[대시보드 조감] ➡️ [상세 차트 대조] ➡️ [정량 테이블 실측]**의 깔끔하고 완벽한 인지적 하향식 도메인 분석 흐름을 형성합니다.
