---
name: "agent_hooks"
description: "에이전트 실행 주기 관측(Runs Observer), 자율 세션 실시간 로그 분석(Runs Analyzer), WSL 오작동 방지 및 역동기화 제어(Reverse Sync), 장애상황 릴리즈 수동 복구(Release Hooks)를 총괄 관리하는 하네스 운영 및 감시 전용 툴킷입니다."
id: skill.agent_hooks
type: skill
status: active

parent: "[[skills/index.md]]"

related:
  - "[[skills/index.md]]"

consumers:
  - agent.all

updated: 2026-06-28
---

# agent_hooks (하네스 라이프사이클 훅 및 자율 감시 스킬)

## Overview / Connections
* **Parent (상위 개념)**: [[skills/index.md]]


이 스킬은 에이전트의 오작동을 실시간으로 관측 및 통제하고, 자율 작업 세션에서 생성된 이력을 추적 분석하며, WSL(로컬)과 Ubuntu(서버) 환경의 연쇄 역동기화를 차단하여 일회성 장애 상황에서의 즉각 수동/자동 복구를 지원하는 시스템 관리 제어용 특수 스킬입니다.

## 1. 수록된 4대 핵심 모듈 및 사용법

### ① Runs Observer (`agent_runs_observer.py`)
- 에이전트 구동 전후의 작업 세션 변경점을 추적하여 7대 아티팩트와 작업 히스토리를 정밀 관측하고, 자가 교정 피드백의 핵심 데이터로 영속 보존합니다.

### ② Runs Analyzer (`agent_runs_analyzer.py`)
- 자율 작업 결과 수집된 아티팩트, 소스 Diff, 로그 기록들을 지능적으로 분석하여 세션의 성공 및 비정상 오작동 상태 여부를 평가하고 최종 리포트를 작성합니다.

### ③ Reverse Sync Defender (`reverse_sync.py`)
- WSL 호스트와의 윈도우 파일 시스템 인코딩 및 마운트 오작동을 차단하고, WSL-서버 간의 동기화 단방향 불변 수칙이 무너지지 않도록 동적 모니터링 및 상호 롤백 가이드를 구동합니다.
- 오작동 감지 시 근본 원인(RCA)을 추적하는 진단 데이터를 생성합니다.

### ④ Release Hooks (`release_ops_hooks.py`)
- 서비스 장애가 의발되었을 때, SQLite 임시 로그 적재 상황 분석을 구동하고 롤백 대책을 수립할 수 있도록 릴리즈 운영 훅을 제공합니다.

## 2. 사용 명령어 및 호출 예시
```bash
# 자율 세션 오작동 여부 분석 및 자가 진단 가동
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/agent_hooks/scripts/agent_runs_analyzer.py

# 역동기화 차단 및 로컬 환경 동적 복구 루프 기동
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/agent_hooks/scripts/reverse_sync.py
```


## Sub-Assets (하위 참조 자산)
* [[skills/agent_hooks/ncf_metrics_revamp_plan.md]] — Ncf Metrics Revamp Plan 참조 및 가이드 명세서.
* [[skills/agent_hooks/scripts/README.md]] — Readme 참조 및 가이드 명세서.
