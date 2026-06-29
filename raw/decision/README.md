---
title: "[Raw] Readme"
id: raw.readme
type: raw
status: unresolved
updated: 2026-06-29
---
# Raw Decision Repository (결정 이력 원본 데이터 저장소)

## 1. 보존 대상 정보 (Stored Information)
이 폴더에는 아키텍처 변경안 확정, UI 디자인 시맨틱 컬러 선정, 예외 처리 설계 확정 등 개발 전반에서 인간과 AI가 최종 합의하여 도출한 주요 의사결정 사항(ADR, Architecture Decision Records)의 원본과 합의 맥락 정보를 기록 보존합니다.

## 2. 데이터 관리 대원칙 (Data Immutability Rules)
- **AI 전용 생성 제한**: 이 영역의 모든 파일과 데이터는 오직 AI 개발 에이전트만이 자동으로 생성 및 기록할 수 있습니다.
- **영구 수정 및 가공 금지 (Immutable Raw Space)**: 한 번 기록된 원본 정보는 시스템의 과거 이력을 증명하는 유일한 물리적 단서(Evidence)이므로, 기록된 이후에는 인간 및 AI를 막론하고 **그 어떠한 상황에서도 수정, 삭제, 가공(Mutation)할 수 없습니다.**
