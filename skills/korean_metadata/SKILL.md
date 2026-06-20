---
name: korean_metadata
description: 원천 DB 영문 물리 컬럼명에 대응하는 디스플레이용 한글 명칭, 소수점 포맷팅, 툴팁 설명 등의 정적 딕셔너리를 자동 매핑 및 업데이트해 줍니다.
---

# korean_metadata (디스플레이용 한글 메타데이터 생성 및 매핑 스킬)

이 스킬은 데이터베이스의 영문 물리 컬럼명들과 디스플레이용 한글 명칭, 정적 포맷팅, 툴팁 도움말 정보 등을 동적으로 매핑하고 구성 파일 형태로 자동 작성/유지보수할 수 있도록 돕는 메타데이터 관리 전용 도구입니다.

## 1. 사용 시기 (Usage Trigger)
- 데이터베이스 테이블 구조가 변경되거나, UI 화면 상에 새로운 물리 컬럼을 노출해야 할 때.
- 수많은 영문 피처 및 지표 컬럼명들에 대해 일관된 디스플레이 명칭 사전을 동적 수집하여, 코드의 수작업 하드코딩 맵핑 리스크를 전면 우회하고자 할 때.

## 2. 사용 명령어 및 호출 방법
```bash
PYTHONPATH=/home/jumasi/workstation /home/jumasi/miniconda3/envs/goeq/bin/python .agents/skills/korean_metadata/scripts/skill_generate_korean_metadata.py
```

## 3. 핵심 아키텍처 연동 수칙
- 바이브 코딩 및 동적 메타데이터 컬럼 맵핑을 성실히 이행하기 위해, 본 툴을 통해 산출된 메타데이터 설정 사전을 UI 화면(`st.dataframe`, `st.data_editor`)의 `column_config` 설정으로 동적 연동하여 주입합니다.
- 이로써 SQL 쿼리를 고치지 않고 메타데이터만 갱신하여 UI 전체의 피처 한글 명칭 및 포맷팅을 유연하게 제어하는 고수준 격리 아키텍처를 실현합니다.
