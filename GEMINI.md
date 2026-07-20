# Agent OS 에이전트 스킬 거버넌스 및 설계 지침 (.agents/GEMINI.md)

본 문서는 Agent OS 내 12대 전문 에이전트와 외부 도입 에코시스템 스킬 간의 **매핑 매트릭스** 및 **스킬 위계/트리거/워크플로우 가이드라인**을 기술한 핵심 지침서입니다.

---

## 1. 에코시스템 스킬 - 12대 에이전트 매핑 매트릭스

각 에이전트가 본연의 책무(Contract)를 완수하기 위해 기동해야 하는 에코시스템 스킬 및 `Superpowers` 서브 스킬 목록입니다.

> 💡 **범례**: `◎` (주요 주도 스킬), `○` (협업 지원 스킬)

| 에이전트 (Agent) | 매핑되는 주요 에코시스템 스킬 및 Superpowers 서브 스킬 | 관계 |
| :--- | :--- | :---: |
| **router-agent** | `find-skills`, `using-superpowers`, `subagent-driven-development` (SDD), `dispatching-parallel-agents` | **◎** |
| | `graphify` (아키텍처 정보 기반 라우팅 지원) | **○** |
| **product-agent** | `brainstorming` (기획 타당성 정렬), `ui-ux-pro-max-skill` (제품 방향성 수렴) | **◎** |
| | `graphify` (기존 제품 지식 쿼리) | **○** |
| **architecture-agent**| `writing-plans` (구현 로드맵 및 테스트 설계), `mermaid-skill` (아키텍처 다이어그램 도식화) | **◎** |
| | `graphify` (3-Layer 경계 검증 및 스키마 분석) | **◎** |
| **analysis-agent** | `ponytail-audit` / `ponytail-debt` / `ponytail-gain` (파이썬 복잡도 및 부채 진단) | **◎** |
| | `systematic-debugging` (장애 원인 추적 및 가설 검증) | **◎** |
| **design-agent** | `taste-skill` (색채, 여백, 브루탈리스트 UI 등 테마 설계), `ui-ux-pro-max` (디자인 시스템 설계) | **◎** |
| **engineering-agent**| `ponytail` (단순하고 유지보수하기 쉬운 Python 작성), `executing-plans` (순차 구현) | **◎** |
| | `test-driven-development` (TDD 구현), `receiving-code-review` (피드백 반영 리팩토링) | **◎** |
| **ui-agent** | `taste-skill` (디자인 요소 적용), `ui-styling` (Streamlit 마크업 및 CSS 튜닝) | **◎** |
| | `executing-plans` (UI 화면 조립) | **○** |
| **quality-agent** | `impeccable` (UI/UX 결함 및 웹 접근성 검증), `verification-before-completion` (종료 전 게이트 패스) | **◎** |
| | `requesting-code-review` (품질 검사 및 체크리스트), `ponytail-review` (품질 기준선 도달 심증) | **◎** |
| **release-agent** | `finishing-a-development-branch` (브랜치 마무리 및 린트), `using-git-worktrees` (작업 분리) | **◎** |
| | `mermaid-skill` (배포 변경점 도식화) | **○** |
| **documentation-agent**| `mermaid-skill` (다이어그램 이미지 빌드), `slides` (리뷰 및 데모 슬라이드 레이아웃) | **◎** |
| **prompt-agent** | `graphify` (각 에이전트 시스템 프롬프트 및 컨텍스트 주입 경로 탐색) | **○** |
| **knowledge-base** | `writing-skills` (새로운 모범 패턴 패키징), `graphify` (지식 그래프 갱신 및 wiki 색인 관리) | **◎** |

---

## 2. 디자인 스킬 유기적 운영 규칙 (Mandatory Workflow)

모든 디자인 관련 작업은 다음 3단계 워크플로우를 반드시 순차적으로 준수해야 합니다.

### 2.1 디자인 스킬 3단계 워크플로우

| 단계 | 대상 스킬 | 주도 에이전트 | 핵심 작업 |
| :--- | :--- | :--- | :--- |
| **1. 구조화** | `ui-ux-pro-max` | `product-agent` | 레이아웃 시스템, 토큰 정의, 와이어프레임 |
| **2. 감각 폴리싱** | `design-taste-frontend`| `design-agent` | 색상 밸런스, 여백, 마이크로 인터랙션 |
| **3. 품질 감사** | `impeccable` | `quality-agent` | 접근성, 인지 부하, 엣지 케이스 검증 |

### 2.2 스킬 활용 원칙
1. **순서 강제:** 1단계 없이 2단계를 진행하거나, 2단계 없이 3단계로 바로 넘어갈 수 없습니다.
2. **에이전트 책임:** 각 단계는 명시된 에이전트가 주도하여 완수해야 합니다.
3. **결과물 아카이빙:** 각 단계 완료 시, 해당 스킬이 산출한 디자인 정의(토큰, 레이아웃 규칙, 폴리싱 가이드)를 `.agents/docs/design/` 하위 파일들에 즉시 반영해야 합니다.

---

## 3. 스킬 트리거 조건 (Triggering Conditions)

에이전트는 당면한 자연어 명령어, 소스 코드 상태 및 컨텍스트에 따라 다음 조건에 맞춰 최적의 스킬을 트리거해야 합니다.

### 💡 `ui-ux-pro-max` 트리거 조건
* **주요 타겟 에이전트**: `product-agent`, `design-agent`, `architecture-agent`
* **명령어 기반**: `"화면 설계해줘"`, `"기본 레이아웃 뼈대 잡아줘"`, `"새로운 페이지 그리드 구성해줘"` 등
* **컨텍스트 기반**:
  - 신규 대시보드 화면 기획 또는 와이어프레임 뼈대 설계 시.
  - 전역 테마 토큰, CSS 변수 및 공용 컴포넌트 라이브러리 레이아웃을 정의/변경할 때.

### 💡 `taste` / `taste-skill` 트리거 조건
* **주요 타겟 에이전트**: `design-agent`, `ui-agent`
* **명령어 기반**: `"디자인이 너무 촌스러워, 세련되게 다듬어줘"`, `"색상 조화롭게 어울리게 맞춰줘"`, `"위젯 간 패딩/여백 어색해"` 등
* **컨텍스트 기반**:
  - 이미 구동하는 화면의 세부 위젯 마진/패딩 수치를 세밀히 조율해야 할 때.
  - 개별 컴포넌트 간 비주얼 간섭이나 정렬 불일치가 발견되어 미세 폴리싱이 필요할 때.

---

## 4. 유기적 개발 수명 주기(SDLC) 워크플로우

```
[ Phase 1: 규격화 및 뼈대 ] ────────► [ Phase 2: 감각적 폴리싱 ] ────────► [ Phase 3: 완벽성 검증 ]
   - ui-ux-pro-max 기동                 - taste-skill 기동                 - impeccable 기동
   - 그리드/공용 테마 확정               - 미세 패딩 바느질/톤앤매너          - UX 품질 게이트 감사
```

### 1단계: 구조적 설계 및 토큰 수립 (Phase 1)
* **작업 주체**: `product-agent` ➡️ `design-agent`
* **기동 스킬**: **`ui-ux-pro-max`**
* **행동**:
  1. 기획 단계에서 수립된 완료 기준(DoD)을 바탕으로, 화면의 거시적 구조(3단 분할 그리드, 사이드바 레이아웃 등)를 결정합니다.
  2. `ui-ux-pro-max/design-system` 서브 스킬을 기동하여 프로젝트 고유의 공통 디자인 토큰서 및 CSS 가이드라인을 정의해 전달합니다.

### 2단계: 감각적 스타일링 및 미세 튜닝 (Phase 2)
* **작업 주체**: `design-agent` ➡️ `ui-agent`
* **기동 스킬**: **`taste` / `taste-skill`**
* **행동**:
  1. 1단계에서 수립된 기본 그리드 레이아웃을 상속받아, Streamlit 위젯들이 실제 렌더링될 때의 미세한 위화감을 걷어냅니다.
  2. `taste/stitch-design-taste` 스킬을 사용하여 위젯과 차트 프레임 간 여백을 픽셀(px) 단위로 조율하고, `brandkit`을 활성화하여 차트와 폰트 색상이 브랜드 정체성과 일치하도록 세부 색조를 입힙니다.

### 3단계: 최종 품질 검역 (Phase 3)
* **작업 주체**: `ui-agent` ➡️ `quality-agent`
* **기동 스킬**: **`impeccable`** (💎 결함 제로의 UI 품질 보증)
* **행동**:
  1. `ui-agent`가 화면 개발을 임시 종료하면, `quality-agent`는 `impeccable` 스킬을 트리거합니다.
  2. `impeccable` 스킬을 가동하여 인지 부하(Cognitive Load) 최소화, 웹 접근성 표준, 반응형 엣지 렌더링 검사 등 UX 디테일을 집요하게 감사 및 다듬은 후 릴리스 배포 게이트를 패스시킵니다.
