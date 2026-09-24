# 02. AI Basics

Vision AI를 이해하기 전에 필요한 AI / Machine Learning / Deep Learning의 최소 공통 개념을 다룹니다.  
목표는 수식을 외우는 것이 아니라 **Data → Training → Evaluation → Inference** 흐름을 이해하는 것입니다.

## 슬라이드 흐름

1. AI / Machine Learning / Deep Learning / Computer Vision 관계
2. Rule-based vs Machine Learning
3. Supervised Learning / Unsupervised Learning
4. Classification / Regression
5. Binary / Multi-class Classification
6. Model / Parameter / Hyperparameter
7. Linear Regression
8. Loss Function
9. Gradient / Optimizer / Learning Rate
10. Perceptron으로 보는 가장 단순한 Neural 계산
11. AND / XOR와 Linear Separability
12. Linear Layer를 여러 개 쌓아도 Activation이 없으면 하나의 Linear 변환
13. Activation Function / ReLU / Non-linearity
14. Feature / Representation
15. Prediction → Loss → Gradient → Parameter Update
16. Backpropagation
17. Training vs Inference
18. Batch / Iteration / Epoch
19. Dataset Quality
20. Image Preprocessing
21. Data Augmentation
22. Train / Validation / Test
23. Threshold / Confusion Matrix
24. Accuracy / Precision / Recall / F1
25. Data Leakage
26. Group Split
27. K-Fold / Group K-Fold
28. Generalization / Overfitting
29. AI Development Cycle

## 핵심 개념

## 지도학습과 비지도학습

- **Supervised Learning**: Input과 Target Label의 관계를 학습해 새로운 Input의 Target을 예측
- **Unsupervised Learning**: Target Label 없이 데이터의 Cluster, Structure, Representation을 탐색

강의 Figure는 논문에서 자주 사용하는 **Feature Space scatter plot** 형태로 두 학습 방식을 비교합니다.

## Classification과 Regression

- **Classification**: 유한한 Class 중 하나를 예측하는 문제
- **Regression**: 연속적인 실수 값을 예측하는 문제

강의 Figure는 Classification의 **Decision Boundary**와 Regression의 **Fitted Function**을 같은 좌표계 스타일로 비교합니다.


### Parameter와 Hyperparameter

- **Parameter**: Weight, Bias처럼 Training 과정에서 Gradient에 의해 수정되는 값
- **Hyperparameter**: Learning Rate, Batch Size, Epoch, Layer 수처럼 학습 동작을 정하는 설정값

### Loss와 Optimizer

Loss는 Prediction이 Target과 얼마나 다른지를 학습에 사용할 수 있는 숫자로 만듭니다.  
Gradient는 Parameter를 바꿨을 때 Loss가 어떻게 변하는지 알려주고, Optimizer는 Gradient의 반대 방향으로 Parameter를 업데이트합니다.

```text
Prediction → Loss → Gradient → Parameter Update → 다음 Prediction
```

### 왜 Activation Function이 필요한가

AND는 직선 하나로 Class를 나눌 수 있지만 XOR는 그렇지 않습니다.  
Activation이 없는 Linear Layer 여러 개는 결국 하나의 Linear 변환으로 합쳐집니다.  
ReLU 같은 비선형 Activation이 들어가야 더 복잡한 Decision Boundary를 표현할 수 있습니다.

### Training과 Inference

```text
Training
Image + Label → Model → Prediction → Loss → Backward → Weight Update

Inference
New Image → Trained Model → Prediction
```

Inference에는 Label, Backward, Weight Update가 없습니다.

### Dataset Quality

Dataset은 실제 운영 환경을 대표해야 합니다.

- **Coverage**: 조명, 크기, 배경, 설비, 시간대 등 다양한 운영 조건
- **Label Quality**: 정확하고 일관된 정답 기준
- **Class Balance**: 희귀 Class도 학습·평가 가능한 수량 확보
- **Bias Check**: Train 분포와 실제 운영 분포 차이 확인

### Image Preprocessing

카메라 이미지는 Model이 기대하는 입력 형식으로 변환합니다.

```text
Camera Image → Resize → Scale / Normalize → Tensor → Model
```

Tensor 축 순서는 Framework마다 다를 수 있습니다. 예를 들어 PyTorch에서는 `[B, C, H, W]` 형태가 흔합니다.  
Train과 Inference에는 같은 기본 전처리 규칙을 적용해야 합니다.

### Data Augmentation

밝기, 회전, 크기, Crop, Blur 등 현실에서 의미가 유지되는 변화를 학습 데이터에 적용합니다.  
목적은 단순히 이미지 수를 늘리는 것이 아니라 중요하지 않은 변화에 덜 민감한 모델을 만드는 것입니다.

Detection / Segmentation에서는 Image를 변환할 때 Box / Mask Label에도 같은 기하 변환을 적용해야 합니다.

### Train / Validation / Test

- **Train**: Weight 학습
- **Validation**: Model / Hyperparameter / Threshold 선택
- **Test**: 가능한 마지막까지 보지 않고 최종 Generalization 평가

### Threshold와 Confusion Matrix

Score를 실제 판정으로 바꾸려면 Threshold가 필요할 수 있습니다.

- **TP**: 실제 Positive를 Positive로 판정
- **FN**: 실제 Positive를 놓침
- **FP**: 실제 Negative를 Positive로 잘못 판정
- **TN**: 실제 Negative를 Negative로 판정

### Classification Metric

- **Accuracy**: 전체 Sample 중 맞춘 비율
- **Precision**: Positive라고 판정한 것 중 실제 Positive 비율
- **Recall**: 실제 Positive 중 찾아낸 비율
- **F1**: Precision과 Recall의 조화 평균

**Loss는 Weight를 학습할 때 최적화하는 값**, **Metric은 성능을 평가·비교하는 값**이라는 차이를 구분합니다.

### Data Leakage

대표적인 Leakage:

- 같은 원본 영상의 인접 Frame이 Train과 Validation/Test에 나뉨
- 전체 Dataset을 이용해 Normalization / Feature 통계를 계산
- Test 결과를 보며 Model / Threshold / Hyperparameter를 반복 선택

### Group Split

Frame 수가 많아도 같은 원본에서 나온 Sample은 독립적이지 않을 수 있습니다.  
영상·설비·대상·환자·제품·날짜처럼 상관관계가 강한 단위를 **Group 전체로 Train / Val / Test 중 하나에만 배정**하는 것이 안전합니다.

### K-Fold Cross Validation

K개 Fold를 만들고 Validation Fold를 바꿔가며 K번 Training합니다.  
같은 Metric의 평균뿐 아니라 Fold 간 변동도 확인합니다.

Group 상관관계가 강하면 일반 K-Fold보다 Group K-Fold가 적절할 수 있습니다.  
최종 Test Set은 Cross Validation 바깥에 별도로 유지하는 것이 일반적입니다.

### Generalization / Overfitting

목표는 Train Dataset을 잘 외우는 것이 아니라 **보지 못한 새로운 데이터에서도 성능이 유지되는 것**입니다.  
Train Loss는 계속 낮아지는데 Validation Loss가 다시 증가하면 Overfitting을 의심할 수 있습니다.

## 최종 흐름

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

운영에서 발생한 실패 사례를 다음 Dataset과 Training에 반영하는 반복 Cycle이 실제 AI 개발의 핵심입니다.
