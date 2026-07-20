# Data Analysis Page Header Info Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 제품 분석(Data Analysis) 페이지의 메타데이터와 조회 기간 요약을 별도의 `st.info` 패널로 렌더링하지 않고, `page_header` 공통 위젯의 `info_items` 매개변수에 주입하여 디자인 시스템에 완전 병합 및 통합합니다.

**Architecture:** 
`generate_iqm_plus_master_df` 를 통해 추출된 동적 메타데이터(공장 코드, OEM, 차종, 모니터링 기간)를 `{"label": "...", "value": "..."}` 형태의 딕셔너리 리스트(`info_items`)로 패키징합니다. 이 리스트를 `page_header` 공통 위젯 호출 시 함께 주입하여 헤더 영역 우측 정보 패널 레이아웃에 완전히 녹여냅니다. 기존의 `st.info` 노출 블록은 완벽히 제거합니다.

**Tech Stack:** Streamlit, Pandas, Python Datetime

## Global Constraints

- Safety Lock 준수: 수정 전 반드시 본 구현 계획 아티팩트를 사용자에게 제시하여 동의를 획득하고 수정을 이행해야 합니다.
- 이모지 전면 사용 금지: 마크다운 계획서, 소스코드 및 주석 등 어디에서도 유니코드 이모지를 직접 쓰지 않습니다.
- WSL 마크다운 상대 경로 준수: 마크다운 하이퍼링크 작성 시 워크스페이스 루트 기준의 상대경로만 사용해야 합니다.

---

### Task 1: Merge Metadata Panel into page_header

**Files:**
- Modify: [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py:1260-1309)

**Interfaces:**
- Consumes: `generate_iqm_plus_master_df()`, `analysis_params`
- Produces: Integrated `page_header` layout with meta information in `info_items`

- [ ] **Step 1: Replace logic in data_analysis_page_dev.py**

Modify [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py) around lines 1260-1309 to:
1. Extract dynamic metadata before calling `page_header`.
2. Construct the `info_items` list.
3. Call `page_header` with `info_items=info_items`.
4. Delete the duplicate `st.info` widget call.

```python
# =========================================================================
# SECTION 9. Main Streamlit Execution (메인 화면 및 탭별 렌더링)
# =========================================================================
load_css()

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

# 디자인 시스템 중앙 통제 헤더용 info_items 딕셔너리 빌드
info_items = [
    {"label": "공장지정보 M - Code 정보", "value": f"M-Code {target_mcode}({plant_val})"},
    {"label": "OEM / Vehicle", "value": f"{oem_val} / {vehicle_val}"},
    {"label": "IQM 모니터링 기간", "value": f"{start_str} ~ {end_str}"}
]

page_header(
    title="Data Analysis",
    title_icon=":material/view_object_track:",
    subtitle="제품 규격 마스터, 생산 이력, 품질 현황 및 계측 데이터를 다차원으로 교차 연계 분석합니다.",
    info_items=info_items,
)

# 본문과 네비게이션 사이의 공간 확보용 여백 (유니코드 이모지 배제 규칙 준수)
st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
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
git commit -m "feat: merge dynamic metadata into page_header info_items"
```
