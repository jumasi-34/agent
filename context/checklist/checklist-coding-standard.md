---
id: checklist.coding_standard
title: "[Context] Checklist Coding Standard"
type: reference
status: active

summary: >
  L2 코드 및 데이터 전처리 코딩 표준 체크리스트.
  명명 거버넌스, 데이터 흐름/파라미터 바인딩, 컬럼 맵핑 및 이모지 금지, Pandas 전처리 및 캐싱 등을 자체 검역하기 위한 항목을 포함한다.

keywords:
  - checklist
  - coding-standard
  - naming
  - clean-code
  - pandas

parent: "[context/checklist/checklist-index.md](checklist-index.md)"

related:
  - "[rules/L2-naming-convention.md](../../rules/L2-naming-convention.md)"
  - "[rules/L3-service.md](../../rules/L3-service.md)"
  - "[context/checklist/checklist-architecture.md](checklist-architecture.md)"

consumers:
  - "[agents/roles/code-reviewer.md](../../agents/roles/code-reviewer.md)"
  - "[agents/roles/quality-evaluator.md](../../agents/roles/quality-evaluator.md)"

updated: 2026-06-28
---


# checklist-coding-standard.md (L2 코드 및 데이터 전처리 코딩 표준 체크리스트)

## Overview
* **왜 존재하는가 (Why)**: 코드 스타일의 불일치로 인한 가독성 저하를 방지하고, 이모지 유출 및 SQL 하드코딩 별칭으로 발생하는 런타임 결함을 사전에 자율적으로 예방하기 위함입니다.
* **언제 사용하는가 (When)**: 클래스/함수를 설계하고 생성할 때, 혹은 Pandas 전처리 체이닝을 구성한 후 검역 단계에서 참조합니다.
* **연계 실행 (Next Action)**: 이 체크리스트를 통과한 후 Git 형상관리 및 Rsync 동기화 규칙을 준수하는지 검증하려면 [checklist-git.md](checklist-git.md)를 대조해 보십시오.

## Connections
* **상위 개념**: [.agents/context/checklist/checklist-index.md](checklist-index.md)
* **연관 자산**: 
  - [.agents/rules/L2-naming-convention.md](../../rules/L2-naming-convention.md)
  - [.agents/context/checklist/checklist-architecture.md](checklist-architecture.md)
---

## 1. 명명 거버넌스 및 규칙 준수
- [ ] **레이어별 파일 명명**: 파일명이 각 레이어 표준 접미사(`*_page.py`, `*_plots.py`, `*_df.py`, `*_query.py` 또는 `q_*.py`)를 정확히 준수하는가?
- [ ] **변수 및 함수 표기**: 모든 변수 및 함수 명명에 스네이크 표기법(`snake_case`)을 일관되게 사용하는가?
- [ ] **클래스 표기**: 모든 클래스 이름 명명에 파스칼 표기법(`PascalCase`)을 일관되게 사용하는가?

---

## 2. 데이터 흐름 및 파라미터 바인딩 표준
- [ ] **파라미터 데이터클래스 준수**: 모든 서비스/쿼리 함수가 개별 변수들의 나열이 아닌, `app/core/params/parameters.py` 에 선언된 정형화된 데이터클래스 인자를 넘겨받아 사용하는가?
- [ ] **비즈니스 상수 표준**: 품질 지표 공식이나 공장 코드 사전 등의 비즈니스 상수가 하드코딩되지 않고, `app/core/constants/`를 거쳐 일관되게 로드 및 관리되는가?
- [ ] **SQL 인젝션 방지**: 외부 필터 인자 및 사용자 입력값이 원시 쿼리 문자열에 문자열 포맷팅(`f-string` 등)으로 직접 결합되지 않고, `QueryFilter` 및 `SQLConverter` 헬퍼를 경유하여 동적으로 안전하게 바인딩되는가?

---

## 3. 컬럼 맵핑 및 이모지 엄금 규칙
- [ ] **동적 컬럼 맵핑 준수**: SQL 쿼리 내부에 디스플레이 명칭(한글 별칭, 예: `AS "공장코드"`)을 하드코딩하지 않고 순수 영문 물리 컬럼명만 반환하며, 화면 노출 시 한글화 및 포맷팅 설정은 UI 단에서 `get_dynamic_column_configs` 동적 헬퍼 함수를 연동해 처리하는가?
- [ ] **이모지 사용 전면 금지**: Streamlit UI 페이지, 탭 라벨, 마크다운 텍스트, 버튼, 토스트, 주석 등 모든 소스 코드 영역에서 일반 유니코드 이모지(Emoji) 사용이 완전히 배제되었는가?
- [ ] **Material Symbols 표준**: 아이콘이 필수적인 곳에는 일반 이모지 대신 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 사용하고 있는가?

---

## 4. Pandas 데이터 전처리 및 캐싱 규칙
- [ ] **Pandas 메서드 체이닝**: 서비스 레이어의 데이터 가공 처리가 표준 가이드라인에 맞춰 가독성 높게 메서드 체이닝(Method Chaining) 구조로 일관성 있게 구현되었는가?
- [ ] **방어적 데이터 처리**: Null/NaN 결측치 값 대체 및 Zero Division 예외 방지 등 데이터 부재 시의 런타임 크래시를 예방하기 위한 방어 코드가 삽입되었는가?
- [ ] **캐싱 규정 및 TTL 준수**: Databricks 쿼리 비용 절감을 위한 `@st.cache_data` 캐시 데코레이터가 필수 부착되었으며, TTL 수칙이 엄격히 설계되었는가?
- [ ] **캐시 훼손 매개변수 차단**: 캐시 데코레이터가 부착된 함수 인자로 DB 클라이언트 인스턴스 등 직렬화가 불가능하거나 무의미한 상태 변수가 전송되지 않는가?
