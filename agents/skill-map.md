---
id: map.agent_skill
title: "[Skill Map]"
type: wiki
status: active

summary: >
  에이전트별 필수 기동 스킬 맵핑 정의서.
  각 에이전트 페르소나가 완수해야 할 가동 스킬들을 명시한다.

keywords:
  - agent-os
  - skill-map
  - capabilities

parent: concept.agent_os.governance

related:
  - "[[agents/agents.md]]"
  - "[[skills/using-superpowers/SKILL.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"

updated: 2026-06-28
---
# 에이전트별 필수 기동 스킬 맵핑 정의서 (agents/skill-map.md)

## Overview
* **왜 존재하는가 (Why)**: 각 에이전트 페르소나가 자기 기동 단계 및 기능에 맞춰 올바른 스킬셋(Tool)을 학습하고 적소에 오작동 없이 사용하도록 정의하기 위함입니다.
* **언제 사용하는가 (When)**: 새로운 스킬을 에이전트 라이프사이클에 이식하거나, 특정 에이전트 페르소나의 권한과 가동 규칙을 변경할 때 사용합니다.
* **연계 실행 (Next Action)**: 전체 에이전트 규정을 담은 [.agents/agents/agents.md](.agents/agents/agents.md)를 연이어 참조하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](.agents/AGENTS.md)
* **연관 자산**: [.agents/agents/agents.md](.agents/agents/agents.md) | [.agents/skills/index.md](.agents/skills/index.md)
---

본 문서는 프로젝트 내에서 고유한 역할 페르소나를 지니고 협업하는 각 AI 에이전트가 어떤 스킬을 핵심적으로 기동하고 활용해야 하는지 명시한 **에이전트-스킬 물리 연동 정의서**입니다.

에이전트는 자신의 정체성(Identity)과 담당 단계에 맞추어 필수 매핑 스킬들을 최우선적으로 습득 및 실행하십시오.


## 1. 최상위 설계 및 기획 에이전트 (Planner Agent)

### [Planner Orchestrator (최상위 기획 에이전트)](.agents/agents/roles/planner-orchestrator.md)
*   **본질적 임무**: 사용자 요구사항을 분석하고, `prd-template.md`에 의거한 완전한 PRD 기획서를 수립하며, 빌더 에이전트들의 구현 방향과 단계별 기획 체크리스트를 총괄 지휘합니다.
*   **권장 및 필수 가동 스킬**:
    *   [using-superpowers](.agents/skills/using-superpowers/SKILL.md): 세션 시작 즉시 활용 가능한 비즈니스 규칙 및 인프라 지침 탐색
    *   [brainstorming](.agents/skills/brainstorming/SKILL.md): 설계 단계 전 사용자와의 실시간 의도 합치 및 디자인 맵핑
    *   [writing-plans](.agents/skills/writing/plans/SKILL.md): 코드 변경 전에 완벽한 단계별 순차 구현 계획서(SDDD) 구축
    *   [understand](.agents/skills/understand/SKILL.md): 전체 코드 아키텍처 및 영향 범위(Impact Area) 사전 점검
    *   [handoff](.agents/skills/collaboration/handoff/SKILL.md) / [session-history](.agents/skills/memory/session-history/SKILL.md): 이전 세션의 미해결 과제와 흐름 신속 연속 이행
    *   [recall](.agents/skills/memory/recall/SKILL.md) / [remember](.agents/skills/memory/remember/SKILL.md): 과거 세션 메모리 내의 기획 핵심 이정표 회상 및 신규 로컬 아키텍처 규칙 영속화

---

## 2. 프로덕션 구현 및 최적화 빌더 에이전트 (Builder Agent)

### [Data Layer Builder (쿼리 및 전처리 개발 에이전트)](.agents/agents/roles/data-layer-builder.md)
*   **본질적 임무**: 데이터베이스 원천 테이블의 DDL을 파악하고, `app/queries/` 하위에 고품질 SQL 쿼리를 작성하며, `app/service/` 하위에서 Pandas를 활용해 지표 연산 및 `@st.cache_data` 전처리 공급 로직을 개발합니다.
*   **권장 및 필수 가동 스킬**:
    *   [understand](.agents/skills/understand/SKILL.md): 데이터 흐름도 생성 및 원천 데이터베이스 DDL/스키마 관계 정밀 분석
    *   [sql_analyzer](.agents/skills/quality/sql/SKILL.md): SQL 쿼리 내 하드코딩된 한글 별명(AS "한글") 배제 및 아키텍처 수칙 검역
    *   [korean_metadata](.agents/skills/quality/korean-metadata/SKILL.md): 컬럼 설명 사전을 갱신하여 쿼리-UI 간 디스플레이용 한글 포맷 정합성 정렬
    *   [systematic-debugging](.agents/skills/development/debugging/SKILL.md): 쿼리 실행 실패 및 전처리 Pandas 데이터 타입 에러의 체계적 가설 추적 및 해소
    *   [test-driven-development](.agents/skills/development/tdd/SKILL.md): 원천 데이터 공급 모듈 작성 전 견고한 데이터 모킹(Mocking) 및 단위 테스트 설계
    *   [verification-before-completion](.agents/skills/quality/verify-completion/SKILL.md): 전처리 및 쿼리 파이썬 파일 정적 컴파일(`py_compile`) 및 무결 정합 입증

### [Dashboard Layer Builder (화면 및 시각화 조립 에이전트)](.agents/agents/roles/dashboard-layer-builder.md)
*   **본질적 임무**: `app/pages/` 하위에 Streamlit UI 레이아웃을 작성하고, 프리미엄 Plotly 시각화 오브젝트(`*_plots.py`)를 개발하며, 네비게이션 매핑, CSS 앰비언트 인젝션 및 유니코드 이모지 Google Material Symbols 치환 등 비주얼 고도화 작업을 완수합니다.
*   **권장 및 필수 가동 스킬**:
    *   [developing-with-streamlit](.agents/skills/development/streamlit/SKILL.md): Streamlit 앱 구축 수칙, 세션 상태 가로채기, 캐싱 및 반응형 성능 튜닝
    *   [frontend-design](.agents/skills/development/design/SKILL.md): 글래스모피즘, 화이트 카드 컨테이너 포장, 정돈된 타이포그래피 정렬 등의 미학적 디테일 극대화
    *   [humanizer](.agents/skills/humanizer/SKILL.md): 화면 내 탭 라벨, 경고창, 수치 요약 텍스트 및 주석을 가장 자연스럽고 세련된 한국어 텍스트로 치환
    *   [systematic-debugging](.agents/skills/development/debugging/SKILL.md): Streamlit 위젯 세션 강제 변경 오류(StreamlitAPIException) 및 렌더링 루프 병목 자율 추적 및 교정
    *   [verification-before-completion](.agents/skills/quality/verify-completion/SKILL.md): UI 컨트롤러 및 차트 시각화 모듈의 빌드 정상 작동 확인 및 최종 렌더링 무결 증명

---

## 3. 분석, 리뷰 및 검역 서브에이전트 (Sub-Agent)

### [Data Insights Analyst (사전 분석 서브에이전트)](.agents/agents/roles/data-insights-analyst.md)
*   **본질적 임무**: 본격적인 개발 작업 착수 전, 데이터베이스의 Read-Only DDL과 로우 레벨 메타 통계를 자율 검증하여 비즈니스 맥락과 융합한 정밀 EDA 가이드북을 작성해 둡니다.
*   **권장 및 필수 가동 스킬**:
    *   [understand](.agents/skills/understand/SKILL.md): 신규 추가될 테이블 구조 분석 및 비즈니스 도메인 지식 흐름 추출
    *   [recall](.agents/skills/memory/recall/SKILL.md) / [remember](.agents/skills/memory/remember/SKILL.md): 유사 도메인 지표(OEQG, MTTC 등) 연산 수식의 과거 지식 베이스 검색 및 기록 연계

### [Governance Compliance Auditor (사전/사후 검역 서브에이전트)](.agents/agents/roles/governance-compliance-auditor.md)
*   **본질적 임무**: 파일, 함수, 변수 및 DB 영문 원천 물리 컬럼과 UI 한글명 간의 1:1 디스플레이 매핑 표준 및 3-Layer 물리 명명 규정을 검역하고 메타데이터 json 수정을 동기화합니다.
*   **권장 및 필수 가동 스킬**:
    *   [guardrail](.agents/skills/quality/guardrail/SKILL.md): 이모지 혼용 검역, 커밋 메시지 규격 검사, 데이터베이스 스키마와 물리 테이블 정적 구조 유효성 정밀 검정
    *   [sql_analyzer](.agents/skills/quality/sql/SKILL.md): SQL 구문 내 불법 영문 Alias 하드코딩 여부 정밀 정적 분석
    *   [korean_metadata](.agents/skills/quality/korean-metadata/SKILL.md): 영문 물리 컬럼명에 매칭되는 한국어 디스플레이 사전 자동 업데이트 연동
    *   [verification-before-completion](.agents/skills/quality/verify-completion/SKILL.md): 검역 결과가 완벽한지 테스트 스위트를 구동하여 물리적 무오류 보증

### [Code Reviewer (리뷰어 서브에이전트)](.agents/agents/roles/code-reviewer.md)
*   **본질적 임무**: 구현 빌더들이 제안한 파이썬 소스 코드의 잠재 버그 및 규칙 위반 사항을 검진하고, 리팩토링 개선안(Diff)을 주도적이고 가독성 높게 설계하여 피드백합니다.
*   **권장 및 필수 가동 스킬**:
    *   [receiving-code-review](.agents/skills/quality/receive-review/SKILL.md) / [requesting-code-review](.agents/skills/quality/request-review/SKILL.md): 코드 변경점의 PRD 충족도, 스타일 규정 위반 및 잠재적인 부작용(Side Effect)의 정교한 크로스 체크
    *   [commit-context](.agents/skills/memory/commit-context/SKILL.md) / [commit-history](.agents/skills/memory/commit-history/SKILL.md): 특정 소스 한 줄이 이전에 어떤 맥락(Session History)에서 도입되었는지 확인하여 불필요한 코드 리팩토링 간섭을 차단
    *   [karpathy-guidelines](.agents/skills/karpathy-guidelines/SKILL.md): 기저 가정의 노출, 코드 비대화 차단 및 수술식 수정(Surgical Edit)을 유도하는 Karpathy 개발 대원칙 준수

### [Quality Evaluator (평가 서브에이전트)](.agents/agents/roles/quality-evaluator.md)
*   **본질적 임무**: 로컬 하네스 테스트 자율 구동, 빌드 컴파일 무결 진증 및 PRD 정량 평가 스코어카드를 최종 기재하고 최종 릴리즈 게이트를 승인 제어합니다.
*   **권장 및 필수 가동 스킬**:
    *   [guardrail](.agents/skills/quality/guardrail/SKILL.md): 배포 직전 코드 이모지 규정 및 데이터 스키마 물리 매핑 유효성 최종 정밀 자율 통과 여부 검진
    *   [verification-before-completion](.agents/skills/quality/verify-completion/SKILL.md): `make verify` 등의 전수 단위 테스트 구동 지침 실행 및 에러 바운더리 검정 완수
    *   [finishing-a-development-branch](.agents/skills/finishing-a-development-branch/SKILL.md): 완치 확인 후 로컬 브랜치 안전 로컬 머지 및 워크트리 복원 마무리 실행
    *   [agent_hooks](.agents/skills/agent_hooks/SKILL.md): 자율 세션 실시간 로그 분석 및 장애 요인의 ChromaDB 장기 학습 기억 연계 등록 지휘
