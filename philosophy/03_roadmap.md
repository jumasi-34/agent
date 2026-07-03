# 03_ROADMAP.md

# AI Agent Platform Roadmap

## 목적

이 문서는 AI Agent Platform이 어떤 방향으로 발전할 것인지 정의한다.

Roadmap은 기능 목록이 아니라 플랫폼의 성장 계획이다.

모든 개발은 Roadmap의 Phase를 기준으로 진행하며, 한 번에 하나의 Phase와 하나의 Iteration만 수행한다.

---

# Development Strategy

프로젝트는 다음 순서로 발전한다.

```text
Vision
    ↓
Principles
    ↓
Project Charter
    ↓
Roadmap
    ↓
Iteration
    ↓
Implementation
```

Roadmap은 **무엇을 언제 구축할 것인가**를 정의한다.

---

# Phase 1. Router Foundation

## 목표

AI Agent Platform의 기반이 되는 Router를 설계한다.

## 완료 기준

* Router Architecture 정의
* Intent 체계 정의
* Router Pipeline 정의
* Routing Strategy 정의
* Router와 기존 Agent의 관계 정의

## 주요 산출물

* Router Specification
* Intent Schema
* Routing Strategy
* Routing Table
* Agent Responsibility Matrix

---

# Phase 2. Agent Ecosystem

## 목표

Router와 연계되는 Agent의 책임을 명확하게 정의한다.

## 완료 기준

* 기존 Agent 역할 정리
* 신규 Agent 설계
* Agent 간 협업 구조 정의
* Agent 호출 순서 정의

## 대상 Agent

기존

* Planner
* Data Agent
* Component Agent
* Page Builder
* Reviewer
* Evaluator

신규

* Architecture Agent
* Data Modeling Agent
* Design System Agent
* Component Librarian Agent
* Insight Agent
* Performance Agent
* Refactoring Agent
* Automation Agent
* Documentation Agent
* Prompt Optimizer Agent
* Project Health Agent

---

# Phase 3. Development Platform

## 목표

품질 분석 플랫폼 개발을 위한 공통 개발 기반을 구축한다.

## 대상

* Dashboard Framework
* Analysis Page Framework
* Navigation
* Layout
* Session 관리
* Page Template
* 공통 유틸리티

---

# Phase 4. Component & Design System

## 목표

재사용 가능한 UI 플랫폼을 구축한다.

## 대상

* Chart Component
* Metric Card
* Filter
* Table
* Dialog
* Layout Component
* Theme
* Color Token
* Typography
* Icon
* Chart Palette

---

# Phase 5. Data Intelligence

## 목표

품질 데이터를 효과적으로 분석하기 위한 데이터 플랫폼을 구축한다.

## 대상

* Data Model
* KPI
* Metric
* SQL Framework
* Aggregation
* Insight
* Root Cause Analysis
* Trend Analysis
* Quality Analytics

---

# Phase 6. Automation Platform

## 목표

반복적인 품질 업무를 자동화한다.

## 대상

* Email Report
* Scheduler
* Alert
* Batch
* Export
* Report Generator

---

# Phase 7. Quality & Governance

## 목표

프로젝트 품질을 지속적으로 관리한다.

## 대상

* Rule 검증
* Code Review
* Documentation
* Test Framework
* Project Health
* 품질 지표 관리

---

# Phase 8. Self-Improving Platform

## 목표

AI Agent Platform이 스스로 발전할 수 있는 구조를 구축한다.

## 대상

* Prompt Optimization
* Knowledge Management
* Pattern Learning
* Agent Improvement
* Router Optimization
* Rule Evolution

---

# Phase Completion Rule

각 Phase는 다음 순서를 따른다.

```text
분석

↓

설계

↓

검토

↓

Iteration 수행

↓

Review

↓

Documentation

↓

다음 Phase 준비
```

다음 Phase는 현재 Phase의 완료 기준을 만족한 이후에만 진행한다.

---

# Iteration Rule

각 Phase는 여러 개의 Iteration으로 구성된다.

예시

Phase 1

* Iteration 01
* Iteration 02
* Iteration 03

...

Iteration은 하나의 명확한 목표만 가진다.

Iteration이 완료된 후 다음 Iteration을 시작한다.

---

# Success Criteria

Roadmap이 성공적으로 진행되면 다음 상태를 달성해야 한다.

* 품질 부서와 공장 운영 인원이 신뢰할 수 있는 데이터 분석 플랫폼을 사용할 수 있다.
* Dashboard와 분석 페이지를 빠르고 일관성 있게 개발할 수 있다.
* 대부분의 기능이 재사용 가능한 자산으로 관리된다.
* AI Agent가 역할을 분담하여 안정적으로 협업한다.
* Router가 프로젝트 전체 개발 과정을 조율한다.
* 반복 업무가 자동화되고, 프로젝트는 지속적으로 발전한다.

---

# Current Focus

현재 프로젝트는 **Phase 1 - Router Foundation**을 진행한다.

현재 목표는 Router를 구현하는 것이 아니라 **Router Architecture를 설계하고 기존 프로젝트에 자연스럽게 통합할 수 있는 기반을 마련하는 것**이다.

현재 Phase가 완료되기 전까지는 이후 Phase의 구현을 진행하지 않는다.
