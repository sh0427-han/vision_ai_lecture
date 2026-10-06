# 03. Vision AI — Task에서 CNN까지

Vision AI를 처음 배우는 사람이 **무엇을 출력할지 → 어떤 Label이 필요한지 → CNN이 이미지를 어떻게 계산하는지 → 실제 Model 구조와 학습으로 어떻게 이어지는지** 순서대로 이해하도록 구성합니다.

## 강의 흐름

1. 현장 질문 → 원하는 Output → Vision Task → Label → Model / Metric
2. Classification
3. Object Detection
4. Segmentation
5. Task별 Label 구조
6. IoU: 위치 Prediction과 Ground Truth의 겹침
7. 왜 이미지에서 CNN이 유용한가
8. Kernel: Local Pattern에 반응하는 학습 Weight
9. Convolution 한 칸의 계산
10. Stride / Padding / Downsampling
11. Feature Map / Channel
12. Feature Hierarchy
13. Receptive Field
14. CNN Training
15. Backbone / Task Head
16. Transfer Learning / Fine-tuning
17. Shortcut Learning / 현장 실패 원인
18. Vision AI Project Cycle

## 1. Model보다 Output이 먼저

Vision AI에서 첫 질문은 “어떤 Model을 쓸까?”가 아니라 **“문제를 해결하려면 무엇을 출력해야 하는가?”**입니다.

```text
현장 질문
  ↓
원하는 Output
  ↓
Vision Task
  ↓
Label
  ↓
Model / Metric
```

- 이미지 전체의 상태가 필요 → Classification
- 객체의 위치가 필요 → Detection
- 정확한 Pixel 영역이 필요 → Segmentation

## 2. Classification

질문: **이 Image 전체는 무엇인가?**

```text
Input Image → Model → Class Score
```

객체 위치를 직접 출력하지 않습니다.

대표 Metric: Accuracy / Precision / Recall / F1

## 3. Object Detection

질문: **무엇이 어디에 있는가?**

Output은 보통 Class, Bounding Box, Score를 포함합니다.

대표 Metric: Precision / Recall / IoU / mAP

## 4. Segmentation

질문: **정확히 어느 Pixel인가?**

Output은 Pixel Mask입니다. 면적, 경계, 형상 분석이 필요한 문제에 유용합니다.

대표 Metric: IoU / Dice / Boundary IoU 등

## 5. Label 형태

같은 Image라도 Task가 바뀌면 Label 구조도 달라집니다.

```text
Classification → class label
Detection      → class + bounding box
Segmentation   → pixel mask
```

## 6. IoU

**IoU(Intersection over Union)**는 Ground Truth와 Prediction의 겹친 영역을 합집합 영역으로 나눈 값입니다.

```text
IoU = Intersection / Union
```

완전히 겹치면 1.0입니다.

Detection의 mAP는 여러 조건에서 Precision-Recall 성능을 요약하는 대표 Metric입니다. 입문 단계에서는 먼저 IoU가 위치 예측의 겹침 정도를 표현한다는 점을 이해합니다.

## 7. 왜 CNN인가

Image는 가까운 Pixel끼리의 공간 관계가 중요합니다.

CNN의 두 가지 핵심 직관:

- **Local connectivity**: 작은 주변 영역부터 계산
- **Weight sharing**: 같은 Kernel Weight를 여러 위치에서 재사용

이 때문에 같은 Pattern이 이미지의 다른 위치에 나타나도 같은 Kernel로 반응을 계산할 수 있습니다.

## 8. Kernel

Kernel(Filter)은 작은 Weight 배열입니다.

처음에는 “작은 Pattern에 얼마나 반응하는지 계산하는 Weight 묶음”으로 이해하면 됩니다.

강의에서 Edge Kernel을 예로 보여주지만, 실제 CNN에서는 사람이 모든 Kernel을 정하는 것이 아니라 Training으로 학습합니다.

## 9. Convolution

한 위치의 계산:

```text
Image Patch × Kernel
        ↓
같은 위치끼리 곱하기
        ↓
모두 더하기
        ↓
Output 한 칸
```

같은 Kernel을 여러 위치에 반복 적용하면 Feature Map이 만들어집니다.

RGB 입력에서는 Kernel도 Channel 방향을 포함하므로, 예를 들어 3 × 3 Kernel의 실제 크기는 3 × 3 × 3처럼 볼 수 있습니다.

## 10. Stride / Padding / Downsampling

- **Stride**: Kernel 이동 간격
- **Padding**: Input 가장자리 주변에 값을 채우는 방법
- **Downsampling**: Feature Map의 공간 해상도를 줄이는 과정

Downsampling에는 Strided Convolution, Pooling 등 여러 방법이 있습니다.

## 11. Feature Map / Channel

Kernel 하나를 공간 전체에 적용한 반응 결과를 Feature Map으로 볼 수 있습니다.

```text
Input: 224 × 224 × 3
          ↓
      64 Kernels
          ↓
Output: 224 × 224 × 64
```

여기서 64는 Output Feature Map, 즉 Channel 수와 연결됩니다.

각 Channel이 반드시 사람이 명확한 이름을 붙일 수 있는 Feature 하나와 대응하는 것은 아닙니다.

## 12. Feature Hierarchy

개념적으로는 다음과 같이 이해할 수 있습니다.

```text
Pixel / Color
   ↓
Local Pattern
   ↓
Part / Shape
   ↓
Task Representation
```

실제 Feature는 사람이 이름 붙일 수 있는 형태로 깔끔하게 분리되지 않을 수 있습니다.

## 13. Receptive Field

Receptive Field는 **한 Feature 위치가 원본 Input의 어느 범위에서 영향을 받는가**를 의미합니다.

Layer가 쌓이거나 Downsampling이 진행되면 더 넓은 문맥 정보를 사용할 수 있습니다.

## 14. CNN Training

AI Basics에서 배운 학습 과정과 동일합니다.

```text
Image + Label
   ↓
CNN Forward
   ↓
Prediction
   ↓
Loss
   ↓
Backward
   ↓
Optimizer
   ↓
Kernel / Layer Weight Update
```

Kernel 역시 Training으로 학습되는 Parameter입니다.

## 15. Backbone / Head

입문적으로 많은 Vision Architecture를 다음 관점으로 볼 수 있습니다.

- **Backbone**: 공통 Feature 추출
- **Head**: Task에 맞는 Output 생성

```text
Image → Backbone
            ├→ Classification Head → Class
            ├→ Detection Head      → Class + Box
            └→ Segmentation Head   → Mask
```

모든 모델이 이 구조로 정확히 나뉘는 것은 아니지만 Architecture를 처음 읽을 때 유용한 관점입니다.

## 16. Transfer Learning / Fine-tuning

큰 Dataset에서 이미 학습한 Backbone Weight를 새 Task의 출발점으로 사용할 수 있습니다.

```text
Large Dataset
   ↓
Pretrained Backbone
   ↓
My Dataset + Labels
   ↓
Fine-tuning
   ↓
My Task Model
```

데이터가 적을 때 좋은 출발점이 될 수 있지만, Pretraining Domain과 실제 운영 Domain 차이가 크면 반드시 별도 검증해야 합니다.

## 17. Shortcut Learning과 Vision Model의 실패

높은 Score가 곧 사람이 기대한 의미를 이해했다는 뜻은 아닙니다.

Vision Model은 다음과 같은 단서를 Shortcut으로 사용할 수 있습니다.

- 배경 색이나 바닥 Pattern
- 특정 Camera / 설비에서만 생기는 영상 특성
- Annotation과 우연히 함께 나타나는 Marker
- Object 자체가 아니라 위치나 촬영 조건

따라서 평균 Metric뿐 아니라 **실패 Image, 설비·시간대·조명별 Slice, 운영 분포 변화**를 함께 확인해야 합니다.

이 관점은 Geirhos et al.의 “Shortcut Learning in Deep Neural Networks”에서 정리된 문제의식과 연결됩니다.

## 18. 전체 Project Cycle

```text
문제 정의
   ↓
Data / Label
   ↓
Train
   ↓
Evaluate
   ↓
Deploy
   ↓
Monitor
   └→ 실패 사례 → Data 보강 / 문제 재정의 → Retraining
```

Vision AI의 핵심은 Model Architecture 하나가 아니라 **문제 정의부터 운영 피드백까지 전체 Cycle을 설계하는 것**입니다.

## 2026-10-06 배포 슬라이드 순서

현재 배포 HTML의 순서는 아래를 기준으로 합니다. 상세 설명은 관련 개념 바로 뒤에 배치합니다. 앞의 개념 노트는 참고용입니다.

1. 필요한 결과부터 정하면 Vision Task가 정해집니다 (기본)
2. 이미지 전체의 상태나 종류를 예측합니다 (기본)
3. 객체나 결함의 위치를 사각형으로 찾습니다 (기본)
4. 어느 Pixel이 관심 영역인지 구분합니다 (기본)
5. 같은 사진이라도 Task가 바뀌면 정답 형태가 바뀝니다 (기본)
6. 위치와 영역은 정답과 얼마나 겹치는지 평가합니다 (기본)
7. 겹친 칸 수를 전체 합집합 칸 수로 나눕니다 (상세)
8. 작은 영역의 경계·밝기 변화를 먼저 살펴봅니다 (기본)
9. CNN은 작은 영역을 보고 같은 가중치를 재사용합니다 (기본)
10. 같은 필터도 이미지 영역에 따라 반응이 달라집니다 (기본)
11. 같은 위치끼리 곱하고 더해 출력 한 칸을 만듭니다 (상세)
12. 반응값을 위치대로 모으면 특징 지도가 됩니다 (기본)
13. RGB 전체를 보는 필터 하나가 출력 Channel 하나를 만듭니다 (상세)
14. 필터를 몇 칸씩 이동할지 정합니다 (기본)
15. 가장자리 주변에 값을 채워 계산 범위를 조절합니다 (기본)
16. 공간 해상도를 줄여 더 작은 특징 지도를 만듭니다 (기본)
17. Kernel·Stride·Padding으로 출력 크기를 계산합니다 (상세)
18. Layer는 앞의 특징을 조합해 더 복잡한 표현을 만듭니다 (기본)
19. 깊은 층의 한 위치는 더 넓은 입력 범위의 영향을 받습니다 (상세)
20. 특징을 만드는 부분과, 결과를 만드는 부분을 나눠 봅니다 (기본)
21. 블록을 연결하고 각 단계의 특징 크기를 표시합니다 (상세)
22. CNN의 필터도 오차를 줄이는 방향으로 학습합니다 (기본)
23. 이미 배운 가중치에서 내 Task의 학습을 시작합니다 (기본)
24. 고정할 부분과 추가 학습할 부분을 구분합니다 (상세)
25. 높은 점수만으로 판단 근거가 맞다고 보장할 수 없습니다 (기본)
26. 문제 정의부터 운영 관찰까지 연결해 개선합니다 (기본)

계산·숫자·Tensor 구조 그림은 `scripts/build_lesson_revision.py`에서 생성하며, 외부 이미지 서버나 CDN을 사용하지 않습니다.
