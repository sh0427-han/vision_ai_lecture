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
- Intro 10 활용 이미지: 스마트폰·CCTV·블랙박스 / 로봇청소기·자율주행 / 열화상 검사·비접촉 온도 측정.

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
