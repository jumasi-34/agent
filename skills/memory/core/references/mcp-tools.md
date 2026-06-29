---
id: skill.memory.core.mcp_tools
title: "[Skill] Mcp Tools"
type: reference
status: active

summary: >
  Mcp Tools 참조 및 가이드 명세서.

parent: "[skills/memory/core/SKILL.md](../SKILL.md)"

updated: 2026-06-28
---

# agentmemory MCP 도구 세트 및 파라미터

* **Parent (상위 스킬)**: [skills/memory/core/SKILL.md](../SKILL.md)

---


본 문서는 agentmemory가 MCP(Model Context Protocol) 도구로 제공하는 전체 기능 매핑, 역할 및 파라미터 규격을 기술합니다.

agentmemory는 전체 기능 세트를 MCP 도구 형태로 노출합니다. 본 스킬은 인덱스 역할을 수행하며, 특정 목적을 위해 어떤 도구를 호출해야 하고 각 도구의 상세 파라미터가 무엇인지 상세히 파악할 수 있도록 안내합니다.

## 빠른 시작 (도구 사용법 예시)

데이터 저장 및 검색 흐름:

1. `memory_save`를 호출할 때 `content`(인사이트 내용), `concepts`(쉼표로 구분된 키워드), `files`(쉼표로 구분된 파일 경로)를 매개변수로 전달하여 정보를 저장합니다.
2. 이후 필요할 때 `query`와 `limit`를 인자로 `memory_smart_search`를 호출하여 정보를 검색합니다. 이 도구는 BM25, 벡터 유사도 및 연결된 개념 간의 그래프 확장 검색 방식을 하이브리드로 결합하여 수행합니다.

## 도구 패밀리 분류 (Tool Families)

- **수집 및 기록 (Capture)**: `memory_save`, `memory_observe` 흐름, `memory_compress_file`.
- **조회 및 검색 (Retrieve)**: `memory_smart_search`, `memory_recall`, `memory_file_history`, `memory_timeline`, `memory_vision_search`.
- **세션 및 커밋 (Sessions & Commits)**: `memory_sessions`, `memory_commits`, `memory_commit_lookup`.
- **지식 및 그래프 (Knowledge & Graph)**: `memory_lesson_save`, `memory_lesson_recall`, `memory_graph_query`, `memory_relations`, `memory_patterns`, `memory_crystallize`.
- **구조화 슬롯 (Structured Slots)**: `memory_slot_create`, `memory_slot_append`, `memory_slot_get`, `memory_slot_list`, `memory_slot_replace`, `memory_slot_delete`.
- **거버넌스 및 자가 치유 (Governance & Health)**: `memory_governance_delete`, `memory_audit`, `memory_verify`, `memory_heal`, `memory_diagnose`.

## 에이전트 실행 워크플로우

1. 수행할 태스크에 가장 적절하고 좁은 범위의 도구를 선택하십시오. 예를 들어, 일반적인 메모리 검색에는 `memory_smart_search`를 사용하고, 구체적인 쿼리가 정해져 있을 때는 `memory_recall`을 사용하며, 단순 세션 목록이 필요할 때는 `memory_sessions`를 선택하는 것이 바람직합니다.
2. 도구를 호출하기 전에 파라미터 이름 및 필수 여부를 `mcp-tools-reference.md` 문서에서 확인하십시오.
3. 문서화된 정확한 필드만 전달하십시오. REST 핸들러는 허용 목록(Whitelist)에 포함된 필드만 처리하며, 정의되지 않은 미확인 필드는 무시합니다.

## 관련 문서

- HTTP 통신 기반의 동일 엔드포인트 정보: agentmemory-rest-api
- 도구 가시성 제어 및 기능 플래그: agentmemory-config
- 공통 도구들을 감싸서 제공되는 고수준 액션 스킬: remember, recall, recap, handoff, forget

## 참고 자료

각 도구의 파라미터 사양과 코어 도구 식별 정보가 포함된 전체 도구 명세 테이블은 소스 코드를 통해 자동 갱신되는 [skills/memory/core/references/mcp-tools-reference.md](mcp-tools-reference.md)에서 확인하실 수 있습니다.
