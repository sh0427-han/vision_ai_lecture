# 01. Vision AI 입문

## 1. 첫 질문

> AI는 세상을 어떻게 볼까?

사람에게 자연스러운 “보는 것”도 컴퓨터에게는 수많은 숫자에서 의미를 찾는 문제입니다.

## 2. 사진 속 크기와 실제 크기는 다를 수 있다

카메라에 매우 가까운 고양이는 화면을 크게 차지하고, 멀리 있는 사람은 작게 보일 수 있습니다.

사람은 다음 정보를 함께 사용해 상황을 자연스럽게 이해합니다.

- 원근감
- 거리 단서
- 고양이와 사람의 일반적인 실제 크기
- 장면 전체의 맥락

반면 단일 RGB Image의 Pixel 값에는 **실제 거리와 실제 물체 크기가 명시적으로 들어 있지 않습니다.**

따라서 Vision AI는 많은 데이터에서 물체의 형태와 원근감, 장면의 Pattern을 학습해야 합니다.

> 핵심: **사진 속 Pixel 크기 ≠ 실제 물체 크기**

## 3. 이 이미지는 무엇으로 보이나요?

사람은 사과 이미지를 보자마자 전체 형태와 의미를 빠르게 인식합니다.

컴퓨터가 처음 받는 것은 “사과”라는 의미가 아니라 **Pixel과 Channel로 이루어진 숫자 배열**입니다.

## 4. 사람은 의미를 보고, 컴퓨터는 RGB 숫자를 받는다

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

이번 Intro의 LiDAR 생활 예시는 자동차를 제외하고 **로봇청소기 한 가지 사례에 집중**합니다.

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
