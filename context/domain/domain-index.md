---
id: domain.index
title: "Ref: CONTEXT > DOMAIN > DOMAIN-INDEX"
type: reference
status: active

summary: >
  domain/ 디렉터리 규정 마이크로 가이드라인.
  비즈니스 도메인 지식 원장 레이어의 로컬 규칙과 보유 파일 정보를 요약한다.

keywords:
  - domain
  - business-logic
  - index
  - readme

parent: concept.home

related:
  - "[[context/domain/domain-knowledge.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"
  - "[[agents/roles/quality-evaluator.md]]"

updated: 2026-06-28
---


# domain/ 규정

## Overview
* **왜 존재하는가 (Why)**: 물리적인 기술 구현 세부사항(DWH, SQL)에 귀속되지 않는 범용 비즈니스 개념, 용어, 마스터 코드 및 정밀 지표 산식을 단일 진실 공급원(SSOT)으로 확보하여, 비즈니스 오차를 예방하기 위함입니다.
* **언제 사용하는가 (When)**: 대시보드 내 품질 공식(MTTC, 성적서 합격률 등)을 구현하거나 공장 코드 매핑 논리를 검토할 때 참고합니다.
* **연계 실행 (Next Action)**: 공장별 마스터 코드 및 핵심 수식 세부를 보려면 [.agents/context/domain/domain-knowledge.md](.agents/context/domain/domain-knowledge.md)를 연이어 대조하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](.agents/AGENTS.md)
* **연관 자산**: 
  - [.agents/context/domain/domain-knowledge.md](.agents/context/domain/domain-knowledge.md)
---

## 1. 로컬 핵심 제약 (Local Rules)

* **비즈니스 도메인 순수성 (Domain Purity)**: 이 폴더는 오직 비즈니스 요구 개념, 용어, 산식, 마스터 코드 값의 의미 등 순수한 논리적 비즈니스 맥락만을 보관합니다. 하드웨어 서버 설정, SQL 쿼리 문자열, 물리 데이터베이스 접속 키 등 기술 명세는 절대로 작성하지 마십시오. (→ `infra/`로 이관)
* **산식 정량성 (Mathematical Precision)**: 비즈니스 품질 지표 등 공식 산식을 기재할 경우, 수학적 혹은 관계형 논리에 근거하여 명확하고 엄밀하게 수식화해야 합니다. 모호한 자연어 설명을 최소화하십시오.
* **UI-Service 일관성 (SSOT)**: 여기에 정의된 디코드 명칭(영문 코드 <-> 한글 표시명) 및 데이터 의미 체계는 프로덕션 소스 코드의 비즈니스 서비스(`service/`)와 화면 구성(`pages/`) 전처리에서 일관되게 준수해야 하는 공통의 표준 정의 역할을 수행합니다.

---

## 2. 활성 파일 목록 인덱스 (Active Files)

| 파일명 | 파일의 본질적 역할 및 책임 (1줄 요약) |
| :--- | :
---
 |
| `domain-knowledge.md` | 공장별 마스터 코드, 디코드 테이블, 품질 핵심 공식(수식) 및 도메인 지식 원장 |

---

## 3. 변경 이력 (Changelog)

* **2026-06-14**:
  * [REFACTOR] `domain/` 레이어 정의를 특정 품질 데이터베이스(CQMS, GMES 등)에 귀속되지 않는 범용 '비즈니스 도메인 지식 원장'으로 승격하고, 기술 명세를 엄격히 격리시키는 도메인 순수성 규칙 추가.
  * [Feat] 도메인 폴더 전용 `agents.md` 최초 비치.
