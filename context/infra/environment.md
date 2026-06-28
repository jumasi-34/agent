---
id: infra.environment
title: "Ref: CONTEXT > INFRA > ENVIRONMENT"
type: reference
status: active

summary: >
  WSL2 로컬 개발환경과 Ubuntu 리눅스 Production 실서비스 환경 간의 하드웨어, OS 사양, Python 패키지 버전(Miniconda), 오라클 및 Databricks 드라이버 구성 정합성 보고 가이드라인.

keywords:
  - environment
  - system-spec
  - python-packages
  - wsl2
  - miniconda

parent: "[[context/infra/infra-index.md]]"

related:
  - "[[context/infra/infrastructure-summary.md]]"
  - "[[context/guide/manual-setup.md]]"

consumers:
  - "[[agents/roles/planner-orchestrator.md]]"
  - agent.system_administrator

updated: 2026-06-28
---


# context-environment.md (개발 및 서비스 환경 정합성 보고서)

## Overview
* **왜 존재하는가 (Why)**: 로컬 개발 환경과 실제 운영 환경 간의 패키지 버전 이격이나 드라이버 설정 차이를 사전에 식별하여 배포 시의 시스템 비호환 런타임 오류를 완벽히 차단하기 위함입니다.
* **언제 사용하는가 (When)**: 신규 파이썬 라이브러리를 추가하거나, 실서버 배포 중 라이브러리 충돌이 의심될 때, Miniconda 가상환경 구성을 동기화할 때 참조합니다.
* **연계 실행 (Next Action)**: 구체적인 운영 서버 배포 매뉴얼과 수동 배포 단계를 보려면 [[context/guide/manual-setup.md]]을 참조하십시오.

## Connections
* **상위 개념**: [infra.readme](.agents/context/infra/infra-index.md)
* **연관 자산**:
  - [.agents/context/guide/manual-setup.md](.agents/context/guide/manual-setup.md)
  - [.agents/context/infra/infrastructure-summary.md](.agents/context/infra/infrastructure-summary.md)

---

본 문서는 `goeq_bi` 프로젝트의 **WSL2 로컬 개발환경**과 **Ubuntu 리눅스 실서비스 환경**의 시스템 사양, 패키지 구성, 네트워크 엔드포인트 및 동기화 상태를 정밀 분석하고 기록하기 위한 개발환경 정보 아키텍처 가이드입니다. 

---

## 1. 하드웨어 및 운영체제 사양 비교

| 구분 | 개발환경 (WSL2 Local) | 서비스환경 (Ubuntu Production Server) | 분석 및 특이사항 |
| :--- | :--- | :--- | :
---
 |
| **운영체제** | Ubuntu 24.04.2 LTS (Noble) | Ubuntu 24.04.1 LTS (Noble) | 동일 배포판 계열로 매우 일치함 |
| **커널** | `6.6.87.2-microsoft-standard-WSL2` | `6.8.0-106-generic` (Ubuntu 공식) | WSL 가상화 커널 vs 네이티브 리눅스 커널 차이 |
| **메모리(RAM)**| 7.6 GiB (여유: 5.0 GiB) | **15.0 GiB** (여유: 12.0 GiB) | 실서비스 환경의 메모리 자원이 약 2배 넉넉함 |
| **디스크(SSD)**| 1.0 TB (44GB 사용 중) | 98 GB (24GB 사용, 여유 70GB) | `/dev/mapper/ubuntu--vg` 마운트 적용됨 |

---

## 2. Python 런타임 및 주요 패키지 버전 분석

양쪽 환경 모두 동일한 미니콘다(Miniconda) 가상환경 경로를 사용하고 있으나, 일부 프론트엔드 패키지 버전 불일치가 감지되었습니다.

### ① 런타임 경로 일치도
- **개발 환경 Python**: `/home/jumasi/miniconda3/envs/goeq/bin/python` (Python 3.12.9)
- **서비스 환경 Python**: `/home/jumasi/miniconda3/envs/goeq/bin/python` (Python 3.12.9)
- > [!NOTE]
  > 실행 경로 및 파이썬 메이저/마이너 버전이 완벽히 일치하여 스크립트 실행 정합성이 매우 우수합니다.

### ② 주요 패키지 버전 정합성 비교

| 패키지 명 | 개발환경 (WSL2) | 서비스환경 (Production) | 정합성 점검 결과 |
| :--- | :--- | :--- | :--- |
| **streamlit** | `1.42.2` | **`1.50.0`** | [주의] 버전 불일치 (서비스 환경이 더 최신) |
| **pandas** | `2.2.3` | `2.2.3` | 완벽히 일치함 |
| **numpy** | `2.2.5` | `2.2.3` | 정상 (미세한 마이너 패치 차이) |
| **scipy** | `1.15.3` | `1.16.0` | 정상 (미세한 마이너 패치 차이) |
| **plotly** | `6.0.0` | `6.0.0` | 완벽히 일치함 |
| **matplotlib** | `3.10.3` | `3.10.1` | 정상 (미세한 마이너 패치 차이) |
| **databricks-sql-connector** | `4.0.5` | `4.0.5` | 완벽히 일치함 |

> [!WARNING]
> **Streamlit 버전 불일치 관련 권고사항**
> - 서비스 환경이 `1.50.0`인 반면, 개발 환경은 `1.42.2`입니다.
> - Streamlit은 마이너 버전 업데이트 시 세션 상태(Session State), 차트 렌더링, 탭 UI 등에서 호환성 동작이 다를 수 있으므로, 원활한 로컬 검증을 위해 개발 환경(WSL)의 Streamlit 버전을 서비스 환경에 맞추어 `1.50.0`으로 업데이트하는 것을 강력히 권장합니다.
> - **업데이트 명령어 (WSL)**: `/home/jumasi/miniconda3/envs/goeq/bin/python -m pip install streamlit==1.50.0`

---

## 3. Git 및 서비스 아키텍처 정합성

### ① 소스코드 형상 관리 동기화 (WSL ↔ Github ↔ Ubuntu)
- **개발환경 원격지 주소**: `git@github.com:jumasi-34/goeq_bi.git` (SSH 프로토콜 사용)
- **서비스환경 원격지 주소**: `https://github.com/jumasi-34/goeq_bi.git` (HTTPS 프로토콜 사용)
- **커밋 및 동기화 시차 감지**:
  - 개발환경(WSL) 최근 커밋: `bbdbda0` (Refactor: docs/document 하위의 구 문서 파일 Git 추적 제거)
  - 서비스환경(Ubuntu) 최근 커밋: `afc453d` (Refactor EV3 page to ensure proper initialization...)
  - **분석**: 개발환경에서 새로 커밋된 사항이 실서비스(Ubuntu) 환경에 아직 반영(`git pull`)되지 않았거나, 원격 브랜치 관리에 시차가 있습니다. 서비스를 배포할 때 Ubuntu 환경에서 최종 `pull`을 수행해야 동기화가 정상 완료됩니다.

### ② 실서비스 가동 프로세스 및 포트 현황
Ubuntu 서비스 환경에서 2개의 Streamlit 앱 인스턴스가 백그라운드로 실행 중입니다.

1. **포트 8501 운영 서버 (메인)**:
   - PID: `566536` (May 28일 실행됨)
   - 실행 명령어: `/home/jumasi/miniconda3/envs/goeq/bin/python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
2. **포트 8502 운영/검증 서버 (예비/검증용)**:
   - PID: `499147` (May 19일 실행됨)
   - 실행 명령어: `/home/jumasi/miniconda3/envs/goeq/bin/python -m streamlit run app.py --server.port=8502 --server.address=0.0.0.0`

---

## 4. 데이터베이스 연동 및 환경 변수 사양

- **Oracle Instant Client 라이브러리 경로**:
  - 개발환경: `/opt/oracle/instantclient_23_8` 등 설정 활성화
  - 서비스환경: `/opt/oracle/instantclient_23_8` 및 `/opt/instantclient_23_8` 등이 이미 환경 변수 `LD_LIBRARY_PATH`에 성공적으로 바인딩되어 시스템 레벨에서 원활히 동작 중입니다.
- **TNS_ADMIN**:
  - 양쪽 환경 모두 기본 시스템 설정 내에는 비어 있으나, 개발환경에서는 `setup_oracle_env.sh`가 로드될 때 활성화될 수 있는 하이브리드 구성을 가지고 있어 Oracle DB 연결 및 쿼리 테스트 환경이 정상적으로 조율되어 있습니다.
