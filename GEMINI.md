# Agent OS 에이전트 스킬 거버넌스 및 설계 지침 (.agents/GEMINI.md)

본 문서는 Agent OS 내 에이전트 및 스킬 간의 관리 지침입니다.

## .agents 디렉토리 분류 체계 (Taxonomy)

| 분류 | 폴더 | 설명 | 주요 문서 |
| :--- | :--- | :--- | :--- |
| **지식 (Know)** | `context/` | 실시간 실무 지식 베이스 | `checklist/`, `prd/`, `guide/` |
| | `wiki/` | 구조화된 기술 자산 위키 | 위키 마크다운 |
| **철학 (Why)** | `docs/` | 프로젝트 비전 및 설계 원칙 | `philosophy/`, `router/` |
| **규칙 (Guard)** | `rules/` | 프로젝트 준수 제약 표준 | `L2-architecture.md` 등 |
| **기능 (Do)** | `skills/` | 에이전트 행동 역량 패키지 | `impeccable/`, `ponytail/` |
| **인프라 (Manage)**| `tools/` | 파이프라인 관리 유틸리티 | `lint_markdown.py` |
| **산출물 (Output)**| `artifact/` | 에이전트 작업 결과물 | `plans/`, `specs/` |

---

## 상세 분류 기준 (Definition)

- **Context vs Docs**: **Context**는 에이전트가 코드를 짤 때 옆에 펼쳐두는 '실무 지침(How)'이며, **Docs**는 프로젝트의 존재 이유와 근본 철학을 설명하는 '설계 사상(Why)'입니다.
- **Tools vs Skills**: **Tools**는 시스템 자체가 스스로를 관리하고 배포/린트하는 '관리 도구(Ops)'이며, **Skills**는 에이전트가 사용자의 목적을 해결하기 위해 기동하는 '전문 행동 능력(Action)'입니다.
