#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=========================================================================
[Automation] label_graphify_communities.py (Graphify 커뮤니티 시각화 패치 도구)
=========================================================================
이 스크립트는 graphify-out/ 산하의 정적 분석 결과들을 수집하여,
기계적인 번호 기반 커뮤니티(Community XX)를 사람이 읽을 수 있는 한글 세맨틱 라벨로 변환하고,
graph.html 및 graph.json 등을 지능적으로 패치하여 대시보드 상에 실시간 반영시킵니다.
"""

import os
import re
import json
from datetime import datetime

# =========================================================================
# SECTION 1. Core Metadata Dictionary (지식 정밀 매핑 사전)
# =========================================================================

METADATA_PRESETS = {
    0: {
        "label": "SQL 조건/필터 동적 빌더",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "QueryFilter 클래스 및 날짜 SQL 가공 유틸리티가 혼재되어 있습니다."
    },
    1: {
        "label": "전역 설정 및 공통 필터 모델",
        "layer": "Business Domain",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "시스템 전역 상수 및 핵심 지표 매개변수 구조체, 주간 공통 지표 연산식이 섞여 있습니다."
    },
    2: {
        "label": "공용 Plotly 시각화 컴포넌트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "Shadcn 스타일 상속을 강제하는 표준 차트 추상체 및 컴포넌트군입니다."
    },
    3: {
        "label": "가류/컷팅 공정 품질 지수 산식",
        "layer": "Business Domain",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "타이어 가류/컷팅 핵심 공정 계산 논리가 결합되어 있습니다."
    },
    4: {
        "label": "IQM Plus 대시보드 화면 컨트롤러",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "제품 완성도 메인 대시보드 화면을 구성하며, 모달과 탭 라우팅을 총괄합니다."
    },
    5: {
        "label": "중앙 예외 제어 및 로깅 인프라",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "SQLiteDML을 활용한 안전 로깅 및 데코레이터 기반 에러 핸들러 영역입니다."
    },
    6: {
        "label": "디자인 시스템 CSS 테마 로더",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "공통 CSS 주입 및 Plotly 범례/축 스타일 셋업을 처리합니다."
    },
    7: {
        "label": "차트 컴포넌트 추상 프레임워크",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "기저 시각화 클래스 BaseChartComponent와 자식 컴포넌트가 묶여 있습니다."
    },
    8: {
        "label": "시각화 공통 툴팁 및 너비 유틸",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "한글-영문 가중 문자 너비 및 hover 템플릿 생성 헬퍼 함수입니다."
    },
    9: {
        "label": "멀티 DB 연결 팩토리 및 바인딩",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "get_client() 허브 기반의 다중 DB principal 검증 및 세션 관리를 보장합니다."
    },
    10: {
        "label": "대시보드 그리드 및 공통 헤더 패널",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "화면 전체의 반응형 HTML 컬럼 그리드와 타이틀 바를 구성합니다."
    },
    11: {
        "label": "로컬 품질 관리 DB 영속화 유틸",
        "layer": "DB / Infrastructure",
        "confidence": "Medium",
        "risk": "High",
        "split_candidate": True,
        "reason": "SQLite 로컬 파일 제어 및 수동 업로드 CSV 가공 DML 세트입니다."
    },
    12: {
        "label": "데이터 분석 유저 입력 컨트롤러",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "사이드바 필터 수집 및 세션 초기화 intercept 흐름을 지탱합니다."
    },
    13: {
        "label": "차트 범례 정렬 및 레이아웃 스타일",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "시각화 축선, 여백, 범례 엘리먼트 고정 사양 파일입니다."
    },
    14: {
        "label": "품질 지표 및 날짜 필터 매개변수",
        "layer": "Business Domain",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "HGWS PPM 계산 등의 기준이 되는 도메인 데이터 매개변수 클래스입니다."
    },
    15: {
        "label": "배치 자동화 로거 및 수동 집계 허브",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "AutomationLogger 인프라와 수동 배치 구동 Streamlit 화면이 섞여 있습니다."
    },
    16: {
        "label": "AST 기반 3계층 레이어 검증 분석기",
        "layer": "Test",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "소스 구문 파싱을 통해 계층 위반 임포트를 정적 단언하는 테스트 지원 유틸입니다."
    },
    17: {
        "label": "미확정: [크론탭 자동화 설정 가이드]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "크론 스케줄 및 알림 구성 문서가 수집된 영역입니다."
    },
    18: {
        "label": "물리 테이블 설정 메타 동적 사전",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": True,
        "reason": "JSON 설정을 기반으로 물리 테이블명과 필드 정보를 클래스에 바인딩합니다."
    },
    19: {
        "label": "CTMS 정밀 측정 전처리 및 쿼리",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "CTMS 실측치 조회 SQL과 판다스 가공 로직이 물리 혼재된 서비스입니다."
    },
    20: {
        "label": "HOPE OE 및 셀인 수집 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "공급량 데이터 정적 캐시 조인 및 SQL 빌딩을 결합 처리합니다."
    },
    21: {
        "label": "원형 게이지 차트 및 비주얼 테마 패치",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "품질 완성도 표출용 도넛/게이지 차트 및 커스텀 스타일 인젝터입니다."
    },
    22: {
        "label": "시계열 갭 연산 및 ECharts 변환 패치",
        "layer": "Mixed / Needs Review",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "ECharts 패치와 갭 계산이 혼재되어 있습니다."
    },
    23: {
        "label": "동적 누적 품질지수 연산 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "PPM 및 합격률 정규화 공식을 판다스로 계산하는 핵심 로직입니다."
    },
    24: {
        "label": "IBM Carbon 팔레트 및 배치 분석 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "글로벌 테마 컬러 상수 및 실행 소요 시간 분포 차트입니다."
    },
    25: {
        "label": "미확정: [달력 대시보드 기획 명세서]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "Streamlit 달력 구성안 기획 마크다운 문서들입니다."
    },
    26: {
        "label": "세션 보안 및 네비게이션 권한 통제",
        "layer": "Runtime App",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "로그인 타임아웃 감지 및 유저 역할별 메뉴 렌더링 관문입니다."
    },
    27: {
        "label": "생산 이슈 테이블 조건부 서식 설정",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "메타데이터 기반 st.column_config 조립 및 테이블 조건부 채색 유틸입니다."
    },
    28: {
        "label": "전역 폰트 및 시맨틱 디자인 컬러 토큰",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "디자인 시스템의 근간이 되는 전역 폰트패밀리 및 컬러 상수 클래스입니다."
    },
    29: {
        "label": "불릿 게이지 성과 지표 컴포넌트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "타겟 실적 성과를 불릿 형태로 표출하는 고성능 시각화 모듈입니다."
    },
    30: {
        "label": "SQLite DDL 스키마 및 자동 인덱스 제어",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Staging DB 스키마 생성 및 초기 테스트 환경 셋업 DDL을 관장합니다."
    },
    31: {
        "label": "Lot Tracking 생산 이력 화면",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "그린/가류 타이어 이력 수집 및 메트릭 요약을 뿌려주는 컨트롤러입니다."
    },
    32: {
        "label": "메타데이터 직렬화 정밀 검증 스위트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "메타데이터 사전 JSON 규격과 DLP 방지 논리를 검증하는 유닛 테스트입니다."
    },
    33: {
        "label": "Plotly 축 스타일 및 여백 프리셋",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": True,
        "reason": "시각화 플롯 공용 레이아웃 및 Trace 구성 요소를 제공합니다."
    },
    34: {
        "label": "물리 데이터베이스 커넥션 클라이언트",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Databricks 및 Oracle 물리 드라이버 호출 및 판다스 연동을 처리합니다."
    },
    35: {
        "label": "글로벌 Plotly light_theme 테마 팩토리",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "디자인 시스템 테마를 Plotly pio에 자동 전역 주입하는 모듈입니다."
    },
    36: {
        "label": "미확정: [품질 관리 DB 매핑 문서]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "테이블 마스터 구조 분석 및 명세서 마크다운입니다."
    },
    37: {
        "label": "미확정: [쿼리 함수 인터페이스 사양서]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "SQL 빌더 연동 규격을 정리해둔 기획 마크다운입니다."
    },
    38: {
        "label": "메타데이터 동적 병합 서비스 엔진",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "JSON 스키마와 물리 데이터베이스 테이블의 동적 Outer Join 병합을 총괄합니다."
    },
    39: {
        "label": "PLM 제품 규격 리비전 비교 대시보드",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "규격 변동 전후 이력 분석 테이블과 탭 레이아웃을 렌더링합니다."
    },
    40: {
        "label": "SQL WHERE 조건절 가드 조립 유틸",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "인젝션 방지 및 날짜 가드를 갖춘 동적 다중 결합 SQL 완성 유틸리티입니다."
    },
    41: {
        "label": "CQMS 품질 이슈 전처리 및 피벗",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "고객 불량 이슈 원천 데이터를 가공하여 일별 피벗 데이터셋을 준비합니다."
    },
    42: {
        "label": "원천 품질 측정 분포 시각화 플롯",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "정밀 측정이력 분포를 비교하는 공용 플롯 생성기입니다."
    },
    43: {
        "label": "SQLite 누적 캐시 자가 치유 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Staging DB에 과거월 캐시가 결측되었을 경우 실시간 동적 대칭 조인을 태워 자동 자가 보정합니다."
    },
    44: {
        "label": "주간 품질이슈/4M 변경 모니터링 히트맵",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "주간 일정 및 4M 변동 사건 현황을 그리드 형태의 Plotly 히트맵으로 렌더링합니다."
    },
    45: {
        "label": "MES 제품 품질 데이터 원천 쿼리",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "타이어 중량/런아웃 등 실시간 제조 계측 데이터를 수집하는 SQL을 빌딩합니다."
    },
    46: {
        "label": "Worst 규격 부적합 분석 대시보드",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "공장 Worst 규격의 스크랩/리워크 발생 비율 및 TOP3 메트릭 카드 메인 화면입니다."
    },
    47: {
        "label": "PLM 마스터 규격 수집 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "PLM 원천 규격 이력을 Databricks에서 가져와 전처리하는 모듈입니다."
    },
    48: {
        "label": "공정 요인별 트렌드 및 수명 주기 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "가류/성형 공정 인자별 상관관계 및 양산 그룹별 합격률 시계열 플롯입니다."
    },
    49: {
        "label": "KMC 반품 및 흡음재 부착 수집 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "KMC 원천 반품 데이터 및 타이어 바코드 매핑 처리를 수행합니다."
    },
    50: {
        "label": "미확정: [품질 완성도 지수 산출 기획서]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "PPM 및 품질 합격률 점수 표준 변환 수식이 명시된 마크다운 기획서입니다."
    },
    51: {
        "label": "글로벌 정규식 필터 무결성 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "공통 입력 폼 필터의 유효성 검사 성능을 보장하는 정적 유닛 테스트입니다."
    },
    52: {
        "label": "스크랩/NCF 분석 상세 탭 화면",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Worst 규격의 다차원 상세 분석 탭 레이아웃 및 가류 시간 플롯 렌더러입니다."
    },
    53: {
        "label": "Cpk 편측/양측 통계 가동 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "공정 능력 지수 Cp, Cpk 및 월말 일자 연산 튜플을 반환하는 통계 서비스입니다."
    },
    54: {
        "label": "달력 이벤트 동적 생성 빌더",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "4M 변동 및 고객 감사, 품질이슈 일정을 JSON FullCalendar 이벤트 객체로 가공합니다."
    },
    55: {
        "label": "Release Ops 통합 게이트 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "수정 영향도 트리아지 및 배포 예외 면제 정책의 문법 정합성을 단언하는 테스트입니다."
    },
    56: {
        "label": "미확정: [CQMS 고객 품질 이슈 기획서]",
        "layer": "Doc / PRD / Spec",
        "confidence": "Low",
        "risk": "Low",
        "split_candidate": True,
        "reason": "MTTC 처리 단계 및 산출 메커니즘을 상세히 명시한 기획 마크다운입니다."
    },
    57: {
        "label": "대시보드 공통 플롯 무오작동 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "통합 모니터링 화면 내의 Plotly 생성 함수들의 예외 차단을 증명하는 테스트입니다."
    },
    58: {
        "label": "품질 요인별 PPM 분포 플롯 및 테스트",
        "layer": "Mixed / Needs Review",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "PremiumPpmByFactorPlot 시각화 모듈과 해당 유닛 테스트가 혼재되어 있습니다."
    },
    59: {
        "label": "업무일 기준 실적 처리 지연 연산 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "공휴일 및 연차를 연계하여 MTTC 처리 단계별 실질 가중 일수를 연산해 줍니다."
    },
    60: {
        "label": "Staging 캐시 월별 누적 병합 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "1월/2월 실물 데이터를 SQLite Staging에 적재하여 누계 병합 연산을 실증하는 테스트입니다."
    },
    61: {
        "label": "DWH 실적 월 단위 SQLite 적재 서비스",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Databricks 원천 데이터를 수집하여 로컬 Staging DB에 캐싱 이식하는 파이프라인입니다."
    },
    62: {
        "label": "제품 규격 수집 파이프라인 Golden Test",
        "layer": "Mixed / Needs Review",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "수집 전처리 로직 및 Golden Test 검증 스위트가 한 커뮤니티로 통합 수집되어 있습니다."
    },
    63: {
        "label": "정적 스캐너 테이블 참조 유효성 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "코드베이스의 SQL 조립부에서 메타데이터 명세를 위반해 하드코딩된 참조를 색출하는 테스트입니다."
    },
    64: {
        "label": "NCF 기반 공장Worst 부적합 분석기",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "NonconformityParams 모델을 화면 UI 필터와 연계하여 최상단 글로벌 부적합 분석을 트리거합니다."
    },
    69: {
        "label": "실행 기록 분석기 정밀 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "에이전트 실행로그 파싱 및 합격률 KPI 요약 로직의 정상 작동을 단언하는 테스트입니다."
    },
    70: {
        "label": "자가 치유 역동기화 시스템 단위 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "Pandas KeyError 복구 및 중앙 에방대책체크리스트 동적 갱신을 정밀 단언하는 테스트입니다."
    },
    71: {
        "label": "HTML 태그 정제 유틸리티 및 테스트",
        "layer": "Mixed / Needs Review",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": True,
        "reason": "HTML 태그를 걷어내는 유틸과 해당 단위 테스트 코드가 섞여 있습니다."
    },
    72: {
        "label": "감사 마스터 DDL 및 CSV 배치 유틸",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "제품 감사 마스터 테이블 스키마 생성 및 초기 CSV 일괄 주입을 자동 수행하는 스크립트입니다."
    },
    74: {
        "label": "마크다운 경로 및 링크 린트 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "문서 자산 내의 데드링크, 이중대괄호 비표준 링크, 절대경로 사용을 린팅하는 품질 게이트 테스트입니다."
    },
    75: {
        "label": "CSS Injector 및 공통 카드 컴포넌트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "디자인 시스템 테마를 주입하고 일관된 컨테이너 프레임 및 헤더 패널을 동적 렌더링합니다."
    },
    76: {
        "label": "Oracle SQL DECODE 동적 컴파일 유틸",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "딕셔너리를 Oracle DECODE 구문으로 매핑 가공해 주는 순수 SQL 가공 유틸리티입니다."
    },
    77: {
        "label": "글로벌 OE 품질 이슈 분석 모달 뷰어",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "글로벌 품질 추이, 이슈 도넛 차트 및 상세 로우데이터를 모달 창에 뿌려주는 프레젠테이션 영역입니다."
    },
    82: {
        "label": "라이트/다크 대응 UI 스타일 패치",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "Material Icon 연동 헤더 및 시스템 테마 대응 스코어박스 렌더링 보조 유틸입니다."
    },
    83: {
        "label": "이중대괄호 비표준 링크 식별 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "마크다운 문서 내의 비표준 더블백틱이나 비정상 물리 파일 누수를 걸러내는 통합 테스트입니다."
    },
    84: {
        "label": "공장 제품 사양 전처리 Golden Test",
        "layer": "Mixed / Needs Review",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "GMESSpecMasterParams 모델과 공장 제품 사양 전처리 검색 논리, Golden Test가 혼재되어 있습니다."
    },
    85: {
        "label": "IQM 월간 품질 리포트 메인 대시보드",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "단일 스크롤 레이아웃의 월간 리포트 화면 및 Shadcn UI 스타일 고밀도 KPI 카드를 그리는 컨트롤러입니다."
    },
    86: {
        "label": "품질지수 도넛 시각화 및 서머리 렌더러",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "품질지수 총괄 도넛 차트 및 규격 완성도 요약 테이블 렌더링 세션입니다."
    },
    89: {
        "label": "OneDrive 동기화 자동화 및 pre-push 훅",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "rsync 자동화 스크립트, git 훅, Makefile 및 동기화 기획서가 한데 엮여 있습니다."
    },
    90: {
        "label": "월간 리포트 서비스/쿼리 단위 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "하이브리드 데이터 폴백 시나리오, 요약 메트릭 계산 수식을 정밀 입증하는 테스트 스위트입니다."
    },
    91: {
        "label": "테스트 이메일 HTML 포맷팅 발송 엔진",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "Pandas df를 이메일 전송용 인라인 CSS HTML 테이블로 가공하고 Plotly를 Base64로 이메일에 동봉 발송합니다."
    },
    92: {
        "label": "PPM 비교 및 리턴사유 도넛 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "자재코드별 PPM 비교 수평 바 차트 및 원인 비중 분석 도넛 차트 드로어 세트입니다."
    },
    97: {
        "label": "에이전트 실행 기록 옵저버 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "7대 아티팩트(plan.md, diff.patch 등)의 물리 수집 훅 정상 동작을 검증하는 테스트입니다."
    },
    98: {
        "label": "Plotly 통합 라이트/다크 테마 템플릿",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "전체 플롯에 일관적 디자인을 덧입히는 light_theme, dark_theme 템플릿 클래스 패키지입니다."
    },
    99: {
        "label": "Lot Tracking 세부 트렌드 그리드",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Lot별 측정 편차 상세 데이터프레임과 선택 탭 뷰어의 구성 요소입니다."
    },
    100: {
        "label": "엑셀 기반 OE 문서 카탈로그 뷰어",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "Excel 마스터 규격을 읽어와 Material Icon과 매칭해 카탈로그로 렌더링하는 뷰어 화면입니다."
    },
    101: {
        "label": "엑셀 데이터 DB 업로드 관리 유닛",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "사용자 엑셀 업로드 자산의 파싱 및 SQLite 영속 적재를 수행하는 UI 컴포넌트입니다."
    },
    104: {
        "label": "아웃라이어 동적 정제 및 UF 히스토그램",
        "layer": "Service / Preprocessing",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "IQR/Z-score 기반 품질 계측 데이터 아웃라이어를 동적 정제하고 히스토그램 플롯을 생성합니다."
    },
    105: {
        "label": "설비별 PPM 히트맵 및 누적 히스토그램",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "설비*근무조 매핑 PPM 히트맵과 마일리지별 품질 리턴 누적 히스토그램 플롯입니다."
    },
    106: {
        "label": "글로벌 Factory Management 모니터링 화면",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "전 세계 공장별 FM 부적합 수준과 상세 공장 탭을 뿌리는 메인 화면 컨트롤러입니다."
    },
    107: {
        "label": "구간별 품질 지표 연산기 및 리그레션 테스트",
        "layer": "Mixed / Needs Review",
        "confidence": "Medium",
        "risk": "Medium",
        "split_candidate": True,
        "reason": "90D/365D 비누적 구간 차감 산식 로직과 회귀 검사 하네스 코드가 결합되어 있습니다."
    },
    111: {
        "label": "CQMS 품질이슈 전처리 파이프라인 Golden Test",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "가짜 DB 모킹 컨텍스트를 활용해 수집 변환 파이프라인의 타입 무결을 실증하는 테스트입니다."
    },
    112: {
        "label": "CQMS 통합 모니터링 서비스 단위 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "CQMS 달력 및 4M 데이터프레임 가공 서비스의 리턴 유효성을 보장하는 테스트입니다."
    },
    113: {
        "label": "품질 규격 추세 분석 어드민 대시보드 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "KeyError 및 ZeroDivision 발생 유무를 최종 핫리로드 검증하는 어드민 대시보드 테스트입니다."
    },
    114: {
        "label": "GMES 부적합 및 흡음재 제조 이력 쿼리 빌더",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "V-Spec 부적합 데이터 및 타이어 제조 바코드 이력을 Databricks에서 긁어오는 ANSI SQL을 컴파일합니다."
    },
    116: {
        "label": "HOPE SELLIN 데이터 변환 자동화 스크립트",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Oracle 원천 공급량을 긁어와 로컬 SQLite Staging 캐시로 집계 적재하는 독립 구동 스크립트입니다."
    },
    122: {
        "label": "양산 vs 개발 합격률 시계열 비교 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "Mass status별 합격율 추이 라인 차트 및 그룹 비교 바 플롯 드로어입니다."
    },
    123: {
        "label": "리워크/균일성 분석 상세 탭 화면 UI",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "설비별 균일성 Pie 차트 및 리워크 발생 원인 분석 원천 데이터를 표출하는 컨트롤러입니다."
    },
    133: {
        "label": "PR 변경 변경 이력 메타 무결성 린터",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "풀리퀘스트 설명란의 AI 하네스 키워드 누락 및 위험 지표 검출 유효성 검사 스크립트입니다."
    },
    134: {
        "label": "시스템 로그 접속 이력 정렬 정밀 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "로그 테이블 조회 시 접속 시간 내림차순 정렬 및 특정 불필요 세션 배제 논리 보증 테스트입니다."
    },
    135: {
        "label": "골든 태스크 매니페스트 추적 검증 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "품질 관리 게이트에 필요한 core domains 추적 지표 일치성을 확인하는 정적 테스트입니다."
    },
    136: {
        "label": "과거 캐시 결측 실시간 자가 치유 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "인메모리 상에서 결측 시그널을 주입해 실시간 자가 치유 동적 보정이 가동되는지 단언하는 테스트입니다."
    },
    137: {
        "label": "부적합(SCRAP) 점유 지분 도넛 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "설비/공정/항목별 품질 부적합 발생 지분을 명확히 투사하는 프리미엄 도넛 차트 컴포넌트입니다."
    },
    138: {
        "label": "품질 불량 누적 파레토 차트 컴포넌트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "불량 원인별 점유율과 80% Cutoff 관리 대시 가이드라인을 그리는 차트 컴포넌트입니다."
    },
    139: {
        "label": "Scrap 코드 공정 관리도 프리미엄 p-Chart",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "DFT CD별 불량률 공정 관리 상태를 계측해 UCL/LCL 한계 및 아웃라이어를 감지하는 차트입니다."
    },
    140: {
        "label": "생산량/불량수량/PPM 시계열 통합 추이 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "생산량과 부적합 수량, PPM 추이를 단일 이중 축(Dual-Axis)에 결합하는 프리미엄 복합 플롯입니다."
    },
    141: {
        "label": "HOPE OE App 임시 원시 데이터 쿼리 생성기",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "Databricks 원천 마스터 테이블에서 정규 개발 대상 mcode 목록을 긁어오는 SQL을 가공합니다."
    },
    156: {
        "label": "브랜치 보호 규칙 강제화 자동화 스크립트",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "GitHub REST API를 직접 호출해 메인 브랜치 머지 가드 및 상태 승인을 자동 규제하는 도구입니다."
    },
    157: {
        "label": "Oracle 인스턴스 전용 환경 셋업 쉘 스크립트",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "TNS_ADMIN, LD_LIBRARY_PATH 등 Oracle Client 통신에 필수적인 환경 변수를 세팅해 줍니다."
    },
    158: {
        "label": "대시보드 메인 컨트롤러 기동 스모크 테스트",
        "layer": "Test",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "iqm_analysis_page.py를 Import할 때 KeyError 및 의존성 오류로 뻗지 않고 정상 로딩되는지 보증합니다."
    },
    159: {
        "label": "UniformityParams 기반 원천 측정 전처리",
        "layer": "Business Domain",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "타이어 균일성 측정 데이터프레임의 정형화 전처리를 수행하는 도메인 모듈입니다."
    },
    160: {
        "label": "4대 지수별 전월 누적 vs 당월 수평 막대 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "4대 지수 실적(PPM, Pass Rate 등)의 누적 평균과 당월 실적을 직관적으로 1대1 수평 대비합니다."
    },
    161: {
        "label": "Databricks 세션 소유 권한 정보 수집기",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "현재 Databricks 유저의 테이블 카탈로그 조회 권한 등 메타 정보를 수집해 줍니다."
    },
    162: {
        "label": "SQLite Staging DB 월별 캐시 테이블 초기화",
        "layer": "DB / Infrastructure",
        "confidence": "High",
        "risk": "High",
        "split_candidate": False,
        "reason": "SQLite Staging DB에 신규 월보 정적 테이블 DDL을 무중단 생성하고 보장하는 유닛입니다."
    },
    169: {
        "label": "데이터클래스 입력 위젯 동적 빌더 유틸",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "매개변수 데이터클래스 정보를 수입해 Streamlit의 적절한 다중 필터 위젯으로 자동 치환해 줍니다."
    },
    170: {
        "label": "디자인 시스템 공용 차트 초기화 기저 클래스",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "차트 렌더링에 필요한 파라미터 유효성을 사전 조율하는 공통 기저 유닛입니다."
    },
    171: {
        "label": "SQL 쿼리 조립 런타임 추적 데코레이터",
        "layer": "Query / SQL Builder",
        "confidence": "High",
        "risk": "Medium",
        "split_candidate": False,
        "reason": "쿼리 조립 시작/완료 시점의 로깅 및 빌드된 SQL 문자 수를 트래킹해 주는 데코레이터입니다."
    },
    172: {
        "label": "진행중 4M 변경 공장별 파이 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "진행 상태인 공장별 4M 변경 건수 비중을 공용 Pie 컴포넌트를 이식해 렌더링합니다."
    },
    173: {
        "label": "진행중 품질 이슈 공장별 파이 차트",
        "layer": "Design System / Chart",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "진행 중인 불량 품질이슈 공장별 발생 점유율을 공용 Pie 컴포넌트로 표출합니다."
    },
    174: {
        "label": "마크다운 단계별 GIF 애니메이션 렌더러",
        "layer": "UI / Streamlit Page",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "가이드 마크다운 본문에 화질 저하 없는 설명형 GIF 및 스텝 표출 HTML 컴포넌트를 뿌려줍니다."
    },
    177: {
        "label": "SKILL.md 최상단 상대경로 환산 빌더",
        "layer": "Automation / Ops",
        "confidence": "High",
        "risk": "Low",
        "split_candidate": False,
        "reason": "중첩 마크다운 경로에서 root custom skills의 SKILL.md 파일까지 상대경로 평문을 실시간 빌드해 줍니다."
    }
}

# =========================================================================
# SECTION 2. Automation Helper Class
# =========================================================================

class GraphifyCommunityLabeller:
    def __init__(self, root_dir="."):
        self.root_dir = os.path.abspath(root_dir)
        self.graphify_out = os.path.join(self.root_dir, ".agent-storage", "graphify-out")
        self.report_path = os.path.join(self.graphify_out, "GRAPH_REPORT.md")
        self.graph_json_path = os.path.join(self.graphify_out, "graph.json")
        self.graph_html_path = os.path.join(self.graphify_out, "graph.html")
        self.graph_labeled_html_path = os.path.join(self.graphify_out, "graph_labeled.html")
        self.labels_path = os.path.join(self.graphify_out, "community_labels.json")
        self.override_path = os.path.join(self.graphify_out, ".graphify-community-labels.json")

    def run(self):
        print("[*] Starting Graphify Labeled Patch Automation Flow...")
        
        # 1. GRAPH_REPORT.md 및 graph.json 기반 수집
        raw_communities = self.parse_report_and_json()
        
        # 2. 수동 오버라이드 병합
        overrides = self.load_manual_overrides()
        
        # 3. 통합 매핑 데이터 구축
        final_mapping = self.build_final_labels(raw_communities, overrides)
        
        # 4. community_labels.json 영속화
        self.save_labels_json(final_mapping)
        
        # 5. HTML 시각화 및 범례 패치 단행
        self.patch_graph_html(final_mapping)
        
        print("[+] Graphify Labeled Patch Automation Flow completed successfully!")

    def parse_report_and_json(self):
        """GRAPH_REPORT.md에서 커뮤니티 기본 정보를 파싱하고, graph.json에서 코어 노드 목록을 상호 매핑합니다."""
        print("[*] Step 1: Parsing GRAPH_REPORT.md and graph.json...")
        communities = {}
        
        # graph.json에서 각 커뮤니티별 실제 수집된 node list를 추출
        node_map = {}
        if os.path.exists(self.graph_json_path):
            try:
                with open(self.graph_json_path, "r", encoding="utf-8") as f:
                    gdata = json.load(f)
                    for node in gdata.get("nodes", []):
                        cid = node.get("community")
                        if cid is not None:
                            label = node.get("label", "")
                            # 괄호나 리터럴, 파일명 정제
                            if label:
                                node_map.setdefault(cid, []).append(label)
            except Exception as e:
                print(f"[!] Warning while parsing graph.json: {e}")

        # GRAPH_REPORT.md 파싱
        if os.path.exists(self.report_path):
            with open(self.report_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # '### Community {ID}' 패턴 스캔
            sections = content.split("### Community ")
            for section in sections[1:]:
                lines = section.strip().split("\n")
                if not lines:
                    continue
                header_line = lines[0]
                # ID 파싱 (예: "0 - \"Community 0\"")
                match_id = re.match(r"^(\d+)", header_line)
                if not match_id:
                    continue
                cid = int(match_id.group(1))
                
                # cohesion, nodes 파싱
                cohesion = 0.0
                node_count = 0
                core_snippet_nodes = []
                
                for line in lines[1:]:
                    if line.startswith("Cohesion:"):
                        try:
                            cohesion = float(line.split("Cohesion:")[1].strip())
                        except:
                            pass
                    elif line.startswith("Nodes ("):
                        # Nodes (14): ...
                        match_nodes = re.search(r"Nodes \((\d+)\): (.*)", line)
                        if match_nodes:
                            node_count = int(match_nodes.group(1))
                            snippet = match_nodes.group(2)
                            # 모킹/설명 구문 정제하고 3~7개 추출
                            parts = [p.strip() for p in re.split(r",\s*(?![^(]*\))", snippet)]
                            core_snippet_nodes = [p for p in parts if p][:6]

                # graph.json의 고정 노드 정보가 있으면 덮어씌움
                actual_nodes = node_map.get(cid, core_snippet_nodes)
                
                communities[cid] = {
                    "cid": cid,
                    "cohesion": cohesion,
                    "node_count": node_count if node_count > 0 else len(actual_nodes),
                    "core_nodes": actual_nodes[:10]  # 최대 10개만 보존
                }
        else:
            print("[!] Warning: GRAPH_REPORT.md not found. Generating default mappings from graph.json nodes.")
            # graph.json의 node_map 기반으로 복구
            for cid, nodes in node_map.items():
                communities[cid] = {
                    "cid": cid,
                    "cohesion": 0.33, # fallback default
                    "node_count": len(nodes),
                    "core_nodes": nodes[:10]
                }
                
        return communities

    def load_manual_overrides(self):
        """루트의 .graphify-community-labels.json이 있으면 읽어들여 적용합니다."""
        if os.path.exists(self.override_path):
            print(f"[*] Step 2: Found manual override file: {self.override_path}")
            try:
                with open(self.override_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # "0": "한글 라벨" 형태를 정수로 변환하여 반환
                    return {int(k): str(v) for k, v in data.items() if str(k).isdigit()}
            except Exception as e:
                print(f"[!] Error reading override file: {e}")
        return {}

    def build_final_labels(self, parsed_communities, overrides):
        """기본 사전 프리셋, 파싱된 런타임 데이터, 사용자 수동 오버라이드를 지능적으로 병합합니다."""
        print("[*] Step 3: Resolving semantic labels and layer mapping...")
        final_mapping = {}
        
        # 0번부터 현재 수집된 커뮤니티 전량을 매핑 루프
        all_ids = set(parsed_communities.keys()) | set(METADATA_PRESETS.keys()) | set(overrides.keys())
        
        for cid in sorted(all_ids):
            # 1. 프리셋에서 기초 데이터 확보
            preset = METADATA_PRESETS.get(cid, {})
            parsed = parsed_communities.get(cid, {
                "cid": cid,
                "cohesion": 0.33,
                "node_count": 0,
                "core_nodes": []
            })
            
            # 2. 라벨 결정 위계: 수동 오버라이드 > 프리셋 명시 라벨 > 미확정 디폴트 라벨
            label = "Unknown Area"
            layer = "Unknown"
            confidence = "Low"
            risk = "Low"
            split_candidate = False
            reason = "정밀 분석 대기 중인 독립 군집 영역입니다."
            
            if preset:
                label = preset["label"]
                layer = preset["layer"]
                confidence = preset["confidence"]
                risk = preset["risk"]
                split_candidate = preset["split_candidate"]
                reason = preset["reason"]
            else:
                # 기획/명세 문서인지, 테스트 코드인지, 런타임 코드인지 코어 노드를 단서로 지능적 추정
                core_nodes = [str(n).lower() for n in parsed["core_nodes"]]
                is_doc = any(".md" in n or "prd" in n or "spec" in n or "개요" in n or "1." in n for n in core_nodes)
                is_test = any("test" in n or "mock" in n or "harness" in n for n in core_nodes)
                is_ops = any(".sh" in n or "script" in n or "sync" in n or "deploy" in n for n in core_nodes)
                
                if is_doc:
                    label = f"미확정: [기획 및 아카이브 명세서]"
                    layer = "Doc / PRD / Spec"
                    reason = "마크다운 기반 기획서 및 계획서 노드가 뭉쳐진 영역으로 추정됩니다."
                elif is_test:
                    label = f"미확정: [유닛/통합 검증 테스트]"
                    layer = "Test"
                    reason = "tests/ 하위의 모킹 콘텍스트 및 무결성 단언 테스트 스위트 영역으로 추정됩니다."
                elif is_ops:
                    label = f"미확정: [자동화 스크립트 및 훅]"
                    layer = "Automation / Ops"
                    reason = "배치 및 외부 동기화 스크립트 노드 영역으로 추정됩니다."
                else:
                    label = f"미확정: [개별 독립 서비스 모듈]"
                    layer = "Mixed / Needs Review"
                    reason = "분석이 수립되지 않은 세부 비즈니스 로직 영역으로 추정됩니다."

            # Cohesion 및 Nodes 기반으로 Split_candidate 동적 보정
            # Cohesion < 0.08 이고 Nodes >= 25 이면 자동 Split 후보 지정
            if parsed["cohesion"] < 0.08 and parsed["node_count"] >= 25:
                split_candidate = True
                reason += " (Cohesion 및 노드 규모 기준 분해 후보 지정)"

            # 오버라이드가 있으면 최종 덮어씌움
            if cid in overrides:
                label = overrides[cid]
                confidence = "High"
                reason = "사용자 수동 오버라이드로 강제 주입된 라벨입니다."

            final_mapping[cid] = {
                "label": label,
                "original": f"Community {cid}",
                "layer": layer,
                "confidence": confidence,
                "risk": risk,
                "split_candidate": split_candidate,
                "cohesion": parsed["cohesion"],
                "node_count": parsed["node_count"],
                "core_nodes": parsed["core_nodes"],
                "reason": reason
            }
            
        return final_mapping

    def save_labels_json(self, final_mapping):
        """community_labels.json 영속화"""
        print(f"[*] Step 4: Writing community_labels.json to {self.labels_path}...")
        
        # JSON 키 호환성을 위해 문자열 키로 직렬화 구조화
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "source": "GRAPH_REPORT.md + graph.json",
            "labels": {str(k): v for k, v in final_mapping.items()}
        }
        
        with open(self.labels_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    def patch_graph_html(self, final_mapping):
        """graph.html을 정교하게 패치하여 graph_labeled.html로 신규 저장합니다.
        안전성을 보장하기 위해 graph.html도 원본 백업이 존재하므로 직접 업데이트해 주어,
        사용자가 어떤 방식으로 열어도 한글 라벨이 노출되도록 보증합니다."""
        
        if not os.path.exists(self.graph_html_path):
            print("[!] Error: original graph.html not found. Cannot apply patch.")
            return

        print(f"[*] Step 5: Patching graph.html and generating graph_labeled.html...")
        with open(self.graph_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 1. RAW_NODES 내의 "community_name": "Community XX"를 "community_name": "한글라벨 (Community XX)"로 치환
        # 정규식을 활용해 JSON 구문을 해체하지 않고 노드 텍스트 자체를 지능적으로 스트리밍 치환합니다.
        def replace_node_community_name(match):
            cid = int(match.group(1))
            preset = final_mapping.get(cid)
            if preset:
                semantic_label = f"{preset['label']} (Community {cid})"
                return f'"community_name": "{semantic_label}"'
            return match.group(0)

        patched_html = re.sub(
            r'"community_name":\s*"Community\s+(\d+)"',
            replace_node_community_name,
            html_content
        )

        # 2. LEGEND 상수 내부의 "label": "Community XX"를 "label": "한글라벨 (Community XX)"로 치환
        def replace_legend_label(match):
            cid = int(match.group(1))
            preset = final_mapping.get(cid)
            if preset:
                semantic_label = f"{preset['label']} (Community {cid})"
                return f'"label": "{semantic_label}"'
            return match.group(0)

        # "label": "Community 0" 패턴 치환
        # LEGEND 내부의 개별 "label"을 안전하게 바꾸기 위해 전후 맥락을 결합합니다.
        patched_html = re.sub(
            r'"label":\s*"Community\s+(\d+)"',
            replace_legend_label,
            patched_html
        )

        # 3. HTML 렌더링 내 타이틀 패널에 상위 계층(Layer) 및 위험도 메타데이터 추가 노출하는 JS 패치 주입
        # vis-network selectNode 이벤트 발생 시 meta 정보를 Sidebar panel 에 예쁘게 수치화하도록 인젝션
        # 렌더링 로직의 hook을 찾기 위해 'network.on("selectNode"' 혹은 info-content 가공 부분을 공략
        js_injection = """
        // Injecting Semantic Meta Panel Extender
        network.on("selectNode", function(params) {
            const nodeId = params.nodes[0];
            const node = RAW_NODES.find(n => n.id === nodeId);
            if (node) {
                // community_labels.json 구조체에서 메타 검색 기동
                fetch('community_labels.json')
                .then(r => r.json())
                .then(data => {
                    const cidStr = String(node.community);
                    const meta = data.labels[cidStr];
                    if (meta) {
                        const origContent = document.getElementById('info-content').innerHTML;
                        const extContent = origContent + `
                        <div class="field" style="margin-top:10px; border-top:1px dashed #4a4a7a; padding-top:8px;">
                            <b>Layer:</b> <span style="color:#EDC948">${meta.layer}</span>
                        </div>
                        <div class="field">
                            <b>Risk:</b> <span style="color:${meta.risk === 'High' ? '#FF5733' : '#aaccff'}">${meta.risk}</span>
                        </div>
                        <div class="field">
                            <b>Confidence:</b> <span>${meta.confidence}</span>
                        </div>
                        <div class="field" style="font-size:11px; color:#aaa; font-style:italic;">
                            <b>Reason:</b> ${meta.reason}
                        </div>`;
                        document.getElementById('info-content').innerHTML = extContent;
                    }
                }).catch(err => console.log('Metadata load bypassed:', err));
            }
        });
        """
        
        # updateSelectAllState 선언부 바로 다음에 JS 인젝션 배치
        if "updateSelectAllState()" in patched_html:
            patched_html = patched_html.replace(
                "updateSelectAllState();",
                "updateSelectAllState();\n" + js_injection
            )

        # 4. patched html 영속 파일로 분배 및 안전 저장
        with open(self.graph_labeled_html_path, "w", encoding="utf-8") as f:
            f.write(patched_html)
        print(f"[+] Labeled graph html successfully saved: {self.graph_labeled_html_path}")

        # graph.html도 덮어써서 사용자가 기본 graph.html을 실행해도 안전한 한글 렌더링이 투명하게 노출되도록 강제 보장!
        with open(self.graph_html_path, "w", encoding="utf-8") as f:
            f.write(patched_html)
        print(f"[+] Default graph html safely synchronized and patched: {self.graph_html_path}")


if __name__ == "__main__":
    import sys
    # execute context relative to workstations
    root = "."
    if len(sys.argv) > 1:
        root = sys.argv[1]
    labeller = GraphifyCommunityLabeller(root)
    labeller.run()
