# router/08_routing_table.md

# Router Routing Table

## 목적

Routing Table은 Router가 분석한 결과를 실제 실행 계획으로 변환하는 규칙이다.

Work Classification과 Intent Analysis를 기반으로 다음을 결정한다.

* 어떤 Agent를 사용할 것인가
* 어떤 순서로 실행할 것인가
* 어떤 산출물을 생성할 것인가
* 어떤 Review가 필요한가

Routing Table은 프로젝트의 표준 실행 흐름을 정의한다.

---

# Router Decision Flow

모든 요청은 아래 순서로 처리한다.

```text
User Request
    ↓
Work Classification
    ↓
Intent Analysis
    ↓
Routing Table
    ↓
Execution Plan
    ↓
Agent Execution
```

---

# Standard Routing Rules

## 1. Platform Development

### 목적

플랫폼 구조를 구축하거나 개선한다.

### 기본 실행 순서

```text
Planner
↓
Architecture Agent
↓
Reviewer
↓
Documentation Agent
```

### 산출물

* Architecture Document
* Design Decision
* Review Report

---

## 2. Agent Development

### 목적

AI Agent를 추가하거나 개선한다.

### 기본 실행 순서

```text
Planner
↓
Architecture Agent
↓
Prompt Optimizer Agent
↓
Reviewer
↓
Documentation Agent
```

### 산출물

* Agent Specification
* Prompt
* Responsibility 정의

---

## 3. Analysis Page Development

### 목적

새로운 품질 분석 페이지를 개발한다.

### 기본 실행 순서

```text
Planner
↓
Architecture Agent
↓
Data Modeling Agent
↓
Insight Agent
↓
Component Librarian Agent
↓
Design System Agent
↓
Page Builder
↓
Performance Agent
↓
Reviewer
↓
Evaluator
↓
Documentation Agent
```

### 산출물

* Page Architecture
* KPI 정의
* Data Model
* 구현 코드
* Review Report

---

## 4. Existing Page Improvement

### 목적

기존 페이지를 개선한다.

### 기본 실행 순서

```text
Planner
↓
Architecture Agent
↓
Component Librarian Agent
↓
Refactoring Agent
↓
Performance Agent
↓
Page Builder
↓
Reviewer
↓
Documentation Agent
```

---

## 5. Component Development

### 목적

재사용 가능한 Component를 개발한다.

### 기본 실행 순서

```text
Planner
↓
Component Librarian Agent
↓
Design System Agent
↓
Component Agent
↓
Reviewer
↓
Documentation Agent
```

---

## 6. Design System

### 목적

디자인 일관성을 유지한다.

### 기본 실행 순서

```text
Planner
↓
Design System Agent
↓
Reviewer
↓
Documentation Agent
```

---

## 7. Data Engineering

### 목적

데이터 모델과 집계 구조를 구축한다.

### 기본 실행 순서

```text
Planner
↓
Data Modeling Agent
↓
Data Agent
↓
Performance Agent
↓
Reviewer
↓
Documentation Agent
```

---

## 8. Analytics

### 목적

데이터를 분석하고 인사이트를 제공한다.

### 기본 실행 순서

```text
Planner
↓
Insight Agent
↓
Data Agent
↓
Reviewer
↓
Documentation Agent
```

---

## 9. Automation

### 목적

반복 업무를 자동화한다.

### 기본 실행 순서

```text
Planner
↓
Automation Agent
↓
Reviewer
↓
Documentation Agent
```

---

## 10. Quality Improvement

### 목적

프로젝트 품질을 향상시킨다.

### 기본 실행 순서

```text
Planner
↓
Performance Agent
↓
Refactoring Agent
↓
Reviewer
↓
Project Health Agent
↓
Documentation Agent
```

---

## 11. Knowledge Management

### 목적

프로젝트 지식을 축적하고 관리한다.

### 기본 실행 순서

```text
Planner
↓
Documentation Agent
↓
Project Health Agent
```

---

# Routing Rules

모든 Routing은 다음 규칙을 따른다.

## Rule 1

Planner는 항상 가장 먼저 실행한다.

---

## Rule 2

Architecture가 필요한 작업은 구현 전에 반드시 수행한다.

---

## Rule 3

새로운 UI를 만들기 전에 Component 재사용 여부를 확인한다.

---

## Rule 4

새로운 UI는 Design System을 반드시 확인한다.

---

## Rule 5

모든 구현은 Reviewer를 거친다.

---

## Rule 6

문서화가 필요한 작업은 Documentation Agent로 종료한다.

---

## Rule 7

성능이 중요한 작업은 Performance Agent를 포함한다.

---

## Rule 8

Router는 필요한 Agent만 선택한다.

모든 Agent를 항상 실행하지 않는다.

---

# Dynamic Routing

위 실행 순서는 기본(Standard) 흐름이다.

Router는 요청의 목적과 범위에 따라 일부 Agent를 생략하거나 추가할 수 있다.

단, 다음 원칙은 유지한다.

* Planner는 항상 포함한다.
* Reviewer는 구현 작업에 항상 포함한다.
* Documentation Agent는 설계 변경 또는 구현 변경 시 포함한다.
* Architecture Agent는 신규 구조 설계 시 포함한다.

---

# Definition of Success

Routing이 성공했다는 것은 다음을 의미한다.

* 올바른 Agent가 선택되었다.
* 불필요한 Agent는 실행하지 않았다.
* 실행 순서가 논리적이다.
* 프로젝트 원칙을 위반하지 않는다.
* 구현보다 설계를 우선한다.
* 재사용 가능한 자산을 우선 활용한다.
* 결과가 문서와 지식으로 축적된다.

---

# Final Statement

Routing Table은 고정된 워크플로가 아니다.

프로젝트가 성장함에 따라 Work와 Agent는 추가될 수 있다.

그러나 Router의 역할은 변하지 않는다.

**Router는 항상 사용자의 요청을 프로젝트의 비전과 연결하고, 가장 적절한 실행 계획을 생성하여 품질 분석 플랫폼이 일관된 방향으로 발전하도록 조율한다.**
