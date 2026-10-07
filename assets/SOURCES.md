# Visual / Reference Sources

강의 자료의 출처와 사용 원칙을 기록합니다.

## 원칙

1. 외부 Figure를 그대로 복사하기보다 가능한 경우 직접 다시 그린 교육용 Diagram을 사용합니다.
2. 외부 자료를 참고해 재구성한 경우 원 출처 링크를 기록합니다.
3. 외부 사진을 추가할 경우 License와 원본 URL을 기록합니다.
4. 출처가 불명확한 이미지는 강의자료에 포함하지 않습니다.

## 현재 직접 제작한 Diagram

- `vision_ai_pipeline.svg`
- `sensor_overview.svg`
- `image_as_numbers.svg`
- `ai_ml_dl.svg`
- `supervised_tasks.svg`
- `perceptron.svg`
- `linear_vs_nonlinear.svg`
- `training_loop.svg`
- `dataset_split.svg`
- `ml_workflow.svg`
- `human_feature_to_cnn.svg`
- `cnn_flow.svg`
- `intro_question_apple.svg`
- `intro_human_vs_computer.svg`
- `supervised_unsupervised_industry.svg`
- `vision_tasks_comparison.svg`
- `and_xor_linear_separability.svg`
- `linear_layers_collapse.svg`
- `apple_visual_variations.svg`

## 2026-09 도표 재구성

- `docs/assets/*.svg`: 41개 도표를 1200×600 좌표계로 재구성.
- 사과 이미지: 이 프로젝트에서 AI로 생성한 교육용 이미지.
  `docs/assets/vision_task_apple_reference.jpg` (960×640).
  실사 촬영이나 실제 검사 데이터가 아님.
- 사과의 검출 박스, 분할 마스크, 0.98 점수는 설명용 예시이며 모델 추론 결과가 아님.
- RGB 숫자는 해당 JPG를 디코딩한 픽셀에서 직접 취득.
  밝기·크기·가림 변형은 SVG에서 만든 도식적 시뮬레이션.
- Noto Sans CJK KR Regular의 사용 글리프만 WOFF로 부분 집합화해 SVG에 내장.
  원본: https://github.com/notofonts/noto-cjk
  라이선스: SIL Open Font License 1.1 (`assets/NOTO_FONT_LICENSE.txt`).
- SVG를 HTML `img`로 사용할 때 외부 이미지 로딩이 제한되므로 JPG를 data URL로 내장.
  근거: https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image
- 생성: `scripts/rebuild_visuals.py --font <NotoSansCJKkr-Regular.otf>`
- 검증: `scripts/verify_visuals.py` (선택: `--render-dir <directory>`)

### 레이아웃 및 내용 검증 기준

1. 텍스트는 실제 글꼴 폭으로 줄바꿈하고 지정한 박스 높이를 초과하면 생성을 중단.
2. 사진·폰트를 포함한 도표 내부 리소스는 외부 네트워크에 의존하지 않음.
3. 합성곱: 5×5 / kernel 3×3 / stride 1 / padding 0 → 3×3 출력.
4. Batch: 10장 / batch_size 4 / drop_last=False → 4+4+2, 총 3 step.
5. 원본 이미지와 예시 annotation을 구분하고, AI 생성 이미지임을 명시.

## Intro Sensor 생성 이미지

- Intro 9 / 10의 사진형 장면은 이 프로젝트에서 AI로 생성한 교육용 이미지입니다.
- 실제 제품 사진, 실제 LiDAR scan, 실제 열화상 측정 데이터가 아닙니다.
- Intro 9 / 10은 2172 × 724 해상도의 AI 생성 원본 PNG를 Repository에 직접 저장해 사용합니다.
- 외부 이미지 서버나 runtime base64 조립에 의존하지 않고 `docs/assets/generated/*_hd.png`를 HTML에서 직접 참조합니다.
- Intro 9 비교 이미지: RGB 거리 장면 / LiDAR 실내 공간 scan / IR 전기 설비 열화상.
- 기존 Intro 10 합성 이미지는 RGB / IR 영역의 시각 예시로만 재사용하며, LiDAR 생활 예시는 별도 로봇청소기 생성 이미지를 사용합니다.

## AI 기초 참고 자료 (기존)

### WikiDocs — 딥 러닝 파이토치 교과서
https://wikidocs.net/book/2788

다음 입문 내용을 참고해 Vision AI 강의 흐름에 맞게 재구성했습니다.

- Machine Learning Workflow
- Data Splitting
- Linear Regression / Gradient Descent / Autograd
- Mini Batch / Batch Size / Epoch / Iteration
- Classification / Regression
- Supervised Learning
- Perceptron / MLP / XOR
- Backpropagation
- Overfitting

## CNN 관련 논문

### VGG
https://arxiv.org/abs/1409.1556

### ResNet
https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html

## Intro / Sensor References

### OpenCV Mat - The Basic Image Container
https://docs.opencv.org/4.10.0/d6/d6d/tutorial_mat_the_basic_image_container.html

### Intel RealSense D400 Documentation
https://dev.intelrealsense.com/docs/multiple-depth-cameras-configuration%C2%A0

### Event-based Vision: A Survey
https://arxiv.org/abs/1904.08405


## AI Basics 시각자료 개편

다음 자산은 이 프로젝트에서 초보자 강의용으로 직접 재구성한 SVG입니다.

- `docs/assets/optimizer_loss_landscape.svg`
- `docs/assets/activation_relu_boundary.svg`
- `docs/assets/backpropagation_visual.svg`
- `docs/assets/data_leakage_visual.svg`
- `docs/assets/group_split_visual.svg`
- `docs/assets/and_xor_linear_separability.svg`
- `docs/assets/rule_vs_ml.svg`
- `docs/assets/overfit_leakage.svg`
- `docs/assets/ml_workflow.svg`

개념 관계와 흐름을 전달하는 용도이므로 논문 Figure를 복제하지 않고 강의용으로 단순화했습니다.


## Intro 원근감 / LiDAR 생활 예시 생성 이미지

- `docs/assets/generated/intro_perspective_cat_generated.svg`
  - AI로 생성한 교육용 이미지의 사진 영역을 Crop해 사용.
  - Camera 가까이의 고양이가 크게, 멀리 있는 사람이 작게 보이는 원근감 예시.
  - 실제 촬영 사진이나 측정 데이터가 아님.
- `docs/assets/generated/intro_lidar_robot_vacuum_generated.svg`
  - AI로 생성한 로봇청소기 LiDAR 공간 스캔 장면.
  - 자동차 이미지는 포함하지 않으며, 로봇청소기의 공간 맵핑 예시에만 사용.
  - 실제 LiDAR Point Cloud 측정 결과가 아니라 교육용 시각화임.
- 두 SVG는 생성 이미지 WebP를 내부에 그대로 포함하며 외부 이미지 서버에 의존하지 않습니다.


## Paper-style 기본 학습 Figure

- `docs/assets/supervised_unsupervised_industry.svg`
  - Supervised / Unsupervised Learning을 Feature Space scatter plot으로 비교.
  - 지도학습은 Label과 Decision Boundary, 비지도학습은 unlabeled sample과 Cluster structure를 표현.
- `docs/assets/classification_regression.svg`
  - Classification은 discrete class와 Decision Boundary, Regression은 continuous target과 fitted function으로 표현.
- 두 Figure 모두 특정 논문의 Figure를 복제한 것이 아니라, 학술 논문에서 흔히 사용하는 축·점·경계선 중심의 시각 문법을 강의용으로 재구성한 도표입니다.


## Beginner-first AI Basics 재구성

2026-09-25 개편에서는 처음 AI를 배우는 학생이 개념을 순서대로 연결할 수 있도록 다음 교육용 SVG를 새로 만들거나 전면 재작성했습니다.

- `docs/assets/perceptron.svg`
- `docs/assets/weight_bias_intuition.svg`
- `docs/assets/and_xor_linear_separability.svg`
- `docs/assets/neural_network_layers.svg`
- `docs/assets/linear_layers_collapse.svg`
- `docs/assets/activation_relu_boundary.svg`
- `docs/assets/feature_representation.svg`
- `docs/assets/loss_intuition.svg`
- `docs/assets/gradient_intuition.svg`
- `docs/assets/optimizer_loss_landscape.svg`
- `docs/assets/training_loop.svg`
- `docs/assets/backpropagation_visual.svg`
- `docs/assets/training_inference.svg`
- `docs/assets/batch_epoch.svg`
- `docs/assets/kfold_visual.svg`

특정 논문의 Figure를 복제하지 않았으며, Neural Network / Optimization 교과서에서 일반적으로 사용하는 Node, Layer, Loss landscape, Gradient, Decision Boundary 표현을 입문 강의용으로 단순화했습니다.


## Beginner-first Vision AI 재구성

2026-09-25 개편에서는 Vision AI 입문자가 Task와 CNN 계산을 단계적으로 연결할 수 있도록 다음 교육용 SVG를 새로 만들거나 전면 재작성했습니다.

- `docs/assets/iou_visual.svg`
- `docs/assets/cnn_why_local.svg`
- `docs/assets/kernel_pattern_detector.svg`
- `docs/assets/convolution_visual.svg`
- `docs/assets/stride_padding_downsampling.svg`
- `docs/assets/feature_maps.svg`
- `docs/assets/cnn_hierarchy.svg`
- `docs/assets/cnn_training.svg`
- `docs/assets/backbone_head.svg`
- `docs/assets/transfer_learning.svg`
- `docs/assets/vision_task_selection.svg`
- `docs/assets/vision_project_pipeline.svg`

특정 논문의 Figure를 복제하지 않았으며, Computer Vision 교재와 논문에서 일반적으로 사용하는 Convolution, Kernel, Feature Map, Receptive Field, Backbone/Head 표현을 초보자 강의용으로 단순화했습니다.


## Shortcut Learning 참고

### Geirhos et al. — Shortcut Learning in Deep Neural Networks
https://www.nature.com/articles/s42256-020-00257-z

- Nature Machine Intelligence, 2020.
- 표준 평가에서는 잘 작동하지만 더 어려운 실제 조건에서 전이되지 않는 decision rule을 Shortcut 관점으로 설명합니다.
- 강의의 `docs/assets/shortcut_learning.svg`는 논문 Figure를 복제하지 않고, 배경색과 Class가 우연히 연관된 Toy Example로 개념을 재구성한 교육용 Diagram입니다.
- AI Basics에서는 Shortcut Learning과 Data Leakage의 차이를 설명하고, Vision AI에서는 높은 Score가 사람이 기대한 Feature 사용을 보장하지 않는다는 운영 관점으로 연결합니다.


## 고해상도 생성 Lecture Figure — 2026-09-27

다음 자산은 ChatGPT에서 강의 목적에 맞게 생성한 뒤, 제목 중복을 줄이기 위해 Figure 영역을 Crop하고 WebP로 저장한 교육용 이미지입니다.

- `docs/assets/generated/lecture/intro_human_vs_computer.webp`
- `docs/assets/generated/lecture/intro_perspective.webp`
- `docs/assets/generated/lecture/intro_sensor_modalities.webp`
- `docs/assets/generated/lecture/ai_perceptron.webp`
- `docs/assets/generated/lecture/ai_leakage_shortcut.webp`
- `docs/assets/generated/lecture/vision_task_selection.webp`
- `docs/assets/generated/lecture/vision_convolution.webp`
- `docs/assets/generated/lecture/vision_backbone_head.webp`
- `docs/assets/generated/lecture/vision_transfer_learning.webp`

사용 원칙:
- 실제 촬영·실측·실제 Model 추론 결과가 아니라 강의용 시각화입니다.
- 당시 생성 Convolution Figure는 전체 Feature Map 값의 오류가 확인되어 2026-10-06 개편에서 사용을 중단했습니다. 현재 계산 그림은 아래 검증된 SVG를 사용합니다.
- LiDAR Figure는 자동차 예시 없이 로봇청소기와 실내 공간 Scan 예시만 사용합니다.
- AI / Machine Learning / Deep Learning / Computer Vision의 포함관계는 생성 이미지보다 정확성이 중요한 Diagram이므로 기존 `ai_ml_dl.svg`를 유지합니다.
- Repository 내부 WebP를 직접 참조하며 외부 이미지 Host나 Runtime base64 조립에 의존하지 않습니다.

## 기본 그림 + 상세 Figure 개편 — 2026-10-06

- `docs/assets/lesson/`: AI Basics와 Vision AI에서 실제 사용하는 그림.
- `docs/assets/lesson/manifest.json`: 슬라이드 번호·개념·설명 수준·자산 경로.
- 쉬운 기본 그림 뒤에 계산 그래프, 수식, Tensor 크기, 공간 연산 조건을 담은 상세 Figure를 배치.
- 특정 논문 Figure를 복제하지 않고 직접 작성한 SVG. 색은 기본 설명과 상세 설명에서 동일하게 사용.
- 사과 사진은 기존 AI 생성 교육용 이미지. Box·Mask·점수는 실제 모델 출력이 아닌 설명용 예시.
- AND 경계 `x1+x2=1.5`, XOR의 두 경계, Gradient 방향, 합성곱 전체 출력, RGB 전체 필터 합산을 교정.
- 5×5 합성곱 예시의 출력: `[[-6,12,16],[-6,8,15],[-4,2,7]]`.
- RGB 입력 224×224×3, 필터 64개, Kernel 3×3, Stride 1, Padding 1 → 224×224×64.
- Backbone의 고양이/컵 생성 그림 대신 동일한 사과 사진과 결함 annotation을 사용.
- `vision_convolution.webp`, `vision_backbone_head.webp`는 배포 슬라이드에서 사용하지 않음.
- 기존 SVG의 중복 제목을 제거한 context 자산은 원본에서 파생. 데이터는 그림 안에 포함하고 외부 요청을 사용하지 않음.

### 근거 자료

- Stanford CS231n, Optimization: https://cs231n.github.io/optimization-1/
  - Loss의 Gradient와 반대 방향으로 Parameter를 갱신하는 경사하강법.
- Stanford CS231n, Backpropagation: https://cs231n.github.io/optimization-2/
  - 계산 그래프에서 Chain Rule로 Gradient를 역방향 계산.
- Stanford CS231n, Neural Networks: https://cs231n.github.io/neural-networks-1/
  - Layer, 비선형 Activation, ReLU와 표현력.
- Stanford CS231n, CNN: https://cs231n.github.io/convolutional-networks/
  - Local connectivity, Weight sharing, 공간 출력 크기, Feature Map.
- PyTorch Conv2d: https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
  - Cross-correlation, Channel 합산, Weight shape와 Stride/Padding 조건.
- PyTorch Transfer Learning: https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
  - 고정된 특징 추출기와 Fine-tuning의 구분.
- scikit-learn Model Selection: https://scikit-learn.org/stable/modules/cross_validation.html
  - Train/Test 분리, 교차검증, Group 단위 검증.
- scikit-learn Metrics: https://scikit-learn.org/stable/modules/model_evaluation.html
  - Confusion Matrix, Accuracy, Precision, Recall, F1.

### 생성과 검증

- 생성: `python scripts/build_lesson_revision.py`
- 검증: `python scripts/verify_lesson_revision.py`
- HTML 슬라이드 수·연속 번호·자산 경로, SVG XML·내부 리소스 참조, 합성곱·Gradient·AND·IoU·평가지표 수치 검증.
- 두 챕터 전용 `docs/lesson.css`로 레이아웃 적용. Intro의 공통 CSS/JS는 변경하지 않음.

## 2026-10-06 전문 강의용 사진 자산

- ChatGPT Image Generation으로 생성한 사과·오렌지 사진형 자산과 촬영 조건 비교 이미지: `docs/assets/generated/`. 교육용 합성 이미지이며 실제 관측 데이터나 모델 실험 결과가 아닙니다. 상세 용도와 생성 명세는 해당 폴더 `README.md`에 기록했습니다.
- 사진 파일을 기반으로 지도/비지도학습, 신경망 입력, Dataset 촬영 조건, 계층적 Feature, Shortcut Learning 그림을 재구성했습니다. 수식·텐서·계산값은 기존 검증 가능한 SVG 방식으로 유지했습니다.

## Loss / Gradient / Optimizer 재구성 (2026-10-06)

- 개념 출처: Stanford CS231n Optimization — https://cs231n.github.io/optimization-1/ . Loss를 줄이는 가중치 탐색, Gradient와 경사하강법 설명을 참고했습니다.
- 모든 숫자·곡선은 `scripts/build_loss_optimizer_figures.py`에서 직접 계산한 단일 샘플 회귀 예시입니다. x=2, y=4, b=0, 초기 w=1; L(w)=(2w−4)²; Gradient=8w−16. 실제 학습 실험 결과나 모델 Benchmark가 아닙니다.
- Optimizer는 기본 SGD로 고정하고 학습률 0.025/0.1/0.3만 비교합니다. 업데이트 t=0~3을 표시하며, 증가 예시의 세로축은 0~34로 별도 표기합니다. Momentum·Weight Decay는 사용하지 않습니다.
- SVG는 NumPy/Matplotlib로 생성하며 글꼴 윤곽을 포함합니다. 재생성 환경에는 Noto Sans CJK KR 글꼴이 필요합니다. 예측값을 비교하는 Loss 그림과 가중치를 비교하는 Loss 곡선의 가로축을 구분합니다.

## Alzubaidi et al. (2021) 기반 보강

- Alzubaidi et al., Review of deep learning: concepts, CNN architectures, challenges, applications, future directions, Journal of Big Data 8, 53 (2021). https://doi.org/10.1186/s40537-021-00444-8
- Fig. 3의 특징 설계/학습 비교, Fig. 7의 CNN 흐름, CNN architectures의 연결 원리, Fig. 20의 Residual 연결, Loss·Regularization·Imbalanced data 절을 강의 흐름에 맞춰 재구성했습니다. 원본 Figure를 복제하지 않았습니다. `survey_*.svg`는 직접 작성한 도표이며 성능 측정 결과가 아닙니다.
- 자동 특징 학습: LeCun, Bengio & Hinton, Deep learning (2015). https://www.nature.com/articles/nature14539
- VGG: Simonyan & Zisserman. https://arxiv.org/abs/1409.1556
- Inception: Szegedy et al. https://openaccess.thecvf.com/content_cvpr_2015/html/Szegedy_Going_Deeper_With_2015_CVPR_paper.html
- ResNet: He et al. https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html
- Dropout: Srivastava et al. https://jmlr.org/papers/v15/srivastava14a.html
- Dropout의 매 Forward 샘플링 및 추론 동작: https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html
- CE와 클래스 가중치: https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
- Conv Shape: https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
- 정규화 및 Early Stopping: https://cs231n.github.io/neural-networks-2/
- 비교 그림의 사과는 기존 `apple_studio_preview.png` 생성 사진을 재사용했습니다. CE는 정답을 고정한 단일 샘플 L=−ln(p)의 직접 계산이며, CNN Shape와 Residual 숫자도 설명용 예시입니다.
- 생성: `scripts/build_survey_figures.py` 또는 전체 `scripts/build_lesson_revision.py`. 논문과 슬라이드의 대응·주의점은 `lectures/PAPER_REVIEW_2021.md`에 기록했습니다.

## Szeliski 3장 Image Processing 기반 보강 (2026-10-06)

- Richard Szeliski, Computer Vision: Algorithms and Applications, 1판, 3장.
  저자 공식 안내: https://szeliski.org/Book/1stEdition.htm
- Brown 강의용 3장 PDF: https://mesh.brown.edu/engn1610/szeliski/03-ImageProcessing.pdf
  이 주소의 응답 실패로 2010-09-03 교재 초안 본문을 대조했습니다.
  대학 미러: https://www.cs.ccu.edu.tw/~damon/tmp/SzeliskiBook_20100903_draft.pdf
- `processing_*.svg` 7종은 원문 Figure를 복제한 그림이 아닙니다. 기존 AI 생성 사과
  사진과 합성 잡음·이진 Mask를 실제로 필터링한 결과 및 직접 작성한 계산 도표입니다.
- Pixel/이웃 연산(3.1–3.2), Gaussian·Sobel(3.2), 중앙값(3.3.1),
  형태학(3.3.2), 축소·다중 해상도(3.5.2–3.5.3)를 강의용으로 재구성했습니다.
- OpenCV 공식 설명으로 대조: https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
  https://docs.opencv.org/4.x/d5/d0f/tutorial_py_gradients.html
  https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
  https://docs.opencv.org/4.x/d4/d1f/tutorial_pyramids.html
- 생성: `scripts/build_image_processing_figures.py` (NumPy/Pillow/SciPy).
  출처·계산 조건·현재 페이지: `lectures/SZELISKI_IMAGE_PROCESSING_REVIEW.md`.

## Intro 3 흑백 사진과 밝기 행렬 (2026-10-07)

- 기존 사과 사진을 재사용: Intro 2의 vision_task_apple_reference.jpg와 같은 사진이 포함된 docs/assets/task_classification.svg에서 읽습니다.
- Pillow로 Grayscale L(8-bit 1채널)로 변환하고 BOX 평균으로 12열×8행에 축소합니다. 중간 Pixel 영상과 오른쪽 숫자 행렬은 같은 96개 값을 사용합니다.
- 초록 테두리는 4행 6열(1부터 세는 위치), 밝기 97을 세 패널에서 연결합니다. 원본 사진의 테두리는 축소 Pixel에 대응하는 영역입니다.
- 사진 패널은 표시용 JPEG로 압축합니다. 숫자는 압축 전 원본에서 축소한 실제 8-bit 값입니다.
- 생성: scripts/build_intro_grayscale.py. 자산: docs/assets/intro_grayscale_values.svg. 외부 Figure를 복제하지 않습니다.
