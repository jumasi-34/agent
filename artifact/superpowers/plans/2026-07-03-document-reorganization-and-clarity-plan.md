# CQ-BI Agent OS Document Reorganization & Agent Role Boundary Clarification Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up the flat files (`00_` to `08_`) at the root of the `.agents` submodule into structured subdirectories (`philosophy/`, `router/`), update all internal relative links to prevent breakage, and establish clear, distinct agent boundaries for the 22-agent catalog.

**Architecture:** 
1. **Constitution Placement**: Keep `AGENTS.md` at the root of `.agents/` as the single entry point ("Supreme Constitution").
2. **Subfolder Reorganization**: Group documents into `.agents/philosophy/` (Core vision and roadmap) and `.agents/router/` (Routing logic and classification).
3. **Link Integrity Restoration**: Use a automated script to parse and update all relative markdown links in `.agents/agents/roles/*.md`, `.agents/agents/agents.md`, `.agents/agents/agents_registry.json`, and `.agents/agents/router-agent/` files.
4. **Agent Role Boundaries**: Clearly define role groups (Strategic, Business/Architectural, Builder, Quality/Governance) to prevent boundary overlapping.

**Tech Stack:** Python 3 (link-checking and path updates), Bash (git movements), Markdown (documentation).

## Global Constraints
- No unicode emoji anywhere in Streamlit screens, text assets, markdown files, buttons, or source comments. Use only Streamlit's `:material/icon_name:` syntax for icons.
- All file links must be WSL relative path format (no `file:///` protocol, relative to workspace root) to ensure VS Code Windows compatibility.
- Korean localization standard for all docstrings, comments, and agent specifications.
- Prohibit any modification of production files under `app/` and `app.py`. All changes must be strictly bounded inside the `.agents` submodule.

---

## Folder Reorganization Mapping

```
[.agents/] (Submodule Root)
├── AGENTS.md (Supreme Constitution - Remains at Root)
│
├── philosophy/ (New Directory)
│   ├── 00_vision.md (Moved from root)
│   ├── 01_principles.md (Moved from root)
│   ├── 02_project_charter.md (Moved from root)
│   ├── 03_roadmap.md (Moved from root)
│   └── 04_iteration_template.md (Moved from root)
│
└── router/ (New Directory)
    ├── 05_router_architecture.md (Moved from root)
    ├── 06_work_classification.md (Moved from root & renamed to lowercase)
    ├── 07_intent_analysis.md (Moved from root & renamed to lowercase)
    └── 08_routing_table.md (Moved from root & renamed to lowercase)
```

---

## Task 1: Physical Reorganization of Core Documents

**Files:**
- Modify: `.agents/` files (physical movement)
- Create: `.agents/philosophy/` (directory)
- Create: `.agents/router/` (directory)

**Interfaces:**
- Consumes: Raw `00_` to `08_` files at the root of `.agents/`
- Produces: Structured, clean folders with files cleanly tracked by Git

- [ ] **Step 1: Create subdirectories in `.agents` submodule**

Run in bash terminal:
```bash
mkdir -p /home/jumasi/workstation/.agents/philosophy
mkdir -p /home/jumasi/workstation/.agents/router
```

- [ ] **Step 2: Execute Git Move commands to transfer philosophy files**

Run:
```bash
cd /home/jumasi/workstation/.agents
git mv 00_vision.md philosophy/00_vision.md
git mv 01_principles.md philosophy/01_principles.md
git mv 02_project_charter.md philosophy/02_project_charter.md
git mv 03_roadmap.md philosophy/03_roadmap.md
git mv 04_iteration_template.md philosophy/04_iteration_template.md
```

- [ ] **Step 3: Execute Git Move commands to transfer and normalize router files**

Run:
```bash
git mv 05_router_architecture.md router/05_router_architecture.md
git mv 06_WORK_CLASSIFICATION.md router/06_work_classification.md
git mv 07_INTENT_ANALYSIS.md router/07_intent_analysis.md
git mv 08_ROUTING_TABLE.md router/08_routing_table.md
```

- [ ] **Step 4: Verify Git Status and file positions**

Run:
```bash
git status
```
Expected: Clean list of renamed files inside the submodule, ready for staging.

---

## Task 2: Automated Link Integrity Restoration

**Files:**
- Create: `/home/jumasi/workstation/.agents/scratch/restore_links.py` (Temporary link restoration script)
- Modify: All files under `.agents/agents/roles/*.md`, `.agents/agents/agents.md`, `.agents/agents/agents_registry.json`, and `.agents/agents/router-agent/`

**Interfaces:**
- Consumes: The newly reorganized physical directory layout.
- Produces: Corrected markdown files containing valid relative paths referencing `philosophy/*` and `router/*` instead of flat root paths.

- [ ] **Step 1: Write the python script `restore_links.py`**

Write the following script to `/home/jumasi/workstation/.agents/scratch/restore_links.py`:
```python
import os
import re

AGENTS_DIR = "/home/jumasi/workstation/.agents"

# Exact mapping from old relative links to new relative links
path_replacements = {
    r"00_vision.md": "philosophy/00_vision.md",
    r"01_principles.md": "philosophy/01_principles.md",
    r"02_project_charter.md": "philosophy/02_project_charter.md",
    r"03_roadmap.md": "philosophy/03_roadmap.md",
    r"04_iteration_template.md": "philosophy/04_iteration_template.md",
    r"05_router_architecture.md": "router/05_router_architecture.md",
    r"06_WORK_CLASSIFICATION.md": "router/06_work_classification.md",
    r"07_INTENT_ANALYSIS.md": "router/07_intent_analysis.md",
    r"08_ROUTING_TABLE.md": "router/08_routing_table.md",
}

def replace_links_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for old, new in path_replacements.items():
        # Handle cases where the path has some relative parent dots, e.g. ../00_vision.md -> ../philosophy/00_vision.md
        # Or ../../00_vision.md -> ../../philosophy/00_vision.md
        pattern = re.compile(r"(\.\./)*" + re.escape(old))
        def repl(match):
            dots = match.group(0).replace(old, "")
            return f"{dots}{new}"
        
        if pattern.search(content):
            content = pattern.sub(repl, content)
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Restored links in: {filepath}")

# Walk through all md and json files under .agents
for root, dirs, files in os.walk(AGENTS_DIR):
    # Skip git folder
    if ".git" in root:
        continue
    for file in files:
        if file.endswith((".md", ".json")):
            replace_links_in_file(os.path.join(root, file))
```

- [ ] **Step 2: Run link restoration script**

Run:
```bash
python3 /home/jumasi/workstation/.agents/scratch/restore_links.py
```
Expected: Output showing files edited (e.g. `agents.md`, `agents_registry.json`, `router-agent/agent.json`, various `roles/*.md` files).

- [ ] **Step 3: Clean up scratch script and commit changes**

Run:
```bash
rm /home/jumasi/workstation/.agents/scratch/restore_links.py
cd /home/jumasi/workstation/.agents
git add .
```

---

## Task 3: Clarify Agent Role Boundaries (SSOT)

To resolve any future overlap and friction between the 22 agents, we define four distinct governance tiers. This mapping will be permanently recorded inside `.agents/agents/agents.md`.

### 1. Strategic & Coordination Tier (전략 및 조율 레이어)
* **`router-agent`**: Request analysis, Work/Intent classification, dynamic minimal pipeline generation (lazy loading).
* **`planner-agent`**: Global requirements intake, high-level iteration plans, user-facing communication, and PRD life-cycle control.
* **`requirements-agent`**: Detailed functional/non-functional criteria mapping, DoD success thresholds.
* **`architecture-agent`**: High-level system architecture, component boundaries, 3-Layer separation guards.

### 2. Implementation Tier (구현 빌더 레이어)
* **`data-modeling-agent`**: Fact, Dimension, KPI formulas, raw storage schemas.
* **`data-agent`**: DB SQL query development, pandas service manipulation, cached datasets (`@st.cache_data`).
* **`page-builder-agent`**: Streamlit layout composition, theme CSS injections, session interception management. No raw data processing.
* **`component-agent`**: Plotly visualization formatting, interactive metric card designs.
* **`refactoring-agent`**: Dead code pruning, complexity reduction, 3-Layer extraction.
* **`automation-agent`**: Background cron schedules, mail systems, API webhooks.
* **`test-agent`**: Unit test cases, mock dataset structures (In-memory). No production file edits.

### 3. Analytics & Quality Tier (분석 및 정적 품질 레이어)
* **`insight-agent`**: Pre-development statistical analysis (EDA), anomaly alarms, domain reports.
* **`reviewer-agent`**: Static code syntax audits, style checks, security scanning.
* **`project-health-agent`**: Naming-convention audit compliance metrics, DB metadata sync.
* **`performance-agent`**: Streamlit Rerun counts, query profiling, caching validation reports.

### 4. Governance & Deployment Tier (거버넌스 및 배포 레이어)
* **`evaluator-agent`**: Unit/integration tests runner, scorecard grading (Pass/Fail gatekeeper).
* **`release-agent`**: Final deployment health checklists, release notes authoring.
* **`knowledge-curator-agent`**: Post-completion wiki harvesting, Graphify updates.
* **`documentation-agent`**: System manuals, ADRs, Swagger-like API docs.
* **`prompt-optimizer-agent`**: Automated agent prompt compression, run analyzer error feedbacks.

- [ ] **Step 1: Update `.agents/agents/agents.md` with Tier-based definitions**

Modify the intro text of [.agents/agents/agents.md](agents/agents/agents.md) to explain this 4-tier model.

- [ ] **Step 2: Stage and Update Graphify**

Run:
```bash
cd /home/jumasi/workstation/.agents
git add .
cd /home/jumasi/workstation
graphify update .
```
Expected: AST-based Knowledge graph refreshed with correct file paths and nodes.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-03-document-reorganization-and-clarity-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
