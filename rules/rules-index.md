---
id: rule.index
title: "Ref: RULES > RULES-INDEX"
type: rule
status: active

summary: >
  rules/ 디렉터리 규정 마이크로 가이드라인.
  표준 정책 및 행동 규칙 규정 레이어의 로컬 규칙과 활성 파일 목록 및 책임을 요약한다.

keywords:
  - rules
  - index
  - readme
  - directory-rules

parent: concept.home

related:
  - "[[rules/L1-git.md]]"
  - "[[rules/L2-architecture.md]]"
  - "[[rules/L2-business-constants.md]]"
  - "[[rules/L2-color-system.md]]"
  - "[[rules/L2-context-readability.md]]"
  - "[[rules/L2-naming-convention.md]]"
  - "[[rules/L2-sync-policy.md]]"
  - "[[rules/L3-dashboard.md]]"
  - "[[rules/L3-plot.md]]"
  - "[[rules/L3-query.md]]"
  - "[[rules/L3-service.md]]"
  - "[[rules/L2-metadata-standard.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"
  - "[[agents/roles/quality-evaluator.md]]"

updated: 2026-06-28
---


# rules/ 규정

## Overview
* **왜 존재하는가 (Why)**: 에이전트와 소스 코드가 예외 없이 준수해야 하는 강제 규정(L1, L2, L3)의 종류와 파일별 본질적 책임을 일관되게 정렬하고 한눈에 관리하기 위함입니다.
* **언제 사용하는가 (When)**: 규칙 제정, 개정, 또는 소스 코드 아키텍처의 기준이 되는 상위 제약을 검토하고자 할 때 참고합니다.
* **연계 실행 (Next Action)**: 본 규정 내 폴더의 핵심 설계 수칙을 파악하려면 연이어 [L2-architecture.md](.agents/rules/L2-architecture.md) 대원칙을 확인하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](.agents/AGENTS.md)
* **연관 자산**: 
  - [.agents/rules/L2-architecture.md](.agents/rules/L2-architecture.md)
---

## 1. 로컬 핵심 제약 (Local Rules)

* **절대 강제 규칙 (Absolute Rule enforcement)**: 본 폴더에 배치되는 `L1-*.md`, `L2-*.md`, `L3-*.md` 파일들은 에이전트와 소스 코드가 **예외 없이 100% 준수해야 하는 강제 규정(Must/Shall)**입니다. 어떠한 사적인 우회나 예외 적용도 허용하지 않습니다.
* **설명 및 코드 튜토리얼 배제 (No Tutorials)**: 문서 작성을 할 때는 장황한 설명, 환경설정 커맨드, 구체적인 파이썬 문법 등 교육 목적의 지침을 생략하고, 오로지 **"참/거짓", "수치적 제약", "허용/금지 조항"** 등 법률적 선언 형태로만 조항을 고도로 압축 기술하십시오. (설명과 구현 절차는 `guide/`로 이관)
* **가드레일 자동 검사 연동 (Automated Gate Link)**: 본 폴더에 등재되는 모든 표준 정책(Naming Convention, Git 규칙, 아키텍처 정합 수칙 등)은 신뢰성 확보를 위해 가능한 한 `guardrail/` 산하에 정적 분석 검사기 스크립트로 구현되어 배치 승인 파이프라인에 즉시 편입되어야 합니다.
* **WSL Markdown Link Constraint (WSL 환경 링크 제약)**: WSL(Windows Subsystem for Linux) 환경의 VS Code 터미널 및 채팅창, 마크다운 문서 내에서 절대 리눅스 경로(`file:///home/jumasi/...`)를 사용하면, 호스트 OS(Windows)가 해당 파일 링크를 로컬 윈도우 파일로 해석하여 `0x2` 에러가 발생합니다. 모든 마크다운 자산 내 하이퍼링크 및 AI 에이전트가 채팅창을 통해 제공하는 파일 링크는 반드시 워크스페이스 루트 기준의 평문 상대 경로(예: `[L2-architecture.md](.agents/rules/L2-architecture.md)`) 또는 `./` 기반 상대 경로만을 사용해 에디터 내부에서 정상 열리도록 조치합니다.

---

## 2. 활성 파일 목록 및 온디맨드 매핑 인덱스 (Active Files & Targeted Loading)

에이전트는 수행 중인 작업 유형에 맞춰 아래 매핑 테이블을 기준으로 **단 1개의 타겟 파일**만 선택하여 로드하십시오.

| 작업 유형 | 타겟 규칙 파일 | 파일의 본질적 역할 및 핵심 제약 수칙 |
| :--- | :--- | :--- |
| **Git 버전 관리** | [L1-git.md](.agents/rules/L1-git.md) | 커밋 메시지 한국어 작성 및 태그 접두사 의무화, Dual Push 원칙 |
| **시스템 아키텍처** | [L2-architecture.md](.agents/rules/L2-architecture.md) | 3-Layer(UI-Service-Query) 물리 격리 및 Pandas 체이닝, UI 6대 정합성 수칙 |
| **비즈니스 상수** | [L2-business-constants.md](.agents/rules/L2-business-constants.md) | 물리 공장 코드 정적 매핑 및 이중화 방지, 도메인 상수 일원화 |
| **컬러 시스템** | [L2-color-system.md](.agents/rules/L2-color-system.md) | IBM Carbon 테마 기반의 대시보드 및 플롯 컬러 시스템 정적 일치화 |
| **코드 가독성** | [L2-context-readability.md](.agents/rules/L2-context-readability.md) | 중복 명 접두사 배제 및 AI 컨텍스트 가독성 최적화 수칙 |
| **메타데이터 표준** | [L2-metadata-standard.md](.agents/rules/L2-metadata-standard.md) | YAML Frontmatter 속성 규격 및 상태(status) 생애주기 관리 제약 |
| **코드 명명 규칙** | [L2-naming-convention.md](.agents/rules/L2-naming-convention.md) | 계층별 명명 규칙 표준화 및 함수 생성, 독스트링 기술 표준 |
| **자산 동기화** | [L2-sync-policy.md](.agents/rules/L2-sync-policy.md) | 로컬과 원격 간의 rsync 일방향 동기화 및 자산/데이터 불변 수칙 |
| **쿼리 설계** | [L3-query.md](.agents/rules/L3-query.md) | SQL 내 디스플레이 한글 AS 하드코딩 금지 및 영문 물리 컬럼명 보존 |
| **서비스 전처리** | [L3-service.md](.agents/rules/L3-service.md) | 데이터프레임 가공 전담 및 메서드 체이닝 표준 준수 |
| **UI 화면 구성** | [L3-dashboard.md](.agents/rules/L3-dashboard.md) | Streamlit 페이지 라우팅 제어 및 Google Material Symbols 화면 렌더링 |
| **데이터 시각화** | [L3-plot.md](.agents/rules/L3-plot.md) | UI 레이어 1:1 매핑 Plotly 차트 격리 구현 규정 |


---

## 3. 변경 이력 (Changelog)

* **2026-06-14**:
  * [FIX] 마크다운 자산 내 절대 파일 경로(`file:///`)를 프로젝트 상대 경로로 일괄 변환(19개 파일)하고, 향후 재발 방지를 위해 WSL 하이퍼링크 제약 수칙을 로컬 규칙에 추가 영속화.
  * [REFACTOR] `rules/` 레이어 정의를 단순 가이드에서 예외 없는 '표준 정책 및 행동 규칙 규정 레이어'로 승격하고, 설명/튜토리얼 생략 및 법률적 압축 수칙을 명문화.
  * [Feat] 규정 폴더 전용 `agents.md` 최초 비치.
