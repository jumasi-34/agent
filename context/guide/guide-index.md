---
id: guide.index
type: reference
status: active

summary: >
  guide/ 기술 지침 및 아키텍처 가이드라인 레이어의 로컬 규칙과 보유 파일 정보를 요약한다.

keywords:
  - guide
  - readme
  - architecture-guidelines
  - design-system

parent: concept.home

related:
  - "[[context/guide/3layer-development-process.md]]"
  - "[[context/guide/coding-templates.md]]"
  - "[[context/guide/common-column-metadata-design.md]]"
  - "[[context/guide/design-system-guide.md]]"
  - "[[context/guide/error-handling.md]]"
  - "[[context/guide/manual-setup.md]]"
  - "[[context/guide/menu-navigation-definition.md]]"
  - "[[context/guide/new_page_development_workflow.md]]"
  - "[[context/guide/page-template-standard.md]]"
  - "[[context/guide/plotly-style-guide.md]]"
  - "[[context/guide/plotly-workflow-template.md]]"
  - "[[context/guide/preprocessing-boundary.md]]"
  - "[[context/guide/testing-verification.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"
  - agent.ui_builder
  - agent.service_builder

updated: 2026-06-28
---


# guide/ 규정

## Overview
* **왜 존재하는가 (Why)**: `rules/`의 절대 제약 규정을 실제 코드 상에 어떻게 우아하게 구현하고 녹여낼 수 있는지 모범 사례와 디자인 시스템, 아키텍처 및 화면 템플릿 등의 가이드를 정립하기 위함입니다.
* **언제 사용하는가 (When)**: 대시보드 UI, 비즈니스 가공 서비스, SQL 쿼리층을 새로 구현하거나 고도화할 때, 디자인 시스템과 에러 처리 등을 참고하여 아키텍처 표준을 완수해야 할 때 참고합니다.
* **연계 실행 (Next Action)**: 구체적인 3레이어 구조 개발 프로세스 절차를 보려면 [guide.3layer_development_process](.agents/context/guide/3layer-development-process.md)를, 템플릿 코드를 보려면 [guide.coding_templates](.agents/context/guide/coding-templates.md)를 먼저 확인하십시오.

## Connections
* **상위 개념**: [AGENTS.md](.agents/AGENTS.md)
* **하위 자산**:
  - [.agents/context/guide/3layer-development-process.md](.agents/context/guide/3layer-development-process.md)
  - [.agents/context/guide/coding-templates.md](.agents/context/guide/coding-templates.md)
  - [.agents/context/guide/common-column-metadata-design.md](.agents/context/guide/common-column-metadata-design.md)
  - [.agents/context/guide/design-system-guide.md](.agents/context/guide/design-system-guide.md)
  - [.agents/context/guide/error-handling.md](.agents/context/guide/error-handling.md)
  - [.agents/context/guide/manual-setup.md](.agents/context/guide/manual-setup.md)
  - [.agents/context/guide/menu-navigation-definition.md](.agents/context/guide/menu-navigation-definition.md)
  - [.agents/context/guide/new_page_development_workflow.md](.agents/context/guide/new_page_development_workflow.md)
  - [.agents/context/guide/page-template-standard.md](.agents/context/guide/page-template-standard.md)
  - [.agents/context/guide/plotly-style-guide.md](.agents/context/guide/plotly-style-guide.md)
  - [.agents/context/guide/plotly-workflow-template.md](.agents/context/guide/plotly-workflow-template.md)
  - [.agents/context/guide/preprocessing-boundary.md](.agents/context/guide/preprocessing-boundary.md)
  - [.agents/context/guide/testing-verification.md](.agents/context/guide/testing-verification.md)

---

이 문서는 `.agents/context/guide/` (기술 지침 및 아키텍처 가이드라인 레이어) 고유의 로컬 규칙과 파일 정보를 신속히 인지하기 위한 마이크로 가이드라인입니다.

---

## 1. 로컬 핵심 제약 (Local Rules)

* **해설 및 방법론 전담 (Implementation How-to)**: 이 폴더는 `rules/`의 절대 제약 규정(Must/Shall)을 프로덕션 코드에 어떻게 구현하고 적용해야 하는지 구체적인 **모범 사례(Best Practices), 구현 절차, 아키텍처 및 화면 템플릿, 지침** 등을 상세히 다룹니다.
* **강제력 소유 금지 (No Mandate)**: 이 폴더의 마크다운들은 강제 룰을 제정하지 않으며, 제정된 대원칙을 올바르게 수행하기 위한 가이드 역할만 수행합니다. 절대 규정은 오직 `rules/`에만 위임하십시오.
* **정적 검증 로직 배제 (No Validation Code)**: 코드 정적 분석이나 린트, 스키마 검증기 등 실질적인 품질 검역 및 통제 룰 엔진은 본 폴더에 배치하지 않으며, 해당 기능은 반드시 `guardrail/`로 전향 배치하고 격리하십시오.

---

## 2. 활성 파일 목록 인덱스 (Active Files)

| 파일명 | 파일의 본질적 역할 및책임 (1줄 요약) |
| :--- | :
---
 |
| `3layer-development-process.md` | UI - 비즈니스 서비스 - SQL 쿼리가 분리된 3레이어 구조 개발 프로세스 절차 및 규격 지침 |
| `coding-templates.md` | 데이터프레임 가공 서비스, 쿼리 모듈, 시각화 plots 및 streamlit 화면 구현 표준 코드 템플릿 |
| `design-system-guide.md` | 프리미엄 테마 적용 및 Google Material Symbols 기반의 일관성 있는 웹 디자인 가이드라인 |
| `plotly-style-guide.md` | 세련된 시각화 연출과 사용자 툴팁 설정을 위한 Plotly 차트 레이아웃 구현 상세 가이드 |
| `plotly-workflow-template.md` | 사용자 요청에 대응하여 일관된 고품질 Plotly 시각화를 생성하기 위한 개발 프로세스 및 표준 함수 템플릿 |
| `preprocessing-boundary.md` | SQL 쿼리층(순수 영문 컬럼 반환)과 UI층(한글 별칭 및 configs 변환) 간의 데이터 전처리 및 명 맵핑 경계 수칙 |
| `error-handling.md` | 사용자 경험 및 에이전트 자율 분석 가독성을 고도화하기 위한 다중 레이어 통합 에러 처리 가이드 |
| `testing-verification.md` | 기능을 훼손하지 않는 인메모리 mocking 기법 기반의 독립 테스트 하네스 기획 및 검증 표준서 |
| `common-column-metadata-design.md` | 하드코딩을 배제하고 메타데이터로부터 UI 한글명 및 소수점 설정을 동적으로 주입받는 컬럼 configs 설계 가이드 |
| `manual-setup.md` | Oracle client 가동 환경, Miniconda 가상환경 구축 등 초동 온보딩을 위한 수동 설정 설명서 |
| `query_module_template.py` | 쿼리 빌더 및 동적 쿼리 필터 클래스를 활용하는 쿼리 모듈 구현용 표준 파이썬 템플릿 |
| `menu-navigation-definition.md` | CQ-BI 애플리케이션의 네비게이션 메뉴 구조와 카테고리 정의, 그리고 페이지 매핑 표준에 대한 지침 |
| `new_page_development_workflow.md` | Streamlit 기반 신규 화면 개발 시 준수해야 하는 계층별 표준 워크플로우 기술 가이드라인 |
| `page-template-standard.md` | 신규 Streamlit 페이지 개발 시 참고할 수 있는 표준 레이아웃 마크다운 템플릿 |
| `page_template_standard.py` | 3-Layer 아키텍처를 준수하여 구현된 표준 Streamlit 페이지 파이썬 코드 템플릿 |

---

## 3. 변경 이력 (Changelog)

* **2026-06-14**:
  * [REFACTOR] 100% 중복 및 레거시 자산인 `agent-common.md`, `current-workflow.md`를 전격 폐지(삭제)하고 `reverse-sync-prevention.md` 로그 문서를 `runs/` 디렉터리로 정상 이관 및 정리함에 따라 로컬 액티브 파일 인덱스 테이블 갱신 완료.
  * [REFACTOR] `guide/` 레이어 정의를 단순 코딩 가이드에서 범용 '기술 지침 및 아키텍처 가이드라인 레이어'로 격상하고, 강제력의 rules/ 위임 및 검증 로직 배제 수칙을 로컬 제약으로 명문화.
  * [Feat] 가이드 폴더 전용 `agents.md` 최초 비치.
