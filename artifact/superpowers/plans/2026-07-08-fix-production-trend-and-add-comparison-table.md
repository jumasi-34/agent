# Production Trend X-Axis Fix & BP Comparison Table Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the overlapping/numeric X-axis issue in the weekly Production Trend plot by changing the weekly format to `YYYY.WW`, and implement a high-fidelity Slate-themed HTML comparison table comparing production before and after the Break Point based on actual calendar days.

**Architecture:** 
1. **X-Axis Week Formatting (`YYYY.WW`)**: Update the `fig_production_trend` function in both `data_analysis_plots_dev.py` and `data_analysis_plots.py` to normalize and store weekly period IDs as strings formatted with a dot (`year.week`), forcing Plotly to treat the X-axis strictly as a categorical sequence. Update `test_production_trend_plot.py` expectations and verify with Pytest.
2. **BP Comparison Table**: Inside `data_analysis_page_dev.py` and `data_analysis_page.py`, add a helper function `_render_bp_comparison_table(params, df_production)` to calculate the sum and daily average (Total / Actual Calendar Days) for two intervals: `[Start ~ BP]` and `[BP + 1 ~ End]`. Display a beautiful, premium Slate-themed HTML table directly below the Production Trend chart using Streamlit markdown.

**Tech Stack:** Streamlit, Plotly, Pandas, Python (datetime)

## Global Constraints
- **Safety Lock**: Modify only designated files (`data_analysis_plots_dev.py`, `data_analysis_plots.py`, `data_analysis_page_dev.py`, `data_analysis_page.py`, `test_production_trend_plot.py`).
- **WSL Markdown Link Constraint**: Avoid absolute linux paths or `file:///` protocols in markdown files/chat. Use relative paths such as `app/pages/_20_analysis/data_analysis_plots_dev.py`.
- **UI & Emoji Ban**: Absolutely NO unicode emojis (e.g., ⭐, 🚀, ✔️, ❌) are allowed in UI text, labels, HTML, or code comments. Use Streamlit Material Icons (`:material/icon_name:`) if icons are needed.
- **Korean Comments Principle**: Ensure all python code docstrings and comments are written in Korean (한국어) for code maintainability and team alignment. Follow Google style and Section Highlight headers.

---

## Task 1: Weekly X-Axis Format Normalization (`YYYYWW` -> `YYYY.WW`)

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_plots_dev.py`
- Modify: `app/pages/_20_analysis/data_analysis_plots.py`
- Modify: `tests/pages/test_production_trend_plot.py`

**Interfaces:**
- Consumes: Raw `df_production` with integer or string `PERIOD_ID` (e.g., `202615` or `2026.15`).
- Produces: `go.Figure` with `year.week` formatted strings on the X-axis, and correctly aligned BP vertical lines.

- [ ] **Step 1: Update expectations in unit tests**
  Modify `tests/pages/test_production_trend_plot.py` to expect dots (`.`) in weekly period strings.

  ```python
  # Target File: tests/pages/test_production_trend_plot.py
  # Lines 43, 87: expected_x = ["2026.12", "2026.13", "2026.14", "2026.15"]
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/pages/test_production_trend_plot.py -v`
  Expected: FAIL (due to expecting `2026.12` instead of `202612`)

- [ ] **Step 3: Modify `fig_production_trend` in Dev Plots**
  Edit `app/pages/_20_analysis/data_analysis_plots_dev.py` to convert `PERIOD_ID` to `YYYY.WW` and format the generator.

  ```python
  # Target File: app/pages/_20_analysis/data_analysis_plots_dev.py
  
  # 1. Normalize PERIOD_ID input
  def normalize_period(x):
      x_str = str(x).strip()
      if len(x_str) == 6 and x_str.isdigit():
          return f"{x_str[:4]}.{int(x_str[4:]):02d}"
      return x_str

  df["PERIOD_ID"] = df["PERIOD_ID"].apply(normalize_period)
  
  # 2. Adjust min_period and max_period parsing
  min_period = str(df["PERIOD_ID"].min()).strip()
  if "." in min_period:
      parts = min_period.split(".")
      if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
          s_year = int(parts[0])
          s_week = int(parts[1])
  elif len(min_period) == 6 and min_period.isdigit():
      s_year = int(min_period[:4])
      s_week = int(min_period[4:])
      
  # 3. Modify get_weekly_periods to yield dots
  def get_weekly_periods(sy, sw, ey, ew) -> list:
      res = []
      cy, cw = sy, sw
      limit = 0
      while (cy < ey or (cy == ey and cw <= ew)) and limit < 600:
          res.append(f"{cy}.{cw:02d}")
          cw += 1
          last_week = pd.Timestamp(cy, 12, 28).isocalendar()[1]
          if cw > last_week:
              cw = 1
              cy += 1
          limit += 1
      return res
      
  # 4. Modify vline_x generation
  year, week, _ = dt.isocalendar()
  vline_x = f"{year}.{week:02d}"
  ```

- [ ] **Step 4: Modify `fig_production_trend` in Prod Plots**
  Apply the exact same changes to `app/pages/_20_analysis/data_analysis_plots.py` to keep the dual pipelines in sync.

- [ ] **Step 5: Run tests to verify they pass**
  Run: `pytest tests/pages/test_production_trend_plot.py -v`
  Expected: PASS

- [ ] **Step 6: Commit X-axis changes**
  ```bash
  git add app/pages/_20_analysis/data_analysis_plots_dev.py app/pages/_20_analysis/data_analysis_plots.py tests/pages/test_production_trend_plot.py
  git commit -m "refactor: change weekly production trend X-axis format to year.week"
  ```

---

## Task 2: Break Point Comparison Table Implementation (Approach A)

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page_dev.py`
- Modify: `app/pages/_20_analysis/data_analysis_page.py`

**Interfaces:**
- Consumes: `IqmPlusParams` (containing start date, end date, and BP), `df_production` (reindexed and padded dataframe).
- Produces: Premium Slate HTML markup rendered right below the plotly chart inside the `col_prod` layout.

- [ ] **Step 1: Design of the Calculation Logic**
  Implement an internal helper function `_render_bp_comparison_table(params, df_production)` inside both pages:
  - If NOT in Break Point menu, or if start_date, end_date, or bp_date is missing, return immediately.
  - Parsed datetimes: `start_dt`, `end_dt`, `bp_dt`.
  - Validate: `start_dt <= bp_dt <= end_dt`.
  - Interval 1 Days: `(bp_dt - start_dt).days + 1`
  - Interval 2 Days: `(end_dt - bp_dt).days` (if `end_dt <= bp_dt`, set days to 0 or 1 safely).
  - Production Filter & Sum:
    - Weekly: parse each `PERIOD_ID` (e.g. `2026.15`) into its ISO week Monday date.
    - Monthly: parse each `PERIOD_ID` (e.g. `2026-03`) into the 1st of that month.
    - If representing date `<= bp_dt` -> Interval 1.
    - If representing date `> bp_dt` -> Interval 2.
    - Calculate sum of `PRDT_QTY` for both intervals.
  - Calculate Daily Average: `total_interval_qty / interval_days`. If `interval_days == 0`, average is `0.0`.
  - Calculate YoY/Chg Comparison: `((avg_interval_2 - avg_interval_1) / avg_interval_1 * 100)` if `avg_interval_1 > 0` else `0.0`.

- [ ] **Step 2: Design of the Premium Slate HTML Table**
  Use raw HTML formatted via Streamlit `st.markdown(..., unsafe_allow_html=True)`.
  - No emojis. Use material icon inline if needed.
  - Layout: `display: grid` or `width: 100%; border-collapse: collapse;`.
  - Typography: Geist, Inter, system-ui.
  - Borders: Slate 200. Header background: Slate 800 with white text.
  - Hover transition effect on `tr`: `transition: background-color 0.2s ease;`.
  
  *Calculation Helper Mock Test & Implementation in Dev Page*:
  ```python
  # =========================================================================
  # SECTION 4. Helper Functions (비즈니스 집계 헬퍼)
  # =========================================================================
  def _calculate_bp_production_metrics(params, df):
      # 로직 구현 (한국어 독스트링 필치)
  ```

- [ ] **Step 3: Modify Dev Page (`data_analysis_page_dev.py`)**
  Define `_render_bp_comparison_table(params, df_production)` and call it inside the overview tab layout below `col_prod.plotly_chart`.

- [ ] **Step 4: Modify Prod Page (`data_analysis_page.py`)**
  Replicate the implementation in `data_analysis_page.py` to keep production in parity.

- [ ] **Step 5: Visual Check and Run Application Verification**
  Run and ensure no streamlit runtime exceptions or syntax errors exist. Run tests again.

- [ ] **Step 6: Commit comparison table changes**
  ```bash
  git add app/pages/_20_analysis/data_analysis_page_dev.py app/pages/_20_analysis/data_analysis_page.py
  git commit -m "feat: add premium Slate-themed BP production comparison table"
  ```
