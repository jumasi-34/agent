# 에이전트 스킬 디렉토리 통합 가이드 (skills/README.md)

본 문서는 현재 워크스페이스의 `.agents/skills/` 및 `.gemini/skills/` 폴더 하위에 탑재 및 활성화되어 있는 **모든 에이전트 스킬(Specialized Skills)들의 상세 정의와 이력, 그리고 오픈소스/에코시스템 원천 출처(Source)**를 통합 기술한 최상위 색인서입니다.

에이전트는 당면한 태스크의 성격(품질 검사, 계획 수립, 자율 디버깅 등)에 맞추어 아래에 정의된 최적의 스킬을 활성화하여 기동하십시오.

---

## 1. 프로젝트 고유 로컬 스킬 (Workspace-specific Local Keep Skills)

본 프로젝트의 WSL 환경, SQLite 데이터베이스 정합성, Streamlit 비주얼 UI 가이드라인 등 고유한 설계 배경 및 인프라 한계를 방어하고 고사양 컴포넌트 일원화를 달성하기 위해 로컬 영역에서 독립적으로 형상 관리되는 핵심 독자 자산입니다.

| 스킬 식별자 | 위치 (상대 경로) | 상태 | 설명 (한글 기술 표준 준수) |
| :--- | :--- | :--- | :--- |
| **`developing-with-streamlit`** | [development/streamlit/SKILL.md](development/streamlit/SKILL.md) | **Active** | Streamlit 대시보드 화면 설계, 위젯 테밍, 세션 스테이트 최적화, 그리고 **Plotly 프리엄 컴포넌트 격리화 설계 패턴** 및 컬러/폰트 의미론적 토큰(Semantic Tokens) 바인딩을 강제 준증하는 고사양 UI 개발 스킬입니다. |
| **`quality-assurance`** | [quality-assurance/SKILL.md](quality-assurance/SKILL.md) | **Active** | 코드 배포 전 소스 가드레일 스캔, SQL 정적 분석, 메타데이터 동기화, 자율 정적 컴파일 및 Mock 단위 테스트 등 **5대 품질 관문(Quality Gate)**을 순차 통과시키는 품질 검역 게이트 스킬입니다. |
| **`guardrail`** | [quality/guardrail/SKILL.md](quality/guardrail/SKILL.md) | **Active** | 에이전트가 코드를 커밋/배포하기 전, 이모지 유무 체크, 커밋 메시지 규격 검정, SQLite 골든 스키마 유효성을 사전 심증하는 **정적 가드레일** 도구입니다. |
| **`sql_analyzer`** | [quality/sql/SKILL.md](quality/sql/SKILL.md) | **Active** | SQL 쿼리 파일 내에 프론트엔드용 한글 AS 별칭이 잘못 하드코딩되었거나 SQL 작성 5대 불변 규칙을 위배했는지 탐지하는 **쿼리 정적 분석기**입니다. |
| **`korean_metadata`** | [quality/korean-metadata/SKILL.md](quality/korean-metadata/SKILL.md) | **Active** | 원천 데이터베이스 영문 물리 컬럼명에 매핑되는 화면용 한글 표기명, 소수점 포맷팅, 툴팁 디테일 등의 정적 메타데이터를 자동 갱신하고 연동해 주는 **한글화 메타 도구**입니다. |
| **`agent_hooks`** | [agent_hooks/SKILL.md](agent_hooks/SKILL.md) | **Active** | WSL 가상 환경과의 역동기화 장애를 미연에 방지하고, 에이전트 자율 세션 로그를 실시간 분석해 SQLite 잠금 오류 등을 복구하며, 종료 전 완벽한 컨텍스트 인계(Handoff)를 실행하는 **라이프사이클 훅**입니다. |
| **`knowledge-capture`** | [knowledge-capture/SKILL.md](knowledge-capture/SKILL.md) | **Active** | 카파시 코딩 가이드라인 준수 여부 진단, 마크다운 문서 및 상대 경로 링크 린팅, 세션 완료 시 중요 지식 수확(Capture) 및 위키 인덱스 최적화를 아우르는 **지식 자산 케어 시스템**입니다. |
| **`agentmemory`** | [memory/core/SKILL.md](memory/core/SKILL.md) | **Active** | 에이전트의 단기/장기 지식 조각들을 데이터 저장 서버에 보관(Remember), 회상(Recall), 소거(Forget)하는 라이프사이클과 메모리 데몬 배선 규격을 규정한 **컨텍스트 메모리 스킬**입니다. |

---

## 2. 외부 도입 에코시스템 스킬 (Ecosystem Installed Skills)

오픈 에이전트 스킬 생태계(`skills.sh`) 또는 검증된 원천 저장소로부터 획득하여 프로젝트에 결합한 범용 고성능 스킬들입니다.

### 📌 에이전트 스킬 발견 (find-skills)
* **스킬 ID**: `find-skills`
* **설치 위치**: [find-skills/SKILL.md](find-skills/SKILL.md)
* **원천 출처**: Built-in CLI Skills Ecosystem (오픈 에이전트 생태계 기본 내장)
* **설명**: 에이전트가 특정 분야의 전문 도구나 다른 작업 양식이 필요할 때 `skills.sh` 및 오픈 에이전트 커뮤니티의 검증된 스킬 패키지를 탐색, 발견, 추천 및 자동 배포해 주는 스킬 패키지 매니저 검색 브릿지입니다.

---

### 🎨 지식 그래프 코드베이스 맵퍼 (graphify)
* **스킬 ID**: `graphify`
* **설치 위치**: `.gemini/skills/graphify/SKILL.md`
* **원천 출처**: [https://github.com/Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (GitHub Official)
* **설치 방식**: `graphify install --project --platform gemini`를 통한 프로젝트 로컬 구성 및 Hook 자동 바인딩
* **설명**: 전체 소스 코드(tree-sitter AST 구문 분석), 데이터베이스 골든 스키마, 인프라 사양 및 마크다운 문서(LLM 기반)를 분석하여 **Traversable Knowledge Graph(탐색 가능한 지식 그래프)**를 빌드합니다. 코드베이스 관련 질문에 대해 `graphify query`를 가동하여 최단 구조와 신뢰할 수 있는 개념 경로를 찾아내며, 코드 변경 시 `graphify update`를 연동하는 혁신적 스킬입니다.

---

### 💇 간결한 Python 코드 엔지니어링 (ponytail)
* **스킬 ID**: `ponytail`
* **설치 위치**: `.agents/skills/ponytail/SKILL.md` (및 부속 폴더 6종)
* **원천 출처**: [https://github.com/DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (GitHub Official)
* **설치 방식**: `npx skills add DietrichGebert/ponytail -y`에 의한 비대화형 로컬 연동 동기화
* **설명**: 파이썬 프로그래밍 작성 및 리팩토링 시, 불필요한 추상화나 순환 복잡도를 극한으로 낮추고 **"단순함(Minimal Complexity)"**을 추구하여 유지보수하기 쉬운 프로덕션을 지향하게 보좌하는 최상위 엔지니어링 스킬셋입니다.

이 패키지는 본래 목적인 코드 구현과 더불어, 기술 부채 추정 및 코드 감사를 위한 **6대 전문 서브 스킬**을 격리 제공합니다:
* **`ponytail`**: 파이썬 최소 복잡성 사상에 기반한 단순 설계 및 모범적 구현 전개
* **`ponytail-audit`**: 대상 파이썬 모듈의 순환 복잡도(Cognitive Complexity) 및 아키텍처 정밀 진단 감사
* **`ponytail-debt`**: 지저분하게 threaded된 상태, 하드코딩된 결함 및 숨겨진 기술 부채(Technical Debt) 색출
* **`ponytail-gain`**: 복잡성을 제거하고 단순한 composition/delegation 구조로 리팩토링했을 때 확보하는 정량 이득 분석
* **`ponytail-help`**: 파이썬 클린 코드 실천과 관련된 빠른 질의응답 및 설계 레퍼런스 가이드 기동
* **`ponytail-review`**: 신규 병합될 구현 코드를 정밀 분석하여 리팩토링 우려 요소를 선제 리뷰 및 수정안 피드백

---

### 🎨 비주얼 UI 디자인 파트너 (taste-skill)
* **스킬 ID**: `taste` / `taste-skill`
* **설치 위치**: `.agents/skills/...` (및 부속 폴더 13종)
* **원천 출처**: [https://github.com/Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (GitHub Official)
* **설치 방식**: `npx skills add Leonxlnx/taste-skill -y`에 의한 비대화형 로컬 연동 동기화
* **설명**: Streamlit 및 웹 인터페이스 설계 시 색상 팔레트, 타이포그래피, 마진(여백) 조율, 고사양 비주얼 디자인 방향성을 결정하는 전문 디자인 스킬셋입니다.

이 패키지는 본래 목적인 비주얼 제안과 더불어, 디자인 구현과 리팩토링을 위한 **13대 전문 서브 스킬**을 격리 제공합니다:
* **`brandkit`**: 브랜드 아이덴티티 및 일관된 시각 가이드 기반 팔레트 제안
* **`industrial-brutalist-ui`**: 볼드한 타이포그래피와 산업용 네오 브루탈리즘 스타일 설계
* **`gpt-taste`**: AI 생성 기반의 세련되고 조화로운 트렌드 테마 제안
* **`image-to-code`**: 디자인 시안이나 레이아웃 캡처 스크린샷 이미지를 정밀 코드로 변환
* **`imagegen-frontend-mobile`**: 모바일 인터페이스 디자인을 위한 반응형 목업 및 프리젠테이션 생성
* **`imagegen-frontend-web`**: 데스크톱 웹 환경을 위한 일관된 와이어프레임 및 실사 수준 시각물 배치
* **`minimalist-ui`**: 여백을 극대화하고 노이즈를 걷어낸 초간결 미니멀리즘 비주얼 테마 수립
* **`full-output-enforcement`**: 코드 작성 시 CSS 및 마크업 생략(Omission)을 막고 완전히 렌더링되게 보장
* **`redesign-existing-projects`**: 노후화되고 투박한 기존의 화면 레이아웃과 CSS를 고풍스럽게 재설계
* **`high-end-visual-design`**: 고사양 예술 지침에 기반한 고급 마이크로 인터랙션 및 프레젠테이션 설계
* **`stitch-design-taste`**: 여러 컴포넌트 간의 레이아웃 간격과 패딩을 조화롭게 바느질(Stitch)하듯 조율
* **`design-taste-frontend`**: 디자이너 수준의 감각적인 프론트엔드 비주얼 레이어 자율 전개
* **`design-taste-frontend-v1`**: 레거시 화면 레이어 감사를 위한 프론트엔드 테이스터 1버전 가이드

---

### 💎 결함 제로의 UI 품질 보증 (impeccable)
* **스킬 ID**: `impeccable`
* **설치 위치**: `.agents/skills/impeccable/SKILL.md`
* **원천 출처**: [https://github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable) (GitHub Official)
* **설치 방식**: `npx skills add pbakaus/impeccable -y`에 의한 비대화형 로컬 연동 동기화
* **설명**: 웹사이트, 대시보드 및 애플리케이션 화면 구현이 끝난 뒤 디자인 시안과의 정보 아키텍처적 일치성, 인지적 부하(Cognitive Load) 최소화, 웹 접근성 표준, 반응형 레이아웃 및 엣지 케이스 에러 렌더링에 이르는 UX의 세부 마이크로 디테일을 집요하게 **감사(Audit) 및 다듬어내는 품질 최적화 스킬**입니다.

---

### 📊 아키텍처 다이어그램 도식화 (mermaid-skill)
* **스킬 ID**: `mermaid` / `mermaid-skill`
* **설치 위치**: `.agents/skills/mermaid-skill/SKILL.md`
* **원천 출처**: [https://github.com/Agents365-ai/mermaid-skill](https://github.com/Agents365-ai/mermaid-skill) (GitHub Official)
* **설치 방식**: `npx skills add Agents365-ai/mermaid-skill -y`에 의한 비대화형 로컬 연동 동기화
* **설명**: 기술 문서 및 가이드 작성 시 복잡한 모듈 관계, API 트랜잭션 수순, 클래스 상속 및 상태 제어를 **Mermaid 다이어그램(.mmd) 및 미려한 비주얼 이미지(PNG, SVG)로 자동 빌드 및 렌더링**해 주는 설계 도구화 스킬입니다. 12가지 이상의 풍부한 차트 유형(Flowchart, Sequence, ERD, GitGraph 등)을 자동 레이아웃 정밀 지원합니다.

---

### 💎 극상의 UI/UX 제품 엔지니어링 (ui-ux-pro-max)
* **스킬 ID**: `ui-ux-pro-max` / `ui-ux-pro-max-skill`
* **설치 위치**: `.agents/skills/...` (및 부속 폴더 7종)
* **원천 출처**: [https://github.com/nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (GitHub Official)
* **설치 방식**: `npx skills add nextlevelbuilder/ui-ux-pro-max-skill -y`에 의한 비대화형 로컬 연동 동기화
* **설명**: 고도의 비주얼 자산 가이드라인, 그리드 레이아웃 구축, 정교한 타이포그래피 미학 및 제품 디자인 전반의 고품격 가이드라인을 결정하고 빌드해 주는 프론트엔드 최정상 UI/UX 스킬셋입니다.

이 패키지는 본래 목적인 UI/UX 설계와 더불어, 명세화 및 자산 제작을 위한 **7대 전문 서브 스킬**을 격리 제공합니다:
* **`banner-design`**: 대시보드 메인 배너 및 상단 히어로 영역 전용 고품격 기하학 CSS 배너 설계
* **`brand`**: 제품의 도메인 특화 색채론 및 심리적 감각에 부합하는 일관된 로고/브랜드 가이드 정립
* **`design`**: 와이어프레임 구조의 뼈대를 촘촘히 조율하며, 인터랙션 복잡도를 제어하는 사용자 관찰 설계
* **`design-system`**: 타이포그래피, 마진, 아이콘 셋, 그리고 공용 테마 토큰을 한데 수렴한 통합 디자인 시스템 아키텍처
* **`slides`**: 결과물 데모나 아키텍처 피칭용 고사양 슬라이드 프리젠테이션 레이아웃 디자인
* **`ui-styling`**: Streamlit 내부 인젝션 마크업 스타일링 및 순수 CSS/HTML 튜닝
* **`ui-ux-pro-max`**: 최고 수준의 미학적 룩앤필과 접근성 편의를 동시에 달성하는 최정상 디자인 게이트 지침

---

### ⚡ Superpowers 스킬 패키지 (14대 자율 개발 세부 스킬군)
* **패키지 ID**: `obra/superpowers`
* **원천 출처**: [https://github.com/obra/superpowers](https://github.com/obra/superpowers) (GitHub Official)
* **설치 방식**: `npx skills add obra/superpowers -y`에 의한 비대화형 로컬 동기화

이 패키지는 에이전트가 작업 요구 사항 분석부터 계획 수립, 격리된 개발 구현, 단위 검증 및 최종 브랜치 딜리버리까지 전체 소프트웨어 수명 주기를 완전 자율로 지휘할 수 있게 보좌하는 핵심 서브 가이드 세트입니다.

| 서브 스킬 식별자 | 로컬 설치 디렉토리 경로 | 상태 | 서브 스킬 역할 요약 (한글 기술) |
| :--- | :--- | :--- | :--- |
| **`brainstorming`** | [.agents/skills/brainstorming](brainstorming/SKILL.md) | **Active** | 요구 사항 구현 이전에 사용자 기획 의도를 정밀 수렴하고, 다각도 아키텍처 적합성 및 타당성을 사전 정렬하는 브레인스토밍 스킬 |
| **`writing-plans`** | [.agents/skills/writing-plans](writing-plans/SKILL.md) | **Active** | 탐색 단계를 거쳐 구체적으로 무엇을 어떻게 수정할 것인지 마일스톤과 테스트 검증 경로를 수립하는 계획 설계 스킬 |
| **`executing-plans`** | [.agents/skills/executing-plans](executing-plans/SKILL.md) | **Active** | 설계된 마일스톤에 따라 체크리스트 단위 작업을 엄격하게 하나씩 실천하고 추적해 나가는 실행 전용 가이드 스킬 |
| **`subagent-driven-development`** | [.agents/skills/subagent-driven-development](subagent-driven-development/SKILL.md) | **Active** | 복잡도가 높은 태스크에 직면했을 때, 독자적인 전문 분야를 가진 서브 에이전트를 적재적소에 파견하고 모니터링하여 전체 효율을 극대화하는 SDD 워크플로 관리 스킬 |
| **`test-driven-development`** | [.agents/skills/test-driven-development](test-driven-development/SKILL.md) | **Active** | 코드 수정과 동시에 반드시 단위/회귀 테스트 케이스를 우선 설계하여, 프로덕션의 결함률을 영률에 수렴하게 관리하는 TDD 구현 기법 스킬 |
| **`systematic-debugging`** | [.agents/skills/systematic-debugging](systematic-debugging/SKILL.md) | **Active** | 예상치 못한 오류에 부딪렸을 때 비이성적 패치를 지양하고, 가설을 세운 뒤 가설마다 격리된 로깅과 테스트 증거로 버그 요인을 단계적 색출하는 디버깅 스킬 |
| **`verification-before-completion`** | [.agents/skills/verification-before-completion](verification-before-completion/SKILL.md) | **Active** | 개발 결과물을 최종 선언하거나 PR로 엮기 전, 통합 빌드/타입체킹/린팅/자가 테스트 등 일체의 프로덕션 게이트를 자율 완수하여 결함 제로를 증명하는 스킬 |
| **`requesting-code-review`** | [.agents/skills/requesting-code-review](requesting-code-review/SKILL.md) | **Active** | 변경 파일들의 아키텍처적 인과성, 임팩트 존, 테스트 커버리지를 투명하게 설명하는 고품질 코드 리뷰 패키지 및 메시지 요청 템플릿 생성 스킬 |
| **`receiving-code-review`** | [.agents/skills/receiving-code-review](receiving-code-review/SKILL.md) | **Active** | 코드 리뷰어 혹은 사용자 검수 과정에서 주입된 수정 피드백을 수신하여 결함이나 우려 사항을 올바르게 디코딩하고 리팩토링하는 상호 작용 스킬 |
| **`using-git-worktrees`** | [.agents/skills/using-git-worktrees](using-git-worktrees/SKILL.md) | **Active** | 동시다발적인 피처 개발이나 긴급 핫픽스 발생 시 현재 소스를 어지럽히지 않고 Git Worktree를 생성하여 안전하게 컨텍스트를 평행 격리하는 스킬 |
| **`finishing-a-development-branch`** | [.agents/skills/finishing-a-development-branch](finishing-a-development-branch/SKILL.md) | **Active** | 개발 브랜치를 온전히 마무리하고 정합성 린팅을 적용하며, 충돌(Conflict) 유무를 미리 점검하고 딜리버리를 준비하는 브랜치 정리 스킬 |
| **`using-superpowers`** | [.agents/skills/using-superpowers](using-superpowers/SKILL.md) | **Active** | 슈퍼파워 프레임워크 대화형 세션 기동 시, 사용자의 배경 및 제약조건을 사전에 학습하고 알맞은 도구를 조준 탑재하는 세션 초기화 스킬 |
| **`dispatching-parallel-agents`** | [.agents/skills/dispatching-parallel-agents](dispatching-parallel-agents/SKILL.md) | **Active** | 독립적으로 분할 처리 가능한 대규모 연산을 여러 서브 에이전트에게 동시 파견하여 수렴 결과를 고속 조립하는 병렬 분산 관리 스킬 |
| **`writing-skills`** | [.agents/skills/writing-skills](writing-skills/SKILL.md) | **Active** | 개발 과정에서 유용하게 반복되는 일련 of 전문가 패턴을 하나의 신규 스킬 사양(`SKILL.md`)으로 패키징하고 배포하여 에이전트 생태계 자산을 증대시키는 스킬 |

---

## 3. 에이전트 지연 스킬 로딩 지침

1. **인덱스 우선 탐색**: 에이전트는 본격적인 작업을 수행하기 전 반드시 `skills/index.md` 및 본 문서를 참고하여 현재 시나리오에 필요한 단 1개의 최상위 통합 스킬을 매핑하여 가동해야 합니다.
2. **설명문 표준**: 스킬과 관련된 부가 규칙, 운영 가이드라인 등은 일체의 다국어 혼선을 방지하고 명확한 상호 운영성을 사수하기 위해 **오직 한국어(Korean) 표준**에 맞춰 유지보수해야 합니다.
3. **증거 기반의 확인**: 모든 외부 에코시스템 패키지는 `npx skills check`를 통해 가끔씩 무결성과 버전 상태를 조율하는 것을 권장합니다.
