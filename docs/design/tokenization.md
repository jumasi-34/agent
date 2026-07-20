# CQ-BI Tokenization Strategy

CQ-BI는 일관된 시스템 구축을 위해 디자인 요소를 토큰화합니다.

## 1. 구현 단계별 토큰화 우선순위
1. **Foundation:** UI/Data 색상 분리, Semantic 색상 정의, Neutral 배경/테두리 기준, Typography, Spacing Token, Primary 버튼 규칙.
2. **Core Components:** Page Header, Filter Bar, KPI/Chart Card, Status Badge, Table 등 주요 컴포넌트의 토큰화.
3. **Data Visualization:** 카테고리, 연속형, 발산형 팔레트의 매핑 토큰.
4. **Governance:** 신규 페이지 디자인 리뷰 시 토큰 준수 여부 검사.

## 2. 관리 구조 (권장)
```text
design/
├── color/ (UI, Semantic, Data, Accessibility)
├── typography.md
├── spacing.md
└── layout.md
```

## 3. 원칙
- 모든 디자인 요소는 하드코딩하지 않고 토큰(변수)으로 관리한다.
- 토큰 이름은 그 의미(Semantic)를 반영해야 한다(예: `color-danger-main` 대신 `color-semantic-danger`).
