---
id: skill.memory.core.architecture
title: "Ref: CORE > REFERENCES > ARCHITECTURE"
type: reference
status: active

summary: >
  Architecture 참조 및 가이드 명세서.

parent: "[[skills/memory/core/SKILL.md]]"

updated: 2026-06-28
---

# agentmemory 저장소 및 백엔드 아키텍처

* **Parent (상위 스킬)**: [[skills/memory/core/SKILL.md]]

---


본 문서는 agentmemory가 어떻게 빌드되는지, 기반이 되는 iii 엔진 프리미티브, 저장소 모델, 포트 정책 및 뷰어에 대한 아키텍처 지침을 기술합니다.

agentmemory는 코딩 에이전트를 위한 메모리 서버입니다. 로컬에서 실행되며, 관측 데이터를 수집하고 하이브리드 검색을 위해 인덱싱한 뒤, REST 및 MCP 프로토콜을 통해 다시 제공합니다. iii 엔진 위에 구축되었습니다.

## iii 프리미티브 (iii Primitives)

모든 구성 요소는 iii 엔진 위의 함수, 트리거 또는 워커 상태로 동작합니다. 별도의 플러그인 시스템은 존재하지 않으며, 워커가 함수(`mem::*`) 및 HTTP 트리거(`api::*`)를 등록하면 iii 엔진이 호출을 라우팅합니다. agentmemory는 iii 엔진을 우회하지 않으며, 신규 기능은 항상 신규 함수 및 트리거의 조합으로 개발됩니다.

## 검색 모델 (Retrieval Model)

검색(Recall)은 하이브리드 방식을 사용합니다: BM25 키워드 검색, 벡터 유사도 검색, 그리고 연결된 개념 간의 그래프 확장 기법을 결합합니다. 기본 설치 시 임베딩이 온디바이스(로컬)로 실행되고 BM25도 별도 키가 필요 없기 때문에, API 키 없이 작동이 가능합니다. LLM 프로바이더 연동은 더욱 풍부한 요약 및 자동 주입 기능(모두 선택 사항)을 위해 제공됩니다.

## 저장소 및 라이프사이클 (Storage & Lifecycle)

메모리는 내용, 개념, 파일 경로, 중요도, 타임스탬프 등의 데이터를 포함하며, 세션 단위로 그룹화되고 옵션에 따라 커밋 정보와 연결될 수 있습니다. 단순 누적으로 저장소가 무한히 확장되는 것을 방지하기 위해 '수집(Capture) -> 압축(Compress) -> 통합(Consolidate) -> 망각(Forget)'으로 이어지는 라이프사이클을 통해 지속적으로 유용한 정보만을 유지 관리합니다.

## 포트 정책 (Ports)

REST API는 기본적으로 `3111` 포트를 앵커로 사용합니다. 스트림은 N+1(`3112`), 뷰어는 N+2(`3113`), 엔진은 N+46023(`49134`) 포트를 점유합니다. `--instance N` 인자를 주면 전체 포트 블록이 N*100 만큼 시프트됩니다.

## 뷰어 (Viewer)

`http://localhost:3113`에서 제공되는 실시간 웹 뷰어를 통해 세션이 진행됨에 따라 메모리가 구축되는 과정을 시각적으로 모니터링할 수 있습니다. 데모 및 수집 정상 동작 여부 확인에 매우 유용합니다.

## 관련 문서

- 인터페이스 스펙: agentmemory-mcp-tools, agentmemory-rest-api
- 자동 수집 작동 방식: agentmemory-hooks
- 포트 및 기능 플래그 설정: agentmemory-config
