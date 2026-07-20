---
id: map.agent_contracts
title: "Level 2: 에이전트 입출력 계약 및 연결 사양서"
type: wiki
status: active

summary: >
  [Level 2: Contract Specification]
  Agent OS 내 12대 고성능 에이전트의 구체적인 입력(Inputs), 출력(Outputs), 금지사항(Non-Responsibilities) 및 에이전트 간 순차 연결 계약 프로토콜 명세서입니다.

keywords:
  - agent-contracts
  - interfaces
  - api-specs
  - connection-rules

parent: "[01_agent_governance_constitution.md](01_agent_governance_constitution.md) (Level 1: 거버넌스 설계 헌법)"

related:
  - "[01_agent_governance_constitution.md](01_agent_governance_constitution.md) (Level 1: 거버넌스 설계 헌법)"
  - "[agents_registry.json](agents_registry.json)"

updated: 2026-07-20
---

# 에이전트 입출력 계약 및 연결 사양서 (Level 2: Contract Specification)

## 1. 목적 (Purpose)
본 문서는 상위 설계 헌법서([01_agent_governance_constitution.md](01_agent_governance_constitution.md))를 보완하여, 12대 에이전트들의 **데이터 입출력 계약(Contract)**, **협업 체인(Chaining)**, 그리고 **문서 작성 템플릿 규격**을 엄격하게 명세하는 API 수준의 기술 사양서(SSOT)입니다.

---

## 2. 공통 Agent Contract 템플릿 규격
모든 에이전트의 역할 명세서(`.md`)는 예외 없이 다음의 `Frontmatter`와 `Body` 표준 구조를 준수해야 합니다.

### 2.1 Frontmatter (YAML)
파일 최상단의 YAML Frontmatter 헤더에 다음 필드들을 명시합니다.
* **name**: 에이전트의 고유 식별 명칭 (예: `product-agent`)
* **description**: 에이전트의 역할 및 핵심 목적 요약
* **version**: 에이전트 사양의 버전 (예: `1.0.0`)
* **inputs**: 작업을 수행하는 데 필요한 필수 입력 목록 (예: `user_request`, `project_conventions`)
* **outputs**: 생산하는 핵심 산출물 목록 (예: `prd`)
* **collaborates_with**: 협업하는 관련 에이전트 목록
* **skills**: 에이전트에 매핑되거나 활성화되는 스킬 목록

### 2.2 Body (본문)
Frontmatter 아래의 마크다운 본문은 다음 구조화된 섹션들로 구성됩니다.
1. **Overview**: 에이전트가 존재하는 이유와 비즈니스/기능적 핵심 가치 요약
2. **Responsibilities**: 완수해야 하는 상세 책임 목록과 하지 말아야 할 작업(Non-Responsibilities) 및 가이드라인
3. **Inputs**: 수행에 필요한 개별 입력 항목들의 세부 사양과 소스(출처) 정의
4. **Outputs**: 최종적으로 생성/갱신해야 하는 구체적인 결과물의 포맷과 저장 경로 규칙
5. **Collaborates With**: 워크플로우 상 전/후에 연계되는 에이전트들과의 협업 흐름(`Receives From` 및 `Sends To`)
6. **Skills**: 임무를 고도화하거나 자동화하기 위해 매핑/활성화되는 전문 기능(Skills) 및 역량

---

## 3. 에이전트 입출력 및 연결 계약 총괄표
기존의 불필요한 서술형 명세를 폐기하고, 각 에이전트의 구체적인 책임 한계와 입/출력, 그리고 다음 연결 대상(Sends To)을 직관적인 표로 압축하여 명세합니다.

| 에이전트 | 핵심 책임 및 금지사항 (Responsibility & Non-Responsibility) | 주요 입력 (Inputs) | 주요 출력 (Outputs) | 연결 대상 (Sends To) |
| :--- | :--- | :--- | :--- | :--- |
| **router-agent** | 오케스트레이션 파이프라인 수립 (비즈니스 상세 기획 금지) | `user_request` | `orchestration_pipeline` | `product-agent` |
| **product-agent** | 요구사항(PRD) 및 완료 기준 수립 (코드 작성 금지) | `user_request`, `project_conventions` | `prd` | `architecture-agent`, `design-agent` |
| **architecture-agent** | 3-Layer 경계 및 데이터 스키마 설계 (UI 구현 금지) | `prd`, `system_architecture_standards` | `architecture_design` | `analysis-agent`, `engineering-agent` |
| **analysis-agent** | 도메인 통계 및 성능/병목 사전 진단 (데이터 변조 금지) | `architecture_design`, `metrics_telemetry` | `analysis_report` | `design-agent` |
| **design-agent** | 디자인 규칙 및 컴포넌트 재사용성 가이드 (백엔드 로직 금지) | `prd`, `design_system_standards` | `design_guide_compliance` | `engineering-agent` |
| **engineering-agent** | Python, SQL 개발 및 백엔드 로직 구현 (UI 세션 처리 금지) | `prd`, `architecture_design`, `coding_standards` | `queries_modules`, `service_modules` | `ui-agent` |
| **ui-agent** | Streamlit 화면 렌더링 및 세션 상태 조립 (무거운 전처리 코딩 금지) | `queries_modules`, `service_modules`, `ui_standards` | `streamlit_pages` | `quality-agent` |
| **quality-agent** | 코드 스타일 리뷰 및 mock 격리 테스트 (운영 DB 파괴 테스트 금지) | `changed_files`, `test_specs`, `prd` | `review_report`, `evaluation_scorecard` | `release-agent`, `documentation-agent` |
| **release-agent** | 배포 변경 이력 요약 및 릴리스 체크리스트 점검 (강제 푸시 금지) | `changed_files`, `evaluation_scorecard` | `release_note` | `documentation-agent` |
| **documentation-agent** | 기술 사양서, API 명세, 다이어그램 영속화 (실행 코드 작성 금지) | `prd`, `architecture_design`, `evaluation_scorecard` | `documentation_assets` | `knowledge-base` |
| **prompt-agent** | 에이전트 행동 지침 프롬프트 최적화 (비즈니스 로직 개입 금지) | `agents_registry` | `optimized_prompts` | - |
| **knowledge-base** | 주요 설계 가치(Decisions, Patterns) 수확 및 보존 (무분별한 전파 금지) | `documentation_assets` | `decisions_patterns_incidents` | - |

---

## 4. 예외 및 완료 규칙 (Failure & Completion Rules)

* **예외 처리 (Failure Handling)**
  * 입력이 부족하거나 요구사항이 불명확한 경우, 에이전트는 작업을 임의로 추측하지 않습니다.
  * 누락된 입력을 명시하거나 위험도를 기록하여 다음 에이전트(또는 Reviewer)에게 전달합니다.
  * 중대한 구조적/기획적 결함 발견 시, 각각 `Architecture Agent` 또는 `Product Agent`로 작업을 반송합니다.
* **작업 완료 기준 (Completion Criteria)**
  * 할당된 입력을 명확히 사용하고 자신의 책임 범위를 벗어나지 않아야 합니다.
  * 다음 에이전트가 즉시 사용할 수 있는 형태의 유효한 산출물(Outputs)을 명확하게 반환할 때 이터레이션이 완료된 것으로 간주합니다.
