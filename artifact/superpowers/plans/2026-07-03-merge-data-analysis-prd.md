# Merge Data Analysis PRD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `app/pages/_20_analysis/data_analysis_prd.md`와 `data_analysis_plots_prd.md` 파일을 하나로 흡수 통합하여 단일 PRD로 만들고 레거시 개별 파일을 깔끔하게 정리합니다.

**Architecture:** 대시보드 시각화 테마(Grayscale 95% + Anomaly Orange Accent 5%) 개요를 전면에 배치하고, 데이터 원천(Data Sources), 화면 레이아웃(Page Layout), 컴포넌트 및 탭별 플롯 시각화 스펙(Plot Specifications by Tab), 비즈니스 계산 수식 및 임계치 룰(Business Logic), 마지막으로 품질 및 검증(Verification & Gates) 구조를 단일 문서 내에 계층화하여 완성합니다.

**Tech Stack:** Markdown (No Emojis, WSL-Relative Links)

## Global Constraints

- Streamlit UI, 마크다운 문서, 소스 코드 주석 등 어떠한 곳에서도 일반 유니코드 이모지(별, 느낌표, 전구 등)를 절대 사용할 수 없습니다.
- 모든 파일 하이퍼링크는 반드시 프로토콜을 제외하고 워크스페이스 루트 기준의 평문 상대 경로(예: `app/pages/_20_analysis/data_analysis_prd.md`)만을 사용하여 작성해야 합니다.
- 이 문서 및 생성되는 통합 PRD 내의 모든 설명과 주석은 한국어(Korean) 작성을 기본 원칙으로 합니다.

---

## Task 1: 통합 PRD 초안 설계 및 작성

**Files:**
- Modify: `app/pages/_20_analysis/data_analysis_prd.md`
- Reference: `app/pages/_20_analysis/data_analysis_plots_prd.md`

**Interfaces:**
- Consumes: `app/pages/_20_analysis/data_analysis_prd.md` 및 `app/pages/_20_analysis/data_analysis_plots_prd.md` 원본 파일 내용
- Produces: `app/pages/_20_analysis/data_analysis_prd.md` (통합된 최종 PRD)

- [ ] **Step 1: 통합 PRD 본문 작성**
  - 두 파일의 내용을 논리적 흐름에 맞춰 병합합니다.
  - 배색 원칙(Shadcn UI 스타일 Grayscale 95% + Anomaly Orange Accent 5%)을 최상단 "SECTION 1. Background & Goals"에 위치시키고, 그 뒤로 데이터 소스, 레이아웃, 플롯 세부 스펙(Top 3 메트릭 카드 및 탭별 플롯 규격), 비즈니스 수식, 최종 품질 검증 게이트를 순차 계층으로 병합합니다.
  - 본문 작성 중 유니코드 이모지가 포함되지 않도록 원본의 불필요한 장식 이모지를 완전 배제합니다.
  - 마크다운 파일 링크는 워크스페이스 상대 경로 형식을 준수합니다. (예: `[data_analysis_page.py](app/pages/_20_analysis/data_analysis_page.py)`)

- [ ] **Step 2: 로컬 품질 검증 수행**
  - 생성된 통합 PRD 파일에 유니코드 이모지가 남아있는지 텍스트 검색을 통해 검증합니다.
  - 마크다운 렌더링에 문제가 없는지 구조적 결합도를 확인합니다.

- [ ] **Step 3: 형상 관리 반영 (임시 커밋)**
  - `git add app/pages/_20_analysis/data_analysis_prd.md`
  - `git commit -m "docs: merge data_analysis_plots_prd into data_analysis_prd"`

---

## Task 2: 레거시 개별 plots prd 제거 및 최종 정리

**Files:**
- Modify/Delete: `app/pages/_20_analysis/data_analysis_plots_prd.md`

**Interfaces:**
- Consumes: Task 1에서 완결된 통합 PRD (`app/pages/_20_analysis/data_analysis_prd.md`)
- Produces: `app/pages/_20_analysis/data_analysis_plots_prd.md` 삭제 상태 반영 및 최종 릴리즈 준비

- [ ] **Step 1: 개별 plots prd 파일 물리적 삭제**
  - `data_analysis_plots_prd.md` 파일이 정상적으로 `data_analysis_prd.md`에 전량 흡수 통합되었음을 재확인한 뒤, 해당 파일을 삭제합니다.
  - Command: `rm app/pages/_20_analysis/data_analysis_plots_prd.md`

- [ ] **Step 2: Git 파일 삭제 반영 및 최종 커밋**
  - Git 트래킹 상에서 삭제를 반영하고, 최종 상태를 정리합니다.
  - Command:
    ```bash
    git rm app/pages/_20_analysis/data_analysis_plots_prd.md
    git add app/pages/_20_analysis/data_analysis_prd.md
    git commit -m "docs: remove legacy data_analysis_plots_prd after unified consolidation"
    ```
