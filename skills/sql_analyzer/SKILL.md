---
name: "sql_analyzer"
description: "SQL 쿼리 파일 내에 디스플레이용 한글 별칭(AS "한글")이 하드코딩되었는지, 혹은 SQL 5대 불변 규칙을 위배했는지 사전에 감지하고 정밀 진단하는 쿼리 정적 분석기입니다."
id: skill.sql_analyzer
type: skill
status: active

parent: "[[skills/index]]"

related:
  - "[[skills/index]]"
  - "[[context/infra/queries-specification]]"

consumers:
  - agent.all

updated: 2026-06-28---
# sql_analyzer (SQL 쿼리 정적 분석 스킬)

## Overview / Connections
* **Parent (상위 개념)**: [skills/index.md](../index.md)


이 스킬은 개발되거나 리팩토링된 SQL 쿼리 빌더 파일들을 분석하여 하드코딩된 디스플레이 별칭이나 아키텍처 규칙 침범을 사전에 격리 검출하기 위한 전용 정적 분석기입니다.

## 1. 사용 시기 (Usage Trigger)
- 신규 SQL 쿼리 빌더(`app/queries/*_query.py` 등)를 작성하였거나 기존 쿼리를 전면 수정하였을 때.
- 코드 커밋/푸시 이전 또는 에이전트 자율 배포 가이드라인에 따른 SQL 5대 불변 규칙 정합성 검증이 필요할 때.

## 2. 사용 명령어 및 호출 방법
```bash
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/sql_analyzer/scripts/skill_sql_static_analyzer.py [대상_파일_경로]
```

## 3. 정적 검사 주요 원칙 (SQL 5대 불변 규칙)
- **한글 별칭 하드코딩 금지**: SQL 내부에서는 영문 물리 컬럼명만 반환해야 하며, 디스플레이용 한글 맵핑은 반드시 UI 단에서 처리되어야 합니다.
- **예외 없는 에러 격리**: 쿼리 구문 내 문법 오류가 없는지 및 데이터베이스 커넥션을 낭비하지 않는 결합 구조를 취하는지 검사합니다.
- 분석기는 규칙 위반이 감지되는 즉시 상세 문제 라인과 위반 사유를 CLI 화면에 출력하여 개발자와 에이전트에게 즉각적인 오작동 피드백을 제공합니다.
