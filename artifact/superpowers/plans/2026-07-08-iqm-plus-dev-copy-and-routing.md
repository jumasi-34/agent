# IQM Plus Dev Copy & Admin Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** IQM Plus 메인 대시보드 화면 및 플롯 모듈의 개발용 사본(`*_dev.py`)을 생성하고, 이를 어드민 권한 전용 라우팅으로 등록하여 안전하게 테스트 및 검증할 수 있는 독립 개발 환경을 구축합니다.

**Architecture:** 프로덕션 코드인 `app/pages/_10_dashboard/iqm_plus_main_page.py` 및 `iqm_plus_main_plots.py`를 복제하여 `*_dev.py`를 생성하고, `iqm_plus_main_page_dev.py` 내부에서 개발용 플롯 모듈인 `iqm_plus_main_plots_dev`를 로드하도록 임포트를 재배선합니다. 이후 `app/core/infrastructure/routing.py`의 라우팅 설정 맵에 어드민 권한(`roles: ["Admin"]`)으로 추가 등록합니다.

**Tech Stack:** Python, Streamlit, Routing System.

## Global Constraints

- **Safety Lock 준수**: 사용자의 명시적인 직접 승인을 받은 이후에만 실제 코드 생성 및 수정을 진행합니다. (계획 승인 단계 필수)
- **WSL Markdown Link Constraint 준수**: 모든 마크다운 링크 및 자산 주소는 프로토콜(`file:///`) 없이 워크스페이스 루트 기준의 평문 상대 경로만을 사용합니다.
- **UI 및 주석 내 이모지 전면 금지**: 신규 생성 및 수정되는 파일 내의 주석, 독스트링, 화면 마크다운 등 어떠한 곳에도 유니코드 이모지(예: 🌟, ⚠️, ✅ 등)를 절대 기입하지 않으며, 아이콘은 오직 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용합니다.
- **한국어 독스트링 원칙**: 새로 추가되거나 수정되는 코드 및 문서 내 모든 주석과 독스트링(Docstring)은 기본적으로 한국어(Korean)로 작성합니다.

---

### Task 1: IQM Plus 메인 대시보드 플롯 모듈 개발 사본 생성

**Files:**
- Create: `app/pages/_10_dashboard/iqm_plus_main_plots_dev.py`
- Test: `tests/test_routing_validation.py` (임시 검증)

**Interfaces:**
- Consumes: `app/pages/_10_dashboard/iqm_plus_main_plots.py` 원본 코드
- Produces: `app/pages/_10_dashboard/iqm_plus_main_plots_dev.py` 복제본 파일

- [ ] **Step 1: 플롯 원본 파일을 개발 사본 파일로 복사**

  터미널에서 `cp` 명령을 통해 원본 파일을 그대로 복사합니다.
  Run:
  ```bash
  cp app/pages/_10_dashboard/iqm_plus_main_plots.py app/pages/_10_dashboard/iqm_plus_main_plots_dev.py
  ```

- [ ] **Step 2: 파일 생성 결과 확인**

  복사된 파일이 올바르게 생성되었는지 확인합니다.
  Run:
  ```bash
  ls -lh app/pages/_10_dashboard/iqm_plus_main_plots_dev.py
  ```
  Expected: 파일 크기 및 생성 완료 정보 출력

- [ ] **Step 3: Commit**

  ```bash
  git add app/pages/_10_dashboard/iqm_plus_main_plots_dev.py
  git commit -m "feat: create dev copy for iqm plus main plots"
  ```

---

### Task 2: IQM Plus 메인 대시보드 페이지 컨트롤러 개발 사본 생성 및 재배선

**Files:**
- Create: `app/pages/_10_dashboard/iqm_plus_main_page_dev.py`
- Modify: `app/pages/_10_dashboard/iqm_plus_main_page_dev.py:28`

**Interfaces:**
- Consumes: `app/pages/_10_dashboard/iqm_plus_main_page.py` 원본 코드, `app/pages/_10_dashboard/iqm_plus_main_plots_dev.py`
- Produces: `app/pages/_10_dashboard/iqm_plus_main_page_dev.py` 복제본 파일 및 플롯 모듈 임포트 재배선 완료

- [ ] **Step 1: 대시보드 메인 페이지 원본 파일을 개발 사본 파일로 복사**

  터미널에서 `cp` 명령을 통해 원본 파일을 그대로 복사합니다.
  Run:
  ```bash
  cp app/pages/_10_dashboard/iqm_plus_main_page.py app/pages/_10_dashboard/iqm_plus_main_page_dev.py
  ```

- [ ] **Step 2: 개발 사본 내 플롯 모듈 임포트 구문 수정**

  `app/pages/_10_dashboard/iqm_plus_main_page_dev.py` 내부 28번째 줄 부근의 임포트 경로를 기존 `iqm_plus_main_plots`에서 새로 생성한 `iqm_plus_main_plots_dev`로 변경합니다.
  
  Target Content (Line 28 부근):
  ```python
  from app.pages._10_dashboard import iqm_plus_main_plots as viz
  ```
  
  Replacement Content:
  ```python
  from app.pages._10_dashboard import iqm_plus_main_plots_dev as viz
  ```

- [ ] **Step 3: 변경 내용 정밀 검증**

  수정된 부분의 코드 차이를 확인하여 정확히 재배선되었는지 확인합니다.
  Run:
  ```bash
  git diff app/pages/_10_dashboard/iqm_plus_main_page_dev.py
  ```
  Expected: `iqm_plus_main_plots_dev`로 올바르게 교체된 diff 확인

- [ ] **Step 4: Commit**

  ```bash
  git add app/pages/_10_dashboard/iqm_plus_main_page_dev.py
  git commit -m "feat: create dev copy for iqm plus main page and re-route import to plots_dev"
  ```

---

### Task 3: 어드민 전용 라우팅 등록 및 정합성 검증

**Files:**
- Modify: `app/core/infrastructure/routing.py:96-102`
- Test: `validate_all_configs` 기동을 통한 정적 라우팅 유효성 검사

**Interfaces:**
- Consumes: `app/pages/_10_dashboard/iqm_plus_main_page_dev.py` 파일의 실제 경로
- Produces: `PAGE_CONFIGS` 내에 어드민 접근 권한 전용 `"IQM Plus Overview Dev"` 키가 에러 없이 추가 반영 완료

- [ ] **Step 1: 라우팅 설정 파일에 개발용 페이지 추가**

  `app/core/infrastructure/routing.py` 파일의 `PAGE_CONFIGS` 내부 `"IQM Plus Overview"` 항목 하단에 `"IQM Plus Overview Dev"` 페이지를 추가합니다. 어드민 권한 전용으로 설정해야 하므로, `roles` 속성 값을 `["Admin"]`으로만 구성합니다. (이모지 전면 금지 규칙에 맞춰 `:material/science:` 구글 머티리얼 아이콘 구문을 사용합니다)

  Target Content (Line 96-101 부근):
  ```python
      "IQM Plus Overview": {
          "filename": "app/pages/_10_dashboard/iqm_plus_main_page.py",
          "icon": ":material/science:",
          "category": "Dashboard",
          "roles": ["Viewer", "Contributor", "Admin"],
      },
  ```

  Replacement Content:
  ```python
      "IQM Plus Overview": {
          "filename": "app/pages/_10_dashboard/iqm_plus_main_page.py",
          "icon": ":material/science:",
          "category": "Dashboard",
          "roles": ["Viewer", "Contributor", "Admin"],
      },
      "IQM Plus Overview Dev": {
          "filename": "app/pages/_10_dashboard/iqm_plus_main_page_dev.py",
          "icon": ":material/science:",
          "category": "Dashboard",
          "roles": ["Admin"],
      },
  ```

- [ ] **Step 2: 라우팅 정합성 자동 검증 스크립트 실행**

  `routing.py` 내의 `validate_all_configs()` 함수를 기동하여 새로 추가된 페이지의 파일 존재 여부, 유효 카테고리 여부, 권한 제약조건 유효성 등을 원스톱으로 정량 검증합니다.
  Run:
  ```bash
  python -c "from app.core.infrastructure.routing import validate_all_configs; validate_all_configs()"
  ```
  Expected: 오류 메시지 없이 프로세스가 정상 종료 (반환 코드 0)

- [ ] **Step 3: Commit**

  ```bash
  git add app/core/infrastructure/routing.py
  git commit -m "feat: register IQM Plus Overview Dev to routing with Admin role constraints"
  ```

- [ ] **Step 4: 최신 지식 그래프 빌드 갱신 (graphify)**

  프로덕션 소스 코드 및 라우팅 설정에 변경이 일어났으므로, 지식 그래프인 `graph.json` 정보가 정합하게 유지되도록 `graphify update`를 실행합니다.
  Run:
  ```bash
  graphify update .
  ```
  Expected: AST 기반의 정적 분석 갱신 성공 메시지 출력
