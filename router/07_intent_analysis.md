# router/07_intent_analysis.md

# Intent Analysis

## 목적

Intent Analysis는 Work Classification 이후 수행되는 두 번째 분석 단계이다.

Work가 **무슨 종류의 작업인가**를 정의한다면,

Intent는 **사용자가 무엇을 달성하려는가**를 정의한다.

Router는 구현 방법보다 먼저 사용자의 목적을 이해해야 한다.

---

# Router 분석 흐름

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

Intent는 Router가 프로젝트의 방향과 사용자의 목적을 연결하는 핵심 정보이다.

---

# Intent Category

## 1. Create

새로운 기능이나 자산을 만든다.

예시

* 새로운 Dashboard
* 새로운 분석 페이지
* 새로운 Component
* 새로운 Agent
* 새로운 Rule

결과

프로젝트에 새로운 자산이 추가된다.

---

## 2. Improve

기존 자산을 개선한다.

예시

* UX 개선
* 구조 개선
* 기능 개선
* 성능 개선

결과

기존 자산의 품질이 향상된다.

---

## 3. Standardize

프로젝트의 일관성을 높인다.

예시

* Design Token 적용
* Component 통합
* Naming 통일
* Rule 정리

결과

프로젝트의 유지보수성이 향상된다.

---

## 4. Reuse

기존 자산을 활용한다.

예시

* 기존 Component 사용
* 기존 SQL 활용
* 기존 Dashboard 확장

결과

중복 개발을 방지한다.

---

## 5. Analyze

데이터를 분석한다.

예시

* KPI 분석
* Trend 분석
* 이상치 분석
* 불량 원인 분석

결과

사용자의 의사결정을 지원한다.

---

## 6. Automate

반복 업무를 자동화한다.

예시

* 이메일
* Scheduler
* Report
* Batch

결과

반복 작업이 감소한다.

---

## 7. Optimize

효율을 향상시킨다.

예시

* SQL 최적화
* Cache 적용
* 렌더링 개선
* DataFrame 최적화

결과

성능과 생산성이 향상된다.

---

## 8. Govern

프로젝트 품질을 관리한다.

예시

* Rule 검토
* Code Review
* Documentation
* Health Check

결과

프로젝트의 일관성이 유지된다.

---

## 9. Learn

프로젝트 경험을 자산으로 만든다.

예시

* 문서화
* Best Practice 작성
* Rule 개선
* Prompt 개선

결과

프로젝트가 지속적으로 발전한다.

---

# Intent 결정 기준

Router는 다음 질문을 통해 Intent를 판단한다.

### 무엇을 만들려고 하는가?

↓

Create

---

### 기존 것을 개선하려는가?

↓

Improve

---

### 프로젝트를 통일하려는가?

↓

Standardize

---

### 기존 자산을 활용하려는가?

↓

Reuse

---

### 데이터를 이해하려는가?

↓

Analyze

---

### 반복 업무를 줄이려는가?

↓

Automate

---

### 더 빠르고 효율적으로 만들려는가?

↓

Optimize

---

### 프로젝트 품질을 관리하려는가?

↓

Govern

---

### 프로젝트를 더 똑똑하게 만들려는가?

↓

Learn

---

# Multiple Intent

하나의 요청은 여러 Intent를 가질 수 있다.

예시

새 Dashboard 개발

↓

Create

Reuse

Analyze

---

기존 Dashboard 개선

↓

Improve

Optimize

Standardize

---

Router 개선

↓

Improve

Govern

Learn

---

Email 자동화

↓

Automate

Analyze

Reuse

---

# Output

Intent Analysis 결과는 다음 정보를 생성한다.

* Primary Intent
* Secondary Intent
* 사용자 목적
* 기대 효과
* 성공 기준

Intent는 구현 방법을 결정하지 않는다.

Intent는 사용자가 무엇을 달성하려는지를 정의한다.

---

# Relationship

```text
Work

무슨 종류의 작업인가?

↓

Intent

무엇을 이루려는가?

↓

Execution

어떻게 수행할 것인가?
```

---

# Success Criteria

Intent Analysis가 성공했다는 것은

* 사용자의 목적을 올바르게 이해했다.
* Work와 Intent를 구분했다.
* 실행 방법을 아직 결정하지 않았다.
* 다음 단계에서 실행 계획을 세울 수 있는 정보를 제공했다.

Intent는 프로젝트의 방향을 결정하는 기준이며,

Execution은 그 방향을 실현하는 방법이다.
