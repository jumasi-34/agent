# 코드베이스 기반 대화형 질의응답 가이드라인 (understand-chat)

본 지침은 지식 그래프(`.understand-anything/knowledge-graph.json`)를 활용하여 코드베이스의 아키텍처, 의존 관계, 특정 컴포넌트 정보에 대해 질문하고 정확히 이해하는 분석 가이드라인입니다.

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

## 세부 분석 수행 지침 (Instructions)

1.  **지식 그래프 존재 여부 확인**: 현재 워크스페이스 내에 `.understand-anything/knowledge-graph.json`이 존재하는지 검증하십시오. 파일이 없다면 사용자에게 `understand` 스킬을 먼저 기동하여 지식 그래프를 생성하도록 안내하십시오.
2.  **프로젝트 메타데이터 읽기**: `grep_search` 등을 통해 파일 상단부의 `"project"` 섹션만 제한적으로 로드하여 언어, 프레임워크, 대략적 개요 등의 기초 컨텍스트를 확보하십시오.
3.  **관련 노드 탐색**: 질의어 키워드를 기준으로 지식 그래프의 다음 필드를 탐색하십시오.
    - 노드 명칭 검색: `"name"` 필드 내의 문자열 일치 여부 확인
    - 요약 설명 검색: `"summary"` 필드의 시맨틱 매칭 여부 확인
    - 태그 탐색: `"tags"` 배열 내의 토픽 정보 탐색
    - 매칭되는 노드의 `id` 목록을 파악합니다.
4.  **연관 엣지 추적 (1-Hop)**: 매칭된 노드 ID에 대해 `edges` 섹션 내에서 해당 ID가 `source` 또는 `target`으로 작용하는 관계들을 검색합니다.
    - 해당 모듈이 가져오는 의존성(하류 의존성, downstream) 확인
    - 해당 모듈을 호출하는 주체(상류 호출자, upstream) 확인
5.  **아키텍처 계층 파악**: 매칭된 노드 ID가 `"layers"`의 어떤 물리적 계층에 속하는지 파악하고 해당 계층의 역할을 컨텍스트에 포함시키십시오.
6.  **질의응답 및 결과 요약**: 연관된 서브그래프(Subgraph)를 바탕으로 다음과 같은 형식으로 명확하게 답변을 구성하십시오.
    - 매칭된 핵심 파일, 함수 및 아키텍처 레이어를 직접 명시하며 설명
    - 모듈 간의 연결 구조를 바탕으로 데이터 및 호출 흐름 설명
    - 가독성이 높고 간결한 한국어로 설명하며, 필요시 소스 코드의 실제 라인을 지칭하십시오.
