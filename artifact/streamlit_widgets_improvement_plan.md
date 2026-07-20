# app/core/design_system/streamlit_widgets.py 검토 및 개선 계획서

본 문서는 `app/core/design_system/streamlit_widgets.py` 모듈의 프리미엄 디자인 정합성, 코드 표준 및 가이드라인 준수 여부를 종합 검토하고, 이를 바탕으로 도출한 구체적인 품질 개선 계획을 명세합니다.

---

## 1. 종합 검토 결과 및 진단 (Review & Diagnosis)

`streamlit_widgets.py`는 디자인 시스템 토큰을 기반으로 Streamlit 대시보드 전반의 프리미엄 UI(Header, Metric, Custom Table 등)를 책임지는 핵심 모듈입니다. 전반적인 모듈 설계와 미려한 글래스모피즘 테이블 렌더링은 우수하지만, `GEMINI.md` 6대 가이드라인 및 하위 L2/L3 규칙들과 대조했을 때 다음과 같은 잠재적 기술 부채 및 불일치가 발견되었습니다.

### 1.1 하드코딩된 HEX 컬러 (L2-color-system.md 위배)
- **현상**: `render_production_summary_table` 및 `_render_premium_defect_card` 등의 CSS 주입부, 함수 아규먼트 기본값 등에서 `#e2e8f0`, `#64748b`, `#f8fafc`, `#16a34a`, `#dc2626` 같은 HEX 색상 코드가 다수 직접 기술(하드코딩)되어 있습니다.
- **리스크**: 테마(라이트/다크 모드) 전환 시 글자 색상과 배경의 가독성 뭉개짐이 발생할 수 있고, 시맨틱 토큰 중앙 통제가 불가능해집니다.

### 1.2 유니코드 특수기호/이모지 사용 (L3-dashboard.md 위배)
- **현상**: 테이블 정렬 지시계(`↕`), 툴팁 트리거(`ⓘ`) 등에서 유니코드 특수문자를 하드코딩하여 사용 중입니다.
- **리스크**: 브라우저 폰트 렌더링 지연 또는 OS에 따라 깨짐 현상이 발생할 수 있으며, 이모지/특수문자 전면 금지 및 구글 머티리얼 심볼 일원화 원칙과 정합성이 맞지 않습니다.

### 1.3 HTML 평탄화 (Minify) 누락
- **현상**: `_minify_html` 헬퍼 함수가 구현되어 있으나 `vertical_metric`, `horizontal_metric`, `render_production_summary_table` 등의 출력부에서는 이 헬퍼를 거치지 않고 날것의 멀티라인 문자열을 `st.markdown`에 직접 전달하고 있습니다.
- **리스크**: Streamlit의 마크다운 파서가 줄바꿈과 공백을 잘못 파싱하여 뜻하지 않은 `<p>` 단락이 삽입되거나 레이아웃 정렬이 뭉개지는 현상이 간헐적으로 발생합니다.

### 1.4 타입 힌팅 및 Docstring 불일치 (GEMINI.md ⑥번 규칙)
- **현상**: `_render_premium_metric_card`를 비롯한 프리미엄 헬퍼 함수군에서 Google/NumPy 스타일의 Docstring 포맷이 다소 혼용되어 있으며, 인자 및 반환값에 대한 Type Hinting이 부분적으로 누락되어 있습니다.
- **리스크**: 정적 컴파일러(MyPy 등) 분석 시 경고가 발생할 수 있고 코드 유지보수성이 저하됩니다.

### 1.5 물리 경로 정합성 불일치
- **현상**: `L3-dashboard.md` 규칙 문서 상에는 공통 UI 컴포넌트의 경로를 `app/core/ui/`로 안내하고 있으나, 실제 물리적인 소스 구조는 `app/core/design_system/`에 단일화되어 있습니다.
- **리스크**: 에이전트가 다른 개발 작업을 시작할 때 경로 혼선 및 작업 지연을 유발합니다.

---

## 2. 세부 개선 계획 (Improvement Plan)

위 진단 결과를 토대로 기존 대시보드 작동에 어떠한 사이드 이펙트도 주지 않으면서 정적 무결성을 100% 확보할 수 있는 **5대 핵심 개선 과제**를 제시합니다.

### 과제 [1] HEX 컬러의 시맨틱 토큰화 및 일원화
- **내용**: 
  - 파일 상단에서 임포트된 `colors` 객체(`from app.core.design_system.tokens import colors`)를 활용하여 인라인 스타일의 HEX 코드를 런타임 바인딩으로 전수 대체합니다.
  - **매핑 설계 예시**:
    - `#e2e8f0` (테두리) ➡️ `{colors.app_border}`
    - `#64748b` (보조 텍스트) ➡️ `{colors.app_text_secondary}`
    - `#f8fafc` (헤더 배경) ➡️ `{colors.app_background}`
    - `#0f172a` (본문 메인 텍스트) ➡️ `{colors.app_text_primary}`
    - `#1e3a8a` / `#0f766e` / `#b45309` (지표값 컬러) ➡️ `colors`에 정의된 프리미엄 차트/상태 시맨틱 값 연동
    - `#16a34a` (성공/양호 상태) ➡️ `{colors.status_success}` 또는 `{colors.green_600}`
    - `#dc2626` (오류/부적합 상태) ➡️ `{colors.status_error}` 또는 `{colors.red_600}`

### 과제 [2] 특수문자 제거 및 Material Icon 폰트 바인딩 전환
- **내용**:
  - `↕` 정렬 지시계 ➡️ Material Symbols의 `unfold_more` (`&#xf194;`) 또는 CSS 가상 요소 배치로 전환하여 시스템 폰트 깨짐 예방.
  - `ⓘ` 툴팁 트리거 ➡️ 구글 머티리얼 아이콘인 `info` (`&#xe88e;`)를 활용하도록 HTML 태그 클래스 및 렌더링 방식 개선.
  - 인라인으로 결합된 특수 기호 대신, 클래스를 통해 표준 아이콘 폰트를 입혀 렌더링 무결성을 확보합니다.

### 과제 [3] st.markdown 주입 HTML 전수 평탄화 (Minify) 적용
- **내용**:
  - `vertical_metric`, `horizontal_metric`, `render_production_summary_table` 등 HTML 마크업을 직접 출력하는 모든 컴포넌트의 끝자락에 `_minify_html`을 감싸서 한 줄의 완전한 플랫 스트링으로 변환 후 주입합니다.
  - 예: `st.markdown(_minify_html(html_content), unsafe_allow_html=True)`

### 과ze [4] NumPy/Google 스타일 Docstring 및 Type Hinting 완전 정비
- **내용**:
  - `_render_premium_metric_card`, `_render_premium_multi_metric_card` 등의 내부 헬퍼 함수 시그니처에 명확한 타입 힌팅 적용 (예: `sub_metrics: list[dict[str, str]]`, `-> str` 등).
  - 함수별 Docstring을 NumPy/Google 표준 스타일로 통일하여 매개변수 설명 및 리턴 타입을 엄격히 명세합니다.

### 과제 [5] L3-dashboard.md 가이드 문서의 경로 최신화
- **내용**:
  - `.agents/rules/L3-dashboard.md` 파일 내의 `app/core/ui/` 표기를 실제 물리 구조인 `app/core/design_system/`로 일괄 치환하여 문서의 정합성을 최신화합니다.

---

## 3. 검증 및 배포 전략 (Verification & Rollout Strategy)

1. **테스트 하네스 검증**:
   - `tests/` 디렉터리 내에 독립 테스트 케이스를 구축하여 개선된 위젯 렌더링 시 HTML 파싱이 깨지지 않는지 확인합니다 (Mocking Streamlit context).
   - 기존의 `tests/refactoring_harness_test.py` 등 연관된 UI/디자인 시스템 테스트를 구동하여 리그레션(회귀 오류) 여부를 완전 검증합니다.
2. **실시간 테마 호환성 확인**:
   - 다크/라이트 모드에서 시맨틱 컬러 토큰이 정상적으로 변경 적용되는지 CSS 인라인 매핑 상태를 비교 검증합니다.

---

위 개선 계획에 동의하시면 **"승인"** 또는 **"수정 사항"**을 말씀해 주십시오. 승인해주시는 즉시 가이드라인에 맞추어 안전하고 정확한 리팩토링 작업을 속행하겠습니다.
