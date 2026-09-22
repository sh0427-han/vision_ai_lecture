"""Validate SVG resources and optionally render contact sheets for visual review."""
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    assets = sorted((ROOT / "docs/assets").glob("*.svg"))
    for path in assets:
        tree = ET.parse(path)
        root = tree.getroot()
        assert root.attrib["viewBox"] == "0 0 1200 600", path
        for element in root.iter():
            for key, value in element.attrib.items():
                if key.endswith("href"):
                    assert value.startswith(("#", "data:")), (path, value)
            if element.tag == SVG + "text":
                assert 0 <= float(element.attrib["x"]) <= 1200, path
                assert 0 <= float(element.attrib["y"]) <= 600, path
        if "task_" in path.name or path.name == "vision_tasks_comparison.svg":
            if path.name != "vision_task_selection.svg":
                assert "data:image/jpeg;base64," in path.read_text(), path
        mirror = ROOT / "assets/diagrams" / path.name
        if mirror.exists():
            assert path.read_bytes() == mirror.read_bytes(), path
    links = 0
    for path in (ROOT / "docs").glob("*.html"):
        for value in re.findall(r'(?:src|href)="([^"#]+)"', path.read_text()):
            if value.startswith(("http:", "https:", "data:", "mailto:")):
                continue
            target = value.split("?", 1)[0].split("#", 1)[0]
            assert (path.parent / target).exists(), (path, target)
            links += 1
    print(f"PASS: {len(assets)} valid self-contained SVGs; {links} local HTML links.")
    if args.render_dir:
        import cairosvg
        args.render_dir.mkdir(parents=True, exist_ok=True)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
        for index, path in enumerate(assets):
            output = args.render_dir / (path.stem + ".png")
            # Cairo does not implement web fonts; use the same installed source font.
            markup = re.sub(r'text\{font-family:[^}]+\}',
                            'text{font-family:"Noto Sans CJK KR"}', path.read_text())
            cairosvg.svg2png(bytestring=markup.encode(), write_to=str(output),
                            output_width=1200, output_height=600)
        for start in range(0, len(assets), 6):
            sheet = Image.new("RGB", (1200, 990), "#e2e8f0")
            draw = ImageDraw.Draw(sheet)
            for i, path in enumerate(assets[start:start+6]):
                preview = Image.open(args.render_dir / (path.stem + ".png")).convert("RGB")
                preview.thumbnail((590, 295))
                x, y = (i % 2)*600, (i // 2)*330
                sheet.paste(preview, (x+5, y+28))
                draw.text((x+8, y+5), path.name, fill="#17243b", font=font)
            sheet.save(args.render_dir / f"contact_{start//6+1}.jpg")
        print("Rendered all diagrams and contact sheets.")


if __name__ == "__main__":
    main()
