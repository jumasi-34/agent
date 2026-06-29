---
title: "[Dashboard]"
id: wiki.dashboard
type: wiki
status: active
updated: 2026-06-29
---
# 🤖 Agent Knowledge Dashboard

이 대시보드는 에이전트의 활동 내역(Raw)과 프로젝트 지식(Wiki)의 진화 상태를 실시간으로 모니터링하는 **중앙 관제탑**입니다. 에이전트의 사고 흐름과 지식 융합의 병목 지점을 파악하십시오.

---

## 🚨 1. 해결 중인 오류 및 디버깅 로그 (Active Bugs)
에이전트가 현재 직면하여 해결 중이거나 미해결 상태인 오류 기록입니다.

```dataview
TABLE status AS "상태", agent AS "담당 에이전트", file.mtime AS "업데이트 시간"
FROM "raw/bug"
WHERE status != "synthesized" AND status != "resolved"
SORT file.mtime DESC
LIMIT 10
```

---

## 🧠 2. 위키화 대기 중인 기억 (Needs Synthesis)
기록된 지 오래되었으나, 아직 위키(`wiki/`) 문서로 귀납적 병합(Synthesis)이 이루어지지 않은 원시 데이터(`raw/`)들입니다. Knowledge Capture 스킬의 발동이 필요합니다.

```dataview
TABLE category AS "유형", file.ctime AS "발생일", agent AS "작성자"
FROM "raw"
WHERE type = "raw" AND status != "synthesized"
SORT file.ctime ASC
LIMIT 10
```

---

## 📚 3. 최근 업데이트된 아키텍처 및 위키 (Recent Wiki)
최근에 에이전트나 사용자에 의해 융합되어 갱신된 공식 문서 및 규칙들입니다.

```dataview
TABLE type AS "분류", file.mtime AS "갱신 시간"
FROM "wiki" OR "rules" OR "principles"
SORT file.mtime DESC
LIMIT 5
```

---

## 💬 4. 인간의 검토 대기 항목 (Needs Human Review)
에이전트가 단독으로 결정하지 못하고 인간 사용자의 피드백, 전략적 의사결정, 또는 승인을 대기 중인 항목입니다. 확인 후 태그를 제거하십시오.

```dataview
TABLE type AS "분류", status AS "상태"
FROM ""
WHERE contains(tags, "requires/human-review")
SORT file.mtime DESC
```
