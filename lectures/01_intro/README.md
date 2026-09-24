# 01. Vision AI 입문

## 1. 첫 질문

> AI는 세상을 어떻게 볼까?

사람에게 자연스러운 “보는 것”도 컴퓨터에게는 수많은 숫자에서 의미를 찾는 문제입니다.

## 2. 이 이미지는 무엇으로 보이나요?

사람은 사과 이미지를 보자마자 전체 형태와 의미를 빠르게 인식합니다.

컴퓨터가 처음 받는 것은 “사과”라는 의미가 아니라 **Pixel과 Channel로 이루어진 숫자 배열**입니다.

## 3. 사람은 의미를 보고, 컴퓨터는 RGB 숫자를 받는다

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

중요한 점은 이 RGB 배열에 **색과 2D 위치는 있지만 실제 거리(m)와 실제 물체 크기가 직접 기록되지는 않는다**는 것입니다.

## 4. 가까워서 크게 보이는 것과 실제로 큰 것은 다르다

카메라에 매우 가까운 고양이는 화면에서 많은 Pixel을 차지하고, 멀리 있는 사람은 적은 Pixel을 차지합니다.

사람은 원근감, 장면 맥락, 물체의 일반적인 크기를 함께 이용해 **“고양이가 사람보다 큰 것이 아니라 Camera에 더 가깝다”**고 이해합니다.

반면 단일 RGB Image의 숫자 배열만 보면:

```text
가까운 고양이 → 큰 Pixel 영역
먼 사람      → 작은 Pixel 영역
```

이라는 결과가 먼저 보입니다.

따라서 AI는 여러 장면을 통해 **거리·원근감과 물체 Pattern의 관계**를 학습해야 합니다.

> 핵심: **2D Pixel 크기 ≠ 실제 물체 크기**

## 5. Pixel 하나는 위치와 RGB 값을 가진다

Pixel은 이미지의 한 위치입니다.

```text
image[y=225, x=590]
= [R, G, B]
= [98, 67, 38]
```

한 Pixel만 보면 “사과”라는 의미가 직접 들어 있는 것이 아니라 세 개의 숫자가 있을 뿐입니다.

## 6. Signal과 Noise는 Task 기준으로 구분한다

Signal과 Noise는 서로 다른 종류의 이미지가 아닙니다. 둘 다 컴퓨터에는 Pixel 숫자로 입력됩니다.

- **Signal**: 현재 Task의 판단에 반복적으로 도움이 되는 Pattern
- **Noise**: 정답과 관계없이 우연히 변하는 Sensor Noise, 반사, 불필요한 배경 변화 등

Signal / Noise의 역할은 Task에 따라 달라질 수 있습니다.

## 7. 같은 사과도 촬영 조건에 따라 Pixel이 달라진다

조명, 방향, 거리, 가림, 초점, 색 환경 등이 바뀌면 같은 물체도 Pixel 값과 위치가 크게 달라집니다.

## 8. AI는 변하는 Pixel을 외우기보다 반복되는 Pattern을 배워야 한다

Generalization은 학습에서 보지 못한 새로운 조건에서도 필요한 Pattern을 이용해 올바르게 판단하는 능력입니다.

## 9. 센서가 다르면 숫자의 물리적 의미도 달라진다

| Sensor | 주로 측정하는 정보 | 컴퓨터가 받는 대표 데이터 |
|---|---|---|
| RGB Camera | 색 · 밝기 · 질감 | H × W × 3 Image |
| LiDAR | 거리 · 3D 위치 | Point Cloud |
| IR Sensor / Camera | 적외선 강도 또는 열 정보 | Intensity / Temperature Map |

## 10. 우리 주변에서 만나는 Sensor

- **RGB Camera**: 스마트폰 카메라, CCTV, 블랙박스
- **LiDAR**: 로봇청소기의 거리 측정과 공간 맵핑
- **IR Sensor / Camera**: 열화상 카메라, 설비 발열 검사, 비접촉 온도 측정

LiDAR 생활 예시는 자동차를 제외하고 **로봇청소기 한 가지 사례에 집중**합니다.

## 11. 다음 질문: AI는 숫자에서 어떻게 Pattern을 배울까?

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
