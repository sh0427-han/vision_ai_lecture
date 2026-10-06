"""Reproducible image-processing examples based on Szeliski, chapter 3.

All filters are actually evaluated. Photos reuse an existing AI-generated
teaching asset; noise and binary masks are deterministic synthetic examples.
Requires numpy, Pillow and scipy. No textbook figure is copied.
"""
import base64
import io

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

from build_survey_figures import REPO_DIR, BLUE, GREEN, ORANGE, MUTED, label, box, arrow, save_svg

PATCH = np.array([[80, 82, 79], [81, 160, 80], [78, 83, 77]])
SEED = 1610
SECTIONS = {
    "processing_point_neighborhood": "§3.1–3.2",
    "processing_gaussian": "§3.2.2",
    "processing_mean_detail": "§3.2",
    "processing_median": "§3.3.1",
    "processing_gradient": "§3.2.1–3.2.2",
    "processing_morphology": "§3.3.2",
    "processing_pyramid": "§3.5.2–3.5.3",
}


def grayscale_input():
    rgba = Image.open(REPO_DIR / "docs/assets/generated/apple_studio_preview.png").convert("RGBA")
    rgb = Image.alpha_composite(Image.new("RGBA", rgba.size, "white"), rgba).convert("RGB")
    # Explicit luminance coefficients; work in float before filtering/clipping.
    return np.asarray(rgb, dtype=float) @ np.array([.299, .587, .114])


def image_panel(array, x, title, subtitle, y=85, size=280, nearest=False):
    buf = io.BytesIO()
    img = Image.fromarray(np.clip(np.rint(array), 0, 255).astype("uint8"))
    img.save(buf, format="PNG", optimize=True)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    rendering = 'style="image-rendering:pixelated"' if nearest else ''
    return (label(x+size/2, y-27, title, 26, BLUE, "middle", True)
            + box(x, y, size, size, "white")
            + f'<image x="{x}" y="{y}" width="{size}" height="{size}" {rendering} '
            f'xlink:href="data:image/png;base64,{encoded}"/>'
            + label(x+size/2, y+size+35, subtitle, 22, MUTED, "middle"))


def three_panels(name, arrays, titles, subtitles, footer, description):
    out = "".join(image_panel(a, x, t, s, nearest=name == "processing_morphology") for a, x, t, s in
                  zip(arrays, [55, 460, 865], titles, subtitles))
    out += label(600, 454, footer, 24, GREEN, "middle")
    save_svg(name, out, description)


def mask_examples():
    mask = np.zeros((40, 40), dtype=bool)
    mask[10:30, 10:30] = True
    mask[19, 19] = False
    mask[5, 7] = mask[33, 33] = True
    structure = np.ones((3, 3), dtype=bool)
    return mask, ndi.binary_opening(mask, structure), ndi.binary_closing(mask, structure)


def build_image_processing_figures():
    image = grayscale_input()
    three_panels("processing_point_neighborhood",
                 [image, np.clip(image+30, 0, 255), ndi.uniform_filter(image, 7, mode="reflect")],
                 ["입력 영상", "밝기 변환 · 한 Pixel", "평균 필터 · 주변 Pixel"],
                 ["0–255의 밝기 값", "g(x,y) = min(f(x,y)+30, 255)", "7×7 이웃을 평균"],
                 "한 칸의 값을 바꾸는 연산과, 이웃을 함께 보는 연산을 구분합니다.",
                 "동일한 사과 영상의 원본, 밝기 증가, 7×7 평균 필터 결과")

    rng = np.random.default_rng(SEED)
    noisy = np.clip(image+rng.normal(0, 20, image.shape), 0, 255)
    # Same enlarged boundary crop in all three panels, making loss of detail visible.
    crop = (slice(55, 215), slice(35, 195))
    three_panels("processing_gaussian",
                 [a[crop] for a in [noisy, ndi.gaussian_filter(noisy, 1, mode="reflect"),
                                     ndi.gaussian_filter(noisy, 3, mode="reflect")]],
                 ["잡음을 더한 입력", "Gaussian · σ = 1", "Gaussian · σ = 3"],
                 ["합성 Gaussian 잡음 · 표준편차 20", "주변을 거리 가중치로 평균", "잡음과 함께 작은 변화도 감소"],
                 "같은 경계 영역을 확대했습니다. 강한 평활화는 세부 정보도 흐리게 합니다.",
                 "고정 시드 Gaussian 잡음과 두 강도의 Gaussian 필터를 같은 경계 확대 영역에서 비교")

    out = label(200, 55, "(a) 입력 3×3 영역", 26, BLUE, "middle", True)
    out += label(600, 55, "(b) 평균 필터", 26, BLUE, "middle", True)
    out += label(1010, 55, "(c) 출력 중심 한 칸", 26, BLUE, "middle", True)
    for i in range(3):
        for j in range(3):
            x, y = 80+j*80, 85+i*80
            out += box(x, y, 80, 80, "#f7e9d9" if (i,j)==(1,1) else "#f2f6fa")
            out += label(x+40, y+49, PATCH[i,j], 27, ORANGE if (i,j)==(1,1) else BLUE, "middle")
            x = 480+j*80
            out += box(x, y, 80, 80)
            out += label(x+40, y+49, "1/9", 26, GREEN, "middle")
    out += arrow(350, 205, 450, 205) + arrow(750, 205, 860, 205)
    out += box(890, 135, 235, 140, "#eef5f3")
    out += label(1007, 193, "800 / 9", 32, GREEN, "middle", True)
    out += label(1007, 239, "≈ 88.9", 32, GREEN, "middle", True)
    out += label(200, 368, "中心 160도 이웃과 함께 평균", 23, MUTED, "middle")
    out = out.replace("中心", "중심")
    out += label(600, 368, "가중치 합 = 1", 23, MUTED, "middle")
    out += label(1007, 368, "반올림한 8-bit 출력: 89", 23, MUTED, "middle")
    out += label(600, 443, "g(x,y) = Σᵢ Σⱼ h(i,j) f(x+i,y+j)  ·  입력과 가중치를 곱한 뒤 합산", 25, GREEN, "middle")
    save_svg("processing_mean_detail", out, "3×3 평균 필터의 가중합 계산: 합 800, 평균 88.9, 반올림 89")

    impulse = image.copy()
    choice = np.random.default_rng(SEED+1).random(image.shape)
    impulse[choice < .025] = 0
    impulse[choice > .975] = 255
    three_panels("processing_median",
                 [a[crop] for a in [impulse, ndi.uniform_filter(impulse, 3, mode="reflect"),
                                    ndi.median_filter(impulse, 3, mode="reflect")]],
                 ["점 잡음이 있는 입력", "평균 필터 · 3×3", "중앙값 필터 · 3×3"],
                 ["검정·흰색 합성 잡음 · 약 5%", "극단값도 평균에 포함", "이웃 값을 정렬해 가운데 선택"],
                 "앞의 9개 숫자: 평균 88.9 / 중앙값 80  ·  같은 입력에서도 계산 방식이 다릅니다.",
                 "같은 점 잡음 영상에 적용한 평균 필터와 중앙값 필터의 확대 비교")

    smooth = ndi.gaussian_filter(image, 1, mode="reflect")
    gx, gy = ndi.sobel(smooth, axis=1, mode="reflect"), ndi.sobel(smooth, axis=0, mode="reflect")
    magnitude = np.hypot(gx, gy)
    scale = max(float(magnitude.max()), 1)
    three_panels("processing_gradient", [image, np.abs(gx)/scale*255, magnitude/scale*255],
                 ["입력 밝기", "좌우 변화 · |Gₓ|", "전체 변화 · √(Gₓ²+Gᵧ²)"],
                 ["밝기 영상 · 0–255", "세로 방향 경계에서 큰 반응", "밝을수록 변화가 큰 위치"],
                 "영상 기울기: 위치 x·y에 대한 밝기 변화  ≠  Loss 기울기: 가중치에 대한 오차 변화",
                 "Sobel 좌우 미분과 영상 기울기 크기: 공통 최댓값으로 표시 범위를 정규화")

    masks = mask_examples()
    three_panels("processing_morphology", [m.astype(float)*255 for m in masks],
                 ["입력 Mask", "Opening · 열기", "Closing · 닫기"],
                 ["흰색=1 · 점 2개와 구멍 1개", "침식 → 팽창 · 작은 점 제거", "팽창 → 침식 · 작은 구멍 채움"],
                 "두 결과는 각각 같은 입력에서 계산  ·  3×3 정사각형 구조 요소  ·  바깥은 0",
                 "40×40 합성 이진 마스크의 열기와 닫기 연산을 동일한 입력에서 각각 비교")

    # Full centered square image resized to the pedagogical 224 input.
    levels = [np.asarray(Image.fromarray(image.astype("uint8")).resize((224,224), Image.Resampling.LANCZOS), dtype=float)]
    for _ in range(2):
        levels.append(ndi.gaussian_filter(levels[-1], 1, mode="reflect")[::2, ::2])
    out = ""
    for x, a, title in zip([65, 490, 915], levels, ["L₀ · 224×224", "L₁ · 112×112", "L₂ · 56×56"]):
        # Common display size exposes the decreasing resolution, with explicit label.
        out += image_panel(a, x, title, f"Pixel 수: {a.size:,}", size=224, nearest=True)
    out += arrow(310, 196, 460, 196) + arrow(735, 196, 885, 196)
    out += label(385, 153, "평활화", 23, GREEN, "middle")
    out += label(385, 253, "2칸마다 추출", 22, MUTED, "middle")
    out += label(810, 153, "평활화", 23, GREEN, "middle")
    out += label(810, 253, "2칸마다 추출", 22, MUTED, "middle")
    out += box(90, 365, 1020, 81)
    out += label(600, 400, "Lₖ₊₁(x,y) = (Gaussian σ=1로 평활화한 Lₖ)(2x,2y)", 25, GREEN, "middle", True)
    out += label(600, 432, "서로 다른 해상도를 비교하도록 세 영상을 같은 화면 크기로 표시", 22, MUTED, "middle")
    save_svg("processing_pyramid", out, "Gaussian 피라미드의 224,112,56 해상도와 평활화 후 2배 축소 계산")


if __name__ == "__main__":
    build_image_processing_figures()
