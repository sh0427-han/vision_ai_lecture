# Vision AI Study & Lecture

Vision AI를 처음 접하는 사람도 **이미지 데이터 → CNN → Vision Transformer → 실제 Vision Task** 순서로 이해할 수 있도록 만든 학습/강의 저장소입니다.

이 저장소는 세 가지를 함께 목표로 합니다.

1. **학습 노트** — 개념과 용어를 쉬운 말과 수치 예제로 정리
2. **강의 자료** — 그림과 흐름 중심으로 설명 가능한 콘텐츠
3. **실습 자료** — Notebook과 웹 데모로 개념을 직접 확인

## 학습 순서

```text
01. Vision AI 입문
        ↓
02. CNN
        ↓
03. Vision Transformer
        ↓
Classification / Detection / Segmentation
        ↓
Dataset / Training / Evaluation
        ↓
Industrial Vision AI
```

| 순서 | 챕터 | 핵심 질문 |
|---|---|---|
| 1 | [Vision AI 입문](lectures/01_intro/README.md) | 컴퓨터에게 이미지는 무엇인가? |
| 2 | [CNN](lectures/02_cnn/README.md) | 작은 필터로 어떻게 특징을 찾는가? |
| 3 | [Vision Transformer](lectures/03_vision_transformer/README.md) | 이미지를 왜 Patch와 Token으로 바꾸는가? |
| 4 | [용어집](GLOSSARY.md) | 낯선 용어는 정확히 무슨 뜻인가? |
| 5 | [논문 읽기 가이드](papers/README.md) | 어떤 논문을 어떤 순서로 읽을 것인가? |

## CNN과 ViT 한눈에 보기

![CNN vs ViT](assets/diagrams/cnn_vs_vit.svg)

- **CNN**: 작은 영역(Local)을 반복해서 관찰하면서 점점 넓은 특징을 만듭니다.
- **Vision Transformer**: 이미지를 Patch로 나눈 뒤 각 Patch 사이의 관계를 Self-Attention으로 학습합니다.

둘 중 하나가 항상 우월한 것은 아닙니다. 데이터 규모, 해상도, 연산량, 문제 특성에 따라 선택이 달라집니다.

## 저장소 구조

```text
vision_ai/
├── README.md
├── GLOSSARY.md
├── lectures/
│   ├── 01_intro/
│   ├── 02_cnn/
│   └── 03_vision_transformer/
├── papers/
├── assets/
│   ├── diagrams/
│   └── SOURCES.md
├── notebooks/
├── demos/
└── docs/
```

## 작성 원칙

- 수식보다 먼저 **입력 → 처리 → 출력** 흐름을 설명합니다.
- 핵심 개념에는 가능한 한 **숫자 예시**를 붙입니다.
- 논문 Figure를 그대로 복사하기보다 **직접 다시 그린 도식**을 우선 사용합니다.
- 논문에 기반한 설명에는 원 논문 링크를 남깁니다.
- 교육적 비유와 엄밀한 정의를 구분합니다.
- 처음 접하는 용어는 [GLOSSARY.md](GLOSSARY.md)에서 다시 확인할 수 있습니다.

## Web Lecture

정적 강의 사이트 초안은 [docs/index.html](docs/index.html)에 있습니다.  
디자인은 **흰색 배경, 짙은 본문, 최소한의 포인트 컬러**를 기본으로 합니다.
