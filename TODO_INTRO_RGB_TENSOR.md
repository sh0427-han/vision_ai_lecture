# TODO — Intro RGB 3D Tensor 개선

## 목적

Intro의 사람 vs 컴퓨터 이미지 인식 설명을 더 직관적으로 수정한다.

핵심 메시지:

> 사람은 사과 이미지를 바로 “사과”로 이해하지만, 컴퓨터 입력은 RGB 3채널로 쌓인 Pixel 숫자 배열이다.

현재 구현된 `원본 사과 → 15×10 Downscale Canvas → R/G/B 숫자 배열 3개 카드` 구조는 사용자의 의도와 다르므로 교체한다.

---

## 현재 상태

- 대상 파일: `docs/intro.html`, `docs/slide.css`
- 현재 cache key: `realpixels-20260923-10`
- Intro 내부 `slide-number = 1` 슬라이드가 수정 대상
- 현재 슬라이드에는 다음 구조가 존재함:
  - Original image
  - Downscale · 15×10
  - Actual RGB arrays
- 현재 관련 요소:
  - `apple-pixel-flow`
  - `apple-pixel-canvas`
  - `apple-r-matrix`
  - `apple-g-matrix`
  - `apple-b-matrix`
  - `Intro real pixel extraction` inline script
  - 관련 `apple-pixel-*`, `apple-rgb-*` CSS

이 구조는 제거 또는 대체 대상이다.

---

## 원하는 최종 구성

### 1. 왼쪽 — 원본 사과 이미지

- 기존 `docs/assets/vision_task_apple_reference.jpg` 사용
- 사람 관점:
  - 전체 형태
  - 색
  - 윤곽
  - 질감
  - 의미
- 문구는 짧게 유지:
  - 예: `사람: “사과”라는 의미를 바로 인식`

### 2. 오른쪽 — 하나의 3차원 RGB Tensor

R / G / B를 서로 떨어진 카드 3개로 보여주지 않는다.

반드시 **3개의 Channel Plane이 깊이 방향으로 겹쳐진 3차원 Tensor 형태**로 표현한다.

권장 형태:

```text
          B plane
       ┌──────────┐
      / 숫자 배열 /
     └──────────┘

        G plane
     ┌──────────┐
    / 숫자 배열 /
   └──────────┘

      R plane
   ┌──────────┐
  / 숫자 배열 /
 └──────────┘
```

실제 구현에서는 기존 Intro에 사용했던 `rgb-tensor`, `tensor-plane--r/g/b`, `tensor-axis` 계열 구조를 재사용하거나 개선하는 것을 우선 검토한다.

중요:
- R/G/B가 한눈에 **같은 이미지의 3채널**임을 보여야 함
- 세 Plane은 같은 Width × Height를 공유
- Channel 축 방향으로 3장이 쌓여 있다는 느낌이 명확해야 함
- 각 Plane 내부에 Pixel 숫자가 충분히 크게 보여야 함
- 숫자와 테두리/축/라벨이 겹치지 않아야 함

---

## Pixel 숫자 표시 규칙

실제 이미지 전체 Pixel 수를 모두 표시하려고 하지 않는다.

강의용 가독성을 위해 실제 사과 이미지를 **작은 해상도로 Downscale한 RGB 값**만 표시한다.

### 권장
- 표시용: `12 × 10 × 3`
- 대안: `15 × 10 × 3`
- 숫자 가독성이 떨어지면 12×10을 우선

중요:
- 숫자는 임의 예시값보다 **실제 사과 이미지에서 추출한 RGB 값**을 사용
- Downscale은 숫자 표시량을 줄이기 위한 것일 뿐, 별도의 “Downscale 단계”를 슬라이드에 보여주지 않음
- 시각 흐름은 반드시:
  - `사과 이미지 → RGB 3D Tensor`

### 데이터 생성 권장 방식

가능하면 수정 작업 시 사과 이미지를 실제로 Downscale하여 RGB 값을 **정적으로 HTML에 삽입**한다.

권장 이유:
- 강의 중 브라우저 런타임 계산 불필요
- Canvas / `getImageData()` 스크립트 불필요
- 구조 단순
- 렌더링 안정성 향상

정적 생성이 어려운 경우에만 runtime Canvas 방식을 사용한다.

---

## Slide 문구 권장안

### 제목

`사람은 “사과”를 보고, 컴퓨터는 RGB 숫자 배열을 봅니다`

### 부제

`사람은 전체 형태와 의미를 한 번에 인식하지만, 컴퓨터가 처음 받는 것은 위치별 R · G · B 값이 쌓인 3차원 배열입니다.`

### 하단 설명

`표시된 숫자는 실제 사과 이미지를 작게 Downscale해 일부 Pixel 값을 보여준 예시입니다.`

또는:

`실제 이미지는 훨씬 많은 Pixel을 가지며, 여기서는 구조를 보기 위해 숫자 배열만 축소해 표현했습니다.`

---

## Tensor 축 / Shape 표현

3D Tensor 옆 또는 아래에 다음 의미를 표시한다.

- Height
- Width
- Channel = 3
- R · G · B

단, 표시용 Downscale 숫자 배열과 실제 원본 이미지 해상도를 혼동시키지 않는다.

예:

```text
Display example = 10 × 12 × 3
Actual input = H × W × 3
```

원본 이미지의 실제 해상도를 표기하려면 반드시 실제 asset 크기를 확인한 뒤 사용한다.

---

## 제거 대상

새 구조가 완성되면 아래 현재 구현 중 더 이상 사용하지 않는 요소를 제거한다.

### HTML
- 가운데 별도 Downscale Canvas 카드
- R/G/B 별도 세로 카드
- 선택 Pixel `(7, 5)` 강조 UI
- `apple-pixel-rgb`
- 불필요해진 runtime Canvas script

### CSS
사용되지 않게 된 아래 계열 정리:
- `apple-pixel-flow`
- `apple-pixel-card`
- `apple-pixel-canvas-frame`
- `apple-pixel-grid-overlay`
- `apple-pixel-selected`
- `apple-pixel-sample`
- `apple-rgb-stack`
- `apple-rgb-plane`
- 기타 PR #11에서 추가된 미사용 스타일

기존 `rgb-tensor` 계열을 다시 사용할 경우 중복 CSS를 만들지 않는다.

---

## 디자인 원칙

- 초보자가 그림만 봐도 `사과 → RGB 3채널 숫자 배열` 흐름을 이해할 수 있어야 함
- 한 슬라이드 핵심 메시지 하나 유지
- 시각 자료 비중을 높임
- 숫자는 실제 강의 화면에서도 읽을 수 있는 크기 유지
- 텍스트/숫자가 Plane 경계나 축을 침범하지 않도록 함
- 기존 Intro 디자인과 일관성 유지
- 외부 CDN 추가 금지

---

## 검증 체크리스트

수정 완료 후 반드시 확인:

- [ ] 최신 `main`에서 작업 시작
- [ ] `PROJECT_GUIDE.md` 확인
- [ ] Intro `slide-number = 1`이 `사과 → RGB 3D Tensor` 2단 구조인지 확인
- [ ] 별도의 Downscale 단계 카드가 화면에 존재하지 않음
- [ ] R/G/B가 분리 카드가 아니라 3D로 겹친 Channel Plane 형태임
- [ ] 세 Plane 내부 숫자가 실제 사과 이미지에서 추출된 값임
- [ ] 표시용 숫자 배열 크기가 12×10 또는 15×10 수준인지 확인
- [ ] 숫자가 Plane 내부를 충분히 채우고 강의 화면에서 읽힘
- [ ] Height / Width / Channel 축이 겹치지 않음
- [ ] Intro 전체 section 수와 slide-number 순서 확인
- [ ] HTML tag 구조 확인
- [ ] CSS 중괄호 수 확인
- [ ] 사용하지 않는 PR #11용 Canvas/Pixel CSS 및 JS 제거
- [ ] 공유 `slide.css` 변경 시 `intro.html`, `ai_basics.html`, `vision_ai.html` cache key 함께 갱신
- [ ] PR 생성 및 merge
- [ ] merge 후 `main`의 실제 파일 재확인
- [ ] 가능하면 merge commit 기준 GitHub Actions / Pages Workflow 상태 확인

---

## 최종 목표 화면

```text
┌─────────────────────┐       ┌─────────────────────────────┐
│                     │       │       B Channel Plane       │
│       APPLE         │       │      [ Pixel numbers ]      │
│       IMAGE         │  →    │    G Channel Plane          │
│                     │       │   [ Pixel numbers ]         │
│                     │       │ R Channel Plane             │
└─────────────────────┘       │ [ Pixel numbers ]           │
                              └─────────────────────────────┘

 사람: “사과”                   컴퓨터: H × W × 3 RGB Tensor
```

핵심은 **Downscale 자체를 설명하는 슬라이드가 아니라, 사과 이미지가 컴퓨터 입력에서는 RGB 3차원 숫자 배열이라는 사실을 직관적으로 보여주는 것**이다.
