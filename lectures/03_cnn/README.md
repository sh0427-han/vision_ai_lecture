# 03. CNN — 작은 특징을 조합해 사물을 인식하기

## 핵심 직관

사람은 사물을 볼 때 Pixel 전체의 숫자를 외워서 판단하지 않습니다.

예를 들어 사과를 보면:

```text
빨간색
+ 둥근 윤곽
+ 꼭지
+ 표면 질감
        ↓
여러 특징을 종합
        ↓
"사과 같다"
```

처럼 여러 시각적 단서를 종합해 빠르게 판단합니다.

CNN도 교육적인 관점에서는 비슷한 흐름으로 이해할 수 있습니다.

![Human Feature and CNN](../../assets/diagrams/human_feature_to_cnn.svg)

단, **인간의 시각 처리 메커니즘과 CNN의 계산 구조가 실제로 동일하다는 뜻은 아닙니다.** 이 비교는 CNN의 Feature Hierarchy를 쉽게 이해하기 위한 직관입니다.

## 1. CNN의 핵심: Local → Complex

```text
Pixel
 ↓
Edge / 방향
 ↓
Texture / 반복 패턴
 ↓
Shape
 ↓
Object Part
 ↓
Object-level Feature
```

실제 Feature가 사람이 붙인 이름대로 정확히 분리되는 것은 아니지만, 단순한 지역 패턴에서 더 복잡한 표현으로 바뀐다는 직관이 중요합니다.

## 2. Kernel / Filter

**Kernel / Filter**는 이미지의 작은 영역에서 패턴을 추출하기 위한 학습 가능한 Weight입니다.

```text
3 × 3 Kernel

[ w1 w2 w3 ]
[ w4 w5 w6 ]
[ w7 w8 w9 ]
```

Kernel Weight는 Dataset을 통해 학습됩니다.

## 3. Convolution

**Convolution**은 같은 Kernel을 이미지 여러 위치에 적용해 각 위치에서 패턴 반응값을 계산하는 연산입니다.

```text
Input Patch         Example Filter

1 2 1               1  0 -1
0 1 0       ×       1  0 -1
1 2 1               1  0 -1
```

위 Filter는 개념 설명용 예시입니다. 실제 CNN에서는 Weight가 학습으로 결정됩니다.

### Weight Sharing

같은 Kernel Weight를 이미지 여러 위치에서 공유해 사용합니다.

## 4. Feature Map

**Feature Map**은 특정 Kernel이 이미지의 각 위치에서 얼마나 반응했는지를 공간적으로 표현한 출력입니다.

```text
Input
224 × 224 × 3

Conv 64 filters
       ↓
224 × 224 × 64
```

## 5. Channel

서로 다른 Feature Map을 쌓아 놓은 축입니다.

```text
Filter 1  → Feature Map 1
Filter 2  → Feature Map 2
...
Filter 64 → Feature Map 64

= 64 Channels
```

## 6. Stride와 Padding

### Stride
Kernel이 한 번에 몇 Pixel씩 이동할지 정합니다.

### Padding
입력 가장자리에 값을 추가해 출력 크기와 경계 처리를 조절합니다.

출력 크기:

```text
O = floor((W - K + 2P) / S) + 1
```

예:

```text
W=224
K=3
P=1
S=1

→ O=224
```

## 7. Receptive Field

특정 Feature가 원본 이미지에서 영향을 받는 영역입니다.

Stride=1인 3×3 Conv를 단순히 연속해서 쌓는 예:

```text
1 layer → 약 3×3
2 layers → 약 5×5
3 layers → 약 7×7
```

CNN이 깊어질수록 더 넓은 영역의 정보를 조합할 수 있습니다.

## 8. Downsampling

Feature Map의 H×W를 줄이는 과정입니다.

```text
224×224×64
    ↓
112×112×128
    ↓
56×56×256
```

Pooling이나 Strided Convolution 등을 사용할 수 있습니다.

목적은 보통:

- 연산량 감소
- 더 넓은 문맥 표현
- 세밀한 위치보다 의미 있는 특징에 집중

등입니다.

## 9. CNN도 학습으로 Feature를 찾는다

```text
Image + Label
      ↓
CNN Forward
      ↓
Prediction
      ↓
Loss
      ↓
Backpropagation
      ↓
Kernel Weight Update
```

사람이 특정 Kernel을 직접 지정하는 것이 아니라 Task의 Loss가 줄어들도록 Kernel Weight가 학습됩니다.

## 10. 한 문장 정리

> **CNN은 작은 지역 패턴을 학습하고 여러 Layer에서 그 패턴을 조합해 점점 더 복잡하고 의미 있는 Feature를 만드는 신경망입니다.**

강의에서는 Kernel 수식을 외우기보다 다음 흐름을 먼저 기억합니다.

```text
특징을 찾는다
   ↓
특징을 조합한다
   ↓
더 복잡한 특징을 만든다
   ↓
판단한다
```
