---
id: skill.index
title: "Ref: SKILLS > INDEX"
type: reference
status: active

summary: >
  에이전트 스킬 인덱스 및 기동 타이밍 가이드.
  프로젝트 내 모든 스킬들의 기동 시점과 관계도를 색인화하여 관리한다.

keywords:
  - skills
  - index
  - timing
  - triggers

parent: concept.context

related:
  - "[[rules/L2-sync-policy.md]]"
  - "[[context/infra/hooks-specification.md]]"

consumers:
  - agent.all

updated: 2026-06-28
---


# 에이전트 스킬 인덱스 및 기동 타이밍 가이드 (skills/index.md)

## Overview / Connections
* **Parent (상위 개념)**: [[AGENTS.md]]
* **Related (연관 문서)**:
  * [[rules/L2-sync-policy.md]] (자산 동기화 정책)
  * [[context/infra/hooks-specification.md]] (품질 릴리즈 훅 규격)

---


본 문서는 프로젝트 내의 모든 활성 AI 에이전트들이 복잡한 스킬셋 중 적합한 지침을 즉각적으로 파악하고 가동할 수 있도록 돕는 **스킬 기동 시점 색인(Index) 정의서**입니다.

에이전트는 요구사항을 수신한 즉시 아래 정의된 트리거 타이밍을 탐색하여 최적의 스킬을 `view_file` 도구로 습득하십시오.

---

## 1. 개발 수명 주기(SDLC) 단계별 핵심 스킬

### ① 기획 및 의도 정렬 단계 (Planning)
*   **스킬명**: [brainstorming](.agents/skills/brainstorming/SKILL.md)
    - **기동 타이밍**: 새로운 기능을 설계하거나 코드 수정을 본격 착수하기 전, 사용자의 잠재적 의도와 요구사항을 실시간으로 정합하고 브레인스토밍할 때 반드시 먼저 실행합니다.
*   **스킬명**: [writing-plans](.agents/skills/writing/plans/SKILL.md)
    - **기동 타이밍**: 복잡한 요구사항이나 다단계 리팩토링 설계가 제시되었을 때, 실제 소스 코드를 수정하기 전에 완벽한 순차 구현 계획서(Markdown 체크리스트 양식)를 수립할 때 사용합니다.

### ② 구현 및 특화 설계 단계 (Implementation)
*   **스킬명**: [developing-with-streamlit](.agents/skills/development/streamlit/SKILL.md)
    - **기동 타이밍**: Streamlit 기반 대시보드 화면 개발, 탭 구성, 세션 상태 관리(Session State), CSS 스타일링 주입, 또는 로딩 성능 최적화(Caching, Fragment) 작업을 처리할 때 언제나 가동합니다.
*   **스킬명**: [frontend-design](.agents/skills/development/design/SKILL.md)
    - **기동 타이밍**: 프리미엄 룩앤필 및 비주얼 디자인 시스템(일관된 타이포그래피 위계, 그리드 시스템, IBM Carbon 스타일 등)을 구현하여 완성도 높은 대시보드 미학을 구성하고자 할 때 사용합니다.
*   **스킬명**: [test-driven-development](.agents/skills/development/tdd/SKILL.md)
    - **기동 타이밍**: 소스 코드 작성 전에 먼저 독립된 검증용 테스트 케이스를 설계하여 구현의 코드 무결성을 선제적으로 확보하려 할 때 기동합니다.
*   **스킬명**: [using-git-worktrees](.agents/skills/development/worktrees/SKILL.md)
    - **기동 타이밍**: 현재 워크스페이스의 수정 중인 상태와 격리하여 새로운 피처 브랜치 작업을 병렬로 완수해야 할 때 독립 작업 디렉토리를 분기하기 위해 사용합니다.

### ③ 소스 코드 품질 검역 및 자율 리뷰 단계 (Quality Gates)
*   **스킬명**: [guardrail](.agents/skills/quality/guardrail/SKILL.md)
    - **기동 타이밍**: 작성된 코드를 커밋/푸시하거나 배포하기 전, 소스 트리 내에 잔존 유니코드 이모지가 없는지, 커밋 메시지가 규격을 지켰는지, SQLite 골든 스키마가 일치하는지 종합 스캔할 때 기동합니다.
*   **스킬명**: [sql_analyzer](.agents/skills/quality/sql/SKILL.md)
    - **기동 타이밍**: SQL 쿼리 내부에 디스플레이용 한글 별칭(AS "한글")이 하드코딩되었는지 여부나 SQL 5대 아키텍처 제약 사항 위배 여부를 정적으로 스캔할 때 사용합니다.
*   **스킬명**: [korean_metadata](.agents/skills/quality/korean-metadata/SKILL.md)
    - **기동 타이밍**: 영문 원천 테이블 물리 컬럼에 매핑되는 디스플레이 한글명, 소수점 포맷, 마우스 호버 툴팁 등의 메타데이터 사전을 신규 생성하거나 업데이트할 때 사용합니다.
*   **스킬명**: [requesting-code-review](.agents/skills/quality/request-review/SKILL.md)
    - **기동 타이밍**: 구현 완료된 분량을 검증계에 넘기기 직전, 변경점이 PRD 요구사항 및 3-Layer 격리 수칙과 정확히 부합하는지 자율적으로 정합성을 사전 검사할 때 실행합니다.
*   **스킬명**: [receiving-code-review](.agents/skills/quality/receive-review/SKILL.md)
    - **기동 타이밍**: 리뷰어 서브에이전트나 인간의 피드백을 전달받아, 기계적으로 적용하지 않고 엄격한 기술적 가설 입증 및 무결성 조정을 거쳐 패치할 때 기동합니다.

### ④ 릴리즈 및 마무리 단계 (Release)
*   **스킬명**: [verification-before-completion](.agents/skills/quality/verify-completion/SKILL.md)
    - **기동 타이밍**: 작업을 종료하고 성공을 주장하기 전에, 실제 빌드 정적 컴파일(`py_compile`), 린트, 테스트 스위트 구동 등의 구체적인 증거(Evidence) 데이터를 획득하여 무결함을 확증할 때 반드시 기동합니다.
*   **스킬명**: [finishing-a-development-branch](.agents/skills/finishing-a-development-branch/SKILL.md)
    - **기동 타이밍**: 모든 단위 테스트가 통과된 후 변경 사항을 로컬 메인에 병합(Merge)하거나 PR 생성, 피처 브랜치 삭제 및 임시 워크트리 정리 등 일련의 릴리즈 흐름을 실행할 때 사용합니다.

---

## 2. 분석 및 디버깅 가속화 스킬 (Analysis & Debugging)

*   **스킬명**: [understand](.agents/skills/understand/SKILL.md)
    - **기동 타이밍**: 대규모 코드베이스의 물리 계층(UI-Service-Query) 흐름을 진단하거나, 모듈 간 결합 관계 지식 그래프를 렌더링하고, 영향 범위(Impact Area)를 계산하거나 신규 사원을 위한 온보딩 가이드를 수립할 때 통합 가동합니다.
*   **스킬명**: [systematic-debugging](.agents/skills/development/debugging/SKILL.md)
    - **기동 타이밍**: 테스트 케이스가 오작동하거나 런타임 예외가 발생했을 때, 추측을 배제하고 과학적인 가설-검증 단계를 거쳐 버그의 원인 영역을 체계적으로 추려 고치고자 할 때 기동합니다.
*   **스킬명**: [commit-context](.agents/skills/memory/commit-context/SKILL.md)
    - **기동 타이밍**: 특정 파일의 코드가 언제, 어떤 세션 맥락에서 작성되었는지, 변경 배후에 숨겨진 기획 요구사항을 추적하여 "왜 이 코드가 작성되었는가"를 심도 있게 조회할 때 사용합니다.
*   **스킬명**: [commit-history](.agents/skills/memory/commit-history/SKILL.md)
    - **기동 타이밍**: 에이전트 세션들과 긴밀하게 연계된 최근 Git 커밋 로그를 신속히 탐색하고 필터링해보고 싶을 때 사용합니다.

---

## 3. 에이전트 자율 환경 및 메모리 수호 스킬 (Infrastructure & Memory)

*   **스킬명**: [agent_hooks](.agents/skills/agent_hooks/SKILL.md)
    - **기동 타이밍**: 자율 세션의 시작/진행/마무리 전반에 대한 런타임 수명 주기를 모니터링하고, 에러 로그 분석, WSL 오작동 자동 감색 및 예방 체크리스트를 역동기화하고자 할 때 관리 기동합니다.
*   **스킬명**: [agentmemory](.agents/skills/memory/core/SKILL.md)
    - **기동 타이밍**: 단기/장기 에이전트 기억을 보관하는 서버, MCP 연동 어댑터, 자동 주기 훅 및 REST 엔드포인트 명세를 확인하고 이를 확장/연결하고자 할 때 가동합니다.
*   **스킬명**: [using-superpowers](.agents/skills/using-superpowers/SKILL.md)
    - **기동 타이밍**: 새로운 대화 콘텍스트가 시작될 때 가용한 비즈니스 스킬의 존재 유무와 수칙 가이드들을 신속하게 매칭하여 습득할 때 기동합니다.
*   **스킬명**: [remember](.agents/skills/memory/remember/SKILL.md)
    - **기동 타이밍**: 개발 중 축적된 소중한 로컬 아키텍처 규칙, 중요 설계 의사결정 사항, 혹은 장애 복구 교훈을 ChromaDB 장기 벡터 기억 저장소에 안전하게 기록할 때 사용합니다.
*   **스킬명**: [recall](.agents/skills/memory/recall/SKILL.md)
    - **기동 타이밍**: 현재 직면한 기술 문제나 소스 환경이 이전에 분석되었거나 구현해 보았던 사항인지 하이브리드(BM25, 벡터, 그래프) 검색을 거쳐 과거 세션 메모리에서 회상해 내고자 할 때 실행합니다.
*   **스킬명**: [forget](.agents/skills/memory/forget/SKILL.md)
    - **기동 타이밍**: 잘못 기입되었거나 보안상의 이유로 에이전트 메모리에서 영구히 지워야 하는 단/장기 관측 데이터를 안전하게 영구 소거할 때 기동합니다.
*   **스킬명**: [recap](.agents/skills/memory/recap/SKILL.md)
    - **기동 타이밍**: 최근 프로젝트 내에서 이루어진 에이전트 세션들의 일자별 변경 사안을 한눈에 조감하여 파악하고자 할 때 요약 실행합니다.
*   **스킬명**: [session-history](.agents/skills/memory/session-history/SKILL.md)
    - **기동 타이밍**: 워크스페이스의 이전 세션 이력을 타임라인 구조로 간결하게 시각화하여 현재 작업의 연속성을 측정하고자 할 때 사용합니다.
*   **스킬명**: [handoff](.agents/skills/collaboration/handoff/SKILL.md)
    - **기동 타이밍**: 세션 인계 후 새로운 에이전트가 이전의 마지막 질문이나 해결 과제 맥락을 즉각적으로 도출하여 개발을 연속 이행하려 할 때 실행합니다.

---

## 4. 기타 유틸리티 보조 스킬 (Utility Helpers)

*   **스킬명**: [humanizer](.agents/skills/humanizer/SKILL.md)
    - **기동 타이밍**: AI가 생성해 낸 다소 번역투 같고 어색한 한글 가이드 문서, 주석, 오류 피드백 텍스트를 고품질 국어학적 분석을 거쳐 정교하고 매끄러운 인간의 서술조 언어로 정제할 때 가동합니다.
*   **스킬명**: [karpathy-guidelines](.agents/skills/karpathy-guidelines/SKILL.md)
    - **기동 타이밍**: 코딩 실수나 비대해지는 설계를 사전 차단하고, 가장 직관적이면서 수술식 변경(Surgical Edit)을 관철하는 Karpathy 개발 대원칙을 준수하고자 할 때 사용합니다.
*   **스킬명**: [find-skills](.agents/skills/find-skills/SKILL.md)
    - **기동 타이밍**: 구현 요구 사항을 만나 가용할 추가 확장 스킬을 탐색 및 다운로드하거나 등록하고 싶을 때 지칭합니다.
*   **스킬명**: [writing-skills](.agents/skills/writing/skills/SKILL.md)
    - **기동 타이밍**: 새로운 스킬 폴더를 신설하고 YAML 프론트매터 및 세부 행동 규칙을 제정하여 영속화하려 할 때 기동합니다.
*   **스킬명**: [executing-plans](.agents/skills/collaboration/execute-plans/SKILL.md)
    - **기동 타이밍**: 완성된 구현 기획을 병렬 혹은 체크포인트 검증 검사를 동반하여 신중하게 순차적으로 완수하려 할 때 구동합니다.
*   **스킬명**: [dispatching-parallel-agents](.agents/skills/collaboration/parallel-agents/SKILL.md)
    - **기동 타이밍**: 두 개 이상의 서로 영향이 없는 완전 독립적인 구현 과제나 정적 검증 임무를 복수의 서브에이전트에게 동시 분산 기동할 때 활용합니다.
*   **스킬명**: [subagent-driven-development](.agents/skills/collaboration/subagent-development/SKILL.md)
    - **기동 타이밍**: 복수의 서브에이전트들을 기동하여 체계적으로 병렬 위임 및 단계별 정합성 평가 흐름을 총괄 오케스트레이션 개발하고자 할 때 전격 가동합니다.
