# 01. Vision AI 입문

## 학습 목표

이 챕터가 끝나면 다음 질문에 답할 수 있어야 합니다.

1. Vision AI는 무엇을 하는 기술인가?
2. Vision 정보를 얻는 센서에는 어떤 종류가 있는가?
3. 컴퓨터에게 이미지는 어떤 숫자 구조인가?
4. 같은 물체인데도 왜 입력 데이터는 달라지는가?
5. Classification, Detection, Segmentation 등은 어떤 질문에 답하는가?

---

## 1. Vision AI란?

Vision AI는 이미지나 영상뿐 아니라 Depth Map, 3D Point Cloud, Event Stream처럼
**시각 센서에서 얻은 데이터를 이용해 장면의 의미를 추출하는 AI 기술**입니다.

단순한 이미지 분류보다 범위가 넓습니다.

```text
Real World
    ↓
Sensor
    ↓
Numeric Data
    ↓
Vision Model
    ↓
판단 / 측정 / 제어
```

예를 들면 다음과 같습니다.

- 사진 속 물체의 종류를 분류
- 사람이나 차량의 위치를 Detection
- 결함 영역을 Pixel 단위로 Segmentation
- 영상 속 물체를 Tracking
- 두 물체 사이의 거리나 3차원 구조를 추정
- 제품의 정상/이상 상태를 자동 판정

---

## 2. 일상에서 어디에 쓰일까?

### Smartphone
- 장면·얼굴 인식
- 배경 분리
- 사진 검색
- 카메라 자동 보정

### OCR / Document
- 사진 속 문자 인식
- QR / Barcode 인식
- 문서 구조 분석

### Mobility
- 차선
- 보행자
- 차량
- 장애물
- 이동 가능 영역

### Manufacturing
- Scratch / 오염 / 파손
- 부품 누락
- 위치·조립 상태
- 형상 및 거리 측정

### Medical
- X-ray, CT, MRI 등 의료 영상의 관심 영역 분석

---

## 3. Vision 정보를 얻는 센서

Vision AI에서 입력은 반드시 일반 RGB 사진일 필요가 없습니다.

| 센서 | 주로 얻는 정보 | 대표 데이터 |
|---|---|---|
| RGB Camera | 가시광의 색과 밝기 | H×W×3 Image |
| Mono Camera | 밝기 | H×W Image |
| IR / NIR | 적외선 반사 특성 | Intensity Image |
| Thermal Camera | 열 분포 | Temperature Map |
| Depth Camera | 물체까지 거리 | Depth Map |
| LiDAR | 3차원 거리 | Point Cloud |
| Event Camera | Pixel 밝기 변화 | Event Stream |

### Depth Camera

Depth Camera는 각 Pixel에 장면의 색이 아니라 **카메라와 물체 사이 거리**를 기록합니다.

대표적인 방식:
- Stereo
- Time of Flight (ToF)
- Structured Light

### LiDAR

Laser를 이용해 여러 방향의 거리를 측정하고 3차원 점 집합을 만듭니다.

```text
(x, y, z)
(x, y, z)
(x, y, z)
...
```

이런 형태를 **Point Cloud**라고 합니다.

### Event Camera

일반 카메라는 예를 들어 30 FPS라면 1초에 30장의 완전한 Frame을 만듭니다.

Event Camera는 다릅니다.

Pixel의 밝기가 일정 수준 이상 변할 때:

```text
(x, y, timestamp, polarity)
```

형태의 Event를 비동기로 출력합니다.

Event-based Vision Survey:
https://arxiv.org/abs/1904.08405

---

## 4. 사람에게 사진, 컴퓨터에게 숫자

사람은 이미지를 보면 곧바로 "자동차", "사람", "제품" 같은 의미를 떠올립니다.

컴퓨터가 처음 받는 것은 숫자 배열입니다.

예를 들어:

```text
224 × 224 RGB Image

→ 224 × 224 × 3
→ 150,528 channel values
```

Full HD에서는:

```text
1920 × 1080 × 3
= 6,220,800 channel values / frame
```

30 FPS라면:

```text
6,220,800 × 30
= 186,624,000 channel values / second
```

즉 영상 AI는 매초 매우 많은 숫자에서 필요한 정보만 찾아야 합니다.

### Pixel

이미지의 작은 위치 단위입니다.

RGB Pixel 예:

```text
[255, 0, 0]     red
[0, 255, 0]     green
[0, 0, 255]     blue
```

### Channel

한 Pixel에 저장되는 정보 축입니다.

RGB:
```text
R
G
B
→ 3 channels
```

### Tensor

딥러닝에서 데이터를 저장하고 연산하는 다차원 배열입니다.

예:
- Gray image: `[H, W]`
- RGB image: `[H, W, 3]`
- PyTorch image: `[C, H, W]`
- Batch: `[B, C, H, W]`

OpenCV의 이미지/Matrix 설명:
https://docs.opencv.org/4.10.0/d6/d6d/tutorial_mat_the_basic_image_container.html

---

## 5. 왜 Vision은 어려운가?

같은 물체라도 입력 숫자는 쉽게 바뀝니다.

- 조명
- 카메라 각도
- 거리
- 크기
- 회전
- 일부 가림
- Motion Blur
- 반사
- 배경
- 카메라와 Lens

예를 들어 한 Pixel이 밝은 조건에서:

```text
[180, 170, 165]
```

였다가 어두운 조건에서는:

```text
[80, 75, 72]
```

가 될 수 있습니다.

사람은 같은 물체라고 이해하지만 컴퓨터가 받는 숫자는 크게 다릅니다.

---

## 6. Vision AI의 대표 Task

### Classification

"이 이미지가 무엇인가?"

```text
Image
  ↓
Model
  ↓
Normal 97%
Abnormal 3%
```

### Object Detection

"무엇이 어디에 있는가?"

```text
Image
  ↓
Model
  ↓
Class + Bounding Box + Confidence
```

### Segmentation

"정확히 어느 Pixel이 그 물체인가?"

Detection이 대략적인 상자를 찾는다면 Segmentation은 물체의 실제 모양에 가까운 Pixel 영역을 찾습니다.

### Tracking

"이 물체가 시간에 따라 어디로 움직이는가?"

### Depth / 3D

"물체까지 거리는 얼마이고, 공간 구조는 어떤가?"

---

## 7. 그럼 AI는 무엇을 배워야 할까?

Raw Pixel을 그대로 외우는 것이 목표가 아닙니다.

```text
Sensor Data
    ↓
Feature
    ↓
Representation
    ↓
Task Output
```

판단에 필요한 특징을 만드는 과정이 중요합니다.

이제 다음 질문으로 넘어갑니다.

> 수백만 개의 Pixel에서 어떻게 Feature를 찾을까?

대표적인 답이 CNN입니다.

→ [02. CNN](../02_cnn/README.md)
