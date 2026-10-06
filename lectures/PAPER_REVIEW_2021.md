# Alzubaidi et al. (2021) 기반 강의 보강 기록

원문: [Review of deep learning: concepts, CNN architectures, challenges,
applications, future directions](https://doi.org/10.1186/s40537-021-00444-8),
Journal of Big Data 8, 53, 2021-03-31.

이 리뷰의 기초 개념, CNN 구성 요소·연결 원리, 학습의 어려움을 기존 입문
강의에 연결했습니다. 2021년까지의 리뷰이며 최신 모델 순위 자료로 사용하지
않습니다. 원본 그림과 문장을 복제하지 않고 강의용 도표를 직접 재구성했습니다.
쉬운 비교 그림 뒤에 선택한 계산·구조 상세 설명을 배치합니다.

## 논문과 배포 자료의 대응

페이지는 표지까지 포함한 슬라이드 기준입니다. 이후 순서 변경 시
`docs/assets/lesson/manifest.json`의 `number + 1`이 실제 페이지입니다.

| 챕터·페이지 | 보강 내용 | 리뷰의 해당 부분 | 도표 |
| --- | --- | --- | --- |
| AI Basics 22 | 특징 설계와 특징 학습 비교 | Background, Fig. 3 | survey_feature_learning.svg |
| AI Basics 34 | 증강·Dropout·Early Stopping | Regularization, Overfitting | survey_regularization.svg |
| AI Basics 40 | 클래스 불균형 대응과 평가 | Imbalanced data | survey_class_imbalance.svg |
| AI Basics 42 | 분류용 Cross-entropy 계산 | CNN layers, Loss Functions | survey_classification_loss.svg |
| Vision AI 21 | 작은 분류 CNN의 전체 흐름 | CNN layers, Fig. 7 | survey_cnn_pipeline.svg |
| Vision AI 24 | 순차·병렬·우회 연결 | CNN architectures | survey_architecture_patterns.svg |
| Vision AI 25 | Residual 합산과 Shape 조건 | ResNet, Fig. 20 | survey_residual_detail.svg |

기존 Pooling 설명에도 공간 해상도 감소로 작은 결함·경계 정보가 일부 사라질
수 있다는 점을 보강했습니다. 모델 이름을 나열하기보다 입력에서 출력으로
어떤 계산이 연결되는지 설명합니다.

## 원 논문·공식 문서를 대조해 명확하게 한 점

- 자동 특징 학습은 사람이 특징을 일일이 설계할 필요를 줄인다는 뜻입니다.
  지도학습에서 Label 없이 학습한다는 뜻으로 설명하지 않습니다. 전통적 ML의
  한 파이프라인과 딥러닝의 한 파이프라인을 비교하며 모든 ML을 이분하지 않습니다.
- CNN 공간 출력 크기는 PyTorch Conv2d의 일반식으로 계산합니다. 기존 강의의
  정확한 합성곱 예시와 Channel 합산 설명을 유지합니다.
- CE 그림은 단일 정답·가중치 없음·Label smoothing 없음의 단일 샘플입니다.
  자연로그를 사용하며 p=0.2이면 1.609, p=0.8이면 0.223입니다.
  PyTorch CrossEntropyLoss의 실제 입력은 Softmax 확률이 아닌 Logit입니다.
- Dropout은 매 Forward마다 표본을 새로 뽑으며 p=0.5는 제거 확률입니다.
  항상 정확히 절반을 제거한다는 뜻이 아닙니다. PyTorch의 inverted dropout은
  학습 중 유지한 값을 1/(1-p)로 조정하고 eval에서는 항등 연산입니다.
- Residual 그림은 활성화 전 합산을 나타냅니다. Shape가 같은 x와 F(x)를
  원소별로 더합니다. 원래 ResNet v1은 합산 후 ReLU를 적용합니다.
  Shape가 달라지면 Projection 등으로 맞춰야 하며 Channel 결합과 다릅니다.
- 구조를 깊게 만들면 항상 성능이 높아진다거나, Residual이 모든 최적화 문제를
  해결한다고 설명하지 않습니다. 연결 방식의 설계 원리를 비교합니다.

## 강의 목적에 맞춘 적용 판단

이는 리뷰의 실험 결론을 복사한 것이 아니라 현재 강의에 맞춘 편집 판단입니다.
학습 표본 조정은 Train에서 수행하고, 설정 선택은 Validation에서 하며,
최종 Test는 실제 평가하려는 운영 분포와 독립성을 유지하도록 안내합니다.
Early Stopping은 Stanford CS231n의 정규화 설명으로 보완했습니다.
증강·Dropout·가중치 조정은 Validation에서 비교할 선택지로 설명합니다.

기존 데이터 누수·Group Split·전이학습·Shortcut 설명에 연결했습니다.
입문 강의의 범위에 맞춰 의료 응용 목록, CPU/GPU/FPGA 상세, 모든 CNN의 연혁,
RNN/GAN/강화학습은 이번 슬라이드 확장에 포함하지 않았습니다.

## 추가 검증 출처

- [LeCun et al., Deep learning](https://www.nature.com/articles/nature14539)
- [VGG 원 논문](https://arxiv.org/abs/1409.1556)
- [Inception 원 논문](https://openaccess.thecvf.com/content_cvpr_2015/html/Szegedy_Going_Deeper_With_2015_CVPR_paper.html)
- [ResNet 원 논문](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)
- [Dropout 원 논문](https://jmlr.org/papers/v15/srivastava14a.html)
- [PyTorch Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
- [PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [PyTorch Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html)
- [Stanford CS231n 정규화](https://cs231n.github.io/neural-networks-2/)

## 자산과 검증

기존 AI 생성 사과 사진을 재사용했습니다. 텐서 크기·비율·연결은 직접 작성한
SVG이며 CE 곡선은 NumPy/Matplotlib로 계산했습니다. 측정된 모델 성능이나
실험 결과를 표현한 그림이 아닙니다. 도표는 저장소 내부 자산만 참조합니다.

생성: `python scripts/build_lesson_revision.py`

검증: `python scripts/verify_lesson_revision.py`

SVG 렌더링과 글자 영역을 확인하고 배포 후 추가한 7장을 브라우저에서 확인합니다.
