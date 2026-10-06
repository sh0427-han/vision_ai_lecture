"""Build exact SVG teaching figures and beginner/detail slide sequences.

Requires lxml, numpy and Pillow. Run from any directory; output stays in this repo.
All numeric figures are calculated here rather than painted by image generation.
"""

from __future__ import annotations

import html
import json
import base64
from pathlib import Path

import numpy as np
from lxml import etree

REPO_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_DIR / "docs/assets/lesson"
VERSION = "professional-20261006-2"
BLUE = "#275879"
GREEN = "#36756f"
ORANGE = "#b2773d"
INK = "#17243b"
MUTED = "#64748b"
FONT_FAMILY = "'Noto Sans CJK KR', 'Malgun Gothic', sans-serif"
SVG_NS = "http://www.w3.org/2000/svg"
ASSET_DIR.mkdir(parents=True, exist_ok=True)


def text(x, y, value, size=28, color=INK, anchor="middle", bold=False):
    """Draw one text line; coordinates describe its baseline and anchor."""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{700 if bold else 400}">'
        f'{html.escape(str(value))}</text>'
    )


def rect(x, y, w, h, fill="#f8fafc", stroke="#cbd5e1", radius=4):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')


def arrow(x1, y1, x2, y2, color=BLUE, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" '
            f'stroke-width="2.5" fill="none" marker-end="url(#arrow-{color[1:]})"{dash}/>')


def svg(name, content, height=500):
    markers = "".join(
        f'<marker id="arrow-{c[1:]}" markerWidth="8" markerHeight="8" '
        f'refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="{c}"/></marker>'
        for c in [BLUE, GREEN, ORANGE, MUTED]
    )
    if '#lesson-photo' in content:
        markers += f'<image id="lesson-photo" width="960" height="640" xlink:href="{PHOTO_DATA}"/>'
    result = (f'<svg xmlns="{SVG_NS}" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 {height}" '
              f'font-family="{html.escape(FONT_FAMILY, quote=True)}">'
              f'<defs>{markers}</defs><rect width="1200" height="{height}" '
              f'fill="white"/>{content}</svg>\n')
    etree.fromstring(result.encode())
    (ASSET_DIR / f"{name}.svg").write_text(result, encoding="utf-8")
    return f"assets/lesson/{name}.svg"


def card(x, title, lines, color=BLUE, y=70, w=330, h=350):
    out = rect(x, y, w, h) + text(x + w / 2, y + 48, title, 30, color, bold=True)
    for i, line in enumerate(lines):
        out += text(x + w / 2, y + 118 + i * 52, line, 27)
    return out


def fruit(x, y, kind="apple", scale=1):
    """Place generated photographic examples instead of symbolic fruit drawings."""
    size = 88 * scale
    data = GENERATED_DATA[kind]
    return (f'<image x="{x-size/2}" y="{y-size/2}" width="{size}" '
            f'height="{size}" xlink:href="{data}" preserveAspectRatio="xMidYMid meet"/>')


def grid(x, y, values, cell=48, highlights=(), pale=False):
    out = ""
    for iy, row in enumerate(values):
        for ix, value in enumerate(row):
            fill = "#e5edf3" if (iy, ix) in highlights else "#f8fafc"
            if pale:
                shade = int(245 - float(value) * 20)
                fill = f"rgb({shade},{shade},{shade})"
            out += rect(x+ix*cell, y+iy*cell, cell, cell, fill, radius=0)
            out += text(x+(ix+.5)*cell, y+(iy+.65)*cell, value, min(27, cell*.48))
    return out


def heatmap(x, y, values, cell=40):
    values = np.asarray(values, dtype=float)
    lo, hi = values.min(), values.max()
    out = ""
    for iy, row in enumerate(values):
        for ix, value in enumerate(row):
            ratio = (value-lo)/(hi-lo) if hi != lo else .1
            c = tuple(int(a+(b-a)*ratio) for a, b in zip((239,246,255),(37,99,235)))
            out += rect(x+ix*cell, y+iy*cell, cell, cell, f"rgb{c}", "white", 0)
    return out


def pipeline(name, items, note=""):
    out = ""
    width = (1080 - 40*(len(items)-1))/len(items)
    for i, (title, lines) in enumerate(items):
        x = 60+i*(width+40)
        out += card(x, title, lines, y=85, w=width, h=300)
        if i < len(items)-1:
            out += arrow(x+width+5, 235, x+width+33, 235)
    if note:
        out += text(600, 455, note, 25, MUTED)
    return svg(name, out)


photo_root = etree.parse(str(REPO_DIR / "docs/assets/task_classification.svg"))
PHOTO_DATA = photo_root.find(f".//{{{SVG_NS}}}image").get("href")
GENERATED_DIR = REPO_DIR / "docs/assets/generated"
GENERATED_DATA = {
    name: "data:image/png;base64," + base64.b64encode(
        (GENERATED_DIR / f"{name}_studio_preview.png").read_bytes()
    ).decode("ascii")
    for name in ["apple", "orange"]
}
DEFECT_PATH = "M581 201 C595 200 605 209 609 221 C614 234 606 244 594 246 C580 247 572 236 571 224 C568 213 574 204 581 201Z"


def photo(x, y, w=240, mode="plain"):
    scale = w / 960
    out = (f'<use xlink:href="#lesson-photo" transform="translate({x} {y}) scale({scale})"/>')
    if mode == "box":
        out += rect(x+565*scale, y+197*scale, 53*scale, 57*scale, "none", BLUE, 0)
    if mode == "mask":
        out += (f'<path transform="translate({x} {y}) scale({scale})" '
                f'd="{DEFECT_PATH}" fill="#38bdf8" fill-opacity=".75" '
                f'stroke="{BLUE}" stroke-width="4"/>')
    return out


def build_professional_figures():
    """Use generated photography as examples, with exact native annotations."""
    out = text(185,65,"입력 이미지",28,BLUE,bold=True)
    out += fruit(185,230,"apple",3.4)
    stages = [(420,"국소 패턴",["명암 변화 · 경계","작은 수용영역"]),
              (675,"패턴 조합",["부분 형태 · 질감","이전 층의 반응 조합"]),
              (930,"Task 표현",["분류에 유용한 특징","더 넓은 입력 범위"]) ]
    for x, label, lines in stages:
        out += rect(x,95,235,255) + text(x+117.5,143,label,27,BLUE,bold=True)
        for j,line in enumerate(lines):
            out += text(x+117.5,218+j*52,line,22)
    out += arrow(345,230,410,230)
    out += arrow(660,230,670,230)+arrow(915,230,925,230)
    out += text(600,415,"계층적 표현: 국소 연산의 반복 → 넓은 문맥의 특징 조합",27,MUTED)
    out += text(600,460,"설명용 구조이며 실제 Feature Map을 관찰한 결과는 아닙니다",22,MUTED)
    svg("hierarchy_professional",out)

    out = text(285,55,"학습 데이터의 상관관계",29,BLUE,bold=True)
    out += text(915,55,"촬영 환경이 바뀐 데이터",29,GREEN,bold=True)
    for x, kind, fill, label in [(55,"apple","#e5edf3","Class: 사과"),
                                  (315,"orange","#f2e9dc","Class: 오렌지"),
                                  (685,"apple","#f2e9dc","Class: 사과"),
                                  (945,"orange","#e5edf3","Class: 오렌지")]:
        out += rect(x,105,200,235,fill,fill)
        out += fruit(x+100,205,kind,1.9)+text(x+100,375,label,25)
    out += arrow(530,225,660,225,MUTED)
    out += text(285,425,"Class와 배경색이 항상 함께 반복",25,BLUE)
    out += text(915,425,"물체는 유지, 배경색의 관계는 변경",25,GREEN)
    out += text(600,478,"배경만으로 맞춘 모델은 새로운 조건에서 실패할 수 있습니다",25,MUTED)
    svg("shortcut_professional",out)

    plate = "data:image/jpeg;base64," + base64.b64encode(
        (GENERATED_DIR / "capture_conditions.jpg").read_bytes()
    ).decode("ascii")
    out = f'<image x="35" y="85" width="1130" height="280" xlink:href="{plate}" preserveAspectRatio="xMidYMid meet"/>'
    for x,label in [(220,"기준 촬영"),(600,"측면 조명 · 저조도"),(980,"초점 변화")]:
        out += text(x,55,label,29,BLUE,bold=True)
        out += text(x,410,"정답 Class: 사과",26,GREEN)
    out += text(600,468,"촬영 조건을 다양하게 포함하고, Label 기준을 일관되게 관리",26,MUTED)
    svg("capture_conditions",out)


def build_figures():
    build_professional_figures()
    # Labels precede abstract feature-space plots.
    out = rect(30, 35, 550, 430) + rect(620, 35, 550, 430)
    out += text(305, 80, "지도학습: 입력–Label 관계 학습", 29, BLUE, bold=True)
    out += text(895, 80, "비지도학습: 데이터 구조 탐색", 29, GREEN, bold=True)
    for i, kind in enumerate(["apple", "orange", "apple"]):
        x=135+i*165
        out += fruit(x, 160, kind) + text(x, 220, "사과" if kind=="apple" else "오렌지", 25)
    out += arrow(305, 250, 305, 315) + text(305, 365, "새 이미지의 Class 예측", 28)
    out += rect(675, 115, 190, 235, "#f4f7fa", "#a9bfcc")
    out += rect(930, 115, 190, 235, "#fff7ed", "#fdba74")
    for x,y,k in [(725,165,"apple"),(815,230,"apple"),(745,295,"apple"),
                  (975,170,"orange"),(1060,235,"orange"),(990,295,"orange")]:
        out += fruit(x,y,k,.75)
    out += text(895, 405, "Label 없이 유사한 데이터 군집 탐색", 27)
    svg("learning_basic", out)

    out = ""
    for x, title in [(60,"Label을 이용해 경계 학습"),(650,"거리로 군집 탐색")]:
        out += rect(x, 40, 490, 410) + text(x+245, 85, title, 29, BLUE, bold=True)
        out += arrow(x+65, 370, x+435, 370, MUTED) + arrow(x+65, 370, x+65, 120, MUTED)
        out += text(x+270, 415, "특징 1", 23, MUTED) + text(x+68, 110,"특징 2",23,MUTED)
    for px,py,label in [(160,320,0),(210,280,0),(245,335,0),(300,300,0),
                        (365,180,1),(410,210,1),(450,160,1),(400,270,1)]:
        out += f'<circle cx="{px}" cy="{py}" r="12" fill="{BLUE if label==0 else ORANGE}"/>'
    out += '<path d="M320 130 L320 360" stroke="#334155" stroke-width="3" stroke-dasharray="8 6"/>'
    for cx,cy,color in [(790,290,BLUE),(990,205,ORANGE)]:
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="75" ry="58" fill="none" stroke="{color}" stroke-width="3"/>'
        for dx,dy in [(-30,-8),(0,20),(28,-18)]:
            out += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="12" fill="#64748b"/>'
    svg("learning_detail", out)

    out=rect(45,45,1110,185)+rect(45,270,1110,185)
    out+=text(180,95,"분류",31,BLUE,bold=True)+photo(80,115,200)
    out+=arrow(310,145,470,145)+rect(490,100,230,100,"#f4f7fa")
    out+=text(605,160,"모델",30,BLUE)+arrow(730,145,850,145)
    out+=text(985,145,"사과",34,GREEN,bold=True)+text(985,195,"범주 이름",27)
    out+=text(180,320,"회귀",31,BLUE,bold=True)+text(180,395,"입력 x = 2",30)
    out+=arrow(310,370,470,370)+rect(490,325,230,100,"#f4f7fa")
    out+=text(605,385,"모델",30,BLUE)+arrow(730,370,850,370)
    out+=text(985,370,"예측값 3.6",34,GREEN,bold=True)+text(985,420,"연속적인 숫자",27)
    svg("classification_basic",out)

    out=""
    for x,title,rows in [(45,"Binary: 2개 Class",[("정상",.18),("불량",.82)]),
                         (655,"Multi-class: 3개 이상",[("정상",.10),("Case A",.75),("Case B",.15)])]:
        out+=rect(x,35,500,430)+text(x+250,85,title,29,BLUE,bold=True)
        for i,(label,score) in enumerate(rows):
            y=150+i*100
            out+=text(x+30,y+30,label,26,INK,anchor="start")
            out+=rect(x+135,y,240,40,"#f4f7fa","none",3)
            out+=rect(x+135,y,240*score,40,BLUE,"none",3)
            out+=text(x+435,y+30,f"{score:.2f}",28,BLUE,bold=True)
    svg("classification_outputs",out)

    out = card(40,"입력 x = 2",["정답 y = 4","예측: ŷ = w × x","Bias는 0으로 고정"],w=330)
    out += card(435,"처음: w = 1",["ŷ = 1 × 2 = 2","정답보다 2 작음","Loss = (2 − 4)² = 4"],w=330)
    out += card(830,"수정 후: w = 1.8",["ŷ = 1.8 × 2 = 3.6","정답보다 0.4 작음","Loss = 0.16"],color=GREEN,w=330)
    out += arrow(375,240,425,240) + arrow(770,240,820,240)
    svg("learning_update",out)

    out = rect(80,55,1040,360)
    out += text(600,105,"오차를 보고 계산 기준을 바꿉니다",31,BLUE,bold=True)
    for x,v,label,color in [(245,4,"정답",INK),(510,2,"처음 예측",ORANGE),(810,3.6,"수정 후 예측",GREEN)]:
        out += text(x,165,label,27,color,bold=True)
        out += rect(x-40,340-v*34,80,v*34,"#e5edf3" if color==INK else "#e4efec" if color==GREEN else "#ffedd5",color,0)
        out += text(x,385,f"{v}",34,color,bold=True)
    out += text(600,465,"같은 입력 2 → 정답 4에 가까워지는 예측",28)
    svg("loss_basic",out)

    out = card(40,"입력",["밝기 x₁ = 0.5","모양 x₂ = 1.0"],w=300)
    out += card(450,"가중합",["0.2 × 0.5", "+ 0.8 × 1.0", "− 0.6 = 0.3"],w=300)
    out += card(860,"판정",["합계 0.3 ≥ 0","사과로 판정","예시 규칙"],color=GREEN,w=300)
    out += arrow(350,240,440,240) + arrow(760,240,850,240)
    svg("perceptron_basic",out)
    out = ""
    for y,label in [(150,"x₁ = 0.5"),(300,"x₂ = 1.0")]:
        out += rect(45,y-40,210,80,"#f4f7fa") + text(150,y+10,label,30)
    out += arrow(260,150,445,220) + arrow(260,300,445,240)
    out += text(330,145,"w₁ = 0.2",25,BLUE) + text(330,340,"w₂ = 0.8",25,BLUE)
    out += rect(455,175,310,120,"#f2f7f5")
    out += text(610,220,"z = Σ wᵢxᵢ + b",32,GREEN,bold=True)
    out += text(610,265,"z = 0.3",30)
    out += text(610,125,"b = −0.6",28,GREEN) + arrow(610,135,610,170,GREEN)
    out += arrow(775,235,850,235) + rect(860,175,300,120,"#f4f7fa")
    out += text(1010,220,"y = 1 if z ≥ 0",29,BLUE,bold=True)
    out += text(1010,265,"y = 0 if z < 0",29)
    out += text(600,430,"하나의 임계값 판정을 사용하는 퍼셉트론 예시",27,MUTED)
    svg("perceptron_detail",out)

    out = ""
    for x,gate in [(50,"AND"),(650,"XOR")]:
        out += rect(x,35,500,430) + text(x+250,80,gate,32,BLUE,bold=True)
        for a,b in [(0,0),(0,1),(1,0),(1,1)]:
            yes=(a and b) if gate=="AND" else a!=b
            px=x+135+a*240; py=350-b*200
            out += f'<circle cx="{px}" cy="{py}" r="18" fill="{BLUE if yes else "white"}" stroke="#334155" stroke-width="2"/>'
            out += text(px,py+45,f"({a}, {b})",23)
        if gate=="AND":
            # x1+x2=1.5 maps to a line sloping down in SVG coordinates.
            out += f'<path d="M{x+255} 150 L{x+375} 250" stroke="{GREEN}" stroke-width="4"/>'
            out += text(x+250,435,"직선 하나로 파란 점 분리",26,GREEN)
        else:
            out += text(x+250,435,"직선 하나로 파란 점 분리 불가",25,ORANGE)
    svg("and_xor",out)

    out = ""
    out += fruit(160,245,"apple",1.8) + text(160,370,"입력 이미지",27)
    for cx in [465,750]:
        for cy in [135,245,355]:
            out += f'<circle cx="{cx}" cy="{cy}" r="27" fill="#f4f7fa" stroke="{BLUE}" stroke-width="3"/>'
    for cy in [205,245,285]:
        for dy in [135,245,355]: out += arrow(205,cy,435,dy,MUTED)
    for sy in [135,245,355]:
        for dy in [135,245,355]:
            out += f'<path d="M492 {sy} L722 {dy}" stroke="#cbd5e1" stroke-width="2"/>'
    out += arrow(785,245,900,245) + card(915,"출력",["사과 점수","오렌지 점수"],y=130,w=240,h=245)
    out += text(465,440,"Layer 1",27,BLUE) + text(750,440,"Layer 2",27,BLUE)
    svg("network_basic",out)

    # Gradient: one parameter, one target, bias fixed. Arrow labels are exact.
    for detailed in [False,True]:
        out = arrow(100,405,740,405,MUTED)+arrow(100,405,100,40,MUTED)
        out += text(65,40,"Loss",25,MUTED)+text(755,440,"w",27,MUTED)
        def point(w): return 100+(w-.5)*200,405-((2*w-4)**2)*36
        points=[point(w) for w in np.linspace(.5,3.5,101)]
        out += '<polyline points="'+" ".join(f"{x:.2f},{y:.2f}" for x,y in points)+'" fill="none" stroke="#94a3b8" stroke-width="4"/>'
        for w in [1,2,3]:
            px,_=point(w);out+=text(px,435,str(w),23,MUTED)
        px,py=point(1)
        out+=f'<circle cx="{px}" cy="{py}" r="12" fill="{ORANGE}"/>'
        out+=text(px,py-25,"현재 w = 1",26,ORANGE)
        out+=arrow(px-8,py,px-90,py,ORANGE)+text(200,195,"Gradient: 왼쪽",24,ORANGE)
        out+=arrow(px+12,py,px+160,py,GREEN)+text(465,py-18,"수정: 오른쪽",25,GREEN)
        out+=card(820,"Loss를 줄이는 방향",["현재 위치의 경사 확인","반대 방향으로 이동","한 번에 조금씩"],y=80,w=330,h=340)
        if detailed:
            out=out[:out.index('<rect x="820"')]
            out+=card(800,"x = 2, y = 4, b = 0",["L(w) = (2w − 4)²","dL/dw = 8w − 16","w = 1: Gradient = −8","w′ = 1 − 0.1 × (−8)","= 1.8, Loss = 0.16"],y=35,w=370,h=430)
        svg("gradient_detail" if detailed else "gradient_basic",out)

    out = ""
    for i,(title,line) in enumerate([("예측","ŷ = 2"),("정답과 비교","y = 4"),("오차","Loss = 4"),("가중치 수정","w: 1 → 1.8")]):
        out+=card(45+i*295,title,[line],y=100,w=230,h=230)
        if i<3:out+=arrow(280+i*295,215,330+i*295,215)
    out+=f'<path d="M1045 345 L1045 405 L160 405 L160 345" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-36756f)"/>'
    out+=text(600,455,"바뀐 가중치로 다음 예측을 계산",28,GREEN)
    svg("training_basic",out)
    pipeline("backprop_basic",[("입력",["x = 2"]),("모델 계산",["ŷ = wx + b"]),("오차",["정답과 비교"])],"Forward: 예측 계산 / Backward: 각 가중치의 Gradient 계산")
    out = card(40,"Forward",["x = 2, w = 1, b = 0","ŷ = wx + b = 2","y = 4","L = (ŷ − y)² = 4"],y=35,w=330,h=430)
    out += card(435,"Backward",["∂L/∂ŷ = 2(ŷ − y) = −4","∂ŷ/∂w = x = 2","∂L/∂w = −4 × 2 = −8","∂L/∂b = −4"],y=35,w=330,h=430)
    out += card(830,"SGD, η = 0.1",["w′ = 1 − 0.1 × (−8)","= 1.8","b′ = 0.4","ŷ′ = 1.8 × 2 + 0.4 = 4"],color=GREEN,y=35,w=330,h=430)
    out += arrow(375,245,425,245) + arrow(770,245,820,245)
    svg("backprop_detail",out)

    out=""
    for x,title,lines in [(50,"학습 Training",["사진 + 정답","예측과 오차 계산","Weight 수정"]),
                          (650,"사용 Inference",["새 사진","학습된 Weight 고정","예측 결과 출력"])]:
        out+=rect(x,35,500,430)+text(x+250,80,title,31,BLUE,bold=True)
        out+=photo(x+130,115,240)
        for i,line in enumerate(lines):out+=text(x+250,320+i*49,line,27)
    svg("training_inference_basic",out)

    out=rect(45,50,1110,370)
    out+=text(600,100,"정답과 판정을 나란히 비교합니다",30,BLUE,bold=True)
    matrix=[("실제 불량","불량 판정: TP = 18","정상 판정: FN = 2"),
            ("실제 정상","불량 판정: FP = 4","정상 판정: TN = 76")]
    for i,row in enumerate(matrix):
        for j,v in enumerate(row):out+=text(235+j*360,210+i*130,v,28,INK if j==0 else GREEN if i==j-1 else ORANGE)
    out+=text(600,465,"전체 100개: 실제 불량 20개 / 실제 정상 80개",27,MUTED)
    svg("confusion_counts",out)
    out=card(55,"Precision 정밀도",["불량이라고 알린 22개","진짜 불량은 18개","18 / 22 = 81.8%"],w=490)
    out+=card(655,"Recall 재현율",["실제 불량 20개","찾아낸 불량은 18개","18 / 20 = 90%"],color=GREEN,w=490)
    svg("precision_recall",out)
    out=card(55,"Accuracy 정확도",["전체 중 맞춘 비율","(18 + 76) / 100","= 94%"],w=490)
    out+=card(655,"F1",["정밀도와 재현율의 조화평균","2TP / (2TP + FP + FN)","36 / 42 = 85.7%"],color=GREEN,w=490)
    svg("accuracy_f1",out)

    out=card(55,"Parameter",["모델이 배우는 값","Weight w = 1 → 1.8","Bias b = 0 → 0.4"],w=490)
    out+=card(655,"Hyperparameter",["학습을 설정하는 값","학습률 0.1","Batch 크기 4"],color=GREEN,w=490)
    svg("parameters_basic",out)

    out=""
    for i,(title,lines) in enumerate([
        ("촬영 조건",["밝기·거리·가림"]),("정답 기준",["일관된 Label"]),
        ("희귀 사례",["적은 불량도 확인"]),("운영 환경",["설비·시간대 확인"]) ]):
        x=35+i*295
        out+=rect(x,60,250,365)+text(x+125,110,title,29,BLUE,bold=True)
        if i==0:
            out+=photo(x+20,155,210)+text(x+125,365,lines[0],23)
        elif i==1:
            out+=fruit(x+125,210,scale=1.4)+text(x+125,295,"사과",32,GREEN)
            out+=text(x+125,365,lines[0],23)
        elif i==2:
            for j in range(8):
                out+=f'<circle cx="{x+55+(j%4)*46}" cy="{185+(j//4)*70}" r="15" fill="{ORANGE if j==7 else BLUE}"/>'
            out+=text(x+125,365,lines[0],23)
        else:
            for yy,label in [(170,"설비 A / 설비 B"),(235,"낮 / 밤")]:
                out+=rect(x+20,yy-30,210,60,"#f4f7fa")+text(x+125,yy+10,label,25)
            out+=text(x+125,365,lines[0],23)
    svg("dataset_basic",out)

    out=""
    for i,(title,label) in enumerate([("사진","960 × 640 RGB"),("크기 맞추기","예: 640 × 640"),("값 변환","0~255 → 0~1"),("축 순서","[1, 3, 640, 640]")]):
        x=35+i*295
        out+=rect(x,60,250,350)+text(x+125,110,title,29,BLUE,bold=True)
        if i==0:out+=photo(x+20,150,210)
        elif i==1:
            out+=rect(x+55,150,140,140,"#f4f7fa",BLUE,0)
            out+=text(x+125,225,"Resize",27,BLUE)
        elif i==2:
            out+=text(x+125,205,"128 / 255",30,BLUE)+text(x+125,260,"≈ 0.502",30,GREEN)
        else:
            for dx,dy,c in [(20,0,"#fee2e2"),(10,10,"#dcfce7"),(0,20,"#e5edf3")]:
                out+=rect(x+65+dx,150+dy,120,120,c,BLUE,0)
            out+=text(x+125,300,"B · C · H · W",24)
        out+=text(x+125,365,label,22)
        if i<3:out+=arrow(x+255,240,x+285,240)
    svg("preprocess_basic",out)

    out='<defs><filter id="dark"><feComponentTransfer><feFuncR type="linear" slope="0.5"/><feFuncG type="linear" slope="0.5"/><feFuncB type="linear" slope="0.5"/></feComponentTransfer></filter><filter id="blur"><feGaussianBlur stdDeviation="4"/></filter></defs>'
    for i,label in enumerate(["원본","어두운 조명","회전","초점 흐림"]):
        x=35+i*295
        out+=rect(x,60,250,350)+text(x+125,110,label,29,BLUE,bold=True)
        picture=photo(x+20,180,210)
        if i==1:picture='<g filter="url(#dark)">'+picture+'</g>'
        if i==2:picture=f'<g transform="rotate(12 {x+125} 250)">'+picture+'</g>'
        if i==3:picture='<g filter="url(#blur)">'+picture+'</g>'
        out+=picture+text(x+125,365,"정답: 불량",25,GREEN)
    svg("augmentation_basic",out)

    out=rect(55,65,1090,350)
    out+=text(600,120,"불량 점수에 기준을 적용합니다",31,BLUE,bold=True)
    out+=arrow(165,255,1040,255,MUTED)
    out+=text(165,300,"0",27,MUTED)+text(1040,300,"1",27,MUTED)
    out+='<path d="M605 180 L605 320" stroke="#334155" stroke-width="3" stroke-dasharray="8 6"/>'
    out+=text(605,165,"Threshold = 0.5",28)
    for value,label,color in [(.31,"정상",BLUE),(.82,"불량",ORANGE)]:
        x=165+875*value
        out+=f'<circle cx="{x}" cy="255" r="14" fill="{color}"/>'
        out+=text(x,365,f"{value}: {label}",28,color,bold=True)
    out+=text(600,465,"기준이 0.9이면 점수 0.82도 정상으로 판정",27,MUTED)
    svg("threshold_basic",out)

    out=card(55,"Loss",["학습의 목적함수","예측과 정답으로 계산","Gradient로 Weight 수정"],w=490)
    out+=card(655,"Metric",["성능을 해석하는 기준","Accuracy·Recall·IoU 등","모델·운영 성능 비교"],color=GREEN,w=490)
    svg("loss_metric_basic",out)

    # CNN: show patterns before numbers.
    out=rect(35,45,330,400)+text(200,90,"입력 이미지",30,BLUE,bold=True)+photo(60,130,280)
    out+=rect(440,45,325,400)+text(602,90,"작은 영역 확인",30,BLUE,bold=True)
    edge=[[0,0,1],[0,0,1],[0,0,1]]
    out+=grid(505,145,edge,65,highlights=[(y,x) for y in range(3) for x in range(3)])
    out+=text(602,395,"주변 Pixel의 밝기 변화",26)
    out+=rect(840,45,325,400)+text(1002,90,"반응 위치를 모으기",29,GREEN,bold=True)
    out+=heatmap(900,140,[[0,0,3,0],[0,1,3,0],[0,0,3,0],[0,0,1,0]],50)
    out+=text(1002,395,"경계에 강한 반응",27)
    out+=arrow(370,245,430,245)+arrow(775,245,830,245)
    svg("cnn_local_basic",out)

    out=card(35,"같은 필터",["세로 밝기 차이에 반응"],w=300)
    out+=grid(103,245,[[-1,0,1]]*3,55)
    out+=card(425,"경계가 있는 영역",["반응값 3"],w=330)
    out+=grid(500,245,edge,55)
    out+=card(830,"평평한 영역",["반응값 0"],color=GREEN,w=330)
    out+=grid(905,245,[[1,1,1]]*3,55)
    svg("kernel_basic",out)

    image=np.array([[1,2,3,0,1],[4,5,6,1,0],[7,8,9,2,1],[0,1,2,3,1],[1,0,1,2,3]])
    kernel=np.array([[1,0,-1]]*3)
    output=np.array([[int((image[y:y+3,x:x+3]*kernel).sum()) for x in range(3)] for y in range(3)])
    assert output.tolist()==[[-6,12,16],[-6,8,15],[-4,2,7]]
    out=text(205,55,"입력: 5 × 5",30,BLUE,bold=True)
    out+=grid(65,95,image.tolist(),56,[(y,x) for y in range(3) for x in range(3)])
    out+=text(560,55,"Kernel: 3 × 3",30,BLUE,bold=True)+grid(470,120,kernel.tolist(),60)
    out+=text(975,55,"출력: 3 × 3",30,GREEN,bold=True)+grid(885,120,output.tolist(),60,[(0,0)])
    out+=arrow(355,200,450,200)+arrow(665,200,860,200)
    out+=text(600,420,"첫 칸: (1 − 3) + (4 − 6) + (7 − 9) = −6",30)
    out+=text(600,470,"stride = 1, padding = 0, bias = 0 / 한 채널 예시",24,MUTED)
    svg("convolution_detail",out)

    for kind in ["stride","padding","downsampling"]:
        out=""
        if kind=="stride":
            for x,s,ow in [(60,1,3),(660,2,2)]:
                out+=rect(x,35,480,430)+text(x+240,80,f"Stride {s}: {s}칸씩 이동",30,BLUE,bold=True)
                out+=grid(x+95,110,[["" for _ in range(5)] for _ in range(5)],48,
                          [(y,x) for y in range(3) for x in range(3)])
                out+=arrow(x+119,135,x+119+48*s,135,ORANGE)
                out+=text(x+240,415,f"5 × 5 입력 → {ow} × {ow} 출력",28)
        elif kind=="padding":
            out+=text(235,60,"가장자리에 0을 채우기",30,BLUE,bold=True)
            padded=[[0 if y in [0,6] or x in [0,6] else "·" for x in range(7)] for y in range(7)]
            out+=grid(55,100,padded,50,[(y,x) for y in range(1,6) for x in range(1,6)])
            out+=arrow(430,270,625,270)+card(670,"Padding = 1",["5 × 5 → 7 × 7로 둘러쌈","Kernel 3, Stride 1","출력은 5 × 5"],y=80,w=475,h=340)
        else:
            values=np.arange(64).reshape(8,8)%11
            pooled=values.reshape(4,2,4,2).max(axis=(1,3))
            out+=text(240,65,"공간 크기 8 × 8",30,BLUE,bold=True)+heatmap(80,105,values,40)
            out+=arrow(445,265,735,265)+text(600,225,"2 × 2 Max Pooling",26,BLUE)
            out+=text(980,65,"공간 크기 4 × 4",30,GREEN,bold=True)+heatmap(840,125,pooled,70)
            out+=text(600,470,"각 2 × 2 영역의 최댓값을 남기는 예시",27,MUTED)
        svg(kind+"_basic",out)

    out=text(600,60,"Hout = floor((H + 2P − K) / S) + 1",34,BLUE,bold=True)
    out+=text(600,105,"dilation = 1 / Wout도 같은 식으로 계산",25,MUTED)
    for i,(title,lines) in enumerate([
        ("줄어드는 출력",["H = 5, K = 3","S = 1, P = 0","Hout = 3"]),
        ("크기 유지",["H = 5, K = 3","S = 1, P = 1","Hout = 5"]),
        ("두 칸씩 이동",["H = 5, K = 3","S = 2, P = 0","Hout = 2"]) ]):
        out+=card(45+i*395,title,lines,y=150,w=320,h=300)
    svg("spatial_detail",out)

    out=photo(35,130,310)+text(190,95,"같은 입력",30,BLUE,bold=True)
    out+=arrow(355,230,460,230)
    for i,(label,vals) in enumerate([
        ("세로 경계",[[0,1,4,0]]*4),
        ("가로 경계",[[0]*4,[1]*4,[4]*4,[0]*4]),
        ("밝은 영역",[[0,0,0,0],[0,4,4,0],[0,4,4,0],[0,0,0,0]])]):
        x=490+i*235
        out+=text(x+90,95,label,27,GREEN,bold=True)+heatmap(x,135,vals,45)
        out+=text(x+90,370,f"반응 지도 {i+1}",26)
    out+=text(600,460,"설명용 반응 지도: 실제 모델의 Feature Map은 학습으로 결정",25,MUTED)
    svg("feature_basic",out)

    out=card(35,"RGB 입력",["H × W × Cin","224 × 224 × 3"],y=100,w=300,h=290)
    out+=card(440,"64개 필터",["필터 하나: 3 × 3 × 3","RGB 전체를 곱하고 합산","stride 1, padding 1"],y=100,w=330,h=290)
    out+=card(870,"64개 출력 Channel",["Hout × Wout × Cout","224 × 224 × 64"],color=GREEN,y=100,w=300,h=290)
    out+=arrow(345,245,430,245)+arrow(780,245,860,245)
    out+=text(600,460,"PyTorch Weight: [64, 3, 3, 3] / Weight 1,728개 + Bias 64개",27,MUTED)
    svg("feature_detail",out)

    out=photo(30,145,255)+text(158,105,"같은 사과 사진",29,BLUE,bold=True)
    out+=arrow(295,230,360,230)+card(370,"Backbone",["판단에 유용한","특징 계산"],y=120,w=255,h=270)
    for i,(title,mode,result) in enumerate([("분류 Head","plain","불량"),("검출 Head","box","결함 Box"),("분할 Head","mask","결함 Mask")]):
        y=20+i*155
        out+=arrow(635,250,720,y+70,BLUE)+rect(740,y,420,140,"#f8fafc")
        out+=text(835,y+45,title,27,BLUE,bold=True)+text(835,y+100,result,26,GREEN)
        out+=photo(950,y+10,180,mode)
    svg("backbone_basic",out)
    out=text(455,60,"Backbone: Conv 3 × 3, Stride 2, Padding 1",30,BLUE,bold=True)
    for i,(label,shape) in enumerate([("Input","224² × 3"),("Conv 1","112² × 64"),("Conv 2","56² × 128"),("Conv 3","28² × 192"),("Conv 4","14² × 256")]):
        x=30+i*170
        out+=text(x+65,135,label,26,BLUE)
        out+=rect(x+10,180,100,140-i*17,"#e5edf3",BLUE,0)
        out+=f'<path d="M{x+110} 180 l20 -15 v{140-i*17} l-20 15Z" fill="#a9bfcc" stroke="{BLUE}" stroke-width="2"/>'
        out+=text(x+65,380,shape,23)
        if i<4:out+=arrow(x+135,240,x+165,240)
    for i,(label,result) in enumerate([("분류 Head","Class logits"),("검출 Head","Box + Class"),("분할 Head","Pixel logits")]):
        y=105+i*120
        out+=arrow(855,245,920,y+43)+rect(935,y,240,90,"#f2f7f5",GREEN)
        out+=text(1055,y+35,label,27,GREEN,bold=True)+text(1055,y+72,result,25)
    out+=text(600,465,"크기는 H × W × C / 예시 구조이며 Task별 Head·Decoder는 다름",26,MUTED)
    svg("backbone_detail",out)

    out=card(35,"이미 배운 모델",["여러 이미지로 학습","기본적인 특징 계산"],w=330)
    out+=card(435,"내 사진 + 정답",["새 Task의 Label","내 조건으로 추가 학습"],w=330)
    out+=card(835,"내 Task에 맞춘 모델",["새 조건에서 평가","필요하면 더 학습"],color=GREEN,w=330)
    out+=arrow(375,245,425,245)+arrow(775,245,825,245)
    svg("transfer_basic",out)
    out=rect(45,55,1110,365)
    out+=text(325,110,"Feature Extractor",31,BLUE,bold=True)+text(905,110,"새 Head",31,GREEN,bold=True)
    for i in range(4):out+=rect(105+i*115,150,90,130,"#e5edf3",BLUE)
    out+=arrow(585,215,745,215)+rect(775,150,270,130,"#e4efec",GREEN)
    out+=text(325,345,"Freeze: Weight 고정",27,BLUE)+text(905,345,"Task Label로 학습",27,GREEN)
    out+=text(600,475,"Fine-tuning: Backbone 일부 또는 전체까지 업데이트하며 검증",27,MUTED)
    svg("transfer_detail",out)

    # A clean numeric IoU example; no ambiguous overlap approximation.
    out=""
    for x,title,color in [(110,"정답과 예측",BLUE),(610,"겹침 / 합집합",GREEN)]:
        out+=text(x+190,60,title,30,color,bold=True)
    for x in [110,610]:
        for iy in range(4):
            for ix in range(5):
                gt=ix<3;pred=ix>=2
                fill="#99f6e4" if gt and pred else "#e5edf3" if gt else "#fed7aa"
                out+=rect(x+ix*75,110+iy*75,75,75,fill,"white",0)
    out+=text(300,455,"파랑: 정답 / 주황: 예측",27)
    out+=text(800,455,"초록 4칸 / 전체 20칸",27)
    svg("iou_detail",out)

    out=rect(35,35,470,420)+text(270,80,"ReLU: 음수는 0, 양수는 그대로",27,BLUE,bold=True)
    out+=arrow(95,345,445,345,MUTED)+arrow(270,395,270,115,MUTED)
    out+=f'<path d="M105 345 H270 L420 155" fill="none" stroke="{BLUE}" stroke-width="5"/>'
    out+=text(180,400,"x < 0 → 0",25)+text(360,400,"x > 0 → x",25)
    out+=rect(570,35,590,420)+text(865,80,"비선형 계산으로 XOR 경계 표현",28,GREEN,bold=True)
    # In these plot coordinates, s=x1+x2=.5 and 1.5 form a diagonal strip.
    out+='<path d="M705 245 L825 345 L945 345 L945 245 L825 145 L705 145Z" fill="#e4efec" fill-opacity=".65"/>'
    out+=f'<path d="M705 245 L825 345 M825 145 L945 245" fill="none" stroke="{GREEN}" stroke-width="4"/>'
    for a,b in [(0,0),(0,1),(1,0),(1,1)]:
        px=705+a*240;py=345-b*200
        out+=f'<circle cx="{px}" cy="{py}" r="15" fill="{BLUE if a!=b else "white"}" stroke="#334155" stroke-width="2"/>'
        out+=text(px,py+38,f"({a}, {b})",22)
    out+=text(865,425,"두 경계 사이: x₁ + x₂가 0.5~1.5",24,GREEN)
    svg("activation_basic",out)

    out=""
    for i,(title,lines) in enumerate([("Data",["사진·Label","분리 기준"]),("Train",["Weight 학습","설정 선택"]),("Evaluate",["최종 Test","실패 사례"]),("Deploy",["추론 시스템","전처리 일치"]),("Monitor",["운영 실패","새 조건 확인"]) ]):
        x=30+i*235
        out+=card(x,title,lines,y=60,w=200,h=260)
        if i<4:out+=arrow(x+205,190,x+230,190)
    out+=f'<path d="M1070 340 V385 H130 V340" fill="none" stroke="{GREEN}" stroke-width="4" marker-end="url(#arrow-36756f)"/>'
    out+=text(600,450,"운영 실패 사례를 데이터 보강과 재학습에 연결",29,GREEN)
    svg("workflow_basic",out)


def legacy_figure(name):
    """Copy an existing diagram without repeating the slide title inside it."""
    source=REPO_DIR / "docs/assets" / f"{name}.svg"
    root=etree.parse(str(source)).getroot()
    for child in list(root):
        if child.tag==f"{{{SVG_NS}}}text" and float(child.get("y","999"))<=100:
            root.remove(child)
    for element in root.iter(f"{{{SVG_NS}}}text"):
        if element.text=="위치 구조가 숫자 나열로 사라짐":
            element.text="공간 이웃 구조를 명시하지 않음"
        if element.text=="Weight가 크면 그 입력이 Output에 더 크게 영향을 줍니다.":
            element.text="가중치의 부호·크기와 입력 범위를 함께 봅니다."
    for element in root.iter():
        if element.tag==f"{{{SVG_NS}}}path" and element.get("stroke") and not element.get("fill"):
            element.set("fill","none")
        if element.tag==f"{{{SVG_NS}}}image" and element.get("href"):
            element.set("{http://www.w3.org/1999/xlink}href",element.get("href"))
    # Existing content starts below the removed headings.
    root.set("viewBox","0 105 1200 495")
    path=ASSET_DIR / f"context_{name}.svg"
    serialized = etree.tostring(root,encoding="unicode",xml_declaration=False)
    for old, new in {"#2563eb":BLUE,"#0f766e":GREEN,"#ea580c":ORANGE,
                     "#dbeafe":"#e5edf3","#93c5fd":"#a9bfcc"}.items():
        serialized = serialized.replace(old, new)
    serialized = serialized.replace('rx="18"', 'rx="4"').replace('rx="20"', 'rx="4"')
    path.write_text(serialized, encoding="utf-8")
    return "assets/lesson/"+path.name


def build_deck(filename, title, subtitle, cards, lessons, prev_page, next_page=""):
    """Write a complete deck, continuous visible numbers, and a source manifest."""
    header=f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="slide.css?v=generatedfigfit-20260927-27">
<link rel="stylesheet" href="lesson.css?v={VERSION}">
<script src="slide.js?v=generatedfigfit-20260927-27" defer></script>
</head><body class="deck-page lesson-deck" data-prev-page="{prev_page}" data-next-page="{next_page}">
<header class="site-header"><nav class="nav"><a class="brand" href="intro.html">Vision AI</a>
<div class="nav-links"><a href="intro.html">01 Intro</a><a href="ai_basics.html">02 AI Basics</a>
<a href="vision_ai.html">03 Vision AI</a></div></nav></header>
<main class="deck" aria-live="polite">
<section class="slide active"><div class="slide-inner">
<div class="lesson-meta">{html.escape(title)}</div>
<h1 class="slide-title">{html.escape(subtitle)}</h1>
<div class="lesson-outline">'''
    for label,body in cards:
        header+=f'<article><strong>{html.escape(label)}</strong><p>{html.escape(body)}</p></article>'
    header+='</div></div></section>\n'
    manifest=[]
    for index, lesson in enumerate(lessons,1):
        topic,heading,description,asset,takeaway,*extra=lesson
        detailed=bool(extra and extra[0])
        if asset.startswith("old:"):
            asset=legacy_figure(asset[4:])
        else:
            asset=f"assets/lesson/{asset}.svg"
        reference=""
        if detailed:
            url="https://cs231n.github.io/convolutional-networks/" if filename=="vision_ai.html" else "https://cs231n.github.io/"
            reference=f'<p class="lesson-reference">개념 참고: <a href="{url}" target="_blank" rel="noopener">Stanford CS231n</a> · 직접 재구성한 설명용 Figure</p>'
        if any(name in asset for name in ["learning_basic", "network_basic", "capture_conditions", "shortcut_professional", "hierarchy_professional"]):
            reference += '<p class="lesson-reference">사진: AI 생성 교육용 예시 · 실제 측정/실험 결과가 아님</p>'
        header+=f'''<section class="slide" data-topic="{html.escape(topic)}" data-level="{"detail" if detailed else "basic"}">
<div class="slide-inner"><div class="lesson-meta"><span>{index:02d} · {html.escape(topic)}</span>
<span class="lesson-level{" lesson-level--detail" if detailed else ""}">{"상세 설명" if detailed else "기본 개념"}</span></div>
<h2 class="slide-title">{html.escape(heading)}</h2>
<p class="slide-subtitle">{html.escape(description)}</p>
<figure class="lesson-figure"><img src="{asset}?v={VERSION}" alt="{html.escape(heading)}"></figure>
<p class="lesson-takeaway">{html.escape(takeaway)}</p>{reference}</div></section>\n'''
        manifest.append({"number":index,"topic":topic,"level":"detail" if detailed else "basic","title":heading,"asset":asset})
    header+='''</main><div class="deck-controls"><div class="deck-controls-inner">
<button class="deck-button" type="button" data-slide-prev>← 이전</button>
<div class="deck-status"><span class="deck-counter"><span data-slide-current>1</span> / <span data-slide-total>1</span></span>
<div class="deck-progress"><div class="deck-progress-bar" data-slide-progress></div></div></div>
<button class="deck-button" type="button" data-slide-next>다음 →</button></div></div></body></html>\n'''
    (REPO_DIR / "docs" / filename).write_text(header,encoding="utf-8")
    return manifest


def build_lessons():
    # Basic illustrations are followed by selected exact diagrams, not mixed on one slide.
    ai=[
        ("AI의 범위","AI·머신러닝·딥러닝은 어떻게 다를까요?","Artificial Intelligence는 넓은 기술 영역, Machine Learning은 데이터에서 배우는 방법, Deep Learning은 다층 신경망을 사용하는 방법입니다.","old:ai_ml_dl","Computer Vision(컴퓨터 비전)은 이미지·영상 문제를 다루는 분야입니다."),
        ("규칙과 학습","판단 규칙을 사람이 쓰거나, 데이터에서 배울 수 있습니다","밝기가 100보다 작으면 후보로 찾는 규칙과, 다양한 사진·정답을 이용해 판단 기준을 배우는 방법을 비교합니다.","old:rule_vs_ml","실제 시스템에서는 영상처리 규칙과 학습 모델을 함께 사용하기도 합니다."),
        ("지도학습과 비지도학습","지도학습과 비지도학습은 학습 목표가 다릅니다","지도학습은 사진과 정답을 함께 사용합니다. 비지도학습은 정답 이름표 없이 데이터의 공통 구조를 찾습니다.","learning_basic","정답 Label(라벨)은 모델이 배워야 할 목표를 알려주는 데이터입니다."),
        ("지도학습과 비지도학습","사진을 숫자로 표현하면 경계와 군집으로 설명할 수 있습니다","Feature(특징)는 판단에 유용한 단서입니다. 특징 공간은 각 데이터를 그 단서들의 숫자로 배치한 공간입니다.","learning_detail","점의 색은 지도학습의 정답, 오른쪽 원은 비슷한 데이터의 군집을 나타냅니다.",True),
        ("분류와 회귀","분류는 이름을, 회귀는 연속적인 숫자를 예측합니다","Classification(분류)은 사과·오렌지 같은 범주를, Regression(회귀)은 입력 숫자에서 3.6 같은 연속적인 값을 예측합니다.","classification_basic","먼저 어떤 형태의 결과가 필요한지 정하면 학습 목표가 분명해집니다."),
        ("분류의 출력","두 종류 또는 여러 종류 중에서 점수를 비교합니다","Binary Classification(이진 분류)은 두 Class, Multi-class Classification(다중 클래스 분류)은 세 개 이상을 구분합니다.","classification_outputs","그림은 확률 형식의 점수 예시입니다. 높은 점수가 현실의 정확한 확률이나 정답을 보장하지는 않습니다."),
        ("학습의 의미","학습은 예측 오차가 줄도록 계산 기준을 바꾸는 과정입니다","입력 x=2, 정답 y=4를 사용합니다. 모델 ŷ=w×x의 w를 바꾸면 같은 입력의 예측값이 달라집니다.","learning_update","여기서 w는 학습으로 바꾸는 가중치이고, Bias는 0으로 고정한 예시입니다."),
        ("Loss","정답에서 얼마나 벗어났는지를 숫자로 계산합니다","Loss(손실)는 학습할 때 줄이는 값입니다. 제곱오차 예시에서 예측 2의 Loss는 4, 예측 3.6의 Loss는 0.16입니다.","loss_basic","여러 샘플의 제곱오차를 평균한 값이 MSE(Mean Squared Error, 평균제곱오차)입니다."),
        ("Gradient","현재 위치에서 Loss가 줄어드는 쪽으로 이동합니다","Gradient(기울기)는 가중치 변화에 따른 Loss의 변화율입니다. 반대 방향으로 작은 걸음을 이동하는 것이 경사하강법의 직관입니다.","gradient_basic","곡선의 가로축은 가중치 w, 세로축은 Loss입니다. 아래쪽일수록 오차가 작습니다."),
        ("Gradient와 Learning Rate","같은 예제의 가중치를 실제로 한 번 수정해 봅니다","x=2, y=4, b=0에서 w=1의 Gradient는 −8입니다. Learning Rate(학습률) 0.1로 수정하면 w는 1.8이 됩니다.","gradient_detail","SGD 기본식: 새 가중치 = 현재 가중치 − 학습률 × Gradient.",True),
        ("Optimizer","Optimizer는 수정 규칙, 학습률은 한 걸음의 크기입니다","Optimizer(최적화 알고리즘)는 Gradient를 이용해 Parameter를 갱신합니다. 학습률이 너무 크면 최소점을 지나칠 수 있습니다.","old:optimizer_loss_landscape","지금 본 식은 기본 SGD 예시입니다. Momentum·Adam은 갱신에 추가 정보를 사용합니다."),
        ("Training Loop","예측 → 오차 → Gradient → 수정을 반복합니다","Training(학습)은 한 번의 계산으로 끝나지 않습니다. 바뀐 가중치로 다음 예측을 계산하고 다시 오차를 줄입니다.","training_basic","Forward는 예측 계산, Backward는 Gradient 계산, Update는 가중치 수정입니다."),
        ("Training과 Inference","배울 때는 Weight를 바꾸고, 사용할 때는 고정합니다","Inference(추론)는 학습된 모델에 새 입력을 넣어 결과를 얻는 과정입니다. 정답 없이도 예측할 수 있습니다.","training_inference_basic","추론 과정 자체는 새로운 데이터로 가중치를 학습하는 과정이 아닙니다."),
        ("Perceptron","입력마다 가중치를 곱하고, 더해서 하나의 판정을 만듭니다","Perceptron(퍼셉트론)은 기본적인 신경 계산입니다. 아래 숫자는 밝기와 모양을 두 입력으로 놓은 설명용 예시입니다.","perceptron_basic","Weight는 입력의 기여도를, Bias는 합계의 기준 위치를 조절합니다."),
        ("Perceptron","입력·가중합·판정 함수를 계산 그래프로 연결합니다","z는 가중합, b는 Bias(편향) Parameter입니다. 여기서는 z≥0이면 1을 출력하는 임계값 판정을 사용합니다.","perceptron_detail","가중치의 영향은 부호·절댓값과 입력의 크기를 함께 봐야 합니다.",True),
        ("Parameter와 Hyperparameter","모델이 배우는 값과, 학습을 설정하는 값은 다릅니다","Parameter(파라미터)는 Weight·Bias처럼 학습하는 값입니다. Hyperparameter(하이퍼파라미터)는 학습률·Batch 크기 등 설정입니다.","parameters_basic","Bias Parameter와 데이터가 한쪽으로 치우쳤다는 의미의 Data Bias는 다른 개념입니다."),
        ("AND와 XOR","하나의 직선으로 나눌 수 없는 문제도 있습니다","AND는 두 입력 모두 1일 때만 1입니다. XOR는 두 입력이 서로 다를 때 1입니다. 파란 점은 출력 1, 흰 점은 출력 0입니다.","and_xor","AND의 경계는 x₁+x₂=1.5입니다. XOR의 파란 점 두 개는 직선 하나로 분리할 수 없습니다."),
        ("Neural Network","여러 계산을 Layer로 연결하면 신경망이 됩니다","Neural Network(신경망)의 각 Layer(층)는 앞에서 받은 숫자를 조합해 다음 층으로 전달합니다.","network_basic","그림의 노드·연결은 계산 구조를 나타내며, 실제 모델의 뉴런 수와는 다릅니다. 사진 1장을 입력하는 예시입니다."),
        ("Activation","Layer를 쌓을 때 비선형 계산도 필요합니다","Activation Function(활성화 함수)은 계산에 비선형성을 넣습니다. ReLU(Rectified Linear Unit)는 음수를 0으로, 양수를 그대로 전달합니다.","activation_basic","ReLU: f(x)=max(0,x). 여러 비선형 계산을 조합하면 더 복잡한 경계를 표현할 수 있습니다."),
        ("선형 Layer의 한계","비선형성이 없으면 여러 Layer도 하나로 합쳐집니다","Linear Layer 사이에 활성화 함수가 없으면 전체 계산은 하나의 Affine Transformation(선형 계산+편향)으로 표현됩니다.","old:linear_layers_collapse","깊이만 늘린다고 XOR 같은 문제를 해결하는 비선형 표현력이 생기지는 않습니다.",True),
        ("Feature와 Representation","이미지 숫자는 판단에 유용한 내부 표현으로 바뀝니다","Feature는 유용한 단서, Representation(표현)은 그 단서를 담은 내부 숫자입니다. 경계·부분 형태는 직관을 위한 예시입니다.","hierarchy_professional","실제 Channel 하나가 항상 사람이 이름 붙인 특징 하나와 대응하는 것은 아닙니다."),
        ("Backpropagation","오차에서 각 가중치의 Gradient를 뒤로 계산합니다","Backpropagation(역전파)은 출력의 오차가 각 가중치에 얼마나 민감한지 계산합니다. 가중치 수정은 Optimizer가 수행합니다.","old:backpropagation_visual","오차를 뒤로 보내는 그림은 Gradient 계산 흐름을 표현합니다."),
        ("Backpropagation","Chain Rule로 각 Parameter의 변화율을 계산합니다","같은 x=2, y=4 예제에 Bias를 추가합니다. w=1, b=0에서 가중치와 Bias의 Gradient를 계산합니다.","backprop_detail","이 장에서는 w와 b를 모두 학습합니다. 앞의 Gradient 예제에서는 b를 0으로 고정했습니다.",True),
        ("Batch·Iteration·Epoch","데이터를 작은 묶음으로 나누어 반복해서 봅니다","Batch는 한 번에 처리하는 묶음, Iteration은 보통 한 묶음의 처리, Epoch은 학습 데이터 전체를 한 번 보는 주기입니다.","old:batch_epoch","이미지 10장, batch_size=4, 마지막 묶음을 버리지 않으면 4+4+2의 3번 처리가 1 Epoch입니다."),
        ("Dataset","데이터는 실제 사용할 조건을 대표해야 합니다","Dataset(데이터셋)은 학습·평가에 사용하는 데이터 모음입니다. 조명·크기·배경·설비·시간대와 일관된 정답 기준을 확인합니다.","capture_conditions","특정 배경만 정답과 함께 반복되면, 모델이 물체 대신 배경으로 판단할 수 있습니다."),
        ("데이터 분리","학습·모델 선택·최종 평가의 데이터를 나눕니다","Train은 가중치 학습, Validation은 모델·설정·Threshold 선택, Test는 최종 일반화 평가에 사용합니다.","old:dataset_split","예: 1,000장의 70/15/15 분리. 비율보다 서로 독립적인 평가 데이터 확보가 중요합니다."),
        ("Group Split","같은 영상의 비슷한 Frame은 통째로 분리합니다","연관된 샘플을 묶은 단위를 Group(그룹)이라고 합니다. 평가하려는 새 조건에 맞춰 영상·설비·대상 등을 분리 기준으로 정합니다.","old:group_split_visual","새 영상 성능은 영상 단위, 새 설비 성능은 설비 단위 분리가 필요할 수 있습니다."),
        ("Data Leakage","평가 데이터의 정보가 학습·선택에 새어들면 점수가 왜곡됩니다","Data Leakage(데이터 누수)는 평가 때 몰라야 할 정보를 사용한 경우입니다. 중복 장면·전체 데이터 통계·반복적인 Test 선택을 점검합니다.","old:data_leakage_visual","학습하는 전처리 통계는 Train에서 계산합니다. 미리 정한 255 나누기는 통계를 학습하는 과정이 아닙니다."),
        ("전처리","모델이 기대하는 크기·값 범위·채널 순서를 맞춥니다","Preprocessing(전처리)은 입력 형식을 맞추는 과정입니다. 1920×1080을 640×640으로 맞출 때는 Resize·Crop·Padding의 차이를 고려합니다.","preprocess_basic","RGB/BGR, 0~255/정규화 값, HWC/CHW를 확인하고 Train·Inference의 기본 규칙을 맞춥니다."),
        ("Data Augmentation","의미를 유지하는 변화를 학습 중에 보여줍니다","Data Augmentation(데이터 증강)은 밝기·회전·가림 같은 변화를 적용하는 방법입니다. 현실적인 변화 범위와 정답 유지 여부를 확인합니다.","augmentation_basic","검출·분할에서는 이미지와 Box·Mask에 같은 공간 변환을 적용해야 합니다."),
        ("Overfitting","Train에서 잘하는 것과 새 데이터에서 잘하는 것은 다릅니다","Overfitting(과적합)은 학습 데이터에 지나치게 맞춰 새 데이터 성능이 떨어지는 현상입니다. Validation 추세와 실패 사례를 함께 봅니다.","old:overfit_leakage","Generalization(일반화)은 직접 학습하지 않은 데이터에서도 성능을 유지하는 능력입니다."),
        ("K-Fold","평가 대상을 바꾸어 성능의 변동도 확인합니다","K-Fold Cross Validation(교차검증)은 데이터 부분집합을 번갈아 Validation으로 사용하며 모델을 각각 새로 학습합니다.","old:kfold_visual","같은 원본을 공유하는 샘플은 Group K-Fold로 분리하고, 최종 Test는 별도로 유지합니다.",True),
        ("Threshold","점수에 기준을 적용하면 실제 판정이 됩니다","Threshold(임계값)는 불량으로 판정할 점수 기준입니다. 예: 불량 점수 0.82는 기준 0.5에서 불량으로 판정합니다.","threshold_basic","기준을 바꾸면 찾는 불량과 오알람 수가 달라집니다. 기준은 Validation에서 선택합니다."),
        ("Confusion Matrix","정답과 판정을 비교해 네 가지 결과를 셉니다","Confusion Matrix(혼동행렬)는 TP·FN·FP·TN을 구분합니다. 실제 불량 20개 중 18개를 찾고, 정상 80개 중 4개를 잘못 알린 예시입니다.","confusion_counts","TP: 찾은 불량 / FN: 놓친 불량 / FP: 오알람 / TN: 정상 통과."),
        ("Precision과 Recall","알람의 정확성과 불량을 찾는 비율을 구분합니다","Precision은 불량이라 알린 것 중 진짜 불량의 비율, Recall은 실제 불량 중 찾아낸 비율입니다.","precision_recall","같은 모델도 임계값에 따라 Precision·Recall이 달라질 수 있습니다."),
        ("Accuracy와 F1","전체 정답률과 Precision·Recall의 균형을 함께 봅니다","Accuracy는 전체 중 맞춘 비율입니다. F1은 Precision과 Recall의 조화평균이며 두 지표가 모두 높아야 높아집니다.","accuracy_f1","불량이 1%인 데이터에서 모두 정상으로 예측해도 Accuracy는 99%이지만 Recall은 0%입니다.",True),
        ("Loss와 Metric","학습할 때 줄이는 값과, 평가할 때 보는 값은 역할이 다릅니다","Loss는 가중치를 갱신하는 목적함수입니다. Metric(평가지표)은 실제 문제에서 성능을 해석하고 비교하는 기준입니다.","loss_metric_basic","Loss가 줄었다고 원하는 Metric이나 운영 성능이 항상 개선되는 것은 아닙니다."),
        ("Shortcut Learning","모델이 우리가 원한 단서를 사용했는지도 확인합니다","Shortcut Learning(지름길 학습)은 물체 형태 대신 배경처럼 쉬운 단서로 정답을 맞추는 현상입니다.","shortcut_professional","Leakage는 정보가 새는 문제, Shortcut은 입력의 원치 않는 상관관계를 이용하는 문제입니다."),
        ("개발과 운영","운영의 실패 사례를 다음 데이터와 학습에 연결합니다","배포 후에도 조명·설비·제품 조건이 바뀔 수 있습니다. 실패 이미지를 모으고 정답 기준과 평가 조건을 다시 확인합니다.","workflow_basic","데이터 수집 → 학습 → 평가 → 배포 → 관찰을 반복하며 개선합니다."),
    ]
    vision=[
        ("문제 정의","필요한 결과부터 정하면 Vision Task가 정해집니다","이미지 전체가 불량인지, 결함이 어디에 있는지, 정확한 면적이 얼마인지에 따라 필요한 결과가 다릅니다.","old:vision_task_selection","질문 → 결과 형태 → Task → Label → 평가 기준과 모델 순으로 연결합니다."),
        ("Classification","이미지 전체의 상태나 종류를 예측합니다","Classification(분류)은 이미지 단위의 클래스와 점수를 출력합니다. 아래 예시는 사과 사진 전체의 불량 여부입니다.","old:task_classification","이 예시는 단일 Label 분류입니다. 위치나 정확한 결함 영역은 출력하지 않습니다."),
        ("Object Detection","객체나 결함의 위치를 사각형으로 찾습니다","Object Detection(객체 검출)은 클래스·Bounding Box(경계 상자)·점수를 출력합니다.","old:task_detection","Box 내부 전체가 결함인 것은 아닙니다. 상자는 위치를 둘러싸는 표현입니다."),
        ("Segmentation","어느 Pixel이 관심 영역인지 구분합니다","Segmentation(분할)은 Pixel별 클래스나 Mask(영역 표시)를 출력합니다. 아래 예시는 결함 영역입니다.","old:task_segmentation","형상·면적·경계가 필요하면 Box보다 Mask가 적합합니다."),
        ("Label","같은 사진이라도 Task가 바뀌면 정답 형태가 바뀝니다","분류는 이미지 클래스, 검출은 클래스와 Box, 분할은 Pixel Mask를 정답으로 사용합니다.","backbone_basic","여기서 결과 그림을 정답으로 작성한 것이 Label이고, 모델이 계산한 것이 Prediction입니다."),
        ("IoU","위치와 영역은 정답과 얼마나 겹치는지 평가합니다","IoU(Intersection over Union, 교집합/합집합 비율)는 정답 영역과 예측 영역의 겹침 정도입니다.","old:iou_visual","완전 일치하면 1, 겹치는 영역이 없으면 0입니다."),
        ("IoU","겹친 칸 수를 전체 합집합 칸 수로 나눕니다","정답 12칸과 예측 12칸이 4칸 겹치면, 합집합은 12+12−4=20칸입니다.","iou_detail","IoU = 4/20 = 0.2. 검출은 Box, 분할은 Mask의 영역으로 계산합니다.",True),
        ("이미지의 단서","작은 영역의 경계·밝기 변화를 먼저 살펴봅니다","이미지에서는 가까운 Pixel의 배치가 중요합니다. 작은 영역의 반응을 여러 위치에서 계산하면 패턴이 있는 위치를 알 수 있습니다.","cnn_local_basic","Patch는 이미지의 작은 영역, Feature Map은 위치별 반응값을 모은 지도입니다."),
        ("CNN","CNN은 작은 영역을 보고 같은 가중치를 재사용합니다","Convolutional Neural Network(합성곱 신경망)는 지역 연결과 가중치 공유로 이미지의 공간적 패턴을 계산합니다.","old:cnn_why_local","Flatten은 값과 순서를 유지하지만, 완전연결층에는 공간 이웃 관계와 가중치 공유가 명시되어 있지 않습니다."),
        ("Kernel","같은 필터도 이미지 영역에 따라 반응이 달라집니다","Kernel 또는 Filter(커널·필터)는 작은 가중치 배열입니다. 세로 밝기 변화가 있는 영역과 평평한 영역의 반응을 비교합니다.","kernel_basic","그림은 사람이 정한 경계 필터 예시입니다. CNN의 필터 값은 학습으로 정해집니다."),
        ("Convolution","같은 위치끼리 곱하고 더해 출력 한 칸을 만듭니다","입력의 3×3 영역과 필터를 곱해 합산하고, 필터를 옮겨 다음 칸을 계산합니다. 모든 출력은 실제 계산한 값입니다.","convolution_detail","이 장은 한 채널·Bias 0 예시입니다. 일반적인 딥러닝 Conv는 필터를 뒤집지 않는 Cross-correlation 연산입니다.",True),
        ("Feature Map","반응값을 위치대로 모으면 특징 지도가 됩니다","서로 다른 필터는 서로 다른 위치에서 반응합니다. 여러 반응 지도를 쌓은 것이 출력 Channel(채널)입니다.","feature_basic","이 그림은 설명용 예시입니다. 실제 학습된 Channel의 의미는 항상 사람이 이름 붙일 수 있지는 않습니다."),
        ("Feature Map과 Channel","RGB 전체를 보는 필터 하나가 출력 Channel 하나를 만듭니다","일반적인 Conv2d에서 필터 하나는 입력 Channel 전체를 곱해 합산합니다. 출력 Channel 수는 필터 수입니다.","feature_detail","224×224×3 입력, 64개 필터, Stride 1·Padding 1이면 224×224×64가 됩니다.",True),
        ("Stride","필터를 몇 칸씩 이동할지 정합니다","Stride(이동 간격)가 1이면 한 칸, 2이면 두 칸씩 이동합니다. 같은 입력과 필터에서 이동 간격이 크면 출력 크기가 작아집니다.","stride_basic","5×5 입력과 3×3 필터, Padding 0: Stride 1은 3×3, Stride 2는 2×2 출력입니다."),
        ("Padding","가장자리 주변에 값을 채워 계산 범위를 조절합니다","Padding(패딩)은 입력 주위를 채우는 방법입니다. 아래는 가장자리 한 칸에 0을 채우는 Zero Padding입니다.","padding_basic","5×5 입력, Kernel 3·Stride 1·Padding 1이면 출력의 공간 크기가 5×5로 유지됩니다."),
        ("Downsampling","공간 해상도를 줄여 더 작은 특징 지도를 만듭니다","Downsampling(다운샘플링)은 가로·세로 크기를 줄이는 과정입니다. 아래는 2×2에서 최댓값을 남기는 Max Pooling 예시입니다.","downsampling_basic","8×8 → 4×4는 공간 위치 수가 64개에서 16개로 줄어드는 변화입니다."),
        ("출력 크기 계산","Kernel·Stride·Padding으로 출력 크기를 계산합니다","H는 입력 높이, K는 필터 크기, S는 Stride, P는 양쪽 Padding입니다. floor는 소수점 아래를 버립니다.","spatial_detail","Dilation 1 기준 식입니다. Channel 수는 공간 크기와 별도로 필터 수가 결정합니다.",True),
        ("특징의 조합","Layer는 앞의 특징을 조합해 더 복잡한 표현을 만듭니다","초기 반응들을 여러 층에서 조합하면 더 넓은 형태와 Task에 유용한 내부 표현을 만들 수 있습니다.","hierarchy_professional","경계 → 부분 → 형태는 개념적 설명이며 모든 모델에서 같은 방식으로 나타난다고 보장하지 않습니다."),
        ("Receptive Field","깊은 층의 한 위치는 더 넓은 입력 범위의 영향을 받습니다","Receptive Field(수용영역)는 한 출력 위치에 영향을 주는 원본 입력 영역입니다.","old:receptive_field","3×3 Conv, Stride 1, Dilation 1을 쌓으면 이론적 수용영역은 3×3 → 5×5 → 7×7입니다.",True),
        ("Backbone과 Head","특징을 만드는 부분과, 결과를 만드는 부분을 나눠 봅니다","Backbone(백본)은 특징을 추출하고, Head(헤드)는 Task별 결과를 만듭니다. 입력과 결과는 동일한 사과 사진을 사용합니다.","backbone_basic","세 가지 Head는 구조 비교를 위한 개념도입니다. 실제 한 모델이 항상 세 Task를 동시에 출력하는 것은 아닙니다."),
        ("Backbone과 Head","블록을 연결하고 각 단계의 특징 크기를 표시합니다","Architecture(모델 구조)는 어떤 연산을 어떤 순서로 연결하는지 나타냅니다. 아래 크기는 구조를 설명하는 예시입니다.","backbone_detail","검출·분할 모델에는 여러 해상도 특징을 결합하는 Neck·Decoder 등이 추가될 수 있습니다.",True),
        ("CNN 학습","CNN의 필터도 오차를 줄이는 방향으로 학습합니다","Forward로 예측하고 Label과 Loss를 비교한 뒤, Backpropagation으로 Gradient를 계산하고 Optimizer가 필터를 갱신합니다.","old:cnn_training","기본 학습 원리는 AI Basics와 같습니다. 학습하는 Parameter에 Kernel 가중치가 포함됩니다."),
        ("Transfer Learning","이미 배운 가중치에서 내 Task의 학습을 시작합니다","Transfer Learning(전이학습)은 사전학습 모델의 지식을 재사용하는 방법입니다. 처음부터 모든 값을 새로 배우는 것과 비교할 수 있습니다.","transfer_basic","내 데이터가 사전학습 데이터와 다르면 효과가 달라질 수 있으므로 별도 평가가 필요합니다."),
        ("Freeze와 Fine-tuning","고정할 부분과 추가 학습할 부분을 구분합니다","Freeze는 가중치 고정, Fine-tuning(미세조정)은 사전학습 가중치 일부 또는 전체를 새 데이터로 업데이트하는 과정입니다.","transfer_detail","새 Head만 학습하는 경우와 Backbone까지 학습하는 경우를 구분해 검증합니다.",True),
        ("평가와 실패 사례","높은 점수만으로 판단 근거가 맞다고 보장할 수 없습니다","배경·조명·장비가 정답과 우연히 연결되면 모델은 쉬운 Shortcut을 사용할 수 있습니다.","shortcut_professional","평균 Metric과 함께 실패 이미지·설비별·조명별 결과를 점검합니다."),
        ("운영 Cycle","문제 정의부터 운영 관찰까지 연결해 개선합니다","성공 기준을 정하고 데이터를 모아 학습·평가·배포합니다. 운영의 실패 사례는 다음 데이터 보강의 근거가 됩니다.","old:vision_project_pipeline","모델 구조뿐 아니라 Label 기준·데이터 분리·운영 조건까지 함께 관리합니다."),
    ]
    ai_manifest=build_deck("ai_basics.html","02. AI Basics","AI는 오차를 줄이며 판단 기준을 배웁니다",[("예측하고 배우기","입력·정답·오차·가중치 수정"),("신경망 이해하기","작은 계산을 층으로 연결"),("제대로 평가하기","데이터 분리·실패 사례·지표")],ai,"intro.html","vision_ai.html")
    vision_manifest=build_deck("vision_ai.html","03. Vision AI","이미지에서 필요한 패턴을 찾아 결과로 바꿉니다",[("결과 정하기","분류·검출·분할과 Label"),("이미지 계산하기","작은 영역·필터·특징 지도"),("학습하고 적용하기","모델 구조·전이학습·운영")],vision,"ai_basics.html")
    manifest={"generated_assets":["assets/generated/apple_studio.webp","assets/generated/orange_studio.webp","assets/generated/capture_conditions.webp"],"version":VERSION,"ai_basics":ai_manifest,"vision_ai":vision_manifest}
    used={Path(item["asset"]).name for key in ["ai_basics","vision_ai"] for item in manifest[key]}
    for asset in ASSET_DIR.glob("*.svg"):
        if asset.name not in used:
            asset.unlink()
    (ASSET_DIR / "manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for folder,key in [("02_ai_basics","ai_basics"),("03_vision_ai","vision_ai")]:
        note=REPO_DIR / "lectures" / folder / "README.md"
        previous=note.read_text(encoding="utf-8")
        if "## 2026-10-06 배포 슬라이드 순서" in previous:
            previous=previous.split("## 2026-10-06 배포 슬라이드 순서")[0].rstrip()+"\n"
        previous+="\n## 2026-10-06 배포 슬라이드 순서\n\n현재 배포 HTML의 순서는 아래를 기준으로 합니다. 상세 설명은 관련 개념 바로 뒤에 배치합니다. 앞의 개념 노트는 참고용입니다.\n\n"
        for item in manifest[key]:
            previous+=f"{item['number']}. {item['title']} ({'상세' if item['level']=='detail' else '기본'})\n"
        previous+="\n계산·숫자·Tensor 구조 그림은 `scripts/build_lesson_revision.py`에서 생성하며, 외부 이미지 서버나 CDN을 사용하지 않습니다.\n"
        note.write_text(previous,encoding="utf-8")
    print(json.dumps({key:len(value)+1 for key,value in manifest.items() if key in ["ai_basics", "vision_ai"]}))


if __name__=="__main__":
    build_figures()
    build_lessons()
    for target, source in {
        "and_xor_linear_separability": "and_xor",
        "gradient_intuition": "gradient_basic",
        "convolution_visual": "convolution_detail",
        "feature_maps": "feature_detail",
        "backbone_head": "backbone_basic",
    }.items():
        (REPO_DIR / f"docs/assets/{target}.svg").write_bytes(
            (ASSET_DIR / f"{source}.svg").read_bytes()
        )
