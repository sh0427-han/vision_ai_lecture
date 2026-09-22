# 02. AI 기초 — 신경망은 어떻게 학습하는가?

CNN이나 Vision Transformer의 구조를 보기 전에, 딥러닝 모델이 **왜 여러 Layer를 사용하고, 무엇을 학습하며, Dataset이 왜 중요한지** 먼저 이해합니다.

## 학습 목표

이 챕터가 끝나면 다음을 설명할 수 있어야 합니다.

1. Model, Parameter, Weight가 무엇인가?
2. 선형 변환만 여러 층 쌓으면 왜 한계가 있는가?
3. ReLU 같은 Activation Function은 왜 필요한가?
4. Forward, Loss, Backpropagation, Optimizer는 어떤 순서로 동작하는가?
5. Dataset이 모델 성능에 왜 큰 영향을 주는가?
6. Train / Validation / Test는 왜 분리하는가?
7. Overfitting과 Data Leakage는 무엇인가?

---

## 1. AI 모델은 결국 함수다

아주 단순화하면 모델은 입력 숫자를 받아 다른 숫자로 바꾸는 함수입니다.

```text
Input x
  ↓
Model f(x; θ)
  ↓
Prediction y_hat
```

여기서 θ는 모델이 학습하는 값들입니다.

### Parameter / Weight

**Parameter**는 학습 과정에서 값이 바뀌는 숫자입니다.  
그중 가장 대표적인 것이 **Weight(가중치)** 입니다.

예를 들어:

```text
y = wx + b
```

에서 w와 b가 학습 대상입니다.

- w: 입력을 얼마나 크게 반영할지
- b: 전체 출력을 얼마나 이동시킬지

딥러닝 모델에는 이런 Parameter가 매우 많이 존재합니다.

---

## 2. Linear Layer는 무엇을 하는가?

신경망의 기본 연산 중 하나는 다음과 같은 **아핀 변환(Affine Transformation)** 입니다.

```text
y = Wx + b
```

딥러닝에서는 흔히 편의상 Linear Layer라고 부르지만, Bias b까지 포함하면 수학적으로는 Affine Transformation입니다.

Weight Matrix W가 여러 입력을 섞어 새로운 Feature를 만듭니다.

---

## 3. 왜 비선형성이 필요한가?

여기가 신경망을 이해하는 핵심입니다.

Linear/Affine Layer를 여러 개 쌓아보겠습니다.

```text
x
 ↓
W1x + b1
 ↓
W2x + b2
 ↓
W3x + b3
```

중간에 다른 연산이 없다면 전체 식은 결국:

```text
y = W'x + b'
```

형태의 **하나의 Affine Transformation으로 합쳐질 수 있습니다.**

즉 Layer를 3개, 30개 쌓더라도 표현 가능한 관계가 본질적으로 크게 늘지 않습니다.

![Linear vs Nonlinear](../../assets/diagrams/linear_vs_nonlinear.svg)

현실의 이미지 문제는 밝기, 형태, Texture, 배경, 시점, 물체 간 관계처럼 복잡한 요인이 섞여 있습니다.

그래서 Layer 사이에 **Activation Function(활성화 함수)** 을 넣어 비선형성을 부여합니다.

---

## 4. Activation Function

Activation Function은 Layer의 출력에 비선형 변환을 추가합니다.

대표적인 예가 **ReLU**입니다.

```text
ReLU(x) = max(0, x)

Input : [-2, -0.5, 0, 1, 3]
ReLU  : [ 0,  0,   0, 1, 3]
```

구조는 다음처럼 됩니다.

```text
Linear
  ↓
ReLU
  ↓
Linear
  ↓
ReLU
  ↓
Linear
```

이렇게 비선형 함수가 들어가면 여러 Layer를 쌓는 것이 의미를 갖게 됩니다.

현대 모델에서는 ReLU 외에도 GELU, SiLU 등 다양한 Activation Function을 사용합니다.

---

## 5. Feature와 Representation

모델이 입력을 그대로 외우는 것이 목표는 아닙니다.

모델 내부에서는 입력을 문제 해결에 더 유용한 표현으로 계속 바꿉니다.

- **Feature**: 문제를 푸는 데 유용한 특징
- **Representation**: 입력을 모델 내부에서 표현한 숫자 형태

교육적으로 이미지에서는 다음 흐름을 생각할 수 있습니다.

```text
Raw Pixel
   ↓
Edge / Texture
   ↓
Shape
   ↓
Object Part
   ↓
Task에 유용한 Feature
```

실제 모델의 내부 Feature가 사람이 이름 붙일 수 있는 단일 의미로 정확히 분리되는 것은 아닙니다.

---

## 6. 그럼 "학습"은 정확히 무엇인가?

학습은 모델이 정답에 더 가까운 출력을 만들도록 Parameter를 반복해서 수정하는 과정입니다.

![Training Loop](../../assets/diagrams/training_loop.svg)

전체 흐름:

```text
Input + Label
      ↓
Forward
      ↓
Prediction
      ↓
Loss
      ↓
Backward
      ↓
Gradient
      ↓
Optimizer
      ↓
Weight Update
      ↓
반복
```

### Forward
현재 Weight를 사용해 입력에서 예측값을 계산하는 과정입니다.

### Label
학습 데이터에 붙어 있는 정답입니다.

### Loss
모델 예측과 정답 사이의 차이를 하나의 숫자로 표현한 값입니다. 학습은 보통 이 Loss를 작게 만드는 방향으로 진행됩니다.

---

## 7. Backpropagation과 Gradient

**Gradient**는 어떤 Parameter를 조금 바꿨을 때 Loss가 어느 방향으로 얼마나 변하는지를 나타냅니다.

**Backpropagation**은 Loss에서 출발해 네트워크 뒤에서 앞으로 이동하며 각 Parameter의 Gradient를 계산하는 과정입니다.

**Optimizer**는 Gradient를 이용해 실제 Weight를 수정하는 알고리즘입니다.

가장 단순한 형태:

```text
new_weight
=
old_weight - learning_rate × gradient
```

SGD, Adam, AdamW 등이 대표적인 Optimizer입니다.

---

## 8. Learning Rate, Batch, Epoch

### Learning Rate
Weight를 한 번에 얼마나 크게 바꿀지 결정합니다. 너무 크면 학습이 불안정할 수 있고, 너무 작으면 매우 느릴 수 있습니다.

### Batch
한 번의 Forward/Backward에 함께 사용하는 샘플 묶음입니다.

예:

```text
batch_size = 32
```

### Epoch
Train Dataset 전체를 한 번 모두 사용한 것을 1 Epoch라고 합니다.

예를 들어 10,000장과 batch_size=32라면, 마지막 Batch 처리 방식에 따라 약 313 Step이 1 Epoch가 됩니다.

---

## 9. Dataset은 모델이 배우는 세상이다

모델은 우리가 준 Dataset에서 패턴을 배웁니다.

![Dataset Split](../../assets/diagrams/dataset_split.svg)

Dataset에는 다음이 중요합니다.

- 실제 운영 환경을 충분히 대표하는가?
- Label 기준이 정확하고 일관적인가?
- 중요한 희귀 Class가 포함되어 있는가?
- 특정 장비/배경/날짜에 과도하게 치우치지 않았는가?
- Train과 Test 사이에 같은 원본 정보가 새어 들어가지 않았는가?

```text
좋은 Architecture
+
잘못된 Label
+
편향된 Dataset
=
신뢰하기 어려운 Model
```

문제가 잘 정의되고 Dataset이 충분히 대표적이라면 상대적으로 단순한 모델도 강력할 수 있습니다.

---

## 10. Train / Validation / Test

### Train
실제로 Weight를 학습하는 데이터입니다.

### Validation
학습 도중 모델 선택, Hyperparameter 조정, Early Stopping 등에 사용하는 데이터입니다.

### Test
최종 모델의 일반화 성능을 평가하기 위한 데이터입니다. 가능하면 최종 평가 전까지 반복적으로 보고 의사결정에 사용하지 않는 것이 좋습니다.

예:

```text
Train 70%
Validation 15%
Test 15%
```

이 비율은 예시일 뿐이고 데이터 규모와 문제 특성에 따라 달라질 수 있습니다.

---

## 11. Data Leakage

**Data Leakage**는 모델이 평가 시점에는 알면 안 되는 정보가 Train 과정에 흘러 들어가는 문제입니다.

예를 들어 하나의 영상에서 나온 연속 Frame을 무작위로 나누면:

```text
Train: frame_001
Test : frame_002
```

처럼 거의 동일한 장면이 Train과 Test에 동시에 들어갈 수 있습니다.

그러면 Test 성능이 실제 새로운 영상에 대한 성능보다 좋아 보일 수 있습니다.

Vision 문제에서는 원본 Video, Lot, Patient, Product, Equipment, 촬영 Session 등 실제 독립 단위를 기준으로 Split해야 할 수 있습니다.

---

## 12. Overfitting과 Underfitting

### Underfitting
Train 데이터조차 충분히 설명하지 못하는 상태입니다.

```text
Train 성능 낮음
Val 성능 낮음
```

### Overfitting
Train 데이터에는 매우 잘 맞지만 새로운 데이터에서 성능이 떨어지는 상태입니다.

```text
Train 성능 매우 높음
Val/Test 성능 상대적으로 낮음
```

---

## 13. Data Augmentation

Train Image를 일부 변형해 다양한 조건을 경험하게 만드는 방법입니다.

예:

- Flip
- Crop
- Rotation
- Brightness / Contrast
- Blur
- Noise

실제 현장에서 발생할 수 있는 변화와 Task의 의미를 깨뜨리지 않는 범위에서 설계해야 합니다.

---

## 14. 이 모든 것이 CNN과 어떤 관계가 있는가?

이제 CNN을 다음 구조로 볼 수 있습니다.

```text
Image Tensor
    ↓
Convolution
    ↓
Activation Function
    ↓
Feature
    ↓
Convolution
    ↓
Activation Function
    ↓
더 복잡한 Feature
    ↓
Prediction
```

CNN 내부의 Kernel Weight는 사람이 직접 정하는 것이 아니라:

```text
Forward
→ Loss
→ Backpropagation
→ Optimizer
```

과정을 통해 Dataset으로부터 학습됩니다.

## 핵심 정리

```text
Dataset
   ↓
Forward
   ↓
Loss
   ↓
Backpropagation
   ↓
Weight Update
   ↓
Feature Learning
```

그리고 여러 Layer가 복잡한 관계를 표현할 수 있도록:

```text
Linear / Conv
    +
Activation Function
    =
Nonlinear Neural Network
```

를 사용합니다.

→ [03. CNN](../03_cnn/README.md)
