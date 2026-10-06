"""Create exact, publication-style figures for the four loss/optimizer slides.

The same scalar regression example is used throughout: x=2, y=4, b=0.
Dependencies: matplotlib, numpy. SVG labels are paths for portable rendering.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

REPO_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_DIR / "docs/assets/lesson"
X = 2.0
TARGET = 4.0
INITIAL_WEIGHT = 1.0
LEARNING_RATES = (0.025, 0.1, 0.3)
UPDATE_COUNT = 3
BLUE = "#275879"
GREEN = "#36756f"
ORANGE = "#b2773d"
INK = "#17243b"
MUTED = "#64748b"
GRID = "#e5eaf0"


def squared_error(weight: np.ndarray | float) -> np.ndarray | float:
    """Return the single-sample squared error for the fixed input and target."""
    return (X * weight - TARGET) ** 2


def gradient(weight: float) -> float:
    """Differentiate squared error with respect to the one trainable weight."""
    return 2 * X * (X * weight - TARGET)


def weight_history(learning_rate: float, steps: int) -> np.ndarray:
    """Apply vanilla SGD without momentum, decay, or a changing learning rate."""
    values = [INITIAL_WEIGHT]
    for _ in range(steps):
        values.append(values[-1] - learning_rate * gradient(values[-1]))
    return np.array(values)


def configure_style() -> None:
    """Use a local CJK font when available; embed outlines in the final SVG."""
    local_font = Path.home() / ".local/share/fonts/lecture-NotoSansCJKkr-Regular.otf"
    if local_font.exists():
        font_manager.fontManager.addfont(str(local_font))
    plt.rcParams.update({
        "font.family": ["Noto Sans CJK KR", "DejaVu Sans"],
        "font.size": 15,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.edgecolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "loss-optimizer-20261006",
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })


def finish(figure: plt.Figure, name: str) -> None:
    """Save the exact figure without timestamps or an external font dependency."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    figure.savefig(ASSET_DIR / f"{name}.svg", metadata={"Date": None})
    plt.close(figure)


def add_loss_curve(axis: plt.Axes, show_minimum: bool = True) -> None:
    """Draw a labeled one-dimensional slice, with the same scale on both slides."""
    weights = np.linspace(0.4, 3.6, 301)
    axis.plot(weights, squared_error(weights), color=BLUE, lw=2.5)
    axis.set(xlim=(0.4, 3.6), ylim=(-0.25, 10.8),
             xlabel="가중치 w", ylabel="Loss  L(w)",
             xticks=[1, 2, 3], yticks=[0, 2, 4, 6, 8, 10])
    axis.grid(axis="y", color=GRID, lw=0.8)
    if show_minimum:
        axis.scatter([2], [0], color=GREEN, s=55, zorder=4)
        axis.annotate("최솟값: w = 2", (2, 0), xytext=(2, 0.65),
                      fontsize=13, color=GREEN, ha="center",
                      bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})


def build_loss() -> None:
    """Separate prediction error from the scalar objective used in training."""
    figure = plt.figure(figsize=(12, 5.2))
    left = figure.add_axes([0.09, 0.23, 0.39, 0.61])
    predictions = [2.0, 3.6, 4.0]
    positions = [2, 1, 0]
    colors = [ORANGE, BLUE, GREEN]
    for prediction, position, color in zip(predictions, positions, colors):
        left.plot([prediction, TARGET], [position, position], color=color,
                  lw=5, solid_capstyle="butt")
        left.scatter([prediction], [position], s=95, color=color, zorder=4)
        left.annotate(f"차이 {prediction - TARGET:g}",
                      ((prediction + TARGET) / 2, position),
                      xytext=(0, 13), textcoords="offset points",
                      ha="center", color=color, fontsize=14)
    left.axvline(TARGET, color=INK, lw=1.6, ls=(0, (4, 4)))
    left.text(TARGET, 2.68, "정답 y = 4", ha="center", fontsize=16)
    left.set(xlim=(1.5, 4.6), ylim=(-0.55, 2.8),
             xlabel="예측값", xticks=[2, 3, 4],
             yticks=positions, yticklabels=["예측 2", "예측 3.6", "예측 4"])
    left.spines["left"].set_visible(False)
    left.tick_params(axis="y", length=0)
    left.set_title("(a) 정답과 예측 사이의 차이", loc="left", pad=30,
                   fontsize=17, fontweight="bold")
    right = figure.add_axes([0.54, 0.22, 0.43, 0.63])
    right.axis("off")
    right.text(0, 1.01, "(b) 제곱오차로 Loss 계산", fontsize=17,
               fontweight="bold", transform=right.transAxes)
    table = right.table(
        cellText=[["2", "2 − 4 = −2", "(−2)² = 4"],
                  ["3.6", "3.6 − 4 = −0.4", "(−0.4)² = 0.16"],
                  ["4", "4 − 4 = 0", "0² = 0"]],
        colLabels=["예측", "오차", "Loss"], cellLoc="center",
        colWidths=[0.17, 0.4, 0.43], bbox=[0, 0.08, 1, 0.8],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        cell.set_facecolor("#edf2f6" if row == 0 else "#f8fafc")
        if row == 0:
            cell.set_text_props(weight="bold", color=BLUE)
        elif column == 2:
            cell.set_text_props(weight="bold", color=colors[row - 1])
    figure.text(0.5, 0.055,
                "같은 정답에 대한 후보 예측 비교  ·  Loss = (예측 − 정답)²",
                ha="center", fontsize=16, color=BLUE)
    finish(figure, "loss_basic")


def build_gradient(detailed: bool = False) -> None:
    """Distinguish the local tangent from the actual finite parameter update."""
    figure = plt.figure(figsize=(12, 5.2))
    left = figure.add_axes([0.09, 0.20, 0.46, 0.66])
    add_loss_curve(left, show_minimum=not detailed)
    left.scatter([1], [4], color=ORANGE, s=95, zorder=5)
    left.annotate("현재: (w=1, Loss=4)", (1, 4), xytext=(1.35, 6.7),
                  fontsize=14, color=ORANGE,
                  arrowprops={"arrowstyle": "-", "color": ORANGE})
    if detailed:
        new_weight = weight_history(0.1, 1)[-1]
        left.scatter([new_weight], [squared_error(new_weight)], color=GREEN,
                     s=95, zorder=5)
        left.annotate("수정 후: (1.8, 0.16)", (new_weight, 0.16),
                      xytext=(2.1, 5.2), fontsize=14, color=GREEN,
                      bbox={"facecolor": "white", "edgecolor": "none", "pad": 1},
                      arrowprops={"arrowstyle": "-", "color": GREEN})
        left.annotate("", (1.8, 0.8), (1, 0.8),
                      arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 2})
        left.text(1.4, 1.35, "Δw = +0.8", ha="center", fontsize=14, color=GREEN)
    else:
        local_weights = np.linspace(0.65, 1.35, 50)
        left.plot(local_weights, 4 + gradient(1) * (local_weights - 1),
                  color=ORANGE, lw=2.1, ls=(0, (5, 3)))
        left.annotate("접선의 기울기 = −8", (0.75, 6),
                      xytext=(1.6, 8.8), fontsize=14, color=ORANGE,
                      arrowprops={"arrowstyle": "-", "color": ORANGE})
    right = figure.add_axes([0.62, 0.17, 0.35, 0.69])
    right.axis("off")
    if detailed:
        lines = [("① Gradient 계산", BLUE),
                 ("dL/dw = 8w − 16 = −8", INK),
                 ("② SGD로 가중치 갱신", BLUE),
                 ("w′ = w − η × Gradient", INK),
                 ("= 1 − 0.1 × (−8) = 1.8", GREEN),
                 ("③ 예측과 Loss 재계산", BLUE),
                 ("ŷ′ = 2 × 1.8 = 3.6", INK),
                 ("L′ = (3.6 − 4)² = 0.16", GREEN)]
        sizes = [16, 15, 16, 15, 15, 16, 15, 15]
        ys = [0.97, 0.85, 0.66, 0.54, 0.43, 0.24, 0.12, 0.01]
    else:
        lines = [("무엇이 바뀌나요?", BLUE),
                 ("x=2, y=4는 고정", INK),
                 ("가중치 w를 바꾸며 Loss 확인", INK),
                 ("현재 기울기가 음수", BLUE),
                 ("w가 조금 커지면 Loss는 감소", INK),
                 ("수정 방향: w를 증가", GREEN)]
        sizes = [17, 15, 15, 17, 15, 17]
        ys = [0.97, 0.81, 0.68, 0.43, 0.27, 0.02]
    for (label, color), y, size in zip(lines, ys, sizes):
        right.text(0, y, label, fontsize=size, color=color,
                   fontweight="bold" if color == BLUE else "normal")
    figure.text(0.5, 0.035, "동일 예제: x = 2, y = 4, b = 0  ·  L(w) = (2w − 4)²",
                ha="center", fontsize=15, color=MUTED)
    finish(figure, "gradient_detail" if detailed else "gradient_basic")


def build_optimizer() -> None:
    """Show calculated loss trajectories, holding SGD and all other inputs fixed."""
    figure, axes = plt.subplots(1, 3, figsize=(12, 5.2))
    figure.subplots_adjust(left=0.07, right=0.98, bottom=0.29,
                           top=0.76, wspace=0.36)
    titles = ["η = 0.025  |  느린 감소", "η = 0.1  |  빠른 감소",
              "η = 0.3  |  Loss 증가"]
    for axis, rate, color, title in zip(axes, LEARNING_RATES,
                                        [BLUE, GREEN, ORANGE], titles):
        weights = weight_history(rate, UPDATE_COUNT)
        losses = squared_error(weights)
        axis.plot(range(UPDATE_COUNT + 1), losses, color=color, lw=2.4,
                  marker="o", markersize=7)
        axis.set(xlim=(-0.1, 3.15), xticks=[0, 1, 2, 3],
                 xlabel="업데이트 횟수 t", ylabel="Loss",
                 ylim=(0, 34) if rate == 0.3 else (0, 4.5))
        axis.grid(axis="y", color=GRID)
        axis.set_title(title, fontsize=16, color=color, pad=15,
                       fontweight="bold")
        axis.annotate(f"{losses[-1]:.4g}", (3, losses[-1]),
                      xytext=(-5, 12), textcoords="offset points",
                      ha="right", color=color, fontsize=14)
        axis.text(0.5, -0.33,
                  f"1회: w = {weights[1]:g}\nLoss = {losses[1]:g}",
                  ha="center", va="top", transform=axis.transAxes,
                  fontsize=15, color=color)
    figure.text(0.5, 0.94, "SGD:  wₜ₊₁ = wₜ − η × Gradient", ha="center",
                fontsize=21, color=BLUE)
    figure.text(0.5, 0.84, "같은 시작 w₀ = 1 · 같은 Loss · 학습률 η만 변경",
                ha="center", fontsize=15, color=MUTED)
    figure.text(0.5, 0.025, "t=0은 갱신 전  ·  오른쪽 그래프의 세로축 범위는 다릅니다",
                ha="center", fontsize=13, color=MUTED)
    finish(figure, "optimizer_learning_rates")


def build_loss_optimizer_figures() -> None:
    """Build the four figures after verifying the underlying scalar calculations."""
    assert np.isclose(gradient(1), -8)
    assert np.isclose(weight_history(0.1, 1)[-1], 1.8)
    assert np.isclose(squared_error(1.8), 0.16)
    assert np.isclose(squared_error(weight_history(0.3, 1)[-1]), 7.84)
    for rate in LEARNING_RATES:
        # Independent closed-form solution of this quadratic update recurrence.
        expected = 2 + (INITIAL_WEIGHT - 2) * (1 - 8 * rate) ** np.arange(4)
        assert np.allclose(weight_history(rate, UPDATE_COUNT), expected)
    configure_style()
    build_loss()
    build_gradient()
    build_gradient(detailed=True)
    build_optimizer()


if __name__ == "__main__":
    build_loss_optimizer_figures()
