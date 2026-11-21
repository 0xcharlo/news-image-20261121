#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 (news.png).

A newspaper front page drawn with Pillow: navy masthead, one wide lead
story on Russian missiles crashing in Poland, a 2x2 grid of the day's
other big stories, and an ALSO TODAY briefs strip. No image generator
is used, so no text is garbled. Every headline was checked against
live reporting (AP/BBC via wire digests, Reuters, Motley Fool, CNBC).
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 244, 236)
CARD = (255, 255, 255)
INK = (24, 24, 24)
NAVY = (13, 38, 68)
NAVY_DEEP = (9, 27, 50)
GOLD = (198, 158, 38)
GOLD_SOFT = (214, 178, 88)
GREY = (98, 98, 98)
RULE = (214, 208, 194)
CRIMSON = (172, 40, 46)
TEAL = (23, 96, 110)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_lines(draw, x, y, lines, fnt, fill, step):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# ------------------------------------------------------------------ scenes
def scene_missile(draw, x0, y0, x1, y1):
    """Dusk sky over Polish farmland: a missile trail and a burst."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y0 + h * 0.62], fill=(58, 58, 84))
    draw.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(44, 66, 44))
    # stars
    for sx, sy in ((0.12, 0.14), (0.30, 0.08), (0.55, 0.18), (0.78, 0.10),
                   (0.90, 0.24), (0.42, 0.26)):
        draw.ellipse([x0 + (x1 - x0) * sx - 2, y0 + h * sy - 2,
                      x0 + (x1 - x0) * sx + 2, y0 + h * sy + 2],
                     fill=(235, 235, 225))
    # missile trail arcing down to the burst
    bx = x0 + (x1 - x0) * 0.62
    by = y0 + h * 0.58
    pts = []
    for t in range(0, 21):
        f = t / 20.0
        px = x0 + (x1 - x0) * 0.18 + f * (bx - x0 - (x1 - x0) * 0.18)
        py = y0 + h * 0.06 + f * f * (by - y0 - h * 0.06)
        pts.append((px, py))
    draw.line(pts, fill=(255, 190, 90), width=4)
    # explosion burst over the field
    for r, col in ((30, (255, 120, 40)), (20, (255, 180, 80)),
                   (11, (255, 230, 150))):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        ex = bx + int(math.cos(rad) * 40)
        ey = by + int(math.sin(rad) * 40)
        draw.line([(bx, by), (ex, ey)], fill=(255, 150, 60), width=3)
    # treeline and a road
    for tx in range(x0 + 8, x1 - 8, 26):
        draw.ellipse([tx, y0 + h * 0.62 - 12, tx + 18,
                      y0 + h * 0.62 + 2], fill=(30, 48, 32))
    draw.polygon([(x0 + (x1 - x0) * 0.30, y1),
                  (x0 + (x1 - x0) * 0.46, y0 + h * 0.62),
                  (x0 + (x1 - x0) * 0.56, y0 + h * 0.62),
                  (x0 + (x1 - x0) * 0.72, y1)], fill=(70, 66, 60))
    # a small jet silhouette top right
    jx, jy = x0 + (x1 - x0) * 0.86, y0 + h * 0.16
    draw.polygon([(jx - 16, jy), (jx + 14, jy - 4), (jx + 18, jy),
                  (jx + 14, jy + 4)], fill=(220, 220, 210))


def scene_market(draw, x0, y0, x1, y1):
    """A falling red chart: bars stepping down, arrow pointing down."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 228))
    base = y0 + h * 0.88
    bars = [0.78, 0.66, 0.70, 0.52, 0.56, 0.38, 0.22]
    bw = (x1 - x0) / (len(bars) + 1)
    for i, frac in enumerate(bars):
        bx = x0 + (i + 0.6) * bw
        top = base - frac * h * 0.72
        draw.rectangle([bx, top, bx + bw * 0.62, base],
                       fill=CRIMSON if i >= len(bars) - 2 else (120, 60, 60))
    pts = []
    for i, frac in enumerate(bars):
        bx = x0 + (i + 0.6) * bw + bw * 0.31
        pts.append((bx, base - frac * h * 0.72 - 8))
    draw.line(pts, fill=CRIMSON, width=4)
    ex, ey = pts[-1]
    draw.polygon([(ex - 12, ey - 4), (ex + 2, ey + 14), (ex + 10, ey - 10)],
                 fill=CRIMSON)
    draw.line([x0, base, x1, base], fill=INK, width=2)


def scene_quake(draw, x0, y0, x1, y1):
    """Andean peaks shaking: a jagged crack and a seismograph trace."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(214, 204, 186))
    # mountain ridge
    ridge = [(x0, y1), (x0 + (x1 - x0) * 0.18, y0 + h * 0.34),
             (x0 + (x1 - x0) * 0.34, y0 + h * 0.62),
             (x0 + (x1 - x0) * 0.52, y0 + h * 0.22),
             (x0 + (x1 - x0) * 0.70, y0 + h * 0.58),
             (x0 + (x1 - x0) * 0.86, y0 + h * 0.30), (x1, y1)]
    draw.polygon(ridge, fill=(96, 84, 70))
    # snow caps
    for px, py in ((0.18, 0.34), (0.52, 0.22), (0.86, 0.30)):
        cx = x0 + (x1 - x0) * px
        cy = y0 + h * py
        draw.polygon([(cx - 12, cy + 8), (cx, cy - 2), (cx + 12, cy + 8)],
                     fill=(250, 250, 246))
    # crack zig-zagging down the slope
    cx = x0 + (x1 - x0) * 0.52
    cy = y0 + h * 0.30
    pts = [(cx, cy)]
    for i in range(1, 6):
        pts.append((cx + (14 if i % 2 else -14), cy + i * h * 0.12))
    draw.line(pts, fill=(40, 32, 26), width=3)
    # seismograph trace across the bottom
    sy = y0 + h * 0.86
    trace = [(x0 + 6, sy)]
    for i in range(1, 24):
        amp = 2 if i < 8 else (16 if 8 <= i < 15 else 3)
        trace.append((x0 + 6 + i * (x1 - x0 - 12) / 23,
                      sy + (amp if i % 2 else -amp)))
    draw.line(trace, fill=CRIMSON, width=2)


def scene_climate(draw, x0, y0, x1, y1):
    """A globe under a hot sun, with a clock running past its deadline."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(206, 226, 232))
    cx = x0 + (x1 - x0) * 0.36
    cy = y0 + h * 0.46
    r = h * 0.34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 150))
    draw.ellipse([cx - r * 0.55, cy - r * 0.72, cx + r * 0.42,
                  cy - r * 0.18], fill=(52, 130, 80))
    draw.ellipse([cx - r * 0.30, cy + r * 0.30, cx + r * 0.62,
                  cy + r * 0.78], fill=(52, 130, 80))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340,
             fill=(220, 235, 240), width=2)
    # sun
    sx = x0 + (x1 - x0) * 0.82
    sy = y0 + h * 0.22
    draw.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(255, 180, 60))
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        draw.line([(sx + int(math.cos(rad) * 15), sy + int(math.sin(rad) * 15)),
                   (sx + int(math.cos(rad) * 22), sy + int(math.sin(rad) * 22))],
                  fill=(255, 180, 60), width=3)
    # clock
    kx = x0 + (x1 - x0) * 0.80
    ky = y0 + h * 0.72
    kr = 13
    draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr],
                 fill=(255, 255, 255), outline=INK, width=2)
    draw.line([(kx, ky), (kx, ky - kr + 3)], fill=INK, width=2)
    draw.line([(kx, ky), (kx + kr - 5, ky + 3)], fill=INK, width=2)


def scene_flags(draw, x0, y0, x1, y1):
    """Union Jack and EU flag panels joined by a gold bridge arc."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 232, 226))
    fw, fh = (x1 - x0) * 0.36, h * 0.56
    fy = y0 + h * 0.16
    # Union Jack (simplified): blue field, white and red crosses
    ux = x0 + (x1 - x0) * 0.08
    draw.rectangle([ux, fy, ux + fw, fy + fh], fill=(28, 52, 110))
    draw.rectangle([ux, fy + fh * 0.40, ux + fw, fy + fh * 0.60],
                   fill=(255, 255, 255))
    draw.rectangle([ux + fw * 0.44, fy, ux + fw * 0.56, fy + fh],
                   fill=(255, 255, 255))
    draw.rectangle([ux, fy + fh * 0.45, ux + fw, fy + fh * 0.55],
                   fill=(200, 30, 40))
    draw.rectangle([ux + fw * 0.47, fy, ux + fw * 0.53, fy + fh],
                   fill=(200, 30, 40))
    # EU flag: blue field, ring of gold stars
    ex = x1 - (x1 - x0) * 0.08 - fw
    draw.rectangle([ex, fy, ex + fw, fy + fh], fill=(22, 48, 120))
    ecx, ecy = ex + fw / 2, fy + fh / 2
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx = ecx + math.cos(ang) * fw * 0.30
        sy = ecy + math.sin(ang) * fh * 0.30
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD_SOFT)
    # bridge arc joining them
    draw.arc([ux + fw * 0.5, fy + fh - 6, ex + fw * 0.5, fy + fh + 26],
             180, 360, fill=GOLD, width=4)



# ------------------------------------------------------------------ page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.rectangle([0, 112, W, 116], fill=GOLD)
    draw.text((W / 2, 12), "THE WORLD IN ONE IMAGE",
              font=load(SERIF_B, 54), fill=(255, 255, 255), anchor="ma")
    draw.text((W / 2, 74), "SATURDAY 21 NOVEMBER 2026",
              font=load(SANS_B, 24), fill=GOLD_SOFT, anchor="ma")

    # Lead story: Russian missiles in Poland
    lx, ly, lw, lh = 24, 132, 976, 318
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD,
                   outline=RULE, width=1)
    scene_missile(draw, lx + 1, ly + 1, lx + lw - 1, ly + 156)
    draw.rectangle([lx, ly + 156, lx + lw, ly + 160], fill=GOLD)
    head = fit_lines(draw, "RUSSIAN MISSILES CRASH IN POLAND",
                     load(SANS_B, 32), lw - 32)
    y = draw_lines(draw, lx + 16, ly + 170, head, load(SANS_B, 32),
                   NAVY, 38)
    body = fit_lines(
        draw,
        "Two Kh-101 cruise missiles and a jet-powered drone come down "
        "in south-east Poland during a huge Russian strike on Ukraine. "
        "No one is hurt. PM Donald Tusk calls it a deliberate "
        "provocation; NATO calls it a grave violation of Polish airspace.",
        load(SANS, 20), lw - 32)
    draw_lines(draw, lx + 16, y + 4, body, load(SANS, 20), INK, 26)

    # 2x2 grid of the day's other stories
    gx, gy = 24, 466
    cw, ch, gap = 476, 172, 16
    stories = [
        ("WALL STREET SLIDES INTO CORRECTION",
         "The S&P 500 falls 3.7% and the Nasdaq 5.3% as the AI trade "
         "unwinds; Nvidia drops 14% on a reported SEC accounting probe.",
         scene_market),
        ("6.8 QUAKE SHAKES PERU, FELT IN LIMA",
         "The tremor strikes the Jun\u00edn region of the Andes; residents "
         "run into the streets of the capital. No casualties reported.",
         scene_quake),
        ("COP31 IN ANTALYA MISSES ITS DEADLINE",
         "The climate summit runs past its deadline with a draft that "
         "drops any mention of fossil fuels.",
         scene_climate),
        ("UK AND EU SEAL FOOD, CARBON AND YOUTH DEALS",
         "Brussels agrees to scrap most food and farm checks from March "
         "2028, link carbon markets, and open a youth mobility scheme.",
         scene_flags),
    ]
    for i, (headline, body, scene) in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD,
                       outline=RULE, width=1)
        scene(draw, cx + 1, cy + 1, cx + cw - 1, cy + 61)
        draw.rectangle([cx, cy + 61, cx + cw, cy + 65], fill=GOLD)
        h_lines = fit_lines(draw, headline, load(SANS_B, 20), cw - 24)
        y = draw_lines(draw, cx + 12, cy + 72, h_lines, load(SANS_B, 20),
                       NAVY, 24)
        b_lines = fit_lines(draw, body, load(SANS, 16), cw - 24)
        draw_lines(draw, cx + 12, y + 2, b_lines, load(SANS, 16), INK, 20)

    # ALSO TODAY briefs strip
    sy = 842
    draw.rectangle([24, sy, W - 24, sy + 114], fill=CARD,
                   outline=RULE, width=1)
    draw.rectangle([24, sy, W - 24, sy + 34], fill=NAVY)
    draw.text((40, sy + 6), "ALSO TODAY", font=load(SANS_B, 20),
              fill=(255, 255, 255))
    briefs = [
        "Trump threatens to bar US firms from building AI data centres "
        "overseas and impose a \u201ctremendous tax\u201d on them.",
        "New York Mayor Mamdani sets 2032 as the date to close the "
        "Rikers Island jail complex.",
        "Saudi-led strikes hit Yemen as fighting with the Houthis "
        "escalates; Nepal\u2019s PM heads to Delhi on his first trip abroad.",
    ]
    y = sy + 44
    for brief in briefs:
        draw.ellipse([40, y + 7, 48, y + 15], fill=CRIMSON)
        lines = fit_lines(draw, brief, load(SANS, 17), W - 24 - 64 - 24)
        y = draw_lines(draw, 60, y, lines, load(SANS, 17), INK, 21)
        y += 5

    # Footer
    draw.text((W / 2, 974), "All events of Saturday 21 November 2026, as reported.",
              font=load(SERIF, 17), fill=GREY, anchor="ma")

    img.save("news.png", optimize=True)
    print("saved news.png")


if __name__ == "__main__":
    main()
