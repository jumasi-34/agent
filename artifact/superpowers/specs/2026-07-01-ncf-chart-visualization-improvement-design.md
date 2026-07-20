# NCF Chart Visualization Improvement Design Specification

## Overview

Improve the NCF tab's bottom process factor PPM distribution subplots by dynamically adjusting the subplot widths in proportion to the number of bars on the X-axis, formatting bar labels to include thousands separators, and displaying the SOP elapsed duration as "D+N" format to restore the original compact 5-column metric card layout.

## Proposed Architecture

1. **Dynamic Subplot Width Apportionment:**
   - Scan each of the 4 process factor datasets (`BY_SPEC_REV`, `BY_BLDG_MC`, `BY_CURE_MC`, `BY_MOLD`) to compute the actual number of elements that will be rendered, capped at `TOP_N = 20`.
   - Apply a safety lower-bound limit of `3` to each weight to avoid excessively squeezed layout dimensions.
   - Supply the normalized column widths array `column_widths` to Plotly's `make_subplots`.

2. **Formatting Numbers with Thousands Separator:**
   - Modify the `texttemplate` field in `go.Bar` trace configuration from `"%{y:.0f}"` to `"%{y:,.0f}"` to enable native thousands separator support.

3. **Restore Metric Card Layout with D+N Format:**
   - Replace the long YYYY-MM-DD SOP date in the orange badge with a compact "D+N" format representing the exact number of days elapsed since the SOP date.
   - Calculate elapsed days using the current date and SOP date: `days = (today - sop_d).days`.
   - Reverting the badge content to a short string ("D+N") restores the natural compact width of the first metric card, ensuring the 5-column layout remains balanced and unbroken.

## Targeted Files

- `app/core/plot/components.py` (specifically `PremiumPpmByFactorPlot.render`)
- `app/pages/_20_analysis/data_analysis_page.py` (specifically `_render_tab_ncf` around lines 563-578)

## Verification Strategy

- Run the main test suite: `python tests/verify_code.py` to check for syntax and layer boundary violations.
- Verify that `data_analysis_page.py` imports and runs without regressions.
