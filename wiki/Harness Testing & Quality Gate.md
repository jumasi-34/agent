---
title: "[Wiki] 품질 게이트 검증"
id: "wiki.harness testing & quality gate"
type: wiki
status: active
parent: "Git Dual Push & Rsync Sync.md"
related: ["Error Isolation & Logging Standard.md"]
consumers: ["../agents/roles/quality-evaluator.md"]
updated: 2026-06-29
---
# Harness Testing & Quality Gate (하네스 테스트 및 품질 가드레일)

## 1. 왜 존재하는가 (Why)
이 가이드는 사용자의 승인 없이 프로덕션 소스가 오염되거나 린팅 에러, 구문 충돌, SQLite 골든 스키마 일탈 등으로 서비스 불능 상태에 빠지는 것을 선제 검역하기 위해 존재합니다. 정적 정합성 가드레일과 샌드박스 테스트 체계를 구축하여 완벽히 증명된 성공(Evidence) 데이터만 배포되도록 통제합니다.

## 2. 어디와 연결되는가 (Connections)
- **3-Layer 경계 및 쿼리 무결성 진증**: 레이어 침범 및 SQL 구문 한글 하드코딩 여부는 [Architecture Guide](Architecture Guide.md)의 격리 아키텍처에 근간하여 진단됩니다.
- **인수 기준 부합 검증**: 기획 및 순차 구현 계획서 상에 수립된 체크포인트는 [PRD Planning Workflow](PRD Planning Workflow.md)의 목표와 완전 연동됩니다.
- **런타임 에러 로그 감시 및 기억**: 테스트 구동 시 발생한 에러 히스토리와 장애 정보는 [Agent Collaboration & Memory](Agent Collaboration & Memory.md)에 학습 등록됩니다.

## 3. 무엇을 이해해야 하는가 (What)
- **검증 코드의 독립 샌드박스 제약**:
  - 하네스 테스트 및 목킹 검증 코드는 실제 소스에 영향을 주지 않도록 오직 `tests/` 디렉터리 산하에 신규 생성되는 테스트 파일로 격격 구성되어야 합니다.
  - 실제 자산 및 DB 파일을 물리적으로 훼손하거나 오염시키지 않는 인메모리(In-Memory) 목킹 및 데이터 보존 기법을 100% 사수해야 합니다.
- **배포 전 자율 정적 검증 (Quality Gate)**:
  - 배포 전 반드시 `verify_code.py` 정적 코드 컴파일 진증, `emoji_checker.py`를 통한 잔존 유니코드 이모지 완전 소거, `sql_analyzer` 정적 스캔을 가동하여 결함 제로의 상태를 스스로 증빙해야 합니다.
