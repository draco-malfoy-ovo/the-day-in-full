#!/usr/bin/env python3
"""
Render the entry image for make.fun's "Sum up 26 November's world news
in one image" contest: a one-page newspaper-style infographic of the
world news of Thursday 26 November 2026.

Every story below was reported on 26 Nov 2026 and cross-checked across
at least two outlets (Reuters, AP via CNN/Gulf News, Al Jazeera,
The Times, SCMP, The Economic Times, One Turn News, Open Chronicle).
See SOURCES.md for the per-story notes.

The drawing is fully deterministic: fixed canvas, fixed fonts, no
randomness, no clock, no network. Running it twice writes the same
bytes. Output: ../entry.png (1024 x 1024).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W = H = 1024
PAPER = (246, 241, 231)      # warm newsprint
PANEL = (255, 253, 247)      # panel face
INK = (22, 19, 14)           # near-black
MUTE = (96, 88, 74)          # grey-brown for footnotes
RULE = (206, 196, 172)       # hairline
RED = (179, 39, 30)          # accent red
NAVY = (31, 68, 110)         # accent blue
GOLD = (178, 132, 44)        # accent gold
DARK = (24, 26, 31)          # ticker band

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap against pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

MX = 36                      # page margin
CW = W - 2 * MX              # content width

# ---------------------------------------------------------------- masthead

d.text((MX, 24), "THE WORLD'S NEWS · ONE DAY · ONE PICTURE",
       font=font(SANS_B, 23), fill=RED)
d.line([(MX, 58), (W - MX, 58)], fill=INK, width=3)

title = "THE DAY IN FULL"
tf = font(SERIF_B, 62)
d.text(((W - d.textlength(title, font=tf)) / 2, 68), title, font=tf, fill=INK)

# date band — the day, unmissable
d.rectangle([MX, 146, W - MX, 204], fill=RED)
date_line = "THURSDAY  26 NOVEMBER 2026"
df = font(SANS_B, 42)
d.text(((W - d.textlength(date_line, font=df)) / 2, 156),
       date_line, font=df, fill=(255, 250, 240))
d.line([(MX, 216), (W - MX, 216)], fill=INK, width=3)

# ---------------------------------------------------------------- icons
# Small flat spot illustrations, one per story, drawn from primitives
# on the shared canvas (native box about 120 x 90, scaled by s).


def icon_containers(x, y, s):
    """Stacked shipping containers with a percent badge (tariffs)."""
    w, h = int(118 * s), int(30 * s)
    for i, c in enumerate((NAVY, RED, GOLD)):
        yy = y + i * (h + int(6 * s))
        d.rectangle([x, yy, x + w, yy + h], fill=c)
        for k in range(1, 5):
            xx = x + k * w // 5
            d.line([(xx, yy + 3), (xx, yy + h - 3)], fill=(0, 0, 0), width=1)
    r = int(30 * s)
    cx, cy = x + w + int(18 * s), y + int(12 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    d.text((cx, cy), "%", font=font(SANS_B, int(38 * s)),
           fill=(255, 250, 240), anchor="mm")


def icon_flame(x, y, s):
    """Flame over a road with burnt-out cars (Cairo tanker fire)."""
    fx, fy = x + int(46 * s), y
    pts = [(fx, fy), (fx + int(26 * s), fy + int(34 * s)),
           (fx + int(34 * s), fy + int(18 * s)), (fx + int(40 * s), fy + int(52 * s)),
           (fx + int(20 * s), fy + int(66 * s)), (fx - int(2 * s), fy + int(52 * s)),
           (fx - int(6 * s), fy + int(30 * s))]
    d.polygon(pts, fill=RED)
    inner = [(fx + int(14 * s), fy + int(30 * s)), (fx + int(24 * s), fy + int(48 * s)),
             (fx + int(14 * s), fy + int(60 * s)), (fx + int(4 * s), fy + int(46 * s))]
    d.polygon(inner, fill=GOLD)
    ry = y + int(80 * s)
    d.line([(x, ry), (x + int(120 * s), ry)], fill=INK, width=max(2, int(4 * s)))
    for i, cx in enumerate((x + int(8 * s), x + int(52 * s), x + int(92 * s))):
        d.rectangle([cx, ry - int(12 * s), cx + int(24 * s), ry - int(2 * s)],
                    fill=MUTE if i != 1 else INK)


def icon_missile(x, y, s):
    """Skyline with a ballistic missile coming down (Kyiv)."""
    base = y + int(84 * s)
    for bx, bw, bh in ((0, 22, 34), (26, 16, 50), (46, 24, 28), (74, 18, 44), (96, 22, 24)):
        d.rectangle([x + int(bx * s), base - int(bh * s),
                     x + int((bx + bw) * s), base], fill=NAVY)
    d.line([(x, base), (x + int(120 * s), base)], fill=INK, width=max(2, int(3 * s)))
    hx, hy = x + int(84 * s), y + int(2 * s)
    d.polygon([(hx, hy), (hx + int(24 * s), hy + int(14 * s)),
               (hx + int(8 * s), hy + int(30 * s))], fill=RED)
    d.line([(hx + int(3 * s), hy + int(27 * s)), (hx - int(28 * s), hy + int(58 * s))],
           fill=GOLD, width=max(2, int(5 * s)))


def icon_port(x, y, s):
    """Ship, waves and a burst (Gaza strikes / Saudi ports hit)."""
    wy = y + int(64 * s)
    for r in range(2):
        yy = wy + r * int(12 * s)
        for cx in range(0, 120, 30):
            d.arc([x + int(cx * s), yy, x + int((cx + 26) * s), yy + int(14 * s)],
                  0, 180, fill=NAVY, width=max(2, int(3 * s)))
    hx, hy = x + int(26 * s), y + int(38 * s)
    d.polygon([(hx, hy), (hx + int(70 * s), hy), (hx + int(58 * s), hy + int(14 * s)),
               (hx + int(12 * s), hy + int(14 * s))], fill=INK)
    d.rectangle([hx + int(16 * s), hy - int(14 * s), hx + int(34 * s), hy], fill=MUTE)
    bx, by = x + int(98 * s), y + int(8 * s)
    for ang in range(0, 360, 45):
        ex = bx + int(13 * s * math.cos(math.radians(ang)))
        ey = by + int(13 * s * math.sin(math.radians(ang)))
        d.line([(bx, by), (ex, ey)], fill=RED, width=max(2, int(3 * s)))
    d.ellipse([bx - int(4 * s), by - int(4 * s), bx + int(4 * s), by + int(4 * s)], fill=RED)


def icon_eu(x, y, s):
    """Circle of stars around the euro sign (Brussels budget summit)."""
    cx, cy, r = x + int(52 * s), y + int(44 * s), int(38 * s)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        rr = max(2.0, 3.5 * s)
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=GOLD)
    d.text((cx, cy), "€", font=font(SERIF_B, int(52 * s)), fill=NAVY, anchor="mm")


def icon_atom(x, y, s):
    """Atom: nucleus and three elliptical orbits (North Korea)."""
    cx, cy = x + int(52 * s), y + int(44 * s)
    rx, ry = int(50 * s), int(17 * s)
    for deg in (0, 60, 120):
        a = math.radians(deg)
        pts = []
        for t in range(0, 361, 6):
            th = math.radians(t)
            px, py = rx * math.cos(th), ry * math.sin(th)
            pts.append((cx + px * math.cos(a) - py * math.sin(a),
                        cy + px * math.sin(a) + py * math.cos(a)))
        d.line(pts, fill=NAVY, width=max(2, int(3 * s)))
    rr = max(3, int(8 * s))
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=RED)


def icon_satellite(x, y, s):
    """Satellite with panels inside an orbit ring (SpaceX clearance)."""
    d.ellipse([x + int(2 * s), y + int(8 * s), x + int(118 * s), y + int(80 * s)],
              outline=MUTE, width=max(1, int(2 * s)))
    bx, by = x + int(48 * s), y + int(32 * s)
    d.rectangle([bx, by, bx + int(24 * s), by + int(20 * s)], fill=NAVY)
    d.rectangle([bx - int(34 * s), by + int(3 * s), bx - int(4 * s), by + int(17 * s)], fill=GOLD)
    d.rectangle([bx + int(28 * s), by + int(3 * s), bx + int(58 * s), by + int(17 * s)], fill=GOLD)
    d.line([(bx + int(12 * s), by + int(20 * s)), (bx + int(12 * s), by + int(30 * s))],
           fill=INK, width=max(2, int(3 * s)))
    d.ellipse([bx + int(8 * s), by + int(28 * s), bx + int(16 * s), by + int(36 * s)], fill=RED)


# ---------------------------------------------------------------- lead story

LY, LH = 228, 244
d.rectangle([MX, LY, W - MX, LY + LH], fill=PANEL, outline=RULE, width=1)
d.rectangle([MX, LY, MX + 10, LY + LH], fill=RED)
d.text((MX + 30, LY + 16), "TOP STORY — TRADE · WASHINGTON",
       font=font(SANS_B, 22), fill=RED)
text_block(d, (MX + 30, LY + 46),
           "US proposes new tariffs on 14 trading partners",
           font(SERIF_B, 41), INK, 640, 49)
text_block(d, (MX + 30, LY + 152),
           "China faces the highest new rate, 20%, in a US probe into "
           "“structural excess capacity”. The EU, Japan, India and South "
           "Korea are also listed; Beijing calls the charge a false issue.",
           font(SANS_R, 23), INK, 640, 30)
icon_containers(MX + 706, LY + 56, 1.25)

# ---------------------------------------------------------------- grid

stories = [
    ("CAIRO · EGYPT", "Cairo tanker fire kills 31",
     "Flames engulfed 27 vehicles; 21 people were injured.", icon_flame),
    ("KYIV · UKRAINE", "Ballistic missiles strike Kyiv",
     "Seven wounded; grain ships hit near Odesa.", icon_missile),
    ("GAZA · RED SEA", "Gaza strikes; Saudi ports hit",
     "Nine killed in Gaza; a Saudi refinery damaged.", icon_port),
    ("BRUSSELS · EU", "EU haggling over €2tn budget",
     "The bloc's long-term budget and Ukraine aid debated.", icon_eu),
    ("NORTH KOREA", "Kim vows more nuclear arms",
     "He toured nuclear-material production sites.", icon_atom),
    ("SPACE · USA", "SpaceX wins 1M-satellite OK",
     "The FCC authorised the “Starmind” constellation.", icon_satellite),
]

GY = 486
COLW = (CW - 2 * 16) // 3
ROWH = 192
for i, (kick, head, body, icon) in enumerate(stories):
    cx = MX + (i % 3) * (COLW + 16)
    cy = GY + (i // 3) * (ROWH + 12)
    d.rectangle([cx, cy, cx + COLW, cy + ROWH], fill=PANEL, outline=RULE, width=1)
    d.text((cx + 16, cy + 12), kick, font=font(SANS_B, 20), fill=RED)
    icon(cx + COLW - 84, cy + 8, 0.58)
    text_block(d, (cx + 16, cy + 66), head, font(SERIF_B, 29), INK, COLW - 32, 34)
    text_block(d, (cx + 16, cy + 140), body, font(SANS_R, 20), INK, COLW - 32, 25)

# ---------------------------------------------------------------- ticker + footer

TY = 894
d.rectangle([MX, TY, W - MX, TY + 80], fill=DARK)
d.text((MX + 20, TY + 8), "ALSO THURSDAY", font=font(SANS_B, 20), fill=GOLD)
text_block(d, (MX + 20, TY + 32),
           "Ebola cases pass 12,000 in DR Congo's worst outbreak  ·  China "
           "investigates Shanghai party chief Chen Jining  ·  Hong Kong marks "
           "one year since the Tai Po fire", font(SANS_R, 20), (240, 236, 224),
           CW - 40, 23)

d.line([(MX, 986), (W - MX, 986)], fill=INK, width=2)
d.text((MX, 994),
       "Compiled from reports by Reuters, AP, Al Jazeera, CNN, The Times and "
       "SCMP, 26 Nov 2026.", font=font(SANS_R, 18), fill=MUTE)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
img.save(os.path.normpath(out), optimize=True)
print("wrote", os.path.normpath(out), img.size)
