---
name: "agentmemory"
description: "Manage agentmemory server, configurations, automatic lifecycle hooks, REST/MCP APIs, and client wiring adapters for coding agents. Use this skill when asked to explain how memory functions, configure memory environments, look up API/tool specs, inspect hooks, or run connection commands."
id: skill.agentmemory
type: skill
status: active

parent: "[[skills/index]]"

related:
  - "[[skills/index]]"

consumers:
  - agent.all

updated: 2026-06-28
---

# agentmemory 통합 가이드라인 (agentmemory)

## Overview / Connections
* **Parent (상위 개념)**: [[skills/index]]


본 스킬은 에이전트 메모리 시스템(agentmemory)의 구성, 환경설정, 수동/자동 수집 라이프사이클 및 REST/MCP API 명세를 통합 관리합니다.

에이전트는 구체적인 실행 목적에 맞춰 아래의 세부 가이드라인 상대 경로를 확인하고, `view_file` 도구를 활용하여 실시간으로 습득하십시오.

## 세부 영역별 인덱싱 및 라우팅 가이드

*   **호스트 에이전트 연결 지침 (connect)**: [[skills/agentmemory/references/agents]]
    - 에이전트 환경별 메모리 서버 연동 및 MCP 브릿지 마운트 수칙
*   **저장소 및 백엔드 아키텍처 (architecture)**: [[skills/agentmemory/references/architecture]]
    - DB 아키텍처, iii 엔진 원천 레이어 및 데이터 영속화 규격
*   **환경 설정 및 포트 정책 (config)**: [[skills/agentmemory/references/config]]
    - 서버 포트, 토스트 수집 설정, 인증 토큰 및 기능 플래그 수칙
*   **세션 주기 관측 훅 표준 (hooks)**: [[skills/agentmemory/references/hooks]]
    - 세션 전/후반 관측 수집 훅, 디버깅 지침 및 에러 추적
*   **MCP 도구 세트 및 파라미터 (mcp-tools)**: [[skills/agentmemory/references/mcp-tools]]
    - mcp-tools 파라미터 세부 기술 표준 및 [[skills/agentmemory/references/mcp-tools-reference]] 카탈로그 링크
*   **HTTP REST API 사양 (rest-api)**: [[skills/agentmemory/references/rest-api]]
    - HTTP 엔드포인트 명세 및 [[skills/agentmemory/references/rest-api-reference]] 계약서 연동 지침
*   **메모리 스킬 신규 작성 표준 (write-skill)**: [[skills/agentmemory/references/write-skill]]
    - ChromaDB 기반 장기 기억에 인덱싱할 신규 스킬의 구조적 명세 표준


## Sub-Assets (하위 참조 자산)
* [[skills/agentmemory/references/agents]] — Agents 참조 및 가이드 명세서.
* [[skills/agentmemory/references/architecture]] — Architecture 참조 및 가이드 명세서.
* [[skills/agentmemory/references/config]] — Config 참조 및 가이드 명세서.
* [[skills/agentmemory/references/hooks]] — Hooks 참조 및 가이드 명세서.
* [[skills/agentmemory/references/mcp-tools-reference]] — Mcp Tools Reference 참조 및 가이드 명세서.
* [[skills/agentmemory/references/mcp-tools]] — Mcp Tools 참조 및 가이드 명세서.
* [[skills/agentmemory/references/rest-api-reference]] — Rest Api Reference 참조 및 가이드 명세서.
* [[skills/agentmemory/references/rest-api]] — Rest Api 참조 및 가이드 명세서.
* [[skills/agentmemory/references/write-skill]] — Write Skill 참조 및 가이드 명세서.
