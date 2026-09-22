# Vision AI Study & Lecture

## 🌐 배포 사이트

강의용 웹 슬라이드는 아래 GitHub Pages에서 바로 확인할 수 있습니다.

**https://sh0427-han.github.io/vision_ai/**



Vision AI를 처음 접하는 사람도 **현실 세계 → Sensor → 숫자 데이터 → AI 학습 → CNN** 순서로 이해할 수 있도록 만든 완전 기초 강의 자료입니다.

이 저장소는 세 가지를 함께 목표로 합니다.

1. **학습 노트** — 개념을 쉬운 말과 수치 예제로 정리
2. **강의 자료** — 한 슬라이드에 한 메시지, 그림과 비교 중심으로 설명
3. **실습 자료** — Notebook과 웹 데모로 개념을 직접 확인

## 학습 순서

```text
01. Vision AI 입문
        ↓
02. AI 기초
   - Weight / Parameter
   - 비선형성 / Activation
   - Loss / Backpropagation
   - Dataset / Train-Val-Test
        ↓
03. CNN
   - 사람이 특징을 보고 사물을 판단하는 직관
   - Kernel / Convolution
   - Feature Map / Channel
   - Receptive Field
   - VGG / ResNet
        ↓
Classification / Detection / Segmentation / Tracking / 3D
        ↓
실제 Vision AI 개발과 운영
```

| 순서 | 챕터 | 핵심 질문 |
|---|---|---|
| 1 | [Vision AI 입문](lectures/01_intro/README.md) | 컴퓨터는 현실 세계를 어떤 데이터로 보는가? |
| 2 | [AI 기초](lectures/02_ai_basics/README.md) | 신경망은 왜 비선형성이 필요하고 어떻게 학습하는가? |
| 3 | [CNN](lectures/03_cnn/README.md) | 작은 특징들을 어떻게 조합해 사물을 인식하는가? |

## 설명 방식

별도 용어집을 외우게 하지 않습니다. 각 챕터에서 처음 등장하는 용어를 바로 설명합니다.

```text
CNN
 ├─ 사람이 특징을 보고 판단한다는 직관
 ├─ Kernel이란?
 ├─ Convolution이란?
 ├─ Feature Map이란?
 ├─ Channel이란?
 └─ Receptive Field란?
```

## CNN을 이해하는 핵심 직관

사람은 사물을 볼 때 단순히 모든 Pixel 값을 통째로 비교하지 않습니다.

예를 들어 사과를 볼 때:

```text
색
+ 둥근 형태
+ 꼭지
+ 표면 질감
        ↓
"사과 같다"
```

라고 여러 특징을 종합해 판단합니다.

CNN도 교육적인 관점에서는 비슷하게 이해할 수 있습니다.

```text
Pixel
 ↓
Edge / Texture
 ↓
Shape
 ↓
Object Part
 ↓
Object-level Feature
```

단, 이 비유는 이해를 돕기 위한 것이며 **인간의 시각 처리 메커니즘과 CNN의 계산 구조가 실제로 동일하다는 뜻은 아닙니다.**

## 저장소 구조

```text
vision_ai/
├── README.md
├── lectures/
│   ├── 01_intro/
│   ├── 02_ai_basics/
│   └── 03_cnn/
├── assets/
│   ├── diagrams/
│   └── SOURCES.md
├── notebooks/
├── demos/
└── docs/
```

## 작성 원칙

- 수식보다 먼저 **입력 → 처리 → 출력** 흐름을 설명합니다.
- 핵심 개념에는 가능한 한 **수치 예시**를 붙입니다.
- 용어는 별도 목록보다 **실제 맥락 안에서 바로 설명**합니다.
- 인간의 직관과 비교할 때는 교육적 비유와 실제 메커니즘을 구분합니다.
- 모델 구조뿐 아니라 **Dataset, 평가, 운영 환경**까지 함께 설명합니다.

## Web Lecture

정적 강의 사이트는 [docs/index.html](docs/index.html)에 있습니다.

디자인은 **흰색 배경, 한 화면 한 슬라이드, 최소한의 포인트 컬러**를 기본으로 합니다.
