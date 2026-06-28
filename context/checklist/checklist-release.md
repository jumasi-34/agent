---
id: checklist.release
type: reference
status: active

summary: >
  코드 릴리즈 전 전수 검증 및 빌드 정합성 자가 진단 체크리스트.
  동적 컴파일 검증, 릴리즈 훅 테스트, 예외 로깅 및 DB 정합성을 전수 체크한다.

keywords:
  - checklist
  - release
  - verification
  - production-ready

parent: checklist.readme

related:
  - checklist.architecture
  - checklist.coding_standard

consumers:
  - agent.code_reviewer
  - agent.quality_evaluator

updated: 2026-06-28
---

# checklist-release.md (L1 릴리즈 및 빌드 정합성 체크리스트)

## Overview
* **왜 존재하는가 (Why)**: 개발 완료된 코드가 프로덕션 환경에 배포되기 전, 런타임 오류 및 구문 오류를 원천 차단하고 릴리즈 훅이 정상적으로 완수되는지 자가 검증하기 위함입니다.
* **언제 사용하는가 (When)**: 코드 변경 사항을 실제 서버나 프로덕션 환경에 릴리즈/배포하기 직전 최종 게이트 단계에서 준수합니다.
* **연계 실행 (Next Action)**: 릴리즈를 완수하고 배포 결과 및 에러 예방 로그를 확인하려면 [reverse-sync-prevention.md](.agents/context/checklist/reverse-sync-prevention.md)의 이력을 갱신하거나 확인하십시오.

## Connections
* **상위 개념**: [.agents/context/checklist/README.md](.agents/context/checklist/README.md)
* **연관 자산**: 
  - [.agents/context/checklist/checklist-architecture.md](.agents/context/checklist/checklist-architecture.md)
  - [.agents/context/checklist/checklist-coding-standard.md](.agents/context/checklist/checklist-coding-standard.md)
---

## 1. 빌드 및 컴파일 정합성 (Build & Compilation)
- [ ] **구문 에러 전수 부재**: 릴리즈될 모든 파이썬 파일에 문법 및 구문 에러(`SyntaxError`)가 존재하지 않는가?
- [ ] **가동 검증기 구동**: `.agents/context/guide/testing-verification.md` 가이드에 맞춰 `verify_code.py` 정적 코드 컴파일 검증기를 구동하고 결과가 Pass 되었는가?
- [ ] **인메모리 테스트 통과**: `tests/` 디렉터리에 생성된 신규 독립 테스트 파일들이 실제 파일을 오염시키지 않는 인메모리(In-Memory) 기법으로 모두 완벽히 동작하는가?

## 2. 릴리즈 훅 규격 및 안정성 (Release Hooks)
- [ ] **3단계 로컬 품질 게이트**: `.agents/context/infra/hooks-specification.md`에 정의된 3단계 로컬 품질 게이트 및 장애 대응 릴리즈 훅이 정상 통과되었는가?
- [ ] **Git Hook 정상 기동**: 커밋 및 푸시 가동 시 `pre-push` 혹은 `post-commit` 훅 등이 충돌 없이 완수되는가?
- [ ] **SQLite 로그 기록 정합성**: 에러 격리 가이드(`.agents/context/guide/error-handling.md`)에 정의된 SQLite 에러 로깅 기능이 정상 작동하는가?

## 3. 리소스 및 자산 은닉 (Assets Isolation)
- [ ] **보안 유출 금지**: 프로덕션 배포 파일 내부에 로컬 접속 키, 개인 SSH Key, DB 패스워드 등 민감 정보가 하드코딩되지 않고 `.env`에서 완벽히 로드되는가?
- [ ] **덤프 데이터 격리**: 개발 및 검증 단계에서 임시로 생성된 Parquet/CSV 등 덤프 데이터가 `.gitignore`를 통해 Git 추적 대상에서 완전히 제외되어 있는가?
