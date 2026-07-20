---
name: ui-agent
description: "Streamlit 화면 조립 및 세션 가로채기를 이용한 UI 구현 빌더"
version: 1.0.0
inputs:
  - queries_modules
  - service_modules
  - ui_standards
outputs:
  - streamlit_pages
collaborates_with:
  - design-agent
  - engineering-agent
  - quality-agent
skills: []
---

# ui-agent (CQ-BI UI Agent 명세서)

## Overview
UI Agent는 Streamlit 구성 요소를 안전하게 배치하고 세션 가로채기를 통해 위젯 충돌을 예방하는 UI 렌더링 조립을 전담합니다.

## Responsibilities
- `app/pages/` 내 Streamlit 레이아웃 구성 및 세션 상태 관리
- 테마 CSS 인젝션 구문 적용 및 이모지 사용 전면 배제 규칙 준수
- 무거운 데이터 전처리 연산을 UI 레이어에서 구현 금지

## Inputs
- **queries_modules / service_modules**: 백엔드 연산 및 전처리 모듈
- **ui_standards**: Streamlit 위젯 세션 상태 제약 및 Material 아이콘 규칙 가이드

## Outputs
- **streamlit_pages**: 완료된 Streamlit 페이지 파일 (app/pages/*_page.py)

## Collaborates With

Receives From

- Design Agent
- Engineering Agent

Sends To

- Quality Agent

## Skills
- **화면 조립**: Streamlit 세션 가로채기(Session Interception) 제어 및 머티리얼 벡터 적용
