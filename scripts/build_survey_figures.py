"""Build teaching diagrams informed by Alzubaidi et al. (2021).

Relationships and shapes are exact vectors; the CE curve is computed.
Photographic inputs reuse repository assets. No figure is a measured result.
"""

import base64
import html
import io
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from build_loss_optimizer_figures import configure_style, finish

REPO_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_DIR / "docs/assets/lesson"
BLUE = "#275879"
GREEN = "#36756f"
ORANGE = "#b2773d"
INK = "#17243b"
MUTED = "#64748b"
PALE = "#f2f6fa"
SVG_NS = "http://www.w3.org/2000/svg"


def label(x, y, value, size=26, color=INK, anchor="start", bold=False):
    """Place one text baseline with a consistent font size and anchor."""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{700 if bold else 400}">'
        f'{html.escape(str(value))}</text>'
    )


def box(x, y, width, height, fill=PALE, stroke="#cbd5e1"):
    """Draw an aligned panel with a thin border and small corner radius."""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>'
    )


def arrow(x1, y1, x2, y2, color=BLUE):
    """Draw a directed link with an arrowhead proportional to the line."""
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" '
        f'stroke-width="2.5" marker-end="url(#a-{color[1:]})"/>'
    )


def save_svg(name, content, description, height=480):
    """Save a self-contained accessible figure in the deployed asset folder."""
    markers = "".join(
        f'<marker id="a-{color[1:]}" markerWidth="7" markerHeight="7" '
        f'refX="6" refY="3.5" orient="auto">'
        f'<path d="M0 0 L7 3.5 L0 7Z" fill="{color}"/></marker>'
        for color in [BLUE, GREEN, ORANGE]
    )
    result = (
        f'<svg xmlns="{SVG_NS}" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 1200 {height}" '
        'font-family="Noto Sans CJK KR, Malgun Gothic, sans-serif" '
        'role="img" aria-labelledby="figure-title figure-desc">'
        f'<title id="figure-title">{html.escape(description)}</title>'
        f'<desc id="figure-desc">{html.escape(description)}</desc>'
        f'<defs>{markers}</defs><rect width="1200" height="{height}" '
        f'fill="white"/>{content}</svg>\n'
    )
    (ASSET_DIR / f"{name}.svg").write_text(result, encoding="utf-8")


def build_feature_comparison():
    """Compare designed features and jointly learned features on one input."""
    photo_path = REPO_DIR / "docs/assets/generated/apple_studio_preview.png"
    photo_buffer = io.BytesIO()
    Image.open(photo_path).convert("RGB").save(
        photo_buffer, format="JPEG", quality=92, optimize=True
    )
    photo_data = base64.b64encode(photo_buffer.getvalue()).decode("ascii")
    out = (
        '<defs><image id="apple-input" width="320" height="320" '
        f'xlink:href="data:image/jpeg;base64,{photo_data}"/></defs>'
    )
    for y, title, feature, classifier, color in [
        (55, "전통적 ML의 한 예", "사람이 특징을 설계", "분류기를 학습", BLUE),
        (260, "딥러닝의 한 예", "특징을 만드는 층", "분류하는 층", GREEN),
    ]:
        out += label(35, y, title, 27, color, bold=True)
        out += (
            f'<use xlink:href="#apple-input" '
            f'transform="translate(58 {y+18}) scale(0.390625)"/>'
        )
        for x, width, title_text in [
            (250, 340, feature), (690, 240, classifier), (1030, 140, "예측"),
        ]:
            out += box(x, y+25, width, 106)
            out += label(x+width/2, y+69, title_text, 25, color, "middle", True)
        detail = "색 비율 · 경계 · 질감" if y == 55 else "학습 가능한 특징 연산"
        out += label(420, y+108, detail, 23, MUTED, "middle")
        out += arrow(195, y+78, 235, y+78, color)
        out += arrow(605, y+78, 675, y+78, color)
        out += arrow(945, y+78, 1015, y+78, color)
    out += '<path d="M250 419 H930" stroke="#36756f" stroke-width="2"/>'
    out += label(590, 456, "같은 Loss로 특징 층과 분류 층의 가중치를 함께 학습", 25, GREEN, "middle")
    save_svg("survey_feature_learning", out, "설계한 특징과 학습하는 특징 비교")


def build_classification_loss():
    """Compute CE for a fixed class label, with no weights or smoothing."""
    configure_style()
    figure = plt.figure(figsize=(12, 4.8))
    axis = figure.add_axes([0.10, 0.22, 0.43, 0.66])
    probabilities = np.linspace(0.05, 1, 301)
    axis.plot(probabilities, -np.log(probabilities), color=BLUE, lw=2.5)
    axis.set(
        xlim=(0, 1.02), ylim=(-0.08, 3.1),
        xlabel="정답 클래스에 할당한 확률 p", ylabel="Cross-entropy Loss",
        xticks=[0, 0.2, 0.5, 0.8, 1], yticks=[0, 1, 2, 3],
    )
    axis.grid(axis="y", color="#e5eaf0", lw=0.8)
    for probability, color in [(0.2, ORANGE), (0.8, GREEN)]:
        loss = -np.log(probability)
        axis.scatter([probability], [loss], s=65, color=color, zorder=4)
        axis.annotate(
            f"p={probability:.1f}\nLoss={loss:.3f}",
            (probability, loss), xytext=(0, 22), textcoords="offset points",
            ha="center", fontsize=13, color=color,
        )
    figure.text(0.61, 0.81, "정답: 불량", fontsize=21, weight="bold")
    figure.text(0.61, 0.67, "예측 [정상 0.8, 불량 0.2]", fontsize=16)
    figure.text(0.61, 0.57, "−ln(0.2) = 1.609", fontsize=19, color=ORANGE)
    figure.text(0.61, 0.41, "예측 [정상 0.2, 불량 0.8]", fontsize=16)
    figure.text(0.61, 0.31, "−ln(0.8) = 0.223", fontsize=19, color=GREEN)
    figure.text(
        0.61, 0.12, "단일 샘플 · 정답 클래스 1개\n자연로그 · 가중치/Label smoothing 없음",
        fontsize=12, color=MUTED,
    )
    finish(figure, "survey_classification_loss")


def build_regularization():
    """Show three distinct ways to address overfitting without claiming a cure."""
    out = ""
    panels = [
        (35, "데이터 증강", ["정답을 유지하는 변화", "밝기 · 작은 회전", "Train에서만 적용"]),
        (435, "Dropout", ["학습 중 일부 값을 0으로", "예: p = 0.5", "추론에서는 Dropout 해제"]),
        (835, "Early Stopping", ["Validation을 관찰", "악화가 지속되면 중단", "좋은 시점의 모델 선택"]),
    ]
    for x, title, lines in panels:
        out += box(x, 55, 330, 315, "white")
        out += label(x+25, 105, title, 29, BLUE, bold=True)
        out += f'<path d="M{x+25} 132 H{x+305}" stroke="#cbd5e1"/>'
        for i, line in enumerate(lines):
            out += label(x+25, 190+i*62, line, 23)
    out += label(600, 432, "적용 여부와 강도는 Validation 성능으로 비교", 27, GREEN, "middle", True)
    save_svg("survey_regularization", out, "데이터 증강 Dropout Early Stopping 비교")


def build_imbalance():
    """Separate class frequency, training remedies and operational evaluation."""
    out = label(35, 42, "학습 데이터 예시: 정상 95장 · 불량 5장", 27, BLUE, bold=True)
    out += box(35, 70, 1073.5, 58, "#e8eff4", "#e8eff4")
    out += box(1108.5, 70, 56.5, 58, "#ead9c7", "#ead9c7")
    out += label(60, 108, "정상 95%", 25, BLUE, bold=True)
    out += label(1165, 163, "불량 5%", 23, ORANGE, "end", True)
    for x, title, lines in [
        (35, "표본을 조정", ["Train에서만 Sampling", "소수 클래스 노출 증가"]),
        (435, "Loss 기여를 조정", ["클래스별 가중치 적용", "빈도만으로 확정하지 않음"]),
        (835, "클래스별로 평가", ["불량 Recall · Precision", "오알람 수와 함께 확인"]),
    ]:
        out += box(x, 200, 330, 190, "white")
        out += label(x+25, 247, title, 28, BLUE, bold=True)
        for i, line in enumerate(lines):
            out += label(x+25, 300+i*48, line, 23)
    out += label(600, 443, "Test는 실제 운영의 분포를 유지하고, 설정은 Validation에서 선택", 25, GREEN, "middle")
    save_svg("survey_class_imbalance", out, "클래스 불균형의 학습 대응과 평가")


def build_cnn_pipeline():
    """Trace exact HWC shapes through a small classification CNN."""
    out = ""
    stages = [
        (35, "입력", ["RGB 이미지", "224×224×3"]),
        (270, "Conv + ReLU", ["3×3 필터 16개", "224×224×16"]),
        (505, "Max Pooling", ["2×2 · Stride 2", "112×112×16"]),
        (740, "Global Average", ["Channel별 평균", "길이 16 벡터"]),
        (975, "Linear", ["16 → 2", "클래스별 Logit"]),
    ]
    for x, title, lines in stages:
        out += box(x, 85, 190, 230, "white")
        out += label(x+95, 132, title, 23, BLUE, "middle", True)
        for i, line in enumerate(lines):
            out += label(x+95, 204+i*50, line, 22, INK, "middle")
        if x < 975:
            out += arrow(x+200, 205, x+220, 205)
    out += label(35, 370, "Conv: Stride 1 · Padding 1 · Dilation 1 · Groups 1", 25, MUTED)
    out += label(35, 417, "Global Average Pooling은 위치 전체를 평균 → 각 Channel에서 숫자 1개", 25, GREEN)
    out += label(35, 462, "분류 결과를 표시할 때는 Logit에 Softmax를 적용할 수 있습니다", 23, MUTED)
    save_svg("survey_cnn_pipeline", out, "작은 CNN 분류기의 연산과 HWC 크기")


def build_architecture_patterns():
    """Compare stacking, parallel branches and residual addition schematically."""
    out = ""
    for y, title, subtitle in [
        (35, "VGG · 순차 연결", "작은 필터를 여러 층으로"),
        (190, "Inception · 병렬 연결", "여러 경로의 특징을 결합"),
        (350, "ResNet · 우회 연결", "입력과 변환 결과를 더함"),
    ]:
        out += label(35, y+27, title, 27, BLUE, bold=True)
        out += label(35, y+64, subtitle, 23, MUTED)
    for x in [490, 735, 980]:
        out += box(x, 37, 180, 65)
        out += label(x+90, 79, "3×3 Conv", 24, BLUE, "middle", True)
        if x < 980:
            out += arrow(x+195, 70, x+230, 70)
    out += arrow(470, 232, 530, 232)
    out += '<path d="M530 197 V267 M530 197 H570 M530 267 H570" fill="none" stroke="#275879" stroke-width="2.5"/>'
    for y, name in [(168, "경로 A"), (238, "경로 B")]:
        out += box(570, y, 280, 58)
        out += label(710, y+38, name, 24, BLUE, "middle", True)
        out += arrow(865, y+29, 918, y+29)
    out += '<path d="M920 197 V267" stroke="#275879" stroke-width="2.5"/>'
    out += arrow(920, 232, 965, 232)
    out += box(980, 198, 180, 68)
    out += label(1070, 240, "Channel 결합", 22, BLUE, "middle", True)
    out += box(650, 375, 200, 65)
    out += label(750, 416, "F(x)", 28, BLUE, "middle", True)
    out += arrow(470, 408, 635, 408)
    out += arrow(865, 408, 976, 408)
    out += '<path d="M510 408 V345 H1000 V383" fill="none" stroke="#36756f" stroke-width="2.5" marker-end="url(#a-36756f)"/>'
    out += '<circle cx="1000" cy="408" r="25" fill="white" stroke="#36756f" stroke-width="2"/>'
    out += label(1000, 418, "+", 29, GREEN, "middle", True)
    out += arrow(1035, 408, 1150, 408)
    save_svg("survey_architecture_patterns", out, "CNN 구조의 순차 병렬 우회 연결 비교")


def build_residual_detail():
    """Draw elementwise residual addition and an exact illustrative example."""
    out = label(35, 35, "같은 Shape의 두 경로를 원소별로 더합니다", 27, BLUE, bold=True)
    out += box(35, 150, 165, 100, "white")
    out += label(117.5, 193, "입력 x", 27, INK, "middle", True)
    out += label(117.5, 232, "56×56×64", 23, MUTED, "middle")
    out += box(335, 150, 360, 100)
    out += label(515, 193, "변환 블록 F(x)", 29, BLUE, "middle", True)
    out += label(515, 232, "56×56×64", 25, MUTED, "middle")
    out += arrow(200, 200, 320, 200)
    out += arrow(710, 200, 830, 200)
    out += '<path d="M235 200 V105 H865 V165" fill="none" stroke="#36756f" stroke-width="2.5" marker-end="url(#a-36756f)"/>'
    out += label(550, 90, "Identity 경로: x를 그대로 전달", 25, GREEN, "middle")
    out += '<circle cx="865" cy="200" r="34" fill="white" stroke="#36756f" stroke-width="2"/>'
    out += label(865, 211, "+", 32, GREEN, "middle", True)
    out += arrow(912, 200, 1010, 200)
    out += label(1035, 190, "합산 결과", 26, INK, bold=True)
    out += label(1035, 231, "56×56×64", 23, MUTED)
    out += box(35, 315, 1130, 125, "#edf5f2")
    out += label(65, 360, "한 위치의 숫자 예시: x = 2,  F(x) = −0.5", 27)
    out += label(65, 407, "F(x) + x = 1.5     ·     Shape가 다르면 Projection 등으로 맞춤", 26, GREEN)
    save_svg("survey_residual_detail", out, "Residual 합산의 텐서 크기와 수치 예시")


def build_survey_figures() -> None:
    """Generate the seven review-informed teaching assets."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    build_feature_comparison()
    build_classification_loss()
    build_regularization()
    build_imbalance()
    build_cnn_pipeline()
    build_architecture_patterns()
    build_residual_detail()


if __name__ == "__main__":
    build_survey_figures()
