---
id: skill.agentmemory.write_skill
type: reference
status: active

summary: >
  Write Skill 참조 및 가이드 명세서.

parent: "[[skills/agentmemory/SKILL]]"

updated: 2026-06-28
---

# agentmemory 스킬 신규 작성 표준

* **Parent (상위 스킬)**: [[skills/agentmemory/SKILL]]

---


본 문서는 agentmemory 규격의 스킬을 신규 작성하거나 기존 스킬을 갱신할 때 준수해야 하는 공통 포맷과 규칙을 기술합니다.

agentmemory 스킬은 한눈에 읽히고, 정확하며, 최신 상태를 유지할 수 있도록 통일된 계층 구조 포맷을 따릅니다. 스킬 작성 시 이 규격을 엄격히 지켜 주십시오.

## 디렉토리 구조 표준 (Directory Layout)

```text
plugin/skills/<name>/
  SKILL.md      (필수, 100라인 이내로 작성)
  REFERENCE.md  (선택, 빽빽한 세부 정보 및 자동 생성 데이터 테이블 배치)
  EXAMPLES.md   (선택, 작업 트랜스크립트 예시 수록)
```

## SKILL.md 작성 세부 규칙

- **YAML Frontmatter**: `name`, `description`, 선택 옵션인 `argument-hint` 및 `user-invocable` 필드를 선언합니다. 사용자가 슬래시 명령어 형태로 직접 구동하는 액션 스킬인 경우에만 `user-invocable: true`로 설정하며, 참조(Reference) 및 지식(Knowledge)형 스킬은 `false`로 지정합니다.
- **Description(설명)**: 최대 두 문장으로 구성되며, 에이전트가 스킬을 로드할지 결정할 때 조회하는 유일한 필드입니다. 첫 번째 문장에는 핵심 역량을 기재하고, 두 번째 문장은 "Use when"으로 시작하며 구체적인 트리거 조건들을 나열합니다. 다른 형제 스킬들과 확실히 구별되어야 하며, 3인칭 시점으로 1024자 이내로 작성합니다.
- **본문 구성 순서**: Quick start(구체적인 예시 1개) -> Why(핵심 원칙) -> Workflow(판단 분기 처리가 포함된 단계별 순서 번호) -> Anti-patterns(가장 자주 발생하는 실수에 대한 WRONG vs RIGHT 대조 표기) -> Checklist -> See also(연관 스킬 교차 링크) -> Reference 또는 Troubleshooting 포인터 순으로 나열합니다.
- **분량 제약**: 반드시 100라인 이내를 유지하십시오. 복잡하고 많은 양의 사실 관계 정보는 REFERENCE.md로 이관하고, 예제 텍스트들은 EXAMPLES.md 파일로 분리하십시오.
- **교차 참조**: 링크 참조 깊이는 최대 1단계(One level deep)로 제한합니다. 공통 복구 및 해결 절차는 `../_shared/TROUBLESHOOTING.md`에 단일화하여 작성하며, 개별 스킬 본문 내에 인라인으로 중복 기재하지 않습니다.

## 최신성 유지 방안

소스 코드 상에 직접 존재하는 팩트 데이터(도구 이름 및 파라미터, REST 엔드포인트, 환경 변수, 연결 어댑터, 훅 이벤트 등)는 수동으로 기재하지 않고 생성기를 통해 자동 추출합니다. 소스 코드를 편집한 후 `npm run skills:gen`을 실행해 테이블을 자동 갱신하십시오. CI 파이프라인에서 `npm run skills:check` 도구가 구동되어 코드와의 오정합(Drift) 발생 시 빌드를 차단하므로, 데이터의 최신성이 완벽히 보장됩니다.

## 스타일 가이드

외부 또는 타 경쟁사 제품명을 기재하지 마십시오. 이모지 사용을 엄격히 금지합니다. 대시 기호(Em-dashes)나 불필요한 미사여구를 배제하고, 사실 관계를 명확하고 간결하게 서술한 뒤 마무리하십시오.

## 준수 검증 체크리스트 (Checklist)

- Description 필드에 구체적인 트리거가 담긴 "Use when" 문장이 포함되었는가?
- SKILL.md 본문 분량이 100라인 이내로 작성되었는가?
- 시간 가변적인 주장이나 중복된 트러블슈팅 블록이 배제되었는가?
- 구체적인 Quick start 예시가 포함되었으며, 정적인 사실들은 생성기를 통해 자동 추출되었는가?
- 교차 링크가 정상 작동하며 참조 깊이가 1단계 이내인가?
