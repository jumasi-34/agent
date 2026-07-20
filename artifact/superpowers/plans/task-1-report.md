---
id: docs.superpowers.plans.task-1-report
title: "Task 1 Implementation Report: NCF Tab Orange Badge SOP Date Display"
type: report
status: active
summary: >
  NCF 탭의 첫 번째 메트릭 카드 오렌지 뱃지가 기존의 M+N 양산 기간 대신 
  SOP 시작일(YYYY-MM-DD)을 노출하도록 수정한 작업 결과 리포트입니다.
updated: 2026-07-01
---

# Task 1 Implementation Report

## 1. 개요
- **목적**: NCF(New Car Flow) 탭의 첫 번째 메트릭 카드 우상단에 위치한 오렌지 뱃지의 노출 값을 기존 양산 기간(M+N)에서 실제 SOP 일자(YYYY-MM-DD)로 변경하여 사용자에게 직접적인 양산 시점을 제공합니다.
- **작업 대상 파일**: [app/pages/_20_analysis/data_analysis_page.py](app/pages/_20_analysis/data_analysis_page.py)

## 2. 세부 수정 사항
[app/pages/_20_analysis/data_analysis_page.py](app/pages/_20_analysis/data_analysis_page.py#L575-L578)의 뱃지 HTML 렌더링 로직을 다음과 같이 수정하였습니다.

### 변경 전
```python
    badge_html = ""
    if prod_period_str != "-":
        badge_html = f'<span class="ncf-period-badge">{prod_period_str}</span>'
```

### 변경 후
```python
    badge_html = ""
    # * [NCF 탭 주황색 뱃지 SOP 일자 노출] M+N 양산 기간 대신 YYYY-MM-DD 형식의 SOP 시작일을 노출하도록 수정
    if sop_date_str != "-":
        badge_html = f'<span class="ncf-period-badge">{sop_date_str}</span>'
```

## 3. 검증 결과
- **정적 코드 검증**: `python tests/verify_code.py`를 실행하여 256개 파일에 대해 모두 무결성을 확인하였습니다.
  - 결과: `[PASSED] 정상 파일: 256 / 256`
- **테스트 슈트 검증**: 전체 `pytest` 테스트 슈트 166개를 전수 실행하여 모두 성공적으로 통과하였습니다.
  - 결과: `166 passed, 6 warnings in 127.85s (100% 통과)`

## 4. 특이 사항 및 우려 사항 (Concerns)
- 특이 사항 없음. 기존의 양산 기간인 `prod_period_str` 연산 로직(563~573 라인)은 다른 영역에서 활용될 가능성을 고려하여 그대로 유지하였으며, 뱃지에 대입하는 변수만 안전하게 `sop_date_str`로 변경하였습니다.
