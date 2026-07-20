# [Router] Work Classification

## 목적

Work Classification은 Router가 사용자 요청을 이해하기 위한 첫 번째 분석 단계이다.

Router는 Agent를 선택하기 전에 먼저 **"이 요청이 어떤 종류의 작업인가?"**를 판단해야 한다.

Work는 프로젝트의 업무 영역을 의미하며, 이후 Intent 분석과 Agent 선택의 기준이 된다.

---

# Router 분석 흐름

모든 요청은 아래 순서로 분석한다.

```text
User Request
    ↓
Work Classification
    ↓
Intent Analysis
    ↓
Execution Planning
    ↓
Agent Orchestration
```

Work를 잘못 판단하면 이후 모든 단계가 잘못될 수 있다.

---

# Work Category

## 1. Platform Development

### 목적

플랫폼 자체를 확장하거나 기반 기능을 구축하는 작업

### 예시

* Router 개발
* 공통 Framework 개발
* Dashboard Framework
* 공통 Utility
* Session 구조
* 프로젝트 구조 개선

### 주요 특징

* 프로젝트 전체에 영향을 준다.
* 재사용성을 목표로 한다.
* 구현보다 설계를 우선한다.

---

## 2. Agent Development

### 목적

AI Agent 자체를 추가하거나 개선하는 작업

### 예시

* 새로운 Agent 추가
* Prompt 개선
* Agent 역할 재정의
* Agent 협업 구조 개선
* Router 개선

---

## 3. Analysis Page Development

### 목적

새로운 품질 분석 페이지를 개발한다.

### 예시

* 품질 KPI Dashboard
* 불량 분석
* LOT 분석
* 검사 결과 분석
* 공정 분석
* 생산 현황 Dashboard

### 주요 특징

항상

* Architecture
* Data Model
* KPI
* Component
* UI

순으로 진행한다.

---

## 4. Existing Page Improvement

### 목적

기존 페이지를 개선한다.

### 예시

* UX 개선
* 성능 개선
* 화면 재구성
* 기능 추가
* 유지보수

---

## 5. Component Development

### 목적

재사용 가능한 UI Component를 개발하거나 개선한다.

### 대상

* Chart
* Card
* Filter
* Table
* Layout
* Dialog
* Navigation

새 Component를 만들기 전에 반드시 기존 Component를 확인한다.

---

## 6. Design System

### 목적

UI의 일관성을 유지한다.

### 대상

* Color Token
* Typography
* Icon
* Theme
* Chart Palette
* Spacing
* Radius

---

## 7. Data Engineering

### 목적

품질 데이터 분석을 위한 데이터 구조를 설계한다.

### 대상

* Data Model
* SQL
* Aggregation
* KPI
* Metric
* Fact
* Dimension

---

## 8. Analytics

### 목적

데이터를 분석하여 인사이트를 제공한다.

### 예시

* KPI 분석
* 추세 분석
* 불량 원인 분석
* 이상치 분석
* Pareto
* YoY
* MoM

---

## 9. Automation

### 목적

반복 업무를 자동화한다.

### 대상

* Email
* Scheduler
* Report
* Alert
* Batch
* Export

---

## 10. Quality Improvement

### 목적

프로젝트 품질을 향상시킨다.

### 대상

* Code Review
* Rule 개선
* Refactoring
* Performance
* Documentation
* Test

---

## 11. Knowledge Management

### 목적

프로젝트 지식을 관리한다.

### 대상

* Documentation
* Rule
* Skill
* Prompt
* Wiki
* Best Practice

---

# Classification Rules

Router는 하나 이상의 Work를 선택할 수 있다.

예시

새로운 Dashboard 개발

↓

* Analysis Page Development
* Data Engineering
* Component Development

---

기존 Dashboard 개선

↓

* Existing Page Improvement
* Performance
* Quality Improvement

---

Router 개선

↓

* Platform Development
* Agent Development

---

Email 자동화

↓

* Automation
* Data Engineering

---

# Priority

Work가 여러 개 선택될 경우 아래 우선순위를 따른다.

1. Platform Development
2. Agent Development
3. Analysis Page Development
4. Existing Page Improvement
5. Data Engineering
6. Analytics
7. Component Development
8. Design System
9. Automation
10. Quality Improvement
11. Knowledge Management

상위 Work가 하위 Work보다 우선한다.

---

# Output

Work Classification 결과는 최소한 아래 정보를 포함한다.

* Primary Work
* Secondary Work
* Work 목적
* 예상 영향 범위
* 필요한 전문 영역

Work Classification은 아직 Agent를 선택하지 않는다.

이 단계에서는 **무슨 일을 해야 하는지**만 정의한다.

Agent 선택은 다음 단계인 Intent Analysis에서 수행한다.

---

# Success Criteria

Work Classification이 성공했다는 것은 다음을 의미한다.

* 요청의 성격을 정확히 분류했다.
* 프로젝트 관점에서 작업 범위를 이해했다.
* 이후 Intent 분석에 필요한 정보를 제공했다.
* 아직 구현 방법이나 Agent를 결정하지 않았다.

Work Classification의 역할은 **무엇을 해야 하는지 정의하는 것**이며, **어떻게 구현할지는 다음 단계에서 결정한다.**
