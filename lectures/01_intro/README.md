# 01. Vision AI 입문

## 1. 첫 질문

> 이 이미지는 무엇으로 보이나요?

사람은 사과 이미지를 보자마자 전체 형태와 의미를 빠르게 인식합니다.

컴퓨터가 처음 받는 것은 “사과”라는 의미가 아니라 **Pixel과 Channel로 이루어진 숫자 배열**입니다.

## 2. 사람은 의미를 보고, 컴퓨터는 RGB 숫자를 받는다

RGB 이미지는 Height × Width 위치마다 Red, Green, Blue 세 값이 쌓인 3차원 배열로 볼 수 있습니다.

```text
Image
  ↓
H × W × 3

Channel 0 = Red
Channel 1 = Green
Channel 2 = Blue
```

일반적인 8-bit RGB 이미지에서 각 Channel 값은 보통 0~255 범위입니다.

표시용 예시를 10 × 12로 줄이면:

```text
10 × 12 × 3
= 360 channel values
```

실제 이미지는 훨씬 더 많은 Pixel 값을 가집니다.

## 3. Pixel 하나는 위치와 RGB 값을 가진다

Pixel은 이미지의 한 위치입니다.

예를 들어:

```text
image[y=225, x=590]
= [R, G, B]
= [98, 67, 38]
```

한 Pixel만 보면 “사과”라는 의미가 직접 들어 있는 것이 아니라 세 개의 숫자가 있을 뿐입니다.

## 4. Signal과 Noise는 Task 기준으로 구분한다

Signal과 Noise는 서로 다른 종류의 이미지가 아닙니다.

둘 다 컴퓨터에는 Pixel 숫자로 입력됩니다.

예를 들어 Task가 **“이 이미지가 사과인가?”** 라면:

- **Signal**: 사과 여부 판단에 반복적으로 도움이 되는 윤곽, 형태, 질감 등의 Pattern
- **Noise**: 정답과 관계없이 우연히 변하는 Sensor Noise, 반사, 불필요한 배경 변화 등

```text
Pixel input
   ├─ Task 판단에 도움 → Signal에 가까움
   └─ Task와 무관한 변화 → Noise에 가까움
```

중요한 점은 **Signal / Noise의 구분이 Task에 따라 달라질 수 있다**는 것입니다.

## 5. 같은 사과도 촬영 조건에 따라 Pixel이 달라진다

같은 물체라도 다음 조건에 따라 입력 숫자는 크게 달라집니다.

- 조명
- 방향과 시점
- 거리와 크기
- 가림
- 초점
- 색 환경과 White Balance
- Sensor Noise

사람은 여전히 같은 사과라고 이해할 수 있지만, 컴퓨터가 받는 H × W × 3 배열은 달라집니다.

## 6. AI는 변하는 Pixel을 외우기보다 반복되는 Pattern을 배워야 한다

```text
밝은 사과
어두운 사과
기울어진 사과
작게 보이는 사과
가려진 사과
      ↓
서로 다른 Pixel
      ↓
반복되는 Pattern 학습
      ↓
새로운 조건에서도
“사과”
```

**Generalization**은 학습에서 보지 못한 새로운 조건에서도 필요한 Pattern을 이용해 올바르게 판단하는 능력입니다.

## 7. 센서가 다르면 숫자의 물리적 의미도 달라진다

현재 Intro에서는 대표적인 세 Sensor만 비교합니다.

| Sensor | 얻는 정보 | 대표 데이터 |
|---|---|---|
| RGB Camera | 색 · 밝기 · 질감 | H × W × 3 Image |
| LiDAR | 거리 · 3D 위치 | Point Cloud |
| IR Camera | 적외선 강도 또는 열 정보 | Intensity / Temperature Map |

모두 숫자 데이터이지만 숫자가 의미하는 물리량은 서로 다릅니다.

## 8. 다음 질문: AI는 숫자에서 어떻게 Pattern을 배울까?

```text
Sensor / Image
      ↓
Numeric Data
      ↓
AI Learning
      ↓
Feature / Representation
      ↓
Prediction
```

→ [02. AI 기초](../02_ai_basics/README.md)
