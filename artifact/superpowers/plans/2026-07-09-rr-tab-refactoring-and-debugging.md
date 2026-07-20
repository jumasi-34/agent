# RR Tab Refactoring and Debugging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the KeyError on 'WEIGHT' and 'ACTUAL' columns in the RR tab, and refactor the RR tab to handle empty datasets defensively and support IQM Plus Only mode seamlessly.

**Architecture:** 
- Fix `rr_compare_table` in `app/service/data_analysis_df.py` to target the actual RR result column `TEST_RESULT` instead of the non-existent `WEIGHT` and `ACTUAL`.
- Add an empty-check guard in `_render_tab_rr` in `app/pages/_20_analysis/data_analysis_page_dev.py` to prevent indexing exceptions when there is no data.
- Refactor the hardcoded `"일반 규격(변경점 조회)"` conditions to `MENU_SELECT_DICT["BP"]` in `app/pages/_20_analysis/data_analysis_plots_dev.py`, and adjust internal variables in `fig_rr_pdf` to consume `TEST_RESULT`.
- Provide a robust local in-memory pytest test to verify `rr_compare_table` functionality and prevent future regressions.

**Tech Stack:** Python 3.12, Pandas, Plotly, Streamlit

## Global Constraints

- Never use raw unicode emojis. Use Google Material Icons syntax (e.g. `:material/warning:`) instead.
- All code changes must follow the Korean docstring and Section Divider Title highlight guidelines.
- Do not edit production code without prior user agreement (Safety Lock).

---

### Task 1: Create Unit Test and Verify Bug
**Files:**
- Create: `tests/test_rr_compare_table.py`

**Interfaces:**
- Consumes: `app/service/data_analysis_df.py:rr_compare_table`

- [ ] **Step 1: Write a unit test simulating the data structure and recreating the KeyError**

```python
# -*- coding: utf-8 -*-
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import pytest
import pandas as pd
from app.core.data_models.parameters import IqmPlusParams
from app.service.data_analysis_df import rr_compare_table

# =========================================================================
# SECTION 2. Test Cases (테스트 케이스 정의)
# =========================================================================
def test_rr_compare_table_key_error_simulation():
    """
    기존에 WEIGHT, ACTUAL 컬럼 결여로 인한 KeyError가 발생하는 시나리오를 시뮬레이션하고,
    수정된 코드가 TEST_RESULT 기반으로 정상 작동하는지 검증합니다.
    """
    # 원본 데이터 구조 모방
    mock_data = pd.DataFrame({
        "DATE": ["2026-07-01", "2026-07-05", "2026-07-10"],
        "TEST_RESULT": [1.2, 1.3, 1.1],
        "BARCODE": ["B1", "B2", "B3"]
    })
    
    # 파라미터 세팅
    params = IqmPlusParams()
    params.step1_basic_bp_str = "2026-07-05"
    
    # 아래 함수 실행 시 KeyError 가 더이상 발생하지 않는지 검증
    res_df = rr_compare_table(mock_data, params)
    
    assert "PRE" in res_df.index
    assert "POST" in res_df.index
    assert res_df.loc["PRE", ("TEST_RESULT", "mean")] == 1.2
    assert res_df.loc["POST", ("TEST_RESULT", "count")] == 2
```

- [ ] **Step 2: Run the test to confirm it fails on existing code**

Run: `pytest tests/test_rr_compare_table.py -v`
Expected: FAIL with `KeyError: "Columns not found: 'WEIGHT', 'ACTUAL'"`

---

### Task 2: Implement Fix for `rr_compare_table`
**Files:**
- Modify: `app/service/data_analysis_df.py`

**Interfaces:**
- Produces: `rr_compare_table` (returns aggregated df based on `TEST_RESULT`)

- [ ] **Step 1: Replace ACTUAL and WEIGHT references in `rr_compare_table` with `TEST_RESULT`**

Modify: `app/service/data_analysis_df.py:421-445`
```python
# * [SERVICE - RR PRE/POST 비교 통계 테이블 생성]
def rr_compare_table(df_rr_rawdata: pd.DataFrame, params: IqmPlusParams) -> pd.DataFrame:
    """
    Break Point 날짜 전후(PRE vs POST)의 회전저항(RR) 지수 평균, 표준편차 및 표본 수 통계 요약을 산출합니다.

    Parameters
    ----------
    df_rr_rawdata : pd.DataFrame
        회전저항 원천 데이터프레임.
    params : IqmPlusParams
        Break Point 조건이 저장된 파라미터 객체.

    Returns
    -------
    pd.DataFrame
        PRE/POST 그룹별 mean, std, count 통계 요약 데이터프레임.
    """
    df_rr_rawdata = df_rr_rawdata.copy()
    df_rr_rawdata["BP"] = "PRE"
    post_condition = df_rr_rawdata["DATE"] >= params.step1_basic_bp_str
    df_rr_rawdata.loc[post_condition, "BP"] = "POST"
    return (
        df_rr_rawdata.groupby(["BP"])["TEST_RESULT"].agg(["mean", "std", "count"]).round(3)
    )
```

- [ ] **Step 2: Run the test again to verify it passes**

Run: `pytest tests/test_rr_compare_table.py -v`
Expected: PASS

---

### Task 3: Refactor RR Tab UI & Empty Data Guard
**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page_dev.py`

**Interfaces:**
- Modifies: `_render_tab_rr`

- [ ] **Step 1: Add a robust empty-check at the beginning of `_render_tab_rr`**

Modify: `app/pages/_20_analysis/data_analysis_page_dev.py:1642-1660`
```python
    # -- Data Load
    gmes_params = RollingResistanceParams(
        view_mode="rawdata",
        mcode_list=[params.step1_basic_mcode],
        start_date=params.step1_basic_start_date_str,
        end_date=params.step1_basic_end_date_str,
    )
    df_rr_rawdata = gmes_df.preprocessing_gmes_rr_general_rawdata(gmes_params)

    # 데이터가 존재하지 않을 때의 방어적 예외 처리 수립
    if df_rr_rawdata.empty:
        st.warning("선택한 조건에 해당하는 회전저항(RR) 데이터가 존재하지 않습니다.", icon=":material/warning:")
        return

    params.step3_6_rr_ucl = df_rr_rawdata["UCL"].values[0] if "UCL" in df_rr_rawdata.columns else None
    params.step3_6_rr_lcl = df_rr_rawdata["LCL"].values[0] if "LCL" in df_rr_rawdata.columns else None
    params.step3_6_rr_barcd_list = (
        df_rr_rawdata["BARCODE"].unique().tolist() if "BARCODE" in df_rr_rawdata.columns else []
    )

    if params.step3_6_rr_barcd_list:
        df_rr_wt_compare = gmes_df.preprocessing_lottrack_general_rawdata(
            LotTrackParams(barcode_list=params.step3_6_rr_barcd_list)
        )
    else:
        df_rr_wt_compare = pd.DataFrame()
```

---

### Task 4: Refactor Hardcoded Menu Strings & Correct PDF Plot Columns
**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`

**Interfaces:**
- Modifies: `fig_rr_box`, `fig_rr_pdf`

- [ ] **Step 1: Import `MENU_SELECT_DICT` at the top of the file**

Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py:17`
```python
from app.core.data_models.parameters import IqmPlusParams
from app.core.data_models.business import MENU_SELECT_DICT
```

- [ ] **Step 2: Replace `"일반 규격(변경점 조회)"` with `MENU_SELECT_DICT["BP"]` in both functions, and use `TEST_RESULT` in `fig_rr_pdf`**

Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py:2511`
```python
    if params.step0_selected_menu == MENU_SELECT_DICT["BP"]:
```

Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py:2586`
```python
    if params.step0_selected_menu == MENU_SELECT_DICT["BP"]:
        pre_df = df_rr_rawdata.loc[df_rr_rawdata["DATE"] < params.step1_basic_bp_str]
        post_df = df_rr_rawdata.loc[df_rr_rawdata["DATE"] >= params.step1_basic_bp_str]

        pre_rr = pre_df["TEST_RESULT"].dropna()
        post_rr = post_df["TEST_RESULT"].dropna()
```

- [ ] **Step 3: Enhance `fig_compare_rr_test_mcode` with modulo coloring to prevent KeyError on more than 4 machines**

Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py:2916-2917`, `2919`, `2925`
```python
                color=IQM_INST_TINTS[i % len(IQM_INST_TINTS)],
                symbol=INST_SYMBOL_MAP[i % len(INST_SYMBOL_MAP)],
            ),
            line=dict(width=1, color=IQM_INST_TINTS[i % len(IQM_INST_TINTS)]),
```
and:
```python
            marker=dict(color=IQM_INST_TINTS[i % len(IQM_INST_TINTS)], size=6, opacity=0.5),
```

---

### Task 6: Refactor RR PDF Plot Constraints & Verification (Status: COMPLETE)
- [ ] Task 7: Secure GT Weight vs RR Coefficient Plot Safety and Decoupling (Status: PENDING)

---

### Task 7: Secure GT Weight vs RR Coefficient Plot Safety and Decoupling
**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`

**Interfaces:**
- Modifies: `fig_coefficient_gtwt_rr`

- [ ] **Step 1: Strip barcode strings on both dataframes to ensure 100% join match safety**
- [ ] **Step 2: Add an empty check for the merged dataframe. If empty, return a graceful empty plotly figure with "No matching GT Weight data found for correlation" annotation, avoiding min()/max() index errors**
- [ ] **Step 3: Verify with mock-tests that coefficient plotting is 100% robust against empty or missing weight datasets**
