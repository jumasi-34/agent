# Data Analysis Page Header Info Revision Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 제품 분석(Data Analysis) 페이지의 `page_header` 호출부 바로 직후(제출 여부와 무관하게 상단에 항상 노출되는 영역)에 동적 스펙 요약 정보 카드(`st.info`)를 이식합니다.

**Architecture:** 
사이드바 입력 UI(`user_input_section`)의 파라미터 확정 단계를 `page_header` 렌더링 직전으로 상향 조정하여 첫 로드 시에도 유효한 M-Code 데이터가 확정되도록 보장합니다. 그 후 `page_header` 직후에 `generate_iqm_plus_master_df`를 기반으로 선택된 M-Code의 메타데이터를 추출해 `st.info`를 렌더링하고, 기존 탭 내부의 중복 `st.info` 블록은 깔끔히 지웁니다.

**Tech Stack:** Streamlit, Pandas, Python Datetime

## Global Constraints

- Safety Lock 준수: 수정 전 반드시 본 구현 계획 아티팩트를 사용자에게 제시하여 동의를 획득하고 수정을 이행해야 합니다.
- 이모지 전면 사용 금지: 모든 주석 및 코드에 유니코드 이모지를 쓰지 않고 `:material/info:` 머티리얼 벡터를 사용합니다.
- WSL 마크다운 상대 경로 준수: 마크다운 하이퍼링크 작성 시 워크스페이스 루트 기준의 상대경로만 사용해야 합니다.

---

### Task 1: Re-ordering and Header Info Integration

**Files:**
- Modify: [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py:1248-1322)

**Interfaces:**
- Consumes: `generate_iqm_plus_master_df()`, `analysis_params`
- Produces: `st.info` on dynamic header meta info

- [ ] **Step 1: Replace logic in data_analysis_page_dev.py**

Modify [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py) around lines 1248-1322 to:
1. Move the sidebar `user_input_section` rendering before `page_header`.
2. Add the dynamic `st.info` block right after `page_header`.
3. Remove the duplicate `st.info` block inside `if analysis_params.step1_user_form_submit_flag:` block.

```python
# =========================================================================
# SECTION 8. Session State Initialization (세션 상태 초기화)
# =========================================================================
# 모든 파라미터를 데이터클래스에서 관리
# 데이터 클래스를 초기화 후, 데이터 클래스 유무에 따라 메뉴 및 탭 초기화

_init_session_state("analysis_params", IqmPlusParams())
analysis_params = st.session_state.analysis_params
if analysis_params.step0_selected_menu is None:
    analysis_params.step0_selected_menu = MENU_SELECT_DICT["IQM_PLUS"]
if analysis_params.step2_selected_view_tab is None:
    analysis_params.step2_selected_view_tab = TABS[0]

# -- 사용자 입력 섹션 렌더링 (헤더 메타 정보 사전 확정을 위해 우선 실행)
with st.sidebar:
    st.subheader("User Input")
    analysis_params = user_input_section(analysis_params)


# =========================================================================
# SECTION 9. Main Streamlit Execution (메인 화면 및 탭별 렌더링)
# =========================================================================
load_css()
page_header(
    title="Data Analysis",
    title_icon=":material/view_object_track:",
    subtitle="제품 규격 마스터, 생산 이력, 품질 현황 및 계측 데이터를 다차원으로 교차 연계 분석합니다.",
)

# =========================================================================
# SECTION 10. Dynamic Header Meta Info (동적 상단 메타데이터 패널 렌더링)
# =========================================================================
# * [UI 컴포넌트 - 분석 타겟 제품의 메타정보 요약 카드 렌더링]
master_df = generate_iqm_plus_master_df()
target_mcode = analysis_params.step1_basic_mcode
if not target_mcode:
    mcode_list = sorted(master_df["MFG_MCODE"].unique().tolist())
    target_mcode = mcode_list[0] if mcode_list else "-"

mcode_filter = master_df["MFG_MCODE"] == target_mcode
mcode_info_df = master_df.loc[mcode_filter]

plant_val = "-"
oem_val = "-"
vehicle_val = "-"

if not mcode_info_df.empty:
    row = mcode_info_df.iloc[0]
    plant_val = row.get("PLANT", "-") or "-"
    oem_val = row.get("Car Maker", "-") or "-"
    vehicle_val = row.get("Vehicle Model Local", "-") or "-"

# 날짜 가독성 포맷팅 (%Y. %b. %d 형식 적용)
start_dt = analysis_params.step1_basic_start_date
end_dt = analysis_params.step1_basic_end_date
start_str = start_dt.strftime("%Y. %b. %d") if hasattr(start_dt, "strftime") else str(start_dt) if start_dt else "-"
end_str = end_dt.strftime("%Y. %b. %d") if hasattr(end_dt, "strftime") else str(end_dt) if end_dt else "-"

info_text = (
    f"공장지정보 M - Code 정보를 노출하라 : M-Code {target_mcode}({plant_val})\n\n"
    f"OEM / Vehicle - {oem_val} / {vehicle_val}\n\n"
    f"IQM 모니터링 기간 - {start_str} ~ {end_str}"
)
st.info(info_text, icon=":material/info:")

# 본문과 네비게이션 사이의 공간 확보용 여백 (유니코드 이모지 배제 규칙 준수)
st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)


if analysis_params.step1_user_form_submit_flag:
    if "selected_view_tab" not in st.session_state:
        st.session_state["selected_view_tab"] = (
            analysis_params.step2_selected_view_tab or TABS[0]
        )
    selected_view_tab = st.segmented_control(
        label="Tabs",
        options=TABS,
        selection_mode="single",
        label_visibility="collapsed",
        key="selected_view_tab",
    )
    analysis_params.step2_selected_view_tab = selected_view_tab  # 동기화
    # -- M-Code 기반 메타 정보 수집(plm)
    analysis_params = get_meta_info_from_plm(analysis_params)
```

- [ ] **Step 2: Run lint check and compilation check**

Run: `python -m py_compile app/pages/_20_analysis/data_analysis_page_dev.py`
Expected output: No syntax error or compilation error.

- [ ] **Step 3: Update Graphify Knowledge Graph**

Run: `graphify update .`
Expected output: SUCCESS and updated graph representation.

- [ ] **Step 4: Commit the change**

```bash
git add app/pages/_20_analysis/data_analysis_page_dev.py
git commit -m "feat: move dynamic info panel immediately after page_header"
```
