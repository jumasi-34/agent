---
id: skill.agent_hooks.ncf_metrics_revamp_plan
type: reference
status: active

summary: >
  Ncf Metrics Revamp Plan 참조 및 가이드 명세서.

parent: "[[skills/agent_hooks/SKILL.md]]"

updated: 2026-06-28
---

# NCF Metrics Layout and Styling Revamp Implementation Plan

* **Parent (상위 스킬)**: [[skills/agent_hooks/SKILL.md]]

---


> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor NCF tab metric cards to eliminate Streamlit's auto-generated hover anchor links, prevent PPM text-wrapping via custom CSS, consolidate Top 1, 2, and 3 defects into a single, unified metric card with Defect Codes highlighted and explanations underneath, and enlarge the unified card.

**Architecture:** We will replace the default `metric_card_vertical` calls in `_render_tab_ncf` of `data_analysis_page.py` with custom HTML blocks using standard `div` elements styled with identical CSS classes to bypass Streamlit's markdown header anchor tag injection. The layout ratio is modified from `6-column` to `[1, 1, 1, 3]`.

**Tech Stack:** Python, Streamlit, HTML/CSS.

## Global Constraints

- **Safety Lock**: Do not touch unrelated files or production code except `data_analysis_page.py` and `data_analysis_prd.md`.
- **No Unicode Emojis**: Never use any unicode emojis in code, comments, or UI texts. Use `:material/icon_name:` if icons are needed.
- **WSL Relative Links**: Use protocol-less workspace relative links in all markdown files.

---

### Task 1: Update PRD Specification
**Files:**
- Modify: `docs/prd/data_analysis_prd.md`

- [ ] **Step 1: Update SECTION 2 and SECTION 3 in data_analysis_prd.md**
  Reflect the new `[1, 1, 1, 3]` column ratio representing Production, NCF Qty, PPM, and the unified Top 3 defect card.

---

### Task 2: Implement Metric HTML Helpers and Refactor NCF Tab Metrics
**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_page.py:500-580`

- [ ] **Step 1: Code replacement for NCF Metrics Rendering**
  Write custom HTML helper logic inside `_render_tab_ncf` (or as a private helper inside the same file) that wraps card items in `<div class="shadcn-metric-card shadcn-metric-card-vertical shadcn-metric-card-gradient">` but replaces `<h3>` and `<h2>` with plain `<div>` elements. Compress the PPM value font-size to `1.45rem !important`.
  Combine 1st, 2nd, and 3rd defects into a flexbox container within a single card.
  Change the column instantiation to `st.columns([1, 1, 1, 3])`.

- [ ] **Step 2: Run verification**
  Verify the script compiles and conforms to codebase standards.
  Run: `python -m py_compile app/pages/_20_analysis/data_analysis_page.py`
  Expected: Successful compilation without errors.

- [ ] **Step 3: Run verify_code.py**
  Run: `python tests/verify_code.py`
  Expected: PASS

---
