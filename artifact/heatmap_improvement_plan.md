---
id: wiki.heatmap_improvement_plan
title: "[Wiki] [Plan] Uniformity 탭 설비 합격률 히트맵 시각화 개선 계획"
type: wiki
status: active
summary: >
  본 문서는 이 세션에서 생성/수정된 [Wiki] [Plan] Uniformity 탭 설비 합격률 히트맵 시각화 개선 계획 자산입니다.
updated: 2026-07-02
---

# [Plan] Uniformity 탭 설비 합격률 히트맵 시각화 개선 계획

본 문서는 Uniformity(균일성) 분석 탭 내 **기기 × 기간 합격률 히트맵(Heatmap)** 영역을 기존 대시보드의 프리미엄 룩앤필 및 관련 정적 규칙들과 조화롭게 결합하고, 실질적인 시인성과 품질을 극대화하기 위해 수립된 **다차원 개선 설계 제안서**입니다.

---

## 1. 기반 규칙 및 설계 정합성 (Single Source of Truth)

본 개선 계획은 프로젝트의 디자인 핵심 헌법 및 시각화 표준 문서들의 요구 사항을 100% 준수합니다.

* **디자인 및 배색 헌법**: [.agents/rules/L2-color-system.md](../.agents/rules/L2-color-system.md)  
  * *핵심 사상*: "Streamlit UI는 프로젝트 자체 원천 컬러셋을 적용하고, Plotly 데이터 시각화 팔레트는 Carbon Data Visualization 철학을 철저히 따른다."
* **플롯 시각화 격리 규칙**: [.agents/rules/L3-plot.md](../.agents/rules/L3-plot.md)  
  * *핵심 제약*: 무의미한 원시 HEX 하드코딩 금지, 투명 배경(`rgba(0,0,0,0)`) 일관화, 문법 및 레이아웃 정합성 체크리스트 충족.
* **시각화 사양 기획서**: [app/pages/_20_analysis/data_analysis_plots_prd.md](../app/pages/_20_analysis/data_analysis_plots_prd.md)  
  * *핵심 배색*: **95% Grayscale (Slate 명도 대비) + 5% Anomaly Accent (Orange_500)**
  * *히트맵 세부 규정*: "정상적인 고합격률(80% ~ 100%) 구간은 `colors.slate_100`에서 `colors.slate_800`으로 이어지는 Grayscale 흐름, 위험 이탈(80% 미만) 저합격률 구간은 `colors.orange_500` 핫스팟 발색 적용."

---

## 2. 현행 구현 분석 및 한계점 (As-Is vs. To-Be)

현재 [app/pages/_20_analysis/data_analysis_plots.py](../app/pages/_20_analysis/data_analysis_plots.py) 내 `fig_uniformity_machine_heatmap` 함수는 기획서의 컬러 규정을 이식하고 있으나, 실제 사용자 화면에서 분석가들의 조감 품질을 방해하는 **몇 가지 중대한 시인성적 한계와 비정형 레이아웃 오작동**이 잔존합니다.

| 분석 항목 | 현행 구현 (As-Is) | 개선 제안 (To-Be) | 기대 효과 |
| :--- | :--- | :--- | :--- |
| **셀 내 텍스트 시인성** | 글꼴 색상이 `colors.slate_900` 단일색으로 고정되어, 합격률이 높은 정상 구간(`slate_800` 배경)에서 **배경과 글자색이 겹쳐 백분율이 전혀 읽히지 않음**. | 합격률 및 배경색 명도(Lightness)에 따라 텍스트 컬러를 **동적 화이트/슬레이트로 교차 맵핑**하여 높은 대비 확보. | 높은 대비(Contrast)를 확보하여, 한눈에 백분율 데이터를 식별 가능. (WCAG 웹 표준 충족) |
| **컬러스케일 급격한 전이** | 80% 경계점에서 `slate_100`과 `orange_300` 간 보간 오작동으로 경계에 위치한 셀의 색상이 탁해지거나 위급도가 시각적으로 뭉개짐. | 컬러스케일 보간 간격을 정교하게 쪼개고, 오렌지 위험 구역 안에서도 0%에 가까울수록 진해지는 **오렌지 명도 스케일**을 적용. | 위험 설비 중에서도 더욱 위급한 장비(예: 40% vs 75%)를 색상 깊이만으로 명확히 구별함. |
| **Null 데이터 처리** | 생산 실적이 없는 기간(NaN)이 colorscale의 0% 또는 주변 값으로 오해되거나 빈 하얀색으로 퉁겨져 격자가 깨져 보임. | 데이터 미존재(NaN) 셀을 명확히 정의된 **아주 연한 슬레이트 그레이 패턴** 또는 투명화 처리하고, 호버 시 `No Production` 정보를 노출. | 가동 이력 없음과 저합격률 불량을 명확히 분리하여, 통계적 착시 현상 전면 배방. |
| **서브플롯 세로 불균형** | 설비 개수가 장비 유형별(조립, 가류, UF)로 현저히 다른데도, 3개 서브플롯 높이가 **1:1:1로 고정 분할되어 설비 수가 많은 영역이 짓눌림**. | 서브플롯 내의 실제 설비(Y축 범주) 수에 비례하여 **서브플롯별 세로 높이 비율(Row Heights Ratio)을 동적 배분**. | 설비가 많은 조립/가류 영역도 세로로 찌그러지지 않고 균일하고 쾌적한 셀 비율을 유지. |
| **호버 툴팁 가치** | 기본 텍스트 나열형 툴팁으로 구성되어 정보 밀도가 낮고 디자인이 밋밋함. | 좌우 대조 정렬된 **HTML/CSS 프리미엄 미니 테이블 레이아웃**을 이식하고, 수치 단위를 깔끔하게 포맷팅. | 마우스를 올리는 즉시 프리미엄 SaaS 솔루션을 사용하는 것과 같은 고급스러운 사용자 경험 제공. |

---

## 3. 세부 설계 및 개선 시나리오 (Detailed Engineering Steps)

### 3.1 동적 텍스트 고대비 폰트 쉐이딩 (High-Contrast Text Font Map)
각 셀의 배경색 밝기와 텍스트의 대비를 완벽히 통제하기 위해, Plotly 히트맵 셀에 글꼴 색상을 이중 배열 형태로 주입합니다.
* **구현 방식**: `z` 값(합격률) 행렬을 분석하여 `colors.white` (배경이 85% 이상 어두운 슬레이트일 때)와 `colors.slate_900` (배경이 85% 미만 밝은 오렌지 또는 연한 슬레이트일 때)의 색상 행렬 `text_colors`를 생성합니다.
* **코드 컨셉**:
  ```python
  text_colors = np.where(
      (z >= 85.0) & (~np.isnan(z)),  # 고합격률 어두운 슬레이트 배경 구역
      "white",                       # 고대비 밝은 텍스트
      colors.slate_900               # 저합격률 주황색/연한 회색 배경 구역
  )
  ```

### 3.2 오렌지 핫스팟 컬러스케일 고도화 (Orange Hotspot Colorscale)
경고와 정상을 나누는 80% 경계를 명확하게 구분하되, 보간 에러가 없도록 설계합니다.
* **컬러스케일 사양**:
  ```python
  premium_heatmap_colorscale = [
      [0.0, "#ea580c"],               # 0% : 아주 짙고 위급한 오렌지 (Orange 600)
      [0.79, "#fed7aa"],              # 79%: 연하고 경고성 있는 오렌지 틴트 (Orange 200)
      [0.80, colors.slate_100],       # 80%: 그레이스케일 시작 (정상 초입)
      [1.0, colors.slate_800],        # 100%: 짙고 안정적인 슬레이트 (정상 완결)
  ]
  ```

### 3.3 설비 규모 비례형 세로 폭 동적 제어 (Dynamic Row Height Ratio)
각 기기군별 설비 개수가 달라질 경우, 서브플롯이 자동으로 늘어나는 세로 비율을 확보합니다.
* **동적 높이 비율 산출**:
  ```python
  # 각 기기별 Y축 유니크 범주(설비 개수) 수집
  y_counts = [len(pivots[col].index) if col in pivots else 0 for col, _ in available]
  total_ys = sum(y_counts)
  # 설비 개수에 비례하도록 row_heights 가중치 할당
  row_ratios = [count / total_ys for count in y_counts]
  ```
  이 비율을 `make_subplots`의 `row_heights=row_ratios` 매개변수로 전달하고, 전체 피규어의 세로 높이(`height`)도 설비 전체 개수에 비례하여 유동적으로 늘려 쾌적한 고정 셀 크기(Cell Aspect Ratio)를 선사합니다.

### 3.4 프리미엄 도구팁 및 Null 인터랙션
```python
# Hover Template 내에 간결하고 통일감 있는 인라인 CSS 표 탑재
hovertemplate = (
    "<div style='font-family: sans-serif; padding: 4px; min-width: 140px;'>"
    "  <span style='font-size: 11px; color: " + colors.slate_400 + "; font-weight: bold;'>%{y}</span><br>"
    "  <div style='height: 1px; background-color: " + colors.slate_700 + "; margin: 4px 0;'></div>"
    "  <table style='width: 100%; border-collapse: collapse; font-size: 11px; color: " + colors.slate_100 + ";'>"
    "    <tr><td>기간</td><td style='text-align: right; font-weight: bold;'>%{x}</td></tr>"
    "    <tr><td>검사수</td><td style='text-align: right; font-weight: bold;'>%{customdata[0]:,d}</td></tr>"
    "    <tr><td>합격수</td><td style='text-align: right; font-weight: bold; color: #a7f3d0;'>%{customdata[1]:,d}</td></tr>"
    "    <tr style='color: " + colors.orange_300 + "; font-weight: bold;'>"
    "      <td>합격률</td><td style='text-align: right;'>%{z:.1f}%</td>"
    "    </tr>"
    "  </table>"
    "</div><extra></extra>"
)
```

---

## 4. 실행 및 배포 안전성 검증 방안 (Verification Gates)

* **정적 무결성 및 컴파일 진단**: 수정 작업 완료 후 `python -m py_compile app/pages/_20_analysis/data_analysis_plots.py`를 즉시 가동하여 린트 에러 및 문법 누수를 전면 차단합니다.
* **이모지 주입 스캔**: Streamlit 및 Plotly 차트 레이어 전수에 대해 일반 이모지가 주입되지 않았는지 `guardrail` 스캔을 거칩니다.

---

## 5. 피드백 및 승인 요청 (Requesting Action)

본 계획은 기존 UI/UX 가치 표준을 고스란히 지탱하면서 시각 분석적 가치와 완성도를 프로 레벨로 격상시키는 방안입니다. 

사용자님의 의견을 여쭙고자 합니다.
1. 본 **히트맵 시각화 고도화 계획(색상 보정, 글꼴 동적 대비, 서브플롯 높이 비례화, 프리미엄 툴팁)**에 전적으로 동의하십니까?
2. 동의하신다면, 즉시 기존 코드인 `data_analysis_plots.py`의 `fig_uniformity_machine_heatmap`를 안전하고 완성도 있게 구현한 뒤 자가 무결성 린트 검증까지 마쳐 전파해 드릴까요?
