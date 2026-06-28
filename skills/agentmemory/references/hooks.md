---
id: skill.agentmemory.hooks
type: reference
status: active

summary: >
  Hooks 참조 및 가이드 명세서.

parent: "[[skills/agentmemory/SKILL]]"

updated: 2026-06-28---
# agentmemory 세션 주기 관측 훅 표준

본 문서는 에이전트 세션의 라이프사이클 전체에 걸쳐 자동으로 관측 데이터를 수집하는 agentmemory 플러그인 훅(Hooks)에 대한 지침을 기술합니다.

Claude Code 플러그인은 라이프사이클 훅을 등록하여 관측 데이터를 자동으로 수집합니다. 일상적인 작업 시 수동으로 `memory_save`를 호출할 필요가 없습니다. 훅이 도구 사용, 사용자 프롬프트, 세션 경계 등을 능동적으로 감시하고 자동으로 관측 정보를 기록합니다.

## 빠른 시작

플러그인을 설치하면 라이프사이클 훅이 자동으로 등록됩니다:

```bash
/plugin marketplace add rohitg00/agentmemory
/plugin install agentmemory
```

등록 후 `http://localhost:3113`에서 실시간으로 수집되는 관측 데이터를 모니터링할 수 있습니다.

## 훅(Hooks)의 역할 및 동작 범위

- **세션 시작 및 종료 (Session Start & End)**: 각 작업 단위의 경계를 구분 지으며, `handoff` 스킬이 이전 작업을 다시 이어나갈 수 있도록 지원합니다.
- **도구 사용 감시 (Tool-Use Hooks)**: 어떤 부분이 왜 변경되었는지 분석하고 기록하며, 이 데이터는 `recall` 및 `recap` 스킬의 핵심 원천 자료가 됩니다.
- **프롬프트 전송 감시 (Prompt-Submit)**: 사용자의 원천 의도를 캡처합니다. 에이전트가 컨텍스트를 다듬고 자르기 전에, 'Pre-compact' 단계에서 본래의 정교한 컨텍스트 정보를 사전 확보 및 보존합니다.
- **포스트 커밋 감시 (Post-Commit Hook)**: Git 커밋 정보를 현재 세션과 연동시켜 `commit-context` 및 `commit-history` 스킬의 강력한 추적 기능을 작동시킵니다.

## 중요 주의 사항

- 관측 데이터 수집(Capture)은 기본 활성화(ON) 상태로 실행되며, LLM을 사용하지 않는(zero-LLM) 로컬 방식으로 구동되므로 토큰 요금이 발생하지 않습니다.
- 다만, 획득한 관측 데이터를 LLM 요약본으로 변환하는 기능(`AGENTMEMORY_AUTO_COMPRESS`)과 컨텍스트에 메모리를 자동으로 재주입하는 기능(`AGENTMEMORY_INJECT_CONTEXT`)은 토큰 비용을 소모하므로 별도 선택(Opt-in)으로 제공됩니다.
- 만약 수집 기록이 누락되었다면 플러그인이 활성화되어 있는지, 그리고 agentmemory 서버가 정상 구동 중인지 점검하십시오. 세부적인 내용은 `../_shared/TROUBLESHOOTING.md`를 참고하십시오.

## 관련 문서

- 수집 및 주입 플래그 설정 가이드: agentmemory-config
- 수집된 세션 데이터를 최종 활용하는 상위 스킬: handoff, recap, session-history

## 참고 자료

실제 등록되는 상세한 훅 이벤트 목록은 `plugin/hooks/hooks.json` 분석을 기반으로 자동 작성된 REFERENCE.md를 확인하십시오.
