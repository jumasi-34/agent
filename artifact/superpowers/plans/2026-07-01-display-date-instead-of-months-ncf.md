# NCF Tab Badge Display SOP Date Instead of Months Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Change the display value of the orange badge in the first metric card of the NCF tab from "months since SOP (M+N)" to the "exact SOP date (YYYY-MM-DD)".

**Architecture:** Modify the Streamlit page module `app/pages/_20_analysis/data_analysis_page.py` to assign the formatted SOP date string `sop_date_str` (or another custom text representing the date) to the badge element instead of `prod_period_str`.

**Tech Stack:** Python, Streamlit, Pandas

## Global Constraints

- Never use standard unicode emojis in code, comments, or any docstrings.
- Follow Korean docstring/comment guidelines: use Korean for docstrings and comments.
- Do not use absolute Linux paths inside documents or links; use relative paths like `app/pages/_20_analysis/data_analysis_page.py`.

---

### Task 1: Update NCF Tab Metric Card Badge in data_analysis_page.py

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page.py:563-578`

**Interfaces:**
- Consumes: `sop_date_str` formatted as 'YYYY-MM-DD'
- Produces: `badge_html` embedding `sop_date_str` instead of `prod_period_str`

- [ ] **Step 1: Locate and inspect the target file**

Ensure we have exact lines to modify inside `app/pages/_20_analysis/data_analysis_page.py`.

- [ ] **Step 2: Update the badge string assignment**

Modify the logic around line 575. Instead of embedding `prod_period_str`, we embed `sop_date_str` into the `badge_html`.
If `sop_date_str` is not empty or `-`, assign it to `badge_html`.

```python
    badge_html = ""
    if sop_date_str != "-":
        badge_html = f'<span class="ncf-period-badge">{sop_date_str}</span>'
```

- [ ] **Step 3: Run static code verification**

Execute the codebase static verifier to guarantee that the edited file passes linting and syntax validation.

Run: `python tests/verify_code.py`
Expected: PASS
