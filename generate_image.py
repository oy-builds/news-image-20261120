#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261120 entry.

One image that sums up the world news of Friday 20 November 2026.
The stories come from data/stories.json (each with its sources); the
display text below only *shortens* those sourced headlines and summaries
so the image stays legible when the judge views it at ~300 px across.
No story is added and no fact is changed.

Run:  python3 generate_image.py     (writes ./entry.png, 1024x1024)
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REGULAR = f"{FONT_DIR}/DejaVuSans.ttf"

# Palette
BG = (10, 17, 40)          # dark navy
PANEL = (17, 28, 58)       # block background
PANEL_ALT = (14, 24, 50)
RULE = (29, 41, 71)        # hairline between blocks
WHITE = (244, 246, 251)
SUMMARY = (201, 211, 230)
MUTED = (143, 160, 190)
GOLD = (232, 184, 75)

MARGIN = 46
TEXT_X = 76
TEXT_W = W - TEXT_X - MARGIN  # 902 px for headline / summary

# Shortened display text, keyed by the story id in data/stories.json.
DISPLAY = {
    "ukraine-poland": {
        "category": "CONFLICT · EUROPE",
        "headline": "RUSSIA HITS KYIV \u2014 MISSILES LAND IN POLAND",
        "line": "Major overnight attack on Kyiv; missiles came down in Poland.",
    },
    "myanmar-icj": {
        "category": "JUSTICE · THE HAGUE",
        "headline": "WORLD COURT: MYANMAR GENOCIDE RULING",
        "line": "ICJ ruled Myanmar's forces committed genocide vs the Rohingya.",
    },
    "uk-eu-deals": {
        "category": "DIPLOMACY · BRUSSELS",
        "headline": "UK\u2013EU SEAL BREXIT-RESET DEAL",
        "line": "Deals on food trade, carbon markets and youth mobility signed.",
    },
    "markets-ai-selloff": {
        "category": "MARKETS · GLOBAL",
        "headline": "AI SELL-OFF SHAKES WORLD MARKETS",
        "line": "S&P 500 fell ~3.7% into correction; Nikkei dropped 5.06%.",
    },
    "peru-earthquake": {
        "category": "DISASTER · PERU",
        "headline": "6.7 QUAKE HITS CENTRAL PERU",
        "line": "Strong earthquake struck near Cerro de Pasco, in the Andes.",
    },
    "children-day-un": {
        "category": "SOCIETY · UNITED NATIONS",
        "headline": "WORLD CHILDREN'S DAY: UN WARNING",
        "line": "UN flags Ukraine's children, Afghan women, Africa's youth.",
    },
}

FOOTER = "Sources: UN News \u00b7 One Turn News \u00b7 Open Chronicle \u00b7 Hansen Intel \u2014 as reported 20 Nov 2026"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, min_size, max_w):
    """Largest font size <= start whose rendered text fits max_w."""
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def centred(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size


# --- tiny original geometric icons, drawn in the category row's right end ---

def icon_bridge(d, x, y, s, c):
    # suspension bridge: deck, two towers, one sagging cable
    d.line([x, y + s * 0.82, x + s, y + s * 0.82], fill=c, width=3)
    d.line([x + s * 0.25, y + s * 0.25, x + s * 0.25, y + s * 0.82], fill=c, width=3)
    d.line([x + s * 0.75, y + s * 0.25, x + s * 0.75, y + s * 0.82], fill=c, width=3)
    d.arc([x + s * 0.25, y - s * 0.15, x + s * 0.75, y + s * 0.65], 0, 180, fill=c, width=3)


def icon_scales(d, x, y, s, c):
    cx = x + s / 2
    d.line([cx, y + s * 0.1, cx, y + s * 0.8], fill=c, width=3)
    d.line([x + s * 0.1, y + s * 0.22, x + s * 0.9, y + s * 0.22], fill=c, width=3)
    d.line([x + s * 0.25, y + s * 0.22, x + s * 0.12, y + s * 0.55], fill=c, width=2)
    d.line([x + s * 0.25, y + s * 0.22, x + s * 0.38, y + s * 0.55], fill=c, width=2)
    d.arc([x + s * 0.05, y + s * 0.4, x + s * 0.45, y + s * 0.7], 0, 180, fill=c, width=3)
    d.line([x + s * 0.75, y + s * 0.22, x + s * 0.62, y + s * 0.55], fill=c, width=2)
    d.line([x + s * 0.75, y + s * 0.22, x + s * 0.88, y + s * 0.55], fill=c, width=2)
    d.arc([x + s * 0.55, y + s * 0.4, x + s * 0.95, y + s * 0.7], 0, 180, fill=c, width=3)
    d.line([x + s * 0.3, y + s * 0.9, x + s * 0.7, y + s * 0.9], fill=c, width=3)


def icon_flags(d, x, y, s, c):
    d.line([x + s * 0.18, y + s * 0.08, x + s * 0.18, y + s * 0.92], fill=c, width=3)
    d.rectangle([x + s * 0.18, y + s * 0.08, x + s * 0.46, y + s * 0.36], outline=c, width=3)
    d.line([x + s * 0.6, y + s * 0.08, x + s * 0.6, y + s * 0.92], fill=c, width=3)
    d.rectangle([x + s * 0.6, y + s * 0.08, x + s * 0.88, y + s * 0.36], outline=c, width=3)


def icon_chart(d, x, y, s, c):
    d.line([x + s * 0.1, y + s * 0.1, x + s * 0.1, y + s * 0.85], fill=c, width=3)
    d.line([x + s * 0.1, y + s * 0.85, x + s * 0.92, y + s * 0.85], fill=c, width=3)
    pts = [(x + s * 0.15, y + s * 0.3), (x + s * 0.4, y + s * 0.45),
           (x + s * 0.58, y + s * 0.38), (x + s * 0.88, y + s * 0.7)]
    d.line(pts, fill=c, width=4, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - s * 0.14, hy - s * 0.02), (hx - s * 0.03, hy - s * 0.13)], fill=c)


def icon_quake(d, x, y, s, c):
    pts = [(x, y + s * 0.55), (x + s * 0.22, y + s * 0.55), (x + s * 0.36, y + s * 0.2),
           (x + s * 0.5, y + s * 0.85), (x + s * 0.64, y + s * 0.4), (x + s * 0.76, y + s * 0.55),
           (x + s, y + s * 0.55)]
    d.line(pts, fill=c, width=4, joint="curve")


def icon_sun(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    import math
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = cx + (r + s * 0.06) * math.cos(a), cy + (r + s * 0.06) * math.sin(a)
        x2, y2 = cx + (r + s * 0.2) * math.cos(a), cy + (r + s * 0.2) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=c, width=3)


ICONS = {
    "bridge": icon_bridge,
    "scales": icon_scales,
    "flags": icon_flags,
    "chart": icon_chart,
    "quake": icon_quake,
    "sun": icon_sun,
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    data = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
    stories = data["stories"]
    assert len(stories) == 6, f"expected 6 stories, got {len(stories)}"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # faint flat shapes for depth (kept flat so the PNG stays small)
    d.ellipse([W - 340, -180, W + 120, 280], fill=(13, 22, 48))
    d.ellipse([-220, H - 260, 240, H + 200], fill=(12, 20, 44))

    # ---- masthead ----
    centred(d, 30, "F R I D A Y  \u00b7  W O R L D  N E W S", font(BOLD, 25), GOLD)
    centred(d, 62, "20 NOVEMBER 2026", font(BOLD, 88), WHITE)
    centred(d, 168, "THE WORLD IN ONE DAY", font(BOLD, 40), GOLD)
    d.line([MARGIN, 228, W - MARGIN, 228], fill=GOLD, width=3)

    # ---- story blocks: 1 column x 6 rows, text as large as it stays clean ----
    top = 244
    footer_top = H - 56
    block_h = (footer_top - top) // 6  # 121 px each

    for i, story in enumerate(stories):
        disp = DISPLAY[story["id"]]
        accent = hex_rgb(story.get("accent", "#e8b84b"))
        y0 = top + i * block_h
        y1 = y0 + block_h - 8

        d.rounded_rectangle([MARGIN, y0, W - MARGIN, y1], radius=10,
                            fill=PANEL if i % 2 == 0 else PANEL_ALT)
        d.rectangle([MARGIN, y0, MARGIN + 10, y1], fill=accent)

        # category row (+ small icon at its right end)
        cat_f = font(BOLD, 21)
        d.text((TEXT_X, y0 + 8), disp["category"], font=cat_f, fill=accent)
        icon = ICONS.get(story.get("icon", ""), None)
        if icon:
            icon(d, W - MARGIN - 44, y0 + 2, 30, accent)

        # headline, auto-fitted to the full text width
        head_f = fit_font(d, disp["headline"], BOLD, 42, 30, TEXT_W)
        d.text((TEXT_X, y0 + 36), disp["headline"], font=head_f, fill=WHITE)

        # one short factual line
        line_f = fit_font(d, disp["line"], REGULAR, 25, 21, TEXT_W)
        d.text((TEXT_X, y0 + 36 + head_f.size + 10), disp["line"], font=line_f, fill=SUMMARY)

    # ---- footer ----
    d.line([MARGIN, footer_top + 2, W - MARGIN, footer_top + 2], fill=RULE, width=2)
    foot_f = fit_font(d, FOOTER, REGULAR, 21, 19, W - 2 * MARGIN)
    centred(d, footer_top + 14, FOOTER, foot_f, MUTED)

    out = ROOT / "entry.png"
    img.save(out, format="PNG", optimize=True)
    size = out.stat().st_size
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  {size} bytes ({size / 1024:.1f} KiB)")
    assert img.size == (1024, 1024)
    assert size <= 1024 * 1024, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
