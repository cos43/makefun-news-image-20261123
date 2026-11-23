#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news poster (1024x1024 PNG).

Stories cross-checked on 23 Nov 2026 against SCMP, AFP, CNN, Japan Times,
WION, Economic Times and Indian Express headlines of that day.
The poster itself is shipped as entry.png; main.ts only copies it.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 21, 38)
PANEL = (22, 35, 60)
PANEL2 = (27, 42, 70)
WHITE = (245, 247, 250)
GREY = (178, 190, 208)
RED = (232, 64, 64)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- header ----------
d.text((48, 34), "THE WORLD IN ONE DAY", font=font(BOLD, 30), fill=RED)
d.text((48, 74), "MONDAY 23 NOVEMBER 2026", font=font(BOLD, 55), fill=WHITE)
d.rectangle([48, 148, W - 48, 154], fill=RED)

# ---------- panels ----------
def panel(x, y, w_, h_, tag, tag_color, headline, sub, head_size=35):
    d.rounded_rectangle([x, y, x + w_, y + h_], radius=18, fill=PANEL)
    d.rectangle([x, y + 14, x + 8, y + h_ - 14], fill=tag_color)
    tx = x + 28
    d.text((tx, y + 16), tag, font=font(BOLD, 23), fill=tag_color)
    lines = wrap(d, headline, font(BOLD, head_size), w_ - 52)
    yy = y + 50
    for ln in lines:
        d.text((tx, yy), ln, font=font(BOLD, head_size), fill=WHITE)
        yy += head_size + 7
    for ln in wrap(d, sub, font(REG, 24), w_ - 52):
        d.text((tx, yy + 4), ln, font=font(REG, 24), fill=GREY)
        yy += 31

# lead story, full width
panel(48, 172, W - 96, 178, "CLIMATE  ·  COP31", (96, 200, 120),
      "COP31 climate talks collapse with no deal",
      "Nearly 200 countries end the summit divided over fossil fuels; "
      "the EU rejects the final text.",
      head_size=37)

# 2 x 2 grid
gy, gh, gw = 370, 224, (W - 96 - 24) // 2
panel(48, gy, gw, gh, "UNITED STATES", (110, 168, 255),
      "Democrats clinch historic House majority",
      "At least 258 seats, their largest since 1992.", head_size=30)
panel(48 + gw + 24, gy, gw, gh, "EUROPE  ·  UKRAINE WAR", (255, 176, 84),
      "Russian strikes kill 15 in Kyiv region",
      "Poland says 3 Russian missiles crossed into its airspace.",
      head_size=30)
panel(48, gy + gh + 20, gw, gh, "MIDDLE EAST  ·  ENERGY", (255, 110, 110),
      "Hormuz shipping attacks hit highest level of the war",
      "Tankers ablaze in the strait, yet oil prices fall.",
      head_size=30)
panel(48 + gw + 24, gy + gh + 20, gw, gh, "ASIA", (190, 140, 255),
      "Nepal's PM Shah meets Modi in Delhi",
      "Energy ties and a new Ayodhya-Janakpur train launch.",
      head_size=30)

# ---------- also today ----------
ty = gy + 2 * gh + 40
d.text((48, ty), "ALSO TODAY", font=font(BOLD, 24), fill=RED)
also_text = ("Japan-Europe probes enter Mercury's orbit  •  Alcaraz beats Zverev "
             "for his first ATP Finals title  •  Ukraine drone damages a Russian "
             "corvette off Libya  •  Asian markets slide as the AI sell-off deepens  •  "
             "Drone strikes hit homes and a UN building in Sudan's capital")
yy = ty + 36
for ln in wrap(d, also_text, font(REG, 24), W - 96):
    d.text((48, yy), ln, font=font(REG, 24), fill=(210, 218, 232))
    yy += 32

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
