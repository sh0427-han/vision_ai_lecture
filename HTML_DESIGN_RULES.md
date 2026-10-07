# Vision AI Lecture — HTML Design Rules

이 문서는 `vision_ai_lecture`의 HTML 강의자료를 만들거나 수정할 때 사용하는
시각 디자인, 레이아웃, 구현, 검증 기준입니다.

## 1. 적용 우선순위

작업 중 지침이 충돌하면 다음 순서를 따릅니다.

1. 현재 사용자가 직접 요청한 내용
2. `PROJECT_GUIDE.md`
3. 이 문서 `HTML_DESIGN_RULES.md`
4. 기존 슬라이드의 일관된 디자인 패턴
5. 일반적인 웹 디자인 관례

오래된 TODO 문서보다 현재 `PROJECT_GUIDE.md`와 사용자의 최신 요청을 우선합니다.

---

## 2. 대상과 핵심 목표

대상은 AI와 Computer Vision을 처음 접하는 비전공자입니다.

강의자료는 단순히 "예쁜 웹페이지"가 아니라 다음 조건을 만족해야 합니다.

- 한 화면에서 핵심 개념 하나를 이해할 수 있어야 합니다.
- 텍스트를 읽기 전에 그림만 봐도 대략적인 흐름이 보여야 합니다.
- 설명은 쉬워야 하지만 전문성을 잃지 않아야 합니다.
- 그림, 수식, Tensor shape, 화살표의 관계가 기술적으로 정확해야 합니다.
- 발표 화면에서 글자 잘림, 겹침, 과도한 축소가 없어야 합니다.

기본 사고 순서는 다음과 같습니다.

```text
문제 또는 질문
    ↓
직관적인 예시
    ↓
시각적 설명
    ↓
정확한 개념과 용어
    ↓
Vision AI에서의 의미
```

---

## 3. 슬라이드 구성 원칙

### 3.1 한 슬라이드 = 한 핵심 메시지

한 슬라이드에서 여러 개념을 동시에 가르치지 않습니다.

좋은 예:

```text
사과 이미지
    ↓
Grayscale Pixel 값
    ↓
"컴퓨터는 이미지를 숫자로 본다"
```

피해야 할 예:

```text
Pixel + RGB + Tensor + Noise + CNN + Classification
```

내용이 많으면 글씨를 줄이는 대신 슬라이드를 분리합니다.

### 3.2 시각적 흐름

기본 흐름은 왼쪽 → 오른쪽 또는 위 → 아래입니다.

```text
Input  →  Process  →  Output
```

- 화살표 방향을 슬라이드마다 임의로 바꾸지 않습니다.
- 같은 레벨의 요소는 크기와 정렬을 맞춥니다.
- 흐름과 관계가 없는 장식용 화살표는 사용하지 않습니다.
- 텍스트 화살표 문자만 나열하기보다 실제 SVG/HTML 연결선을 우선합니다.

### 3.3 정보 밀도

- 제목은 한 줄을 우선합니다.
- 본문은 핵심 문장 위주로 유지합니다.
- 긴 설명이 필요하면 슬라이드를 추가합니다.
- 작은 글씨로 모든 설명을 한 화면에 넣지 않습니다.
- 같은 의미의 문장을 그림과 본문에서 반복하지 않습니다.

---

## 4. Viewport와 크기

기준 화면은 16:9 Presentation입니다.

권장 설계 기준:

- Reference viewport: 1920 × 1080
- Slide ratio: 16:9
- Title: 약 36–48 px 이상
- Section heading: 약 28–36 px 이상
- Body: 약 22–28 px 이상
- Figure label / annotation: 약 18–22 px 이상

위 수치는 절대값이 아니라 1920 × 1080 기준의 가독성 가이드입니다.
실제 구현에서는 `clamp()`, 상대 단위, 공통 scale 변수를 사용하여 화면 크기에
맞게 조정할 수 있습니다.

### 반드시 지킬 것

- 하나의 슬라이드는 한 viewport 안에 들어와야 합니다.
- 슬라이드 내부 세로 스크롤을 기본 해결책으로 사용하지 않습니다.
- 화면에 맞추기 위해 전체를 지나치게 축소하지 않습니다.
- 작은 화면에서는 자동 Fit이 가능하되, 핵심 label이 읽히는 수준을 유지합니다.
- 제목, figure, footer가 viewport 밖으로 잘리지 않아야 합니다.

---

## 5. 레이아웃

기본적으로 다음 구조를 우선 검토합니다.

### A. 비교형

```text
[ Title ]

[ Before / Human ]       [ After / Computer ]
[ Main visual    ]   →   [ Main visual       ]
```

### B. 흐름형

```text
[ Title ]

[ Input ] → [ Transform ] → [ Output ]
```

### C. Figure 중심형

```text
[ Title ]

        [ Large Main Figure ]

[ 짧은 핵심 설명 또는 takeaway ]
```

### 레이아웃 규칙

- main figure가 가장 큰 시각 요소여야 합니다.
- 같은 중요도의 패널은 동일한 크기와 baseline을 사용합니다.
- panel 간격과 내부 padding을 일정하게 유지합니다.
- card를 기본 단위처럼 남발하지 않습니다.
- 모든 요소를 둥근 사각형으로 감싸지 않습니다.
- 그림을 설명하기 위한 공간보다 장식용 UI가 커지지 않게 합니다.

---

## 6. 전문적인 시각 스타일

현재 프로젝트의 기본 스타일은 다음과 같습니다.

- 흰색 배경
- 절제된 청회색 / 녹색 계열 포인트
- 얇은 선
- 작은 corner radius
- 넉넉한 whitespace
- 명확한 hierarchy
- UI dashboard보다 lecture figure에 가까운 인상

피해야 할 스타일:

- 과도한 gradient
- 과도한 shadow
- glassmorphism
- neon effect
- 모든 내용을 card로 감싸는 dashboard형 구성
- 유아용 clip-art
- 만화풍 icon 남발
- 불필요한 badge / pill / tag
- 장식만을 위한 animation

---

## 7. 이미지, Diagram, SVG 사용 기준

### 실제 장면을 보여줄 때

사진이나 생성 이미지를 우선합니다.

예:

- 조명 변화
- motion blur
- 가림
- 카메라 / LiDAR / IR 사용 장면
- 실제 물체의 시각적 차이

가능하면 Repository 내부 asset으로 저장하여 사용합니다.

### 정확한 구조와 관계를 설명할 때

HTML/SVG Diagram을 우선합니다.

예:

- Tensor shape
- CNN 구조
- Convolution
- Train / Validation / Test split
- Classification / Detection / Segmentation 비교
- Loss / Optimizer 관계
- Data flow

정확한 관계를 설명해야 하는 내용을 생성 이미지에 의존하지 않습니다.

### 외부 Figure

- 논문 Figure를 그대로 복사하기보다 강의용으로 재구성합니다.
- 외부 자료를 직접 사용하면 출처를 기록합니다.
- 출처는 `assets/SOURCES.md`와 동기화합니다.
- 이미지가 단지 "예뻐 보이기 위해" 들어가는지, 학습 목적이 있는지 확인합니다.

---

## 8. Figure 작성 원칙

좋은 Figure는 설명을 읽지 않아도 구조가 보여야 합니다.

### Figure 안에 반드시 명확해야 하는 것

- 무엇이 입력인가?
- 무엇이 처리되는가?
- 무엇이 출력인가?
- 어떤 요소가 서로 대응하는가?
- 방향은 어디인가?

### Label

- 축약어는 첫 등장 시 Full Name을 함께 표시합니다.
- label은 선이나 도형과 겹치지 않아야 합니다.
- label 위치를 억지로 맞추기 위해 font를 지나치게 줄이지 않습니다.
- 동일한 개념에는 동일한 이름을 사용합니다.

### 선과 화살표

- 서로 다른 의미의 연결선을 동일한 형태로 남발하지 않습니다.
- 화살표가 crossing되지 않도록 레이아웃을 먼저 조정합니다.
- 흐름 화살표와 축 표시 화살표를 시각적으로 구분합니다.

---

## 9. 교육 콘텐츠 작성 규칙

### 초보자 관점

새로운 용어가 나오면 먼저 직관을 설명하고 이름을 붙입니다.

권장:

```text
이미지의 작은 영역을 보면서 특정 패턴이 있는지 확인
        ↓
Kernel / Filter
```

피해야 할 방식:

```text
Convolution kernel은 feature extraction을 수행합니다.
```

첫 문장부터 전문 용어만 사용하는 방식은 피합니다.

### 수치 예시

가능하면 구체적인 수치를 사용합니다.

예:

- Grayscale Pixel: 0–255
- RGB Pixel: [R, G, B]
- Image shape: H × W × 3
- Kernel: 3 × 3
- Input: 640 × 640 × 3

단, 실제 asset 크기나 모델 결과를 언급한다면 반드시 실제 값을 확인합니다.

### 정확성

- 교육적 비유와 실제 계산 구조를 구분합니다.
- "CNN이 사람처럼 본다"처럼 과도하게 의인화하지 않습니다.
- 학습되지 않은 내용을 모델이 알고 있다고 표현하지 않습니다.
- Tensor shape, 수식, 연산 순서는 구현 전에 검증합니다.
- 실제 실험 결과가 아닌 그림에는 실제 측정치처럼 보이는 숫자를 넣지 않습니다.

---

## 10. HTML / CSS 구현 규칙

### HTML

- 의미가 있는 section 구조를 사용합니다.
- heading hierarchy를 유지합니다.
- 같은 컴포넌트 구조를 반복할 때 class naming을 통일합니다.
- inline style은 특별한 이유가 없으면 피합니다.
- presentation용 실제 콘텐츠와 개발용 메모를 분리합니다.

### CSS

- 공통 스타일은 `docs/slide.css`를 우선 재사용합니다.
- 비슷한 class를 계속 추가하기 전에 기존 class 재사용 가능성을 확인합니다.
- `!important`는 최후의 수단으로 사용합니다.
- 특정 한 화면에서만 맞는 pixel hack을 최소화합니다.
- 새 스타일을 추가한 뒤 사용되지 않는 이전 스타일을 제거합니다.

### JavaScript

- 정적 표현으로 가능한 내용은 불필요하게 runtime JavaScript로 만들지 않습니다.
- 강의 화면을 구성하기 위해 무거운 외부 library를 추가하지 않습니다.
- 외부 CDN은 현재 프로젝트 방침상 추가하지 않습니다.
- 시각 자료용 데이터가 고정되어 있다면 가능한 경우 정적으로 생성합니다.

---

## 11. 반응형과 Auto-fit

자동 축소는 안전장치이지 콘텐츠 설계의 대체물이 아닙니다.

작업 순서:

```text
콘텐츠 단순화
    ↓
레이아웃 재배치
    ↓
슬라이드 분리
    ↓
마지막으로 Auto-fit
```

금지에 가까운 패턴:

```text
내용이 많음
    ↓
전체 scale: 0.65
    ↓
글씨가 읽히지 않음
```

---

## 12. 기존 자산 재사용

새로운 이미지를 만들기 전에 다음을 확인합니다.

- `docs/assets/generated/`
- `docs/assets/`
- `assets/diagrams/`
- `assets/SOURCES.md`

같은 개념의 자산이 이미 있다면 우선 재사용합니다.

같은 사과, 같은 촬영 장면, 같은 모델 예제를 반복 사용하는 것은
학습자의 인지 부담을 줄이므로 의도적인 재사용으로 봅니다.

---

## 13. 작업 Workflow

모든 수정은 다음 흐름을 권장합니다.

```text
1. 최신 Repository 확인
        ↓
2. PROJECT_GUIDE.md 확인
        ↓
3. HTML_DESIGN_RULES.md 확인
        ↓
4. 대상 HTML/CSS와 주변 슬라이드 확인
        ↓
5. 내용/레이아웃 설계
        ↓
6. 구현
        ↓
7. 시각적 검증
        ↓
8. HTML/CSS/asset 경로 검증
        ↓
9. 불필요한 이전 코드 정리
        ↓
10. 배포 결과 확인
```

기존 슬라이드를 수정할 때 해당 슬라이드만 보지 말고 앞뒤 슬라이드도 함께 확인합니다.
강의 흐름과 시각 스타일이 자연스럽게 이어져야 합니다.

---

## 14. 완료 전 체크리스트

### 내용

- [ ] 한 슬라이드의 핵심 메시지가 하나인가?
- [ ] 초보자가 처음 보는 용어를 이해할 수 있는가?
- [ ] 비유와 실제 기술 설명이 구분되어 있는가?
- [ ] Tensor shape, 수식, 숫자가 정확한가?
- [ ] 앞뒤 슬라이드와 설명이 중복되지 않는가?

### 시각

- [ ] 그림만 봐도 입력 → 처리 → 출력이 보이는가?
- [ ] main figure가 충분히 큰가?
- [ ] 텍스트가 도형/선/축과 겹치지 않는가?
- [ ] slide 밖으로 나가는 요소가 없는가?
- [ ] 지나치게 작은 글씨가 없는가?
- [ ] panel / baseline / spacing이 정렬되어 있는가?
- [ ] card나 장식 요소가 불필요하게 많지 않은가?

### 구현

- [ ] HTML tag 구조가 정상인가?
- [ ] 공통 CSS를 재사용했는가?
- [ ] 미사용 CSS/JS를 남기지 않았는가?
- [ ] asset path가 정상인가?
- [ ] 외부 CDN을 추가하지 않았는가?
- [ ] 수정한 모든 페이지에서 공통 CSS 변경 영향이 없는가?
- [ ] 실제 GitHub Pages 렌더링을 확인했는가?

---

## 15. 참고 기준

HTML과 접근성의 기본 원칙은 다음 공식 문서를 우선 참고합니다.

- MDN Web Docs — HTML
  - https://developer.mozilla.org/docs/Web/HTML
- MDN Web Docs — CSS
  - https://developer.mozilla.org/docs/Web/CSS
- W3C WAI — Page Structure
  - https://www.w3.org/WAI/tutorials/page-structure/
- W3C WCAG
  - https://www.w3.org/WAI/standards-guidelines/wcag/

프레젠테이션 구조의 참고가 필요할 때는 reveal.js의 문서 구조도 참고할 수 있습니다.

- https://revealjs.com/

단, 이 프로젝트가 reveal.js로 반드시 구현되어야 한다는 의미는 아닙니다.
현재 Repository 구조와 공통 스타일을 우선합니다.
