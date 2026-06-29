---
name: "guardrail"
description: "에이전트가 코드 커밋, 푸시, 패치 배포를 가동하기 전에 이모지 존재 유무(emoji_checker.py), 커밋 메시지 표준(commit_msg_validator.py), 데이터베이스 물리 스키마(schema_validator.py)를 사전 자율 진증하는 통합 정적 가드레일 스킬입니다."
id: skill.quality.guardrail
title: "[Skill] Guardrail"
type: skill
status: active

parent: "[skills/index.md](../../index.md)"

related:
  - "[skills/index.md](../../index.md)"

consumers:
  - agent.all

updated: 2026-06-28
---

# guardrail (통합 자가 배포 가드레일 스킬)

## Overview / Connections
* **Parent (상위 개념)**: [skills/index.md](../../index.md)


이 스킬은 코드 형상관리 및 배포 전조 단계에서 에이전트 스스로 패치 무결성과 스타일 수칙 준수 여부를 다각도로 검증할 수 있도록 돕는 자율 진단형 정적 가드레일 툴킷입니다.

## 1. 수록된 3대 검증 유틸리티 및 사용법

### ① Emoji Existence Checker (`emoji_checker.py`)
- 파이썬 소스 코드나 마크다운 파일, Streamlit 컴포넌트 텍스트 내에 일반 유니코드 이모지(Emoji)가 사용되었는지 전수 스캔하여 검출합니다.
- 아이콘이 필요한 곳에는 반드시 Streamlit 기본 Google Material 아이콘 구문(`:material/icon_name:`)만 사용하도록 유도합니다.

### ② Commit Message Validator (`commit_msg_validator.py`)
- Git 커밋 메시지가 한국어로 작성되었는지 및 알맞은 성격 머리말 태그 접두사(`[FEAT]`, `[FIX]`, `[REFACTOR]`, `[RULE]` 등)를 충실히 동반하였는지 유효성을 대조합니다.

### ③ Database Schema Validator (`schema_validator.py`)
- 쿼리 및 서비스 전처리 가동 전, 데이터베이스 원천 테이블의 골든 스키마 정적 구조와 맵핑이 올바르고 깨짐 없이 유지되고 있는지 정밀 진증합니다.

### ④ Plotly Style & Color Validator (`plotly_style_validator.py`)
- 플롯 파일(`*_plots.py`) 및 화면 파일(`*_page.py`) 전반을 스캔하여, `components.py`를 무회하고 직접 차트를 빌딩하는 안티패턴이나 하드코딩된 RGB/HEX 컬러 코드(예: `#f97316` 등)의 사용, `light_theme` 외 불허된 테마 템플릿 호출을 정밀 검출해 냅니다.

## 2. 사용 명령어 및 호출 예시
```bash
# 이모지 검사 전수 스캔 (정적 코드 분석 기동)
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/quality/guardrail/scripts/emoji_checker.py

# Plotly 하드코딩 및 컴포넌트 표준 수칙 검정 기동
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/quality/guardrail/scripts/plotly_style_validator.py

# 커밋 메시지 규격 검증 기동
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/quality/guardrail/scripts/commit_msg_validator.py "일부 소스 정적 수정안"
```

