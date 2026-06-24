# agentmemory 환경 설정 및 포트 정책

본 문서는 agentmemory의 환경 설정, 환경 변수, 포트 정책 및 기능 플래그(Feature Flags) 수칙을 기술합니다.

agentmemory는 시스템 환경 변수 및 `~/.agentmemory/.env` 파일(한 라인에 하나씩 `KEY=value` 형식으로 작성하며, `export` 접두사는 사용하지 않음)로부터 설정을 읽어옵니다. 설정을 수정한 후에는 서버를 재시작해야 적용됩니다.

## 빠른 시작

`~/.agentmemory/.env` 파일에서 더 풍부한 메모리 기능을 활성화하고 API 키를 설정하는 예시입니다:

```env
ANTHROPIC_API_KEY=sk-ant-...
AGENTMEMORY_AUTO_COMPRESS=true
AGENTMEMORY_INJECT_CONTEXT=true
```

## 기억해두어야 할 기본값

- 기본적으로 API 키는 필수가 아닙니다. API 키가 없으면 agentmemory는 로컬 임베딩과 BM25 기반의 zero-LLM 환경으로 실행됩니다.
- 토큰이 소비되는 기능들은 의도적으로 기본 설정에서 **비활성화(OFF)** 상태로 제공됩니다: `AGENTMEMORY_AUTO_COMPRESS`(LLM 요약 기능) 및 `AGENTMEMORY_INJECT_CONTEXT`(컨텍스트 자동 주입) 기능은 도구 사용 빈도에 비례하여 토큰 요금이 발생하기 때문입니다.
- 도구 표시 여부: `AGENTMEMORY_TOOLS=all`(기본값) 또는 최소화된 세트를 위한 `core` 설정을 사용할 수 있습니다.
- 인증: `AGENTMEMORY_SECRET`을 설정하여 REST API 호출 시 `Authorization: Bearer` 인증을 강제하도록 설정할 수 있습니다.

## 포트 정책

REST API의 기본 포트는 `3111`입니다. 스트림은 N+1(`3112`), 뷰어는 N+2(`3113`), 엔진은 N+46023(`49134`) 포트를 점유합니다. `--port <N>` 또는 `--instance <N>` 옵션을 전달하여 포트 블록 전체의 기본 위치를 조정할 수 있습니다.

## 관련 문서

- 보안 및 토큰 처리: agentmemory-rest-api
- 포트 4개 점유 및 아키텍처 배경: agentmemory-architecture

## 참고 자료

감지 및 연동 가능한 전체 환경 변수 목록은 `src/` 스캔 결과를 토대로 자동 생성된 REFERENCE.md를 확인하십시오.
