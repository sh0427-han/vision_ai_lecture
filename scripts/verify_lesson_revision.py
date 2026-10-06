"""Verify lesson structure, diagram paths, numeric examples and SVG resources."""
from pathlib import Path
import json
import re

import numpy as np
from lxml import etree, html

REPO_DIR = Path(__file__).resolve().parents[1]
manifest = json.loads((REPO_DIR / "docs/assets/lesson/manifest.json").read_text())
SVG_NS = "http://www.w3.org/2000/svg"
for name in ["ai_basics", "vision_ai"]:
    doc = html.parse(str(REPO_DIR / f"docs/{name}.html"))
    slides = doc.xpath('//section[contains(concat(" ", @class, " "), " slide ")]')
    assert len(slides) == len(manifest[name]) + 1
    assert len(doc.xpath('//section[contains(@class,"active")]')) == 1
    assert len(doc.xpath('//*[@data-slide-next]')) == 1
    assert len(doc.xpath('//*[@data-slide-prev]')) == 1
    for index, slide in enumerate(slides[1:], 1):
        assert slide.xpath('string(.//div[@class="lesson-meta"]/span[1])').startswith(f"{index:02d} · ")
        assert len(slide.xpath('.//h2')) == 1
        assert len(slide.xpath('.//img')) == 1
        assert slide.get("data-level") in {"basic", "detail"}
    for item in doc.xpath('//*[@src or @href]'):
        link = item.get("src") or item.get("href")
        if link.startswith(("https:", "#")):
            continue
        path = REPO_DIR / "docs" / link.split("?")[0]
        assert path.exists(), path
    for entry in manifest[name]:
        assert entry["number"] > 0
        assert (REPO_DIR / "docs" / entry["asset"]).exists()
    print(name, len(slides), "slides, contiguous numbers and local paths verified")

for path in (REPO_DIR / "docs/assets/lesson").glob("*.svg"):
    root = etree.parse(str(path)).getroot()
    assert root.tag == f"{{{SVG_NS}}}svg"
    assert len(root.get("viewBox").split()) == 4
    identifiers = {element.get("id") for element in root.iter() if element.get("id")}
    for element in root.iter():
        for key, value in element.attrib.items():
            if key.endswith("href"):
                assert value.startswith(("#", "data:")), (path, value)
                if value.startswith("#"):
                    assert value[1:] in identifiers
    assert not root.findall(f".//{{{SVG_NS}}}script")

image = np.array([[1, 2, 3, 0, 1], [4, 5, 6, 1, 0], [7, 8, 9, 2, 1],
                  [0, 1, 2, 3, 1], [1, 0, 1, 2, 3]])
kernel = np.array([[1, 0, -1]] * 3)
output = [[int((image[y:y+3, x:x+3] * kernel).sum()) for x in range(3)]
          for y in range(3)]
assert output == [[-6, 12, 16], [-6, 8, 15], [-4, 2, 7]]
for x1 in [0, 1]:
    for x2 in [0, 1]:
        assert int(x1+x2 >= 1.5) == (x1 & x2)
assert np.isclose((2*1.8-4)**2, .16)
assert np.isclose(1-.1*(-8), 1.8)
assert np.isclose(1.8*2+.4, 4)
assert np.isclose(18/22, .81818181818)
assert np.isclose(36/42, .85714285714)
assert (12+12-4) == 20
for stride, padding, expected in [(1, 0, 3), (1, 1, 5), (2, 0, 2)]:
    assert (5+2*padding-3)//stride+1 == expected
assert 64*3*3*3 == 1728
print("SVG XML/resources, AND, convolution, gradients, IoU and metrics verified")
