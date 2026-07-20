---
id: checklist.index
title: "[Context] Checklist Index"
type: reference
status: active

summary: >
  checklist/ 디렉터리 규정 마이크로 가이드라인.
  품질 검사 및 체크리스트 레이어의 로컬 규칙과 보유 파일 정보 및 책임을 요약한다.

keywords:
  - checklist
  - quality-gate
  - index
  - readme

parent: concept.home

related:
  - "[context/checklist/checklist-architecture.md](checklist-architecture.md)"
  - "[context/checklist/checklist-coding-standard.md](checklist-coding-standard.md)"
  - "[context/checklist/checklist-git.md](checklist-git.md)"
  - "[context/checklist/checklist-release.md](checklist-release.md)"
  - "[context/checklist/checklist-security.md](checklist-security.md)"
  - "[context/checklist/reverse-sync-prevention.md](reverse-sync-prevention.md)"

consumers:
  - "[agents/roles/08_quality-agent.md](../../agents/roles/08_quality-agent.md)"
  - "[agents/roles/08_quality-agent.md](../../agents/roles/08_quality-agent.md)"

updated: 2026-06-28
---


# checklist/ 규정

## Overview
* **왜 존재하는가 (Why)**: 코드 리뷰 및 릴리즈 승인 단계에서 품질 검증 기준으로 활용할 5대 마스터 체크리스트와 자가 치유 피드백 로그를 한눈에 인지하고 동기화하기 위함입니다.
* **언제 사용하는가 (When)**: 개발 완료 후 코드 리뷰를 진행하거나, 릴리즈 전에 최종 무결성을 자체 검증하고자 할 때 참고합니다.
* **연계 실행 (Next Action)**: 아키텍처 정합성 검사 세부를 보려면 [.agents/context/checklist/checklist-architecture.md](checklist-architecture.md)로 이동해 지침을 파악하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](../../AGENTS.md)
* **연관 자산**: 
  - [.agents/context/checklist/checklist-architecture.md](checklist-architecture.md)
---

## 1. 로컬 핵심 제약 (Local Rules)

* **코드 리뷰 연동 필수 (Review Binding)**: 본 폴더에 있는 마스터 체크리스트들은 코드 리뷰어 에이전트(`code-reviewer`)가 작업을 수행할 때 상시 대조·검역하는 용도로 자동 탑재됩니다. 체크리스트 추가 시 에이전트 가이드와의 정합성을 항시 연동하십시오.
* **불변 명문화**: 체크리스트는 프로젝트 아키텍처 및 품질을 가르는 최후의 보루입니다. 체크리스트 수정 시에는 타당한 엔지니어링 사유와 변경 히스토리를 반드시 Changelog에 기록하십시오.
* **이모지 전면 금지 및 표준 기호 채용**: 모든 체크리스트 및 가이드 내에서 유니코드 이모지(Emoji) 사용은 엄격히 금지됩니다. 아이콘 필요시 오직 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용하십시오.

---

## 2. 활성 파일 목록 인덱스 (Active Files)

| 파일명 | 파일의 본질적 역할 및 책임 (1줄 요약) |
| :--- | :
---
 |
| `checklist-architecture.md` | 3-Layer 아키텍처 격벽, 의존성 방향 및 1:1 대칭 매핑 정합성 검사 체크리스트 |
| `checklist-coding-standard.md` | 명명 규칙, 데이터클래스 파라미터 전달, 동적 컬럼 맵핑 및 이모지 금지 검사 체크리스트 |
| `checklist-git.md` | 한국어 커밋 메시지, 대괄호 태그 규칙, Dual Push 및 단방향 Rsync 정책 검사 체크리스트 |
| `checklist-release.md` | 코드 릴리즈 전 전수 검증 및 빌드 정합성 자가 진단 체크리스트 |
| `checklist-security.md` | 컨텍스트 및 시스템 데이터 유출 방지를 위한 최소 권한 및 보안 검토 체크리스트 |
| `reverse-sync-prevention.md` | 에이전트 오작동 자가 치유를 위해 실시간 수집된 RCA 분석록 및 재발 방지 누적 수칙 |

---

## 3. 변경 이력 (Changelog)

* **2026-06-18**:
  * [REFACTOR] `intelligence/checklist/` 폴더를 `.agents/context/checklist/`로 완전히 이관하여 지식 자산 통합 및 관심사 격리(SoC)를 고도화.
* **2026-06-14**:
  * [Feat] 가이드(`guide/`) 레이어에 산재해 있던 체크리스트 항목들을 본 신설 폴더(`checklist/`) 아래 5대 마스터 파일로 승격·이관 완료.
  * [Feat] 체크리스트 폴더 전용 `agents.md` 로컬 가이드라인 최초 수립 및 비치.
