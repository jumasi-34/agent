# 02_PROJECT_CHARTER.md

# AI Agent Platform Charter

## 목적

이 문서는 AI Agent Platform의 운영 기준을 정의한다.

Vision은 프로젝트의 존재 이유를 정의한다.

Principles는 의사결정 기준을 정의한다.

Charter는 AI가 프로젝트에서 어떻게 행동해야 하는지를 정의한다.

모든 Agent, Router, Rule, Skill, Prompt는 본 문서를 따라야 한다.

---

# Document Hierarchy

프로젝트의 모든 판단은 아래 순서를 따른다.

```text
VISION

↓

PRINCIPLES

↓

PROJECT_CHARTER

↓

ROADMAP

↓

ITERATION

↓

RULE

↓

AGENT

↓

SKILL

↓

PROMPT

↓

IMPLEMENTATION
```

하위 문서는 상위 문서를 위반할 수 없다.

---

# Project Operation

프로젝트는 작은 Iteration을 통해 지속적으로 발전한다.

한 번에 모든 구조를 변경하지 않는다.

현재 Iteration에서 정의된 작업만 수행한다.

Iteration이 종료되면 다음 작업을 제안한다.

---

# AI Working Process

모든 작업은 아래 순서를 따른다.

```text
현재 상태 분석

↓

관련 문서 확인

↓

관련 Rule 확인

↓

관련 Agent 확인

↓

영향도 분석

↓

구현

↓

Review

↓

Evaluation

↓

Documentation

↓

다음 Iteration 제안
```

---

# Required Reading Order

모든 Agent와 CLI는 작업을 시작하기 전에 아래 순서로 문서를 확인한다.

```text
01 Vision

↓

02 Principles

↓

03 Charter

↓

04 Roadmap

↓

05 Current Iteration

↓

관련 Rule

↓

관련 Skill

↓

관련 Agent

↓

대상 코드
```

필요하지 않은 Rule과 Skill은 로드하지 않는다.

---

# Router Policy

Router는 프로젝트의 Orchestrator이다.

Router는 다음을 수행한다.

* 작업 목적 분석
* Intent 분석
* Context 선택
* Rule 선택
* Skill 선택
* Agent 선택
* 실행 순서 생성
* Review 기준 선택
* 산출물 정의

Router는 구현을 수행하지 않는다.

Router는 작업을 조율하는 역할만 수행한다.

---

# Agent Policy

모든 Agent는 하나의 전문 영역만 담당한다.

Agent는 자신의 책임 범위를 벗어나지 않는다.

Agent는 다른 Agent의 역할을 대신하지 않는다.

새로운 Agent는 기존 Agent를 대체하지 않는다.

필요한 경우 협업한다.

---

# Rule Policy

Rule은 프로젝트의 표준이다.

Agent는 Rule을 우선적으로 따른다.

Rule이 부족하면 Rule 개선을 제안한다.

Rule을 우회하지 않는다.

---

# Skill Policy

Skill은 작업을 수행하기 위한 재사용 가능한 실행 방법이다.

Skill은 독립적으로 관리한다.

중복 Skill은 생성하지 않는다.

---

# Component Policy

Component는 프로젝트 자산이다.

새로운 Component를 만들기 전에

반드시 기존 Component를 확인한다.

재사용이 가능하면 새로운 Component를 만들지 않는다.

---

# Design System Policy

모든 UI는 Design System을 따른다.

다음 요소는 Token으로 관리한다.

* Color
* Typography
* Icon
* Radius
* Spacing
* Shadow
* Chart Palette

직접 값을 사용하는 것을 최소화한다.

---

# Documentation Policy

모든 중요한 변경은 문서화한다.

다음 내용은 반드시 기록한다.

* 변경 이유
* 변경 내용
* 영향 범위
* 관련 Rule
* 관련 Agent

문서는 프로젝트의 지식 자산이다.

---

# Conflict Policy

기존 구조와 충돌하는 경우

즉시 수정하지 않는다.

먼저

* 충돌 분석
* 영향 분석
* 해결 방안 제안

을 수행한다.

충돌 해결은 별도 Iteration에서 수행한다.

---

# Modification Policy

명시적으로 요청받지 않는 이상

다음 작업은 수행하지 않는다.

* 기존 Agent 삭제
* 기존 Rule 삭제
* 기존 Skill 삭제
* 디렉터리 구조 변경
* 대규모 리팩터링
* 여러 Iteration 동시 수행

필요한 경우 새로운 Layer를 추가한다.

---

# Completion Policy

Iteration 종료 후 반드시 다음 내용을 제공한다.

* 이번 목표
* 수행 내용
* 생성 파일
* 수정 파일
* 영향받는 Agent
* 영향받는 Rule
* 발견된 문제
* 다음 Iteration 제안

---

# Definition of Done

하나의 작업은 아래 조건을 만족해야 완료된 것으로 판단한다.

* Vision에 부합한다.
* Principles를 위반하지 않는다.
* Charter를 따른다.
* 현재 Iteration 범위 내에서 수행되었다.
* 관련 Rule을 준수했다.
* 필요한 Review가 완료되었다.
* 필요한 Documentation이 작성되었다.

이 조건을 만족하지 못하면 작업은 완료되지 않은 것으로 본다.
