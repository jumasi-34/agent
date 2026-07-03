# * [Orchestration - Routing Table & Pipeline Planner]

## 1. Overview
* **왜 존재하는가 (Why)**: 1단계(Work Classification) 및 2단계(Intent Analysis) 판단 결과를 기반으로 프로젝트 전체 에이전트 조직 전반의 구체적인 협업 동선(실행 파이프라인)을 동적으로 튜닝하고 기획하기 위함입니다.
* **언제 사용하는가 (When)**: 사용자의 복잡한 요구사항에 대응하여 중복 개발을 차단하고, 가장 효율적이며 품질이 입증될 수 있는 에이전트 구동 계획을 PM 관점에서 수립하려 할 때 실행합니다.
* **연계 규칙**: [routing_table_rules.json](routing_table_rules.json) | [execution_planner.json](execution_planner.json)

---

## 2. Decision Logic (판단 및 조율 메커니즘)

Router Agent는 다음 5가지 절차적 규칙을 준수하여 최종 실행 파이프라인 계획서(Execution Plan)를 도출해야 합니다.

### ① 입력 정보의 결합 분석 (Context Synthesis)
- 1단계 분류에서 도출된 `Work Category`와 2단계 분류에서 도출된 `Intent ID`를 대조하여, [routing_table_rules.json](routing_table_rules.json)에 수록된 6대 주요 시나리오 중 가장 일치하는 시나리오를 선정합니다.

### ② 지연 바인딩 및 동적 스킵 규칙 (Lazy Loading & Dynamic Skipping)
- 무조건 표준 파이프라인의 모든 에이전트를 차례로 구동하지 않고, 사용자의 요청 범위에 따른 "최소 필수 에이전트"만 편입합니다:
  - **데이터베이스/쿼리 스킵**: 요청 내에 신규 지표나 데이터 마트 정의가 수반되지 않고 단순 화면 UI 렌더링 개선만 요구될 시, `data-modeling-agent` 및 `data-agent` 단계는 파이프라인에서 즉시 소거(Skip)합니다.
  - **컴포넌트 스킵**: 기존에 등록된 공통 필터나 Plotly 시각화 모듈을 완전히 그대로 사용하고 단순 화면 상하단 배치 레이아웃만 조율하는 경우, `component-agent` 단계를 생략합니다.
  - **아키텍처 스킵**: 단순 텍스트 패치나 이모지 치환 등 마이크로 수정 사안인 경우, `architecture-agent`와 `requirements-agent` 단계를 동시 스킵하고 `page-builder-agent` 및 `reviewer-agent`만 편성합니다.

### ③ 사전 재사용 검역 프로토콜 (Pre-Reuse Audit)
- 시나리오상 UI/UX 변경(Create/Improve)이 수반되는 경우, 구현 단계 직전에 반드시 `component-librarian-agent`를 배치하여 "As-Is 컴포넌트 풀 대비 재사용 가치 타당성" 분석 리포트를 먼저 산출하게 규정합니다.

### ④ 검증 및 최종 관문 지정 (Quality Gates)
- 파이프라인에 소스 코드 구현(Python, SQL) 단계가 1개라도 포함된 경우, 반드시 `reviewer-agent` (코드 가드레일 정적 리뷰)와 `evaluator-agent` (테스트 및 정량 스코어 채점) 단계를 연속으로 포함하고, 최종 패치 전 `release-agent`를 배치해 수동 머지 승인 상태로 대기하도록 계획합니다.

### ⑤ 지식 자산화 연동 (Knowledge Curation Hook)
- 모든 이터레이션의 종결 단계에는 `documentation-agent` 및 `knowledge-curator-agent`를 강제 바인딩하여, 개발 중 도출된 주요 사양과 문제 해결 기법이 마스터 위키와 룰에 자율 전파되도록 명시합니다.

---

## 3. Output Format (최종 실행 계획서 표준 규격)

Router Agent는 아래의 완성도 높은 포맷 양식으로 최종 오케스트레이션 계획서를 한국어로 일목요약하여 출력해야 합니다. (일반 유니코드 이모지 사용 절대 금지, WSL 상대 경로 준수)

```markdown
# [Router Orchestration Plan] - <요청 요약 제목>

## 1. 정성적 문맥 이해 (Intent & Context)
- **사용자 요청 본질**: <사용자가 정말로 해결하고자 하는 정성적 비즈니스 가치 기술>
- **분석된 Work 분류**: <1단계 분류 결과 (우선순위 및 탐색 디렉토리)>
- **분석된 Intent 분류**: <2단계 분류 결과 (기대 가치 및 매핑 에이전트)>

## 2. 매칭된 표준 시나리오 (Standard Scenario)
- **선정 시나리오**: <6대 표준 시나리오 중 택1>
- **시나리오 본질**: <해당 시나리오의 목적과 중요성 설명>

## 3. 동적 실행 파이프라인 (Dynamic Pipeline Sequence)
- **최종 확정된 에이전트 목록 및 구동 순서**:
  ```text
  Router Agent
  → <에이전트명 1> (역할 설명 및 기획된 세부 임무)
  → <에이전트명 2> (역할 설명 및 기획된 세부 임무)
  ...
  → Reviewer Agent (정적 코드 및 가이드라인 리뷰)
  → Evaluator Agent (하네스 구동 및 90점 이상 정량 평가 통과 강제)
  → Release Agent (릴리스 노트 작성 및 수동 머지 대기)
  → Knowledge Curator Agent (마스터 위키 및 룰셋 자율 수확 전파)
  ```
- **생략된(Skipped) 에이전트 및 사유**:
  - `<에이전트명>`: <지연 바인딩에 의거하여 스킵된 합리적 아키텍처적 사유 설명>

## 4. 사전 재사용성 대조 가이드 (Pre-Reuse Audit Guide)
- **검역 타겟**: <재사용을 먼저 탐색해야 할 기존 컴포넌트, 쿼리, 룰 명시>
- **기대 효과**: <중복 개발 방지를 통해 보존될 플랫폼 청정도 목표 기술>

## 5. 단계별 예상 산출물 & 합격 기준 (Definition of Done & Gate Score)
- **주요 산출 파일 목록**:
  - `[파일 상대 경로 링크](상대 경로)`: <산출될 결과물의 구체적 포맷 및 책임 내용>
- **품질 게이트 기준**:
  - **Reviewer Agent Gate**: <아키텍처 위반 0건, 명명 규칙 오류 0건 필수 검역>
  - **Evaluator Agent Gate**: <하네스 유닛 테스트 통과율 100%, 종합 품질 평점 90점 이상 달성 필수>
```
