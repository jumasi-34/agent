# Data Analysis Page Header Info Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 제품 분석(Data Analysis) 페이지 상단 탭 바로 위에 선택된 M-Code의 메타데이터(공장 코드, OEM 브랜드, 차량 모델명) 및 분석 기간을 동적으로 노출하는 수려한 안내 박스(st.info)를 이식합니다.

**Architecture:** 사용자가 입력 폼을 제출(Submit)한 이후 영역에서, `generate_iqm_plus_master_df` 모듈을 활용하여 선택된 M-Code에 종속된 공장(PLANT), OEM(Car Maker), 차종(Vehicle Model Local) 메타데이터를 SQLite Staging DB 스펙 마스터로부터 안전하게 추출합니다. 기간은 입력된 날짜 변수에서 추출하여 가독성 높은 포맷(YYYY. Mon. DD)으로 변환 후 `st.info` 패널을 렌더링합니다.

**Tech Stack:** Streamlit, Pandas, Python Datetime

## Global Constraints

- Safety Lock 준수: 수정 전 반드시 본 구현 계획 아티팩트를 사용자에게 제시하여 동의를 획득하고 수정을 이행해야 합니다.
- 이모지 전면 사용 금지: UI 화면, 텍스트, 버튼, 알림 박스 및 코드 주석 등 어떠한 곳에서도 일반 유니코드 이모지(별, 로봇 등)를 사용할 수 없습니다. 아이콘이 필요할 경우 오직 `:material/info:` 등의 머티리얼 벡터 아이콘을 사용해야 합니다.
- WSL 마크다운 상대 경로 준수: 마크다운 하이퍼링크 작성 시 절대경로 및 file 프로토콜을 사용하지 않고 워크스페이스 루트 기준의 상대경로만 사용해야 합니다.

---

### Task 1: Data Analysis Page Header Info Integration

**Files:**
- Modify: [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py:1289-1294)

**Interfaces:**
- Consumes: `generate_iqm_plus_master_df()`, `analysis_params`
- Produces: `st.info` dynamic info widget

- [ ] **Step 1: Get meta data and format date representation**

Modify [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py) around line 1289 (right after `analysis_params = get_meta_info_from_plm(analysis_params)`) to search master DB metadata and render st.info card.

```python
    # -- M-Code 기반 메타 정보 수집(plm)
    analysis_params = get_meta_info_from_plm(analysis_params)

    # =========================================================================
    # SECTION 10. Dynamic Header Meta Info (동적 상단 메타데이터 패널 렌더링)
    # =========================================================================
    # * [UI 컴포넌트 - 분석 타겟 제품의 메타정보 요약 카드 렌더링]
    master_df = generate_iqm_plus_master_df()
    mcode_filter = master_df["MFG_MCODE"] == analysis_params.step1_basic_mcode
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
    start_str = start_dt.strftime("%Y. %b. %d") if hasattr(start_dt, "strftime") else str(start_dt)
    end_str = end_dt.strftime("%Y. %b. %d") if hasattr(end_dt, "strftime") else str(end_dt)

    info_text = (
        f"공장지정보 M - Code 정보를 노출하라 : M-Code {analysis_params.step1_basic_mcode}({plant_val})\n\n"
        f"OEM / Vehicle - {oem_val} / {vehicle_val}\n\n"
        f"IQM 모니터링 기간 - {start_str} ~ {end_str}"
    )
    st.info(info_text, icon=":material/info:")
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
git commit -m "feat: add dynamic info panel to data analysis page header"
```
