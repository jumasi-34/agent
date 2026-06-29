---
title: "[Wiki] 에러 격리 및 로깅"
id: "wiki.error isolation & logging standard"
type: wiki
status: active
updated: 2026-06-29
---
# Error Isolation & Logging Standard (에러 격리 및 로깅 표준 가이드)

## 1. 왜 존재하는가 (Why)
이 가이드는 다수의 유저가 접속하여 세션을 공유하는 Streamlit 운영 런타임 중에 특정 컴포넌트의 오류가 화면 전체의 먹통(Crash)으로 유입되는 것을 물리적으로 차단하고, 데이터베이스 쓰기 경합 도중 발생하는 `database is locked` 예외와 로그 위변조 현상을 원천 방어하기 위해 존재합니다. 엄격한 에러 격리 및 로깅 감사 표준을 설계하여 시스템 운영 무결성을 성취합니다.

## 2. 어디와 연결되는가 (Connections)
- **아키텍처 레이어 예외 전파 차단**: 데이터베이스 연산 단계에서 발생한 에러를 안전하게 포장하여 상위 계층으로 반환하는 흐름은 [Architecture Guide](Architecture Guide.md)에 근간합니다.
- **테스트 예외 감지 및 디버깅**: 테스트 수행 중의 오류 로그 감사는 [Harness Testing & Quality Gate](Harness Testing & Quality Gate.md)의 샌드박스 테스트 시나리오와 완전 동기화됩니다.
- **장애 완치 기록 장기 기억 학습**: 수집된 런타임 오류 및 복구 패턴 정보는 [Agent Collaboration & Memory](Agent Collaboration & Memory.md)의 장기 벡터 데이터베이스 지식으로 영속 등록됩니다.

## 3. 무엇을 이해해야 하는가 (What)
- **SQLite 동시성 잠금 예외 방어 (WAL Mode)**:
  - 동시 읽기 및 쓰기 성능 저하와 Lock 현상을 극적으로 극복하기 위해 SQLite 커넥션 취득 시 WAL(Write-Ahead Logging) 모드를 명시적으로 활성화해야 하며, `timeout=30.0`초 이상의 타임아웃을 안전 래퍼 구문 내에 필수 적용합니다.
- **Streamlit 에러 바운더리 격리 렌더링**:
  - 화면 일부에서 연산 크래시가 유발되더라도 페이지 전체 렌더링이 중단되지 않도록, 예외 발생 구역을 `st.error` 경고 보드로 격리 렌더링하고 세션은 안정 탈출하도록 예외 처리 구조를 짭니다.
- **오디팅 로그의 생성 일시 서버 고정**:
  - 로그 조작을 방지하기 위해 생성 타임스탬프(`LOG_DT`)는 클라이언트 측 입력을 일절 배제하며, 오직 서버 시스템의 실시간 표준시(`datetime.now()`)에 의해 원천 고정 기입되도록 로직을 일원화합니다. 관련 실물 헬퍼는 [app/core/infrastructure/sqlite_client.py](app/core/infrastructure/sqlite_client.py) 등에 안전하게 내장 설계합니다.
