# Remove header_main_title_info_panel Legacy Function Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the deprecated legacy `header_main_title_info_panel` helper function entirely from `streamlit_widgets.py` and migrate all of its references across 24+ pages to call `page_header` directly.

**Architecture:** A lightweight python refactoring script will scan and replace imports and calls of `header_main_title_info_panel` with `page_header`. Afterward, the function declaration will be removed from `streamlit_widgets.py`.

**Tech Stack:** Python 3, Pytest, Git, Graphify

## Global Constraints

- No unicode emojis in code, comments, or docstrings (Only google material syntax `:material/icon_name:` is allowed).
- All file/markdown links must use flat relative workspace paths (no `file:///` or absolute linux paths).
- Docstrings and comments must be in clear and descriptive Korean.

---

### Task 1: Codebase Refactoring Script and Execution

**Files:**
- Create: `tests/scratch/refactor_header_main_title.py` (temporary scratch script)
- Modify: `app/core/design_system/streamlit_widgets.py`
- Test: `tests/test_streamlit_widgets.py`

**Interfaces:**
- Consumes: None
- Produces: Clean imports and direct calls to `page_header` on all 24+ pages, and the complete removal of `header_main_title_info_panel`.

- [ ] **Step 1: Write a refactoring script**
  Create `tests/scratch/refactor_header_main_title.py` to automate the text replacements across the workspace files.
  
  ```python
  # * [Refactoring - 레거시 헤더 함수 이관 자동화 스크립트]
  import pathlib

  def main():
      root = pathlib.Path("/home/jumasi/workstation")
      target_files = []
      
      # 1. 대상 파일 검색 (app/ 및 tests/ 하위의 모든 파이썬 파일)
      for path in root.glob("**/*.py"):
          if ".git" in path.parts or ".agents" in path.parts or ".agent-storage" in path.parts:
              continue
          target_files.append(path)

      modified_count = 0
      for path in target_files:
          content = path.read_text(encoding="utf-8")
          if "header_main_title_info_panel" in content:
              # 단순 문자열 및 가져오기 구문 교체
              new_content = content.replace("header_main_title_info_panel", "page_header")
              path.write_text(new_content, encoding="utf-8")
              print(f"[REPLACED] {path.relative_to(root)}")
              modified_count += 1

      print(f"Total files modified: {modified_count}")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 2: Run the refactoring script**
  Run: `PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python tests/scratch/refactor_header_main_title.py`
  Expected: Successful text replacement across 24+ python files.

- [ ] **Step 3: Remove the legacy function from `streamlit_widgets.py`**
  Modify `app/core/design_system/streamlit_widgets.py` to delete lines 528-560 (the entire `header_main_title_info_panel` function definition).

- [ ] **Step 4: Verify git diff and ensure no leftovers**
  Run: `git diff --name-only`
  Expected: All 24+ page files, `streamlit_widgets.py`, and any relevant test files should be modified.

- [ ] **Step 5: Run unit tests to verify**
  Run: `PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python -m pytest tests/test_streamlit_widgets.py`
  Expected: All tests pass.

- [ ] **Step 6: Commit**
  ```bash
  git add .
  git commit -m "refactor(widgets): remove legacy header_main_title_info_panel and migrate pages"
  ```

---

### Task 2: Verification and Graph Synchronization

**Files:**
- Modify: None
- Test: All workspace pages via `verify_code.py`

- [ ] **Step 1: Run compiler checks to guarantee zero import or syntax errors**
  Run: `PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python tests/verify_code.py`
  Expected: 258/258 PASSED with 100% success.

- [ ] **Step 2: Run link validator and quality checks**
  Run: `PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/tools/link_validator.py`
  Expected: Success or zero new broken links in our modified files.

- [ ] **Step 3: Update Graphify database**
  Run: `graphify update .`
  Expected: Graph database and reports rebuilt successfully.

- [ ] **Step 4: Commit and finalize**
  ```bash
  git commit -m "test(verify): complete compiler and graphify verification gates"
  ```
