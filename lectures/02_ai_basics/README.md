# 02. AI Basics

Vision AI를 처음 배우는 사람이 **Model이 어떻게 계산하고, 어떻게 학습하고, 어떻게 평가되는지** 하나의 흐름으로 이해하도록 구성합니다.

## 강의 흐름

### A. AI가 무엇을 해결하는가
1. AI / Machine Learning / Deep Learning / Computer Vision 관계
2. Rule-based vs Machine Learning
3. Supervised Learning / Unsupervised Learning
4. Classification / Regression
5. Binary / Multi-class Classification

### B. Model은 어떻게 계산하는가
6. Perceptron: 가장 단순한 Neural 계산
7. Weight / Bias 직관
8. Parameter / Hyperparameter
9. AND / XOR와 Linear Separability
10. Perceptron → Layer → Neural Network
11. Linear Layer만 쌓았을 때의 한계
12. Activation Function / ReLU
13. Feature / Representation

### C. Model은 어떻게 학습하는가
14. Linear Regression으로 보는 Parameter 학습
15. Loss Function
16. Gradient
17. Optimizer / Learning Rate
18. Training Loop: Forward → Loss → Backward → Update
19. Backpropagation
20. Training vs Inference
21. Batch / Iteration / Epoch

### D. 좋은 학습 데이터를 어떻게 준비하는가
22. Dataset Quality
23. Image Preprocessing
24. Data Augmentation
25. Train / Validation / Test

### E. 진짜 잘하는 Model인지 어떻게 평가하는가
26. Threshold / Confusion Matrix
27. Accuracy / Precision / Recall / F1
28. Data Leakage
29. Group Split
30. K-Fold / Group K-Fold
31. Generalization / Overfitting
32. AI Development Cycle

## 꼭 이해해야 할 연결

### Perceptron → Weight / Bias

Perceptron은 입력 Feature에 Weight를 곱해 더하고 Bias와 Activation을 적용해 Output을 만듭니다.

- **Weight**: 각 입력을 얼마나 중요하게 볼지 결정
- **Bias**: 판단 기준의 위치를 조절
- **Parameter**: Training이 데이터에서 찾는 Weight와 Bias 같은 값

여기서 Bias Parameter는 Dataset이 한쪽으로 치우쳤다는 의미의 Data Bias와 다른 개념입니다.

### Perceptron → Neural Network

Perceptron 여러 개를 같은 단계에 모으면 Layer가 되고, Layer를 여러 단계 연결하면 Neural Network가 됩니다.

Activation이 없는 Linear Layer 여러 개는 결국 하나의 Linear Transformation으로 합쳐질 수 있습니다. ReLU 같은 비선형 Activation이 있어야 XOR처럼 단순한 직선으로 나눌 수 없는 Pattern을 표현할 수 있습니다.

### Feature / Representation

Network는 Pixel을 그대로 외우는 것이 아니라 학습을 통해 판단에 유용한 내부 숫자 표현을 만듭니다.

```text
Pixel
 → Edge / Color Change
 → Part / Shape
 → Internal Representation
 → Prediction
```

### Loss → Gradient → Optimizer

- **Loss**: 현재 Prediction이 Target에서 얼마나 벗어났는지 나타내는 학습용 숫자
- **Gradient**: Parameter를 움직였을 때 Loss가 어느 방향으로 변하는지 알려주는 정보
- **Optimizer**: Gradient를 이용해 Parameter를 실제로 Update
- **Learning Rate**: 한 번에 얼마나 크게 Update할지 정하는 값

```text
Prediction
   ↓
Loss
   ↓
Gradient
   ↓
Optimizer
   ↓
Parameter Update
```

### Training Loop

한 Batch마다 다음 과정이 반복됩니다.

```text
① Forward
Image → Model → Prediction
        ↓
② Loss
Prediction ↔ Target
        ↓
③ Backward
Gradient 계산
        ↓
④ Update
Weight 수정
        ↺ 다음 Batch
```

### Backpropagation

Backpropagation은 최종 Loss에 각 Weight가 얼마나 영향을 주었는지를 뒤쪽 Layer부터 앞쪽 Layer 방향으로 계산하는 과정입니다. 수학적으로는 Chain Rule을 사용하지만 입문 단계에서는 **“Loss의 책임을 뒤에서부터 나누어 계산한다”**고 이해하면 충분합니다.

### Training vs Inference

Training은 Label과 Loss를 이용해 Weight를 바꾸지만, Inference는 학습된 Weight를 고정하고 Prediction만 계산합니다.

### Dataset / Evaluation

- Train: Weight 학습
- Validation: Model / Hyperparameter / Threshold 선택
- Test: 마지막 Generalization 평가
- 같은 원본 영상이나 강하게 연관된 Sample은 Group 단위로 Split
- Test 결과를 보면서 반복해서 Model을 고르면 Test가 더 이상 공정한 최종 평가셋이 아니게 됨

### Loss와 Metric

- **Loss**: Training 중 Weight를 Update하기 위해 최적화하는 값
- **Metric**: Model 성능을 사람이 해석하고 비교하기 위한 값

### 최종 목표

좋은 AI Model은 Train Dataset을 잘 외우는 Model이 아니라, **보지 못한 새로운 조건에서도 필요한 Pattern을 이용해 올바르게 판단하는 Model**입니다.

```text
Data
 ↓
Train
 ↓
Evaluate
 ↓
Deploy / Inference
 ↓
Monitor
 ↓
실패 사례 수집
 └────────→ 다음 Data / Retraining
```
