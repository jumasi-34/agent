# CQ-BI Color System

## 1. 기본 관점
CQ-BI는 카테고리형 데이터가 많기 때문에 색상을 일률적으로 줄이는 접근은 적절하지 않습니다. 중요한 것은 색상이 맡는 역할입니다.
> 색이 많은 것이 아니라, UI 색과 데이터 색의 역할이 섞여 있는 것이 문제다.

## 2. Color Roles (색상 역할)

### A. UI Color (인터페이스 구성)
- 적용 대상: Background, Card, Border, Sidebar, Button, Text 등.
- 원칙: Neutral 중심, 제한적이고 차분하게 운영. Shadow보다 Border와 Spacing 활용.

### B. Semantic Color (상태와 의미)
- Info (안내), Success (정상), Warning (주의), Danger (오류).
- 다른 의미로 재사용 금지.

### C. Data Color (분석 데이터 범주 및 값)
- **Categorical Palette:** 순서 없는 카테고리 구분용.
- **Sequential Palette:** 연속적인 크기 표현 (데이터 밀도).
- **Diverging Palette:** 기준값 중심의 양방향 차이 표현.

### D. Module Accent (위치 인지)
- 현재 모듈/영역 위치를 인지시키는 보조 색상 (Navigation, Icon, Marker).
- 넓은 배경이나 카드 전체 채우기 금지.

## 3. 핵심 규칙
1. **분리:** UI 색과 Data 색을 명확히 분리한다.
2. **일관성:** 같은 카테고리는 가급적 같은 색을 유지한다.
3. **분석 목적:** 카테고리 비교, 크기 비교, 편차, 상태에 따라 팔레트를 결정한다.
4. **구조화:** 색상 수가 많아지면 구조(Top N, Small Multiples 등)를 바꾼다.
5. **강조:** 핵심 항목만 강하게, 나머지는 Neutral/낮은 채도로 처리한다.
6. **의미 고정:** Semantic Color(Red, Orange, Green, Blue)의 의미를 고정한다.
7. **복합 인코딩:** 색상 외 요소(Line style, Marker, Label 등)를 병행한다.
