---
id: rule.metadata
title: "[Rule] 옵시디언 메타데이터 표준"
type: rule
status: active
summary: 옵시디언(Obsidian) 연동 및 에이전트 지식 관리를 위한 YAML 메타데이터(Frontmatter) 표준 규격
parent: rule.index
updated: 2026-06-29
---

# L2-metadata-standard (YAML Frontmatter 규격)

## Overview
* **왜 존재하는가 (Why)**: 옵시디언의 Dataview 플러그인, Graph View 필터링, 그리고 에이전트의 조건부 동적 파일 로딩(Lazy Loading)을 가능하게 하기 위해, 모든 지식 및 규칙 파일의 속성을 정형화합니다.
* **언제 사용하는가 (When)**: `.agents` 폴더 내에 새로운 규칙, 위키, 원시(Raw) 로그를 생성하거나 편집할 때 반드시 본 규정에 따라 문서 상단에 메타데이터를 삽입해야 합니다.

## Connections
* **상위 개념**: [rules-index.md](rules-index.md)
* **연관 자산**: 
  - [Knowledge Curation.md](../docs/philosophy/Knowledge Curation.md)
  - [Dashboard.md](../Dashboard.md)

---

## 1. 전역 메타데이터 표준 (Global Standards)

모든 Markdown 문서(규칙, 위키, 로그 등) 생성 시 파일 최상단에 다음과 같은 형식의 YAML Frontmatter 블록을 **반드시** 작성해야 합니다.

### 기본 템플릿 (Template)
```yaml
---
id: "파일고유식별자" # 예: rule.metadata, wiki.architecture, raw.bug.123
title: "[Rule] 옵시디언 메타데이터 표준"
type: ""          # rule, wiki, raw, index, principle 중 택 1
status: ""        # active, unresolved, resolved, synthesized, deprecated 중 택 1
category: ""      # (선택) raw 데이터의 경우: bug, chat, decision, idea 등
agent: ""         # (선택) 작성 에이전트명 (예: research-agent)
tags:             # (선택) 옵시디언 태그 목록
  - "agent/log"
  - "arch/updated"
updated: 2026-06-29
---
```

## 2. 속성(Property) 제약 수칙

1. **`type` (필수)**: 문서의 성격을 나타내며, `rule`, `wiki`, `raw`, `index`, `principle`, `reference`, `skill`, `agent` 외의 임의 값 사용을 금지합니다.
2. **`status` (필수)**: 문서의 현재 생애주기 상태를 나타냅니다.
   * `active`: 현재 유효하고 적용 중인 규칙 및 위키.
   * `unresolved`: 아직 해결되지 않은 에러나 논의 (`raw` 전용).
   * `resolved`: 단발적으로 해결된 에러 (`raw` 전용).
   * `synthesized`: `wiki`로 지식 융합이 완료되어 더 이상 대시보드에 표출될 필요가 없는 과거 기억 (`raw` 전용).
   * `deprecated`: 더 이상 사용되지 않는 과거 규칙이나 위키.
3. **`tags` 체계 (Taxonomy)**: 옵시디언 내 탐색 편의성을 위해 해시태그(`#`) 기호를 생략하고 배열 형태로 작성합니다.
   * ⚠️ **인간의 검토가 필요한 경우**: 의사결정이나 확인이 필요한 파일에는 반드시 `- "requires/human-review"` 태그를 부착하여 대시보드 알림을 활성화합니다.

## 3. 에이전트 행위 강제 (Agent Actions)

* **Raw 파일 생성 시 (Memory)**: 에러 해결 과정이나 아이디어 논의를 `.agents/raw/` 하위 폴더에 저장할 때, 반드시 `type: raw` 및 현재 상황에 맞는 `status`로 문서를 생성합니다.
* **Knowledge Synthesis 시 (Understanding)**: `raw` 파일들을 귀납적으로 분석하여 `wiki`를 갱신하고 나면, 융합의 재료가 된 대상 `raw` 파일들을 열어 `status: synthesized`로 변경해야 합니다. 이를 통해 옵시디언 대시보드의 '위키화 대기 큐'에서 해당 항목을 지워야 합니다.
