---
id: guide.new_page_development_workflow
type: reference
status: active

summary: >
  새로운 품질 대시보드 화면이나 신규 데이터 테이블 연계 요청 시 요구사항 분석(PRD), 데이터 분석(EDA), 3레이어 설계, 코드 생성, 품질 통과 검증 및 자동화 배포에 이르는 단계별 자율 에이전트 협업 실행 프로세스(Run-book).

keywords:
  - workflow
  - page-development
  - process
  - deployment
  - automation

parent: "[[context/guide/guide-index]]"

related:
  - "[[context/guide/3layer-development-process]]"
  - "[[context/guide/page-template-standard]]"

consumers:
  - "[[agents/roles/planner-orchestrator]]"
  - agent.ui_builder
  - agent.service_builder

updated: 2026-06-28---

# new_page_development_workflow.md (신규 품질 대시보드 화면 및 시각화 개발 프로세스)

## Overview
* **왜 존재하는가 (Why)**: 신규 화면 추가 또는 대규모 마이그레이션 요구 시 단 한 단계의 데이터 검증이나 3레이어 격리 수칙도 무시되지 않도록 기획부터 검증, 푸시까지의 표준 작업 경로를 완수하기 위함입니다.
* **언제 사용하는가 (When)**: 새로운 Streamlit 웹 애플리케이션 화면 개발을 시작하거나 대시보드 신규 탭을 대규모 기획하여 반영할 때 참조합니다.
* **연계 실행 (Next Action)**: 구체적으로 작성해야 할 표준 PRD 문서 템플릿과 보관 위치를 파악하려면 [prd.readme](../prd/prd-index.md)를 참조하십시오.

## Connections
* **상위 개념**: [guide.readme](.agents/context/guide/guide-index.md)
* **연관 자산**:
  - [.agents/context/prd/prd-index.md](.agents/context/prd/prd-index.md)
  - [.agents/context/guide/3layer-development-process.md](.agents/context/guide/3layer-development-process.md)
  - [.agents/context/guide/page-template-standard.md](.agents/context/guide/page-template-standard.md)

---

이 문서는 사용자가 "새로운 품질 모니터링 화면을 추가해 달라" 또는 "신규 테이블 데이터를 연계해 달라"는 프롬프트를 건넸을 때, 여러 에이전트와 자원들이 유기적으로 체이닝되어 안전한 코드를 최종 배포하기까지 거쳐야 하는 **실행형 다단계 협업 프로세스(Run-book)**입니다.

---

## 🚀 전체 협업 워크플로우 맵 (Chaining Map)

```
[사용자 요청 수임]
       │
       ▼
 ┌───────────────┐
 │   1단계       │  ── Planner 에이전트가 요구사항을 분석하여 PRD 마크다운 작성
 │   PRD 기획    │     - 작성 경로: .agents/context/prd/prd-*.md
 └───────┬───────┘
         │ PRD 배포 완료
         ▼
 ┌───────────────┐
 │   2단계       │  ── EDA 서브에이전트 기동 (사전 브리핑 지원)
 │  데이터 EDA   │     - skill/skill_db_schema_loader.py 및 skill_data_profiler.py 기동
 └───────┬───────┘     - 산출 마크다운: .agents/context/domain/eda-*.md
         │ 사전 데이터 명세 확정
         ▼
 ┌───────────────┐
 │   3단계       │  ── Query & Service 빌더 에이전트 개발
 │ 쿼리/전처리   │     - SQL 쿼리 구현: app/queries/*_query.py
 └───────┬───────┘     - Pandas 가공 & 캐싱: app/service/*_df.py
         │ 가공 데이터 공급 준비 완료
         ▼
 ┌───────────────┐
 │   4단계       │  ── Page & Plot 빌더 에이전트 개발 (WOW Factor 구현)
 │ 화면/시각화   │     - Plotly 차트: app/pages/*_plots.py
 └───────┬───────┘     - Streamlit UI: app/pages/*_page.py
         │ 코드 제출 완료 (Git pre-commit 트리거)
         ▼
 ┌───────────────┐
 │   5단계       │  ── Code Reviewer 및 Quality Evaluator 정적/정량 검증
 │ 코드리뷰/평가 │     - rules/L2-architecture.md 5대 불변 규칙 대조
 └───────┬───────┘     - guardrail/ 검역 엔진 실행 후 배포 게이트(Merge) 통과
         │ Pass
         ▼
[수동 병합 및 최종 배포]
```

---

## 📋 단계별 실행 세부 수칙 및 검증 게이트

### **[1단계] 요구사항 수집 및 PRD 기획 (Planner)**
* **목수**: 사용자 프롬프트로부터 비즈니스 요구사항을 가시화하고 구현할 화면 사양을 마크다운으로 설계합니다.
* **통제 게이트 (Gate)**:
  - 기획서는 반드시 `.agents/context/prd/` 하위에 위치해야 하며, 임의 개발 전 사용자의 피드백을 통해 1차 완결성을 획득해야 합니다.
  - 프로덕션 소스 코드(`.py`)를 절대 직접 생성하거나 수정하지 마십시오.

### **[2단계] 사전 데이터 분석 및 EDA (Analyst)**
* **목수**: 신규 개발에 연계할 원천 DB 테이블을 정량/정성적으로 철저히 해설하여 개발 에이전트들의 버그를 예방합니다.
* **통제 게이트 (Gate)**:
  - 수동으로 SQL 풀 스캔 쿼리를 작성하여 로컬 메모리를 오염시키는 것을 금지합니다.
  - 반드시 `skill/skill_db_schema_loader.py`와 `skill_data_profiler.py` 스킬 도구를 실행하여 안전하게 스키마 메타데이터와 결측치 통계를 수집하십시오.

### **[3단계] SQL 쿼리 빌더 및 전처리 개발 (Query & Service Builder)**
* **목수**: 영문 물리명 기반의 안전한 SQL을 조립하고, Pandas 메서드 체이닝을 활용해 전처리를 고속 수행 및 캐싱합니다.
* **통제 게이트 (Gate)**:
  - SQL 쿼리에 디스플레이용 한글 명칭(AS "공장코드" 등)을 절대 하드코딩하지 마십시오.
  - Pandas 가공은 체이닝 방식을 철저히 적용하고, Databricks 과금 비용 통제를 위해 `@st.cache_data` 캐싱을 반드시 부착하십시오.

### **[4단계] Streamlit 화면 및 시각화 조립 (Page & Plot Builder)**
* **목수**: 사용자에게 프리미엄 첫인상(WOW Factor)을 줄 수 있는 고급스럽고 아름다운 Streamlit 대시보드를 빌드합니다.
* **통제 게이트 (Gate)**:
  - `*_page.py` 파일 내에서 Plotly 차트 스타일링이나 대규모 데이터 루프 연산을 하드코딩하지 마십시오. 모든 시각화 Object 생성은 `*_plots.py` 내부로 귀속시켜 격리합니다.
  - UI 레이어, 탭, 텍스트, 주석 등 소스 코드 전반에서 유니코드 이모지(Emoji) 사용을 전면 배제하고 오직 `:material/icon_name:` 구문만 사용하십시오.
  - **Plotly 6대 수칙 완수 여부 자가 진증**:
    1. 모든 하드코딩된 HEX/RGB 컬러 코드가 배제되고 `Colors` 토큰화가 적용되었는가?
    2. 중복 드로잉 대신 `components.py` 기반으로 컴포넌트화가 수행되었는가?
    3. 필요한 컬러가 없을 경우 `ui.py`에 토큰화 후 사용하였는가?
    4. 무분별한 신설 대신 기존 시각화 컴포넌트의 기능 확장을 검토하였는가?
    5. 기능 확장이 불가능한 경우에만 독립 컴포넌트를 추가하였는가?
    6. Layout 공통 요소(축 스타일, 타이틀 등)는 요소별 공통 모듈/메서드를 활용해 캡슐화하였는가?

### **[5단계] 정적 코드 리뷰 및 평가 검역 (Review & Evaluation)**
* **목수**: 작성 완료된 소스 코드가 시스템 대원칙과 L2 아키텍처 수칙을 완벽히 수호했는지 정밀 분석합니다.
* **통제 게이트 (Gate)**:
  - 개발자가 `git commit`을 시도하면, `hook/`이 개입하여 `guardrail/` 검사기를 자동으로 구동시킵니다.
  - 가드레일 검사기가 코드 스타일, 한글 하드코딩 여부, 이모지 유무, **그리고 Plotly 컬러 하드코딩 및 테마 수칙 준수 여부(`plotly_style_validator.py`)**를 스캔하여 0이 아닌 Exit Code를 반환할 경우, 커밋 및 푸시는 즉각 실패(Abort) 처리됩니다.

