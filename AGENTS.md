# agents.md (Antigravity 프로젝트 제약 및 행동 규칙 헌법)

이 문서는 본 워크스페이스 내에서 AI 에이전트(Antigravity 등)가 자율 개발, 하네스 엔지니어링 및 리팩토링 작업을 수행할 때 반드시 준수해야 하는 **초핵심 제약 사항 및 설계 헌법(SSOT)**입니다.

---

## 1. 초핵심 제약 6대 헌법 (Absolute Guardrails)

### ① Safety Lock (기존 소스 코드 변경 금지)
- 사용자의 명시적인 직접 승인 및 요청이 있기 전까지 기존 프로덕션 소스 코드(`app/` 하위 전수 및 루트의 `app.py`)를 수정, 생성, 가공할 수 없습니다.
- 소스 코드 변경 시에는 반드시 **[분석 및 제안] -> [사용자 동의 획득] -> [수정 수행]** 프로세스를 엄격히 따릅니다.

### ② WSL Markdown Link Constraint (WSL 환경 상대 경로 의무화)
- VS Code 터미널, 채팅창, 마크다운 자산 내에서 절대 리눅스 경로(`file:///home/jumasi/...`)나 `file:///` 프로토콜을 사용하면 윈도우 호스트 연동 에러가 발생합니다.
- 모든 파일 하이퍼링크는 **반드시 프로토콜을 제외하고** 워크스페이스 루트 기준의 평문 상대 경로(예: `[.agents/rules/L2-architecture.md](.agents/rules/L2-architecture.md)`)만을 사용하여 클릭 시 정상적으로 열리도록 작성해야 합니다.

### ③ UI 규칙 및 이모지 사용 전면 금지
- Streamlit UI 페이지, 탭 라벨, 마크다운 텍스트, 버튼, 토스트, 소스 코드 주석 등 어떠한 곳에서도 일반 유니코드 이모지(예: 👤, ⚠️, ❌, 🤖, 📄)를 사용할 수 없습니다.
- 아이콘이 필요한 경우 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용합니다.

### ④ Streamlit 위젯 세션 상태 제약
- `key`가 할당되어 렌더링된 Streamlit 위젯은 런타임 중에 프로그램 상에서 `st.session_state[key] = value` 형태로 값을 직접 할당하여 수정할 수 없습니다. (`StreamlitAPIException` 유발)
- 위젯 값을 리셋할 때는 반드시 위젯이 인스턴스화되기 직전에 해당 세션 키를 클리어하는 **세션 가로채기(Session Interception)** 기법을 활용하십시오.

### ⑤ 하네스 엔지니어링 작업 범위 제한 (Sandbox for Harnessing)
- 하네스 엔지니어링 및 검증 코드 작성은 `tests/` 디렉터리 하위의 신규 독립 테스트 파일 생성만 허용합니다.
- 검증 및 목킹 시 실제 파일을 오염시키지 않는 **인메모리(In-Memory) 기법**만 사용해야 합니다.

### ⑥ 함수 생성, 독스트링 및 코드 구조 표준 (Function, Docstring & Code Structure Standards)
- 신규 모듈, 클래스, 함수를 작성하거나 대규모 리팩토링할 경우, 반드시 식별용 헤더 주석(`# * [대분류 - 요약]`), 명확한 타입 힌팅, 그리고 Google/NumPy 스타일의 독스트링(Docstring) 구조를 엄격히 준수하여 선언해야 합니다.
- **한국어 독스트링 원칙**: 소스 코드 내 모든 모듈, 클래스, 함수에 작성되는 독스트링(Docstring) 및 주석은 가독성과 협업 효율을 극대화하기 위해 **가능하면 한국어(Korean)로 작성**하는 것을 기본 원칙으로 삼습니다.
- **섹션 구분 타이틀 하이라이트 표준**: 페이지 모듈 및 서비스 소스 코드 내의 주요 기능적/물리적 레이아웃 구역을 정의할 때, 가독성을 비약적으로 높이기 위해 반드시 아래와 같은 통일된 주석 장식 블록 양식을 사용해야 합니다.
  ```python
  # =========================================================================
  # SECTION 1. Imports (라이브러리 및 모듈 임포트)
  # =========================================================================
  ```
- 세부적인 서식 규칙 및 예시는 [L2-naming-convention.md](rules/L2-naming-convention.md)를 참조하십시오.

---

## 2. 세부 표준 정책 및 행동 규정 링크 (Detailed Rules)

에이전트는 작업 성격에 맞춰 아래의 세부 표준 정책 문서를 스스로 로드하고 정합성을 검증해야 합니다.

| 영역 | 규정 파일 (상대 경로 링크) | 본질적 역할 및 핵심 제약 수칙 |
| :--- | :--- | :--- |
| **Git & 형상관리** | [L1-git.md](rules/L1-git.md) | 커밋 메시지 한국어 작성 및 태그 접두사 의무화, Dual Push(메인 & intelligence) 순차 동시 수행 수칙 |
| **시스템 아키텍처** | [L2-architecture.md](rules/L2-architecture.md) | 3-Layer(UI-Service-Query) 물리 격리 및 Pandas 체이닝 표준, UI 6대 정합성 수칙 준수 |
| **비즈니스 상수** | [L2-business-constants.md](rules/L2-business-constants.md) | 물리 공장 코드 정적 매핑 및 이중화 방지, 도메인 상수 일원화 관리 |
| **컬러 시스템** | [L2-color-system.md](rules/L2-color-system.md) | IBM Carbon 테마 기반의 대시보드 및 플롯 컬러 시스템 정적 일치화 |
| **코드 가독성** | [L2-context-readability.md](rules/L2-context-readability.md) | 중복 명 접두사(context-) 배제 및 AI 컨텍스트 가독성 극대화 표준 |
| **코드 명명 규칙** | [L2-naming-convention.md](rules/L2-naming-convention.md) | 물리/논리 계층 명명 규칙 표준화, DB-UI 컬럼 매핑 정합성, 함수 생성 및 독스트링 기술 표준 |
| **자산 동기화** | [L2-sync-policy.md](rules/L2-sync-policy.md) | 로컬과 원격 간의 Rsync 일방향 동기화 및 자산/데이터 Push/Pull 흐름 불변 수칙 |
| **쿼리 설계** | [L3-query.md](rules/L3-query.md) | SQL 내 디스플레이 한글 AS 하드코딩 전면 금지 및 영문 물리 컬럼명 보존 규칙 |
| **서비스 전처리** | [L3-service.md](rules/L3-service.md) | 데이터프레임 가공 전담 및 메서드 체이닝 표준 준수 |
| **UI 화면 구성** | [L3-dashboard.md](rules/L3-dashboard.md) | Streamlit 페이지 라우팅 제어 및 Google Material Symbols 화면 렌더링 표준 |
| **데이터 시각화** | [L3-plot.md](rules/L3-plot.md) | UI 레이어 1:1 매핑 Plotly 차트 격리 구현 규칙 |

---

## 3. 비즈니스 도메인 지식 베이스 및 개발 가이드 링크 (Reference Knowledge)

코딩 작업 진행 시 필요한 비즈니스 수식, API 계약, 에러 처리 등의 영속 지식은 다음 상대 경로 링크를 탐색하여 지식을 흡수하십시오.

- **품질 비즈니스 도메인 지식**: [domain-knowledge.md](context/domain/domain-knowledge.md) (6대 핵심 품질 도메인 지표 수식 및 데이터 집계 룰 SSOT)
- **공용 인프라 사양**: [infrastructure-summary.md](context/infra/infrastructure-summary.md) (API, 인사정보, DB 자원 관리 요약서)
- **릴리즈 훅 규격**: [hooks-specification.md](context/infra/hooks-specification.md) (3단계 로컬 품질 게이트 및 장애 대응 릴리즈 훅)
- **에러 격리 가이드**: [error-handling.md](context/guide/error-handling.md) (Streamlit Error Boundary 격리 렌더링 및 SQLite 로깅 가이드)
- **테스트 및 코드 정적 검증**: [testing-verification.md](context/guide/testing-verification.md) (인메모리 Mocking 기법 및 `verify_code.py` 정적 코드 컴파일 검증 기동 가이드)
- **에이전트 품질 평가 데이터 (Golden Tasks)**: [golden_tasks.yaml](context/evals/golden_tasks.yaml) (에이전트 성능 정량 평가 명세셋)
- **신규 페이지 개발 워크플로우**: [new_page_development_workflow.md](context/guide/new_page_development_workflow.md) (Streamlit 화면 개발 계층별 표준 워크플로우)
- **시각화 개발 워크플로우 및 템플릿**: [plotly-workflow-template.md](context/guide/plotly-workflow-template.md) (일관된 고품질 Plotly 생성을 위한 표준 워크플로우 및 코드 템플릿)

---

## 4. 자가 정제 루프 및 오작동 재발 방지 (Self-Refinement)

- 에이전트는 작업 중 에러나 규칙 미준수를 인지하는 즉시 원인을 정밀 분석하여 [reverse-sync-prevention.md](context/checklist/reverse-sync-prevention.md) 내의 히스토리 테이블에 양식에 맞춰 추가 기록해야 합니다.
- 동시에 로컬 및 글로벌 규칙을 갱신 및 보강하여 지속적으로 실시간 자가 정제를 완수합니다.
- **AI 읽기 금지 구역**: `intelligence/note/` 및 그 하위 경로는 어떠한 경우에도 조회, 검색, 참조해서는 안 됩니다.

---

## 5. UI 및 시각화 리팩토링 제약 6대 수칙 (UI & Visualization Refactoring Rules)

에이전트가 Streamlit UI 및 Plotly 시각화 리팩토링을 수행할 때 반드시 다음 6대 수칙을 철저히 준수해야 합니다.

1. **컬러는 무조건 토큰화**: 모든 하드코딩된 HEX 코드, 색상 문자열 및 빌트인 컬러스케일은 반드시 `app/core/constants/ui.py` 내의 디자인 시스템 토큰(Colors)으로 일원화하여 참조합니다.
2. **Plotly는 컴포넌트화**: 개별 플롯 파일(`*_plots.py`) 내에 차트 드로잉 코드가 직접 노출되지 않도록 `app/core/plot/components.py` 등에 컴포넌트 클래스(Factory 패턴 등)로 캡슐화하여 공통 관리합니다.
3. **필요한 컬러가 없을 경우 토큰화 후 사용**: 디자인 시스템 상에 구현되어 있지 않은 신규 컬러가 필요할 경우, 코드 내에 직접 상수를 정의하지 말고 `app/core/constants/ui.py`에 물리 및 시맨틱 토큰으로 등록 후 간접 참조하여 사용해야 합니다.
4. **재사용할 컴포넌트가 없을 경우 기존 컴포넌트 기능 확장**: 완전히 동일한 컴포넌트가 없더라도 기존에 개발된 컴포넌트의 파라미터나 분기 처리를 개선(기능 확장)하여 해결할 수 있는지 최우선적으로 검토합니다.
5. **기능 확장이 안될 경우 컴포넌트 추가**: 기존 컴포넌트의 단순 확장으로 수용하기 힘든 완전히 다른 데이터 유형이나 프레젠테이션 스펙인 경우에 한해, 신규 컴포넌트 클래스를 추가 작성합니다.
6. **Layout 공통 요소는 요소별 컴포넌트 생성**: 타이틀, 범례, 그리드선, 축 스타일 등 Plotly 레이아웃을 구성하는 중복 제어 속성들은 개별 레이아웃 헬퍼 혹은 요소별 공통 컴포넌트 메서드로 분리 정의하여 재사용합니다.

---

## 6. 에이전트 복수 스킬 간섭 방지 및 자율 정합성 운영 5대 수칙 (Anti-Conflict Rules)

에이전트는 최근 대량 배치된 47대 확장 스킬의 유기적 조율 및 오작동 방지를 위해 다음 5대 운영 수칙을 무조건적으로 이행해야 합니다.

1. **Git Worktree 동기화 통제**: `using-git-worktrees`로 가상 개발 영역을 생성해 작업 중인 경우, 해당 영역 내에서는 절대 `make push-assets` 또는 `make pull-data` 등의 rsync 동기화를 기동하지 않습니다. 모든 데이터 동기화는 메인 워크스페이스 원점(`/home/jumasi/workstation/`)에서 브랜치 조율 하에 단일하게 수행합니다.
2. **데이터 및 쿼리 3단계 정합성 준증**: 데이터 모델/쿼리 변경 시 반드시 `korean_metadata` 사전에 한글 디스플레이 컬럼 정보를 선등록한 뒤, `sql_analyzer` 수칙에 의거하여 SQL 쿼리 내 하드코딩 별칭(`AS "한글"`)을 배제하여 개발하고, 최종적으로 `guardrail` 정적 검증을 통과해야 배포할 수 있습니다.
3. **병렬 위임의 물리적 범위 완전 격리**: `dispatching-parallel-agents`를 구동할 때, 호출 대상 서브에이전트들이 동일한 물리적 소스 파일에 대해 동시 쓰기(Write) 작업을 수행하지 못하도록 작업 영역을 완벽히 분리하고, 순차 의존성이 있는 단계별 설계 위임 시에는 반드시 `subagent-driven-development` 단일 가이드 하에 진행합니다.
4. **장단기 기억 상호 Inter-locking**: 매 세션 마무리 단계(`finishing-a-development-branch` 작동 전)에서, `agent_hooks`에 기록된 로컬 SQLite 세션 장애 원인 및 완치 정보를 `remember` 스킬을 사용하여 ChromaDB 장기 기억(Vector)에 핵심 학습 코드로 반드시 연계 등록해야 합니다.
5. **분석 데이터 경로 은닉**: `understand-` 계열 분석 스킬 구동 시 생성되는 모든 그래프 원천 데이터 및 메타파일은 `.gitignore`에 확실히 격리 등록되어 있는지 검증하여 Reverse Sync Defender의 오작동 감지 로직을 방어해야 합니다.

