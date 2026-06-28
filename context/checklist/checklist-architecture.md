---
id: checklist.architecture
type: reference
status: active

summary: >
  L2 3-레이어 아키텍처 및 모듈 격리 체크리스트.
  파일 배치 규칙, 레이어 격리, 파일 1:1 대칭 매핑 등을 정적으로 자가 진증하기 위한 항목들을 담고 있다.

keywords:
  - checklist
  - architecture
  - layer-isolation
  - modularity

parent: "[[context/checklist/checklist-index]]"

related:
  - "[[rules/L2-architecture]]"
  - "[[context/checklist/checklist-coding-standard]]"

consumers:
  - "[[agents/roles/code-reviewer]]"
  - "[[agents/roles/quality-evaluator]]"

updated: 2026-06-28
---


# checklist-architecture.md (L2 3-레이어 아키텍처 및 모듈 격리 체크리스트)

## Overview
* **왜 존재하는가 (Why)**: 개발 중 실수로 아키텍처 격벽을 허물어 UI와 DB가 강결합되는 스파게티 코드가 작성되는 것을 미연에 방지하고, 일률적인 구조적 정합성을 검증하기 위함입니다.
* **언제 사용하는가 (When)**: 개발 완료 후 PR을 생성하기 전이나, 에이전트 자율 코드 검역을 수행할 때 체크리스트 항목을 전수 확인합니다.
* **연계 실행 (Next Action)**: 아키텍처 정합성을 통과한 뒤 구체적인 코딩 표준(명명 규칙 등)을 준증하려면 [checklist-coding-standard.md](.agents/context/checklist/checklist-coding-standard.md)를 확인하십시오.

## Connections
* **상위 개념**: [.agents/context/checklist/checklist-index.md](.agents/context/checklist/checklist-index.md)
* **연관 자산**: 
  - [.agents/rules/L2-architecture.md](.agents/rules/L2-architecture.md)
  - [.agents/context/checklist/checklist-coding-standard.md](.agents/context/checklist/checklist-coding-standard.md)
---

## 1. 3-레이어 파일 배치 규칙
- [ ] **UI 레이어 배치**: 모든 화면 컨트롤러 및 레이아웃, 시각화 파일이 `app/pages/` 하위에 위치하는가?
- [ ] **서비스 레이어 배치**: 모든 비즈니스 로직 및 전처리, 메모리 캐싱 모듈이 `app/service/` 하위에 위치하는가?
- [ ] **쿼리 레이어 배치**: SQL 쿼리 문자열 조립 모듈이 `app/queries/` 하위에 위치하는가?
- [ ] **공통 코어 배치**: 공통 DB 커넥터, 파라미터 데이터클래스, 상수 정의 등이 `app/core/` 하위에 적절히 구성되었는가?

---

## 2. 레이어간 격리 및 격벽 제약 조건
- [ ] **역방향 의존성 금지**: 의존성 방향이 `[UI -> Service -> Query]` 흐름을 충족하며 역방향 참조(예: 쿼리가 서비스를 임포트 등)가 전혀 없는가?
- [ ] **UI 직접 DB 통신 차단**: `app/pages/*_page.py` 또는 `*_plots.py` 내부에서 직접 DB 클라이언트를 구동하거나 쿼리를 실행하지 않고, 서비스 레이어(`app/service/*_df.py`)의 함수를 게이트웨이로만 데이터를 수집하는가?
- [ ] **서비스 레이어 UI 종속성 배제**: `app/service/` 모듈 내에서 `streamlit`, `plotly`, `matplotlib` 등의 시각화/UI 패키지를 임포트하여 차트 객체를 리턴하지 않는가? (서비스는 순수 데이터 타입인 DataFrame, dict, list 등만 취급해야 함)
- [ ] **쿼리 레이어 실행 책임 제거**: `app/queries/` 하위 모듈은 오직 순수 문자열(`str`)인 SQL을 조립하고 반환할 뿐이며, 직접 DB 커넥션을 맺고 쿼리를 실행하지 않는 구조인가?

---

## 3. 파일 1:1 대칭 매핑 및 문서 관리 표준
- [ ] **1:1 대칭 구조**: 모든 화면에서 화면 컨트롤러(`*_page.py`)와 시각화 드로잉(`*_plots.py`)이 명확히 1:1 매핑되어 파일이 분리되었는가?
- [ ] **UI-시각화 역할 분담**: `*_page.py` 내에 Plotly 드로잉 코드가 직접 삽입되지 않았고, 반대로 `*_plots.py` 내부에서 Streamlit 레이아웃 요소(`st.write`, `st.columns` 등)를 호출하지 않았는가?
- [ ] **문서화 리소스 영속 보관**: 모든 도메인 지식, 기술 사양, 가이드 문서가 `.agents/context/` 하위의 공식 지정 폴더(`domain/`, `infra/`, `guide/`)에 구조화되어 저장되었는가? (개별 `CONTEXT.md` 파일의 독립적 존재는 금지함)
- [ ] **AI 참조 차단 영역(Exclusion Zone) 보호**: 개인 메모 공간인 `intelligence/note/` 및 하위 경로에 대해 에이전트의 읽기/검색이 엄격히 통제되고 차단되는가?
