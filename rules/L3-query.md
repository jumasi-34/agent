---
id: rule.l3.query
title: "[Rule] SQL 쿼리 작성 표준"
type: rule
status: active

summary: >
  L3 쿼리 레이어 개발 규칙.
  Pure SQL 문자열 조립, CTE 구조, 한글 AS 금지, q_ 접두사 및 과금 방지 수칙을 제어한다.

keywords:
  - sql
  - query
  - cte

parent: "[rules/rules-index.md](rules-index.md)"

related:
  - "[rules/L2-naming-convention.md](L2-naming-convention.md)"
  - "[rules/L3-service.md](L3-service.md)"

consumers:
  - agent.all

updated: 2026-06-29
---


# L3-query.md (L3 쿼리 레이어 개발 규칙)

본 문서는 SQL 문자열 조립 복잡성을 제어하고 필드 매핑 결함을 원천 예방하기 위해 SQL 작성 표준을 규정하는 **단일 진실 공급원(SSOT) 규칙**입니다.

---

## 1. 쿼리 레이어의 핵심 역할 및 위치
* **위치**: `app/queries/` 아래 배치
* **파일명**: `*_query.py` 또는 `q_*.py` 명명 규칙 준수
* **책임**: 오직 데이터베이스에 전달할 **순수 SQL 문자열(`str`)**을 동적으로 조립 및 반환하는 업무만 전담하며, 직접 DB 커넥션을 성립하거나 실행(`execute`)하지 않습니다.

---

## 2. SQL 작성 및 조립 5대 표준

1. **복잡 쿼리 CTE(Common Table Expressions) 지향**: 2단계 이상의 집계 결합, LATERAL VIEW 등 복잡한 로직이 수반될 때는 반드시 CTE(`WITH` 구문)를 설계하여 흐름을 위에서 아래로 논리 나열합니다. 단순 조회는 일반 SELECT문으로 가볍게 처리합니다.
2. **선언적 쿼리 헬퍼 인라인 호출**: `QueryFilter`와 `SQLConverter`를 활용하여 동적 조건을 결합합니다. 이때 가독성을 위해 개별 조건 변수를 남발하지 않고 `QueryFilter.build_where` 리스트 인수 내부에 직접 헬퍼를 인라인 호출로 조립합니다.
3. **한글 AS Alias(별칭) 사용 전면 금지**: SQL 내부에서 디스플레이용 한글 `AS "별칭"` 선언을 엄격히 금지합니다. 무조건 영문 물리 컬럼명(예: `PLANT_CODE`, `MTTC_VAL`)을 그대로 반환하도록 설계하며, 한글 레이블 매핑은 UI 단의 동적 메타데이터 헬퍼에 위임합니다.
4. **반환값 변수(query) 바인딩 및 단일 반환**: 모든 쿼리 조립 함수는 완성된 SQL 문자열을 무조건 `query` 지역 변수에 바인딩한 후 최종 줄에서 `return query` 형태로만 단일 반환해야 합니다. 인라인 즉시 리턴을 금지하여 로깅 및 디버깅을 고도화합니다.
5. **중앙화 테이블 상수 및 파라미터**: 테이블 경로 참조 시 반드시 `core/query/query_database.py` 상수를 바인딩하며, 입력 인자는 `core/params/parameters.py`에 선언된 파라미터 `dataclass`로 수집합니다.

---

## 3. Databricks 과금 방지 및 개발 가이드
* **Parquet 로컬 덤프 활용**: 단순 UI 가공이나 변환 로직 변경 시 실제 DB를 찌르지 말고 `local.data/` 하위 Parquet/CSV 덤프 파일을 활용해 로컬 Mocking 테스트를 진행하십시오.
* **LIMIT 강제 바인딩**: 개발/검증용 임시 쿼리에는 데이터 풀 스캔을 원천 차단하기 위해 반드시 `LIMIT 100` ~ `LIMIT 1000`을 명시하십시오.

---

## 4. 쿼리 레이어 4대 정합성 체크리스트

1. 함수 선언부 직전 라인에 대괄호 형태의 식별용 헤더 주석(`# * [대분류 - 요약 설명]`)을 작성했는가?
2. 쿼리 함수는 직접 실행을 처리하지 않고, 오직 순수 SQL 문자열(`str`)만 반환하는가?
3. SQL 내부의 한글 AS 별칭 하드코딩이 완전히 배제되고 영문 물리 명칭이 보존되어 있는가?
4. 결과 SQL 문자열이 `query` 지역 변수에 명시적으로 담겨 단일 리턴되는가?
