---
id: map.agent_skill
title: "[Skill Map]"
type: wiki
status: active

summary: >
  22대 대형 에이전트 카탈로그와 연동되는 에이전트별 필수 기동 스킬 맵핑 정의서.
  각 거버넌스 레이어별 에이전트가 완수해야 할 가동 스킬들을 최신화하여 명시한다.

keywords:
  - agent-os
  - skill-map
  - capabilities
  - 22-agents

parent: concept.agent_os.governance

related:
  - "[.agents/agents/agents.md](.agents/agents/agents.md)"
  - "[.agents/skills/index.md](.agents/skills/index.md)"

consumers:
  - "[.agents/agents/roles/planner-agent.md](.agents/agents/roles/planner-agent.md)"
  - "[.agents/agents/roles/router-agent.md](.agents/agents/roles/router-agent.md)"

updated: 2026-07-04
---
# 에이전트별 필수 기동 스킬 맵핑 정의서 (.agents/agents/skill-map.md)

## Overview
* **왜 존재하는가 (Why)**: 22대 대형 에이전트 카탈로그 환경에서 각 에이전트 페르소나가 자기 기동 단계 및 역할에 부합하는 정량적 스킬셋(Tool)을 정상 수렴하고 오작동 없이 사용하도록 일원화된 연동 정합성을 보장하기 위함입니다.
* **언제 사용하는가 (When)**: 신규 글로벌/로컬 스킬을 에이전트 라이프사이클에 안전하게 이식하거나, 특정 에이전트의 권한 및 협업 동선을 확장하고자 할 때 참조하고 개정합니다.
* **연계 실행 (Next Action)**: 전체 에이전트 거버넌스 규정을 담은 [.agents/agents/agents.md](.agents/agents/agents.md) 및 [.agents/skills/index.md](.agents/skills/index.md)를 함께 열어 정합성을 지속 검역하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](.agents/AGENTS.md)
* **연관 자산**: [.agents/agents/agents.md](.agents/agents/agents.md) | [.agents/skills/index.md](.agents/skills/index.md) | [.agents/agents/agents_registry.json](.agents/agents/agents_registry.json)
---

본 문서는 프로젝트 내의 22대 AI 에이전트 역할군이 어떤 스킬을 핵심적으로 기동하고 활용해야 하는지 명시한 **에이전트-스킬 물리 연동 정의서**입니다. 모든 하이퍼링크는 WSL Markdown Link Constraint 수칙에 부합하도록 평문 상대 경로로 연결되었습니다.

---

## 1. 전략 및 조율 레이어 (Strategic & Coordination Tier)

### [router-agent (Router Agent)](.agents/agents/roles/router-agent.md)
*   **본질적 임무**: 최소 지연 다이내믹 바인딩 및 사전 재사용성 대조 프로토콜을 가동하여 사용자 쿼리에 따른 최적의 파이프라인 시퀀스를 형성합니다.
*   **권장 및 필수 가동 스킬**:
    *   `using-superpowers` (글로벌): 세션 시작 즉시 요구사항 파악 전 에이전트 능력 준비
    *   `subagent-driven-development` (글로벌): 하위 실행 에이전트들로의 유기적 분배 및 관리
    *   `dispatching-parallel-agents` (글로벌): 상호 의존성 없는 태스크의 병렬 실행 가속화
    *   [.agents/skills/agent_hooks/SKILL.md](.agents/skills/agent_hooks/SKILL.md) (로컬): 비정상 동작 제어 및 세션 라이프사이클 런타임 수렴

### [planner-agent (Planner Agent)](.agents/agents/roles/planner-agent.md)
*   **본질적 임무**: 사용자 및 비즈니스 의도가 수집되면 최상위에서 기획 방향성 및 작업 로드맵 체크리스트를 정립합니다.
*   **권장 및 필수 가동 스킬**:
    *   `using-superpowers` (글로벌): 초기화 소통 및 지침의 선제 탐색
    *   `brainstorming` (글로벌): 요구 조건의 타당성 검증 및 상위 수준 기획 정렬
    *   `writing-plans` (글로벌): 단계별 순차 구현 계획서 구축
    *   `understand` (글로벌): 전체 아키텍처 및 소스 경계 사전 조감

### [requirements-agent (Requirements Agent)](.agents/agents/roles/requirements-agent.md)
*   **본질적 임무**: 사용자 자연어 요청의 세부 기능/비기능 요구사항을 구체화하고 완료 정의(DoD) 성공 기준을 상세 수립합니다.
*   **권장 및 필수 가동 스킬**:
    *   `brainstorming` (글로벌): 요구 수준의 조밀한 예외 케이스 정의 및 가치 정렬
    *   `writing-plans` (글로벌): DoD 만족을 위한 기획 이정표 수립

### [architecture-agent (Architecture Agent)](.agents/agents/roles/architecture-agent.md)
*   **본질적 임무**: 3-Layer 레이어 경계 준수율을 관리하고 컴포넌트 간 순환 참조 종속성을 원천 방지하는 흐름을 설계합니다.
*   **권장 및 필수 가동 스킬**:
    *   `understand` (글로벌): 컴포넌트 경계 스캔 및 종속 관계 시각 분석
    *   `writing-plans` (글로벌): 구조 설계 계획 수립

---

## 2. 구현 빌더 레이어 (Implementation Tier)

### [data-modeling-agent (Data Modeling Agent)](.agents/agents/roles/data-modeling-agent.md)
*   **본질적 임무**: 집계 분석 마트, Fact, Dimension 테이블 물리/논리 스키마를 수립하고 KPI 공식을 설계합니다.
*   **권장 및 필수 가동 스킬**:
    *   `understand` (글로벌): 원천 데이터베이스 DDL 스캔 및 구조 관계 탐색
    *   `writing-plans` (글로벌): 물리 컬럼 설계 이정표 기획

### [data-agent (Data Agent)](.agents/agents/roles/data-agent.md)
*   **본질적 임무**: SQL 쿼리 설계 및 Pandas 가공, 서비스 전처리 및 캐싱 모듈을 완벽하게 개발합니다.
*   **권장 및 필수 가동 스킬**:
    *   `understand` (글로벌): 소스-DB 간 데이터 흐름 종속성 대조
    *   `test-driven-development` (글로벌): 데이터 공급 함수 개발 전 단위 테스트 및 Mock 설계
    *   `systematic-debugging` (글로벌): 쿼리 실행 병목 및 Pandas 타입 에러의 체계적 디버깅
    *   `verification-before-completion` (글로벌): 정적 컴파일 검증 및 쿼리 무결 증명
    *   [.agents/skills/quality/sql/SKILL.md](.agents/skills/quality/sql/SKILL.md) (로컬): SQL 한글 별칭 하드코딩 여부 정적 진단

### [page-builder-agent (Page Builder Agent)](.agents/agents/roles/page-builder-agent.md)
*   **본질적 임무**: Streamlit 레이아웃 구성, 네비게이션 동적 매핑, 세션 가로채기 적용 및 공통 CSS 인젝션을 담당합니다.
*   **권장 및 필수 가동 스킬**:
    *   `frontend-design` (글로벌): 프리미엄 화면 타이포그래피 및 글래스모피즘 테마 주입
    *   `systematic-debugging` (글로벌): 위젯 강제 할당 오류(StreamlitAPIException) 자율 극복
    *   `verification-before-completion` (글로벌): Streamlit 화면 렌더링 무결성 증거 획득

### [component-agent (Component Agent)](.agents/agents/roles/component-agent.md)
*   **본질적 임무**: 프리미엄 Plotly 반응형 차트 튜닝, 미학적 일관성 확보 및 프리미엄 비주얼 요소를 탑재합니다.
*   **권장 및 필수 가동 스킬**:
    *   `frontend-design` (글로벌): 시각화 차트의 시각적 하모니 및 고급 테마 앰비언트 구현
    *   `verification-before-completion` (글로벌): 시각화 오브젝트 정상 작동 정밀 검정

### [refactoring-agent (Refactoring Agent)](.agents/agents/roles/refactoring-agent.md)
*   **본질적 임무**: 코드 복잡도 정밀 진단, 중복 제어 및 소스 코드 다이어트를 통한 3-Layer 전향 배치를 완수합니다.
*   **권장 및 필수 가동 스킬**:
    *   `systematic-debugging` (글로벌): 리팩토링 과정에서 유입되는 가설 오류 추적
    *   `verification-before-completion` (글로벌): 소스 경량화 후의 단위 빌드 정상성 통과 여부 검증

### [automation-agent (Automation Agent)](.agents/agents/roles/automation-agent.md)
*   **본질적 임무**: 백그라운드 크론 스케줄러, 보고서 생성기 및 웹훅 알림 자동화 동작 환경을 빌딩합니다.
*   **권장 및 필수 가동 스킬**:
    *   `systematic-debugging` (글로벌): 백그라운드 구동 예외 및 통지 누수 추적
    *   `verification-before-completion` (글로벌): 배치 실행 스크립트 정합 증명

### [test-agent (Test Agent)](.agents/agents/roles/test-agent.md)
*   **본질적 임무**: 단위 테스트 케이스 설계, 인메모리 고립 Mocking 테스트 및 회귀 테스트 스위트를 기획 구축합니다.
*   **권장 및 필수 가동 스킬**:
    *   `test-driven-development` (글로벌): 구현 전 테스트 스케포커스 및 회귀 무결성 검증 케이스 생성
    *   `verification-before-completion` (글로벌): 단위 테스트 정상 작동 입증

---

## 3. 분석 및 정적 품질 레이어 (Analytics & Quality Tier)

### [insight-agent (Insight Agent)](.agents/agents/roles/insight-agent.md)
*   **본질적 임무**: 데이터 이상치(Anomaly) 조기 진단 및 Pareto, Trend, YoY 정량/정성 브리핑 분석 리포트를 생산합니다.
*   **권장 및 필수 가동 스킬**:
    *   `understand` (글로벌): 데이터셋 구조 분석 및 비즈니스 인과 분석 연동
    *   [.agents/skills/memory/core/SKILL.md](.agents/skills/memory/core/SKILL.md) (로컬): 과거 유사 지표 분석 리포트 메모리 회상 및 연계

### [reviewer-agent (Reviewer Agent)](.agents/agents/roles/reviewer-agent.md)
*   **본질적 임무**: 파이썬 소스 코드의 스타일 규정, 3-Layer 위반 검지 및 아키텍처 결합도 피드백(Diff)을 발행합니다.
*   **권장 및 필수 가동 스킬**:
    *   `receiving-code-review` / `requesting-code-review` (글로벌): 코드 정밀 교정 및 안전 리뷰 프로세스 조율
    *   [.agents/skills/memory/core/SKILL.md](.agents/skills/memory/core/SKILL.md) (로컬): 변경된 소스코드 라인의 장기 기억 맥락 대조
    *   [.agents/skills/knowledge-capture/SKILL.md](.agents/skills/knowledge-capture/SKILL.md) (로컬): 카파시 코딩 규정 적용, 기술 마크다운 린트, 세션종료 자율 지식 캡처(Raw) 및 위키 정합성 관리

### [project-health-agent (Project Health Agent)](.agents/agents/roles/project-health-agent.md)
*   **본질적 임무**: 명명 규칙 준수율 정량 감사, DB 테이블 상수 동기화 진단 및 결합도 지표를 관리합니다.
*   **권장 및 필수 가동 스킬**:
    *   [.agents/skills/quality/guardrail/SKILL.md](.agents/skills/quality/guardrail/SKILL.md) (로컬): 배포 전 이모지 혼용율 스캔, 커밋 메시지 규격 검사 및 골든 스키마 연동 진단
    *   [.agents/skills/quality/sql/SKILL.md](.agents/skills/quality/sql/SKILL.md) (로컬): SQL 파일 구문 내 AS 별칭 물리 룰 준수율 감사
    *   [.agents/skills/quality/korean-metadata/SKILL.md](.agents/skills/quality/korean-metadata/SKILL.md) (로컬): 디스플레이 사전 데이터 갱신 및 컬럼 정합성 동기화

### [performance-agent (Performance Agent)](.agents/agents/roles/performance-agent.md)
*   **본질적 임무**: Rerun 지연 유발 로직 제어, 캐시 정밀 상태 분석 및 연산 병목 정량 진단 보고를 관리합니다.
*   **권장 및 필수 가동 스킬**:
    *   [.agents/skills/development/streamlit/SKILL.md](.agents/skills/development/streamlit/SKILL.md) (로컬): Streamlit 성능 튜닝 가이드 기동
    *   `verification-before-completion` (글로벌): 메모리 누수 및 Rerun 빈도 측정 검증

---

## 4. 거버넌스 및 배포 레이어 (Governance & Deployment Tier)

### [evaluator-agent (Evaluator Agent)](.agents/agents/roles/evaluator-agent.md)
*   **본질적 임무**: 종합 하네스 구동, 빌드 컴파일 무결성 보증 및 최종 Pass/Fail 게이트를 판정하는 채점표(Scorecard)를 발행합니다.
*   **권장 및 필수 가동 스킬**:
    *   [.agents/skills/quality-assurance/SKILL.md](.agents/skills/quality-assurance/SKILL.md) (로컬): 배포 전 5대 품질 관문(Quality Gate) 정밀 종합 자율 완수
    *   [.agents/skills/quality/guardrail/SKILL.md](.agents/skills/quality/guardrail/SKILL.md) (로컬): 배포 직전 이모지 규정 및 데이터 스키마 정합성 최종 통과 진증
    *   `verification-before-completion` (글로벌): `make verify` 등 단위/정적 테스트 종합 실행 및 Evidence 확보

### [release-agent (Release Agent)](.agents/agents/roles/release-agent.md)
*   **본질적 임무**: 배포 준비 상태 체크리스트 확인, 릴리즈 노트 영속 마크다운 기재 및 안전 머지를 정렬합니다.
*   **권장 및 필수 가동 스킬**:
    *   `finishing-a-development-branch` (글로벌): 배포 완료를 위한 로컬 머지 및 브랜치 자율 정비
    *   [.agents/skills/agent_hooks/SKILL.md](.agents/skills/agent_hooks/SKILL.md) (로컬): 세션 장애 SQLite 로그 학습 기억 연계

### [knowledge-curator-agent (Knowledge Curator Agent)](.agents/agents/roles/knowledge-curator-agent.md)
*   **본질적 임무**: 완수된 아키텍처 지식의 자율 큐레이션, 위키 린트 검증 및 지식 그래프와의 동기화를 수행합니다.
*   **권장 및 필수 가동 스킬**:
    *   [.agents/skills/knowledge-capture/SKILL.md](.agents/skills/knowledge-capture/SKILL.md) (로컬): 세션종료 지식 자율 캡처, 위키 자동 마이그레이션 및 정합성 린트
    *   `understand` (글로벌): 최신 구현 소스를 지식 그래프(.understand-anything/knowledge-graph.json) 상에 유기적으로 추가

### [documentation-agent (Documentation Agent)](.agents/agents/roles/documentation-agent.md)
*   **본질적 임무**: 기술 설계 문서, API 명세, 아키텍처 결정 레코드(ADR)를 조밀하게 마크다운에 영속 기록합니다.
*   **권장 및 필수 가동 스킬**:
    *   [.agents/skills/knowledge-capture/SKILL.md](.agents/skills/knowledge-capture/SKILL.md) (로컬): 산출 기술 사양 문서의 WSL 링크 및 린트 정밀 정비
    *   `writing-plans` (글로벌): 정교한 명세서 포맷 조립 기획

### [prompt-optimizer-agent (Prompt Optimizer Agent)](.agents/agents/roles/prompt-optimizer-agent.md)
*   **본질적 임무**: 에이전트별 행동 규칙 프롬프트의 불필요 토큰 압축 및 지침 자율 자가 튜닝을 지휘합니다.
*   **권장 및 필수 가동 스킬**:
    *   `skill-creator` (글로벌): 에이전트 성능 평가 및 지시 정확도 자가 튜닝 성능 측정
    *   `writing-skills` (글로벌): 프롬프트 수정 전후의 정상 구동 검정 통과율 유효성 검증
