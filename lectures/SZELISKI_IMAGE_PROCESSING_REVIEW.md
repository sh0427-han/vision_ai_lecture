# Szeliski 3장 기반 영상처리 강의 보강

사용자가 제공한 자료는 독립 논문이 아니라 Richard Szeliski의
*Computer Vision: Algorithms and Applications* 3장 Image Processing입니다.
[Brown 강의 PDF](https://mesh.brown.edu/engn1610/szeliski/03-ImageProcessing.pdf)는
이번 확인에서 응답하지 않아, 같은 교재의 2010-09-03 초안 본문으로 개념과 절 번호를
대조했습니다. [저자 공식 1판 페이지](https://szeliski.org/Book/1stEdition.htm)와
[교재 초안의 대학 미러](https://www.cs.ccu.edu.tw/~damon/tmp/SzeliskiBook_20100903_draft.pdf)를
참조했습니다. 원문 PDF나 그림을 저장소에 재게시하지 않습니다.

## 출처와 슬라이드 대응

페이지는 표지를 포함합니다. Vision AI는 30장에서 37장으로 확장했습니다.

| Vision AI 페이지 | 내용 | 교재 절 | 그림 자산 |
| --- | --- | --- | --- |
| 9 | Pixel 단위 변환과 이웃 연산 | 3.1–3.2 | processing_point_neighborhood.svg |
| 10 | Gaussian 평활화와 세부 손실 | 3.2.2 | processing_gaussian.svg |
| 11 (상세) | 평균 필터의 3×3 가중합 | 3.2, 식 3.12 | processing_mean_detail.svg |
| 12 | 평균과 중앙값의 점 잡음 처리 비교 | 3.3.1 | processing_median.svg |
| 13 | Sobel 반응과 영상 기울기 크기 | 3.2.1–3.2.2 | processing_gradient.svg |
| 14 | 이진 Mask의 Opening·Closing | 3.3.2 | processing_morphology.svg |
| 24 (상세) | Gaussian 피라미드와 축소 | 3.5.2–3.5.3 | processing_pyramid.svg |

앞의 여섯 장은 IoU 이후, CNN 이전에 배치했습니다. 피라미드는 기존 Max Pooling
뒤에 배치해 공간 크기 감소라는 공통점과 계산 방식의 차이를 설명합니다.
Fourier·Wavelet·변분 최적화의 상세 전개는 이번 입문 강의 확장에 포함하지 않았습니다.

## 자산과 계산 조건

기존 `docs/assets/generated/apple_studio_preview.png`를 재사용했습니다.
투명 영역은 먼저 흰 배경에 합성하고 밝기를 0.299R+0.587G+0.114B로 계산합니다.
이 사진은 AI 생성 교육용 자산이며 결과는 모델 성능이나 실제 실험 데이터가 아닙니다.

- 밝기 변환: 30을 더한 뒤 255에서 잘라냅니다. 비교 평균 필터는 7×7입니다.
- Gaussian 예시: NumPy 시드 1610, 표준편차 20의 잡음을 더하고 0–255에서 잘라냅니다.
  같은 입력에 σ=1과 σ=3을 적용합니다. 160×160의 같은 영역을 확대해 비교합니다.
  σ는 원본 Pixel 단위입니다. SciPy 기본 truncate=4.0, 경계는 reflect입니다.
- 평균 상세: `[80,82,79; 81,160,80; 78,83,77]`의 합은 800입니다.
  평균은 800/9≈88.9, 8-bit 반올림 출력은 89, 중앙값은 80입니다.
- 중앙값 예시: 시드 1611, 각 2.5% 확률로 0과 255를 부여한 점 잡음을 사용합니다.
  약 5%라는 표시는 설정 확률입니다. 3×3 평균과 3×3 중앙값을 같은 입력에 적용합니다.
- Sobel: Gaussian σ=1 평활화 후 Gx·Gy를 계산합니다. 커널 배율은 SciPy 기본값
  (별도 1/8 정규화 없음)입니다. 계산은 부호 있는 실수로 하며 표시할 때만 절댓값과
  sqrt(Gx²+Gy²)를 씁니다. 두 결과는 전체 기울기 크기의 동일 최대값으로 표시합니다.
- Mask: 40×40의 이진 배열, 20×20 전경에 1칸 구멍과 분리된 점 2개입니다.
  3×3 정사각형 구조 요소, 바깥 0을 사용합니다. 열기와 닫기는 원래 입력에서 각각
  계산합니다. 흰색은 전경 1입니다. 전경 수는 입력 401, 열기 399, 닫기 402입니다.
- 피라미드: 입력 사진을 Lanczos로 224×224로 준비한 뒤 각 단계에서 σ=1 평활화,
  `[::2, ::2]` 표본 추출을 반복해 112×112, 56×56을 얻습니다.
  사진 비교는 동일한 화면 크기와 최근접 표시를 사용합니다. 일반적인 피라미드의
  한 구현 예시이며 특정 라이브러리의 pyrDown과 동일한 커널이라고 주장하지 않습니다.

필터는 부동소수점으로 계산하고 그림에 넣을 때만 반올림·클리핑합니다.
모든 자산은 자기완결 SVG에 결과 PNG를 포함하며 외부 이미지 서버에 의존하지 않습니다.

## 설명 검토와 검증

고정 필터와 학습 필터, 영상 좌표에 대한 기울기와 가중치에 대한 Loss 기울기,
Gaussian 피라미드와 Max Pooling을 구분했습니다. 경계는 의미 있는 결함의 정답이
아니며, 평활화·중앙값·형태학은 작은 실제 결함까지 제거할 수 있음을 설명합니다.

`scripts/build_image_processing_figures.py`에 계산과 그림 생성 조건을 보관했습니다.
의존성: NumPy, Pillow, SciPy 및 기존 전체 생성기의 Matplotlib, lxml.
`scripts/verify_lesson_revision.py`는 평균·중앙값의 손계산, 상수 영상의 Gaussian
보존, Sobel 선형 램프 반응, Mask 포함관계·점 제거·구멍 채움, 피라미드 Shape,
출처 링크·슬라이드 번호·자산 경로·SVG 참조를 검증합니다.

보조 공식 문서:
[OpenCV 필터](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html),
[영상 기울기](https://docs.opencv.org/4.x/d5/d0f/tutorial_py_gradients.html),
[형태학](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html),
[이미지 피라미드](https://docs.opencv.org/4.x/d4/d1f/tutorial_pyramids.html).
