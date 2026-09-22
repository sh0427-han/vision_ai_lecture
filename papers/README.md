# Vision AI 논문 읽기 가이드

처음부터 최신 SOTA 논문을 따라가기보다, **CNN이 어떻게 발전했고 Vision Transformer가 왜 등장했는지**를 순서대로 이해하는 것을 목표로 합니다.

## 추천 순서

```text
Convolution Arithmetic
        ↓
AlexNet
        ↓
VGG
        ↓
ResNet
        ↓
 ┌──────┴──────┐
 ↓             ↓
YOLO          U-Net
Detection     Segmentation
        ↓
Vision Transformer
```

## 1. A guide to convolution arithmetic for deep learning

- Dumoulin & Visin
- https://arxiv.org/abs/1603.07285

### 왜 읽는가?
Kernel, Stride, Padding, Transposed Convolution이 공간 크기에 어떤 영향을 주는지 그림으로 이해하기 좋습니다.

### 집중해서 볼 것
- Convolution 출력 크기
- Padding
- Stride
- Transposed Convolution

---

## 2. AlexNet

**ImageNet Classification with Deep Convolutional Neural Networks**

- Krizhevsky, Sutskever, Hinton
- NeurIPS 2012
- https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html

### 왜 읽는가?
현대 Deep CNN 붐을 이해하기 위한 대표적인 출발점입니다.

### 집중해서 볼 것
- Convolution + ReLU + Pooling
- GPU 학습
- 데이터 증강

---

## 3. VGG

**Very Deep Convolutional Networks for Large-Scale Image Recognition**

- Simonyan & Zisserman
- https://arxiv.org/abs/1409.1556

### 핵심
작은 `3×3 Conv`를 반복적으로 쌓아 깊은 네트워크를 구성합니다.

---

## 4. ResNet

**Deep Residual Learning for Image Recognition**

- He et al.
- CVPR 2016
- https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html

### 핵심
`y = F(x) + x` 형태의 Residual Connection으로 매우 깊은 네트워크의 학습을 쉽게 합니다.

---

## 5. YOLO

**You Only Look Once: Unified, Real-Time Object Detection**

- Redmon et al.
- CVPR 2016
- https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html

### 핵심
이미지에서 Bounding Box와 Class를 하나의 네트워크로 직접 예측하는 One-Stage Detection 관점을 이해하기 좋습니다.

---

## 6. U-Net

**U-Net: Convolutional Networks for Biomedical Image Segmentation**

- Ronneberger et al.
- https://arxiv.org/abs/1505.04597

### 핵심
Encoder-Decoder와 Skip Connection을 이용해 Semantic 정보와 세밀한 위치 정보를 함께 사용합니다.

---

## 7. Vision Transformer

**An Image is Worth 16×16 Words: Transformers for Image Recognition at Scale**

- Dosovitskiy et al.
- ICLR 2021
- https://openreview.net/forum?id=YicbFdNTTy
- https://arxiv.org/abs/2010.11929

### 처음 볼 때 집중할 것
1. Figure 1
2. Patch Embedding
3. Position Embedding
4. CLS Token
5. Transformer Encoder
6. 대규모 Pre-training의 의미

### 처음에는 넘어가도 되는 것
- 모든 실험 Table
- 세부 Hyperparameter
- 모든 Ablation Study

먼저 구조를 이해하고 두 번째 읽기에서 실험을 보는 것이 좋습니다.

## 논문 읽는 질문 4개

각 논문에서 아래 네 가지만 먼저 답해봅니다.

1. 이전 방법의 문제는 무엇인가?
2. 이 논문이 바꾼 핵심 아이디어는 무엇인가?
3. 입력과 출력은 무엇인가?
4. 이후 모델에 어떤 영향을 주었는가?
