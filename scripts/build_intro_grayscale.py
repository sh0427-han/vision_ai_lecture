"""Build Intro page 3 from the existing apple photo and its actual gray values.

Read the repository's embedded photo, convert to one channel, and reduce with
BOX averaging to 12 columns × 8 rows. Every displayed number is the resulting
8-bit pixel value. Requires Pillow, NumPy and lxml.
"""
import base64
import io
from pathlib import Path

import numpy as np
from lxml import etree
from PIL import Image

from build_survey_figures import BLUE, GREEN, MUTED, label, box

REPO_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_DIR / "docs/assets/task_classification.svg"
OUTPUT_PATH = REPO_DIR / "docs/assets/intro_grayscale_values.svg"
IMAGE_COLUMNS = 12
IMAGE_ROWS = 8
SELECTED_ROW = 3
SELECTED_COLUMN = 5


def grayscale_images():
    """Return the original gray photo and its 12×8 integer pixel matrix."""
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
    """Draw aligned photo, actual pixel mosaic, and corresponding values."""
    grayscale, values = grayscale_images()
    photo_x, mosaic_x, table_x = 20, 380, 748
    photo_y, table_y = 132, 94
    photo_width, photo_height, cell = 320, 320*2/3, 36
    pixel_width, pixel_height = photo_width/12, photo_height/8
    selected_value = int(values[SELECTED_ROW, SELECTED_COLUMN])
    content = label(180, 53, "흑백 사진 · 1채널", 27, BLUE, "middle", True)
    content += label(540, 53, "12×8 Pixel로 축소", 27, BLUE, "middle", True)
    content += label(964, 53, "같은 위치의 밝기 값", 27, BLUE, "middle", True)
    content += embed_image(grayscale, photo_x, photo_y, photo_width, photo_height)
    for row in range(IMAGE_ROWS):
        for column in range(IMAGE_COLUMNS):
            value = int(values[row, column])
            shade = f"rgb({value},{value},{value})"
            content += (
                f'<rect x="{mosaic_x+column*pixel_width}" '
                f'y="{photo_y+row*pixel_height}" width="{pixel_width}" '
                f'height="{pixel_height}" fill="{shade}" stroke="#ffffff" '
                'stroke-opacity="0.2" stroke-width="0.6"/>'
            )
            x, y = table_x+column*cell, table_y+row*cell
            content += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{shade}" stroke="#ffffff" stroke-opacity="0.75" stroke-width="1"/>'
            content += label(x+cell/2, y+24, value, 18,
                             "white" if value < 135 else "#17243b", "middle")
    for x in [photo_x, mosaic_x]:
        content += (
            f'<rect x="{x+SELECTED_COLUMN*pixel_width}" '
            f'y="{photo_y+SELECTED_ROW*pixel_height}" width="{pixel_width}" '
            f'height="{pixel_height}" fill="none" stroke="{GREEN}" stroke-width="3"/>'
        )
    content += f'<rect x="{table_x+SELECTED_COLUMN*cell}" y="{table_y+SELECTED_ROW*cell}" width="{cell}" height="{cell}" fill="none" stroke="{GREEN}" stroke-width="3"/>'
    for x1, x2 in [(346, 365), (706, 731)]:
        content += f'<path d="M{x1} 239 H{x2}" stroke="{BLUE}" stroke-width="2" marker-end="url(#arrow)"/>'
    content += label(180, 387, "앞 장과 같은 사과 사진", 23, MUTED, "middle")
    content += label(540, 387, "각 칸에 밝기 값 하나", 23, MUTED, "middle")
    content += label(964, 413, "8행 × 12열 = 96개 값", 23, MUTED, "middle")
    content += box(20, 432, 1160, 49, "#f2f6fa")
    content += label(45, 463, "0 = 검정  ·  255 = 흰색", 24, BLUE)
    content += label(1149, 463,
                     f"초록 테두리: 4행 6열  ·  밝기 {selected_value}",
                     24, GREEN, "end", True)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 500" '
        'font-family="Noto Sans CJK KR, Malgun Gothic, sans-serif" '
        'role="img" aria-labelledby="title desc">'
        '<title id="title">흑백 사과 사진과 실제 12×8 밝기 값의 대응</title>'
        '<desc id="desc">동일한 사과 사진을 한 채널로 변환하고 12열 8행으로 '
        '축소한 뒤 각 Pixel의 실제 밝기 값을 표시합니다. 초록 테두리는 '
        f'같은 위치인 4행 6열, 밝기 {selected_value}를 가리킵니다.</desc>'
        f'<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" '
        f'refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="{BLUE}"/>'
        '</marker></defs><rect width="1200" height="500" fill="white"/>'
        f'{content}</svg>\n'
    )
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"12×8 = {values.size} values; selected brightness = {selected_value}")


if __name__ == "__main__":
    build_intro_grayscale()
