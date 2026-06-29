---
id: skill.index
title: "[Skill] Index"
type: reference
status: active

summary: >
  에이전트 통합 매크로 스킬 인덱스 및 기동 타이밍 가이드.
  파편화된 마이크로 스킬들을 5대 대형 매크로 도메인 스킬로 수평 통합하여 인지 로드를 극적으로 낮춘다.

keywords:
  - skills
  - index
  - routing

parent: concept.context

related:
  - "[[rules/rules-index.md]]"

consumers:
  - agent.all

updated: 2026-06-29
---


# 에이전트 통합 매크로 스킬 인덱스 (skills/index.md)

본 문서는 프로젝트 내의 모든 활성 AI 에이전트들이 복잡한 스킬셋 중 적합한 지침을 즉각적으로 파악하고 가동할 수 있도록 돕는 **통합 매크로 스킬 기동 타이밍 색인(Index) 정의서**입니다.

에이전트는 요구사항을 수신한 즉시 아래 정의된 5대 통합 매크로 스킬 테이블을 탐색하여 최적의 스킬을 단일 `view_file` 도구로 습득하십시오.

---

## 1. 5대 통합 매크로 스킬 맵 및 기동 타이밍 (Macro Skills Loading Map)

에이전트는 수행 중인 개발 라이프사이클 단계 및 작업 목적에 맞춰 아래 테이블 기준 **단 1개의 통합 스킬 파일**만 선택하여 로드하십시오.

| 대분류 스킬 | 타겟 스킬 파일 | 기동 타이밍 및 에이전트 행동 수칙 |
| :--- | :--- | :--- |
| **품질 검역 & 리뷰** | [quality-assurance/SKILL.md](.agents/skills/quality-assurance/SKILL.md) | 구현 완료 후 배포 전, 소스 가드레일 스캔, SQL 쿼리 정적 분석, 메타데이터 연동, 자가 정적 컴파일 및 Mock 단위 테스트 기동 등 5대 품질 관문(Quality Gate)을 순서대로 격리 완수하려 할 때 실행합니다. |
| **기억 & 컨텍스트** | [agent-memory/SKILL.md](.agents/skills/agent-memory/SKILL.md) | 에이전트의 단기/장기 기억을 보관(remember)하거나 회상(recall)하고, 불필요한 관측 데이터를 소거(forget)하며, 세션 이력을 일자별로 조감 요약(recap)하여 기억 간 무결성을 확보할 때 가동합니다. |
| **기획 & 플랜** | [planning/SKILL.md](.agents/skills/planning/SKILL.md) | 새로운 피처 구현 및 다단계 대형 리팩토링 설계가 제시되었을 때, 본격 소스 코드 수정 전 인간의 의도를 실시간 정렬(brainstorming)하고 마크다운 체크리스트형 계획서를 수립 및 순차 이행하려 할 때 실행합니다. |
| **환경 훅 & 인계** | [agent-hooks/SKILL.md](.agents/skills/agent-hooks/SKILL.md) | WSL 가상 환경의 역동기화 오작동을 자동 방어하고, 세션 실행 중의 SQLite 장애 원인을 실시간 로그 분석 수렴하며, 세션 종료 직전 다음 에이전트로 명확히 개발 콘텍스트를 인계(handoff)할 때 기동합니다. |
| **지휘 & 확장** | [orchestration/SKILL.md](.agents/skills/orchestration/SKILL.md) | 신규 능력을 자율 확장하기 위해 스킬을 탐색/신설하거나, 두 개 이상의 독립 개발 업무를 다수의 서브에이전트에게 동시 병렬 위임하고 총괄 오케스트레이션 개발할 때 전격 가동합니다. |
| **지식 & 품질** | [knowledge-lint-curator/SKILL.md](.agents/skills/knowledge-lint-curator/SKILL.md) | 모든 마크다운 파일의 YAML Frontmatter 준수 여부를 자동으로 진단/보정(Lint)하고, 소스코드 수정 시 Wiki 및 Index 지식 자산의 동기화 결핍을 실시간으로 감지 차단하려 할 때 실행합니다. |

---

## 2. 에이전트 지연 스킬 로딩 프로토콜

1. **사전 탐색**: 작업을 시작하기 전, 에이전트는 무조건 본 `skills/index.md`만 먼저 읽어 현재 시점에 요구되는 매크로 스킬 1개를 조준 분류합니다.
2. **단일 로딩**: 탐색 완료 후, 지정된 해당 스킬의 마스터 파일(예: [SKILL.md](.agents/skills/quality-assurance/SKILL.md)) 단 1개만 `view_file`로 취득하여 규칙을 각인합니다.
3. **증거 기반 종결**: 특히 `quality-assurance` 기동 시에는 모든 체크리스트를 정량적으로 통과하고 정적 검증(`verify_code.py`) 성공 Evidence 출력을 완료해야만 성공을 최종 선언할 수 있습니다.
