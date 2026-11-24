#!/usr/bin/env python3
"""The World Today — Tuesday 24 November 2026. Dense 45-story broadsheet.
Deterministic PIL renderer: no network, no randomness, no timestamps.
Renders entry.png at 1024x1024, under the 1 MiB cap."""

import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 24, 31)
NAVY = (14, 42, 74)
NAVY_D = (9, 28, 51)
RED = (179, 32, 44)
GOLD = (232, 163, 23)
TEAL = (14, 124, 123)
SKY = (127, 179, 213)
SEA = (18, 64, 96)
CREAM = (248, 244, 230)
GREY = (110, 116, 126)
LIGHT = (228, 232, 236)
GREEN = (22, 140, 74)
ORANGE = (230, 110, 20)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, max_w, max_lines):
    """Wrap and cap at max_lines, truncating the last line with an ellipsis."""
    lines = wrap(d, text, f, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "…", font=f) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "…"
    return lines


def one_line(d, text, f, max_w):
    """Force a single line, truncating with an ellipsis if needed."""
    if d.textlength(text, font=f) <= max_w:
        return text
    while text and d.textlength(text + "…", font=f) > max_w:
        text = text[:-1]
    return text + "…"


def burst(d, cx, cy, r, colour, inner):
    """Starburst: alternating triangles around a centre."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)
    d.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
              fill=inner)


def draw_tanker(d, x0, y0, x1, y1):
    """Strait of Hormuz: night sea, tanker silhouette, mine blast."""
    d.rectangle([x0, y0, x1, y1], fill=(10, 30, 52))
    d.rectangle([x0, y0, x1, y0 + 26], fill=(24, 52, 84))
    for wx in range(x0 + 18, x1 - 10, 34):
        d.ellipse([wx, y0 + 10, wx + 12, y0 + 18], fill=(255, 214, 130))
    d.rectangle([x0, y0 + 62, x1, y1], fill=SEA)
    for wx in range(x0 + 8, x1 - 8, 44):
        d.arc([wx, y0 + 66, wx + 30, y0 + 78], 0, 180, fill=(90, 150, 190), width=2)
    d.rectangle([x0 + 60, y0 + 46, x1 - 60, y0 + 64], fill=(16, 20, 26))
    d.rectangle([x0 + 60, y0 + 46, x0 + 92, y0 + 58], fill=(16, 20, 26))
    d.rectangle([x0 + 150, y0 + 38, x0 + 168, y0 + 46], fill=(16, 20, 26))
    d.rectangle([x0 + 210, y0 + 42, x0 + 224, y0 + 46], fill=(16, 20, 26))
    burst(d, x0 + 265, y0 + 30, 26, ORANGE, GOLD)
    d.ellipse([x0 + 34, y0 + 52, x0 + 44, y0 + 62], fill=(40, 44, 50))
    d.line([x0 + 39, y0 + 52, x0 + 39, y0 + 46], fill=(40, 44, 50), width=2)
    d.line([x0 + 34, y0 + 57, x0 + 44, y0 + 57], fill=(40, 44, 50), width=2)


def draw_chart(d, x0, y0, x1, y1):
    """Nvidia: green board, chip, rising chart arrow."""
    d.rectangle([x0, y0, x1, y1], fill=(8, 46, 28))
    d.rectangle([x0 + 12, y0 + 12, x0 + 96, y0 + 96], fill=(12, 66, 40),
                outline=(40, 180, 110), width=2)
    d.rectangle([x0 + 34, y0 + 34, x0 + 74, y0 + 74], fill=(8, 46, 28),
                outline=(120, 230, 160), width=2)
    d.text((x0 + 42, y0 + 44), "NV", font=font(FB, 20), fill=(140, 240, 170))
    for k in range(4):
        d.line([x0 + 24 + k * 6, y0 + 12, x0 + 24 + k * 6, y0 + 96],
               fill=(40, 180, 110), width=1)
        d.line([x0 + 12, y0 + 24 + k * 6, x0 + 96, y0 + 24 + k * 6],
               fill=(40, 180, 110), width=1)
    pts = [(x0 + 108, y0 + 82), (x0 + 150, y0 + 66), (x0 + 182, y0 + 70),
           (x0 + 224, y0 + 44), (x0 + 268, y0 + 30), (x0 + 306, y0 + 12)]
    d.line(pts, fill=(120, 240, 140), width=4, joint="curve")
    d.polygon([(x0 + 306, y0 + 12), (x0 + 288, y0 + 10), (x0 + 302, y0 + 28)],
              fill=(120, 240, 140))
    d.text((x0 + 118, y0 + 84), "+31%", font=font(FB, 22), fill=(140, 240, 170))


def draw_city(d, x0, y0, x1, y1):
    """Zaporizhzhia: night skyline, apartment block, blast and smoke."""
    d.rectangle([x0, y0, x1, y1], fill=(16, 22, 38))
    d.ellipse([x0 + 262, y0 + 10, x0 + 292, y0 + 40], fill=(220, 225, 235))
    for bx, bw, bh in [(0, 52, 66), (58, 40, 84), (104, 62, 58), (172, 44, 76),
                       (222, 56, 62), (284, 40, 80)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(30, 38, 56))
        for wy in range(y1 - bh + 8, y1 - 6, 16):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 6, 16):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 130))
    burst(d, x0 + 124, y0 + 52, 30, ORANGE, GOLD)
    d.ellipse([x0 + 96, y0 + 18, x0 + 128, y0 + 42], fill=(90, 92, 100))
    d.ellipse([x0 + 130, y0 + 8, x0 + 158, y0 + 30], fill=(70, 72, 82))
    d.ellipse([x0 + 62, y0 + 26, x0 + 88, y0 + 46], fill=(80, 82, 92))

def draw_icon(d, kind, x0, y0, x1, y1):
    """Small recognisable scene for a medium tile."""
    w, h = x1 - x0, y1 - y0
    if kind == "gaza":
        d.rectangle([x0, y0, x1, y1], fill=(58, 32, 28))
        d.rectangle([x0, y0, x1, y0 + h // 2], fill=(90, 60, 44))
        for bx, bw, bh in [(6, 34, 30), (46, 28, 38), (80, 40, 26),
                           (126, 30, 36), (162, 26, 30)]:
            d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(28, 18, 16))
        burst(d, x0 + 96, y0 + 26, 18, ORANGE, GOLD)
        d.ellipse([x0 + 60, y0 + 10, x0 + 84, y0 + 26], fill=(120, 118, 110))
    elif kind == "cop":
        d.rectangle([x0, y0, x1, y1], fill=(18, 70, 62))
        d.ellipse([x0 + w // 2 - 34, y0 + 8, x0 + w // 2 + 34, y0 + 56],
                  fill=(40, 140, 120))
        d.arc([x0 + w // 2 - 34, y0 + 8, x0 + w // 2 + 34, y0 + 56], 0, 360,
              fill=(200, 240, 220), width=3)
        d.line([x0 + w // 2 - 22, y0 + 32, x0 + w // 2 + 22, y0 + 32],
               fill=(200, 240, 220), width=3)
        d.line([x0 + w // 2 - 22, y0 + 32, x0 + w // 2, y0 + 48],
               fill=(200, 240, 220), width=3)
        d.line([x0 + w // 2 + 22, y0 + 32, x0 + w // 2, y0 + 48],
               fill=(200, 240, 220), width=3)
    elif kind == "vote":
        d.rectangle([x0, y0, x1, y1], fill=(30, 44, 96))
        d.rectangle([x0 + 40, y0 + 14, x0 + 158, y0 + 52], fill=(240, 240, 244))
        d.rectangle([x0 + 40, y0 + 14, x0 + 158, y0 + 22], fill=(179, 32, 44))
        d.text((x0 + 48, y0 + 26), "VOTE", font=font(FB, 15), fill=(30, 44, 96))
        d.line([x0 + 108, y0 + 40, x0 + 120, y0 + 50], fill=RED, width=4)
        d.line([x0 + 120, y0 + 50, x0 + 146, y0 + 24], fill=RED, width=4)
    elif kind == "grok":
        d.rectangle([x0, y0, x1, y1], fill=(24, 28, 40))
        d.rectangle([x0 + 66, y0 + 8, x0 + 132, y0 + 52], fill=(60, 70, 96),
                    outline=(140, 160, 220), width=2)
        d.ellipse([x0 + 82, y0 + 20, x0 + 98, y0 + 36], fill=(120, 220, 255))
        d.ellipse([x0 + 116, y0 + 20, x0 + 132, y0 + 36], fill=(120, 220, 255))
        d.line([x0 + 76, y0 + 44, x0 + 122, y0 + 44], fill=(140, 160, 220),
               width=2)
        d.line([x0 + 30, y0 + 58, x0 + 168, y0 + 58], fill=RED, width=4)
        d.line([x0 + 30, y0 + 58, x0 + 44, y0 + 44], fill=RED, width=4)
        d.line([x0 + 168, y0 + 58, x0 + 154, y0 + 44], fill=RED, width=4)
    elif kind == "quake":
        d.rectangle([x0, y0, x1, y1], fill=(52, 44, 34))
        d.polygon([(x0, y1), (x0 + 70, y0 + 14), (x0 + 120, y0 + 30),
                   (x1, y0 + 6), (x1, y1)], fill=(96, 84, 66))
        d.line([(x0 + 40, y1), (x0 + 70, y0 + 40), (x0 + 96, y0 + 52),
                (x0 + 118, y1)], fill=(30, 24, 18), width=4)
        d.line([(x0 + 130, y1), (x0 + 150, y0 + 44), (x0 + 168, y1)],
               fill=(30, 24, 18), width=3)
        d.text((x0 + 8, y0 + 6), "5.3", font=font(FB, 20), fill=(255, 230, 160))
    elif kind == "sat":
        d.rectangle([x0, y0, x1, y1], fill=(10, 14, 30))
        for sx, sy in [(20, 14), (60, 26), (150, 10), (180, 30), (40, 50),
                       (120, 48), (170, 52)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                      fill=(220, 225, 240))
        d.ellipse([x0 + 18, y0 + 30, x0 + 62, y0 + 62], fill=(70, 120, 180))
        d.rectangle([x0 + 84, y0 + 34, x0 + 116, y0 + 52], fill=(180, 190, 210))
        d.rectangle([x0 + 116, y0 + 38, x0 + 150, y0 + 48], fill=(90, 140, 200))
        d.rectangle([x0 + 60, y0 + 38, x0 + 84, y0 + 48], fill=(90, 140, 200))
        d.ellipse([x0 + 156, y0 + 22, x0 + 168, y0 + 34], fill=RED)
    elif kind == "island":
        d.rectangle([x0, y0, x1, y1], fill=(16, 90, 120))
        d.ellipse([x0 + 40, y0 + 34, x0 + 158, y0 + 62], fill=(34, 120, 70))
        d.polygon([(x0 + 88, y0 + 34), (x0 + 100, y0 + 6), (x0 + 112, y0 + 34)],
                  fill=(20, 90, 50))
        d.rectangle([x0 + 96, y0 + 6, x0 + 104, y0 + 34], fill=(90, 60, 30))
        d.line([x0 + 104, y0 + 8, x0 + 128, y0 + 14], fill=(200, 40, 40), width=3)
        d.line([x0 + 104, y0 + 8, x0 + 128, y0 + 14], fill=(255, 255, 255),
               width=1)
    elif kind == "jet":
        d.rectangle([x0, y0, x1, y1], fill=(120, 160, 200))
        d.ellipse([x0 + 12, y0 + 8, x0 + 60, y0 + 30], fill=(240, 244, 248))
        d.ellipse([x0 + 30, y0 + 18, x0 + 78, y0 + 40], fill=(225, 232, 240))
        d.polygon([(x0 + 120, y0 + 26), (x0 + 168, y0 + 20),
                   (x0 + 168, y0 + 34), (x0 + 120, y0 + 34)], fill=(90, 100, 120))
        d.polygon([(x0 + 60, y0 + 40), (x0 + 100, y0 + 58),
                   (x0 + 110, y0 + 44)], fill=(90, 100, 120))
        d.polygon([(x0 + 60, y0 + 16), (x0 + 100, y0 + 2),
                   (x0 + 110, y0 + 18)], fill=(90, 100, 120))
    elif kind == "palace":
        d.rectangle([x0, y0, x1, y1], fill=(40, 52, 70))
        d.rectangle([x0 + 30, y0 + 24, x0 + 168, y0 + 62], fill=(70, 84, 108))
        d.polygon([(x0 + 30, y0 + 24), (x0 + 99, y0 + 4), (x0 + 168, y0 + 24)],
                  fill=(50, 62, 82))
        for cx in range(x0 + 44, x0 + 160, 24):
            d.rectangle([cx, y0 + 36, cx + 12, y0 + 62], fill=(255, 220, 140))
        d.rectangle([x0, y0 + 56, x1, y0 + 62], fill=(200, 40, 40))
        d.line([x0, y0 + 58, x1, y0 + 58], fill=(255, 255, 255), width=1)
    elif kind == "fire":
        d.rectangle([x0, y0, x1, y1], fill=(44, 40, 36))
        d.rectangle([x0 + 30, y0 + 30, x0 + 168, y0 + 62], fill=(70, 64, 58))
        d.rectangle([x0 + 30, y0 + 30, x0 + 168, y0 + 38], fill=(52, 46, 40))
        d.polygon([(x0 + 88, y0 + 30), (x0 + 74, y0 + 6), (x0 + 96, y0 + 18),
                   (x0 + 108, y0 + 2), (x0 + 112, y0 + 30)], fill=ORANGE)
        d.polygon([(x0 + 92, y0 + 30), (x0 + 98, y0 + 16), (x0 + 106, y0 + 30)],
                  fill=GOLD)
        for wx in range(x0 + 40, x0 + 160, 28):
            d.rectangle([wx, y0 + 44, wx + 14, y0 + 54], fill=(255, 220, 140))
    else:
        d.rectangle([x0, y0, x1, y1], fill=LIGHT)


LEADS = [
    ("HORMUZ ON FIRE", "TANKERS HIT", draw_tanker,
     "Iran: three tankers hit mines in the strait",
     "Tehran vows to resist the US blockade; Vance and Rubio meet Qatar's PM."),
    ("HUANG IS BACK", "NVDA +31%", draw_chart,
     "Nvidia reinstates its CEO — Nasdaq soars 7%",
     "Trump intervened to bring Jensen Huang back; shares jump 31%."),
    ("RUSSIA POUNDS UKRAINE", "17 KILLED", draw_city,
     "Overnight strikes hit homes in Zaporizhzhia",
     "Two killed, 40 wounded, four of them children; 15 dead near Kyiv."),
]

MEDIUMS = [
    ("gaza", "Gaza: Hamas security chief killed",
     "Six others die with Abu Nahel."),
    ("cop", "COP31 fallout: rethink the rules",
     "Push to rewrite UN climate rules."),
    ("vote", "Democrats take biggest House majority",
     "Biggest majority in decades."),
    ("grok", "States sue Musk firms over Grok images",
     "Two states sue over Grok images."),
    ("quake", "5.3 quake shakes Nepal and neighbours",
     "Tremors felt across South Asia."),
    ("sat", "Nuclear satellite alarm",
     "Launch feared before 2026 ends."),
    ("island", "Solomon Islands drops China pact",
     "PM to sign treaty with Australia."),
    ("jet", "South Korea scrambles jets",
     "Russian jets enter defence zone."),
    ("palace", "Break-in at Prince William's home",
     "Two held after Anmer Hall raid."),
    ("fire", "Deadly factory fire in Indonesia",
     "Hunt for missing staff goes on."),
]

LIST_ITEMS = [
    "Pentagon: Canada falls short on defence",
    "Trump to fast-track federal death sentences",
    "Trump targets Newsom in speech on violent crime",
    "US blacklists Singapore cloud firm Megaspeed",
    "US envoy doubts Trump $3.8bn Israel aid pledge",
    "Israel rivals clash over Iran threat",
    "Landmine toll hits 5-year high of 7,000",
    "N. Korea threatens to shut Swiss office",
    "China cobalt firms race to beat Congo ban",
    "EU proposes ban on Russian flags at sports",
    "Seven states back EU push to limit Russian visas",
    "Germany first to access Ukraine's Delta system",
    "Russia: Estonia moves 'near open war'",
    "Zelensky urges NATO to admit Ukraine",
    "US detains Chinese Princeton student",
    "Trump offers Philippines $2.4bn for self-defence",
    "Hasina wants to fly home on 16 December",
    "Iraq PM orders ministry to run Kurdish oilfields",
    "UN urges probe into Benghazi port attacks",
    "DRC fighting traps Ebola teams near hospital",
    "Somalia, Uganda step up anti-Shabaab operations",
    "Houthis say Saudi strike kills 17 in Hodeida",
    "India–NZ Wellington Test ends in a draw",
    "Alcaraz wins maiden ATP Finals crown",
    "Gukesh begins world title defence in Geneva",
    "Verstappen wins Las Vegas GP, his 75th victory",
    "Google gives $5m for AI research at IIT Kharagpur",
    "Arm extends CEO Rene Haas' tenure to 2033",
    "LA king tides threaten Thanksgiving floods",
    "Don Toliver postpones London shows",
    "Thousands evacuated from UK concert",
    "Late pope's diary tells of seeing the devil",
]

MAP_PINS = [
    ("Hormuz", 0.60, 0.42), ("Bahrain", 0.585, 0.46), ("Gaza", 0.565, 0.40),
    ("Zaporizhzhia", 0.545, 0.24), ("Kyiv", 0.53, 0.20),
    ("Nepal", 0.71, 0.42), ("Solomon Is.", 0.90, 0.66),
    ("S. Korea", 0.815, 0.30), ("Indonesia", 0.76, 0.62),
    ("London", 0.455, 0.16), ("Washington", 0.20, 0.30),
    ("Brussels", 0.475, 0.18), ("Benghazi", 0.545, 0.40),
]


def draw_map(d, x0, y0, x1, y1):
    """Simplified world map with 13 pins and a legend."""
    d.rectangle([x0, y0, x1, y1], fill=(18, 52, 84))
    d.rectangle([x0, y0, x1, y1], outline=NAVY_D, width=2)
    mx, my, mw, mh = x0 + 8, y0 + 8, x1 - x0 - 16, y1 - y0 - 46
    land = (58, 110, 72)
    # Americas
    d.polygon([(mx + 8, my + 26), (mx + 52, my + 8), (mx + 78, my + 20),
               (mx + 66, my + 52), (mx + 40, my + 62), (mx + 16, my + 48)],
              fill=land)
    d.polygon([(mx + 52, my + 66), (mx + 78, my + 62), (mx + 84, my + 92),
               (mx + 64, my + 118), (mx + 48, my + 96)], fill=land)
    # Europe / Africa
    d.polygon([(mx + 158, my + 10), (mx + 196, my + 6), (mx + 204, my + 30),
               (mx + 182, my + 44), (mx + 164, my + 30)], fill=land)
    d.polygon([(mx + 164, my + 48), (mx + 204, my + 46), (mx + 210, my + 78),
               (mx + 188, my + 104), (mx + 168, my + 82)], fill=land)
    # Asia
    d.polygon([(mx + 208, my + 8), (mx + 300, my + 4), (mx + 322, my + 26),
               (mx + 300, my + 52), (mx + 250, my + 56), (mx + 212, my + 34)],
              fill=land)
    # SE Asia / Oceania
    d.polygon([(mx + 272, my + 62), (mx + 306, my + 60), (mx + 310, my + 80),
               (mx + 282, my + 86)], fill=land)
    d.polygon([(mx + 316, my + 96), (mx + 344, my + 92), (mx + 348, my + 112),
               (mx + 324, my + 118)], fill=land)
    for name, fx, fy in MAP_PINS:
        px, py = mx + fx * mw, my + fy * mh
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    d.text((x0 + 10, y1 - 34), "13 PINS: HORMUZ · GAZA · KYIV · NEPAL ·",
           font=font(FB, 11), fill=CREAM)
    d.text((x0 + 10, y1 - 20), "S. KOREA · SOLOMON IS. · LONDON · WASHINGTON",
           font=font(FB, 11), fill=CREAM)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 78], fill=NAVY)
    d.rectangle([0, 74, W, 78], fill=GOLD)
    d.text((14, 6), "THE WORLD TODAY", font=font(FB, 46), fill=CREAM)
    d.text((14, 56), "45 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           font=font(FB, 13), fill=GOLD)
    d.text((W - 14, 10), "TUESDAY", font=font(FB, 24), fill=CREAM, anchor="ra")
    d.text((W - 14, 38), "24 NOVEMBER 2026", font=font(FB, 24), fill=CREAM,
           anchor="ra")

    # ---- UTC timeline strip ----
    d.rectangle([0, 78, W, 100], fill=(232, 226, 208))
    d.text((14, 83), "UTC", font=font(FB, 12), fill=INK)
    for ex, ecol, elab in [(110, RED, "03:00 Zaporizhzhia strike"),
                           (440, RED, "06:00 Hormuz mines"),
                           (760, GREEN, "14:30 Nasdaq +7%")]:
        d.ellipse([ex - 5, 84, ex + 5, 94], fill=ecol)
        d.text((ex + 9, 83), elab, font=font(FR, 11), fill=INK)

    # ---- Leads ----
    lead_y, lead_h = 104, 222
    lead_w, gap = 330, 7
    for i, (kicker, badge, artist, head, sub) in enumerate(LEADS):
        x0 = 8 + i * (lead_w + gap)
        x1 = x0 + lead_w
        d.rectangle([x0, lead_y, x1, lead_y + lead_h], fill=(255, 255, 255),
                    outline=(180, 184, 188), width=1)
        artist(d, x0 + 1, lead_y + 1, x1 - 1, lead_y + 118)
        d.rectangle([x0, lead_y + 118, x1, lead_y + 140], fill=RED)
        d.text((x0 + 8, lead_y + 122), kicker, font=font(FB, 13), fill=(255, 255, 255))
        bw = d.textlength(badge, font=font(FB, 12)) + 12
        d.rectangle([x1 - 8 - bw, lead_y + 121, x1 - 8, lead_y + 138], fill=GOLD)
        d.text((x1 - 8 - bw + 6, lead_y + 122), badge, font=font(FB, 12),
               fill=INK)
        hl = fit_lines(d, head, font(FB, 17), lead_w - 16, 2)
        yy = lead_y + 146
        for ln in hl:
            d.text((x0 + 8, yy), ln, font=font(FB, 17), fill=INK)
            yy += 20
        sl = fit_lines(d, sub, font(FR, 12), lead_w - 16, 2)
        for ln in sl:
            d.text((x0 + 8, yy), ln, font=font(FR, 12), fill=(60, 64, 72))
            yy += 15

    # ---- Mediums: 2 rows x 5 ----
    med_y, med_h = 334, 152
    med_w, mgap = 198, 8
    for i, (kind, head, sub) in enumerate(MEDIUMS):
        r, c = divmod(i, 5)
        x0 = 8 + c * (med_w + mgap)
        y0 = med_y + r * (med_h + 8)
        x1, y1 = x0 + med_w, y0 + med_h
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                    outline=(180, 184, 188), width=1)
        draw_icon(d, kind, x0 + 1, y0 + 1, x1 - 1, y0 + 62)
        d.rectangle([x0, y0 + 62, x1, y0 + 64], fill=NAVY)
        hl = fit_lines(d, head, font(FB, 13), med_w - 12, 2)
        yy = y0 + 68
        for ln in hl:
            d.text((x0 + 6, yy), ln, font=font(FB, 13), fill=INK)
            yy += 16
        sl = one_line(d, sub, font(FR, 11), med_w - 12)
        d.text((x0 + 6, yy + 2), sl, font=font(FR, 11), fill=(60, 64, 72))

    # ---- Bottom: map + numbered list ----
    bot_y, bot_h = 654, 304
    map_x0, map_x1 = 8, 384
    d.rectangle([map_x0, bot_y, map_x1, bot_y + bot_h], fill=(255, 255, 255),
                outline=(180, 184, 188), width=1)
    d.text((map_x0 + 8, bot_y + 6), "WHERE IT HAPPENED", font=font(FB, 13),
           fill=NAVY)
    draw_map(d, map_x0 + 4, bot_y + 26, map_x1 - 4, bot_y + bot_h - 6)
    lx0 = 396
    d.text((lx0, bot_y + 6), "THE DAY IN 32 LINES", font=font(FB, 13), fill=NAVY)
    d.line([lx0, bot_y + 24, W - 8, bot_y + 24], fill=NAVY, width=2)
    f_num = font(FB, 11)
    f_it = font(FR, 11)
    col_w = (W - 8 - lx0 - 14) // 2
    for idx, item in enumerate(LIST_ITEMS):
        col, row = divmod(idx, 16)
        ix = lx0 + col * (col_w + 14)
        iy = bot_y + 30 + row * 17
        d.text((ix, iy), "%02d" % (idx + 1), font=f_num, fill=RED)
        txt = one_line(d, item, f_it, col_w - 26)
        d.text((ix + 24, iy), txt, font=f_it, fill=INK)

    # ---- Footer: date check + sources ----
    fy = 966
    d.rectangle([8, fy, 620, fy + 50], outline=TEAL, width=2)
    d.rectangle([8, fy, 620, fy + 18], fill=TEAL)
    d.text((14, fy + 2), "DATE CHECK — 24 NOVEMBER 2026", font=font(FB, 11),
           fill=(255, 255, 255))
    d.text((14, fy + 22), "Left out (before today): COP31 collapse 22 Nov ·",
           font=font(FR, 11), fill=INK)
    d.text((14, fy + 36), "Merkury sunk 22 Nov · 'El Chapo Isidro' captured 22 Nov.",
           font=font(FR, 11), fill=INK)
    d.text((W - 8, fy + 4), "SOURCES: AP · REUTERS · BBC · SCMP ·",
           font=font(FR, 11), fill=INK, anchor="ra")
    d.text((W - 8, fy + 18), "JUST SECURITY · THE GLOBAL EYE ·",
           font=font(FR, 11), fill=INK, anchor="ra")
    d.text((W - 8, fy + 32), "HTT NEWS · ANI · SHARJAH24",
           font=font(FR, 11), fill=INK, anchor="ra")
    d.text((W - 8, fy + 46), "THE WORLD TODAY · 24 NOV 2026",
           font=font(FB, 10), fill=GREY, anchor="ra")
    return img


def main():
    img = render()
    img.save("entry.png", format="PNG", optimize=True)
    with open("entry.png", "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("entry.png sha256:", digest)


if __name__ == "__main__":
    main()
