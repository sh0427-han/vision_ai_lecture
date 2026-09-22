# Vision AI 용어집

처음 Vision AI를 공부할 때 자주 만나는 용어를 쉬운 설명과 함께 정리합니다.

## Image / Tensor

### Pixel
이미지를 구성하는 가장 작은 단위입니다. RGB 이미지에서는 한 Pixel이 보통 R, G, B 세 값으로 표현됩니다.

예: `[255, 0, 0]`은 강한 빨강을 의미합니다.

### Channel
이미지의 정보 축입니다. RGB 이미지는 보통 3개 Channel을 가집니다.

```text
224 × 224 × 3
            ↑
         RGB 3채널
```

### Resolution
이미지의 가로×세로 Pixel 수입니다. 예: `1920×1080`.

### Tensor
딥러닝에서 데이터를 담는 다차원 배열입니다.

예:
- Gray image: `[H, W]`
- RGB image: `[H, W, 3]`
- PyTorch batch: `[B, C, H, W]`

---



## Sensor / Imaging

### RGB Camera
가시광 영역의 색과 밝기를 일반적으로 R, G, B 세 Channel의 이미지로 기록하는 카메라입니다.

### Monochrome / Mono Camera
색 Channel 없이 밝기 중심의 영상을 얻는 카메라입니다. 출력은 보통 1 Channel 이미지입니다.

### IR / NIR
Infrared / Near-Infrared. 사람의 눈에 보이지 않는 적외선 영역의 빛을 이용하거나 측정합니다.

### Thermal Camera
물체에서 방출되는 열 복사를 측정해 온도 분포를 영상 형태로 표현하는 센서입니다.

### Depth Map
각 Pixel 위치에 색이 아니라 카메라에서 물체까지의 거리 값을 저장한 2차원 배열입니다.

### Stereo Vision
두 개 이상의 서로 다른 시점의 이미지를 비교해 시차(Disparity)로부터 깊이를 추정하는 방법입니다.

### ToF
Time of Flight. 빛을 보내고 돌아오는 시간이나 위상 차이를 이용해 거리를 추정하는 방식입니다.

### LiDAR
Light Detection and Ranging. Laser를 이용해 주변 물체까지의 거리를 측정하며 결과를 3차원 Point Cloud로 표현하는 경우가 많습니다.

### Point Cloud
3차원 공간의 여러 점을 모은 데이터입니다. 기본적으로 각 점이 `(x, y, z)` 좌표를 가집니다.

### Event Camera
고정 FPS로 전체 Frame을 저장하는 대신, 각 Pixel의 밝기 변화가 발생했을 때 시간·위치·변화 방향을 Event로 출력하는 센서입니다.

---

## CNN

### Kernel / Filter
이미지의 작은 영역을 훑으며 특징을 추출하는 학습 가능한 가중치 집합입니다. 흔히 `3×3`을 사용합니다.

### Convolution
Kernel을 이미지 위에서 이동시키며 곱셈과 덧셈을 수행해 새로운 Feature Map을 만드는 연산입니다.

### Feature Map
Convolution 결과로 만들어지는 특징 지도입니다. 특정 패턴이 어디에서 강하게 나타나는지를 표현합니다.

### Stride
Kernel이 한 번에 몇 Pixel씩 이동하는지 나타냅니다. `stride=2`이면 공간 크기가 빠르게 줄어듭니다.

### Padding
이미지 가장자리 주변에 값을 추가하는 방법입니다. `3×3, stride=1, padding=1`이면 입력과 출력의 H×W를 동일하게 유지할 수 있습니다.

### Receptive Field
특정 Feature가 원본 이미지에서 영향을 받는 영역의 크기입니다. CNN이 깊어질수록 일반적으로 Receptive Field가 커집니다.

### Pooling
Feature Map의 공간 크기를 줄이는 연산입니다. Max Pooling은 영역 내 최댓값을 선택합니다.

### Backbone
입력 이미지에서 유용한 Feature를 추출하는 모델의 중심 부분입니다. ResNet, EfficientNet 등이 대표적입니다.

### Head
Backbone Feature를 이용해 최종 Task를 수행하는 부분입니다. 예: Classification Head, Detection Head, Segmentation Head.

### Residual / Skip Connection
입력을 몇 개 Layer 뒤의 출력에 직접 더하거나 연결하는 구조입니다. ResNet의 핵심입니다.

---

## Vision Transformer

### Patch
이미지를 작은 정사각형 조각으로 나눈 단위입니다.

예: `224×224` 이미지를 `16×16` Patch로 나누면 `14×14 = 196`개 Patch가 됩니다.

### Token
Transformer가 처리하는 기본 단위입니다. ViT에서는 각 Patch를 하나의 Token으로 바꿉니다.

### Embedding
Token을 일정 길이의 숫자 Vector로 표현한 것입니다.

### Patch Embedding
이미지 Patch를 Transformer가 처리할 수 있는 Vector로 바꾸는 과정입니다.

### Position Embedding
Transformer가 각 Token의 위치를 알 수 있도록 추가하는 위치 정보입니다.

### CLS Token
Classification용 ViT에서 전체 이미지를 대표하도록 사용하는 특별한 Token입니다.

### Query (Q)
현재 Token이 다른 Token에서 어떤 정보를 찾을지 표현하는 Vector입니다.

### Key (K)
각 Token이 자신이 어떤 정보를 가지고 있는지를 표현하는 Vector입니다.

### Value (V)
Attention을 통해 실제로 전달될 정보입니다.

### Self-Attention
같은 입력 Token 집합 안에서 Token끼리 관련도를 계산하고, 중요한 Token의 정보를 더 많이 반영하는 연산입니다.

```text
Query와 모든 Key 비교
        ↓
관련도
        ↓
Softmax
        ↓
Attention Weight
        ↓
Value 가중합
```

### Multi-Head Attention
Self-Attention을 여러 개의 Head로 병렬 수행하여 서로 다른 관계를 학습하게 하는 구조입니다.

### MLP
Multi-Layer Perceptron. Transformer Block에서 Attention 뒤에 위치하며 Token Feature를 비선형 변환합니다.

### LayerNorm
각 Token Feature의 값을 정규화하여 학습을 안정화하는 기법입니다.

### Transformer Encoder
Self-Attention, MLP, Residual Connection, LayerNorm으로 구성된 Block을 반복한 구조입니다.

---

## Training / Evaluation

### Epoch
전체 학습 데이터를 한 번 모두 사용한 횟수입니다.

### Batch
한 번의 Forward/Backward 연산에 함께 넣는 샘플 묶음입니다.

### Loss
모델 예측과 정답 사이의 차이를 수치로 표현한 값입니다.

### Backpropagation
Loss가 작아지도록 각 Weight가 얼마나 수정되어야 하는지 Gradient를 계산하는 과정입니다.

### Learning Rate
한 번 업데이트할 때 Weight를 얼마나 크게 변경할지 결정하는 값입니다.

### Overfitting
Train 데이터에는 잘 맞지만 새로운 데이터에서는 성능이 떨어지는 현상입니다.

### Data Augmentation
회전, 밝기 변화, Crop 등으로 학습 데이터를 변형하여 다양한 조건을 학습시키는 기법입니다.

### Domain Shift
학습 데이터와 실제 운영 데이터의 분포가 달라지는 현상입니다. 카메라, 조명, 배경, 제품 상태 변화 등이 원인이 될 수 있습니다.

### Precision
모델이 Positive라고 예측한 것 중 실제 Positive 비율입니다.

### Recall
실제 Positive 중 모델이 찾아낸 비율입니다.

### F1-score
Precision과 Recall의 조화평균입니다.

### mAP
Object Detection/Segmentation에서 여러 Class와 IoU threshold를 바탕으로 성능을 요약하는 대표 지표입니다.
