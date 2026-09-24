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
