# 시각화 일관성 분석 결과 및 아키텍처 리팩토링 계획서 (Visualization Consistency Plan)

본 문서는 사용자와의 정밀 인터뷰(/grill-me)를 통해 도출된 핵심 설계 의사결정을 기반으로, 프로젝트 내 Plotly와 ECharts 차트의 이질감을 극대화하는 요인을 진단하고 이를 중앙 집중식(SSOT) 아키텍처로 일원화하기 위한 구체적인 리팩토링 계획을 명시합니다.

---

## 1. 현재 구현 페이지의 4대 핵심 이질감 및 문제점 진단

현재 구현된 대시보드 페이지(예: app/pages/_10_dashboard/iqm_quality_trend_analysis_page.py 및 관련 plots 파일)를 분석한 결과, Plotly와 ECharts가 물리적/논리적으로 완벽히 조화되지 못하고 이질감을 유발하는 4대 요인은 다음과 같습니다.

### ① 디자인 배색(Color Palette)의 파편화 및 불일치
* **Plotly (TrendRankBarPlot)**: 개선 막대는 `colors.green_500`, 악화 막대는 `colors.red_500`과 같이 물리적(Primitive) 색상 토큰을 직접 지정하여 하드코딩하고 있습니다.
* **ECharts (draw_iqm_trend_rank_echart)**: 개선 막대는 시맨틱 토큰인 `colors.status_success` (물리 색상 `green_600`), 악화 막대는 `colors.status_error` (물리 색상 `red_600`)를 참조합니다.
* **문제점**: 동일한 의미를 나타내는 품질 개선/악화 막대가 화면에서 미세하게 다른 색감으로 렌더링되어 프리미엄 대시보드의 미학적 정합성을 저해하며, "물리 토큰의 직접 호출을 전면 차단하고 시맨틱 토큰을 간접 참조한다"는 L2-color-system 규칙을 위배합니다.

### ② 마우스 호버(Tooltip/Hover Label)의 상이한 스타일 (가장 큰 이질감)
* **Plotly**: Streamlit 기본 세컨더리 배경색(`var(--secondary-background-color)`)을 추종하도록 설정되어, 시스템 테마(라이트/다크) 변화에 유연하게 반응합니다.
* **ECharts**: 툴팁 배경색이 다크 그레이 고정값(`rgba(25, 25, 25, 0.95)`)으로 구성되어 있으며, 인라인 CSS로 구현된 텍스트 크기(12px) 및 선명한 상태 테두리선(Red/Green)이 고정되어 있습니다.
* **문제점**: 라이트 모드 가동 시 Plotly 툴팁은 밝은 톤으로 자동 변환되는 반면, ECharts 툴팁만 다크 모드 고정 형태로 렌더링되어 극심한 비주얼 부조화가 발생합니다.

### ③ 타이포그래피(Typography) 및 폰트 스케일 불일치
* **Plotly**: 제목 글꼴 크기가 `16px`로 렌더링되고, `display` 폰트 패밀리를 사용합니다.
* **ECharts**: 제목 글꼴 크기가 `14px`로 구성되고, `primary` 폰트 패밀리로 일률 적용되어 있습니다.
* **문제점**: 나란히 서 있는 두 개의 차트가 제목 두께, 서체 비중, 스케일 편차를 보여 레이아웃의 균형이 깨집니다.

### ④ 그리드 눈금선(Grid Lines) 및 수치 라벨 표현의 편차
* **Plotly**: 축 그리드가 은은한 회색 실선(`rgba(128, 128, 128, 0.15)`)으로 표현되며, 수치 레이블은 `textposition="outside"`로 표시됩니다.
* **ECharts**: X축 분할선이 점선(`dashed`, `rgba(128, 128, 128, 0.15)`) 형태로 표현됩니다.
* **문제점**: 그리드선 형태(실선 vs 점선)의 불일치로 배경 가시성의 연속성이 떨어집니다.

---

## 2. 합의된 시각화 설계 표준 (Design SSOT)

사용자와의 인터뷰 및 승인 과정을 거쳐 확립된 통합 시각화 설계 표준은 다음과 같습니다.

| 디자인 영역 | Plotly 표준화 규칙 | ECharts 표준화 규칙 |
| :--- | :--- | :--- |
| **디자인 테마 대응** | Streamlit CSS 변수를 완벽히 추종하여 라이트/다크 모드에 실시간 유연 반응 | Streamlit CSS 변수를 주입하여 라이트/다크 모드와 완벽히 다이내믹 동기화 |
| **핵심 배색 토큰** | `colors.status_success` / `colors.status_error` 시맨틱 토큰 전수 매핑 | `colors.status_success` / `colors.status_error` 시맨틱 토큰 전수 매핑 |
| **마우스 툴팁** | 툴팁 배경: `var(--secondary-background-color)` <br> 글자색: `var(--text-color)` | 툴팁 배경: `var(--secondary-background-color)` <br> 글자색: `var(--text-color)` (HTML 인라인 스타일 CSS에 주입) |
| **타이포그래피** | 제목: `16px` (get_font_family("display")) <br> 본문: `11~12px` (get_font_family("primary")) | 제목: `16px` (get_font_family("display")) <br> 본문: `11~12px` (get_font_family("primary")) |
| **그리드 및 축선** | 은은한 점선 스타일 (`dashed`, `rgba(128, 128, 128, 0.15)`) | 은은한 점선 스타일 (`dashed`, `rgba(128, 128, 128, 0.15)`) |
| **수치 값 레이블** | 항상 막대 끝 바깥쪽 (`outside` 지능형 정렬) | 항상 막대 끝 바깥쪽 (`position` 및 `label_pos` 활용 지능형 정렬) |

---

## 3. 중앙 집중형 스타일링 헬퍼 (SSOT) 설계안

중복 코드를 완전히 은닉하고 단일 진실 공급원을 구성하기 위해 `app/core/plot/` 또는 `app/core/design_system/plot/` 계층에 중앙 집중식 스타일 주입 헬퍼 함수를 신설 및 정비합니다.

### ① Plotly 통합 스타일 헬퍼 (`apply_custom_plotly_style`)
* **역할**: 기존 개별 plots 파일에 파편화되어 정의되어 있던 `apply_custom_chart_style`를 제거하고, 중앙의 단일 공통 함수로 관리합니다.
* **위치**: `app/core/plot/components.py` 혹은 별도 설계 모듈

```python
# app/core/plot/helpers.py (예시 설계)
def apply_custom_plotly_style(fig: go.Figure) -> go.Figure:
    if fig is None:
        return None
    
    # CSS 변수 바인딩 및 폰트 규격 통합 적용
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family=get_font_family("primary"), color="var(--text-color)", size=12),
        title=dict(
            font=dict(family=get_font_family("display"), color="var(--text-color)", size=16),
            x=0.01,
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.15)",
            # Plotly dashed grid 에뮬레이션
            gridwidth=1,
            griddash="dash", 
            tickfont=dict(family=get_font_family("primary"), color="var(--text-color)", size=10)
        ),
        yaxis=dict(
            tickfont=dict(family=get_font_family("primary"), color="var(--text-color)", size=10)
        ),
        hoverlabel=dict(
            bgcolor="var(--secondary-background-color)",
            bordercolor="rgba(128, 128, 128, 0.2)",
            font=dict(family=get_font_family("primary"), color="var(--text-color)", size=12)
        )
    )
    return fig
```

### ② ECharts 통합 스타일 헬퍼 (`apply_custom_echarts_style`)
* **역할**: ECharts의 옵션 딕셔너리를 입력받아, 테마CSS 변수와 타이포그래피 표준, 툴팁 테마를 일괄 바인딩하여 완성된 딕셔너리를 반환합니다.

```python
# app/core/plot/helpers.py (예시 설계)
def apply_custom_echarts_style(options: dict, is_improvement: bool = True) -> dict:
    if not options:
        return {}
    
    # 1. 공통 타이틀 스타일 바인딩
    if "title" in options:
        options["title"]["textStyle"] = {
            "fontSize": 16,
            "fontWeight": "bold",
            "color": "var(--text-color)",
            "fontFamily": get_font_family("display")
        }
        
    # 2. 공통 그리드 배경 및 축선 점선화
    if "xAxis" in options:
        options["xAxis"]["splitLine"] = {
            "show": True,
            "lineStyle": {
                "color": "rgba(128, 128, 128, 0.15)",
                "type": "dashed"
            }
        }
        options["xAxis"]["axisLabel"] = {
            "color": "var(--text-color)",
            "fontFamily": get_font_family("primary"),
            "fontSize": 10
        }
        
    if "yAxis" in options:
        options["yAxis"]["axisLabel"] = {
            "color": "var(--text-color)",
            "fontFamily": get_font_family("primary"),
            "fontSize": 10
        }
        options["yAxis"]["axisLine"] = {
            "lineStyle": {
                "color": "rgba(128, 128, 128, 0.15)"
            }
        }

    # 3. 툴팁에 테마 CSS 변수 주입 및 폰트 통일
    # (ECharts Formatter에서 var(--text-color) 및 var(--secondary-background-color) 연동 보증)
    if "tooltip" in options:
        options["tooltip"]["backgroundColor"] = "var(--secondary-background-color)"
        options["tooltip"]["borderColor"] = "rgba(128, 128, 128, 0.2)"
        options["tooltip"]["borderWidth"] = 1
        options["tooltip"]["textStyle"] = {
            "color": "var(--text-color)",
            "fontFamily": get_font_family("primary"),
            "fontSize": 12
        }
        
    return options
```

---

## 4. 리팩토링 및 아키텍처 개편 로드맵

사용자의 승인을 얻는 즉시 아래 단계에 맞추어 작업을 순차적으로 실행하겠습니다.

1. **디자인 토큰 점검 및 중앙 스타일 헬퍼 모듈 구축**:
   * `app/core/plot/` 디렉터리에 `helpers.py`를 신설하여 `apply_custom_plotly_style` 및 `apply_custom_echarts_style`를 구현합니다.
2. **`TrendRankBarPlot` (Plotly) 컴포넌트 리팩토링**:
   * `app/core/plot/components.py` 내의 `TrendRankBarPlot`이 사용하는 마커 배색을 시맨틱 토큰(`status_success`, `status_error`)으로 변경합니다.
   * 복귀 직전에 `apply_custom_plotly_style`을 경유하도록 통일합니다.
3. **ECharts 드로잉 함수 리팩토링**:
   * `app/pages/_10_dashboard/iqm_quality_trend_analysis_plots.py` 내의 `draw_iqm_trend_rank_echart`에 존재하는 인라인 하드코딩 스타일을 걷어냅니다.
   * `apply_custom_echarts_style` 헬퍼를 리턴하기 전에 반드시 적용하도록 개편합니다.
4. **중복 정의된 `apply_custom_chart_style` 전수 제거 및 일원화**:
   * `iqm_plus_main_plots.py`, `oe_quality_issue_dashboard_plots.py` 등의 파일에서 개별 선언된 스타일링 중복 헬퍼를 제거하고 디자인 시스템 중앙의 `apply_custom_plotly_style`을 임포트하여 위임하도록 일괄 치환합니다.
5. **무결성 정적 린트 및 수동 하네스 검증**:
   * UI가 정상 기동하는지 `quality-assurance` 및 정적 분석 린트를 돌려 결함 유무를 완벽히 증명합니다.

---

## 5. 실행 승인 및 다음 작업 선택

계획에 동의하시면 아래의 진행 결정을 선택해 주십시오. 승인해 주시면 즉시 안전한 샌드박스에서 계획된 리팩토링 작업을 시작합니다.
