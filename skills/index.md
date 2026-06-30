---
id: skill.index
title: "[Skill] Index"
type: reference
status: active

summary: >
  에이전트 통합 매크로 스킬 인덱스, 메타데이터 정보 관리 및 기동 타이밍 가이드.
  로컬 워크스페이스 전용 스킬(Local Keep)과 글로벌 환경에서 탑재되어 수동 연동될 외부 스킬(Global)을 이원화하고 설치/업데이트 형상 메타데이터를 통합 보존한다.

keywords:
  - skills
  - index
  - routing
  - metadata

parent: concept.context

related:
  - "[rules/rules-index.md](../rules/rules-index.md)"
  - "[AGENTS.md](../AGENTS.md)"

consumers:
  - agent.all

updated: 2026-06-30
---

# 에이전트 통합 매크로 스킬 인덱스 (skills/index.md)

본 문서는 프로젝트 내의 모든 활성 AI 에이전트들이 복잡한 스킬셋 중 적합한 지침을 즉각적으로 파악하고 가동할 수 있도록 돕는 **통합 매크로 스킬 기동 타이밍 색인 및 메타데이터 이력 관리 정의서**입니다.

정례화 규칙에 따라 본 문서는 로컬 워크스페이스(Workspace-specific) 전용 스킬과 글로벌 저장소(Global System-wide)에서 직접 탑재되어 상속되는 외부 스킬군을 격리 분류하고, 이들의 설치 및 업데이트 이력 메타데이터를 통합 형상 관리합니다.

---

## 1. 4대 활성 통합 매크로 스킬 맵 및 기동 타이밍

에이전트는 수행 중인 개발 라이프사이클 단계 및 작업 목적에 맞춰 아래 테이블 기준 **단 1개의 통합 스킬 파일**만 선택하여 로드하십시오.

| 대분류 스킬 | 타겟 스킬 파일 | 기동 타이밍 및 에이전트 행동 수칙 (설명문 한글화 준수) |
| :--- | :--- | :--- |
| **품질 검역 & 리뷰** | [quality-assurance/SKILL.md](quality-assurance/SKILL.md) | 구현 완료 후 배포 전, 소스 가드레일 스캔, SQL 쿼리 정적 분석, 메타데이터 연동, 자가 정적 컴파일 및 Mock 단위 테스트 기동 등 5대 품질 관문(Quality Gate)을 순서대로 격리 완수하려 할 때 실행합니다. |
| **기억 & 컨텍스트** | [memory/core/SKILL.md](memory/core/SKILL.md) | 에이전트의 단기/장기 기억을 보관(remember)하거나 회상(recall)하고, 불필요한 관측 데이터를 소거(forget)하며, 세션 이력을 일자별로 조감 요약(recap)하여 기억 간 무결성을 확보할 때 가동합니다. |
| **환경 훅 & 인계** | [agent_hooks/SKILL.md](agent_hooks/SKILL.md) | WSL 가상 환경의 역동기화 오작동을 자동 방어하고, 세션 실행 중의 SQLite 장애 원인을 실시간 로그 분석 수렴하며, 세션 종료 직전 다음 에이전트로 명확히 개발 콘텍스트를 인계(handoff)할 때 기동합니다. |
| **지식 & 품질 루프** | [knowledge-capture/SKILL.md](knowledge-capture/SKILL.md) | 카파시 코딩 가이드라인 검정, 마크다운/링크 린트, 세션종료 지식 자율 수확 및 위키 설계/Index 동기화까지 하나의 통합 수명 주기 루프를 실행하고자 할 때 가동합니다. |

---

## 2. Workspace-specific Local Keep Skills (워크스페이스 정의 스킬 및 메타정보)

이 프로젝트의 중추적인 비즈니스 룰, WSL 환경 특화 인프라, SQLite 및 Streamlit 고유 한계 극복 기법, 전용 데이터 정합성 도구들과 100% 밀착되어 로컬 영역(`.agents/skills/`) 하위에서 관리되는 핵심 독자 자산 형상 정보입니다.

| 스킬 식별자 | 위치 (상대 경로) | 최초 설치일 | 최종 업데이트일 | 버전 | 상태 | 스킬 설명문 (한글 기술 표준) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **quality-assurance** | [quality-assurance/SKILL.md](quality-assurance/SKILL.md) | 2026-06-28 | 2026-06-30 | v1.2.0 | Active | 코드 배포 전 정적 무결성 검증, SQL 정적 분석, 메타데이터 동기화, 자가 컴파일 및 자율 테스트 검증을 수립하는 최상위 관문 품질 매크로 스킬입니다. |
| **guardrail** | [quality/guardrail/SKILL.md](quality/guardrail/SKILL.md) | 2026-06-28 | 2026-06-30 | v1.1.0 | Active | 에이전트 배포 전 이모지 존재 유무 검출, 커밋 메시지 규격 표준 검정, 데이터베이스 물리 골든 스키마 유효성을 사전 진증하는 정적 가드레일 스킬입니다. |
| **sql_analyzer** | [quality/sql/SKILL.md](quality/sql/SKILL.md) | 2026-06-28 | 2026-06-30 | v1.0.0 | Active | SQL 쿼리 파일 내에 디스플레이용 한글 AS 별칭이 하드코딩되었는지, 혹은 SQL 5대 불변 규칙을 위배했는지 감지하여 진단하는 쿼리 정적 분석기입니다. |
| **korean_metadata** | [quality/korean-metadata/SKILL.md](quality/korean-metadata/SKILL.md) | 2026-06-28 | 2026-06-30 | v1.0.0 | Active | 원천 DB 영문 물리 컬럼명에 대응하는 디스플레이용 한글 명칭, 소수점 포맷팅, 툴팁 설명 등의 정적 딕셔너리를 자동 매핑 및 업데이트해 주는 도구입니다. |
| **agent_hooks** | [agent_hooks/SKILL.md](agent_hooks/SKILL.md) | 2026-06-28 | 2026-06-30 | v1.2.0 | Active | WSL 가상 환경 역동기화를 차단하고, 세션 실행 중 SQLite 장애를 실시간 로그 분석하며, 종료 시점에 완벽한 컨텍스트 Handoff를 인계 처리하는 수명 주기 툴킷입니다. |
| **knowledge-capture** | [knowledge-capture/SKILL.md](knowledge-capture/SKILL.md) | 2026-06-29 | 2026-06-30 | v2.0.0 | Active | 카파시 코딩 가이드라인, 링크 린트 스크립트 검증, 설계결정 지식 캡처(Raw), 위키 작성 및 Index 정합성 최적화를 아우르는 지식 자산 케어 시스템입니다. |
| **agentmemory** | [memory/core/SKILL.md](memory/core/SKILL.md) | 2026-06-29 | 2026-06-30 | v1.1.0 | Active | 에이전트 장단기 기억 저장 서버의 구성, 자동 라이프사이클 훅 연동, CLI 포트 매핑 및 연결용 클라이언트 배선 어댑터 규정 지침 스킬입니다. |

---

## 3. Global System-wide Skills (글로벌 탑재 수동 연동 외부 스킬 및 메타정보)

프로젝트 고유의 비즈니스 코드에 종속되지 않고 범용적으로 재사용이 가능하여, 사용자가 외부 스킬 저장소로부터 글로벌 영역(`/home/jumasi/.gemini/config/skills/` 등)에 직접 수동으로 설치 및 연동하여 사용되는 스킬 형상 정보입니다.

| 스킬 식별자 | 최초 셋업일 | 최종 동기화일 | 원천 버전 | 탑재 상태 | 스킬 설명문 (한글 기술 표준) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[Superpowers] using-superpowers** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 대화형 세션 기동 시 요구사항 파악 전 에이전트 능력 자율 탐색 및 사전 스킬 준비 기법을 규정한 초기화 소통 툴킷입니다. |
| **[Superpowers] brainstorming** | 2026-06-30 | 2026-06-30 | v2.2.0 | Active | [Superpowers] 개발 구현 이전에 사용자 기획 의도를 엄격히 도출하고 다각도의 아키텍처 타당성 검증을 거쳐 의도를 선제 정렬하기 위한 브레인스토밍 스킬입니다. |
| **find-skills** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | 요구 기능을 바탕으로 에이전트 자율 스킬 저장소 라이브러리를 탐색하고 조준 적재하기 위한 자율 탐색 지원 기능입니다. |
| **skill-creator** | 2026-06-30 | 2026-06-30 | v1.3.0 | Active | 새로운 스킬을 자율 정의하고 Evals 컴파일 및 정확도 성능 평가(Benchmark)를 가동하여 에이전트의 능력을 개선하는 창작 가이드입니다. |
| **[Superpowers] finishing-a-development-branch** | 2026-06-30 | 2026-06-30 | v1.1.0 | Active | [Superpowers] 개발 구현 및 로컬 빌드 검증이 완수된 브랜치를 Merge, PR 서술 작성, 임시 브랜치 자율 정리를 통해 마감하고 배포 대기 상태로 유도하는 마무리 가이드입니다. |
| **understand** | 2026-06-30 | 2026-06-30 | v2.0.0 | Active | 코드베이스 전체 구조 관계를 조감하고, 아키텍처, 컴포넌트, 그리고 그 관계를 지식 그래프(.understand-anything/knowledge-graph.json)로 시각화 분석하는 아키텍처 이해 도구입니다. |
| **[Superpowers] writing-plans** | 2026-06-30 | 2026-06-30 | v1.2.0 | Active | [Superpowers] 복잡한 피처 구현 계획을 마크다운 체크리스트 형태로 쪼개어 수립하고 빌드 컴파일 검증을 강제하는 개발 기획 표준 툴킷입니다. |
| **[Superpowers] writing-skills** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 워크스페이스 내에 에이전트 독자 스킬 규격을 안전하게 추가하거나 `skills.json`에 형상을 정상 등록하기 위한 작성 절차 지침서입니다. |
| **[Superpowers] subagent-driven-development** | 2026-06-30 | 2026-06-30 | v3.0.0 | Active | [Superpowers] 구글 안티그래비티 Superpowers 내장 협업 가이드로, 독립된 서브에이전트들에게 일감을 분배하고 품질 리뷰를 수행하며 총괄 조율하는 오케스트레이션 툴입니다. |
| **[Superpowers] dispatching-parallel-agents** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 공유 상태나 순차적 의존성 없이 독립적으로 처리할 수 있는 2개 이상의 병렬 작업을 만났을 때 사용하며, 여러 에이전트를 동시에 런칭하여 신속하게 수행하도록 지원합니다. |
| **[Superpowers] executing-plans** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 작성된 구현 계획이 있을 때 사용하며, 검증 및 리뷰 체크포인트가 있는 별도의 격리된 세션에서 계획을 체계적으로 실행하도록 돕습니다. |
| **[Superpowers] receiving-code-review** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 코드 리뷰 피드백을 수신했을 때, 제안을 구현하기 전에 사용합니다. 기계적인 동의 대신 기술적 엄격함과 철저한 검증이 필요할 때 가동합니다. |
| **[Superpowers] requesting-code-review** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 작업을 완료했거나, 주요 기능을 구현했거나, 혹은 머지하기 전에 작업물이 요구사항을 완벽히 충족하는지 검증하고 코드 리뷰를 요청할 때 사용합니다. |
| **[Superpowers] systematic-debugging** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 버그, 테스트 실패 또는 예기치 않은 동작을 발견했을 때, 성급하게 해결책을 제시하기 전에 원인을 체계적으로 디버깅하고 추적하기 위해 사용합니다. |
| **[Superpowers] test-driven-development** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 기능 구현이나 버그 수정을 시작할 때, 실제 구현 코드를 작성하기 전에 테스트 주도 개발(TDD)을 가동하기 위해 사용합니다. |
| **[Superpowers] using-git-worktrees** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 현재 작업 영역과 격리해야 하는 새로운 피처 개발을 시작하거나, 구현 계획을 실행하기 전에 사용합니다. git worktree 폴백을 통해 독립된 워크스페이스를 확보합니다. |
| **[Superpowers] verification-before-completion** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | [Superpowers] 작업이 완료되었거나 수정되었다고 선언하기 전, 커밋이나 PR 생성 전 반드시 검증 명령어를 실행하고 출력을 증거 기반으로 검정합니다. |
| **frontend-design** | 2026-06-30 | 2026-06-30 | v1.0.0 | Active | 독창적이고 의도적인 비주얼 웹 디자인과 고급 타이포그래피, 맞춤형 테마 및 레이아웃 설계를 수립하기 위한 프론트엔드 전문 디자인 스킬입니다. |

---

## 4. 에이전트 지연 스킬 로딩 및 정례화 프로토콜

1. **사전 탐색**: 작업을 시작하기 전, 에이전트는 무조건 본 `skills/index.md`만 먼저 읽어 현재 시점에 요구되는 매크로 스킬 1개를 조준 분류합니다.
2. **설명 한글화 사수**: 어떠한 경우에도 스킬에 기술하는 부가 가이드 및 설명글은 본 가이드에 명문화된 대로 **오직 한국어(Korean)로만 기술**하여 일관된 협업을 도모해야 합니다.
3. **증거 기반 종결**: 특히 `quality-assurance` 기동 시에는 모든 체크리스트를 정량적으로 통과하고 정적 검증(`verify_code.py`) 성공 Evidence 출력을 완료해야만 성공을 최종 선언할 수 있습니다.
