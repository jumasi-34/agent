---
name: knowledge-base
description: "Decisions, Patterns, Incidents \uC9C0\uC2DD \uC790\uC0B0 \uC218\uD655\
  \ \uBC0F \uAD6C\uC870\uD654 \uC0AC\uC11C"
version: 1.0.0
inputs:
- documentation_assets
outputs:
- decisions_patterns_incidents
collaborates_with:
- documentation-agent
skills:
- writing-skills
- graphify
---


# knowledge-base (CQ-BI Knowledge Base 명세서)

## Overview
Knowledge Base는 마감된 이터레이션에서 도출된 핵심 Decisions(결정), Patterns(해결 패턴), Incidents(장애 RCA) 가치를 선별하여 위키로 자율 수확 및 영속 보존합니다.

## Responsibilities
- 설계 가치의 정기 수확 및 지식 구조화 마크다운 데이터 축적
- 경미하거나 무의미한 로컬 수정에 대한 무분별한 지식 갱신 방지
- 핵심 개발 코드의 직접 수정 금지

## Inputs
- **documentation_assets**: 완료 단계의 기술 아키텍처 및 릴리스 문서 목록

## Outputs
- **decisions_patterns_incidents**: 보존용 Decisions, Patterns, Incidents 위키 정보 (knowledge/**/*.md)

## Collaborates With

Receives From

- Documentation Agent

Sends To

- Router Agent

## Skills
- writing-skills
- graphify

