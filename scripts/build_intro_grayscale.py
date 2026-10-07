"""Build Intro page 3 from the existing apple photo and its actual gray values.

Read the repository's embedded photo, convert to one channel, and reduce with
BOX averaging to 48 columns × 32 rows. Every displayed number is the resulting
8-bit pixel value. Requires Pillow, NumPy and lxml.
"""
import base64
import io
from pathlib import Path

import numpy as np
from lxml import etree
from PIL import Image

from build_survey_figures import BLUE, MUTED, label, box

REPO_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_DIR / "docs/assets/task_classification.svg"
OUTPUT_PATH = REPO_DIR / "docs/assets/intro_grayscale_values.svg"
IMAGE_COLUMNS = 48
IMAGE_ROWS = 32


def grayscale_images():
    """Return the original gray photo and its 48×32 integer pixel matrix."""
    root = etree.parse(str(SOURCE_PATH))
    image = root.find(".//{http://www.w3.org/2000/svg}image")
    source = image.get("href") or image.get("{http://www.w3.org/1999/xlink}href")
    photo = Image.open(io.BytesIO(base64.b64decode(source.split(",", 1)[1])))
    rgba = photo.convert("RGBA")
    rgb = Image.alpha_composite(Image.new("RGBA", rgba.size, "white"), rgba)
    grayscale = rgb.convert("RGB").convert("L")
    small = grayscale.resize((IMAGE_COLUMNS, IMAGE_ROWS), Image.Resampling.BOX)
    return grayscale, np.asarray(small)


def embed_image(photo, x, y, width, height):
    """Embed the same gray source as a display-only compressed photograph."""
    buffer = io.BytesIO()
    photo.resize((480, 320), Image.Resampling.LANCZOS).save(
        buffer, format="JPEG", quality=92, optimize=True
    )
    data = base64.b64encode(buffer.getvalue()).decode("ascii")
    return (f'<image x="{x}" y="{y}" width="{width}" height="{height}" '
            f'xlink:href="data:image/jpeg;base64,{data}"/>')


def build_intro_grayscale():
    """Draw photo → plain numbers → the same values mapped to brightness."""
    grayscale, values = grayscale_images()
    photo_x, table_x, pixel_x = 20, 292, 748
    panel_y, panel_width, panel_height = 94, 432, 288
    cell_width = panel_width / IMAGE_COLUMNS
    cell_height = panel_height / IMAGE_ROWS
    content = label(130, 53, "흑백 사진 · 1채널", 24, BLUE, "middle", True)
    content += label(508, 53, "컴퓨터가 받는 숫자", 25, BLUE, "middle", True)
    content += label(964, 53, "숫자를 밝기로 표현", 25, BLUE, "middle", True)
    content += embed_image(grayscale, photo_x, 165, 220, 220*2/3)
    # Equal physical panels and equal row/column spacing; numeric background
    # stays completely white and all digits have the same ink color.
    for x in [table_x, pixel_x]:
        content += (
            f'<rect x="{x}" y="{panel_y}" width="{panel_width}" '
            f'height="{panel_height}" fill="white" stroke="#cbd5e1"/>'
        )
    content += '<g font-size="4.5" fill="#17243b" text-anchor="middle">'
    for row in range(IMAGE_ROWS):
        for column in range(IMAGE_COLUMNS):
            x = table_x + (column + .5)*cell_width
            y = panel_y + (row + .5)*cell_height + 1.6
            value = int(values[row, column])
            content += f'<text x="{x}" y="{y}">{value}</text>'
    content += '</g>'
    pixel_buffer = io.BytesIO()
    Image.fromarray(values).save(pixel_buffer, format="PNG", optimize=True)
    pixel_data = base64.b64encode(pixel_buffer.getvalue()).decode("ascii")
    content += (
        f'<image x="{pixel_x}" y="{panel_y}" width="{panel_width}" '
        f'height="{panel_height}" style="image-rendering:pixelated" '
        f'xlink:href="data:image/png;base64,{pixel_data}"/>'
    )
    for x1, x2 in [(253, 280), (728, 741)]:
        content += (
            f'<path d="M{x1} 238 H{x2}" stroke="{BLUE}" '
            'stroke-width="2" marker-end="url(#arrow)"/>'
        )
    content += label(130, 415, "앞 장과 같은 사진", 22, MUTED, "middle")
    content += label(508, 415, "32행 × 48열 = 1,536개 값", 22, MUTED, "middle")
    content += label(964, 415, "같은 행·열의 값을 밝기로 표시", 22, MUTED, "middle")
    content += box(20, 444, 1160, 44, "#f2f6fa")
    content += label(600, 474, "0 = 검정  ·  255 = 흰색  ·  숫자가 클수록 밝습니다", 24, BLUE, "middle")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 500" '
        'font-family="Noto Sans CJK KR, Malgun Gothic, sans-serif" '
        'role="img" aria-labelledby="title desc">'
        '<title id="title">흑백 사진, 48×32 숫자 배열, 밝기 영상의 대응</title>'
        '<desc id="desc">사과 사진을 48열 32행으로 축소해 얻은 1536개 밝기 '
        '값을 중앙에 검정 숫자로 표시합니다. 오른쪽 영상은 같은 값과 같은 '
        '행·열의 위치를 밝기로 표시합니다. 두 패널의 크기는 같습니다.</desc>'
        f'<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" '
        f'refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="{BLUE}"/>'
        '</marker></defs><rect width="1200" height="500" fill="white"/>'
        f'{content}</svg>\n'
    )
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"{IMAGE_COLUMNS}×{IMAGE_ROWS} = {values.size} corresponding values")


if __name__ == "__main__":
    build_intro_grayscale()
