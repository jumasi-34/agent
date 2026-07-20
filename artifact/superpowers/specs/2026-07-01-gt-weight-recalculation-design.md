---
id: gt-weight-recalculation-design
title: "[설계] G/T Weight (완제품 중량) 합격 판정 기준 변경 설계 사양서"
type: spec
status: proposed
summary: >
  DWH 원천 데이터의 G/T Weight(완제품 중량) 합격 여부 판정 기준을 기존 고정형 상하한(UPM_STD_WGT, LWM_STD_WGT)에서,
  기준 중량(STD_WGT) 대비 +/- 2.5% 비율 범위 조건으로 가변 산정하도록 SQL 판정식을 고도화하는 설계 사양서입니다.
updated: 2026-07-01
---

# G/T Weight 합격 판정 기준 변경 설계 사양서

본 문서는 IQM Plus 대시보드 화면 및 데이터 분석 화면에서 완제품 중량(G/T Weight) 지표 산정 시 적용되는 합격률 판정 기준을 기존 원천 규격 상하한에서 기준 중량 대비 가변 범위(+/- 2.5%)로 변경하기 위한 설계 사양서입니다.

---

## 1. 배경 및 필요성

- **기존 방식 (AS-IS)**: GMES 원천 DWH 테이블(`gmes_build_manufacture_report`)에서 이미 계산 및 저장되어 있는 규격 상하한값(`UPM_STD_WGT`, `LWM_STD_WGT`)을 기준으로 중량 측정값(`MRM_WGT`)의 합격 여부(`JDG`)를 판단하였습니다.
- **변경 요구사항 (TO-BE)**: 규격 마스터의 상하한 규격 대신, 실제 해당 규격의 기준 중량(`STD_WGT`) 값 대비 **+/- 2.5%** 범위 안에 중량 측정값(`MRM_WGT`)이 들어올 경우 합격(`JDG = 1`)으로 간주하도록 일괄 변경합니다.
- **아키텍처적 의사 결정 (사용자 승인 완료)**:
  - SQLite Staging DB 테이블 구조(`prd_audit_iqm_plus_monthly_agg`)의 월간 집계 데이터 스키마는 완벽하게 유지합니다. (성능 극대화 및 데이터 전송 레이턴시 최소화)
  - 대신, 원천 DWH에서 월간 데이터를 수집해 집계 캐시를 구축하는 **DWH 원천 SQL 쿼리** 내의 `JDG` 판정 수식을 수정함으로써 일관되고 안전하게 기준 변경을 달성합니다.

---

## 2. 영향 범위 및 수정 대상 파일 목록

| 번호 | 파일명 | 기능 및 역할 | 수정 사항 요약 |
| :--- | :--- | :--- | :--- |
| 1 | [app/queries/q_iqm_plus.py](app/queries/q_iqm_plus.py) | IQM+ 대시보드 집계용 데이터 수집 쿼리 어셈블러 | `get_query_gt_wt_by_unit_period` 함수 내의 SQL `JDG` 판단 수식 수정 |
| 2 | [app/queries/gmes_query.py](app/queries/gmes_query.py) | GMES 원천 상세 분석 및 실시간 쿼리 어셈블러 | `get_gmes_gt_wt_rawdata`, `get_gmes_gt_wt_by_period` 함수 내 SQL `JDG` 판단 수식 수정 |

---

## 3. 상세 수정 설계

### ① [app/queries/q_iqm_plus.py](app/queries/q_iqm_plus.py) 내 `get_query_gt_wt_by_unit_period`

- **AS-IS (Line 363)**:
  ```sql
  CASE WHEN bmr.MRM_WGT <= bmr.UPM_STD_WGT AND bmr.MRM_WGT >= bmr.LWM_STD_WGT THEN 1 ELSE 0 END AS JDG
  ```
- **TO-BE**:
  ```sql
  CASE 
      WHEN bmr.STD_WGT != 0 AND bmr.MRM_WGT >= (bmr.STD_WGT * 0.975) AND bmr.MRM_WGT <= (bmr.STD_WGT * 1.025) THEN 1 
      ELSE 0 
  END AS JDG
  ```
  *(비고: 기준값 `STD_WGT`가 0이거나 NULL일 때 0으로 안전하게 예외 처리)*

### ② [app/queries/gmes_query.py](app/queries/gmes_query.py) 내 `get_gmes_gt_wt_rawdata` 및 `get_gmes_gt_wt_by_period`

- **AS-IS (Line 2115, 2187)**:
  ```sql
  WHEN MRM_WGT <= UPM_STD_WGT AND MRM_WGT >= LWM_STD_WGT THEN 1
  ```
- **TO-BE**:
  ```sql
  CASE 
      WHEN WT.STD_WGT != 0 AND WT.MRM_WGT >= (WT.STD_WGT * 0.975) AND WT.MRM_WGT <= (WT.STD_WGT * 1.025) THEN 1 
      ELSE 0 
  END AS JDG
  ```

---

## 4. 데이터 적재 파이프라인 갱신 및 동기화 절차

수정이 이루어진 후, 기존에 SQLite Staging DB(`staging.db`)에 누적 캐싱되어 있던 기존 판단 기준의 집계 데이터를 지우고 신규 기준으로 갱신(Re-build)하기 위한 데이터 동기화 파이프라인 수동 트리거가 요구됩니다.

- **트리거 서비스 함수**: [app/service/iqm_df.py](app/service/iqm_df.py) 내 `run_iqm_aggregation`
- **적재 스크립트 실행 절차**:
  - `run_iqm_aggregation(save_db=True, target_year=YYYY, target_month=MM)`을 대상 연월(예: 2026년 6월 등)에 대해 명시적 구동함으로써 Staging DB의 집계 데이터를 변경된 비즈니스 룰 기준으로 무결하게 교체 완료합니다.

---

## 5. 검증 및 하네스 엔지니어링 계획 (Sandbox Verification)

- **테스트 격리 원칙 준수**: 실제 소스 코드를 교체하기 전, [tests/](tests/) 하위에 독립 테스트 모듈 `tests/test_gt_weight_spec.py`를 신규 생성합니다.
- **검증 항목**:
  - `q_iqm_plus.get_query_gt_wt_by_unit_period` 함수를 호출하여 생성된 SQL 문자열에 기존의 `UPM_STD_WGT` 대신 신규 기준 수식 비율 인자(`0.975`, `1.025`) 및 `STD_WGT` 가 정밀하게 포함되어 있는지 정적 분석 검증 수행.
  - `gmes_query.get_gmes_gt_wt_rawdata` 및 `get_gmes_gt_wt_by_period` 함수 결과물에 대해서도 동일한 SQL 어셈블링 무결성 정량 테스트 보장.

---

## 6. 개발 및 리팩토링 규칙 준수 확약

- **이모지 전면 금지**: 소스 코드 주석, 스트림릿 UI 화면 및 독스트링 등 어떠한 영역에서도 유니코드 이모지 사용을 엄격히 배제함.
- **한국어 독스트링**: 신규 생성하는 유닛 테스트 및 수정되는 모듈 내 주석은 가독성을 극대화하기 위해 모두 명확한 한국어(Korean)로 통일하여 작성함.
- **세션 상태 가로채기**: 만약 추후 UI 위젯 상에서 세션 연계 변경이 수반될 경우, `StreamlitAPIException`을 방지하도록 세션 가로채기(Session Interception) 패턴을 안전하게 활용함.
