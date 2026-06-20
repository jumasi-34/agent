"""
Standard Template for Dashboard UI Pages (*_page.py)
- Last Modified: 2026-06-19
- Description: This file serves as the gold-standard reference template for all Streamlit page controllers.
  It demonstrates modular tab/section rendering, strict session state interception, defensive data loading,
  and the integration of central UI components, themes, and dynamic column configurations.
"""

# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
# 1) 외부 표준 패키지
import re
from datetime import datetime
from pathlib import Path
from typing import Any, dict, list

import pandas as pd
import streamlit as st

# 2) 공통 코어 모듈 (디자인 시스템, 공통 UI 컴포넌트, 파라미터, 유틸리티)
from app.core.boilerplate_column_config import get_dynamic_column_configs
from app.core.constants.ui import colors
from app.core.params.parameters import BaseFilterParams  # 예시 필터 파라미터 클래스
from app.core.ui.components import (
    header_main_title_info_panel,
    metric_card_vertical,
    subheader_title_panel,
    subheader_title_stats_panel,
)
from app.core.ui.styles import load_css

# 3) 비즈니스 연계 서비스 모듈 (*_df.py) 및 1:1 대칭 시각화 플롯 모듈 (*_plots.py)
# 아래는 템플릿용 가상 모듈 또는 예시 바인딩입니다. 실제 구현 시 해당 도메인 모듈로 대체합니다.
# from app.pages._10_dashboard import domain_dashboard_plots as viz
# from app.service import domain_df as service


# =========================================================================
# SECTION 2. Page Configuration & Initialization (페이지 설정 및 CSS 초기화)
# =========================================================================
# 기본 레이아웃 구성 및 공통 스타일시트 로드
st.set_page_config(
    page_title="Domain Quality Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()


# =========================================================================
# SECTION 3. Session State Interception & Widget Backups (세션 상태 제어)
# =========================================================================
# [중요 규칙] st.session_state 키 충돌 및 StreamlitAPIException 방지 장치
# key가 할당된 위젯의 값을 강제 변경해야 하는 경우, 인스턴스화 전에 백업 및 세션 클리어(가로채기)를 처리합니다.
backup_active_tab = "Overview"
if "tab_selector_key" in st.session_state:
    backup_active_tab = st.session_state.tab_selector_key


# =========================================================================
# SECTION 4. Sidebar Inputs & Parameter Assembly (사용자 필터 제어 및 파라미터 조립)
# =========================================================================
with st.sidebar:
    st.title("Filters")
    
    # 1) 사용자 입력 필터 정의
    selected_plant = st.selectbox(
        label="Select Plant",
        options=["Plant A", "Plant B", "Plant C"],
        index=0,
    )
    
    selected_date_range = st.date_input(
        label="Select Period",
        value=(datetime(2026, 1, 1), datetime(2026, 6, 19)),
    )
    
    st.divider()
    
    # 2) 표준 파라미터 데이터클래스 조립 (개별 변수로 서비스 레이어에 넘기지 말 것)
    # 실제로는 도메인에 알맞은 *Params 클래스(예: IqmPlusParams, ProductionParams)를 인스턴스화합니다.
    params = BaseFilterParams(
        plant_list=[selected_plant],
        start_date=selected_date_range[0].strftime("%Y-%m-%d"),
        end_date=selected_date_range[1].strftime("%Y-%m-%d") if len(selected_date_range) > 1 else selected_date_range[0].strftime("%Y-%m-%d"),
    )


# =========================================================================
# SECTION 5. Data Loading & Service Call (데이터 수집 및 방어적 설계)
# =========================================================================
# 데이터 로드 중 스피너 노출 및 비용 제어를 위한 서비스 레이어 캐싱 연동
with st.spinner("Loading quality data..."):
    # 가상의 서비스 및 플롯 함수를 모킹하여 구조적 작동을 보장합니다.
    # df = service.preprocessing_domain_rawdata(params)
    
    # 템플릿 구동을 위한 모크 데이터프레임 생성
    df = pd.DataFrame({
        "PLANT": ["Plant A", "Plant A", "Plant B", "Plant C"],
        "MCODE": ["M001", "M002", "M003", "M004"],
        "DEFECT_COUNT": [12, 5, 24, 3],
        "SCRAP_INDEX": [92.5, 96.0, 88.2, 99.1],
        "REWORK_INDEX": [95.1, 98.4, 91.0, 97.5],
        "TOTAL_INDEX": [93.8, 97.2, 89.6, 98.3],
        "REG_DATE": ["2026-06-10", "2026-06-12", "2026-06-15", "2026-06-18"],
    })

# [방어적 설계] 데이터프레임 무결성 및 빈 데이터 검증 처리
if df is None or df.empty:
    st.warning("No data found for the selected filter conditions. Please adjust the filters in the sidebar.")
    st.stop()


# =========================================================================
# SECTION 6. Modular Tab/Section Rendering Functions (모듈화 렌더링 함수군)
# =========================================================================
# 렌더링 코드가 길어지거나 복잡해질 경우, 단일 함수에 수백 줄을 몰아넣지 않고
# 아래와 같이 명확한 탭 단위, 탭 내 복잡할 경우 세부 섹션 단위로 역할을 쪼개어 정의합니다.

# * [UI 렌더러 - 상단 메인 헤더 정보 패널]
def render_header_section(data_df: pd.DataFrame) -> None:
    """
    메인 대시보드 상단의 타이틀과 공통 메타 정보 요약 패널을 렌더링합니다.

    Parameters
    ----------
    data_df : pd.DataFrame
        현재 필터링되어 화면에 표시될 메인 데이터프레임.
    """
    # 이모지 전면 배제 및 Material Icons (:material/icon_name:) 필수 규정 준수
    header_main_title_info_panel(
        title="Quality Performance Analysis",
        subtitle="Real-time production quality monitoring and index tracking system",
        info_items=[
            {"label": "Active Plant", "value": ", ".join(params.plant_list)},
            {"label": "Total Specs", "value": str(data_df["MCODE"].nunique())},
            {"label": "Total Defects", "value": str(data_df["DEFECT_COUNT"].sum())},
        ],
    )


# * [UI 렌더러 - 요약 탭 메인 콘텐츠]
def render_overview_tab(data_df: pd.DataFrame) -> None:
    """
    요약(Overview) 탭의 전체 레이아웃과 개별 카드/차트 섹션을 렌더링합니다.

    Parameters
    ----------
    data_df : pd.DataFrame
        표시할 데이터프레임.
    """
    # 탭 내부가 복잡하거나 위젯이 다수 포함되는 경우 하위 섹션 함수로 쪼개어 호출
    _render_overview_kpi_cards(data_df)
    st.markdown("---")
    _render_overview_charts(data_df)


# * [UI 렌더러 - 요약 탭 KPI 지표 카드 섹션]
def _render_overview_kpi_cards(data_df: pd.DataFrame) -> None:
    """
    요약 탭 상단에 위치하는 핵심 성과 지표(KPI) 카드들을 가로 그리드로 렌der합니다.

    Parameters
    ----------
    data_df : pd.DataFrame
        지표 계산용 데이터프레임.
    """
    avg_total = data_df["TOTAL_INDEX"].mean()
    avg_scrap = data_df["SCRAP_INDEX"].mean()
    avg_rework = data_df["REWORK_INDEX"].mean()

    # 타이틀 정보 통계 패널 연동 (Material 아이콘 접두사 적용)
    subheader_title_stats_panel(
        title="Key Quality Indices",
        subtitle="Summary of core quality index performance across targets",
        title_icon="material_icon:analytics",
    )

    # 1:4 가로 그리드 배치 및 개별 메트릭 카드 렌더링
    cols = st.columns(3)
    with cols[0]:
        metric_card_vertical(
            title="Comprehensive Total Index",
            value=f"{avg_total:.2f}",
            unit="pts",
        )
    with cols[1]:
        metric_card_vertical(
            title="Scrap Control Index",
            value=f"{avg_scrap:.2f}",
            unit="pts",
        )
    with cols[2]:
        metric_card_vertical(
            title="Rework Prevention Index",
            value=f"{avg_rework:.2f}",
            unit="pts",
        )


# * [UI 렌더러 - 요약 탭 시각화 차트 섹션]
def _render_overview_charts(data_df: pd.DataFrame) -> None:
    """
    요약 탭의 메인 플롯(막대 그래프 등) 영역을 분할 렌더링합니다.

    Parameters
    ----------
    data_df : pd.DataFrame
        시각화할 데이터프레임.
    """
    subheader_title_panel(
        title="Visualized Quality Trends",
        title_icon="material_icon:bar_chart",
    )

    with st.container(border=True):
        col_left, col_right = st.columns(2)
        
        # 1:1 대칭 시각화 플롯 모듈(domain_dashboard_plots.py) 호출 표준 예시
        # fig_defect = viz.draw_defect_count_bar(data_df)
        # fig_index = viz.draw_quality_index_trend(data_df)
        
        # 템플릿 구동을 위한 인라인 가상 차트 렌더링 (실제 작업 시 plots 모듈로 이관 필수)
        import plotly.express as px
        
        # 디자인 시스템 테마 토큰 적용 (L2-color-system 표준 연동)
        fig_left = px.bar(
            data_df, 
            x="MCODE", 
            y="DEFECT_COUNT", 
            color_discrete_sequence=[colors.get("app_primary", "#FF6B00")]
        )
        fig_left.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        
        fig_right = px.line(
            data_df, 
            x="MCODE", 
            y="TOTAL_INDEX", 
            color_discrete_sequence=[colors.get("status_info", "#0088FF")]
        )
        fig_right.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

        with col_left:
            st.plotly_chart(fig_left, use_container_width=True, key="overview_defect_chart")
        with col_right:
            st.plotly_chart(fig_right, use_container_width=True, key="overview_index_chart")


# * [UI 렌더러 - 상세 내역 탭 메인 콘텐츠]
@st.fragment
def render_details_tab(data_df: pd.DataFrame) -> None:
    """
    상세 내역(Details) 탭의 양방향 탐색 테이블 및 상세 수치 조회를 렌더링합니다.
    Fragment 지정을 통해 테이블 필터 및 조작 시 페이지 전체 Rerun을 유발하지 않고
    로컬 영역만 고속 렌더링하도록 격리 및 최적화합니다.

    Parameters
    ----------
    data_df : pd.DataFrame
        표시할 상세 데이터프레임.
    """
    subheader_title_panel(
        title="Granular Specification Records",
        title_icon="material_icon:table_view",
    )

    with st.container(border=True):
        # 1) 로컬 제어용 인터랙티브 위젯 (Fragment 내부)
        selected_mcode = st.multiselect(
            label="Filter by Specification Code (M-Code)",
            options=data_df["MCODE"].unique().tolist(),
            default=data_df["MCODE"].unique().tolist(),
        )
        
        filtered_df = data_df[data_df["MCODE"].isin(selected_mcode)]
        
        # 2) 동적 컬럼 설정기(Boilerplate) 호출 필수 표준 연동
        # DB 테이블 물리 스키마 정보와 자동 매핑하여 영문 컬럼을 한국어 표시명, 소수점 포맷으로 다듬어 줍니다.
        column_configs = get_dynamic_column_configs("cqms_qi_mttc", filtered_df.columns)
        
        # 3) 데이터 테이블 렌더링
        st.dataframe(
            filtered_df,
            column_config=column_configs,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================================
# SECTION 7. Main Render Loop (메인 렌더링 루프 및 탭 라우팅)
# =========================================================================
# 1) 메인 헤더 및 정보 보드 우선 렌더링
render_header_section(df)

# 2) 프리미엄 탭 메뉴 구성 (Material Icons 적용, 이모지 완전 제거)
main_tabs = st.tabs([
    ":material/dashboard: Overview", 
    ":material/list_alt: Detailed Records"
])

# 3) 선택된 탭에 따라 각각 할당된 독립 렌더링 함수 기동 (역할의 물리 격리)
with main_tabs[0]:
    render_overview_tab(df)

with main_tabs[1]:
    render_details_tab(df)
