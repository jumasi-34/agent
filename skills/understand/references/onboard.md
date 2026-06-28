---
id: skill.understand.onboard
type: reference
status: active

summary: >
  Onboard 참조 및 가이드 명세서.

parent: skill.understand

updated: 2026-06-28
---
# 신규 팀 멤버 온보딩 가이드 제작 가이드라인 (understand-onboard)

* **Parent (상위 스킬)**: [SKILL.md](../SKILL.md)

---


본 지침은 분석된 프로젝트의 지식 그래프(`.understand-anything/knowledge-graph.json`)를 가공 및 요약하여, 신규 합류한 팀 멤버가 복잡한 아키텍처와 로직 위계를 막힘없이 이해할 수 있도록 구조화된 온보딩 가이드라인 문서를 자율 생산하는 제어 가이드라인입니다.

## 지식 그래프 구조 참조 (Graph Structure Reference)

지식 그래프 JSON 파일은 다음과 같은 정적 구조를 가지고 있습니다.
*   `project`: 프로젝트 정보 (`{name, description, languages, frameworks, analyzedAt, gitCommitHash}`)
*   `nodes[]`: 개별 노드 정보 (`{id, type, name, filePath?, summary, tags[], complexity, languageNotes?}`)
    - 코드 노드 유형: `file`, `function`, `class`, `module`, `concept`
    - 비코드 노드 유형: `config`, `document`, `service`, `table`, `endpoint`, `pipeline`, `schema`, `resource`
    - 도메인/지식 노드 유형: `domain`, `flow`, `step`, `article`, `entity`, `topic`, `claim`, `source`
    - 노드 ID 양식: `file:path`, `function:path:name`, `config:path`, `article:path` (노드 타입을 접두사로 사용)
*   `edges[]`: 관계 정보 (`{source, target, type, direction, weight}`)
    - 핵심 관계 유형: `imports`, `contains`, `calls`, `depends_on`, `configures`, `documents`, `deploys`, `triggers`, `contains_flow`, `flow_step`, `related`, `cites`
*   `layers[]`: 아키텍처 계층 구조 (`{id, name, description, nodeIds[]}`)
*   `tour[]`: 안내용 워크스루 단계 (`{order, title, description, nodeIds[]}`)

## 효율적 분석 기법 (How to Read Efficiently)

1.  **전체 로드 방지**: 파일 전체를 한 번에 다 읽어 컨텍스트를 과도하게 차지하지 마십시오. 필요한 노드 정보만 부분적으로 탐색하는 것이 효율적입니다.
2.  **Grep 사전 탐색**: 전체 파일을 열기 전에 `grep_search` 도구를 활용하여 필요한 키워드 및 매칭 부분을 먼저 검색하십시오.
3.  **명칭 및 요약 집중**: 노드의 `name`과 `summary` 필드는 코드베이스의 정수를 나타내는 가장 유용한 정보입니다.
4.  **연결 정보 추적**: `edges` 정보를 따라가며 모듈 간의 물리적/논리적 의존성 및 호출 흐름(Dependency chain)을 확인하십시오.

## 세부 온보딩 가이드 생산 지침 (Instructions)

1.  **지식 그래프 존재 여부 확인**: 현재 워크스페이스 내에 `.understand-anything/knowledge-graph.json`이 존재하는지 검증하십시오. 파일이 없다면 사용자에게 `understand` 스킬을 먼저 기동하여 지식 그래프를 생성하도록 안내하십시오.
2.  **프로젝트 기초 정보 추출**: `grep_search`를 기동하여 지식 그래프 상단에 기록된 `"project"` 정보(명칭, 주 개발 언어, 프레임워크 스펙 및 프로젝트 요약)를 확보하십시오.
3.  **아키텍처 레이어 추출**: `"layers"` 정보 전체를 `grep_search` 등으로 로드하십시오. 레이어 정의는 아키텍처의 거시적 정체성을 드러내며, 완성될 온보딩 문서의 핵심 뼈대를 형성합니다.
4.  **프로젝트 가이드 투어 로드**: `"tour"` 속성 전체를 `grep_search` 등으로 로드하십시오. 가이드 투어 단계들은 신규 개발자가 어떤 흐름으로 시스템을 학습해 나가야 하는지 추천 로드맵을 제공합니다.
5.  **파일 수준의 구조 노드 탐색**: 지식 그래프 파일 내에서 함수나 클래스 같은 세밀한 미시 레벨은 배제하고, 거시적인 파일 수준 정보(`file`, `config`, `document`, `service`, `pipeline`, `table`, `schema`, `resource`, `endpoint` 타입 노드 등)만 `grep_search`로 필터링하여 각 노드의 `name`, `filePath`, `summary`, `complexity` 속성을 수집하십시오.
6.  **코드 복잡도 위험 지대(Hotspots) 식별**: 수집된 파일 수준 노드 중 `complexity` 지표가 가장 극단적으로 높거나 연관 관계가 과도하게 얽힌 컴포넌트들을 발굴하십시오. 이 구역들은 신규 입사자가 코드를 수정할 때 각별히 주의해야 하는 아키텍처적 위험 지대(Hotspots)로 분류됩니다.
7.  **온보딩 가이드 문서 생성**: 수집된 고밀도 지식들을 유기적으로 엮어, 다음 핵심 단락을 빠짐없이 갖춘 가독성 높은 온보딩 가이드라인 문서를 정교한 한글 마크다운 포맷으로 작성하십시오.
    - **프로젝트 개요 (Project Overview)**: 프로젝트 명칭, 주요 언어 및 프레임워크 기술 스택, 전체 비즈니스 정체성
    - **아키텍처 계층 구조 (Architecture Layers)**: 개별 레이어의 설계 의도 및 역할, 레이어별 핵심 진입 파일 목록
    - **핵심 설계 결정 및 철학 (Key Concepts)**: 시스템 전반에 적용된 핵심 디자인 패턴 및 주요 설계 규칙 (노드 요약 및 태그 참조)
    - **순차 학습 가이드 투어 (Guided Tour)**: 1단계부터 차례대로 따라가며 아키텍처를 학습할 수 있는 추천 로드맵
    - **물리적 아키텍처 맵 (File Map)**: 레이어별로 질서 있게 구조화된 파일 일람 및 개별 요약 설명
    - **코드 복잡도 위험 지대 (Complexity Hotspots)**: 작업 시 부작용 우려가 커 각별한 주의가 요구되는 복잡도 위험 파일 및 주의 가이드
8.  **출력 및 저장 유도**: 완성된 마크다운 결과물을 터미널에 긴 텍스트로 단순 출력하지 말고, 사용자에게 프로젝트 루트 하위의 `docs/ONBOARDING.md` 파일로 즉시 파일 쓰기를 하도록 안내하고 유도하십시오.
9.  **형상 관리 등록 추천**: 신규 파일 `docs/ONBOARDING.md` 생성이 완수되면, 팀 동료들과의 공유를 위해 해당 자산을 Git 커밋 및 원격 저장소에 푸시하도록 권장하고 보고를 마무리하십시오.
