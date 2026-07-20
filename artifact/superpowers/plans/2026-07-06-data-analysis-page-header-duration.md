# Data Analysis Page Header Duration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 제품 분석(Data Analysis) 페이지 상단 헤더 우측의 'IQM 모니터링 기간' 정보 값에 두 날짜 간의 실소요 일수(days)를 계산하여 동적으로 표시합니다. (예: `2024. Jun. 01 ~ 2025. Mar. 29 (301D)`)

**Architecture:** 
`analysis_params.step1_basic_start_date` 및 `analysis_params.step1_basic_end_date` 날짜 변수의 호환형식(`Timestamp`/`datetime`/`date`)을 안전하게 동기화한 뒤, 뺄셈 연산(`(end_date - start_date).days`)을 통해 차이 일수를 정밀 산출합니다. 구해진 일수를 `(일수D)` 형태의 접미사로 모니터링 기간 값에 합성하여 주입합니다.

**Tech Stack:** Python Datetime, Pandas Timestamp

## Global Constraints

- Safety Lock 준수: 수정 전 반드시 본 구현 계획 아티팩트를 사용자에게 제시하여 동의를 획득하고 수정을 이행해야 합니다.
- 이모지 전면 사용 금지: 주석 및 소스코드, 마크다운 계획 문서 내 어디서도 유니코드 이모지를 직접 쓰지 않습니다.
- WSL 마크다운 상대 경로 준수: 마크다운 하이퍼링크 작성 시 워크스페이스 루트 기준의 상대경로만 사용해야 합니다.

---

### Task 1: Calculate and Append Duration to Header Date Range

**Files:**
- Modify: [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py:1289-1300)

**Interfaces:**
- Consumes: `analysis_params.step1_basic_start_date`, `analysis_params.step1_basic_end_date`
- Produces: Formatted period string with duration days (e.g., `2024. Jun. 01 ~ 2025. Mar. 29 (301D)`)

- [ ] **Step 1: Calculate duration and modify info_items in data_analysis_page_dev.py**

Modify [app/pages/_20_analysis/data_analysis_page_dev.py](app/pages/_20_analysis/data_analysis_page_dev.py) around lines 1289-1300 to:
1. Extract and convert start/end dates to unified `date` objects.
2. Calculate the difference in days.
3. Build the period string with the calculated days (e.g. `(301D)`).

```python
# 날짜 가독성 포맷팅 (%Y. %b. %d 형식 적용)
start_dt = analysis_params.step1_basic_start_date
end_dt = analysis_params.step1_basic_end_date
start_str = start_dt.strftime("%Y. %b. %d") if hasattr(start_dt, "strftime") else str(start_dt) if start_dt else "-"
end_str = end_dt.strftime("%Y. %b. %d") if hasattr(end_dt, "strftime") else str(end_dt) if end_dt else "-"

# 소요 기간 계산 (Timestamp/datetime/date 간 안전한 뺄셈 대응)
duration_str = ""
if start_dt and end_dt:
    try:
        s_date = start_dt.date() if hasattr(start_dt, "date") else start_dt
        e_date = end_dt.date() if hasattr(end_dt, "date") else end_dt
        days_diff = (e_date - s_date).days
        duration_str = f" ({days_diff}D)"
    except Exception:
        duration_str = ""

# 디자인 시스템 중앙 통제 헤더용 info_items 딕셔너리 빌드
info_items = [
    {"label": "공장지정보 M - Code 정보", "value": f"M-Code {target_mcode}({plant_val})"},
    {"label": "OEM / Vehicle", "value": f"{oem_val} / {vehicle_val}"},
    {"label": "IQM 모니터링 기간", "value": f"{start_str} ~ {end_str}{duration_str}"}
]
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
git commit -m "feat: append calculated duration days to page_header monitoring period"
```
