# OE Quality Issue Dashboard Submenu Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor `oe_quality_issue_dashboard_page.py` by extracting its 4 submenus (tabs) and 3 modal dialogs into a modular subfolder structure `app/pages/_10_dashboard/oe_tabs/`.

**Architecture:** We will create a new package `app.pages._10_dashboard.oe_tabs` containing individual modules for each tab: `global_tab.py` (which also hosts the global dialog modals), `plant_tab.py` (which hosts the plant tab and its local `COMMON_REMAIN_COLUMNS`), `oeqg_tab.py`, and `rawdata_tab.py`. The main page `oe_quality_issue_dashboard_page.py` will import these modular renderers, thereby reducing its code footprint, increasing readability, and avoiding namespace bloat.

**Tech Stack:** Python 3.10+, Streamlit, Pandas, Plotly.

## Global Constraints
- **Safety Lock:** Only modify the specified files. All code changes should maintain functional equivalence.
- **No Emojis:** Do not introduce any raw emojis in UI strings or comments; only Streamlit's Material icon strings are allowed.
- **Relative Pathing:** Ensure VS Code-friendly relative markdown pathing in all updated files.
- **TDD / Validation:** Every task must be verified with automated test executions.

---

## File Structure & Map

We will create the following files inside `app/pages/_10_dashboard/oe_tabs/`:
1. `__init__.py` - Package exposure of tab rendering functions.
2. `global_tab.py` - Modular renderer for the GLOBAL tab and related modals.
3. `plant_tab.py` - Modular renderer for the PLANT tab and its column definitions.
4. `oeqg_tab.py` - Modular renderer for the OEQG tab.
5. `rawdata_tab.py` - Modular renderer for the RAWDATA tab.

We will modify:
1. `app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py` - Main page router.

We will create a new unit test suite:
1. `tests/test_oe_quality_issue_dashboard_page.py` - Verification suite for tabs and imports.

---

## Tasks

### Task 1: Create the Modular Tabs Directory and Scaffolding

**Files:**
- Create: `app/pages/_10_dashboard/oe_tabs/__init__.py`

**Interfaces:**
- Consumes: None
- Produces: Exposed functions: `render_global_tab`, `render_plant_tab`, `render_oeqg_tab`, `render_rawdata_tab`.

- [ ] **Step 1: Write scaffolding package init**

Write the `app/pages/_10_dashboard/oe_tabs/__init__.py` file:

```python
"""
OE Quality Issue Dashboard Tabs Package
- 최종 수정일: 2026-07-20
"""

from app.pages._10_dashboard.oe_tabs.global_tab import render_global_tab
from app.pages._10_dashboard.oe_tabs.plant_tab import render_plant_tab
from app.pages._10_dashboard.oe_tabs.oeqg_tab import render_oeqg_tab
from app.pages._10_dashboard.oe_tabs.rawdata_tab import render_rawdata_tab

__all__ = [
    "render_global_tab",
    "render_plant_tab",
    "render_oeqg_tab",
    "render_rawdata_tab",
]
```

- [ ] **Step 2: Commit init file**

```bash
git add app/pages/_10_dashboard/oe_tabs/__init__.py
git commit -m "refactor: create oe_tabs package scaffolding"
```

---

### Task 2: Implement the Global Tab Module

**Files:**
- Create: `app/pages/_10_dashboard/oe_tabs/global_tab.py`

**Interfaces:**
- Consumes: `app.pages._10_dashboard.oe_quality_issue_dashboard_plots`
- Produces: `render_global_tab` function.

- [ ] **Step 1: Create the `global_tab.py` file with dialogs and render function**

Write the complete code for `app/pages/_10_dashboard/oe_tabs/global_tab.py` matching exactly the implementation currently in `oe_quality_issue_dashboard_page.py` lines 400-668:

```python
"""
GLOBAL 탭 화면 및 모달 대화상자 렌더러
- 최종 수정일: 2026-07-20
"""

import pandas as pd
import streamlit as st

from app.core.design_system.tokens import colors, get_font_family
from app.core.design_system.streamlit_widgets import section_header
from app.pages._10_dashboard import oe_quality_issue_dashboard_plots as viz


@st.dialog("SKU Ratio by Plant", width="large")
def show_sku_ratio_modal(df_plant_data: pd.DataFrame) -> None:
    """
    공장별 SKU, 공급량 및 품질이슈 비율 시각화 도넛 차트를 모달 창에 표출합니다.
    """
    st.markdown(
        f"""
        <p style="font-family: {get_font_family('primary')}; font-size: 0.875rem; color: {colors.app_text_muted}; margin-bottom: 1.5rem;" translate="no">
            Comparative ratio distribution of SKU, supply volume, and quality issue count by plant.
        </p>
        """,
        unsafe_allow_html=True,
    )
    cols_ratios = st.columns(3)
    with cols_ratios[0]:
        st.plotly_chart(viz.draw_sku_ratio_by_plant_pieplot(df_plant_data), use_container_width=True)
    with cols_ratios[1]:
        st.plotly_chart(viz.draw_supply_quantity_ratio_by_plant_pieplot(df_plant_data), use_container_width=True)
    with cols_ratios[2]:
        st.plotly_chart(viz.draw_issue_count_ratio_by_plant_pieplot(df_plant_data), use_container_width=True)


@st.dialog("Issue Category Aggregated Data", width="large")
def show_issue_category_modal(df_issue_type_data: pd.DataFrame) -> None:
    """
    상세 품질이슈 유형 분류 집계 로우데이터 테이블을 모달 창에 표출합니다.
    """
    st.markdown(
        f"""
        <p style="font-family: {get_font_family('primary')}; font-size: 0.875rem; color: {colors.app_text_muted}; margin-bottom: 1.5rem;" translate="no">
            Raw aggregated table of quality issue counts by plant, category, and sub-category.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df_issue_type_data, use_container_width=True, hide_index=True)


@st.dialog("Mean Time To Closure (MTTC) Guidelines", width="large")
def show_mttc_guidelines_modal() -> None:
    """
    MTTC (Mean Time To Closure) 지표의 산출 산식 및 업무 단계별 가이드라인을 모달 창에 표출합니다.
    """
    mttc_help_lines = [
        "MTTC (Mean Time To Closure) represents the average number of business days it takes to close a quality issue.",
        "This metric is calculated by summing up several work phases, including:",
        "• Occurrence to Registration",
        "• Registration to Return (only if the issue is returned)",
        "• Return or Registration to Countermeasure",
        "• Countermeasure to 8D Completion",
        "The system uses business days (excluding weekends) based on actual dates provided in the report.",
        "If certain dates (e.g., completion) are missing, the calculation assumes today's date as the endpoint. This ensures ongoing issues are also reflected in the MTTC calculation.",
        "A lower MTTC indicates faster resolution and better responsiveness to quality issues."
    ]
    html_lines = "".join([f"<p style='margin-bottom: 0.75rem;'>{line}</p>" for line in mttc_help_lines])
    st.markdown(
        f"""
        <div style="font-family: {get_font_family('primary')}; font-size: 0.875rem; line-height: 1.6; color: {colors.app_text_secondary};">
            {html_lines}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_global_tab(
    df_yearly_trend: pd.DataFrame,
    df_monthly_trend: pd.DataFrame,
    df_oem_data: pd.DataFrame,
    df_market_data: pd.DataFrame,
    df_plant_data: pd.DataFrame,
    df_issue_type_data: pd.DataFrame,
    df_mttc_trend: pd.DataFrame,
    df_mttc_plant: pd.DataFrame,
    target_year: int,
) -> None:
    """
    글로벌 품질 KPI 추이, 제조공장별 품질 지표, 품질 이슈 분류 트리맵 등 글로벌 관점의 정보를 렌더링합니다.
    """
    section_header(
        title="Global OE Quality Index Trend",
        subtitle="Global OEQI and quality issue trends (OEQI and supply data are valid from 2023).",
        icon_name="trending_up",
        extra_info_html=f"""
        <div style="font-size: 0.75rem; color: {colors.app_text_muted}; background: {colors.app_background}; border: 1px solid {colors.app_border}; border-radius: 0.25rem; padding: 0.25rem 0.75rem;">
            Trend Period: <strong style="color: {colors.app_text_primary}; font-weight: 600;">Recent 3 Years</strong>
        </div>
        """,
    )
    
    # 1) OEQI 및 이슈 카운트 연간/월간 바인딩 및 렌더링
    cols_row1 = st.columns([25, 45, 30])
    cols_row1[0].plotly_chart(
        viz.draw_three_years_oeqi_barplot(df_yearly_trend),
        use_container_width=True,
    )
    cols_row1[1].plotly_chart(
        viz.draw_monthly_oeqi_trend_lineplot(df_monthly_trend, selected_year=target_year),
        use_container_width=True,
    )
    cols_row1[2].plotly_chart(viz.draw_issue_count_by_oem_pieplot(df_oem_data))

    cols_row2 = st.columns([25, 45, 30])
    cols_row2[0].plotly_chart(
        viz.draw_three_years_issue_count_barplot(df_yearly_trend),
        use_container_width=True,
    )
    cols_row2[1].plotly_chart(
        viz.draw_monthly_issue_count_barplot(df_monthly_trend, selected_year=target_year),
        use_container_width=True,
    )
    cols_row2[2].plotly_chart(viz.draw_issue_count_by_market_pieplot(df_market_data))

    # 2) 제조 공장별 품질 매트릭스 렌더링 (타이틀 우측에 소형 모달 트리거 버튼 배치)
    cols_header_plant = st.columns([8, 2], vertical_alignment="bottom")
    with cols_header_plant[0]:
        section_header(
            title="Manufacturing Plant Quality Metrics",
            subtitle="Manufacturing plant-level comparisons for SKU, supply volume, issues, and OEQI.",
            icon_name="factory",
            top_margin="2rem",
            bottom_margin="0.5rem",
        )
    with cols_header_plant[1]:
        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button(":material/donut_large: View SKU & Volume Ratios", key="btn_sku_ratio_modal", use_container_width=True):
            show_sku_ratio_modal(df_plant_data)

    try:
        cols_plants = st.columns(4)
        cols_plants[0].plotly_chart(viz.draw_sku_by_plant_barhplot(df_plant_data), use_container_width=True)
        cols_plants[1].plotly_chart(
            viz.draw_supply_quantity_by_plant_barhplot(df_plant_data),
            use_container_width=True,
        )
        cols_plants[2].plotly_chart(viz.draw_issue_count_by_plant_barhplot(df_plant_data), use_container_width=True)
        cols_plants[3].plotly_chart(viz.draw_oeqi_by_plant_barhplot(df_plant_data), use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering plant metrics: {str(e)}")

    # 3) 이슈 카테고리 트리맵 및 워스트 분류 렌더링 (타이틀 우측에 모달 트리거 버튼 배치)
    cols_header_issue = st.columns([8, 2], vertical_alignment="bottom")
    with cols_header_issue[0]:
        section_header(
            title="Quality Issue Categorization & Analysis",
            subtitle="Quality issue distribution tree-map and worst 5 categories by manufacturing plant.",
            icon_name="monitoring",
            top_margin="2rem",
            bottom_margin="0.5rem",
        )
    with cols_header_issue[1]:
        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button(":material/table_chart: View Aggregated Table", key="btn_issue_category_modal", use_container_width=True):
            show_issue_category_modal(df_issue_type_data)

    st.plotly_chart(viz.draw_issue_type_tree_map(df_issue_type_data), use_container_width=True)
    st.plotly_chart(viz.draw_worst_by_plant_barplot(df_issue_type_data), use_container_width=True)

    # 4) MTTC 인덱스 렌더링 (타이틀 우측에 모달 가이드 버튼 배치)
    cols_header_mttc = st.columns([8, 2], vertical_alignment="bottom")
    with cols_header_mttc[0]:
        section_header(
            title="Mean Time To Closure (MTTC) Index",
            subtitle="Analysis of elapsed business days from issue occurrence to final 8D closure (MTTC).",
            icon_name="schedule",
            top_margin="2rem",
            bottom_margin="0.5rem",
        )
    with cols_header_mttc[1]:
        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button(":material/help: View MTTC Guidelines", key="btn_mttc_guidelines_modal", use_container_width=True):
            show_mttc_guidelines_modal()

    cols_mttc = st.columns(3)
    cols_mttc[0].plotly_chart(
        viz.draw_three_years_mttc_barplot(df_mttc_trend),
        use_container_width=True,
        key="MTTC_BAR",
    )
    cols_mttc[1].plotly_chart(
        viz.draw_mttc_global_indicator(df_mttc_trend, selected_year=target_year),
        use_container_width=True,
    )
    cols_mttc[2].plotly_chart(
        viz.draw_mttc_by_plant_barhplot(df_mttc_plant),
        use_container_width=True,
    )

    # MTTC 상세 단계별 인디케이터 게이지
    cols_mttc_details = st.columns(4)
    cols_mttc_details[0].plotly_chart(
        viz.draw_mttc_indicator(
            df_mttc_trend,
            target=2,
            col_name="REG_PRD",
            title="Registration",
            selected_year=target_year,
        ),
        use_container_width=True,
    )
    cols_mttc_details[1].plotly_chart(
        viz.draw_mttc_indicator(
            df_mttc_trend,
            target=7,
            col_name="RTN_PRD",
            title="Return",
            selected_year=target_year,
        ),
        use_container_width=True,
    )
    cols_mttc_details[2].plotly_chart(
        viz.draw_mttc_indicator(
            df_mttc_trend,
            target=5,
            col_name="CTM_PRD",
            title="Countermeasure",
            selected_year=target_year,
        ),
        use_container_width=True,
    )
    cols_mttc_details[3].plotly_chart(
        viz.draw_mttc_indicator(
            df_mttc_trend,
            target=2,
            col_name="COMP_PRD",
            title="8D Report",
            selected_year=target_year,
        ),
        use_container_width=True,
    )
```

- [ ] **Step 2: Commit `global_tab.py`**

```bash
git add app/pages/_10_dashboard/oe_tabs/global_tab.py
git commit -m "feat: add modular global_tab.py with modals and render_global_tab"
```

---

### Task 3: Implement the Plant Tab Module

**Files:**
- Create: `app/pages/_10_dashboard/oe_tabs/plant_tab.py`

**Interfaces:**
- Consumes: `app.service.cqms_df`, `app.pages._10_dashboard.oe_quality_issue_dashboard_plots`
- Produces: `render_plant_tab` function and its local `COMMON_REMAIN_COLUMNS`.

- [ ] **Step 1: Create the `plant_tab.py` file**

Write the complete code for `app/pages/_10_dashboard/oe_tabs/plant_tab.py` matching exactly the implementation currently in `oe_quality_issue_dashboard_page.py` lines 189-204 and lines 669-848:

```python
"""
PLANT 탭 화면 렌더러
- 최종 수정일: 2026-07-20
"""

import pandas as pd
import streamlit as st

from app.core.design_system.tokens import colors
from app.core.design_system.streamlit_widgets import section_header, vertical_metric
from app.core.utils.numbers import format_number
from app.core.design_system.column_config import get_dynamic_column_configs
from app.pages._10_dashboard import oe_quality_issue_dashboard_plots as viz
from app.service import cqms_df

# 데이터 테이블 표시를 위한 공통 컬럼 설정 정의
COMMON_REMAIN_COLUMNS = {
    "Basic Info": ["OEQ_GROUP", "PLANT", "OEM", "VEH", "PJT"],
    "Dates": ["OCC_DATE", "REG_DATE", "RTN_DATE", "CTM_DATE", "COMP_DATE"],
    "Status": ["STATUS"],
    "Classification": [
        "LOCATION",
        "MARKET",
        "M_CODE",
        "TYPE_NAME",
        "CAT_NAME",
        "SUB_CAT_NAME",
    ],
    "Periods": ["REG_PRD", "RTN_PRD", "CTM_PRD", "COMP_PRD", "MTTC"],
    "Others": ["URL"],
}


def render_plant_tab(
    df_oeapp_pivot: pd.DataFrame,
    df_plant_agg: pd.DataFrame,
    df_raw: pd.DataFrame,
    df_mttc_plant: pd.DataFrame,
    df_plant_month_trend: pd.DataFrame,
    target_plant: str,
    target_year: int,
) -> None:
    """
    선택된 개별 공장의 프로젝트 수, 공급량, 품질이슈, 주요 지표 추이 및 품질 이슈 리스트를 렌더링합니다.
    """
    # 1) 서비스 레이어를 기동하여 대상 공장용 요약 지표 수집
    (
        df_metric_prjt,
        df_metric_supp,
        df_metric_qi,
        df_metric_oeqi,
        df_metric_mttc,
    ) = cqms_df.present_plant_metrics(
        df_oeapp_pivot_table=df_oeapp_pivot,
        df_global_thisyear_agg_by_plant=df_plant_agg,
        df_rawdata=df_raw,
        df_mttc_this_year_by_plant=df_mttc_plant,
        selected_plant=target_plant,
        selected_year=target_year,
    )

    # 타겟 공장 품질 분석 중제목 패널 렌더링 (중복 정보 제거)
    section_header(
        title="Plant Quality Summary",
        subtitle="Detailed quality metrics, project status, and trend analysis for the selected manufacturing plant.",
        icon_name="factory",
        top_margin="2rem",
        bottom_margin="1.5rem",
    )

    cols_metrics = st.columns(4, gap="medium")

    # 2) 개별 메트릭 정보 패널 렌더링
    with cols_metrics[0]:
        if df_metric_prjt.empty:
            mass_prod_count = 0
            dev_count = 0
        else:
            try:
                mass_prod_count = df_metric_prjt["Supplying"].values[0].astype(int)
                dev_count = df_metric_prjt["Developing"].values[0].astype(int)
            except Exception:
                mass_prod_count = 0
                dev_count = 0
        vertical_metric(
            title="Active Projects",
            value=f"{mass_prod_count} / {dev_count}",
            description="Project status (mass prod / dev)",
            status="neutral",
            gradient=False,
        )

    with cols_metrics[1]:
        supp_qty = df_metric_supp["SUPP_QTY"].values[0] if not df_metric_supp.empty else 0
        vertical_metric(
            title="OE Supplies",
            value=format_number(num=supp_qty),
            description="Cumulative supply volume this year",
            status="neutral",
            gradient=False,
        )

    with cols_metrics[2]:
        if not df_metric_qi.empty:
            comp_cnt = df_metric_qi["Complete"].values[0] if "Complete" in df_metric_qi.columns else 0
            on_going_cnt = df_metric_qi["On-going"].values[0] if "On-going" in df_metric_qi.columns else 0
        else:
            comp_cnt = 0
            on_going_cnt = 0
        vertical_metric(
            title="Quality Issues",
            value=f"{on_going_cnt} / {comp_cnt}",
            description="On-going / Complete",
            status="positive" if on_going_cnt == 0 else "warning",
            gradient=False,
        )

    with cols_metrics[3]:
        oeqi_val = df_metric_oeqi["QI_INDEX"].values[0] if not df_metric_oeqi.empty and "QI_INDEX" in df_metric_oeqi.columns else 0
        mttc_val = df_metric_mttc["MTTC"].values[0] if not df_metric_mttc.empty and "MTTC" in df_metric_mttc.columns else 0
        vertical_metric(
            title="Quality Index",
            value=f"{oeqi_val:.2f} / {mttc_val:.1f}",
            description="OEQI / MTTC(days)",
            status="positive" if oeqi_val >= 90 else "neutral",
            gradient=False,
        )

    section_header(
        title="Comparison & Monthly Trend Analysis",
        subtitle="Monthly trends and performance benchmarking against peer manufacturing plants.",
        icon_name="monitoring",
        top_margin="2rem",
    )

    # 3) 월별 품질 및 이슈 수 추이 분석 차트
    df_selected_plant_monthly_trend = (
        df_plant_month_trend.loc[lambda df: df["PLANT"] == target_plant]
        .assign(YYYY=lambda x: x["YYYYMM"].str[:4].astype("str"))
        .assign(MM=lambda x: x["YYYYMM"].str[4:].astype("str"))
        .loc[lambda df: df["YYYY"] == str(target_year)]
    )
    
    cols_charts = st.columns(2)
    with cols_charts[0]:
        if not df_plant_agg.empty:
            st.plotly_chart(
                viz.draw_plant_view_oeqi_highlight(df_plant_agg, target_plant),
                use_container_width=True,
            )
            st.plotly_chart(
                viz.draw_plant_view_issue_count_highlight(df_plant_agg, target_plant),
                use_container_width=True,
            )
        else:
            st.info("No plant comparison data available")

    with cols_charts[1]:
        if not df_selected_plant_monthly_trend.empty:
            st.plotly_chart(viz.draw_plant_view_oeqi_index_trend(df_selected_plant_monthly_trend))
            st.plotly_chart(viz.draw_plant_view_issue_count_index_trend(df_selected_plant_monthly_trend))
        else:
            st.info("No trend data available for selected plant")

    # 4) 상세 품질이슈 리스트 테이블 표출
    section_header(
        title="Detailed Quality Issue Records",
        subtitle="Detailed listing of individual quality issues for the selected plant and year.",
        icon_name="sticky_note_2",
        top_margin="2rem",
    )
    
    remain_col = [col for cols_group in COMMON_REMAIN_COLUMNS.values() for col in cols_group]
    # PLANT 탭에서는 이미 선택된 공장의 정보만을 보므로, 테이블 상에서 OEQ_GROUP과 PLANT 컬럼은 중복이므로 제외하여 가독성 극대화
    if "OEQ_GROUP" in remain_col:
        remain_col.remove("OEQ_GROUP")
    if "PLANT" in remain_col:
        remain_col.remove("PLANT")

    df_selected_plant_qi_list = df_raw.loc[
        lambda df_temp: df_temp["PLANT"] == target_plant
    ].loc[lambda df_temp: df_temp["REG_DATE"].dt.year == target_year]
    
    df_selected_plant_qi_list = df_selected_plant_qi_list.reindex(columns=remain_col)
    df_selected_plant_qi_list = df_selected_plant_qi_list.sort_values(by="REG_DATE", ascending=False)

    # 동적 컬럼 바인더 활용 (한글 AS 하드코딩 완전 방지 및 툴팁/포맷 연동)
    plant_col_config = get_dynamic_column_configs("cqms_quality_main", list(df_selected_plant_qi_list.columns))
    st.dataframe(
        df_selected_plant_qi_list,
        use_container_width=True,
        column_config=plant_col_config,
        hide_index=True,
    )
```

- [ ] **Step 2: Commit `plant_tab.py`**

```bash
git add app/pages/_10_dashboard/oe_tabs/plant_tab.py
git commit -m "feat: add modular plant_tab.py"
```

---

### Task 4: Implement the OEQG Tab Module

**Files:**
- Create: `app/pages/_10_dashboard/oe_tabs/oeqg_tab.py`

**Interfaces:**
- Consumes: `app.pages._10_dashboard.oe_quality_issue_dashboard_plots`
- Produces: `render_oeqg_tab` function.

- [ ] **Step 1: Create the `oeqg_tab.py` file**

Write the complete code for `app/pages/_10_dashboard/oe_tabs/oeqg_tab.py` matching exactly the implementation currently in `oe_quality_issue_dashboard_page.py` lines 850-955:

```python
"""
OEQG 탭 화면 렌더러
- 최종 수정일: 2026-07-20
"""

import pandas as pd
import streamlit as st

from app.core.design_system.tokens import colors
from app.core.design_system.streamlit_widgets import section_header
from app.pages._10_dashboard import oe_quality_issue_dashboard_plots as viz


def render_oeqg_tab(
    df_oeqg_trend: pd.DataFrame,
    df_raw: pd.DataFrame,
    df_mttc_trend: pd.DataFrame,
    df_mttc_oeqg_data: pd.DataFrame,
    target_year: int,
) -> None:
    """
    각 권역(OEQG)별 월간 품질 이슈 트렌드, 이슈 유형 도넛 차트 및 MTTC 지표를 렌더링합니다.
    """
    # 0) 권역별 통합 분석 중제목 패널 렌더링
    section_header(
        title="Regional OE Quality Group (OEQG) Analysis",
        subtitle="Monthly trends, category distribution, and detailed MTTC performance by region.",
        icon_name="public",
        extra_info_html=f"""
        <div style="font-size: 0.75rem; color: {colors.app_text_muted}; background: {colors.app_background}; border: 1px solid {colors.app_border}; border-radius: 0.25rem; padding: 0.35rem 0.75rem;">
            Target Groups: <strong style="color: {colors.app_text_primary}; font-weight: 600;">Global, China, Europe, NA</strong>
        </div>
        """,
    )

    # 1) 월간 트렌드 서브플롯 통합 차트
    section_header(
        title="Monthly OEQI & Supply Trends by Region",
        subtitle="Monthly OEQI and cumulative supply volume benchmarking by region.",
        icon_name="trending_up",
        top_margin="2rem",
    )
    st.plotly_chart(
        viz.draw_goeq_view_monthly_trend_subplots(df_oeqg_trend),
        use_container_width=True,
    )

    # 2) 권역별 품질 이슈 분류 도넛 차트
    section_header(
        title="Quality Issue Classification by Region",
        subtitle="Quality issue category structure and worst category distribution by region.",
        icon_name="donut_large",
        top_margin="2rem",
    )
    st.plotly_chart(
        viz.draw_oeqg_issue_type_donuts(df_raw, target_year),
        use_container_width=True,
    )

    # 3) MTTC 권역별 비교
    section_header(
        title="Mean Time To Closure (MTTC) Comparison",
        subtitle="Comparison of average business days to close issues (MTTC) by region.",
        icon_name="schedule",
        top_margin="2rem",
    )
    cols_oeqg_mttc = st.columns([2, 7], gap="large", vertical_alignment="center")
    cols_oeqg_mttc[0].plotly_chart(
        viz.draw_three_years_mttc_barplot(df_mttc_trend),
        use_container_width=True,
        key="MTTC_BAR_2",
    )
    cols_oeqg_mttc[1].plotly_chart(
        viz.draw_goeq_view_mttc_compare(df_mttc_oeqg_data),
        use_container_width=True,
    )

    # 4) MTTC 단계별 상세 비교 차트 배치
    section_header(
        title="MTTC Resolution Phase Breakdown",
        subtitle="Phase-by-phase breakdown from occurrence to registration, return, action, and 8D closure.",
        icon_name="account_tree",
        top_margin="2rem",
    )

    mttc_sub_charts = viz.draw_mttc_phase_breakdown_charts(
        df_mttc_oeqg_data,
        selected_year=target_year
    )

    row1_cols = st.columns(2, gap="large")
    row2_cols = st.columns(2, gap="large")

    mttc_layout_mapping = {
        "REG_PRD": row1_cols[0],
        "RTN_PRD": row1_cols[1],
        "CTM_PRD": row2_cols[0],
        "COMP_PRD": row2_cols[1],
    }

    for metric, col in mttc_layout_mapping.items():
        if metric in mttc_sub_charts:
            col.plotly_chart(mttc_sub_charts[metric], use_container_width=True)
```

- [ ] **Step 2: Commit `oeqg_tab.py`**

```bash
git add app/pages/_10_dashboard/oe_tabs/oeqg_tab.py
git commit -m "feat: add modular oeqg_tab.py"
```

---

### Task 5: Implement the Raw Data Tab Module

**Files:**
- Create: `app/pages/_10_dashboard/oe_tabs/rawdata_tab.py`

**Interfaces:**
- Consumes: None
- Produces: `render_rawdata_tab` function.

- [ ] **Step 1: Create the `rawdata_tab.py` file**

Write the complete code for `app/pages/_10_dashboard/oe_tabs/rawdata_tab.py` matching exactly the implementation currently in `oe_quality_issue_dashboard_page.py` lines 956-1015:

```python
"""
RAWDATA 탭 화면 렌더러
- 최종 수정일: 2026-07-20
"""

import pandas as pd
import streamlit as st

from app.core.design_system.tokens import colors
from app.core.design_system.streamlit_widgets import section_header
from app.core.design_system.column_config import get_dynamic_column_configs


def render_rawdata_tab(
    df_raw: pd.DataFrame,
    target_year: int,
) -> None:
    """
    조회 조건에 해당하는 품질이슈 로우데이터(Raw Data) 테이블을 조건부 서식과 함께 표출합니다.
    """
    section_header(
        title="Quality Issue Raw Records",
        subtitle="Detailed raw records of quality issues with real-time conditional styles.",
        icon_name="sticky_note_2",
        extra_info_html=f"""
        <div style="font-size: 0.75rem; color: {colors.app_text_muted}; background: {colors.app_background}; border: 1px solid {colors.app_border}; border-radius: 0.25rem; padding: 0.35rem 0.75rem;">
            Target Year: <strong style="color: {colors.app_text_primary}; font-weight: 600;">{target_year}</strong>
        </div>
        """,
    )
    st.caption(":material/info: Hover over table headers to view detailed descriptions for each column.")

    df_display = df_raw.loc[df_raw["REG_DATE"].dt.year == target_year]

    def highlight_value(val, target_val):
        if val > target_val:
            return f"background-color: {colors.orange_50}; color: {colors.orange_900}; font-weight: 600;"
        return ""

    # IBM Carbon 시각화 컬러 가이드를 연동한 정밀 데이터프레임 스타일링
    styled_df = (
        df_display.style.set_properties(
            subset=["PLANT", "TYPE_NAME", "CAT_NAME", "SUB_CAT_NAME"],
            **{
                "background-color": f"{colors.app_surface_muted}",
                "text-align": "center",
                "font-size": "12px",
                "border": f"1px solid {colors.app_border}",
            },
        )
        .applymap(highlight_value, subset=["REG_PRD"], target_val=2)
        .applymap(highlight_value, subset=["RTN_PRD"], target_val=7)
        .applymap(highlight_value, subset=["CTM_PRD"], target_val=5)
        .applymap(highlight_value, subset=["COMP_PRD"], target_val=2)
        .applymap(highlight_value, subset=["MTTC"], target_val=10)
    )

    # 동적 컬럼 헬퍼 연동
    raw_col_config = get_dynamic_column_configs("cqms_quality_main", list(df_display.columns))
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config=raw_col_config,
        height=500,
        hide_index=True,
    )
```

- [ ] **Step 2: Commit `rawdata_tab.py`**

```bash
git add app/pages/_10_dashboard/oe_tabs/rawdata_tab.py
git commit -m "feat: add modular rawdata_tab.py"
```

---

### Task 6: Refactor the Main Dashboard Page Router

**Files:**
- Modify: `app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py`

**Interfaces:**
- Consumes: `app.pages._10_dashboard.oe_tabs` (modular renderers)
- Produces: Cleaner `oe_quality_issue_dashboard_page.py` that delegates rendering.

- [ ] **Step 1: Apply surgical replacement in the main page router**

Remove the original 4 tab rendering functions and the 3 dialog modal functions, and replace them with imports from the new `oe_tabs` package.

Replace old imports and definitions:
- Remove lines 189-204 (defining `COMMON_REMAIN_COLUMNS`).
- Remove lines 400-1015 (modal definitions and render functions).
- At the top imports section, add:
  ```python
  from app.pages._10_dashboard.oe_tabs import (
      render_global_tab,
      render_plant_tab,
      render_oeqg_tab,
      render_rawdata_tab,
  )
  ```

- [ ] **Step 2: Verify code syntax and compile**

Verify there are no import loops or syntax errors by running python compiler check:
`python -m py_compile app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py`

- [ ] **Step 3: Commit page refactor**

```bash
git add app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py
git commit -m "refactor: simplify main oe_quality_issue_dashboard_page.py by delegating rendering to oe_tabs package"
```

---

### Task 7: Create and Execute the Testing Validation Suite

**Files:**
- Create: `tests/test_oe_quality_issue_dashboard_page.py`

**Interfaces:**
- Consumes: `app.pages._10_dashboard.oe_quality_issue_dashboard_page` and `app.pages._10_dashboard.oe_tabs`
- Produces: Automated test validation.

- [ ] **Step 1: Write the test file**

Write a test file `tests/test_oe_quality_issue_dashboard_page.py` to assert that all renderers and dialog modals can be imported and have valid function signatures:

```python
"""
oe_quality_issue_dashboard_page.py 및 하위 탭 렌더러 임포트와 서명 검증 테스트
- 최종 수정일: 2026-07-20
"""

import inspect
import pandas as pd


def test_oe_tabs_imports():
    """oe_tabs 패키지에서 4개 탭 렌더러가 올바르게 임포트되는지 검증합니다."""
    from app.pages._10_dashboard.oe_tabs import (
        render_global_tab,
        render_plant_tab,
        render_oeqg_tab,
        render_rawdata_tab,
    )
    
    assert render_global_tab is not None
    assert render_plant_tab is not None
    assert render_oeqg_tab is not None
    assert render_rawdata_tab is not None


def test_render_signatures():
    """각 렌더러 함수의 인자 서명(Signature) 정합성을 검증합니다."""
    from app.pages._10_dashboard.oe_tabs import (
        render_global_tab,
        render_plant_tab,
        render_oeqg_tab,
        render_rawdata_tab,
    )
    
    global_sig = inspect.signature(render_global_tab)
    assert "df_yearly_trend" in global_sig.parameters
    assert "df_monthly_trend" in global_sig.parameters
    assert "df_oem_data" in global_sig.parameters
    assert "df_market_data" in global_sig.parameters
    assert "df_plant_data" in global_sig.parameters
    assert "df_issue_type_data" in global_sig.parameters
    assert "df_mttc_trend" in global_sig.parameters
    assert "df_mttc_plant" in global_sig.parameters
    assert "target_year" in global_sig.parameters

    plant_sig = inspect.signature(render_plant_tab)
    assert "df_oeapp_pivot" in plant_sig.parameters
    assert "df_plant_agg" in plant_sig.parameters
    assert "df_raw" in plant_sig.parameters
    assert "df_mttc_plant" in plant_sig.parameters
    assert "df_plant_month_trend" in plant_sig.parameters
    assert "target_plant" in plant_sig.parameters
    assert "target_year" in plant_sig.parameters

    oeqg_sig = inspect.signature(render_oeqg_tab)
    assert "df_oeqg_trend" in oeqg_sig.parameters
    assert "df_raw" in oeqg_sig.parameters
    assert "df_mttc_trend" in oeqg_sig.parameters
    assert "df_mttc_oeqg_data" in oeqg_sig.parameters
    assert "target_year" in oeqg_sig.parameters

    raw_sig = inspect.signature(render_rawdata_tab)
    assert "df_raw" in raw_sig.parameters
    assert "target_year" in raw_sig.parameters


def test_main_page_module_imports():
    """메인 페이지 모듈 자체가 정상적으로 파싱 및 로드되는지 검증합니다."""
    import app.pages._10_dashboard.oe_quality_issue_dashboard_page as page
    assert page is not None
```

- [ ] **Step 2: Run pytest to verify all tests pass**

Run: `pytest tests/test_oe_quality_issue_dashboard_page.py -v`
Expected: PASS

- [ ] **Step 3: Commit tests**

```bash
git add tests/test_oe_quality_issue_dashboard_page.py
git commit -m "test: add imports and signatures test suite for oe_quality_issue_dashboard"
```
