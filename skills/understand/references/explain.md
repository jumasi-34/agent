# 소스코드 및 모듈 상세 딥다이브 가이드라인 (understand-explain)

본 지침은 기존 지식 그래프(`.understand-anything/knowledge-graph.json`)와 연동하여, 코드베이스 내의 특정 소스파일, 함수 또는 클래스 모듈을 입체적으로 추적하고 그 내부 아키텍처 및 상세 로직을 정밀 설명하기 위한 가이드라인입니다.

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
2.  **분석 대상 노드 탐색**: 지식 그래프 파일 내에서 분석 대상으로 지목된 인자(`$ARGUMENTS`)에 해당하는 컴포넌트를 `grep_search` 등으로 신속히 찾아내십시오.
    - 파일 경로 분석 (예: `src/auth/login.ts`): `"filePath"` 필드에서 경로가 일치하는 노드를 검색합니다.
    - 함수/클래스 표기 분석 (예: `src/auth/login.ts:verifyToken`): 지정된 파일 경로를 필터로 걸고 `"name"` 필드에서 해당 식별자를 탐색합니다.
    - 타겟 노드의 고유 `id`, `type`, 요약(`summary`), 태그(`tags`) 및 복잡도(`complexity`) 속성을 메모해 둡니다.
3.  **연관 엣지 추적 (1-Hop)**: 지식 그래프 내 `edges` 영역에서 타겟 노드 ID와 연결된 모든 관계 정보를 `grep_search` 등으로 획득하십시오.
    - `"source"` 필드 매칭: 해당 컴포넌트가 내부에서 사용, 호출 또는 수입하는 하위 노드 정보 (Outgoing edges)
    - `"target"` 필드 매칭: 해당 컴포넌트를 호출하거나 수입하여 사용하는 상류 노드 정보 (Incoming edges)
    - 연결된 노드들의 ID와 관계 타입을 정리해 둡니다.
4.  **주변 이웃 노드 정보 수집**: 3단계에서 정리된 연결 노드 ID들에 대해 지식 그래프에서 해당 노드 정의를 검색하여 각각의 `name`, `summary`, `type` 정보를 확보하십시오. 이를 통해 타겟 컴포넌트 주변의 이웃 관계도(Neighborhood context)가 정교하게 완성됩니다.
5.  **아키텍처 레이어 매핑**: `"layers"` 영역에서 타겟 노드 ID를 검색하여, 이 모듈이 아키텍처 상의 어느 계층에 박혀 있는지 확인하고 해당 계층의 설계 철학을 이해하십시오.
6.  **실물 소스코드 정독**: 타겟 노드의 `filePath` 경로에 있는 실제 디렉토리 또는 소스파일을 열어 세부 구현부와 주석을 꼼꼼히 탐독하십시오.
7.  **입체적 딥다이브 설명서 작성 및 보고**: 모은 지식과 실제 소스코드 분석을 종합하여, 독자가 해당 언어를 상세히 모른다 하더라도 완벽히 아키텍처적 의도를 이해할 수 있도록 한국어로 다음과 같이 보고서를 작성하십시오.
    - **아키텍처적 위상 및 역할**: 어떤 계층(Layer)에 배치되어 있으며 이 프로젝트 내에서 왜 존재하는지 물리적 정수 설명
    - **내부 컴포넌트 구성**: 해당 모듈이 내포하고 있는 구체적 함수 및 클래스 간의 내부 연결망 설명 (`contains` 엣지 기준)
    - **외부 의존 관계**: 무엇을 수입해다 쓰며, 어디에서 이 모듈을 핵심적으로 호출하는지 수렴/발산 의존도 설명 (`calls`, `imports` 엣지 기준)
    - **데이터 및 비즈니스 플로우**: 입력 파라미터가 어떻게 주입되어 중간 처리 과정을 거쳐 어떤 형태로 반환되는지 구체적인 변형 생명 주기 추적
    - **코드 특이점 및 복잡도**: 설계 패턴, 특이 스타일, 그리고 복잡도(`complexity`) 지표에 따른 코드 개선 여지나 잠재 리스크 영역 강조
