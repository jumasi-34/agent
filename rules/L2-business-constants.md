---
id: rule.l2.business_constants
title: "[Rule] 비즈니스 상수 매핑"
type: rule
status: active

summary: >
  L2 비즈니스 상수 관리 및 호출 표준.
  공장 코드 매핑 등 도메인 상수를 단일 파일로 격리하여 중복과 불일치를 차단한다.

keywords:
  - constants
  - business-logic
  - static-mapping

parent: concept.domain

related:
  - context.domain.knowledge

consumers:
  - "[agents/roles/data-layer-builder.md](../agents/roles/data-layer-builder.md)"
  - "[agents/roles/governance-compliance-auditor.md](../agents/roles/governance-compliance-auditor.md)"

updated: 2026-06-28
---


# L2-business-constants.md (L2 비즈니스 상수 관리 및 호출 규칙)

## Overview
* **왜 존재하는가 (Why)**: 코드 전반에 분산된 공장 기호, 품질 기준치 등의 상수 하드코딩을 차단하고, 단일 진실 공급원(SSOT) 상수를 보장하여 비즈니스 불일치를 예방하기 위함입니다.
* **언제 사용하는가 (When)**: 쿼리 필터 구성, 데이터 전처리 지표 분기, 공장 단위 매핑 조건 조립 등 정적 도메인 분기 식별자가 필요할 때 사용합니다.
* **연계 실행 (Next Action)**: 이 상수들을 소비하여 실제 연산을 전개하는 비즈니스 가이드는 [.agents/context/domain/domain-knowledge.md](../context/domain/domain-knowledge.md)에서 확인하십시오.

## Connections
* **상위 개념**: [.agents/AGENTS.md](../AGENTS.md)
* **연관 자산**: [.agents/context/domain/domain-knowledge.md](../context/domain/domain-knowledge.md)
---

이 문서는 프로젝트 내에서 **비즈니스 상수(Business Constants)**가 추가되거나 변경될 때 일관된 코드 품질과 단일 진실 공급원(SSOT, Single Source of Truth)을 유지하기 위해 준수해야 하는 **엄격한 관리 및 호출 개발 표준**을 정의합니다.


## 1. 핵심 원칙 (Core Principle)

모든 비즈니스 관련 매핑 테이블, 상태 목록, 코드 설명 사전(Dictionary), 필터 목록 등은 개별 소스 코드 내에 하드코딩되거나 분산되어 관리되어서는 안 됩니다.

* **단일 진실 공급원(SSOT)**: 모든 비즈니스 상수는 반드시 `app/core/data_models/business_constants.json` 파일 내에 정의되어야 합니다.
* **호출 일원화**: 소스 코드(UI, Service, Query 레이어 등)는 JSON 파일을 직접 읽거나 개별적으로 상수를 하드코딩하지 않고, `app/core/data_models/business.py`를 거쳐 노출된 파이썬 상수를 호출하는 단일화된 경로를 통해 사용해야 합니다.

---

## 2. 신규 비즈니스 상수 추가 및 수정 절차 (Step-by-Step Guide)

새로운 비즈니스 상수(예: 신규 상태 사전, 공장 매핑 리스트 등)가 필요하거나 기존 값을 수정해야 할 경우, 다음 3단계 절차를 **예외 없이 철저히 준수**해야 합니다.

```
┌──────────────────────────────────────────────┐
│  1. JSON 파일 추가/수정                      │
│     - app/core/data_models/                  │
│       business_constants.json                │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│  2. 파이썬 바인딩 및 __all__ 추가             │
│     - app/core/data_models/business.py       │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│  3. 개별 모듈에서 호출 및 사용               │
│     - app/pages/ , app/service/ 등           │
└──────────────────────────────────────────────┘
```

### [Step 1] JSON 파일에 상수 정의
[app/core/data_models/business_constants.json](app/core/data_models/business_constants.json) 파일 내에 원하는 구조(대문자 Key 권장)로 상수를 정의합니다.

* **주의 사항**: JSON 문법을 완벽히 준수해야 하며, 마지막 요소 뒤에 쉼표(`,`)를 남겨두는 Syntax Error(Trailing Comma)가 발생하지 않도록 각별히 유의합니다.
* **예시 (신규 DICT 추가)**:
  ```json
  {
    ...
    "NEW_BUSINESS_DICT": {
      "01": "정상 상태",
      "02": "경고 상태",
      "03": "오류 상태"
    }
  }
  ```

### [Step 2] 파이썬 상수 바인딩 및 내보내기 (Export)
[app/core/data_models/business.py](app/core/data_models/business.py) 파일에서 JSON 파싱 결과인 `_data` 딕셔너리로부터 상수를 바인딩하고 모듈 외부에서 import할 수 있도록 `__all__`에 등록합니다.

1. **상수 선언 및 바인딩 (대문자 스네이크 케이스 준수)**:
   ```python
   # JSON에서 상수를 바인딩 (기존 바인딩 영역 아래에 추가)
   NEW_BUSINESS_DICT = _data["NEW_BUSINESS_DICT"]
   ```
2. **`__all__` 리스트 등록**:
   ```python
   __all__ = [
       ...
       # JSON에서 로드된 상수
       "PLANT_TO_OEQG",
       "ISSUE_AREA",
       ...
       "NEW_BUSINESS_DICT",  # 신규 등록 필수
   ]
   ```

### [Step 3] 비즈니스 코드에서 임포트하여 사용
UI 레이어, 서비스 레이어, 쿼리 레이어 등에서 선언한 상수가 필요할 경우 아래와 같이 참조하여 사용합니다.

```python
# 올바른 사용 예시 (app/core/data_models/business.py 로부터 import)
from app.core.data_models.business import NEW_BUSINESS_DICT

def process_business_status(status_code):
    status_name = NEW_BUSINESS_DICT.get(status_code, "미정의")
    return status_name
```

---

## 3. 금지 및 규제 사항 (Strict Prohibitions)

1. **인라인 하드코딩 금지**: UI 소스(`app/pages/*_page.py`) 또는 서비스 소스(`app/service/*_df.py`) 내부에서 비즈니스 코드 매핑용 임의 딕셔너리(`dict`)나 리스트를 직접 선언하여 사용하는 행위는 엄격히 금지됩니다.
2. **JSON 직접 파일 IO 접근 금지**: 개별 파일 내에서 `business_constants.json` 파일의 경로를 직접 참조하여 `open()` 및 `json.load()`를 반복 호출하는 행위를 금지합니다. 파일 로드 및 캐싱 오버헤드를 최소화하기 위해 반드시 `business.py` 모듈을 매개체로 통하여야 합니다.
3. **가변(Mutation) 조작 금지**: 호출한 비즈니스 상수는 읽기 전용(Read-Only) 정보입니다. 코드 실행 중 임의로 상수의 요소를 변경하거나(`business_constants["KP"] = ...`), 덮어쓰는 행위는 런타임 사이드 이펙트를 야기하므로 절대 금지합니다.

---

## 4. 안전 정책 연동 (No-Mutation Policy Reminder)

이 규칙 역시 `agents.md` 및 `guide/agent-common.md`에 명시된 **[CRITICAL] 기존 소스 코드 변경 금지 및 차단 장치 (Safety Lock)**의 통제를 받습니다.

* 신규 비즈니스 상수를 등록하기 위해 `business_constants.json` 및 `business.py`를 실제로 수정해야 하는 상황에서도, **개발자(AI 에이전트)는 직접 코드를 변경하지 말고 변경 사안(Diff 제안)을 정리하여 사용자에게 먼저 리포트하고 명시적 승인을 득한 후 작업을 수행**하여야 합니다.

## Related

[Quality Metric & Business Rules](../wiki/Quality Metric & Business Rules.md)
