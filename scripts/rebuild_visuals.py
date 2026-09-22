"""Build self-contained lecture SVGs with measured text and explicit layout slots.

Usage: python scripts/rebuild_visuals.py --font /path/to/NotoSansCJKkr-Regular.otf
Requires Pillow and fonttools[woff]. Only generated diagram assets are overwritten.
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import math
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets"
W, H = 1200, 600
INK, MUTED, BLUE, GREEN, RED = "#17243b", "#53647b", "#2563eb", "#087f74", "#cf3e47"
PALE, BORDER = "#f4f7fc", "#d8e1ed"
TEXTS: list[dict] = []
BUILT: dict[str, str] = {}
FONT_PATH = Path()
PHOTO = ""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


class Diagram:
    def __init__(self, title: str, footer: str = ""):
        self.title = title
        self.items = [f'<rect width="{W}" height="{H}" fill="white"/>']
        self.text(32, 16, 1136, 48, title, 30, INK)
        self.line(32, 76, 1168, 76, BORDER, 1)
        if footer:
            self.rect(32, 548, 1136, 40, "#edf3fc", radius=10)
            self.text(48, 550, 1104, 36, footer, 18, MUTED, "middle")

    def add(self, markup: str) -> None:
        self.items.append(markup)

    def rect(self, x, y, w, h, fill="white", stroke="none", radius=12):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def line(self, x1, y1, x2, y2, color=MUTED, width=2, arrow=False):
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        self.add(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"{marker}/>')

    def circle(self, x, y, r, fill=BLUE, stroke="none"):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def text(self, x, y, w, h, value, size=23, color=INK, align="start"):
        """Wrap to a fixed rectangle using real font metrics; fail on overflow."""
        font = ImageFont.truetype(str(FONT_PATH), size)
        lines = []
        value = str(value).translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
        for paragraph in value.split("\n"):
            line = ""
            for char in paragraph:
                if font.getlength(line + char) > w - 12 and line:
                    lines.append(line.rstrip())
                    line = char.lstrip()
                else:
                    line += char
            lines.append(line)
        line_height = size * 1.4
        assert len(lines) * line_height <= h + 1, (self.title, value, w, h, lines)
        tx = x + w / 2 if align == "middle" else x + 4
        baseline = y + (h - len(lines) * line_height) / 2 + size * 1.1
        for i, line in enumerate(lines):
            self.add(f'<text x="{tx}" y="{baseline + i * line_height}" font-size="{size}" fill="{color}" text-anchor="{align}">{esc(line)}</text>')
            TEXTS.append({"title": self.title, "text": line, "box": [x, y, w, h], "size": size})

    def card(self, x, y, w, h, title, accent=BLUE):
        self.rect(x, y, w, h, PALE, BORDER, 16)
        self.rect(x + 20, y + 22, 5, 26, accent, radius=2)
        size = 24
        while size > 20 and ImageFont.truetype(str(FONT_PATH), size).getlength(title) > w - 68:
            size -= 1
        self.text(x + 38, y + 12, w - 56, 48, title, size)

    def photo(self, x, y, width, task="none"):
        height = width * 2 / 3
        self.add(f'<use href="#apple" xlink:href="#apple" x="{x}" y="{y}" width="{width}" height="{height}"/>')
        self.rect(x, y, width, height, "none", BORDER, 0)
        scale = width / 960
        if task == "detect":
            self.add(f'<rect x="{x+565*scale}" y="{y+197*scale}" width="{53*scale}" height="{57*scale}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
        elif task == "segment":
            self.add(f'<path transform="translate({x} {y}) scale({scale})" d="M581 201 C595 200 605 209 609 221 C614 234 606 244 594 246 C580 247 572 236 571 224 C568 213 574 204 581 201Z" fill="#38bdf8" fill-opacity=".68" stroke="{BLUE}" stroke-width="4"/>')

    def grid(self, x, y, values, cell=38, color=BLUE, numeric=True):
        maximum = max(abs(float(v)) for row in values for v in row) or 1
        for row, vals in enumerate(values):
            for col, val in enumerate(vals):
                self.rect(x + col * cell, y + row * cell, cell - 2, cell - 2, "#e9f0fc", radius=3)
                if numeric:
                    self.text(x + col*cell, y + row*cell, cell-2, cell-2, str(val), min(19, int(cell*.38)), INK, "middle")
                else:
                    self.add(f'<rect x="{x+col*cell}" y="{y+row*cell}" width="{cell-2}" height="{cell-2}" rx="3" fill="{color}" opacity="{.15+.8*abs(float(val))/maximum}"/>')

    def icon(self, kind, x, y, w, h):
        if h < 160:
            scale = min(w / 210, h / 170)
            self.add(f'<g transform="translate({x+(w-210*scale)/2} {y+(h-170*scale)/2}) scale({scale})">')
            self.icon(kind, 0, 0, 210, 170)
            self.add('</g>')
            return
        cx, cy = x + w/2, y + h/2
        if kind == "photo":
            width = min(w, h*1.5)
            self.photo(cx-width/2, cy-width/3, width)
        elif kind in {"matrix", "feature", "kernel", "heat", "depth"}:
            values = [[(r*13+c*7)%19 for c in range(5)] for r in range(5)]
            cell = min(34, h/5, w/5)
            if kind in {"heat", "depth"}:
                palette = ["#283b87", "#587dc7", "#efb952", "#f17c38", "#cb3a38"] if kind == "heat" else ["#deeafa", "#afcbed", "#71a5dc", "#3579bc", "#175082"]
                for r in range(5):
                    for c in range(5):
                        level = max(0, 4-int(math.hypot(r-2,c-2)*1.5))
                        self.rect(cx-cell*2.5+c*cell,cy-cell*2.5+r*cell,cell-2,cell-2,palette[level],radius=2)
            else:
                self.grid(cx-cell*2.5, cy-cell*2.5, values, cell, numeric=kind != "feature")
        elif kind in {"outline", "stem"}:
            self.add(f'<path d="M{cx} {cy-42} C{cx-95} {cy-87} {cx-89} {cy+48} {cx-35} {cy+62} Q{cx} {cy+78} {cx+35} {cy+62} C{cx+89} {cy+48} {cx+95} {cy-87} {cx} {cy-42}Z" fill="none" stroke="{RED}" stroke-width="4"/>')
            self.add(f'<path d="M{cx} {cy-42} L{cx-8} {cy-74}" stroke="{GREEN}" stroke-width="7" stroke-linecap="round"/>')
        elif kind in {"linear", "nonlinear"}:
            self.line(cx-88,cy+65,cx+85,cy+65);self.line(cx-88,cy+65,cx-88,cy-62)
            if kind == "linear":self.line(cx-66,cy+43,cx+69,cy-51,BLUE,4)
            else:self.add(f'<path d="M{cx-70} {cy+25} H{cx-10} L{cx+72} {cy-55}" fill="none" stroke="{BLUE}" stroke-width="4"/>')
        elif kind == "layers":
            for i in reversed(range(4)):
                self.rect(cx-62+i*11, cy-62-i*7, 110, 124, ["#dbeafe", "#a9cbfa", "#8ab8f7", "#679eed"][i], BLUE, 5)
        elif kind == "network":
            for a in range(3):
                for b in range(3):
                    self.line(cx-70, cy-54+a*54, cx, cy-54+b*54, "#bbcbe0", 1)
                    self.line(cx, cy-54+a*54, cx+70, cy, "#bbcbe0", 1)
            for xx in [cx-70, cx]:
                for yy in [cy-54, cy, cy+54]:
                    self.circle(xx, yy, 13, "#dbeafe", BLUE)
            self.circle(cx+70, cy, 16, "#c9f1e7", GREEN)
        elif kind == "label":
            self.rect(cx-85, cy-42, 170, 84, "#e0f4ec", GREEN)
            self.text(cx-75, cy-33, 150, 66, "Label\n정답", 22, GREEN, "middle")
        elif kind == "bars":
            for i, v in enumerate([.25, .48, .88]):
                self.rect(cx-80, cy-57+i*45, 160*v, 24, [BLUE, GREEN, RED][i], radius=5)
        elif kind == "update":
            self.add(f'<path d="M{cx-65} {cy+35} C{cx-70} {cy-75} {cx+60} {cy-75} {cx+65} {cy+10}" fill="none" stroke="{BLUE}" stroke-width="5" marker-end="url(#arrow)"/>')
            self.text(cx-80, cy+26, 160, 50, "Weight 갱신", 20, BLUE, "middle")
        elif kind == "scatter":
            for k, (dx, dy) in enumerate([(0,0), (90,55), (-70,40)]):
                for i in range(9):
                    self.circle(cx+dx+math.sin(i*2)*22, cy+dy+math.cos(i*3)*20, 5, [BLUE,GREEN,RED][k])
        else:
            self.rect(cx-68, cy-56, 136, 112, "#e4edfa", BLUE)
            self.text(cx-55, cy-40, 110, 80, kind, 23, BLUE, "middle")

    def save(self, name):
        body = "\n".join(self.items)
        image_def = f'<image id="apple" width="960" height="640" href="{PHOTO}" xlink:href="{PHOTO}"/>' if '#apple' in body else ""
        # A symbol supplies the correct viewBox when <use> is scaled.
        if image_def:
            image_def = f'<symbol id="apple" viewBox="0 0 960 640"><image width="960" height="640" href="{PHOTO}"/></symbol>'
        BUILT[name] = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">{esc(self.title)}</title><desc id="desc">{esc(self.title)}. 교육용 도식.</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="{MUTED}"/></marker>{image_def}</defs>__FONT__{body}</svg>'


def flow(name, title, steps, footer, loop=False):
    d = Diagram(title, footer)
    count = len(steps)
    rows = 2 if count > 4 else 1
    cols = math.ceil(count/rows)
    width = (1136-(cols-1)*40)/cols
    for i, (heading, icon, detail) in enumerate(steps):
        row, col = divmod(i, cols)
        x, y = 32+col*(width+40), (96+row*221 if rows == 2 else 114)
        height = 205 if rows == 2 else 352
        d.card(x, y, width, height, f"{i+1:02d}  {heading}")
        d.icon(icon, x+22, y+65, width-44, 73 if rows == 2 else 170)
        d.text(x+20, y+height-64, width-40, 58, detail, 19, MUTED, "middle")
        if col < cols-1 and i < count-1:
            d.line(x+width+7, y+height/2, x+width+31, y+height/2, arrow=True)
    if rows == 2:
        d.add(f'<path d="M{1168-width/2} 307 V311 H{32+width/2} V315" stroke="{MUTED}" fill="none" stroke-width="2" marker-end="url(#arrow)"/>')
    elif loop:
        d.add(f'<path d="M1060 473 V509 H140 V473" stroke="{BLUE}" fill="none" stroke-width="2" marker-end="url(#arrow)"/>')
        d.text(380, 474, 440, 32, "다음 Batch에서 반복", 18, BLUE, "middle")
    d.save(name)


def comparisons(name, title, panels, footer):
    d = Diagram(title, footer)
    n = len(panels)
    width = (1136-(n-1)*24)/n
    for i, (heading, icon, body) in enumerate(panels):
        x = 32+i*(width+24)
        d.card(x, 96, width, 432, heading, [BLUE,GREEN,RED][i%3])
        d.icon(icon, x+22, 170, width-44, 164)
        d.text(x+24, 358, width-48, 145, body, 22, MUTED, "middle")
    d.save(name)


def build_apples():
    d = Diagram("하나의 사과 이미지, 세 가지 출력", "AI 생성 사과 이미지 · 박스·마스크·점수는 설명용 예시이며 실제 추론 결과가 아닙니다.")
    tasks = [("Classification", "none", "이미지 전체의 상태", "불량 · 점수 0.98"), ("Detection", "detect", "결함의 위치", "결함 1개 · Bounding box"), ("Segmentation", "segment", "결함의 픽셀 영역", "Defect mask")]
    for i,(heading, task, question, output) in enumerate(tasks):
        x = 32+i*387
        d.card(x, 96, 362, 431, heading)
        d.photo(x+18, 176, 326, task)
        d.text(x+20, 405, 322, 42, question, 24, INK, "middle")
        d.text(x+20, 454, 322, 50, output, 21, BLUE, "middle")
    d.save("vision_tasks_comparison.svg")
    for heading, task, question, output in tasks:
        d = Diagram(f"{heading} | {question}", "동일한 960 × 640 입력 · 오버레이와 점수는 개념 설명을 위한 예시")
        d.photo(32, 104, 624, task)
        d.card(700, 104, 468, 416, "모델 출력")
        d.text(728, 184, 412, 82, output, 29, BLUE, "middle")
        details = {"none":"이미지당 하나의 클래스\n결함 위치는 출력하지 않음", "detect":"결함 클래스 + 좌표 + 점수\n박스 내부 전체가 결함은 아님", "segment":"픽셀마다 결함 여부를 구분\n면적·경계·형상 계산에 활용"}
        d.text(728, 294, 412, 100, details[task], 23, MUTED, "middle")
        d.text(728, 419, 412, 65, "학습 라벨: " + {"none":"이미지 클래스", "detect":"Bounding box", "segment":"Pixel mask"}[task], 22, GREEN, "middle")
        d.save("task_"+{"none":"classification","detect":"detection","segment":"segmentation"}[task]+".svg")
    d = Diagram("이 이미지는 무엇으로 보이나요?", "같은 이미지를 뒤에서 숫자 배열과 Vision AI의 세 가지 출력으로 다시 살펴봅니다.")
    d.photo(285, 94, 630)
    d.save("intro_question_apple.svg")
    pixels = Image.open(ASSETS / "vision_task_apple_reference.jpg").convert("RGB")
    d = Diagram("사람은 의미를, 컴퓨터는 픽셀 값을 입력받습니다", "RGB 이미지 한 장 = 높이 × 너비 × 3개 채널의 숫자 배열")
    d.card(32,96,550,432,"사람 | 사과라는 의미")
    d.photo(103,166,408)
    d.text(56,460,502,42,"색 · 윤곽 · 꼭지 · 표면 질감",24,MUTED,"middle")
    d.card(606,96,562,432,"컴퓨터 | RGB 숫자 배열")
    for c,(name,color) in enumerate([("R",RED),("G",GREEN),("B",BLUE)]):
        x=631+c*176
        d.text(x,165,160,40,name,24,color,"middle")
        vals=[[pixels.getpixel((560+col*12,198+row*12))[c] for col in range(4)] for row in range(4)]
        d.grid(x,220,vals,40)
    d.text(630,408,514,96,"오른쪽 값은 왼쪽 사진의\n결함 부근 4 × 4 지점에서 읽은 값",23,MUTED,"middle")
    d.save("intro_human_vs_computer.svg")
    d = Diagram("RGB 이미지의 데이터 구조", "960 × 640 × 3 = 1,843,200개 값 · 일반적인 8-bit 채널 값: 0~255")
    d.photo(32,145,480)
    d.line(535,310,593,310,arrow=True)
    d.card(626,96,542,432,"한 픽셀 = [R, G, B]")
    rgb=pixels.getpixel((590,225))
    d.rect(680,188,86,86,f'rgb{rgb}',radius=8)
    d.text(789,185,340,96,str(list(rgb)),30,BLUE,"middle")
    d.text(650,315,494,165,"예: image[y, x, channel]\ny = 225, x = 590\n채널 순서: R / G / B",25,MUTED)
    d.save("image_as_numbers.svg")
    d=Diagram("촬영 조건이 달라지면 픽셀도 달라집니다", "동일 사진에 밝기·크기·가림을 도식적으로 적용한 예시")
    for i,(title,kind) in enumerate([("원본","normal"),("어두운 조명","dark"),("작은 크기","small"),("일부 가림","hide")]):
        x=32+i*289
        d.card(x,108,269,416,title)
        if kind == "small":
            d.rect(x+14,192,241,161,"#ddd",radius=0)
            d.photo(x+70,235,129)
        else:
            d.photo(x+14,192,241)
        if kind=="dark": d.add(f'<rect x="{x+14}" y="192" width="241" height="161" fill="black" fill-opacity=".45"/>')
        if kind=="hide": d.rect(x+118,248,137,105,"#d5dde8",radius=0)
        d.text(x+20,390,229,106,["입력 기준","픽셀 밝기 감소","대상의 픽셀 수 감소","일부 특징 소실"][i],22,MUTED,"middle")
    d.save("apple_visual_variations.svg")


def build_specials():
    d=Diagram("AI 안에 ML, ML 안에 DL", "CNN은 Deep Learning에 속하는 신경망 구조의 한 예입니다.")
    for x,y,w,h,title,detail,color in [(32,96,1136,432,"Artificial Intelligence","판단·추론·인식 등을 수행하는 기술",BLUE),(230,211,906,285,"Machine Learning","데이터에서 패턴을 학습",GREEN),(440,331,664,137,"Deep Learning","여러 층의 신경망으로 표현을 학습",BLUE)]:
        d.rect(x,y,w,h,"#f0f5fc",color)
        d.text(x+24,y+13,w-48,45,title,28,color)
        d.text(x+24,y+65,w-48,47,detail,23,MUTED)
    d.save("ai_ml_dl.svg")
    d=Diagram("입력 × 가중치 → 가중합 → 활성화 → 출력", "예: x = [0.8, 0.2], w = [0.5, −0.5], b = −0.1 → z = 0.2 → 계단함수 출력 1")
    for i,(label,detail) in enumerate([("입력 x","0.8\n0.2"),("가중합 z","0.8 × 0.5\n+ 0.2 × (−0.5) − 0.1"),("활성화","z ≥ 0이면 1\nz < 0이면 0"),("출력","1")]):
        x=32+i*290
        d.card(x,148,266,323,label)
        d.text(x+18,239,230,160,detail,23,BLUE,"middle")
        if i<3:d.line(x+271,310,x+284,310,arrow=True)
    d.save("perceptron.svg")
    d=Diagram("AND는 직선으로 분리, XOR는 비선형 경계가 필요", "파란 점: 출력 1 · 흰 점: 출력 0 · XOR의 대각선 두 점은 직선 하나로 분리할 수 없음")
    for k,title in enumerate(["AND", "XOR"]):
        x=32+k*580
        d.card(x,96,556,432,title)
        ox,oy=x+145,431
        d.line(ox-30,oy,ox+260,oy,arrow=True);d.line(ox,oy+25,ox,oy-245,arrow=True)
        for a,b in [(0,0),(0,1),(1,0),(1,1)]:
            value=int(a and b) if k==0 else a^b
            d.circle(ox+a*205,oy-b*205,14,BLUE if value else "white",BLUE)
            d.text(ox+a*205-22,oy-b*205+18,44,32,str(value),18,INK,"middle")
        d.text(ox+240,oy-10,40,35,"x₁",18); d.text(ox-18,oy-277,60,35,"x₂",18)
        if k==0:d.line(ox+100,oy-240,ox+245,oy-95,RED,3)
        else:
            d.add(f'<path d="M{ox-25} {oy-100} Q{ox+100} {oy-105} {ox+107} {oy-235} M{ox+103} {oy+25} Q{ox+113} {oy-100} {ox+245} {oy-107}" fill="none" stroke="{RED}" stroke-width="3"/>')
    d.save("and_xor_linear_separability.svg")
    d=Diagram("활성화가 없으면 여러 층도 하나의 아핀 변환", "ReLU 같은 비선형 활성화가 있어야 복잡한 결정 경계를 표현할 수 있습니다.")
    for i, label in enumerate(["입력 x","W₁x + b₁","W₂h + b₂","출력 y"]):
        x=32+i*290
        d.rect(x,132,266,112,PALE,BORDER)
        d.text(x+14,154,238,66,label,28,BLUE,"middle")
        if i<3:d.line(x+273,189,x+284,189,arrow=True)
    d.rect(118,300,964,203,"#f0f8f5",GREEN)
    d.text(145,326,910,64,"W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂)",27,GREEN,"middle")
    d.text(145,402,910,66,"결국 y = W*x + b* 한 층으로 합칠 수 있음",29,INK,"middle")
    d.save("linear_layers_collapse.svg")
    d=Diagram("같은 위치에서 곱하고 더하면 출력 한 칸", "단일 채널 예시 · 5 × 5 입력, 3 × 3 커널, stride 1, padding 0 → 3 × 3 출력")
    vals=[[0,0,1,1,1] for _ in range(5)]
    kernel=[[-1,0,1] for _ in range(3)]
    for x,w,title in [(32,360,"입력 5 × 5"),(420,360,"커널 3 × 3"),(808,360,"출력 3 × 3")]: d.card(x,96,w,432,title)
    d.grid(88,184,vals,50)
    d.rect(86,182,150,150,"none",RED,0)
    d.grid(492,193,kernel,72)
    d.grid(880,193,[[3,3,0]]*3,72)
    d.rect(878,191,72,72,"none",RED,0)
    d.text(57,451,310,52,"빨간 영역이 첫 계산 위치",20,MUTED,"middle")
    d.text(446,431,308,74,"한 행: 0×(−1) + 0×0 + 1×1\n세 행의 합 = 3",19,MUTED,"middle")
    d.text(834,446,308,58,"같은 커널을 오른쪽·아래로 이동",19,MUTED,"middle")
    d.save("convolution_visual.svg")
    d=Diagram("Filter마다 하나의 출력 Feature Map", "3 × 3 convolution · stride 1 · padding 1 · 입력 3채널을 함께 계산하는 Filter 64개")
    for x,title,kind,detail in [(32,"입력","photo","224 × 224 × 3"),(420,"64개 Filter","layers","각 Filter: 3 × 3 × 3"),(808,"출력","layers","224 × 224 × 64")]:
        d.card(x,110,360,404,title)
        d.icon(kind,x+45,197,270,188)
        d.text(x+20,427,320,57,detail,24,BLUE,"middle")
        if x<808:d.line(x+368,312,x+378,312,arrow=True)
    d.save("feature_maps.svg")
    d=Diagram("깊은 층의 한 위치는 더 넓은 입력을 봅니다", "3 × 3 커널, stride 1, dilation 1을 연속 적용한 이론적 수용영역 예시")
    for i,(title,n) in enumerate([("Layer 1",3),("Layer 2",5),("Layer 3",7)]):
        x=32+i*387
        d.card(x,96,362,432,title)
        d.grid(x+60,185,[[1]*9]*9,27,color="#c5cfdd",numeric=False)
        off=(9-n)/2*27
        color=[BLUE,GREEN,RED][i]
        d.add(f'<rect x="{x+60+off}" y="{185+off}" width="{n*27-2}" height="{n*27-2}" fill="{color}" fill-opacity=".24" stroke="{color}" stroke-width="4"/>')
        d.text(x+24,450,314,54,f"수용영역 {n} × {n}",26,[BLUE,GREEN,RED][i],"middle")
    d.save("receptive_field.svg")
    d=Diagram("Batch와 Epoch를 작은 수로 세어봅시다", "drop_last=False, gradient accumulation 없음 · Batch마다 Optimizer Step 1회인 예시")
    d.card(32,96,1136,432,"이미지 10장 / batch_size = 4")
    for i,n in enumerate([4,4,2]):
        x=74+i*370
        d.rect(x,200,330,178,"#e8f0fc",BORDER)
        for j in range(n):d.rect(x+24+j*72,231,60,64,"#a9cafa",BLUE,5)
        d.text(x+18,313,294,46,f"Batch {i+1}: {n}장",24,BLUE,"middle")
    d.text(84,415,1032,77,"10장을 모두 사용 → 3 Iterations → 1 Epoch",31,INK,"middle")
    d.save("batch_epoch.svg")
    d=Diagram("학습·선택·최종평가 데이터를 분리합니다", "예: 클래스별 70 / 15 / 15 · 같은 원본 영상·중복 이미지가 서로 다른 Split에 섞이지 않도록 그룹 분리")
    for x,w,color,title,detail in [(32,630,BLUE,"Train · 70%","가중치 학습"),(686,229,GREEN,"Val · 15%","모델·설정 선택"),(939,229,RED,"Test · 15%","최종 성능 확인")]:
        d.rect(x,136,w,170,color)
        d.text(x+12,160,w-24,72,title,27,"white","middle")
        d.text(x+12,237,w-24,48,detail,21,"white","middle")
    d.text(55,361,1090,146,"전체 1,000장이라면 700 / 150 / 150장\n클래스 비율을 확인하고, 희귀 클래스가 평가셋에서 사라지지 않게 점검\nTest 결과를 보고 반복해서 모델을 선택하면 평가가 편향됨",24,MUTED,"middle")
    d.save("dataset_split.svg")
    d=Diagram("학습 성능이 좋아도 새 데이터 성능은 다를 수 있습니다", "과적합: 학습 데이터에 지나치게 맞춤 · 누수: 평가 데이터의 정보가 학습·선택 과정에 유입")
    d.card(32,96,550,432,"과적합 | Loss 변화 예시")
    d.line(98,423,512,423,arrow=True); d.line(98,423,98,192,arrow=True)
    d.add(f'<path d="M108 205 C200 340 270 400 498 407" fill="none" stroke="{BLUE}" stroke-width="4"/><path d="M108 220 C230 360 290 400 365 330 S450 250 498 211" fill="none" stroke="{RED}" stroke-width="4"/>')
    d.text(124,167,280,32,"Loss (작을수록 좋음)",18,MUTED)
    d.text(375,435,150,40,"Epoch",20,MUTED)
    d.text(128,473,400,35,"파랑 Train / 빨강 Validation",21,MUTED)
    d.card(606,96,562,432,"누수 | 같은 영상의 인접 프레임")
    for i,title in enumerate(["Train", "Test"]):
        d.photo(628+i*272,188,246)
        d.text(630+i*272,366,242,46,title,27,[BLUE,RED][i],"middle")
    d.text(630,425,514,77,"거의 같은 이미지로 평가하면\n실제 일반화 성능보다 높게 보일 수 있음",22,MUTED,"middle")
    d.save("overfit_leakage.svg")
    d=Diagram("기울기를 계산하고, 반대 방향으로 한 걸음", "w_new = w_old − learning_rate × gradient · learning rate가 너무 크면 발산할 수 있음")
    d.card(32,96,550,432,"Loss 곡선의 예시")
    d.line(96,453,520,453,arrow=True);d.line(96,453,96,173,arrow=True)
    d.add(f'<path d="M135 191 Q305 665 500 191" fill="none" stroke="{BLUE}" stroke-width="4"/>')
    d.circle(461,277,10,RED);d.line(451,288,411,330,RED,3,True)
    d.text(123,465,380,37,"가중치 w",21,MUTED,"middle")
    d.card(606,96,562,432,"숫자로 계산하면")
    d.text(634,180,506,250,"현재 w = 1.0\nGradient = 0.4\nLearning rate = 0.1\n갱신: 1.0 − 0.1 × 0.4 = 0.96",26,INK)
    d.save("gradient_update.svg")


def build_remaining():
    flows = [
        ("vision_ai_pipeline.svg","현장에서 판단까지",[("촬영","photo","카메라가 장면을 기록"),("숫자화","matrix","픽셀 × 채널"),("모델 분석","network","학습한 패턴으로 예측"),("활용","bars","판정 · 측정 · 제어")],"센서 입력과 모델 출력을 구분하면 문제 정의가 명확해집니다."),
        ("intro_to_learning.svg","숫자에서 특징을, 특징에서 판단을",[("이미지","photo","RGB 이미지 입력"),("특징 추출","feature","색 · 경계 · 질감 표현"),("학습된 모델","network","Weight에 학습 결과 저장"),("출력","bars","예: 불량 점수 0.98")],"사진과 점수는 개념 설명용 예시입니다."),
        ("vision_task_selection.svg","Output → Label → Task → Model",[("필요한 정보","면적?","예: 결함의 면적"),("정답의 형태","label","픽셀별 결함 마스크"),("문제 유형","Mask","Segmentation"),("모델·평가","network","분할 모델 / IoU 등")],"질문에 맞는 출력을 정한 뒤 라벨·모델·평가 지표를 선택합니다."),
        ("feature_representation.svg","입력을 판단에 유용한 표현으로 바꿉니다",[("입력","photo","RGB 픽셀"),("초기 특징","feature","경계 · 국소 패턴"),("특징 조합","layers","질감 · 부분 구조"),("내부 표현","bars","분류에 사용하는 벡터")],"Feature는 유용한 단서, Representation은 그 단서를 담은 숫자 표현입니다."),
        ("cnn_hierarchy.svg","작은 패턴을 조합해 더 복잡한 특징으로",[("Pixel","matrix","색 · 밝기"),("국소 패턴","feature","경계 · 반복 무늬"),("부분 조합","layers","질감 · 형상"),("Task 특징","network","예측에 유용한 표현")],"이해를 돕는 도식이며, 각 채널이 항상 사람이 이름 붙일 수 있는 특징과 대응하지는 않습니다."),
        ("cnn_flow.svg","CNN의 특징 추출 흐름",[("입력","photo","224 × 224 × 3"),("Convolution","kernel","국소 영역의 곱과 합"),("Activation","ReLU","비선형 변환"),("Feature Maps","layers","다음 층의 입력")],"여러 층을 쌓아 공간 정보를 조합합니다. 크기·채널 수는 모델 설계에 따라 달라집니다."),
        ("training_loop.svg","예측 → 오차 → 기울기 → 가중치 갱신",[("Forward","network","입력으로 예측 계산"),("Loss","label","예측과 정답 비교"),("Backward","bars","Gradient 계산"),("Optimizer","update","가중치 갱신")],"지도학습 예시 · 같은 과정을 Mini-batch마다 반복합니다."),
        ("cnn_training.svg","CNN의 Kernel도 학습되는 가중치입니다",[("Forward","kernel","Kernel로 특징 계산"),("Loss","label","예측과 라벨 비교"),("Backward","bars","Kernel의 기울기 계산"),("Optimizer","update","Kernel Weight 갱신")],"학습할 때 가중치를 갱신하고, 추론할 때는 학습된 가중치를 사용합니다."),
        ("vision_project_pipeline.svg","현장 문제부터 운영까지",[("문제 정의","출력?","필요한 판단 정의"),("데이터·라벨","label","기준과 Split 설계"),("학습","network","모델 가중치 최적화"),("평가","bars","새 조건에서 검증"),("배포","모델","운영 시스템 연결"),("모니터링","update","변화 감지·데이터 보강")],"운영 결과를 바탕으로 문제 정의와 데이터를 다시 점검합니다."),
        ("ml_workflow.svg","모델 학습은 전체 과정의 한 단계",[("수집","photo","현장을 대표하는 데이터"),("탐색","scatter","분포·품질 확인"),("전처리","matrix","입력과 라벨 정리"),("학습","network","Train으로 가중치 학습"),("평가","bars","Val 선택 / Test 평가"),("운영","update","배포·모니터링")],"전처리 통계도 Train에서 계산하고 Val / Test에는 같은 변환을 적용합니다."),
    ]
    for name,title,steps,footer in flows:flow(name,title,steps,footer, "training" in name)
    comparisons("rule_vs_ml.svg","규칙을 작성하거나, 데이터에서 학습하거나",[("Rule-based","matrix","사람이 조건을 설계\n예: 밝기 < 100이면 후보\n조건이 명확한 문제에 활용"),("Machine Learning","network","데이터로 Weight를 학습\n예: 이미지 + 정상/불량 라벨\n여러 특징을 조합해 판단")],"두 방식은 함께 사용할 수도 있습니다. 어느 방식이든 현장 조건에서 검증이 필요합니다.")
    comparisons("learning_types.svg","지도학습과 비지도학습의 차이",[("지도학습","label","입력 + 정답 Label\n예측과 정답을 비교하며 학습\n예: 정상/불량 분류"),("비지도학습","scatter","정답 Label 없는 입력\n유사성·군집·구조를 탐색\n군집의 의미는 사람이 해석")],"강화학습은 이번 강의 범위에서 제외합니다.")
    comparisons("unsupervised_learning.svg","라벨 없이 데이터의 구조를 찾습니다",[("입력 데이터","photo","정답 라벨이 없는 이미지\n예: 제품 표면 이미지"),("구조 탐색","scatter","특징이 비슷한 샘플끼리 군집\n이름이 아닌 유사성을 발견"),("결과 해석","bars","군집별 패턴 확인\n특이 샘플을 검토 후보로 사용")],"이상 탐지가 모두 비지도학습인 것은 아닙니다. 정상 데이터만 쓰는 One-class 등도 존재합니다.")
    comparisons("supervised_unsupervised_industry.svg","산업 데이터에서의 활용",[("지도학습 | 정답 활용","label","Class → 정상/불량 분류\nBox → 결함 위치 검출\nMask → 결함 영역 분할"),("비지도학습 | 구조 탐색","scatter","유사한 표면 패턴 묶기\n새로운 유형의 샘플 탐색\n라벨링 전 데이터 구조 이해")],"라벨의 유무와 학습 목적을 구분하고, 이상 후보는 후속 검증으로 의미를 확인합니다.")
    comparisons("supervised_tasks.svg","같은 지도학습, 다른 정답의 형태",[("분류 Classification","label","정답은 범주\n정상 / 불량\n모델은 클래스별 점수 출력"),("회귀 Regression","bars","정답은 연속적인 값\n예: 거리 12.4 mm\n모델은 수치를 예측")],"Detection과 Segmentation도 Box·Mask 정답을 이용한 지도학습으로 많이 학습합니다.")
    comparisons("classification_regression.svg","범주를 고르는가, 숫자를 예측하는가?",[("Classification","photo","입력: 제품 이미지\n출력 예: 불량\n클래스 점수 0.98"),("Regression","bars","입력: 이미지 또는 센서값\n출력 예: 길이 12.4 mm\n연속적인 수치")],"점수·수치는 설명용 예시입니다. 이미지로 실제 길이를 구하려면 보정 등의 조건이 필요합니다.")
    comparisons("problem_to_task.svg","현장의 질문을 Vision Task로 바꿉니다",[("정상인가?","photo","Classification\n이미지 전체의 상태\nClass label"),("어디에 있는가?","layers","Detection\n결함의 위치\nBounding box"),("어디까지 결함인가?","feature","Segmentation\n결함의 영역·형상\nPixel mask")],"같은 원본 이미지라도 필요한 출력과 라벨의 형태가 달라집니다.")
    comparisons("human_visual_cues.svg","사람은 여러 시각 단서를 함께 봅니다",[("색과 밝기","photo","표면의 붉은색\n명암과 반사"),("윤곽과 구조","outline","둥근 외형\n꼭지와 움푹한 부분"),("표면 패턴","feature","반복되는 무늬\n주변과 다른 어두운 반점")],"사람의 시각 처리와 CNN의 계산 구조가 동일하다는 뜻은 아닙니다.")
    comparisons("human_feature_to_cnn.svg","특징을 조합한다는 직관",[("사람의 인식","photo","색 · 형태 · 질감 · 꼭지\n여러 단서를 함께 해석\n“사과처럼 보인다”"),("CNN의 계산","network","Convolution + Activation\n여러 층의 숫자 표현 조합\nTask에 필요한 출력 계산")],"유사한 직관을 설명하는 그림이며 인간 시각과 CNN의 작동 원리는 같지 않습니다.")
    comparisons("visual_generalization.svg","처음 보는 조건에서도 의미를 찾아야 합니다",[("학습 데이터","photo","다양한 촬영 조건\n밝기·거리·가림 등 포함"),("학습","network","판단에 유용한 패턴을 학습\n배경만 외우지 않도록 주의"),("새 입력 평가","label","미사용 영상·조건으로 평가\n현장 데이터에서 검증")],"Generalization: 학습에 사용하지 않은 데이터에서도 유효하게 판단하는 능력")
    comparisons("linear_vs_nonlinear.svg","활성화가 표현력을 바꿉니다",[("아핀 변환","linear","예: y = 2x + 1\n여러 번 합성해도 아핀 변환\n직선형 경계의 한계"),("비선형 활성화 ReLU","nonlinear","ReLU(x) = max(0, x)\n음수는 0, 양수는 그대로\nLinear 층과 조합해 표현력 확장")],"층을 쌓는 것만으로 충분하지 않습니다. 비선형 변환이 핵심입니다.")
    d=Diagram("센서는 서로 다른 종류의 정보를 기록합니다", "센서별 개념도 · Thermal은 보정 조건에 따라 온도를 추정하고, Event는 밝기 변화 이벤트를 기록")
    sensors=[("RGB","photo","색과 형태"),("Mono","matrix","밝기 한 채널"),("NIR","feature","근적외선 반사"),("Thermal","heat","열복사 정보"),("Depth / LiDAR","depth","거리 지도 / 3D 점"),("Event","scatter","시각·위치·변화 극성")]
    for i,(title,kind,detail) in enumerate(sensors):
        x,y=32+(i%3)*387,96+(i//3)*222
        d.card(x,y,362,207,title)
        d.icon(kind,x+20,y+69,136,112)
        d.text(x+170,y+73,169,112,detail,22,MUTED,"middle")
    d.save("sensor_overview.svg")


def main():
    global FONT_PATH, PHOTO
    parser=argparse.ArgumentParser()
    parser.add_argument("--font",type=Path,required=True)
    args=parser.parse_args()
    FONT_PATH=args.font
    PHOTO="data:image/jpeg;base64,"+base64.b64encode((ASSETS/"vision_task_apple_reference.jpg").read_bytes()).decode()
    build_apples();build_specials();build_remaining()
    characters="".join(t["text"] for t in TEXTS)
    font=TTFont(FONT_PATH)
    missing = set(characters) - set(map(chr, font.getBestCmap())) - {"\n"}
    assert not missing, f"Missing glyphs: {missing}"
    options=subset.Options()
    sub=subset.Subsetter(options=options)
    sub.populate(text=characters)
    sub.subset(font)
    font.flavor="woff"
    buf=io.BytesIO();font.save(buf)
    font_data=base64.b64encode(buf.getvalue()).decode()
    font_css=f'<style>@font-face{{font-family:Lecture;src:url(data:font/woff;base64,{font_data}) format("woff")}}text{{font-family:Lecture,"Noto Sans CJK KR","Malgun Gothic",sans-serif}}</style>'
    import xml.etree.ElementTree as ET
    for name,svg in BUILT.items():
        svg=svg.replace("__FONT__",font_css)
        ET.fromstring(svg)
        (ASSETS/name).write_text(svg,encoding="utf-8")
        mirror=ROOT/"assets/diagrams"/name
        if mirror.exists():mirror.write_text(svg,encoding="utf-8")
    for page in (ROOT / "docs").glob("*.html"):
        markup = page.read_text(encoding="utf-8")
        markup = re.sub(r'(src="assets/[^"?]+\.svg)(?:\?[^" ]*)?"',
                        r'\1?v=visual-20260922"', markup)
        markup = re.sub(r'((?:href|src)="slide\.(?:css|js))(?:\?[^" ]*)?"',
                        r'\1?v=visual-20260922"', markup)
        page.write_text(markup, encoding="utf-8")
    print(f"Built {len(BUILT)} diagrams; measured {len(TEXTS)} text lines; embedded {len(buf.getvalue())} byte font.")


if __name__ == "__main__":
    main()
