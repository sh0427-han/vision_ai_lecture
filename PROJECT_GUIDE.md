# Vision AI Lecture — Project Guide

Vision AI를 처음 접하는 사람을 대상으로 하는 입문 강의자료 제작 프로젝트입니다.

## Links

- GitHub Repository: https://github.com/sh0427-han/vision_ai_lecture
- GitHub Pages: https://sh0427-han.github.io/vision_ai_lecture/

## Course Structure

### 01. Vision AI Intro

- 사람과 컴퓨터가 이미지를 보는 방식의 차이
- RGB 3D Tensor → Pixel / Channel의 의미와 8-bit 0~255 값
- Signal / Noise: 판단에 유용한 Pattern과 무관한 변화의 차이
- 조명, 방향, 크기, 가림, 초점, 색온도 등에 따른 Pixel 변화
- Generalization: 조건이 달라도 반복되는 공통 Pattern 학습
- RGB 입력 → Feature → Classification / Detection / Segmentation Output
- 대표 Vision Sensor: RGB / LiDAR / IR의 출력 데이터와 스마트폰·로봇청소기·열화상 등 친숙한 활용 예

### 02. AI Basics

- AI / Machine Learning / Deep Learning / Computer Vision의 관계
- Supervised Learning / Unsupervised Learning
- Classification / Regression
- Binary / Multi-class Classification
- Linear Regression
- Loss Function / Gradient / Optimizer
- Parameter / Hyperparameter
- Perceptron
- AND / XOR
- 비선형성과 Activation Function
- Backpropagation
- Training / Inference
- Batch / Iteration / Epoch
- Image Preprocessing
- Data Augmentation
- Train / Validation / Test
- Data Leakage와 Group 단위 Split
- K-Fold / Group K-Fold
- Threshold / Confusion Matrix / Precision / Recall / F1
- Overfitting / Generalization

### 03. Vision AI

- 현장 문제 → 원하는 Output → Task → Label → Model
- Classification
- Object Detection
- Segmentation
- Task별 Label 구조
- CNN
- Kernel / Convolution
- Stride / Padding / Downsampling
- Feature Map / Channel
- Feature Hierarchy
- Receptive Field
- CNN Training
- Backbone / Task Head
- Transfer Learning / Fine-tuning

현재 강의 범위에서는 Tracking, Depth/3D, Vision Transformer를 제외합니다.

## Lecture Design Principles

대상은 Vision AI를 처음 접하는 초보자입니다.

- 한 슬라이드에는 하나의 핵심 메시지만 전달합니다.
- 긴 텍스트 설명보다 그림과 예시를 우선합니다.
- 가능하면 슬라이드의 60~75%를 시각 자료로 구성합니다.
- 텍스트와 화살표 문자만으로 만든 흐름 표현은 최소화합니다.
- Process와 학습 과정은 실제 Flow Chart / Block Diagram으로 표현합니다.
- 같은 원본 이미지를 반복 활용해 Classification / Detection / Segmentation의 차이를 직관적으로 보여줍니다.
- 논문 Figure나 외부 이미지를 그대로 복사하기보다 강의용 Diagram으로 재구성합니다.
- 실제 강의 화면에는 강사용 메모, 발표 지시, 다음 챕터 안내 같은 메타 문구를 넣지 않습니다.
- 흰색 배경, 최소한의 색상, 깔끔한 Presentation 스타일을 유지합니다.
- 초보자가 그림만 보고도 개념의 대략적인 의미를 이해할 수 있도록 구성합니다.

## Repository Structure

주요 웹 강의 파일:

- `docs/intro.html`
- `docs/ai_basics.html`
- `docs/vision_ai.html`

강의용 Diagram:

- `docs/assets/`
- `assets/diagrams/`

학습 노트:

- `lectures/01_intro/`
- `lectures/02_ai_basics/`
- `lectures/03_vision_ai/`

시각 자료 출처:

- `assets/SOURCES.md`

## Working Rules

- 수정 전에 Repository의 최신 상태를 확인합니다.
- 사용자가 강의자료 수정을 요청하면 가능한 경우 실제 Repository 파일까지 수정합니다.
- 수정 후 HTML 구조와 링크를 검증하고 GitHub Pages 배포 상태를 확인합니다.
- 기존 강의 흐름과 디자인을 유지하면서 내용을 추가합니다.
- 중복되는 설명은 제거합니다.
- 완전 초보자 관점에서 용어를 설명합니다.
- 그림, Diagram, Flow Chart를 우선 사용합니다.
- 강의자료와 학습노트의 내용이 서로 크게 어긋나지 않도록 함께 관리합니다.

## Current Entry Point

강의는 다음 파일에서 시작합니다.

- `docs/intro.html`

GitHub Pages:

- https://sh0427-han.github.io/vision_ai_lecture/
