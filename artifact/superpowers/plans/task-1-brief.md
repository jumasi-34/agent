### Task 1: Update NCF Tab Metric Card Badge in data_analysis_page.py

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page.py`

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
