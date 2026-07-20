# Unify Icons and Fix TypeError Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unify all icon parameter names to `icon_name` across design system widgets, completely remove hardcoded icon colors in favor of parent text color inheritance (`currentColor` / `inherit`), and fix the `TypeError` inside `data_table`.

**Architecture:** We will implement kwargs interceptors in all target widgets inside `streamlit_widgets.py` to maintain backwards-compatibility with old pages (protecting old pages via Safety Lock). Then we will update `.shadcn-...-icon` CSS selectors in `css_injector.py` to use `inherit` as fallback instead of hardcoded colors, ensuring true minimalism.

**Tech Stack:** Python 3.12, Streamlit, Pytest, Vanilla CSS

## Global Constraints

- Safety Lock: Do not modify existing page files (under `app/pages/`) or `app.py`. Only modify files under `app/core/design_system/` and `tests/`.
- WSL Markdown Link Constraint: Use relative paths for markdown links. Never use `file:///`.
- Unicode Emojis: Strictly banned. Never use raw emojis in comments, docstrings, or UI code. Use Google Material Symbols if icons are needed.
- Docstrings: Use Google style docstrings in Korean for functions.

---

### Task 1: Write Failing Tests for Core Widgets (TDD Setup)

**Files:**
- Modify: `tests/test_streamlit_widgets.py`

**Interfaces:**
- Consumes: `app.core.design_system.streamlit_widgets.data_table`, `dashboard_header`, `stats_header`
- Produces: New unit test functions verifying the correct argument mapping, backwards compatibility, and expected HTML output structure.

- [ ] **Step 1: Write the failing tests**

  Let's add assertions to verify that `data_table`, `dashboard_header`, and `stats_header` can be safely invoked using legacy arguments (`title_icon`, `icon`, `icon_config`) and new unified argument (`icon_name`), and that they generate correct HTML layout without crashes.

- [ ] **Step 2: Run test to verify it fails**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: FAIL (specifically, `data_table` testing will trigger `TypeError: _process_icon_html() takes 2 positional arguments but 3 were given`)

- [ ] **Step 3: Commit TDD Setup**

  ```bash
  git add tests/test_streamlit_widgets.py
  git commit -m "test: add TDD failing tests for data_table and headers"
  ```

---

### Task 2: Fix data_table and shadcn_data_table

**Files:**
- Modify: `app/core/design_system/streamlit_widgets.py:1254-1337`, `app/core/design_system/streamlit_widgets.py:1402-1428`

**Interfaces:**
- Consumes: `_process_icon_html`
- Produces: `data_table` with `icon_name` parameter, legacy `title_icon` / `icon_config` mapping wrapper.

- [ ] **Step 1: Modify `data_table` and `shadcn_data_table` signatures and body**

  Change the parameters of `data_table` from `title_icon` to `icon_name` and add `**kwargs` interceptor. Remove `icon_config` from positional arguments of `_process_icon_html`.

- [ ] **Step 2: Run test to verify passes**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: FAIL on remaining tests (e.g. stats_header or dashboard_header colored SVG) or PASS if those weren't asserting strict colors yet.

- [ ] **Step 3: Commit changes**

  ```bash
  git add app/core/design_system/streamlit_widgets.py
  git commit -m "fix: resolve TypeError in data_table and unify to icon_name with kwargs compatibility"
  ```

---

### Task 3: Fix dashboard_header and stats_header

**Files:**
- Modify: `app/core/design_system/streamlit_widgets.py:527-606`, `app/core/design_system/streamlit_widgets.py:628-755`

**Interfaces:**
- Consumes: `get_svg_icon`, `_process_icon_html`
- Produces: Correctly color-inherited icons in headers, safe `**kwargs` interceptors.

- [ ] **Step 1: Update `dashboard_header` to intercept legacy icon args and pass "currentColor" to `get_svg_icon`**

- [ ] **Step 2: Update `stats_header` and `subheader_title_stats_panel` to intercept and clean all legacy icon args safely**

- [ ] **Step 3: Run test to verify passes**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: PASS

- [ ] **Step 4: Commit changes**

  ```bash
  git add app/core/design_system/streamlit_widgets.py
  git commit -m "refactor: update dashboard_header and stats_header icon color inheritance and kwargs"
  ```

---

### Task 4: Remove Hardcoded Icon Colors in css_injector.py

**Files:**
- Modify: `app/core/design_system/css_injector.py`

**Interfaces:**
- Consumes: None
- Produces: Standard CSS stylesheet injected to Streamlit, with icon styles utilizing `inherit` fallback.

- [ ] **Step 1: Replace hardcoded colors with `inherit` in 9 CSS rules**

  Locate all instances of `color: var(--icon-color, {colors.info});` (9 instances) and change them to `color: var(--icon-color, inherit);`.

- [ ] **Step 2: Run test to verify passes**

  Run: `pytest tests/test_streamlit_widgets.py -v`
  Expected: PASS

- [ ] **Step 3: Commit changes**

  ```bash
  git add app/core/design_system/css_injector.py
  git commit -m "style: remove hardcoded icon colors in css_injector in favor of inheritance"
  ```

---

### Task 5: Final Validation and Quality Gate

- [ ] **Step 1: Run comprehensive tests**

  Run: `pytest tests/ -v`

- [ ] **Step 2: Verification completion**

  We will execute a quick check on files to verify no unicode emojis were accidentally introduced and everything adheres to guidelines.
