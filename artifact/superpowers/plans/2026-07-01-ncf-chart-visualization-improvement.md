# NCF Chart Visualization Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the PPM by factor chart subplot widths dynamically, apply thousands formatting, and restore the 5-column metric card layout by converting the orange badge display to "D+N" elapsed format.

**Architecture:** 
1. Modify `app/core/plot/components.py` (PremiumPpmByFactorPlot.render) for dynamic widths and thousands separator formatting. (DONE in Task 2)
2. Modify `app/pages/_20_analysis/data_analysis_page.py` to calculate exact elapsed days between today and the SOP date, formatting as "D+N", and binding it back to the orange badge.

**Tech Stack:** Python, Plotly, Pandas, Streamlit

## Global Constraints

- Never use standard unicode emojis in code, comments, or docstrings.
- Follow Korean docstring/comment guidelines: use Korean for docstrings and comments.
- Do not use absolute Linux paths inside documents or links; use relative paths.

---

### Task 1: Implement Dynamic Width and Thousands Separator Formatter in PremiumPpmByFactorPlot (DONE)

- Already completed in Task 2. See `.superpowers/sdd/progress.md` for historical traceability.

---

### Task 2: Implement D+N Badge and Restore Metric Card Layout

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page.py`

**Interfaces:**
- Consumes: `sop_date` (Timestamp / datetime) from 마스터 행 데이터
- Produces: `badge_html` embedding `D+N` duration string, restoring compact column layouts

- [ ] **Step 1: Compute elapsed days between SOP date and today**

Modify the date calculation section around lines 563-573. Instead of calculating months, calculate the difference in days.

```python
            # * [양산 기간 연산]
            if isinstance(sop_date, pd.Timestamp):
                sop_d = sop_date.date()
            elif isinstance(sop_date, datetime):
                sop_d = sop_date.date()
            else:
                sop_d = sop_date
                
            today = datetime.now().date()
            days = (today - sop_d).days
            prod_period_str = f"D+{days}" if days >= 0 else "D+0"
```

- [ ] **Step 2: Bind the computed D+N string to badge_html**

Bind `prod_period_str` to the `badge_html` if it is valid.

```python
    badge_html = ""
    if prod_period_str != "-":
        badge_html = f'<span class="ncf-period-badge">{prod_period_str}</span>'
```

- [ ] **Step 3: Run static code verification**

Execute the static verifier to guarantee that the edited file passes linting and syntax validation.

Run: `python tests/verify_code.py`
Expected: PASS

- [ ] **Step 4: Run unit tests**

Run existing unit tests to confirm that importing pages does not crash.

Run: `pytest tests/test_layer_boundary.py`
Expected: PASS

- [ ] **Step 5: Commit**

Commit changes to git.
```bash
git add app/pages/_20_analysis/data_analysis_page.py
git commit -m "feat(ncf): Display SOP elapsed duration as D+N and restore metric card layout"
```
