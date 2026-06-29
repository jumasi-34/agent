---
title: "[Raw] Readme"
id: raw.readme
type: raw
status: unresolved
updated: 2026-06-29
---
# Raw Prompt Repository (프롬프트 원본 데이터 저장소)

## 1. 보존 대상 정보 (Stored Information)
이 폴더에는 에이전트 시스템에 주입된 시스템 프롬프트(System Prompt), 병렬 가동 시 생성된 서브에이전트별 특화 지시 지침서, 그리고 중요 수명 주기 단계에서 사용자가 주입한 실행 지시 프롬프트 원본 템플릿들을 보존합니다.

## 2. 데이터 관리 대원칙 (Data Immutability Rules)
- **AI 전용 생성 제한**: 이 영역의 모든 파일과 데이터는 오직 AI 개발 에이전트만이 자동으로 생성 및 기록할 수 있습니다.
- **영구 수정 및 가공 금지 (Immutable Raw Space)**: 한 번 기록된 원본 정보는 시스템의 과거 이력을 증명하는 유일한 물리적 단서(Evidence)이므로, 기록된 이후에는 인간 및 AI를 막론하고 **그 어떠한 상황에서도 수정, 삭제, 가공(Mutation)할 수 없습니다.**
