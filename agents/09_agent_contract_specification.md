# 09_AGENT_CONTRACT_SPECIFICATION.md

# Agent Contract Specification

## 목적

이 문서는 Router와 Agent가 서로 연결되기 위한 표준 계약을 정의한다.

Router는 Agent를 단순히 호출하지 않는다.

Router는 각 Agent에게 필요한 입력을 전달하고, Agent가 반환해야 하는 산출물을 기준으로 다음 Agent를 연결한다.

따라서 모든 Agent는 동일한 Contract 구조를 따라야 한다.

---

# 기본 원칙

모든 Agent는 다음 구조를 가진다.

```text
Input
↓
Responsibility
↓
Process
↓
Output
↓
Review Criteria
↓
Next Agent
```

Agent는 자신의 책임 범위만 수행한다.

Agent는 다른 Agent의 산출물을 임의로 수정하지 않는다.

필요한 경우 문제를 기록하고 다음 Agent 또는 Reviewer에게 전달한다.

---

# 공통 Agent Contract

모든 Agent 문서는 아래 항목을 반드시 포함한다.

## 1. Agent Name

Agent 이름

## 2. Purpose

이 Agent가 존재하는 이유

## 3. Responsibility

이 Agent가 담당하는 작업

## 4. Non-Responsibility

이 Agent가 하지 말아야 할 작업

## 5. Input

Agent가 작업을 수행하기 위해 필요한 입력

예시:

* user_request
* router_result
* requirements
* prd
* architecture
* data_model
* existing_component
* design_token
* rule_context

## 6. Output

Agent가 반드시 생성해야 하는 산출물

예시:

* prd.md
* architecture.md
* data_model.md
* implementation_plan.md
* review_report.md

## 7. Process

Agent가 작업을 수행하는 표준 절차

## 8. Decision Criteria

Agent가 판단할 때 사용하는 기준

## 9. Quality Criteria

산출물이 만족해야 하는 품질 기준

## 10. Connected Agents

이 Agent 앞뒤로 연결되는 Agent

## 11. Related Rules

이 Agent가 반드시 확인해야 하는 Rule

## 12. Failure Handling

입력이 부족하거나 충돌이 있을 때 처리 방식

## 13. Completion Checklist

작업 완료 전 확인해야 하는 체크리스트

---

# 표준 출력 형식

모든 Agent는 결과를 아래 구조로 반환한다.

```yaml
agent: ""
task_id: ""
status: "completed | blocked | needs_review"
summary: ""
inputs_used: []
outputs_created: []
decisions: []
risks: []
assumptions: []
next_recommended_agent: ""
review_required: true
```

---

# Agent 간 연결 원칙

## Requirements → Architecture

Requirements Agent는 PRD를 생성한다.

Architecture Agent는 PRD를 기반으로 구조를 설계한다.

Architecture Agent는 요구사항을 임의로 변경하지 않는다.

---

## Architecture → Data Modeling

Architecture Agent는 페이지 구조와 데이터 요구를 정의한다.

Data Modeling Agent는 이를 기반으로 Fact, Dimension, KPI, Metric, Aggregation을 설계한다.

---

## Data Modeling → Data Agent

Data Modeling Agent는 데이터 구조를 정의한다.

Data Agent는 SQL, pandas, 집계 로직을 구현한다.

---

## Component Librarian → Component Agent

Component Librarian은 기존 컴포넌트 재사용 가능성을 판단한다.

Component Agent는 필요한 경우에만 신규 컴포넌트를 구현한다.

---

## Design System → Page Builder

Design System Agent는 Token, Theme, Chart Palette 기준을 제공한다.

Page Builder는 해당 기준을 따라 페이지를 구현한다.

---

## Page Builder → Reviewer

Page Builder는 구현 결과와 변경 파일 목록을 전달한다.

Reviewer는 Rule 준수와 변경 범위를 검토한다.

---

## Reviewer → Evaluator

Reviewer는 규칙 준수 여부를 검토한다.

Evaluator는 결과가 요구사항과 성공 기준을 만족하는지 평가한다.

---

## Evaluator → Documentation

Evaluator가 완료를 승인하면 Documentation Agent가 변경사항과 사용법을 문서화한다.

---

# 핵심 Agent Contract 요약

## Router Agent

Input:

* user_request
* vision
* principles
* charter
* roadmap
* current_iteration
* agent_registry
* rules_index

Output:

* target
* required_context
* required_rules
* required_agents
* execution_order
* expected_outputs
* review_plan

Non-Responsibility:

* 분석 업무 (Work Classification, Intent Analysis 등)
* 코드 구현
* SQL 작성
* UI 개발

---

## Requirements Agent

Input:

* user_request
* router_result
* existing_pages
* business_context

Output:

* work_classification
* intent_analysis
* prd
* user_problem
* target_users
* success_criteria
* required_kpi
* required_data
* constraints
* open_questions

Non-Responsibility:

* 아키텍처 설계
* 코드 구현
* 데이터 쿼리 작성

---

## Architecture Agent

Input:

* prd
* router_result
* existing_structure
* existing_pages
* component_inventory

Output:

* page_architecture
* feature_architecture
* data_flow
* component_structure
* implementation_boundary
* architecture_risk

Non-Responsibility:

* 실제 구현
* SQL 작성
* 디자인 토큰 생성

---

## Data Modeling Agent

Input:

* prd
* architecture
* known_data_sources

Output:

* fact_definition
* dimension_definition
* metric_definition
* kpi_definition
* aggregation_strategy
* data_quality_risk

Non-Responsibility:

* 화면 구현
* 차트 구현

---

## Insight Agent

Input:

* prd
* data_model
* quality_context

Output:

* recommended_kpi
* analysis_viewpoints
* comparison_logic
* anomaly_detection_idea
* drilldown_plan

Non-Responsibility:

* SQL 구현
* UI 구현

---

## Component Librarian Agent

Input:

* prd
* architecture
* component_inventory
* design_system

Output:

* reusable_components
* missing_components
* duplication_risk
* component_reuse_plan

Non-Responsibility:

* 신규 컴포넌트 구현

---

## Design System Agent

Input:

* prd
* architecture
* component_reuse_plan
* existing_tokens

Output:

* design_token_plan
* chart_palette_rule
* typography_rule
* icon_rule
* spacing_rule

Non-Responsibility:

* 페이지 구현

---

## Page Builder Agent

Input:

* prd
* architecture
* data_model
* component_reuse_plan
* design_token_plan
* implementation_plan

Output:

* implemented_page
* changed_files
* implementation_notes
* known_limitations

Non-Responsibility:

* 요구사항 변경
* PRD 변경
* 임의 디자인 변경

---

## Reviewer Agent

Input:

* changed_files
* implementation_notes
* related_rules
* prd
* architecture

Output:

* review_report
* rule_violations
* risk_level
* required_fixes

Non-Responsibility:

* 기능 새로 설계
* 범위 외 리팩터링

---

## Evaluator Agent

Input:

* prd
* success_criteria
* review_report
* implemented_result

Output:

* evaluation_report
* acceptance_status
* unmet_requirements
* next_actions

Non-Responsibility:

* 코드 구현

---

## Documentation Agent

Input:

* prd
* architecture
* changed_files
* evaluation_report

Output:

* usage_documentation
* change_summary
* decision_log
* related_agent_notes

Non-Responsibility:

* 구현 변경

---

# Failure Handling

입력이 부족한 경우 Agent는 작업을 추측해서 진행하지 않는다.

다음 중 하나를 수행한다.

1. 누락된 입력을 명시한다.
2. 합리적인 가정을 작성한다.
3. 위험도를 기록한다.
4. 다음 Agent 또는 Reviewer에게 전달한다.

중요한 요구사항이 불명확하면 Requirements Agent로 되돌린다.

구조가 불명확하면 Architecture Agent로 되돌린다.

데이터 정의가 불명확하면 Data Modeling Agent로 되돌린다.

---

# Completion Rule

Agent 작업은 다음 조건을 만족해야 완료된다.

* 입력을 명확히 사용했다.
* 책임 범위를 벗어나지 않았다.
* 산출물을 생성했다.
* 판단 근거를 기록했다.
* 위험과 가정을 기록했다.
* 다음 Agent가 사용할 수 있는 형태로 결과를 반환했다.
