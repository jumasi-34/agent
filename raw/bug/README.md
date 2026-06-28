# Raw Bug Repository (버그 및 장애 원본 데이터 저장소)

## 1. 보존 대상 정보 (Stored Information)
이 폴더에는 단위 테스트 실패, 런타임 `StreamlitAPIException` 충돌, SQLite 데이터베이스 동시성 잠금 에러, WSL 동기화 불일치 등 개발 및 운영 도중 만난 오류 로그(Error Stack Trace) 및 버그의 직접적인 고장 양상(Failure Mode) 원본 데이터를 수집 보존합니다.

## 2. 데이터 관리 대원칙 (Data Immutability Rules)
- **AI 전용 생성 제한**: 이 영역의 모든 파일과 데이터는 오직 AI 개발 에이전트만이 자동으로 생성 및 기록할 수 있습니다.
- **영구 수정 및 가공 금지 (Immutable Raw Space)**: 한 번 기록된 원본 정보는 시스템의 과거 이력을 증명하는 유일한 물리적 단서(Evidence)이므로, 기록된 이후에는 인간 및 AI를 막론하고 **그 어떠한 상황에서도 수정, 삭제, 가공(Mutation)할 수 없습니다.**
