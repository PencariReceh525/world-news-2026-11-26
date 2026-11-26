"""Draw the entry image: the world news of Thursday 26 November 2026 in one picture.

Run locally (needs Pillow) to regenerate entry.png:
    python3 generate_image.py

The submitted program is main.py, which only copies entry.png to the output
directory, so the grader's standard-library-only sandbox never needs Pillow.

Stories (all reported on 26 November 2026, cross-checked across Reuters, BBC,
The Hindu, France 24 and same-day news digests):
  1. US proposes new tariffs on 14 trading partners (China, EU, Japan, India).
  2. Fuel tanker fire on Cairo's ring road kills at least 31 people.
  3. Houthis claim strikes on Saudi ports and the Ras Tanura refinery.
  4. Ukraine says it damaged five jets at Russia's Savasleyka airbase;
     Russia hits two grain ships near Odesa.
  5. Rescuers search for 13 miners trapped in a flooded West Java gold mine.
  6. Muhammad Zeeshan Ali becomes the first Pakistani / foreign astronaut
     aboard China's Tiangong station, arriving on Shenzhou-24.
Footer strip: EU leaders clash in Brussels over a Ukraine loan, North Korea's
Kim urges wider tactical-nuclear deployment, the AI sell-off hits the Nasdaq,
Spain heads to a snap election, and an Israeli strike in Gaza.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 242, 231)
INK = (18, 22, 32)
MUTED = (92, 96, 106)
RULE = (18, 22, 32)
RED = (178, 34, 44)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = FONT_DIR + "/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "/liberation/LiberationSans-Bold.ttf"
SANS = FONT_DIR + "/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, box, color, kicker, headline, body, icon):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=(205, 198, 182), width=2)
    draw.rectangle([x0, y0, x1, y0 + 14], fill=color)
    # icon disc
    cx, cy, r = x0 + 56, y0 + 88, 38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    icon(draw, cx, cy, r)
    tx = x0 + 110
    draw.text((tx, y0 + 26), kicker, font=font(SANS_BOLD, 22), fill=color)
    hy = y0 + 54
    for line in wrap(draw, headline, font(SANS_BOLD, 32), x1 - tx - 16):
        draw.text((tx, hy), line, font=font(SANS_BOLD, 32), fill=INK)
        hy += 37
    by = y0 + 132
    for line in wrap(draw, body, font(SANS, 23), x1 - x0 - 34):
        draw.text((x0 + 17, by), line, font=font(SANS, 23), fill=(52, 56, 66))
        by += 28


def icon_percent(draw, cx, cy, r):
    f = font(SANS_BOLD, 52)
    draw.text((cx, cy), "%", font=f, fill=WHITE, anchor="mm")


def icon_flame(draw, cx, cy, r):
    draw.polygon([(cx, cy - 30), (cx + 20, cy + 4), (cx + 14, cy + 26),
                  (cx - 14, cy + 26), (cx - 20, cy + 4)], fill=WHITE)
    draw.polygon([(cx, cy - 6), (cx + 10, cy + 12), (cx + 6, cy + 24),
                  (cx - 6, cy + 24), (cx - 10, cy + 12)], fill=(255, 140, 40))


def icon_oil(draw, cx, cy, r):
    draw.line([cx - 22, cy + 26, cx, cy - 26], fill=WHITE, width=7)
    draw.line([cx + 22, cy + 26, cx, cy - 26], fill=WHITE, width=7)
    draw.line([cx - 14, cy + 6, cx + 14, cy + 6], fill=WHITE, width=6)
    draw.line([cx - 26, cy + 26, cx + 26, cy + 26], fill=WHITE, width=7)


def icon_jet(draw, cx, cy, r):
    draw.polygon([(cx + 28, cy - 6), (cx - 4, cy - 6), (cx - 18, cy - 24),
                  (cx - 26, cy - 24), (cx - 18, cy - 2), (cx - 30, cy + 14),
                  (cx - 20, cy + 14), (cx - 8, cy + 4), (cx - 4, cy + 18),
                  (cx + 2, cy + 18), (cx + 6, cy + 4), (cx + 18, cy + 2)],
                 fill=WHITE)


def icon_mine(draw, cx, cy, r):
    draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], start=180, end=360,
             fill=WHITE, width=7)
    draw.line([cx - 26, cy + 26, cx - 26, cy - 2], fill=WHITE, width=7)
    draw.line([cx + 26, cy + 26, cx + 26, cy - 2], fill=WHITE, width=7)
    draw.line([cx - 30, cy + 26, cx + 30, cy + 26], fill=WHITE, width=7)
    draw.ellipse([cx - 6, cy - 2, cx + 6, cy + 10], fill=WHITE)


def icon_rocket(draw, cx, cy, r):
    draw.polygon([(cx, cy - 30), (cx + 13, cy - 4), (cx + 13, cy + 14),
                  (cx - 13, cy + 14), (cx - 13, cy - 4)], fill=WHITE)
    draw.polygon([(cx - 13, cy + 8), (cx - 26, cy + 26), (cx - 13, cy + 22)],
                 fill=WHITE)
    draw.polygon([(cx + 13, cy + 8), (cx + 26, cy + 26), (cx + 13, cy + 22)],
                 fill=WHITE)
    draw.ellipse([cx - 6, cy - 16, cx + 6, cy - 4], fill=(70, 130, 200))
    draw.polygon([(cx - 5, cy + 18), (cx + 5, cy + 18), (cx, cy + 30)],
                 fill=(255, 170, 40))


PANELS = [
    ((178, 34, 44), "TRADE - WASHINGTON",
     "US proposes new tariffs on 14 partners",
     "Rates up to 35% on China, the EU, Japan and India. India faces 25%. "
     "Markets rattled worldwide.",
     icon_percent),
    ((214, 110, 20), "DISASTER - CAIRO, EGYPT",
     "Fuel tanker fire kills at least 31",
     "A tanker overturned and burst into flames on Cairo's ring road. "
     "About 21 people were injured.",
     icon_flame),
    ((20, 120, 90), "MIDDLE EAST - SAUDI",
     "Houthis strike Saudi refinery and ports",
     "Attacks claimed on the Ras Tanura refinery; missiles downed near "
     "Riyadh. Oil prices climbed.",
     icon_oil),
    ((44, 92, 178), "WAR IN EUROPE - UKRAINE",
     "Ukraine hits Russian airbase, five jets",
     "Kyiv said it damaged 3 MiG-31 and 2 Su-34 jets at Savasleyka. Russia "
     "hit two grain ships near Odesa.",
     icon_jet),
    ((120, 74, 160), "ASIA - INDONESIA",
     "Rescue race for 13 trapped miners",
     "Rescuers searched a flooded illegal gold mine in West Java; 13 others "
     "already confirmed dead.",
     icon_mine),
    ((16, 130, 170), "SPACE - CHINA / PAKISTAN",
     "First Pakistani astronaut at Tiangong",
     "Muhammad Zeeshan Ali arrived on Shenzhou-24, first foreign astronaut "
     "aboard China's station.",
     icon_rocket),
]

FOOTER = ("ALSO TODAY: EU leaders clash in Brussels over a Ukraine loan | "
          "North Korea's Kim urges wider tactical-nuke deployment | "
          "AI sell-off sinks the Nasdaq | Spain faces a snap election")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.text((W // 2, 34), "THE WORLD IN ONE IMAGE",
              font=font(SERIF_BOLD, 44), fill=INK, anchor="ma")
    draw.line([36, 96, W - 36, 96], fill=RULE, width=5)
    draw.line([36, 106, W - 36, 106], fill=RULE, width=2)
    draw.text((W // 2, 118), "THURSDAY  26 NOVEMBER 2026",
              font=font(SANS_BOLD, 63), fill=RED, anchor="ma")
    draw.text((W // 2, 192),
              "The day's biggest stories, from every region, on one page",
              font=font(SANS, 28), fill=MUTED, anchor="ma")

    # Panels: 2 columns x 3 rows
    gx, gy = 36, 236
    pw, ph = 468, 218
    gap = 12
    for i, (color, kicker, headline, body, icon) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        draw_panel(draw, [x0, y0, x0 + pw, y0 + ph],
                   color, kicker, headline, body, icon)

    # Footer strip
    fy = gy + 3 * ph + 2 * gap + 12
    draw.rectangle([36, fy, W - 36, H - 28], fill=INK)
    lines = wrap(draw, FOOTER, font(SANS_BOLD, 21), W - 72 - 40)
    ty = fy + 12
    for line in lines:
        draw.text((W // 2, ty), line, font=font(SANS_BOLD, 21),
                  fill=(245, 240, 225), anchor="ma")
        ty += 27

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
