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
assert np.isclose(-np.log(0.2), 1.6094379124341003)
assert np.isclose(-np.log(0.8), 0.2231435513142097)
assert (224+2*1-3)//1+1 == 224
assert (224-2)//2+1 == 112
assert 2+(-0.5) == 1.5
assert 1073.5/1130 == 0.95
for name in ["ai_basics", "vision_ai"]:
    for entry in manifest[name]:
        if Path(entry["asset"]).stem.startswith("survey_"):
            slide = html.parse(str(REPO_DIR / f"docs/{name}.html")).xpath(
                '//section[contains(concat(" ", @class, " "), " slide ")]'
            )[entry["number"]]
            refs = slide.xpath('.//p[@class="lesson-reference"]//a/@href')
            assert "https://link.springer.com/article/10.1186/s40537-021-00444-8" in refs
            assert len(refs) >= 2
print("SVG XML/resources, AND, convolution, gradients, IoU and metrics verified")
print("Survey sources, cross-entropy, CNN shapes, class ratio and residual sum verified")

# Check the actual filter routines against hand-calculated independent results.
from scipy import ndimage as ndi
from build_image_processing_figures import PATCH, SECTIONS, mask_examples
assert PATCH.sum() == 800
assert np.isclose(ndi.uniform_filter(PATCH.astype(float), 3)[1, 1], 800/9)
assert ndi.median_filter(PATCH, 3)[1, 1] == 80
constant = np.full((15, 15), 80.0)
assert np.allclose(ndi.gaussian_filter(constant, 1), constant)
assert np.allclose(ndi.sobel(constant, axis=1), 0)
ramp = np.tile(np.arange(15, dtype=float), (15, 1))
assert np.allclose(ndi.sobel(ramp, axis=1)[1:-1, 1:-1], 8)
assert np.allclose(ndi.sobel(ramp, axis=0), 0)
original, opened, closed = mask_examples()
assert [int(a.sum()) for a in (original, opened, closed)] == [401, 399, 402]
assert opened[19, 19] == 0 and closed[19, 19] == 1
assert not opened[5, 7] and closed[5, 7]
assert np.all(opened <= original) and np.all(closed >= original)
assert [a[::2, ::2].shape for a in (np.zeros((224,224)), np.zeros((112,112)))] == [(112,112), (56,56)]
vision_slides = html.parse(str(REPO_DIR / "docs/vision_ai.html")).xpath('//section[contains(concat(" ", @class, " "), " slide ")]')
processing = [item for item in manifest["vision_ai"] if Path(item["asset"]).stem in SECTIONS]
assert len(processing) == 7
for item in processing:
    refs = vision_slides[item["number"]].xpath('.//p[@class="lesson-reference"]//a/@href')
    assert "https://szeliski.org/Book/1stEdition.htm" in refs
print("Szeliski sources, mean/median, Gaussian DC, Sobel ramp, mask opening/closing and pyramid shapes verified")
