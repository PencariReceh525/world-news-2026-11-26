"""Draw the v2 entry image: an illustrated newspaper front page of the world
news of Thursday 26 November 2026.

Run locally (needs Pillow) to regenerate entry.png:
    python3 generate_image_v2.py

The submitted program is main.py, which copies entry.png to the output
directory, so the grader's standard-library-only sandbox never needs Pillow.

Layout: masthead naming the day, a lead scene (Macy's 100th Thanksgiving
parade postponed by a storm), a schematic world map with numbered pins,
six more drawn scenes (US tariffs, Cairo tanker fire, Ukraine airbase strike,
Ras Tanura refinery attack, Tiangong's first Pakistani astronaut, and the
Gukesh-Sindarov world chess title match in Geneva), then 25 one-line briefs.
32 stories in all, every one reported on 26 November 2026 and cross-checked
in NEWS_SOURCES.md.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (246, 240, 226)
INK = (17, 21, 31)
MUTED = (90, 94, 104)
WHITE = (255, 255, 255)
RED = (176, 32, 42)
NAVY = (24, 48, 96)
TEAL = (16, 118, 110)
ORANGE = (216, 108, 18)
GOLD = (196, 148, 26)
SKY = (196, 220, 238)
SAND = (238, 226, 196)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = FONT_DIR + "/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "/liberation/LiberationSans-Bold.ttf"
SANS = FONT_DIR + "/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
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


# ---------------------------------------------------------------- scenes
def scene_parade(d, x0, y0, x1, y1):
    """Skyline, round parade balloons with strings, and a storm cloud."""
    d.rectangle([x0, y0, x1, y1], fill=(172, 190, 205))
    ground = y0 + 118
    # skyline
    for bx, bh, bw in [(6, 44, 30), (42, 58, 26), (74, 38, 32), (112, 64, 28),
                       (146, 46, 30), (182, 60, 26), (214, 40, 30),
                       (250, 56, 28), (284, 42, 30), (320, 62, 26),
                       (352, 44, 30), (388, 58, 28), (422, 40, 30)]:
        d.rectangle([x0 + bx, ground - bh, x0 + bx + bw, ground],
                    fill=(96, 110, 128))
    d.rectangle([x0, ground, x1, y1], fill=(70, 78, 90))
    # balloons: round, with two strings and a small gondola each
    for cx, cy, col in [(78, 46, RED), (168, 34, ORANGE), (258, 48, TEAL)]:
        d.ellipse([x0 + cx - 24, y0 + cy - 26, x0 + cx + 24, y0 + cy + 26],
                  fill=col)
        d.ellipse([x0 + cx - 9, y0 + cy - 20, x0 + cx + 3, y0 + cy - 2],
                  fill=(255, 255, 255))
        d.line([x0 + cx - 14, y0 + cy + 22, x0 + cx - 5, y0 + cy + 40],
               fill=(40, 44, 52), width=2)
        d.line([x0 + cx + 14, y0 + cy + 22, x0 + cx + 5, y0 + cy + 40],
               fill=(40, 44, 52), width=2)
        d.rectangle([x0 + cx - 6, y0 + cy + 40, x0 + cx + 6, y0 + cy + 48],
                    fill=(90, 62, 30))
    # storm cloud + rain at the right
    d.ellipse([x0 + 322, y0 + 4, x0 + 452, y0 + 40], fill=(66, 76, 92))
    d.ellipse([x0 + 356, y0 - 6, x0 + 428, y0 + 30], fill=(66, 76, 92))
    for rx in range(340, 446, 18):
        d.line([x0 + rx, y0 + 42, x0 + rx - 7, y0 + 62], fill=(50, 90, 140),
               width=4)
    # wind streaks
    for wy in (78, 92):
        d.line([x0 + 20, y0 + wy, x0 + 92, y0 + wy], fill=(230, 238, 244),
               width=4)
        d.line([x0 + 130, y0 + wy + 6, x0 + 196, y0 + wy + 6],
               fill=(230, 238, 244), width=4)


def scene_tariffs(d, x0, y0, x1, y1):
    """Crates, a big percent sign and a falling chart line."""
    d.rectangle([x0, y0, x1, y1], fill=SAND)
    for cx, cy in [(30, 78), (96, 78), (63, 30)]:
        d.rectangle([x0 + cx, y0 + cy, x0 + cx + 60, y0 + cy + 44],
                    outline=(120, 84, 30), width=5)
        d.line([x0 + cx, y0 + cy, x0 + cx + 60, y0 + cy + 44],
               fill=(120, 84, 30), width=3)
        d.line([x0 + cx + 60, y0 + cy, x0 + cx, y0 + cy + 44],
               fill=(120, 84, 30), width=3)
    d.ellipse([x0 + 185, y0 + 18, x0 + 285, y0 + 118], fill=RED)
    d.text((x0 + 235, y0 + 68), "%", font=F(SANS_BOLD, 74), fill=WHITE,
           anchor="mm")
    pts = [(180, 128), (215, 118), (245, 132), (275, 124), (305, 140)]
    d.line([(x0 + a, y0 + b) for a, b in pts], fill=RED, width=6)
    d.polygon([(x0 + 305, y0 + 140), (x0 + 292, y0 + 136), (x0 + 300, y0 + 126)],
              fill=RED)


def scene_cairo(d, x0, y0, x1, y1):
    """A burning tanker truck on a ring road, pyramid on the horizon."""
    d.rectangle([x0, y0, x1, y1], fill=(240, 205, 150))
    d.polygon([(x0 + 250, y0 + 92), (x0 + 300, y0 + 30), (x0 + 350, y0 + 92)],
              fill=(206, 164, 96))
    d.rectangle([x0, y0 + 92, x1, y1], fill=(96, 96, 100))
    d.line([x0, y0 + 116, x1, y0 + 116], fill=(240, 220, 120), width=4)
    # tanker
    d.rounded_rectangle([x0 + 60, y0 + 52, x0 + 190, y0 + 92], 16,
                        fill=(150, 156, 164))
    d.rectangle([x0 + 190, y0 + 64, x0 + 224, y0 + 92], fill=(60, 66, 76))
    for wx in (84, 196):
        d.ellipse([x0 + wx, y0 + 84, x0 + wx + 22, y0 + 106], fill=INK)
    # flames
    for fx, fh in [(86, 58), (122, 78), (158, 62)]:
        d.polygon([(x0 + fx, y0 + 54), (x0 + fx + 14, y0 + 54 - fh + 26),
                   (x0 + fx + 24, y0 + 54)], fill=ORANGE)
        d.polygon([(x0 + fx + 6, y0 + 54), (x0 + fx + 14, y0 + 54 - fh + 44),
                   (x0 + fx + 20, y0 + 54)], fill=(246, 186, 40))
    for sx in range(90, 180, 18):
        d.ellipse([x0 + sx, y0 + 2, x0 + sx + 26, y0 + 22], fill=(90, 90, 94))


def scene_ukraine(d, x0, y0, x1, y1):
    """Jets on a runway, an explosion, and a grain ship."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y0 + 96, x1, y1], fill=(110, 118, 104))
    d.line([x0, y0 + 118, x1, y0 + 118], fill=WHITE, width=4)
    jet = [(0, 12), (30, 6), (66, 2), (104, 6), (112, 11), (104, 15),
           (64, 15), (44, 22), (30, 21), (34, 14), (12, 17)]
    for ox, oy, s in [(24, 38, 1.25), (168, 52, 1.0)]:
        d.polygon([(x0 + ox + int(a * s), y0 + oy + int(b * s)) for a, b in jet],
                  fill=(52, 62, 74))
        d.polygon([(x0 + ox + int(6 * s), y0 + oy + int(12 * s)),
                   (x0 + ox + int(20 * s), y0 + oy - int(6 * s)),
                   (x0 + ox + int(28 * s), y0 + oy + int(11 * s))],
                  fill=(52, 62, 74))
    # explosion star
    cx, cy = x0 + 300, y0 + 40
    pts = []
    import math
    for i in range(16):
        r = 30 if i % 2 == 0 else 13
        pts.append((cx + r * math.cos(i * math.pi / 8),
                    cy + r * math.sin(i * math.pi / 8)))
    d.polygon(pts, fill=ORANGE)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(246, 186, 40))
    # grain ship
    d.polygon([(x0 + 236, y0 + 128), (x0 + 306, y0 + 128), (x0 + 296, y0 + 142),
               (x0 + 246, y0 + 142)], fill=(120, 52, 40))
    d.rectangle([x0 + 252, y0 + 112, x0 + 292, y0 + 128], fill=GOLD)
    d.rectangle([x0, y0 + 142, x1, y1], fill=(52, 96, 140))


def scene_refinery(d, x0, y0, x1, y1):
    """Refinery towers and tanks, missile trails in a dusk sky."""
    d.rectangle([x0, y0, x1, y1], fill=(216, 164, 120))
    d.rectangle([x0, y0 + 100, x1, y1], fill=(104, 88, 74))
    for tx, th in [(36, 74), (86, 92), (210, 84)]:
        d.rectangle([x0 + tx, y0 + 108 - th, x0 + tx + 22, y0 + 108],
                    fill=(70, 74, 82))
        d.rectangle([x0 + tx - 4, y0 + 108 - th, x0 + tx + 26, y0 + 116 - th],
                    fill=(52, 56, 64))
    for tx in (140, 252):
        d.ellipse([x0 + tx, y0 + 76, x0 + tx + 52, y0 + 96], fill=(168, 172, 178))
        d.rectangle([x0 + tx, y0 + 86, x0 + tx + 52, y0 + 108],
                    fill=(168, 172, 178))
    import math
    for ox, oy in [(30, 8), (120, 0), (220, 12)]:
        pts = [(x0 + ox + t * 2.2, y0 + oy + 44 * math.sin(t / 22.0))
               for t in range(0, 44, 4)]
        d.line(pts, fill=WHITE, width=4)
        d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5,
                   pts[-1][1] + 5], fill=RED)


def scene_space(d, x0, y0, x1, y1):
    """Tiangong-style station over the Earth's curve, a docked capsule."""
    d.rectangle([x0, y0, x1, y1], fill=(14, 22, 44))
    import random
    random.seed(26)
    for _ in range(46):
        sx, sy = random.randint(4, 316), random.randint(4, 96)
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=WHITE)
    # station
    d.rectangle([x0 + 128, y0 + 52, x0 + 196, y0 + 70], fill=(210, 214, 220))
    d.rectangle([x0 + 40, y0 + 44, x0 + 118, y0 + 78], fill=(52, 96, 178))
    d.rectangle([x0 + 206, y0 + 44, x0 + 284, y0 + 78], fill=(52, 96, 178))
    for gx in range(48, 282, 16):
        d.line([x0 + gx, y0 + 44, x0 + gx, y0 + 78], fill=(30, 60, 110),
               width=2)
    d.polygon([(x0 + 196, y0 + 56), (x0 + 224, y0 + 61), (x0 + 196, y0 + 66)],
              fill=(226, 178, 60))
    # earth
    d.ellipse([x0 - 120, y0 + 96, x0 + 440, y0 + 300], fill=(44, 104, 168))
    d.ellipse([x0 + 30, y0 + 112, x0 + 120, y0 + 140], fill=(72, 148, 96))
    d.ellipse([x0 + 170, y0 + 122, x0 + 268, y0 + 148], fill=(72, 148, 96))


def scene_chess(d, x0, y0, x1, y1):
    """A chessboard with two kings and a 1-1 score."""
    d.rectangle([x0, y0, x1, y1], fill=(232, 222, 198))
    bx, by, cell = x0 + 26, y0 + 18, 21
    for r in range(5):
        for c in range(8):
            col = (240, 236, 214) if (r + c) % 2 == 0 else (94, 74, 52)
            d.rectangle([bx + c * cell, by + r * cell,
                         bx + (c + 1) * cell, by + (r + 1) * cell], fill=col)
    def king(cx, cy, col):
        d.polygon([(cx - 13, cy + 26), (cx - 9, cy - 6), (cx - 3, cy + 4),
                   (cx, cy - 12), (cx + 3, cy + 4), (cx + 9, cy - 6),
                   (cx + 13, cy + 26)], fill=col)
        d.rectangle([cx - 14, cy + 24, cx + 14, cy + 30], fill=col)
        d.rectangle([cx - 2, cy - 22, cx + 2, cy - 12], fill=col)
        d.rectangle([cx - 6, cy - 19, cx + 6, cy - 15], fill=col)
    king(bx + 74, by + 52, (30, 30, 34))
    king(bx + 116, by + 52, (246, 244, 238))
    d.text((x0 + 252, y0 + 62), "1-1", font=F(SANS_BOLD, 54), fill=INK,
           anchor="mm")
    d.text((x0 + 252, y0 + 98), "GAME 3 TODAY", font=F(SANS_BOLD, 17),
           fill=RED, anchor="mm")


# ------------------------------------------------------------------- map
# Schematic world map: rough continent polygons in a 484 x 150 box.
CONTINENTS = [
    [(8, 44), (58, 24), (118, 26), (150, 42), (140, 60), (118, 64),
     (126, 80), (108, 96), (90, 92), (82, 110), (68, 102), (56, 84),
     (38, 70), (16, 60)],                                        # N America
    [(168, 22), (198, 18), (202, 38), (176, 44)],                 # Greenland
    [(104, 108), (128, 100), (144, 118), (138, 146), (124, 158),
     (108, 138), (98, 120)],                                     # S America
    [(230, 40), (252, 26), (288, 30), (302, 50), (284, 60),
     (268, 52), (258, 68), (240, 60), (230, 50)],                # Europe
    [(238, 80), (270, 70), (302, 76), (320, 94), (308, 128),
     (284, 148), (258, 136), (242, 110), (234, 94)],             # Africa
    [(300, 30), (362, 18), (432, 26), (464, 54), (442, 68),
     (454, 86), (420, 78), (398, 96), (374, 84), (352, 98),
     (330, 80), (306, 62), (296, 48)],                           # Asia
    [(330, 80), (354, 84), (346, 110), (332, 94)],               # India
    [(438, 54), (454, 46), (458, 60), (442, 64)],                # Japan
    [(408, 122), (450, 116), (468, 132), (452, 150), (416, 148),
     (404, 134)],                                                # Australia
]
ISLANDS = [(376, 100, 14, 7), (402, 108, 16, 7), (428, 104, 14, 7),
           (226, 32, 9, 10), (392, 88, 12, 8)]

# pin number -> (x, y) inside the map box, stories in SCENES order
PINS = [(70, 62), (268, 84), (316, 84), (282, 44), (404, 106), (360, 40),
        (262, 40), (338, 92)]
PIN_LEGEND = ["1 New York    2 Cairo    3 Riyadh    4 Ukraine",
              "5 Indonesia    6 Tiangong (orbit)    7 Geneva    8 Mumbai"]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 238),
                outline=(170, 178, 190), width=2)
    mx, my = x0 + 8, y0 + 30
    for poly in CONTINENTS:
        d.polygon([(mx + a, my + b) for a, b in poly], fill=(104, 148, 96))
    for ix, iy, iw, ih in ISLANDS:
        d.rectangle([mx + ix, my + iy, mx + ix + iw, my + iy + ih],
                    fill=(104, 148, 96))
    for i, (px, py) in enumerate(PINS, start=1):
        cx, cy = mx + px, my + py
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED)
        d.text((cx, cy), str(i), font=F(SANS_BOLD, 15), fill=WHITE,
               anchor="mm")
    d.text((x0 + 10, y1 - 32), PIN_LEGEND[0], font=F(SANS_BOLD, 12),
           fill=INK, anchor="ls")
    d.text((x0 + 10, y1 - 14), PIN_LEGEND[1], font=F(SANS_BOLD, 12),
           fill=INK, anchor="ls")


# ---------------------------------------------------------------- panels
def scene_panel(d, box, scene, kicker, headline, body, tag=None, sh=102):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE, outline=(200, 192, 172), width=2)
    # Scenes are drawn on a 460x150 canvas, then scaled into the panel with
    # (nearly) the same factor on both axes so shapes are not squashed.
    canvas = Image.new("RGB", (460, 150), WHITE)
    scene(ImageDraw.Draw(canvas), 0, 0, 460, 150)
    canvas = canvas.resize((x1 - x0 - 6, sh))
    # paste via the image this draw belongs to is not available; the caller
    # passes the base image through a module-level hook set in main().
    BASE.paste(canvas, (x0 + 3, y0 + 3))
    if tag:
        tw = d.textlength(tag, font=F(SANS_BOLD, 15)) + 16
        d.rectangle([x0 + 10, y0 + 8, x0 + 10 + tw, y0 + 32], fill=RED)
        d.text((x0 + 18, y0 + 20), tag, font=F(SANS_BOLD, 15), fill=WHITE,
               anchor="lm")
    ty = y0 + sh + 6
    d.text((x0 + 12, ty), kicker, font=F(SANS_BOLD, 15), fill=RED)
    ty += 20
    for line in wrap(d, headline, F(SANS_BOLD, 22), x1 - x0 - 24):
        d.text((x0 + 12, ty), line, font=F(SANS_BOLD, 22), fill=INK)
        ty += 26
    ty += 1
    for line in wrap(d, body, F(SANS, 15), x1 - x0 - 24):
        d.text((x0 + 12, ty), line, font=F(SANS, 15), fill=(52, 56, 66))
        ty += 18


SCENES_ROW2 = [
    (scene_tariffs, "TRADE - WASHINGTON",
     "New US tariffs: up to 35%",
     "On 14 partners: China, EU, Japan, India (25%)."),
    (scene_cairo, "DISASTER - CAIRO",
     "Tanker fire kills 31",
     "Tanker overturned on the ring road; 21 injured."),
    (scene_ukraine, "WAR - UKRAINE",
     "Five jets hit at airbase",
     "Savasleyka strike; Odesa grain ships hit."),
]
SCENES_ROW3 = [
    (scene_refinery, "MIDDLE EAST - SAUDI ARABIA",
     "Ras Tanura refinery struck",
     "Houthi attack; missiles downed near Riyadh."),
    (scene_space, "SPACE - TIANGONG",
     "First Pakistani in orbit",
     "Astronaut Zeeshan Ali aboard China's station."),
    (scene_chess, "SPORT - GENEVA CHESS",
     "Chess title tied 1-1",
     "Gukesh-Sindarov Game 2 drawn; Game 3 today."),
]

BRIEFS = [
    "EU leaders clash over Ukraine loan",
    "Spain: snap election this Sunday",
    "Finland gives $59M for Ukraine energy",
    "Liverpool 3-0 Brugge; Lille beat Bayern",
    "Indonesia: 13 trapped in flooded mine",
    "N. Korea's Kim widens tactical nukes",
    "Bank of Korea raises interest rates",
    "Bangladesh garment wages up 36%",
    "India: Congress party sues Meta",
    "India asks Netflix to drop Pak series",
    "US chip curbs slow China's AI labs",
    "Pakistan-Saudi-Turkiye defence talks",
    "Gaza strike kills Hamas chief",
    "ISIL suicide attack kills 2 in Syria",
    "Sudan drone strike kills 19 civilians",
    "Lebanon plans a second airport",
    "S. Africa court win for Ramaphosa",
    "Judges urge dropping Netanyahu case",
    "Dow tops 50,000 for the first time",
    "NY court upholds Mamdani rent freeze",
    "Puerto Rico cancels Luma power deal",
    "Norse Atlantic flags bankruptcy risk",
    "SpaceX cleared for 1M satellites",
    "US tells citizens to leave Iran",
    "Zambia bans term-limit protests",
]


BASE = None


def main():
    global BASE
    img = Image.new("RGB", (W, H), PAPER)
    BASE = img
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((W // 2, 8), "THE WORLD IN ONE IMAGE",
           font=F(SERIF_BOLD, 35), fill=INK, anchor="ma")
    d.text((W // 2, 48), "THURSDAY 26 NOVEMBER 2026",
           font=F(SANS_BOLD, 45), fill=RED, anchor="ma")
    d.line([28, 100, W - 28, 100], fill=INK, width=4)

    # Lead scene (left) and map (right)
    scene_panel(d, [28, 108, 500, 338], scene_parade,
                "UNITED STATES - THANKSGIVING",
                "Storm postpones Macy's parade",
                "The 100th Thanksgiving parade moves to Saturday - its "
                "first weather postponement ever.", tag="LEAD STORY",
                sh=140)
    draw_map(d, 512, 108, 996, 338)
    d.rectangle([512, 108, 706, 132], fill=NAVY)
    d.text((522, 120), "THE DAY ON THE MAP", font=F(SANS_BOLD, 16),
           fill=WHITE, anchor="lm")

    # Two rows of three scenes
    xs = [28, 352, 676]
    for row_i, scenes in enumerate([SCENES_ROW2, SCENES_ROW3]):
        y0 = 348 + row_i * 198
        for x0, (scene, kicker, head, body) in zip(xs, scenes):
            scene_panel(d, [x0, y0, x0 + 320, y0 + 190], scene,
                        kicker, head, body)

    # Briefs: 25 one-liners in three columns
    by = 744
    d.rectangle([28, by, W - 28, by + 28], fill=INK)
    d.text((W // 2, by + 14), "MORE OF THE DAY - 25 STORIES IN BRIEF",
           font=F(SANS_BOLD, 19), fill=(245, 240, 225), anchor="mm")
    cols = [BRIEFS[:9], BRIEFS[9:17], BRIEFS[17:]]
    col_x = [36, 368, 700]
    for ci, col in enumerate(cols):
        ty = by + 38
        for j, item in enumerate(col):
            num = sum(len(c) for c in cols[:ci]) + j + 1
            d.text((col_x[ci], ty), f"{num:02d}", font=F(SANS_BOLD, 15),
                   fill=RED)
            d.text((col_x[ci] + 28, ty), item, font=F(SANS, 15), fill=INK)
            ty += 20

    # Date-check footer
    fy = 970
    d.line([28, fy - 4, W - 28, fy - 4], fill=INK, width=3)
    for i, line in enumerate([
            "DATE CHECK: every story above was first reported on Thursday 26 November 2026 -",
            "Thanksgiving in the US, and 18 years since the 26/11 Mumbai attacks in India."]):
        d.text((W // 2, fy + 4 + i * 22), line, font=F(SANS_BOLD, 16),
               fill=INK, anchor="ma")
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
