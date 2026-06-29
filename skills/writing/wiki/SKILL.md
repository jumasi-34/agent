---
name: "writing-wiki"
description: "Rule, Skill, Agent, Context, Raw를 분석하여 프로젝트를 이해하기 위한 정돈된 Wiki를 생성하거나 갱신하는 스킬입니다. 내용을 그대로 복제하지 않고 '설명하고 연결'하는 것을 핵심 원칙으로 삼습니다."
id: skill.writing_wiki
title: "[Skill] Wiki"
type: skill
status: active

parent: "[skills/index.md](../../index.md)"

related:
  - "[skills/index.md](../../index.md)"

consumers:
  - agent.all

updated: 2026-06-28
---

# Skill. Writing Wiki (프로젝트 이해를 위한 Wiki 작성 표준)

## Overview / Connections
* **Parent (상위 개념)**: [skills/index.md](../../index.md)


이 스킬은 프로젝트의 다양한 지식 구성 요소(Rule, Skill, Agent, Context, Raw)를 종합 분석하여, 인간과 AI 에이전트가 시스템을 완벽히 이해할 수 있도록 구조화된 **Wiki(Understanding)** 문서를 작성 및 갱신할 때 적용하는 가이드입니다.

Andrej Karpathy의 AI 지식 철학에 따라, Wiki는 개별 규정이나 절차의 복사본(Copy)이 아니라, 이들을 유기적으로 **설명하고 연결(Explain and Connect)**하는 뇌의 시냅스 역할을 수행합니다.

---

## 1. 사전 분석 단계 (Project Analysis Phase)

Wiki를 새로 생성하거나 갱신하기 전에, 에이전트는 프로젝트의 현재 상태를 정확하게 이해하기 위해 아래의 자산들을 반드시 선행 정독해야 합니다.

1. **Rule**: [.agents/AGENTS.md](../../../AGENTS.md) 및 `rules/` 내 행동 제약 조건
2. **Skill**: `skills/` 하위의 자율 개발 절차 명세서
3. **Agent**: `agents/` 또는 에이전트 페르소나 정의 문서
4. **Context**: `context/` 하위의 비즈니스 도메인 규칙 및 영속 지식
5. **Raw**: `.agents/raw/` 하위의 개별 세션 팩트 및 트러블슈팅 이력 (Memory)

---

## 2. Wiki 핵심 3대 불변 규칙 (Core Golden Rules)

* **복사본 제작 금지 (No Redundancy)**
  * Rule의 내용, Skill의 코드나 절차, Agent의 성격, Context의 수식을 Wiki 문서 내에 그대로 복사하여 재하드코딩(Copy & Paste)하지 않습니다.
  * 중복된 복사본은 정보의 파편화와 관리 부채를 유발합니다. Wiki는 원본 문서를 가리키며 맥락을 **"설명하고 연결"**하는 용도로만 사용되어야 합니다.
* **중복 생성 방지 (No Duplication)**
  * 새로운 개념의 Wiki를 생성하기 전에 반드시 기존 Wiki 파일들을 먼저 검색하여, 유사하거나 흡수할 수 있는 기존 문서가 있다면 신설 대신 기존 문서를 리팩토링합니다.
* **항상 최신화 (Keep Updated)**
  * 시스템 변경사항이 발생하면 Wiki 문서는 항상 단일 진실 공급원(SSOT)으로서 실시간 갱신되어야 합니다.

---

## 3. Wiki 필수 구성 서식 (Standard Wiki Template)

모든 Wiki 문서는 프로젝트 이해를 극대화하기 위해 다음의 격식과 섹션을 누락 없이 포함해야 합니다.

```markdown
# [Wiki 제목: 개념의 명확한 명칭]

## 1. 목적 (Why)
- 이 개념/모듈/비즈니스 흐름이 프로젝트에 왜 존재하는지, 해결하고자 하는 핵심 문제가 무엇인지 그 배경과 비전을 가독성 높게 설명합니다.

## 2. 핵심 개념 (Key Concepts)
- 이 지식을 관통하는 핵심 논리, 추상 아키텍처, 또는 설계 패러다임을 직관적으로 서술합니다.

## 3. 관련 Rule (Related Rules)
- 이 개념에 제약을 가하거나 반드시 준수해야 하는 행동 규칙과의 연결 링크를 명시합니다.
- 예: [L2-naming-convention.md](../../../rules/L2-naming-convention.md)

## 4. 관련 Skill (Related Skills)
- 이 개념을 수행하거나 지식을 캡처할 때 연동되는 자율 절차 가이드를 링크합니다.
- 예: [knowledge-capture](../../knowledge-capture/SKILL.md)

## 5. 관련 Agent (Related Agents)
- 이 지식의 수행 주체이거나 관련 책임이 있는 에이전트의 역할과 페르소나를 링크하고 명시합니다.

## 6. 관련 Context (Related Contexts)
- 이 지식과 결합되어 작동하는 정적 도메인 지식, 비즈니스 상수, 인프라 사양을 링크합니다.
- 예: [domain-knowledge.md](../../../context/domain/domain-knowledge.md)

## 7. 관련 코드 (Related Code)
- 이 개념이 물리적으로 구현된 실제 소스 코드 또는 템플릿의 상대 경로와 주요 라인을 링크합니다.
- 예: [app.py](app.py#L120-L150)

## 8. 관련 Wiki (Related Wikis)
- 이 문서와 상호작용하거나 함께 읽으면 시너지가 나는 다른 위키들의 관계망을 정의하고 링크합니다.
- 예: [다른 위키 문서 명칭](.agents/wiki/some-other-wiki.md)
```

---

## 4. 링크 및 스타일링 제약 사항 (Constraints)

* **이모지 전면 금지**: Wiki 본문, 타이틀, 목록 등 어느 곳에서도 유니코드 이모지(예: 👤, ⚠️, ❌)를 노출하지 않습니다.
* **평문 상대 경로 고수**: 모든 연결 링크는 WSL 호스트 연동을 위해 절대 프로토콜(`file:///`) 없이 워크스페이스 루트 기준의 평문 상대 경로(예: `[경로](.agents/wiki/file.md)`)만을 사용하여 정상 연결을 보장합니다.
