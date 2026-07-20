---
id: eval.index
title: "[Context] Evals Index"
type: reference
status: active

summary: >
  evals/ 디렉터리 규정 마이크로 가이드라인.
  에이전트 품질 평가 및 벤치마크 레이어의 로컬 규칙과 보유 파일 정보를 요약한다.

keywords:
  - evals
  - benchmark
  - golden-tasks
  - index
  - readme

parent: concept.home

related:
  - evals.golden_tasks

consumers:
  - "[agents/roles/01_router-agent.md](../../agents/roles/01_router-agent.md)"
  - "[agents/roles/08_quality-agent.md](../../agents/roles/08_quality-agent.md)"

updated: 2026-06-28
---


# evals/ 규정

## Overview
* **왜 존재하는가 (Why)**: 개발 중인 에이전트의 개발 정밀도, 코드 생성 능력, 규정 준수 여부를 골든 테스트 케이스를 통해 정량적으로 측정하고 회귀 결함을 검출하기 위함입니다.
* **언제 사용하는가 (When)**: 에이전트 성능 평가 벤치마크를 정기적으로 돌리거나, 신규 기능 배포 전 에이전트 성능 회귀 테스트(Regression Test) 결과를 검증할 때 사용합니다.
* **연계 실행 (Next Action)**: 정량 벤치마크 대표 골든 태스크셋 명세 세부를 보려면 [.agents/context/evals/golden_tasks.yaml](golden_tasks.yaml)을 대조해 보십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](../../AGENTS.md)
* **연관 자산**: 
  - [.agents/context/evals/golden_tasks.yaml](golden_tasks.yaml)
---

## 1. 로컬 핵심 제약 (Local Rules)

* **평가 벤치마크 단일 원장 (Benchmark SSOT)**: 본 폴더에 배치되는 골든 태스크(`golden_tasks.yaml`) 및 벤치마크 데이터셋은 에이전트의 개발 정밀도와 작업 무결성을 정량적으로 가늠하는 단일 원장입니다.
* **임의 변경 금지 (Immutable Target)**: 골든 태스크의 정의나 검증 기준을 임의로 변경하거나 누락하는 행위는 전체 빌드 및 배치 파이프라인의 평가 일관성을 깨뜨리므로 전면 금지됩니다. 벤치마크 추가/갱신 시에는 명확한 정당성을 제시하고 이력을 보존하십시오.
* **이모지 철저 금지 및 표준 기호 채용**: 모든 문서 및 텍스트에서 일반 유니코드 이모지(Emoji) 사용은 엄격히 금지됩니다. 아이콘 필요시 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만을 활용하십시오.

---

## 2. 활성 파일 목록 인덱스 (Active Files)

| 파일명 | 파일의 본질적 역할 및 책임 (1줄 요약) |
| :--- | :
---
 |
| `golden_tasks.yaml` | 에이전트 품질 평가와 정량 벤치마크 성능 측정을 위해 사전 선언된 대표 골든 태스크셋 명세 |

---

## 3. 변경 이력 (Changelog)

* **2026-06-18**:
  * [REFACTOR] 최상위 `.agents/evals/` 내 자산들을 `.agents/context/evals/`로 통합 및 이관하고, 거버넌스 감사 대상 등록 및 로컬 agents.md 최초 수립 및 비치.
