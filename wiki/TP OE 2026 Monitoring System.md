---
id: wiki.tp_oe_2026_monitoring_system
title: "[Wiki] TP OE 2026 Monitoring System Architecture"
type: wiki
status: active
updated: 2026-07-07
---

# [Wiki] TP OE 2026 Monitoring System Architecture (TP OE 2026 모니터링 시스템 아키텍처)

본 문서는 TP 공장(PLANT = 'TP')의 **2026년 이상 MP-GATE** 타깃 규격을 추적하고, SQLite 및 Databricks DWH를 결합한 삼위일체(PRD, UI, Plot) 통합 데이터 아키텍처를 영구 보존하기 위해 작성된 기술 설계 명세 위키(Wiki) 자산입니다.

---

## 1. 왜 존재하는가? (Why)
- **비즈니스 목적**: 신차 개발 프로젝트의 대량 생산 전환 전, 생산 달성률과 품질 데이터(Scrap, Rework, Uniformity)를 정량 관측함으로써 개발 지연 리스크를 선제 제어합니다.
- **아키텍처 목적**: 분산된 이종 데이터베이스(`staging.db` 와 `ops.db`) 간 데이터 타입 불일치를 해결하고, Streamlit 에디터에서 일어나는 SQLite 다중 DML 가공 처리를 단일 DB 트랜잭션 하에서 수동 보장하여 데이터 정합성 실패 및 오염을 완전히 원천 방어합니다.

---

## 2. 무엇과 연결되는가? (Connections)
- **에이전트 제약 헌법**: [AGENTS.md](../AGENTS.md) (WSL 상대 경로 및 이모지 불용 규칙 준수)
- **요구사항 정의 (PRD)**: [app/pages/_10_dashboard/tp_oe_monitoring_prd.md](../../app/pages/_10_dashboard/tp_oe_monitoring_prd.md)
- **비즈니스 일정 규칙**: [rules/L2-business-constants.md](../rules/L2-business-constants.md)
- **정적 퀄리티 가이드**: [skills/quality-assurance/SKILL.md](../skills/quality-assurance/SKILL.md)
- **원천 의사결정 로그 (Raw)**: [.agents/raw/decision/raw_20260707_161300_tp_oe_2026.md](../raw/decision/raw_20260707_161300_tp_oe_2026.md)

---

## 3. 어디에서 사용하는가? (Where)
- **페이지 화면 렌더러**: [app/pages/_10_dashboard/tp_oe_monitoring_page.py](../../app/pages/_10_dashboard/tp_oe_monitoring_page.py) (Streamlit UI 및 데이터 에디터 트랜잭션 제어)
- **통합 비즈니스 서비스**: [app/service/tp_oe_2026_service.py](../../app/service/tp_oe_2026_service.py) (SQL 연도 필터링 및 Left Join 데이터 타입 캐스팅 병합)
- **품질 회귀 테스트**: [tests/test_tp_oe_2026_service.py](../../tests/test_tp_oe_2026_service.py) (5대 M-Code와 필수 4대 개발 칼럼 무결성 정적 검정)

---

## 4. 아키텍처 상세 사양 및 비즈니스 룰 (Architectural Core Spec)

### ① Target M-Code Extraction (타깃 자재코드 추출 규칙)
- `staging.db`의 `iqm_plus_spec_master` 내에서 `PLANT = 'TP'` 조건과 SQLite 연도 분할 수식 `SUBSTR(MP_GATE_DT, 1, 4) >= '2026'` 조건을 만족하는 5대 유효 자재코드 집합을 도출했습니다.
- 도출 대상: `1033649`, `1033647`, `2022188`, `1034831`, `1034828`

### ② Dual DB Type Casting Left Join (이종 DB 데이터 타입 캐스팅 결합)
- `staging.db` (`MCODE` TEXT형)와 `ops.db` (`M-code` INTEGER형) 간 데이터 병합 시, `CAST(MCODE AS INTEGER)` 처리를 SQL 수준에서 실행하여 데이터 누락 현상을 정적으로 극복했습니다.

### ③ SQLite Manual Transaction and Session Interception (수동 트랜잭션 및 세션 가로채기)
- **트랜잭션 가드**: `conn.isolation_level = None` 설정과 명시적 `BEGIN TRANSACTION / COMMIT / ROLLBACK` 설계를 통해 M-Code 수동 데이터 변경의 완벽한 롤백 안전성을 수립했습니다.
- **세션 클리너**: `st.data_editor` 에디팅 직후 저장 버퍼 충돌을 막기 위해 `st.session_state.pop(key)` 을 가동하고 `st.rerun()`으로 리셋을 트리거하는 인터셉트 기법을 사용했습니다.

---

## 5. 다음에 무엇을 읽어야 하는가? (Next Action)
- **Streamlit 위젯 기법**: [Streamlit UI Development.md](Streamlit UI Development.md) (세션 충돌 방지 및 Segmented Control 구현 지침)
- **테스트 무결성 정립**: [Harness Testing & Quality Gate.md](Harness Testing & Quality Gate.md) (배포 전 격리 Mock 테스트 작성 프로토콜)
