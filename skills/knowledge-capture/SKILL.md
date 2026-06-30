---
name: "knowledge-capture"
description: "카파시 코드 가이드라인 적용, 세션종료 지식 자율 수확(Capture), 마크다운 Frontmatter 및 링크 린트 검증(Lint), 그리고 위키 자동 구조화 동기화를 하나의 통합 루프로 수행하는 고품질 지식 자산 케어 시스템입니다."
id: skill.knowledge_capture
title: "[Skill] Knowledge Capture & Quality Loop"
type: skill
status: active
parent: "[skills/index.md](../index.md)"
related:
  - "[skills/index.md](../index.md)"
  - "[rules/L2-metadata-standard.md](../../rules/L2-metadata-standard.md)"
  - "[principles/Knowledge Curation.md](../../principles/Knowledge Curation.md)"
consumers:
  - agent.all
updated: 2026-06-30
---

# Skill. Knowledge Capture & Quality Loop (지식 및 품질 통합 순환 루프)

## Overview / Connections
* **Parent (상위 개념)**: [skills/index.md](../index.md)
* **연관 가이드 및 자산**:
  - [rules/L2-metadata-standard.md](../../rules/L2-metadata-standard.md)
  - [principles/Knowledge Curation.md](../../principles/Knowledge Curation.md)

본 스킬은 에이전트가 소프트웨어 설계 및 개발 구현을 시작하고 배포 및 종결에 이르기까지, 소스 코드 품질 점검(Karpathy Guidelines), 문서 포맷 및 정합성 검증(Lint), 지식의 정량 수확(Capture), 그리고 위키 연동 보존(Writing Wiki)을 **단 하나의 유기적인 루프로 실행하도록 정의된 통합 품질/지식 수명 주기 시스템**입니다.

---

## 1. 지식 및 품질 4단계 순환 프로토콜 (The Unified 4-Stage Loop)

에이전트는 작업 마감 단계에 진입했을 때(또는 사용자가 "완료", "종료", "정리해줘"를 요청했을 때) 아래 4개의 단계를 하나의 연속적인 파이프라인으로 무조건 수행해야 합니다.

```
[시작] ──> [Stage 1. Karpathy 코드 검정] ──> [Stage 2. 마크다운 & 링크 린트]
                                                      │
[최종 완료] <── [Stage 4. Wiki 문서화/Index] <── [Stage 3. 지식 수확(Capture)]
```

### Stage 1. Andrej Karpathy 코드 무결성 검정 (Karpathy Guidelines)
* **목적**: 대형 언어 모델의 일반적인 코딩 실수와 오작동 유발 코드를 외과 수술식으로 사전 정비합니다.
* **에이전트 수칙**:
  1. **사전 가정 표면화**: 작성된 코드가 암묵적으로 의존하고 있는 환경이나 조건이 있다면 코드 주석과 독스트링을 통해 명확히 기술합니다.
  2. **극단적 복잡성 지양**: 코드는 항상 가장 직관적이고 단순하게 설계하며, 오버엔지니어링(미래용 설계 등)을 배제합니다.
  3. **코드 변경 최소화 (Surgical Changes)**: 꼭 필요한 영역에 대해서만 최소 단위로 수정하고, 기존 주석과 docstring의 포맷을 손상 없이 온전히 보존합니다.
  4. **성공 기준 정량화 및 한글 주석**: 모든 모듈, 클래스, 함수에는 한국어(Korean) 독스트링을 Google/NumPy 포맷으로 필히 삽입하며, 이모지의 삽입은 전면 차단합니다.

### Stage 2. 마크다운 메타데이터 및 연결망 린트 (Knowledge Linting)
* **목적**: 마크다운 파일들의 Frontmatter 유효성과 연결 하이퍼링크의 무결성을 기계적으로 사전 스캔합니다.
* **에이전트 수칙**:
  1. 에이전트는 즉시 아래 검증 스크립트를 기동해야 합니다.
     ```bash
     python3 .agents/skills/knowledge-capture/scripts/lint_markdown.py
     ```
  2. **자동 보정(Auto-Fix) 반영**: Frontmatter 필수 필드(`id`, `title`, `type`, `status`, `updated` 등) 누락으로 스크립트가 자동 보정을 단행했다면 변경 파일을 Git Staged 상태에 업데이트합니다.
  3. **동기화 결핍 경고 (`KNOWLEDGE_OUT_OF_SYNC`) 대응**:
     * 만약 스크립트가 에러 코드 `2`를 리턴하고 지식 갱신 누락을 알리면, 에이전트는 즉시 종료 단계를 중단하고 Stage 3로 기동하여 지식 캡처 및 위키 수록 절차를 이행해야 합니다.

### Stage 3. 세션 종료 지식 자율 수확 (Knowledge Capture)
* **목적**: 이번 세션에서 발견 및 해결한 문제점, 핵심 비즈니스 로직, 새로운 인프라 및 환경 설정을 정제하여 영구 지식 자산으로 수집합니다.
* **에이전트 수칙 (4대 판단 파이프라인)**:
  * **단계 1. 새로운 지식인가? (Raw 수집)**: 세션 중 발생한 독특한 트러블슈팅 이력이나 연동 정보가 있다면 원천 데이터 그대로 `.agents/raw/` 하위에 파일로 캡처합니다. (예: `raw_20260630_142100.md`). *주의: 한 번 작성된 Raw 파일은 사후 수정/편집을 철저히 금지합니다.*
  * **단계 2. 기존 Wiki와 연관되는가? (Wiki 보강)**: 수집된 Raw가 기존 위키 개념을 개정해야 하는 내용인 경우 해당 위키를 최신 SSOT 상태로 즉시 개정 보완합니다.
  * **단계 3. 완전히 새로운 개념인가? (Wiki 설계)**: 기존 어떤 범주에도 속하지 않는 지식은 신규 위키 문서로 설계하여 생성합니다. (Stage 4 규칙 준수)
  * **단계 4. 색인 변경이 필요한가? (Index 동기화)**: 위키 트리 구조가 변경되었다면 인덱스 파일도 실시간 동기화 갱신합니다.

### Stage 4. 위키 정형화 및 평문 상대 링크 배선 (Writing Wiki)
* **목적**: 지식을 정형 템플릿에 맞추어 마크다운 문서로 작성하고, 연결 오류가 없는 무결한 위키 연결망을 생성합니다.
* **에이전트 수칙**:
  1. **위키 구조 필수 4대 구성 원칙**: 모든 위키 문서는 다음 항목을 반드시 명확히 기술해야 합니다.
     * **왜 존재하는가?** (Why)
     * **무엇과 연결되는가?** (Connections) - 관련된 다른 위키, 룰, 스킬로의 상대 경로 링크 제공
     * **어디에서 사용하는가?** (Where)
     * **다음에 무엇을 읽어야 하는가?** (Next Action)
  2. **WSL 호스트 연결 평문 상대 경로 의무화**:
     * 에이전트는 위키 내 하이퍼링크 작성 시 절대 경로 및 `file:///` 프로토콜을 철저히 기각해야 합니다. 오직 워크스페이스 기준 평문 상대 경로(예: `[rules/L2-architecture.md](../../rules/L2-architecture.md)`)만을 사용하여 WSL 환경 하에서의 파일 오픈 연동 에러를 완벽하게 차단합니다.

---

## 2. 핵심 제약 및 가드레일 (Absolute Guardrails)

- **유일성**: 중복되거나 파편화된 위키 생성을 지양하고, 기존 지식을 지속적으로 개정·확장하는 것을 우선 원칙으로 삼습니다.
- **이모지 불용**: 터미널 출력 로그, 마크다운 텍스트, 주석 등 어떠한 곳에서도 일반 유니코드 이모지(아이콘)를 절대 노출하지 않습니다.
- **정량 검증 완료 후 종료**: 모든 4단계 순환 프로토콜을 통과하고 최종 린트 및 앵커 정적 분석 명령어 반환값이 `0` (정상 통과)이 되는 것을 입증해야만 성공을 선언하고 종료할 수 있습니다.
