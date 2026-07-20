# Design System Reorganization (Approach B) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize `app/core/design_system/` by decomposing legacy giant blob files (`streamlit_widgets.py`, `css_injector.py`), separating Plotly into `plotly/`, dedicating a subpackage to ECharts (`echarts/`), and migrating all imports workspace-wide to achieve standard design system separation of concerns (Approach B).

**Architecture:** We use clean, dedicated subpackages for each design system concern: `tokens/` (tokens), `styles/` (raw CSS & loading engine), `components/` (HTML & custom Streamlit widgets), `plotly/` (Plotly charts), `echarts/` (ECharts charts), and `utils/` (column config, error boundary).

**Tech Stack:** Python 3.12, Streamlit, Plotly, ECharts, Pytest

## Global Constraints
- **Safety Lock:** No production code outside the plan may be modified without explicit consent.
- **No Emojis:** Use Google Material symbols (`:material/icon_name:`) instead of emojis.
- **WSL Paths:** All links and file paths must use workspace-relative paths, no `file:///` protocols.
- **Zero Raw Styling:** Styles must be loaded from external CSS sheets using variables bound to Python tokens.

---

### Task 1: Setup ECharts Dedicated Subpackage

**Files:**
- Create: `app/core/design_system/echarts/__init__.py`
- Create: `app/core/design_system/echarts/theme.py`
- Move & Modify: `app/core/design_system/components/radar_chart.py` ➡️ `app/core/design_system/echarts/components/radar.py`
- Modify: `tests/test_radar_chart.py`
- Modify: `tests/test_echarts_load.py`

**Interfaces:**
- Consumes: Design system tokens `Colors` and `colors`.
- Produces: `render_radar_chart(labels, values, ...)` exposed under the `app.core.design_system.echarts` namespace.

- [ ] **Step 1.1: Create ECharts directories & initialization files**
  Create the folder structure:
  ```bash
  mkdir -p app/core/design_system/echarts/components
  ```
  Write the content of `app/core/design_system/echarts/__init__.py` to expose the radar component:
  ```python
  """app.core.design_system.echarts 패키지 엔트리포인트"""
  from app.core.design_system.echarts.components.radar import render_radar_chart

  __all__ = ["render_radar_chart"]
  ```

- [ ] **Step 1.2: Write empty theme file for ECharts**
  Create `app/core/design_system/echarts/theme.py` to hold ECharts global configurations matching the styling system:
  ```python
  """ECharts 글로벌 테마 및 스타일 설정 모듈"""
  from app.core.design_system.tokens import colors

  ECHARTS_TEXT_STYLE = {
      "color": colors.text_primary,
      "fontFamily": "Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
  }
  ```

- [ ] **Step 1.3: Move and adjust radar_chart to its new home**
  Move the file:
  ```bash
  mv app/core/design_system/components/radar_chart.py app/core/design_system/echarts/components/radar.py
  ```
  Edit `app/core/design_system/echarts/components/radar.py` to fix its imports:
  ```python
  # Change:
  # from app.core.design_system.tokens import colors
  # Keep it clean:
  from app.core.design_system.tokens import colors
  ```

- [ ] **Step 1.4: Update tests to point to the new ECharts namespace**
  Update `tests/test_radar_chart.py` to load `render_radar_chart` from `app.core.design_system.echarts`.
  ```python
  # Old:
  # from app.core.design_system.components.radar_chart import render_radar_chart
  # New:
  from app.core.design_system.echarts import render_radar_chart
  ```
  Update `tests/test_echarts_load.py` imports as well.

- [ ] **Step 1.5: Run ECharts tests to verify they pass**
  Run:
  ```bash
  pytest tests/test_radar_chart.py tests/test_echarts_load.py -v
  ```
  Expected: PASS

- [ ] **Step 1.6: Commit Task 1 changes**
  ```bash
  git add app/core/design_system/echarts tests/test_radar_chart.py tests/test_echarts_load.py
  git commit -m "refactor: migrate ECharts radar component to separate subpackage"
  ```

---

### Task 2: Modularize Common Components & Deconstruct `streamlit_widgets.py`

**Files:**
- Create: `app/core/design_system/components/headers.py`
- Create: `app/core/design_system/components/metrics.py` (overwriting the sparse existing one)
- Create: `app/core/design_system/components/tables.py`
- Create: `app/core/design_system/components/tabs.py`
- Modify: `app/core/design_system/components/__init__.py`
- Delete: `app/core/design_system/streamlit_widgets.py`
- Modify: `tests/test_streamlit_widgets.py`

**Interfaces:**
- Consumes: Design system tokens, styles injector.
- Produces: `section_header`, `render_premium_metric_card`, `render_metadata_card`, `data_table`, `shadcn_data_table`, `render_manual`, etc., under `app.core.design_system.components`.

- [ ] **Step 2.1: Extract headers widget logic**
  Create `app/core/design_system/components/headers.py` containing `section_header`, `HeaderPanelConfig`, `HEADER_CONFIGS`, `_build_header_icon_html`, and `_build_stats_html` extracted from `streamlit_widgets.py`. Ensure proper imports:
  ```python
  import streamlit as st
  from app.core.design_system.tokens import colors, spacing
  from app.core.design_system.styles.injector import CSSClasses
  ```

- [ ] **Step 2.2: Extract metrics widget logic**
  Overwrite `app/core/design_system/components/metrics.py` combining the sparse metric components and the metric cards from `streamlit_widgets.py` (`render_premium_metric_card`, `render_metadata_card`).

- [ ] **Step 2.3: Extract tables & manuals widget logic**
  Create `app/core/design_system/components/tables.py` containing `data_table`, `shadcn_data_table`, `render_manual`, `_escape_html`, and `_minify_html`.

- [ ] **Step 2.4: Extract tabs widget logic**
  Create `app/core/design_system/components/tabs.py` containing custom HTML-based interactive multi-tab switcher widget code.

- [ ] **Step 2.5: Update components init to act as the primary aggregator**
  Write `app/core/design_system/components/__init__.py` to aggregate and clean-export all widgets:
  ```python
  """app.core.design_system.components 패키지 엔트리포인트"""
  from app.core.design_system.components.headers import section_header
  from app.core.design_system.components.metrics import render_premium_metric_card, render_metadata_card
  from app.core.design_system.components.tables import data_table, shadcn_data_table, render_manual
  from app.core.design_system.components.tabs import render_custom_tabs # if applicable

  __all__ = [
      "section_header",
      "render_premium_metric_card",
      "render_metadata_card",
      "data_table",
      "shadcn_data_table",
      "render_manual",
  ]
  ```

- [ ] **Step 2.6: Delete legacy `streamlit_widgets.py`**
  ```bash
  rm app/core/design_system/streamlit_widgets.py
  ```

- [ ] **Step 2.7: Update widget tests and verify they pass**
  Update `tests/test_streamlit_widgets.py` imports:
  ```python
  # Old:
  # from app.core.design_system.streamlit_widgets import ...
  # New:
  from app.core.design_system.components import ...
  ```
  Run:
  ```bash
  pytest tests/test_streamlit_widgets.py -v
  ```
  Expected: PASS

- [ ] **Step 2.8: Commit Task 2 changes**
  ```bash
  git add app/core/design_system/components/ tests/test_streamlit_widgets.py
  git rm app/core/design_system/streamlit_widgets.py
  git commit -m "refactor: split streamlit_widgets.py into modular component files"
  ```

---

### Task 3: Extract CSS Rules & Deconstruct `css_injector.py`

**Files:**
- Create: `app/core/design_system/styles/raw/foundations.css`
- Create: `app/core/design_system/styles/raw/headers.css`
- Create: `app/core/design_system/styles/raw/metrics.css`
- Create: `app/core/design_system/styles/raw/tables.css`
- Create: `app/core/design_system/styles/raw/tabs.css`
- Create: `app/core/design_system/styles/injector.py`
- Create: `app/core/design_system/styles/__init__.py`
- Delete: `app/core/design_system/css_injector.py`

**Interfaces:**
- Consumes: Text read of raw `.css` files.
- Produces: `CSSClasses` constants, `load_css()`, `PREMIUM_MANUAL_CSS` under `app.core.design_system.styles`.

- [ ] **Step 3.1: Create styles directories & extract raw CSS rules**
  Create the folder:
  ```bash
  mkdir -p app/core/design_system/styles/raw
  ```
  Locate `PREMIUM_MANUAL_CSS` and other static CSS string blocks in `css_injector.py`. Split them cleanly and write them to:
  - `app/core/design_system/styles/raw/foundations.css`
  - `app/core/design_system/styles/raw/headers.css`
  - `app/core/design_system/styles/raw/metrics.css`
  - `app/core/design_system/styles/raw/tables.css`
  - `app/core/design_system/styles/raw/tabs.css`

- [ ] **Step 3.2: Implement lightweight `injector.py`**
  Write `app/core/design_system/styles/injector.py` to dynamically load these files using `pathlib` and inject them to Streamlit:
  ```python
  """Streamlit 공통 CSS 주입 엔진 모듈"""
  from pathlib import Path
  import streamlit as st

  class CSSClasses:
      # Copy over exact class strings from css_injector.py ...
      HEADER_PANEL = "shadcn-header-info-panel"
      # ...

  def load_css():
      """CSS 파일들을 병합하여 Streamlit 화면에 인젝션합니다."""
      styles_dir = Path(__file__).parent / "raw"
      css_content = []
      for css_file in styles_dir.glob("*.css"):
          css_content.append(css_file.read_text(encoding="utf-8"))
      
      full_css = "\n".join(css_content)
      st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)
  ```

- [ ] **Step 3.3: Expose injector styles in `__init__.py`**
  Write `app/core/design_system/styles/__init__.py`:
  ```python
  from app.core.design_system.styles.injector import CSSClasses, load_css

  __all__ = ["CSSClasses", "load_css"]
  ```

- [ ] **Step 3.4: Delete legacy `css_injector.py`**
  ```bash
  rm app/core/design_system/css_injector.py
  ```

- [ ] **Step 3.5: Commit Task 3 changes**
  ```bash
  git add app/core/design_system/styles/
  git rm app/core/design_system/css_injector.py
  git commit -m "refactor: extract raw styling from css_injector.py into pure CSS files"
  ```

---

### Task 4: Setup System Utilities Subpackage

**Files:**
- Create: `app/core/design_system/utils/__init__.py`
- Move & Modify: `app/core/design_system/error_handler.py` ➡️ `app/core/design_system/utils/error_handler.py`
- Move & Modify: `app/core/design_system/column_config.py` ➡️ `app/core/design_system/utils/column_config.py`
- Modify: `tests/test_error_boundary.py`

**Interfaces:**
- Consumes: SQLite logging dependencies, Streamlit.
- Produces: `error_boundary`, `boilerplate_column_config` under `app.core.design_system.utils`.

- [ ] **Step 4.1: Create utility directory**
  Create:
  ```bash
  mkdir -p app/core/design_system/utils
  ```

- [ ] **Step 4.2: Move and refactor utilities**
  Move the files:
  ```bash
  mv app/core/design_system/error_handler.py app/core/design_system/utils/error_handler.py
  mv app/core/design_system/column_config.py app/core/design_system/utils/column_config.py
  ```
  Create `app/core/design_system/utils/__init__.py` to aggregate them:
  ```python
  """app.core.design_system.utils 패키지 엔트리포인트"""
  from app.core.design_system.utils.error_handler import error_boundary
  from app.core.design_system.utils.column_config import BASIC_COLUMN_CONFIGS

  __all__ = ["error_boundary", "BASIC_COLUMN_CONFIGS"]
  ```

- [ ] **Step 4.3: Update error boundary test**
  Update `tests/test_error_boundary.py` imports to import from `app.core.design_system.utils`.
  Run:
  ```bash
  pytest tests/test_error_boundary.py -v
  ```
  Expected: PASS

- [ ] **Step 4.4: Commit Task 4 changes**
  ```bash
  git add app/core/design_system/utils/ tests/test_error_boundary.py
  git rm app/core/design_system/error_handler.py app/core/design_system/column_config.py
  git commit -m "refactor: relocate error boundary and column configs to utils"
  ```

---

### Task 5: Rename `plot` Folder to `plotly`

**Files:**
- Rename: `app/core/design_system/plot/` ➡️ `app/core/design_system/plotly/`
- Modify: All inner imports under `app/core/design_system/plotly/**/*.py`

**Interfaces:**
- Consumes: Plotly, design system tokens.
- Produces: Standard Plotly KPI charts under the `app.core.design_system.plotly` namespace.

- [ ] **Step 5.1: Perform physical directory renaming**
  Rename directory:
  ```bash
  mv app/core/design_system/plot app/core/design_system/plotly
  ```

- [ ] **Step 5.2: Update internal module imports to `plotly`**
  Search for all internal imports in the renamed directory (like `from app.core.design_system.plot...`) and replace them with `plotly`.
  For example, in `app/core/design_system/plotly/__init__.py`:
  ```python
  # Old: import app.core.design_system.plot.theme
  # New:
  import app.core.design_system.plotly.theme
  ```
  Do this systematically across all files under `app/core/design_system/plotly/` using targeted python scripts or search/replace.

- [ ] **Step 5.3: Commit Task 5 changes**
  ```bash
  git add app/core/design_system/plotly/
  git rm app/core/design_system/plot/
  git commit -m "refactor: rename plot folder to plotly for naming clarity"
  ```

---

### Task 6: Update Package Init and Forwarders

**Files:**
- Modify: `app/core/design_system/__init__.py`
- Delete: `app/core/design_system/tokens.py`

**Interfaces:**
- Exposes: Expose high-level entry points for clean backward compatibility where needed, or maintain direct importing.

- [ ] **Step 6.1: Clean up package init file**
  Update `app/core/design_system/__init__.py` to provide a clean default namespace:
  ```python
  """app.core.design_system 통합 디자인 시스템 패키지"""
  # We can expose key facades
  from app.core.design_system.tokens import colors
  from app.core.design_system.styles import load_css
  from app.core.design_system.utils import error_boundary

  __all__ = ["colors", "load_css", "error_boundary"]
  ```

- [ ] **Step 6.2: Remove tokens forwarder script**
  Since Approach B prefers direct explicit imports, remove the forwarder script:
  ```bash
  rm app/core/design_system/tokens.py
  ```

- [ ] **Step 6.3: Commit Task 6 changes**
  ```bash
  git add app/core/design_system/__init__.py
  git rm app/core/design_system/tokens.py
  git commit -m "refactor: clean up package level entries and remove forwarders"
  ```

---

### Task 7: Workspace-Wide Import Migration & Test Execution

**Files:**
- Modify: All files in `app/pages/**/*.py` and any services/queries calling the design system.
- Modify: All tests under `tests/**/*.py`.

**Interfaces:**
- Verification: Entire test suite passes without any import or runtime failures.

- [ ] **Step 7.1: Perform automated workspace-wide regex replacements**
  Replace old paths with new paths across `app/` and `tests/`:
  - `app.core.design_system.plot` ➡️ `app.core.design_system.plotly`
  - `app.core.design_system.streamlit_widgets` ➡️ `app.core.design_system.components`
  - `app.core.design_system.css_injector` ➡️ `app.core.design_system.styles`
  - `app.core.design_system.error_handler` ➡️ `app.core.design_system.utils`
  - `app.core.design_system.column_config` ➡️ `app.core.design_system.utils`
  - `app.core.design_system.components.radar_chart` ➡️ `app.core.design_system.echarts`

- [ ] **Step 7.2: Run entire test suite to verify full integration success**
  Run:
  ```bash
  pytest tests/ -v
  ```
  Expected: All tests PASS with 100% success.

- [ ] **Step 7.3: Commit and lock down the migration**
  ```bash
  git add app/ tests/
  git commit -m "refactor: complete workspace-wide import migration to new design system standard"
  ```
