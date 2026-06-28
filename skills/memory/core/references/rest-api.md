---
id: skill.memory.core.rest_api
type: reference
status: active

summary: >
  Rest Api 참조 및 가이드 명세서.

parent: "[[skills/memory/core/SKILL.md]]"

updated: 2026-06-28
---

# agentmemory HTTP REST API 사양

* **Parent (상위 스킬)**: [[skills/memory/core/SKILL.md]]

---


본 문서는 agentmemory의 주 프로토콜이자 핵심 서페이스인 HTTP REST API 스펙과 연동 수칙을 기술합니다.

REST API는 agentmemory의 가장 원천적이고 대표적인 인터페이스입니다. MCP는 이 REST API 위에 올라가는 브릿지 계층에 불과합니다. 모든 메모리 연산은 `http://localhost:3111/agentmemory/*` 주소 하위의 HTTP 엔드포인트를 통해 제공됩니다.

## 빠른 시작

```bash
# 활성화 여부 확인 (Liveness Check)
curl -fsS http://localhost:3111/agentmemory/livez

# 기억 저장 (Save)
curl -X POST http://localhost:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{"content":"JWT 리프레시 토큰 로테이션 방식을 채택함","concepts":["jwt-refresh-rotation"]}'

# 검색 (Recall)
curl -X POST http://localhost:3111/agentmemory/smart-search \
  -H "Content-Type: application/json" \
  -d '{"query":"인증 토큰 전략","limit":5}'
```

## 인증 및 보안 (Auth)

기본적으로 로컬호스트(`localhost`) 상의 통신은 열려 있어 별도의 인증이 필요하지 않습니다. 다만, `AGENTMEMORY_SECRET` 환경 변수가 설정된 상태라면 모든 요청 헤더에 `Authorization: Bearer $AGENTMEMORY_SECRET` 인증 토큰을 포함해야만 정상 처리됩니다. 자세한 내용은 agentmemory-config 가이드를 참고하십시오.

## API 프로토콜 규칙 및 규격 (Conventions)

- 데이터 저장은 `201`, 읽기는 `200`, 유효성 검사 에러는 `400` HTTP 상태 코드를 반환합니다.
- API 핸들러는 사전에 지정된 필드만 허용(Whitelist)하고 알 수 없는 임의의 필드는 필터링하여 버리므로, 요청 바디에 정의되지 않은 여분의 키 값을 포함시켜 전송해도 무방하지만 무시됩니다.
- 포트는 `--port` 또는 `--instance` 명령 옵션을 통해 임의 변경할 수 있으며, 스트림, 뷰어, iii 엔진 포트 또한 이 기본 포트를 앵커로 삼아 자동으로 슬라이딩 정렬됩니다.

## 관련 문서

- 동일 규격의 MCP 도구 바인딩 명세: agentmemory-mcp-tools
- 포트 블록 시프트 및 보안 비밀 키 설정: agentmemory-config

## 참고 자료

전체 API 엔드포인트 명세 및 허용 HTTP 메서드 목록은 `src/triggers/api.ts`로부터 추출된 [[skills/memory/core/references/rest-api-reference.md]]에서 확인하실 수 있습니다.
