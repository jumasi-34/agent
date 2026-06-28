---
id: skill.agentmemory.agents
type: reference
status: active

summary: >
  Agents 참조 및 가이드 명세서.

parent: "[[skills/agentmemory/SKILL]]"

updated: 2026-06-28---
# agentmemory 에이전트 연동 가이드

* **Parent (상위 스킬)**: [SKILL.md](../SKILL.md)

---


본 문서는 agentmemory가 `connect` 명령어를 통해 호스트 코딩 에이전트에 연동되는 방식과 수칙을 기술합니다.

`agentmemory connect <agent>` 명령어는 메모리 서버를 호스트 에이전트의 구성에 병합하며, 기존 서버들을 보존합니다. REST가 기본 프로토콜로 사용되며, MCP 전용 호스트의 경우 어댑터가 stdio MCP 브릿지를 연결합니다.

## 빠른 시작

```bash
agentmemory connect claude-code   # 또는 cursor, codex, gemini-cli, ...
```

연결을 마친 후, 호스트를 재시작하거나 MCP 재로딩(예: Claude Code의 경우 `/mcp`)을 실행하여 서버를 인식시키십시오. 그 후 에이전트가 agentmemory의 도구 목록을 올바르게 출력하는지 확인합니다.

## 워크플로우

1. 호출한 에이전트를 감지합니다. 알 수 없는 경우 기본값은 `claude-code`입니다.
2. REFERENCE.md 테이블에 나열된 이름을 참조하여 `agentmemory connect <name>`을 실행합니다.
3. 검증: 서버가 작동 중이고 호스트가 전체 도구 세트를 표시해야 합니다. 도구가 7개만 표시된다면 MCP 심(shim)이 서버에 연결하지 못한 것입니다 (../_shared/TROUBLESHOOTING.md 참조).

## 주의 사항

- 액션 스킬(remember, recall 등)은 `npx skills add rohitg00/agentmemory` 명령어를 통해 별도로 설치됩니다. `connect` 명령은 도구를 사용할 수 있게 만들고, 스킬은 에이전트에게 도구를 사용하는 시점을 교육합니다.
- Windows 환경: WSL2를 사용하십시오. 네이티브 Windows는 서버 실행은 가능하나 `connect`는 지원되지 않습니다.

## 관련 문서

- agentmemory-mcp-tools, agentmemory-rest-api, agentmemory-hooks.

## 참고 자료

`src/cli/connect/`에서 생성된, 디스플레이 이름과 프로토콜 노트가 포함된 전체 어댑터 목록은 REFERENCE.md를 확인하십시오.
