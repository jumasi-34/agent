---
title: "[Skill] Quality Assurance"
name: quality-assurance
description: >
  코드 배포 전 정적 무결성 검증, SQL 정적 분석, 메타데이터 동기화, 자율 정적 컴파일 및 코드 리뷰 프로세스를 전담하는 통합 품질 게이트(Quality Gate) 매크로 스킬입니다.
  에이전트가 코드 수정을 완료하고 최종 승인 및 배포를 이행하려 할 때 반드시 순차 실행하여 무결함 증거를 확보하십시오.
id: wiki.skill
type: wiki
status: active
updated: 2026-06-29
---
# Ref: SKILLS > QUALITY-ASSURANCE (품질 검역 및 자율 리뷰 관문)

본 문서는 개발 수명 주기(SDLC)의 검증 및 배포 준비 단계에서 에이전트가 준수해야 할 모든 정적 검사 및 무결성 검증 단계를 유기적인 5단계 파이프라인으로 단일화하여 제공하는 **통합 품질 검역 매크로 스킬**입니다. 

에이전트는 코드 작성을 완료하는 즉시 본 가이드를 로드하고 아래의 **5대 품질 게이트**를 순차적으로 이행하십시오.

---

## 1. 5대 품질 게이트 유기적 파이프라인 (The Quality Gate Pipeline)

```mermaid
flowchart TD
    Start["[Code Complete] 구현 완료"] --> Gate1["[Gate 1] Guardrail Scan<br>이모지 누락 및 커밋 규격 점검"]
    Gate1 --> Gate2["[Gate 2] SQL Static Analyzer<br>한글 AS 별칭 및 별칭 규칙 점검"]
    Gate2 --> Gate3["[Gate 3] Metadata Sync<br>한글 레이블 사전 연동 상태 점검"]
    Gate3 --> Gate4["[Gate 4] Build & Test Run<br>verify_code.py 및 unittest 무결성 확보"]
    Gate4 --> Gate5["[Gate 5] Review & Handoff<br>리뷰 피드백 반영 및 세션 인계"]
    Gate5 --> End["[Deploy Ready] 배포 승인 대기"]

    style Start fill:rgba(128, 128, 128, 0.1),stroke:var(--text-color),stroke-width:1px
    style Gate1 fill:rgba(128, 128, 128, 0.15),stroke:var(--text-color),stroke-width:1px
    style Gate2 fill:rgba(128, 128, 128, 0.15),stroke:var(--text-color),stroke-width:1px
    style Gate3 fill:rgba(128, 128, 128, 0.15),stroke:var(--text-color),stroke-width:1px
    style Gate4 fill:rgba(128, 128, 128, 0.2),stroke:var(--text-color),stroke-width:1px
    style Gate5 fill:rgba(128, 128, 128, 0.25),stroke:var(--text-color),stroke-width:1px
    style End fill:rgba(128, 128, 128, 0.3),stroke:var(--text-color),stroke-width:1px
```

---

## 2. 게이트별 세부 검증 가이드 및 실행 명령어

### ① Gate 1. Guardrail Scan (정적 가드레일 검사)
* **목적**: 형상 관리에 혼선이 되는 이모지 유출, WSL 절대 경로 기입 및 잘못된 커밋 태그를 정적으로 완벽히 필터링합니다.
* **실천 수칙**:
  1. 소스 코드 내 모든 주석, 문자열, 마크다운 본문 내에 유니코드 이모지가 잔존하지 않는지 `grep_search` 등을 통해 전수 수동 확인합니다.
  2. 마크다운 내 링크가 프로토콜 없는 평문 상대 경로(예: `[L2-architecture.md](../../rules/L2-architecture.md)`) 규격을 빈틈없이 유지하고 있는지 검사합니다.
  3. 에이전트가 코드를 커밋/배포하기 전에, 지식 자산 전반의 깨진 연결과 비표준 링크를 자율 검증하고 무결함을 증명하기 위해 반드시 다음 스크립트를 기동해야 합니다:
     ```bash
     python3 .agents/tools/link_validator.py
     ```
     이 검증기에서 에러가 0건으로 성공("All link validations passed successfully.")해야만 Gate 1을 완전히 통과한 것으로 인정합니다.

### ② Gate 2. SQL Static Analyzer (정적 쿼리 분석)
* **목적**: 쿼리 내 한글 AS 별칭 하드코딩 오류를 선제 방어합니다.
* **실천 수칙**:
  1. 수정된 SQL 쿼리 소스코드(`app/queries/`) 내에 한글 AS 별칭(예: `AS "공장명"`)이 절대 기입되지 않고 오직 물리 영문명만 반환되는지 육안 및 패턴 분석으로 스캔합니다.
  2. 쿼리 반환 값이 `query` 지역 변수에 단일 바인딩되어 최종 리턴되는지 검사합니다.

### ③ Gate 3. Metadata Sync (메타데이터 사전 동기화)
* **목적**: 쿼리에서 영문 컬럼을 반환하므로, 이에 매핑되는 UI 한글 레이블과 툴팁 정보가 메타데이터 사전에 등록되어 있는지 정합성을 정렬합니다.
* **실천 수칙**:
  1. 신규 추가되거나 변경된 데이터베이스 물리 컬럼이 있다면, `local.data/query/` 산하의 관련 메타데이터 사전 JSON 파일에 디스플레이 한글명, 도움말(툴팁) 및 소수점 자릿수 포맷 규격을 수동으로 동기화 등록해야 합니다.

### ④ Gate 4. Build & Test Run (자가 컴파일 및 테스트 기동)
* **목적**: 수정된 파이썬 모듈이 인터프리터 수준에서 에러 없이 완전히 컴파일되고, 독립 테스트 세트가 정상 통과하는지 구체적인 정량적 무결성 증거를 수집합니다.
* **실행 명령어**:
  * **전역 구문/컴파일 분석**:
     ```bash
     PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python tests/verify_code.py
     ```
  * **독립 단위 테스트 격리 기동 (실제 DB 및 파일 오염이 없는 Mock 기반)**:
     ```bash
     PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python -m unittest tests/test_cqms_regression.py
     ```

### ⑤ Gate 5. Review & Handoff (자율 피드백 반영 및 맥락 인계)
* **목적**: 피드백 수집 및 다음 세션에서 작업을 이어나갈 에이전트를 위한 최종 맥락 정합을 완수합니다.
* **실천 수칙**:
  1. 리뷰 피드백이나 에러가 발생한 경우 추측을 배제하고 과학적 가설-검증 프로세스에 의해 수정을 단행합니다.
  2. 작업이 종료되는 시점에 `agent_hooks`에 기록된 런타임 결과 및 성공 증거 데이터를 아티팩트로 출력하고 장기 기억 저장소에 핵심 학습 코드로 등록합니다.

---

## 3. 에이전트 자율 품질 보증 4대 체크리스트

품질 관문을 통과하고 성공을 보고하기 전, 에이전트는 본 문서의 다음 체크리스트에 대해 자율 정합 판단을 내리고 이를 답변에 명시해야 합니다.

1. **[  ] Guardrail**: 프로젝트 소스 트리 내에 유니코드 이모지가 100% 전무하고 마크다운 링크가 평문 상대 경로로 통제되었으며, `link_validator.py`를 실행하여 깨진 연결과 비표준 링크가 0건(SUCCESS)임을 증명하였는가?
2. **[  ] SQL & Metadata**: SQL 쿼리 내의 한글 AS 별칭 하드코딩이 완전히 차단되고, 컬럼명이 로컬 메타데이터 사전에 올바르게 매핑되어 있는가?
3. **[  ] Build & Compilation**: `verify_code.py`를 작동하여 프로젝트 소스 전체 컴파일 무결성을 통과하고, 어떠한 Syntax 에러도 없음이 정량 입증되었는가?
4. **[  ] Test Pass**: 작성된 모든 격리 테스트 케이스(Mock DB 기반)가 정상 성공하여 비즈니스 정합성이 검증되었는가?
