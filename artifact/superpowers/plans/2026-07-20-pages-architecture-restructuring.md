# app/pages/_10_dashboard Restructuring and File Architecture Reorganization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the `app/pages/_10_dashboard` directory into dedicated page-specific folders following the `app/pages/category/page_folder/` hierarchy, establishing uniform prefix naming standards, and split over-1000-line pages into dedicated `renderer_*.py` files.

**Architecture:** We will group each page's code, plots, PRD documents, and custom tab folders into its own isolated page subdirectory under `app/pages/_10_dashboard/`. For pages that exceed 1000 lines (`iqm_plus_main_page.py` and `iqm_quality_trend_analysis_page.py`), we will surgically split the UI layout and section rendering functions into corresponding `renderer_*.py` modules while keeping the main control script lightweight. All import paths and unit tests will be comprehensively updated and validated.

**Tech Stack:** Python, Streamlit, Plotly, Pytest

## Global Constraints

- Never use standard unicode emojis; only use Streamlit's Google Material Icons syntax (e.g. `:material/icon_name:`).
- Retain all functional interfaces, dataclass configurations, and DataFrame column names.
- Do not make program-level session state modifications during widget rendering.
- All modifications must be thoroughly tested using pytest to ensure absolute behavioral correctness before claiming success.

---

### Task 1: Reorganize and Migrate "OE Quality Dashboard" Page

**Files:**
- Create Directory: `app/pages/_10_dashboard/oe_quality_dashboard/`
- Move & Rename Files:
  - `app/pages/_10_dashboard/oe_quality_issue_dashboard_page.py` -> `app/pages/_10_dashboard/oe_quality_dashboard/page_oe_quality_issue_dashboard.py`
  - `app/pages/_10_dashboard/oe_quality_issue_dashboard_plots.py` -> `app/pages/_10_dashboard/oe_quality_dashboard/plots_oe_quality_issue_dashboard.py`
  - `app/pages/_10_dashboard/oe_quality_issue_dashboard_prd.md` -> `app/pages/_10_dashboard/oe_quality_dashboard/prd_oe_quality_issue_dashboard.md`
  - `app/pages/_10_dashboard/oe_tabs/` -> `app/pages/_10_dashboard/oe_quality_dashboard/oe_tabs/`
- Test Files:
  - `tests/test_oe_quality_issue_dashboard_page.py`
  - `tests/test_rawdata_tab.py`

**Interfaces:**
- Consumes: `app.core.params.parameters`, `app.service.cqms_df`
- Produces: `app.pages._10_dashboard.oe_quality_dashboard.page_oe_quality_issue_dashboard`

- [ ] **Step 1: Move and reorganize files**
  Move the files into the new `oe_quality_dashboard` directory and its subfolders.
- [ ] **Step 2: Update internal page and tab imports**
  - In `page_oe_quality_issue_dashboard.py`:
    ```python
    from app.pages._10_dashboard.oe_quality_dashboard import plots_oe_quality_issue_dashboard as viz
    from app.pages._10_dashboard.oe_quality_dashboard.oe_tabs import (
        render_global_tab,
        render_plant_tab,
        render_oeqg_tab,
        render_rawdata_tab,
    )
    ```
  - In `oe_tabs/__init__.py`:
    ```python
    from app.pages._10_dashboard.oe_quality_dashboard.oe_tabs.global_tab import render_global_tab
    from app.pages._10_dashboard.oe_quality_dashboard.oe_tabs.plant_tab import render_plant_tab
    from app.pages._10_dashboard.oe_quality_dashboard.oe_tabs.oeqg_tab import render_oeqg_tab
    from app.pages._10_dashboard.oe_quality_dashboard.oe_tabs.rawdata_tab import render_rawdata_tab
    ```
  - In `oe_tabs/global_tab.py`, `plant_tab.py`, `oeqg_tab.py`, `rawdata_tab.py`:
    ```python
    from app.pages._10_dashboard.oe_quality_dashboard import plots_oe_quality_issue_dashboard as viz
    ```
- [ ] **Step 3: Update unit test imports**
  - In `tests/test_oe_quality_issue_dashboard_page.py` and `tests/test_rawdata_tab.py`, update module references to the new package paths.
- [ ] **Step 4: Run unit tests to verify correctness**
  Run: `pytest tests/test_oe_quality_issue_dashboard_page.py tests/test_rawdata_tab.py -v`
  Expected: PASS
- [ ] **Step 5: Commit changes**
  ```bash
  git add app/pages/_10_dashboard/oe_quality_dashboard tests/test_oe_quality_issue_dashboard_page.py tests/test_rawdata_tab.py
  git commit -m "refactor: migrate OE Quality Dashboard page and tabs to page-specific folder"
  ```

---

### Task 2: Reorganize and Split "IQM Plus Overview" Page (Exceeds 1000 Lines)

**Files:**
- Create Directory: `app/pages/_10_dashboard/iqm_plus_main/`
- Create New File: `app/pages/_10_dashboard/iqm_plus_main/renderer_iqm_plus_main.py`
- Move & Rename Files:
  - `app/pages/_10_dashboard/iqm_plus_main_page.py` -> `app/pages/_10_dashboard/iqm_plus_main/page_iqm_plus_main.py` (Split)
  - `app/pages/_10_dashboard/iqm_plus_main_plots.py` -> `app/pages/_10_dashboard/iqm_plus_main/plots_iqm_plus_main.py`
  - `app/pages/_10_dashboard/iqm_plus_main_prd.md` -> `app/pages/_10_dashboard/iqm_plus_main/prd_iqm_plus_main.md`
  - `app/pages/_10_dashboard/product_audit_plots.py` -> `app/pages/_10_dashboard/iqm_plus_main/plots_product_audit.py`
  - `app/pages/_10_dashboard/quality_metrics_plots.py` -> `app/pages/_10_dashboard/iqm_plus_main/plots_quality_metrics.py`
  - `app/pages/_10_dashboard/iqm_plus_main_page_dev.py` -> `app/pages/_10_dashboard/iqm_plus_main/page_iqm_plus_main_dev.py` (Dev copy)
  - `app/pages/_10_dashboard/iqm_plus_main_plots_dev.py` -> `app/pages/_10_dashboard/iqm_plus_main/plots_iqm_plus_main_dev.py` (Dev copy)
- Test Files:
  - `tests/test_iqm_plus_agg_log.py`
  - `tests/test_iqm_trend_rank_echart.py`

**Interfaces:**
- Consumes: `app.core.params.parameters`, `app.service.iqm_plus_service`
- Produces: `app.pages._10_dashboard.iqm_plus_main.page_iqm_plus_main`

- [ ] **Step 1: Move files to the new `iqm_plus_main` directory**
- [ ] **Step 2: Create `renderer_iqm_plus_main.py` and extract section-rendering functions**
  Move all UI section functions (`_render_manual`, `render_info_section`, `render_metric_section`, `_show_remaining_m_spec_dialog`, `_show_unreleased_spec_dialog`, `render_spec_release_status_section`, `render_launch_distribution_section`, `render_distribution_current_index_section`, `render_by_item_section`, `show_qi_modal`, `show_change_modal`, `show_ctl_modal`, `show_rr_modal`, `render_compliance_summary_section`, `render_index_trend_section`, `render_iqm_plus_rawdata_section`) from `page_iqm_plus_main.py` to `renderer_iqm_plus_main.py`. Keep imports and state variables clean.
- [ ] **Step 3: Update page script to import and delegate rendering**
  In `page_iqm_plus_main.py`, import the section renderers from `.renderer_iqm_plus_main` and call them. Keep `page_iqm_plus_main.py` under 300 lines.
- [ ] **Step 4: Update plot imports inside `plots_iqm_plus_main.py`**
  ```python
  from app.pages._10_dashboard.iqm_plus_main import plots_product_audit as audit_plots
  from app.pages._10_dashboard.iqm_plus_main import plots_quality_metrics as metrics_plots
  ```
- [ ] **Step 5: Run tests to verify correctness**
  Run: `pytest tests/test_iqm_plus_agg_log.py -v`
  Expected: PASS
- [ ] **Step 6: Commit changes**
  ```bash
  git add app/pages/_10_dashboard/iqm_plus_main
  git commit -m "refactor: migrate and split IQM Plus Overview page to page-specific folder"
  ```

---

### Task 3: Reorganize and Split "IQM Quality Trend Analysis" Page (Exceeds 1000 Lines)

**Files:**
- Create Directory: `app/pages/_10_dashboard/iqm_quality_trend_analysis/`
- Create New File: `app/pages/_10_dashboard/iqm_quality_trend_analysis/renderer_iqm_quality_trend_analysis.py`
- Move & Rename Files:
  - `app/pages/_10_dashboard/iqm_quality_trend_analysis_page.py` -> `app/pages/_10_dashboard/iqm_quality_trend_analysis/page_iqm_quality_trend_analysis.py` (Split)
  - `app/pages/_10_dashboard/iqm_quality_trend_analysis_plots.py` -> `app/pages/_10_dashboard/iqm_quality_trend_analysis/plots_iqm_quality_trend_analysis.py`
  - `app/pages/_10_dashboard/iqm_quality_trend_analysis_prd.md` -> `app/pages/_10_dashboard/iqm_quality_trend_analysis/prd_iqm_quality_trend_analysis.md`
  - `app/pages/_10_dashboard/iqm_quality_trend_analysis_analysis_results.md` -> `app/pages/_10_dashboard/iqm_quality_trend_analysis/page_iqm_quality_trend_analysis_results.md`
- Test Files:
  - `tests/test_iqm_trend_page.py`
  - `tests/test_iqm_trend_rank_echart.py`

**Interfaces:**
- Consumes: `app.service.iqm_service`
- Produces: `app.pages._10_dashboard.iqm_quality_trend_analysis.page_iqm_quality_trend_analysis`

- [ ] **Step 1: Move files into the new `iqm_quality_trend_analysis` folder**
- [ ] **Step 2: Create `renderer_iqm_quality_trend_analysis.py` and move helpers**
  Move helper functions (`show_scrap_table_dialog`, `show_rework_table_dialog`, `style_trend_table`, `get_latest_active_period`, etc.) into the new `renderer_iqm_quality_trend_analysis.py` to keep the main page script focused and under 1000 lines.
- [ ] **Step 3: Update page script and imports**
  In `page_iqm_quality_trend_analysis.py`, import plot functions from `.plots_iqm_quality_trend_analysis` and rendering helpers from `.renderer_iqm_quality_trend_analysis`.
- [ ] **Step 4: Update unit test imports**
  - Update `tests/test_iqm_trend_page.py` and `tests/test_iqm_trend_rank_echart.py` to reference the new paths.
- [ ] **Step 5: Run tests to verify correctness**
  Run: `pytest tests/test_iqm_trend_page.py tests/test_iqm_trend_rank_echart.py -v`
  Expected: PASS
- [ ] **Step 6: Commit changes**
  ```bash
  git add app/pages/_10_dashboard/iqm_quality_trend_analysis tests/test_iqm_trend_page.py tests/test_iqm_trend_rank_echart.py
  git commit -m "refactor: migrate and split IQM Quality Trend Analysis page"
  ```

---

### Task 4: Reorganize and Migrate "IQM Monthly Report" Page

**Files:**
- Create Directory: `app/pages/_10_dashboard/iqm_monthly_report/`
- Move & Rename Files:
  - `app/pages/_10_dashboard/iqm_monthly_report_page.py` -> `app/pages/_10_dashboard/iqm_monthly_report/page_iqm_monthly_report.py`
  - `app/pages/_10_dashboard/iqm_monthly_report_plots.py` -> `app/pages/_10_dashboard/iqm_monthly_report/plots_iqm_monthly_report.py`
  - `app/pages/_10_dashboard/iqm_monthly_report_prd.md` -> `app/pages/_10_dashboard/iqm_monthly_report/prd_iqm_monthly_report.md`
- Test Files:
  - `tests/test_iqm_monthly_report.py`

**Interfaces:**
- Consumes: `app.service.iqm_monthly_report_service`
- Produces: `app.pages._10_dashboard.iqm_monthly_report.page_iqm_monthly_report`

- [ ] **Step 1: Move files into the `iqm_monthly_report` directory**
- [ ] **Step 2: Update internal page imports**
  In `page_iqm_monthly_report.py`:
  ```python
  from app.pages._10_dashboard.iqm_monthly_report import plots_iqm_monthly_report as viz
  ```
- [ ] **Step 3: Update unit test imports**
  Update `tests/test_iqm_monthly_report.py` to import from the new path.
- [ ] **Step 4: Run unit tests to verify correctness**
  Run: `pytest tests/test_iqm_monthly_report.py -v`
  Expected: PASS
- [ ] **Step 5: Commit changes**
  ```bash
  git add app/pages/_10_dashboard/iqm_monthly_report tests/test_iqm_monthly_report.py
  git commit -m "refactor: migrate IQM Monthly Report page to page-specific folder"
  ```

---

### Task 5: Reorganize and Migrate "TP OE Monitoring" Page

**Files:**
- Create Directory: `app/pages/_10_dashboard/tp_oe_monitoring/`
- Move & Rename Files:
  - `app/pages/_10_dashboard/tp_oe_monitoring_page.py` -> `app/pages/_10_dashboard/tp_oe_monitoring/page_tp_oe_monitoring.py`
  - `app/pages/_10_dashboard/tp_oe_monitoring_plots.py` -> `app/pages/_10_dashboard/tp_oe_monitoring/plots_tp_oe_monitoring.py`
  - `app/pages/_10_dashboard/tp_oe_monitoring_prd.md` -> `app/pages/_10_dashboard/tp_oe_monitoring/prd_tp_oe_monitoring.md`
- Test Files:
  - `tests/test_tp_oe_monitoring.py`
  - `tests/test_tp_oe_monitoring_plots.py`

**Interfaces:**
- Consumes: `app.service.tp_oe_monitoring_service`
- Produces: `app.pages._10_dashboard.tp_oe_monitoring.page_tp_oe_monitoring`

- [ ] **Step 1: Move files into the `tp_oe_monitoring` directory**
- [ ] **Step 2: Update internal page imports**
  In `page_tp_oe_monitoring.py`:
  ```python
  from app.pages._10_dashboard.tp_oe_monitoring import plots_tp_oe_monitoring as viz
  ```
- [ ] **Step 3: Update unit test imports**
  Update `tests/test_tp_oe_monitoring.py` and `tests/test_tp_oe_monitoring_plots.py` to use the new paths.
- [ ] **Step 4: Run unit tests to verify correctness**
  Run: `pytest tests/test_tp_oe_monitoring.py tests/test_tp_oe_monitoring_plots.py -v`
  Expected: PASS
- [ ] **Step 5: Commit changes**
  ```bash
  git add app/pages/_10_dashboard/tp_oe_monitoring tests/test_tp_oe_monitoring.py tests/test_tp_oe_monitoring_plots.py
  git commit -m "refactor: migrate TP OE Monitoring page to page-specific folder"
  ```

---

### Task 6: Update Global Routing and Navigation Configurations

**Files:**
- Modify: `app/core/infrastructure/routing.py`
- Test Files: All updated unit tests

**Interfaces:**
- Consumes: None (Updates system configuration)
- Produces: `app.core.infrastructure.routing.PAGE_CONFIGS`

- [ ] **Step 1: Update PAGE_CONFIGS mapping inside `routing.py`**
  Modify file paths to reflect the new directory structure:
  ```python
  PAGE_CONFIGS = {
      # Dashboard
      "OE Quality Dashboard": {
          "filename": "app/pages/_10_dashboard/oe_quality_dashboard/page_oe_quality_issue_dashboard.py",
          "icon": ":material/dashboard:",
          "category": "Dashboard",
          "roles": ["Viewer", "Contributor", "Admin"],
      },
      "IQM Plus Overview": {
          "filename": "app/pages/_10_dashboard/iqm_plus_main/page_iqm_plus_main.py",
          "icon": ":material/science:",
          "category": "Dashboard",
          "roles": ["Viewer", "Contributor", "Admin"],
      },
      "IQM Plus Overview Dev": {
          "filename": "app/pages/_10_dashboard/iqm_plus_main/page_iqm_plus_main_dev.py",
          "icon": ":material/science:",
          "category": "Dashboard",
          "roles": ["Admin"],
      },
      "IQM Monthly Report": {
          "filename": "app/pages/_10_dashboard/iqm_monthly_report/page_iqm_monthly_report.py",
          "icon": ":material/analytics:",
          "category": "Dashboard",
          "roles": ["Admin"],
      },
      "TP OE Monitoring": {
          "filename": "app/pages/_10_dashboard/tp_oe_monitoring/page_tp_oe_monitoring.py",
          "icon": ":material/monitor_heart:",
          "category": "Dashboard",
          "roles": ["Contributor", "Admin"],
      },
      ...
      "IQM Quality Trend Analysis": {
          "filename": "app/pages/_10_dashboard/iqm_quality_trend_analysis/page_iqm_quality_trend_analysis.py",
          "icon": ":material/trending_up:",
          "category": "Dashboard",
          "roles": ["Contributor","Admin"],
      },
  }
  ```
- [ ] **Step 2: Run all workspace page and navigation tests**
  Run: `pytest tests/ -v` to ensure no regressions or import breakages.
- [ ] **Step 3: Update `graphify` 지식 그래프**
  Explain and run: `graphify update .` to update the AST indexes.
- [ ] **Step 4: Commit changes**
  ```bash
  git add app/core/infrastructure/routing.py
  git commit -m "refactor: update routing configuration paths for dashboard pages"
  ```
