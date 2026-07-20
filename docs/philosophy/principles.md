# [Philosophy] AI Agent Platform Principles

## 목적

이 문서는 프로젝트의 모든 의사결정 기준을 정의한다.

Vision이 "왜(Why)"를 정의한다면,

Principles는 "어떻게 판단할 것인가(Decision Making)"를 정의한다.

모든 Agent, Router, Rule, Skill, Prompt는 이 원칙을 따라야 한다.

---

# Principle 1. User Value First

모든 개발은 **품질 부서와 공장 운영 인원의 업무 효율과 데이터 기반 의사결정 향상**을 최우선 가치로 한다.

새로운 기술이나 화려한 기능보다 실제 업무에 도움이 되는 기능을 우선한다.

질문해야 하는 것은

> "이 기능이 사용자에게 어떤 가치를 제공하는가?"

이다.

---

# Principle 2. Platform Before Feature

우리는 기능을 만드는 것이 아니라 플랫폼을 만든다.

새로운 기능은 항상 플랫폼 안에서 재사용될 수 있도록 설계한다.

단발성 구현보다

* 확장성
* 재사용성
* 유지보수성

을 우선한다.

---

# Principle 3. Reuse Before Create

새로운 것을 만들기 전에 기존 자산을 먼저 찾는다.

우선순위는 다음과 같다.

1. 기존 Component
2. 기존 Design Token
3. 기존 Rule
4. 기존 Skill
5. 기존 Agent
6. 기존 SQL
7. 기존 Template

재사용이 가능하다면 새로 만들지 않는다.

---

# Principle 4. Architecture Before Implementation

구현보다 설계를 먼저 수행한다.

새로운 페이지나 기능을 개발하기 전에 반드시 다음을 정의한다.

* 목적
* 사용자
* 데이터
* 구조
* 컴포넌트
* KPI
* 화면 구성

설계 없는 구현은 지양한다.

---

# Principle 5. Data Before UI

데이터 구조를 먼저 설계하고 화면을 만든다.

Dashboard는 데이터를 보여주는 도구이다.

따라서

Data Model

↓

Aggregation

↓

KPI

↓

Visualization

순서를 따른다.

---

# Principle 6. Consistency Over Creativity

프로젝트 전체의 일관성을 우선한다.

새로운 디자인이나 구현 방식보다

기존 Rule과 Design System을 따른다.

사용자는 페이지마다 다른 경험을 원하지 않는다.

---

# Principle 7. Rule Driven Development

모든 구현은 Rule을 기반으로 수행한다.

Agent는 Rule을 해석하고 실행하는 존재이다.

Rule보다 Agent의 판단이 우선하지 않는다.

Rule이 부족하다면

Rule을 개선한다.

---

# Principle 8. Single Responsibility

Agent는 하나의 전문 영역만 담당한다.

Component도 하나의 목적만 가진다.

Page도 하나의 업무를 담당한다.

책임이 명확해야 유지보수가 쉬워진다.

---

# Principle 9. Incremental Evolution

프로젝트는 작은 Iteration으로 발전한다.

한 번에 전체 구조를 변경하지 않는다.

한 Iteration은 하나의 목표만 가진다.

완료 후 다음 Iteration을 진행한다.

---

# Principle 10. Automation When Repeated

두 번 이상 반복되는 작업은 자동화를 검토한다.

예를 들어

* 데이터 집계
* 이메일
* 리포트
* KPI 계산
* 차트 생성
* 테스트
* 문서 생성

은 자동화 대상이다.

---

# Principle 11. Knowledge as an Asset

모든 경험은 프로젝트의 자산이다.

개발 경험은

Rule

Skill

Prompt

Document

Template

Agent

로 축적되어야 한다.

같은 문제를 두 번 해결하지 않는다.

---

# Principle 12. Continuous Improvement

프로젝트는 완성되는 것이 아니라 지속적으로 발전한다.

모든 작업은

개발

↓

Review

↓

Evaluation

↓

Learning

↓

Improvement

의 순환 구조를 가진다.

AI 역시 지속적으로 개선 대상이다.

---

# Decision Priority

의사결정이 필요한 경우 아래 우선순위를 따른다.

1. Vision
2. Principles
3. Project Charter
4. Roadmap
5. Iteration
6. Rule
7. Agent
8. Skill
9. Prompt
10. Implementation

하위 단계가 상위 단계를 위반해서는 안 된다.

---

# What Every Agent Must Remember

모든 Agent는 항상 다음 질문을 스스로에게 해야 한다.

* 이 작업은 Vision에 부합하는가?
* 사용자에게 실제 도움이 되는가?
* 기존 자산을 재사용할 수 있는가?
* Rule을 따르고 있는가?
* 다른 Agent의 책임을 침범하지 않는가?
* 지금 Iteration 범위를 벗어나지 않는가?
* 장기적으로 유지보수하기 쉬운가?
* 프로젝트 전체 품질을 향상시키는가?

이 질문에 모두 긍정적으로 답할 수 있을 때만 작업을 수행한다.
