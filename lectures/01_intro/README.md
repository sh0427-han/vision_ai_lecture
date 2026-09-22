# 01. Vision AI 입문

## 학습 목표

이 챕터가 끝나면 다음 질문에 답할 수 있어야 합니다.

1. 컴퓨터에게 이미지는 무엇인가?
2. 같은 물체인데도 왜 Pixel 값은 달라질 수 있는가?
3. Classification, Detection, Segmentation은 어떻게 다른가?
4. Vision AI 개발은 왜 데이터와 평가가 중요한가?

## 1. 컴퓨터에게 사진은 사진이 아니다

사람은 이미지를 보면 곧바로 "고양이", "자동차", "불량" 같은 의미를 떠올립니다.

컴퓨터가 처음 받는 것은 숫자 배열입니다.

```text
RGB Image
224 × 224 × 3

→ 150,528개의 숫자
```

각 Pixel은 예를 들어 다음처럼 표현될 수 있습니다.

```text
[255, 0, 0]     빨강
[0, 255, 0]     초록
[0, 0, 255]     파랑
```

## 2. 왜 Vision이 어려운가?

같은 물체라도 입력 숫자는 쉽게 바뀝니다.

- 조명
- 카메라 각도
- 물체 위치
- 크기
- 회전
- 일부 가림
- Blur
- 반사
- 카메라 종류

예를 들어 한 Pixel이 밝은 조건에서 `[180, 170, 165]`였다가 어두운 조건에서 `[80, 75, 72]`가 될 수 있습니다.

사람은 같은 물체라고 이해하지만, 컴퓨터가 받는 숫자는 크게 달라집니다.

## 3. Vision AI의 대표 Task

### Classification
"이 이미지가 무엇인가?"

```text
Image → Model → Normal 97%, Abnormal 3%
```

### Object Detection
"무엇이 어디에 있는가?"

```text
Image → Model → Class + Bounding Box + Confidence
```

### Segmentation
"어느 Pixel이 그 물체인가?"

Detection이 상자를 찾는다면 Segmentation은 물체의 실제 모양에 가까운 Pixel 영역을 찾습니다.

## 4. 모델 학습 흐름

```text
Image + Label
     ↓
   Model
     ↓
 Prediction
     ↓
정답과 비교
     ↓
    Loss
     ↓
Backpropagation
     ↓
Weight Update
```

이 과정을 반복하면서 모델이 데이터에서 유용한 패턴을 학습합니다.

## 5. 좋은 모델만 있으면 되는가?

아닙니다.

```text
실제 성능
=
문제 정의
+ 데이터 품질
+ Label 품질
+ 모델
+ 평가 방법
+ 운영 환경
```

산업 Vision AI에서는 카메라, 조명, 제품 조건이 바뀌는 것만으로도 성능이 달라질 수 있습니다.

## 6. 다음 챕터

이제 "수많은 Pixel에서 어떻게 유용한 특징을 찾는가?"라는 질문으로 넘어갑니다.

→ [02. CNN](../02_cnn/README.md)
