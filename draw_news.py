#!/usr/bin/env python3
"""Draw a one-page newspaper front page summing up world news.

Reads nothing but the stories listed below, draws everything with Pillow
shapes and text, and writes news.png (1024x1024, under 1 MiB) next to
this script.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "news.png")

PAGE = 1024
MARGIN = 24

PAPER = (247, 243, 232)
NAVY = (16, 38, 74)
GOLD = (201, 162, 39)
INK = (26, 26, 26)
BODY_INK = (40, 40, 40)
MUTED = (110, 105, 90)
RULE = (180, 172, 150)
CARD_BG = (255, 253, 246)
RED = (178, 34, 34)
GREEN_DARK = (38, 74, 52)
SKY_NIGHT = (52, 56, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu face, falling back to Pillow's built-in font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def serif_bold(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def serif_italic(size):
    return font("DejaVuSerif-Italic.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw wrapped lines top-down; return the y just past the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_field(draw, box, count, seed=7):
    """Scatter small white dots across a rectangle, like stars."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(count):
        px = rng.randint(x0 + 4, x1 - 4)
        py = rng.randint(y0 + 4, y1 - 4)
        r = rng.choice([1, 1, 2])
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 255, 255))


def burst(draw, cx, cy, radius, colour):
    """A round explosion with short rays sticking out of it."""
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=colour)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x0 = cx + int(radius * 0.9 * math.cos(rad))
        y0 = cy + int(radius * 0.9 * math.sin(rad))
        x1 = cx + int((radius + 12) * math.cos(rad))
        y1 = cy + int((radius + 12) * math.sin(rad))
        draw.line([x0, y0, x1, y1], fill=colour, width=4)
    draw.ellipse([cx - radius // 2, cy - radius // 2,
                  cx + radius // 2, cy + radius // 2], fill=(255, 214, 90))


def lead_art(draw, box):
    """Night sky over hills, a missile arc and its burst, for the lead."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY_NIGHT)
    star_field(draw, (x0, y0, x1, y0 + 60), 16, seed=21)
    horizon = y0 + 78
    draw.polygon([(x0, y1), (x0, horizon + 18), (x1, horizon - 6),
                  (x1, y1)], fill=GREEN_DARK)
    draw.polygon([(x0 + 300, y1), (x0 + 430, horizon - 4),
                  (x0 + 620, y1)], fill=(74, 66, 60))
    arc = []
    for t in range(0, 101):
        fx = x0 + 120 + t * 4.4
        fy = y0 + 18 + int(40 * (t / 100.0) ** 1.5)
        arc.append((fx, fy))
    draw.line(arc, fill=GOLD, width=3)
    burst(draw, x0 + 620, y0 + 62, 26, (232, 116, 39))
    draw.polygon([(x1 - 130, y0 + 52), (x1 - 96, y0 + 58),
                  (x1 - 130, y0 + 64)], fill=(230, 230, 230))


def chart_art(draw, box):
    """Falling red bars with a downward trend line, for the markets card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 228, 220))
    heights = [46, 38, 42, 30, 34, 22, 16]
    bw = (x1 - x0 - 40) // len(heights)
    tops = []
    for i, h in enumerate(heights):
        bx = x0 + 20 + i * bw
        draw.rectangle([bx, y1 - 8 - h, bx + bw - 8, y1 - 8],
                       fill=(150, 52, 44))
        tops.append((bx + (bw - 8) // 2, y1 - 8 - h - 6))
    draw.line(tops, fill=RED, width=3)
    ex, ey = tops[-1]
    draw.polygon([(ex, ey - 8), (ex + 16, ey + 2), (ex - 2, ey + 10)],
                 fill=RED)


def quake_art(draw, box):
    """Mountains and a jagged seismograph line, for the Peru card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 222, 200))
    peaks = [(x0, y1), (x0 + 90, y0 + 22), (x0 + 210, y1),
             (x0 + 300, y0 + 10), (x0 + 420, y1)]
    draw.polygon(peaks, fill=(96, 84, 72))
    for px, py in [(x0 + 90, y0 + 22), (x0 + 300, y0 + 10)]:
        draw.polygon([(px - 16, py + 12), (px, py), (px + 16, py + 12)],
                     fill=(255, 255, 255))
    zig = []
    step = (x1 - x0) // 12
    for i in range(13):
        zig.append((x0 + i * step, y1 - 14 - (18 if i % 2 else 4)))
    draw.line(zig, fill=RED, width=2)


def climate_art(draw, box):
    """A small globe, a sun and a clock, for the climate card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 231, 238))
    draw.ellipse([x0 + 130, y0 + 12, x0 + 178, y0 + 60],
                 fill=(52, 120, 180))
    draw.ellipse([x0 + 142, y0 + 22, x0 + 162, y0 + 34],
                 fill=(72, 160, 90))
    draw.ellipse([x0 + 150, y0 + 40, x0 + 170, y0 + 54],
                 fill=(72, 160, 90))
    cx, cy = x0 + 380, y0 + 26
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 180, 60))
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        draw.line([cx + int(18 * math.cos(rad)), cy + int(18 * math.sin(rad)),
                   cx + int(26 * math.cos(rad)), cy + int(26 * math.sin(rad))],
                  fill=(240, 180, 60), width=3)
    draw.ellipse([x0 + 388, y0 + 40, x0 + 414, y0 + 66], outline=INK, width=2)
    draw.line([x0 + 401, y0 + 53, x0 + 401, y0 + 44], fill=INK, width=2)
    draw.line([x0 + 401, y0 + 53, x0 + 409, y0 + 57], fill=INK, width=2)


def flags_art(draw, box):
    """Two stylised flags joined by an arc, for the UK-EU card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(226, 230, 236))
    fx, fy, fw, fh = x0 + 40, y0 + 12, 150, 44
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(20, 40, 90))
    draw.rectangle([fx + fw // 2 - 7, fy, fx + fw // 2 + 7, fy + fh],
                   fill=(200, 40, 50))
    draw.rectangle([fx, fy + fh // 2 - 6, fx + fw, fy + fh // 2 + 6],
                   fill=(200, 40, 50))
    gx, gy, gw, gh = x0 + 270, y0 + 12, 150, 44
    draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(20, 40, 110))
    for k in range(8):
        ang = math.radians(k * 45)
        dx = gx + gw // 2 + int(15 * math.cos(ang))
        dy = gy + gh // 2 + int(12 * math.sin(ang))
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=GOLD)
    pts = []
    for t in range(0, 101):
        pts.append((x0 + 60 + t * 3.4,
                    y0 + 58 - int(10 * math.sin(math.pi * t / 100.0))))
    draw.line(pts, fill=GOLD, width=3)


CARD_ART = {
    "markets": chart_art,
    "quake": quake_art,
    "climate": climate_art,
    "flags": flags_art,
}

STORIES = [
    ("markets", "WALL STREET SLIDES INTO CORRECTION",
     "The S&P 500 falls 3.7% and the Nasdaq 5.3% as the AI trade "
     "unwinds; Nvidia drops 14% on a reported SEC accounting probe."),
    ("quake", "6.8 QUAKE SHAKES PERU, FELT IN LIMA",
     "The tremor strikes the Junin region of the Andes; residents run "
     "into the streets of the capital, Lima, 320 km away."),
    ("climate", "COP31 IN ANTALYA MISSES ITS DEADLINE",
     "The climate summit runs past its deadline with a draft that "
     "drops any mention of fossil fuels."),
    ("flags", "UK AND EU SEAL FOOD, CARBON AND YOUTH DEALS",
     "Brussels agrees to scrap most food and farm checks from March "
     "2028, link carbon markets, and open a youth mobility scheme."),
]

ALSO_TODAY = [
    "Trump threatens a \u201ctremendous tax\u201d on US firms building AI "
    "data centres overseas.",
    "New York Mayor Mamdani sets 2032 as the date to close the Rikers "
    "Island jail.",
    "Saudi-led strikes hit Yemen as the Houthi fighting escalates; "
    "Nepal\u2019s PM visits Delhi.",
]

LEAD_HEADLINE = "RUSSIAN MISSILES CRASH IN POLAND"
LEAD_BODY = (
    "Two Kh-101 cruise missiles and a jet-powered drone come down in "
    "south-east Poland during a huge Russian strike on Ukraine. No one "
    "is hurt. PM Donald Tusk calls it a deliberate provocation; NATO "
    "calls it a grave violation of Polish airspace."
)


def draw_card(draw, box, art_key, headline, body):
    """One grid card: art strip on top, headline, then body text."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD_BG, outline=RULE, width=1)
    art_h = 64
    CARD_ART[art_key](draw, (x0 + 1, y0 + 1, x1 - 1, y0 + art_h))
    draw.rectangle([x0, y0 + art_h, x1, y0 + art_h + 4], fill=GOLD)
    tx = x0 + 12
    tw = (x1 - x0) - 24
    head_font = serif_bold(21)
    lines = wrap(draw, headline, head_font, tw)
    y = draw_lines(draw, lines, tx, y0 + art_h + 12, head_font, NAVY, 26)
    body_font = serif(16)
    body_lines = wrap(draw, body, body_font, tw)
    draw_lines(draw, body_lines, tx, y + 4, body_font, BODY_INK, 22)


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, PAGE, 112], fill=NAVY)
    title_font = serif_bold(52)
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=title_font)
    draw.text(((PAGE - tw) / 2, 18), title, font=title_font,
              fill=(255, 255, 255))
    date_font = sans_bold(23)
    date_line = "SATURDAY 21 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=date_font)
    draw.text(((PAGE - dw) / 2, 76), date_line, font=date_font, fill=GOLD)
    draw.rectangle([0, 112, PAGE, 118], fill=GOLD)

    # Lead illustration and story.
    lead_art(draw, (MARGIN, 128, PAGE - MARGIN, 252))
    draw.rectangle([MARGIN, 252, PAGE - MARGIN, 256], fill=GOLD)
    head_font = serif_bold(38)
    hw = draw.textlength(LEAD_HEADLINE, font=head_font)
    draw.text(((PAGE - hw) / 2, 266), LEAD_HEADLINE, font=head_font,
              fill=NAVY)
    body_font = serif(20)
    body_lines = wrap(draw, LEAD_BODY, body_font, PAGE - 2 * MARGIN)
    draw_lines(draw, body_lines, MARGIN, 312, body_font, BODY_INK, 28)

    # 2x2 grid of other stories.
    grid_top = 408
    card_w = (PAGE - 2 * MARGIN - 16) // 2
    card_h = 220
    for i, (art_key, headline, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x0 = MARGIN + col * (card_w + 16)
        y0 = grid_top + row * (card_h + 12)
        draw_card(draw, (x0, y0, x0 + card_w, y0 + card_h),
                  art_key, headline, body)

    # Also-today strip.
    strip_top = grid_top + 2 * card_h + 12 + 12
    draw.rectangle([MARGIN, strip_top, PAGE - MARGIN, strip_top + 34],
                   fill=NAVY)
    label_font = sans_bold(19)
    draw.text((MARGIN + 12, strip_top + 6), "ALSO TODAY",
              font=label_font, fill=(255, 255, 255))
    bullet_font = serif(17)
    by = strip_top + 44
    for item in ALSO_TODAY:
        lines = wrap(draw, item, bullet_font, PAGE - 2 * MARGIN - 28)
        draw.ellipse([MARGIN + 6, by + 7, MARGIN + 14, by + 15], fill=RED)
        by = draw_lines(draw, lines, MARGIN + 24, by, bullet_font,
                        BODY_INK, 23)

    # Footer.
    foot_font = serif_italic(13)
    foot = "All events of Saturday 21 November 2026, as reported."
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((PAGE - fw) / 2, PAGE - 26), foot, font=foot_font, fill=MUTED)

    img.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"wrote {OUT_PATH}: {img.size[0]}x{img.size[1]}, {size} bytes")


if __name__ == "__main__":
    build()
