---
name: "knowledge-lint-curator"
description: "마크다운 메타데이터(Frontmatter) 준수 정적 검증 및 소스코드 변경에 따른 지식 동기화(Wiki & Index 갱신) 결핍을 실시간 차단하는 에이전트 자동화 수칙 스킬입니다."
id: skill.knowledge_lint_curator
title: "[Skill] Knowledge Lint Curator"
type: skill
status: active
parent: skill.index
related:
  - "[[skills/index.md]]"
  - "[[rules/L2-metadata-standard.md]]"
  - "[[principles/Knowledge Curation.md]]"
updated: 2026-06-29
---
# Skill. Knowledge Lint Curator (지식 린트 및 실시간 동기화 가이드)

## Overview / Connections
* **Parent (상위 개념)**: [[skills/index.md]]
* **연관 자산**:
  - [[rules/L2-metadata-standard.md]]
  - [[principles/Knowledge Curation.md]]

본 스킬은 에이전트가 개발 및 리팩토링 작업을 종료하기 직전, 생산된 지식과 마크다운 문서의 품질 표준을 기계적으로 철저하게 검증하고 교정하기 위한 자율 오퍼레이션 자동화 스킬입니다.

---

## 1. 실행 및 기동 타이밍 (Trigger Timing)

본 스킬은 다음 단계에 진입했을 때 **무조건 자동으로 작동**해야 합니다.
- 개발 단계 완료 후, `finishing-a-development-branch` 스킬이 작동하기 직전
- 커밋(`git commit`) 또는 병합(Merge)을 시도하려 하는 수명 주기 직전
- 사용자가 "작업을 종료해줘", "완료해줘", "검증해줘" 등의 요소를 전달하였을 때

---

## 2. 에이전트 자율 행동 수칙 (Agent Standard Operations)

에이전트는 마무리 작업에 진입한 순간, 아래 프로토콜을 순서대로 명확하게 작동시킵니다.

### 단계 1. 검증 스크립트 가동
- 에이전트는 즉시 워크스페이스 내에 내장된 마크다운 린트 도구를 실행해야 합니다.
  - **실행 명령어**: `python3 .agents/skills/knowledge-lint-curator/scripts/lint_markdown.py`

### 단계 2. 자동 보정(Auto-Fix) 피드백 수렴
- 스크립트 실행 후, 일부 마크다운 문서의 메타데이터(id, title, type, status, updated) 누락으로 인한 자동 보정이 일어났다면, 변경 내용을 반영하여 Git Staged 상태를 업데이트합니다.

### 단계 3. 지식 동기화 결핍 경고 (KNOWLEDGE_OUT_OF_SYNC) 대응
- 만약 검증 스크립트가 종료코드 `2`를 반환하고, 화면에 `KNOWLEDGE_OUT_OF_SYNC` 경고 메시지를 출력했다면, **에이전트는 즉시 작업을 종료하는 행동을 멈추고 자율적으로 세션을 지속**해야 합니다.
- **조치 행동**:
  1. 이번 세션에서 수정한 파이썬 로직, 비즈니스 핵심 지식, 환경 세팅 등을 바탕으로 연관된 `.agents/wiki/` 내의 문서를 보강하거나 신설합니다.
  2. 필요 시, `.agents/indexes/` 하위의 인덱스 파일에 개념을 수록합니다.
  3. 지식 자산 수정 및 갱신을 마친 후, 단계 1의 실행 명령어를 다시 가동하여 결과가 최종적으로 `0` (정상 통과)이 되는 것을 완료하고 나서 종료 단계로 이행하십시오.

---

## 3. 핵심 가드레일 (Strict Constraints)

- **경로 무오성**: 린트 스크립트 및 에이전트 주석 작성 시 절대 리눅스 절대 경로(`file:///home/jumasi/...`)를 사용해 링크를 걸지 않으며, 반드시 평문 상대 경로만을 사용해 상호 참조합니다.
- **이모지 전면 금지**: 터미널 출력 로그, 텍스트, 코드 주석 등 어떠한 곳에서도 유니코드 이모지(아이콘)를 절대 노출하지 않습니다.
