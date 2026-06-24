# Git Diff 분석 및 점진 분석 가이드라인 (understand-diff)

본 지침은 기존 지식 그래프(`.understand-anything/knowledge-graph.json`)와 현재 Git 변경 사항(Diff)을 비교 대조하여, 변경된 컴포넌트의 파급 효과, 영향 범위 및 리스크를 계량하고 예측하는 분석 가이드라인입니다.

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
2.  **변경된 파일 목록(Diff) 확보**: 지식 그래프를 읽기 전에 Git 명령어를 활용하여 변경된 파일 목록만 빠르게 추출하십시오.
    - 커밋되지 않은 변경 사항이 있는 브랜치: `git diff --name-only`
    - 피처(Feature) 브랜치 개발 중: `git diff main...HEAD --name-only` (또는 기준 브랜치 대비 비교)
    - 사용자가 PR 번호를 직접 기재한 경우: 해당 PR 정보로부터 변경된 파일 목록(diff)을 가져옵니다.
3.  **프로젝트 메타데이터 읽기**: `grep_search` 등으로 지식 그래프 내 `"project"` 정보만 제한적으로 읽어 분석 기초 컨텍스트를 확보하십시오.
4.  **변경된 파일에 대응하는 노드 탐색**: 파악된 각 변경 파일 경로에 대해 `grep_search`를 기동하여 지식 그래프 내에서 다음을 탐색하십시오.
    - `"filePath"` 필드에 파일 경로를 포함하고 있는 노드들
    - 이를 통해 파일 수준 노드뿐만 아니라 해당 파일 내에 구현된 함수 및 클래스 노드까지 모두 식별합니다.
    - 매칭된 모든 노드의 `id` 목록을 기록합니다.
5.  **연관 엣지 추적 (1-Hop)**: 식별된 변경 대상 노드 ID들을 기준으로 `edges` 섹션 내에서 이 노드들과 직접 연결된 관계를 검색합니다.
    - 해당 모듈에 상류 의존성을 지니는 다른 모듈(수정 시 파급 영향을 받는 호출자, upstream callers) 식별
    - 해당 모듈이 하류에서 호출하고 있는 모듈(의존하는 모듈, downstream dependencies) 식별
    - 이들을 '영향을 받는 컴포넌트(Affected components)'로 명명합니다.
6.  **영향을 받는 아키텍처 계층 파악**: 식별된 노드 ID들을 지식 그래프의 `"layers"` 정보와 대조하여, 어떤 물리 계층들이 영향을 받거나 교차 연동 에러의 가능성이 있는지 파악합니다.
7.  **구조화된 분석 결과 작성 및 보고**: 수집된 하위 연관 지식을 종합하여 아래 템플릿에 맞추어 사용자에게 정밀 분석 보고서를 한국어로 작성하십시오.
    - **직접 변경된 컴포넌트 (Changed Components)**: 직접 수정된 모듈 목록 및 지식 그래프에 명시된 기능 요약 정보
    - **간접 영향을 받는 컴포넌트 (Affected Components)**: 1-Hop 엣지 추적을 통해 발견된, 잠재적 부작용이 우려되는 연관 모듈 목록
    - **영향을 받는 계층 (Affected Layers)**: 물리적 아키텍처 관점에서 침범 및 변경되는 레이어 정보 및 레이어 연동 이슈
    - **리스크 진단 (Risk Assessment)**: 변경된 노드의 복잡도(`complexity`) 지표, 연관 엣지의 총량, 영향력 범위(Blast radius) 등을 바탕으로 종합적인 코드 변경 리스크 평가 및 집중 검토 대상 권고
8.  **대시보드 시각화용 오버레이 파일 작성**: 정밀 분석 결과를 도출한 후, 대시보드에서 시각적으로 변화 추이를 렌더링할 수 있도록 `.understand-anything/diff-overlay.json` 경로에 오버레이 데이터를 기록하십시오. 파일 구조는 다음과 같습니다.
    ```json
    {
      "version": "1.0.0",
      "baseBranch": "<비교에 사용된 기준 브랜치명>",
      "generatedAt": "<ISO 타임스탬프>",
      "changedFiles": ["<변경된 파일 경로 목록>"],
      "changedNodeIds": ["<4단계에서 식별한 직접 변경 노드 ID 목록>"],
      "affectedNodeIds": ["<5단계에서 식별한 간접 영향 노드 ID 목록 (직접 변경 노드 ID 제외)>"]
    }
    ```
    오버레이 저장이 완료되면 사용자에게 `understand-dashboard`를 기동하여 대시보드 화면상에서 변경 지점을 시각적으로 확인하도록 제안하십시오.
