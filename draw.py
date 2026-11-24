#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: 1024x1024, heroes-scene angle."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14  # margin
BG = (250, 246, 236)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
GOLD = (176, 124, 0)
GREY = (90, 90, 90)
LIGHT = (238, 232, 220)
AMBER = (214, 130, 0)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def chip(d, x, y, label, fill):
    f = font(F_SANSB, 9)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # top red rule
    d.rectangle([0, 0, W, 5], fill=RED)
    d.rectangle([0, 5, W, 6], fill=(60, 60, 60))

    # ---- masthead ----
    y = 12
    d.text((M, y), "THE WORLD TODAY", font=font(F_SERIF, 54), fill=INK)
    d.text((W - M, y + 4), "31 STORIES", font=font(F_SANSB, 17), fill=INK, anchor="ra")
    d.text((W - M, y + 26), "6 REGIONS", font=font(F_SANSB, 17), fill=INK, anchor="ra")
    y = 72
    d.text((M, y), "MONDAY 23 NOVEMBER 2026", font=font(F_SANSB, 21), fill=RED)
    d.text((W - M, y + 3), "AI ROUT  ·  AI RULES  ·  POWER SHIFT",
           font=font(F_SANSB, 11), fill=GREY, anchor="ra")
    y = 100
    d.line([(M, y), (W - M, y)], fill=INK, width=2)

    # ---- number strip ----
    nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES"),
            ("10T WON", "SEOUL FUND"), ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
    y = 106
    cw = (W - 2 * M) / len(nums)
    for i, (n, lab) in enumerate(nums):
        x = M + i * cw
        d.text((x + cw / 2, y), n, font=font(F_SANSB, 23), fill=RED, anchor="ma")
        d.text((x + cw / 2, y + 28), lab, font=font(F_SANSB, 10), fill=INK, anchor="ma")
        if i:
            d.line([(x, y + 2), (x, y + 40)], fill=(200, 190, 175), width=1)
    y = 150
    d.line([(M, y), (W - M, y)], fill=INK, width=1)

    # ---- region bar ----
    regions = [("NORTH AMERICA", 8, (31, 90, 180)), ("EUROPE", 6, (196, 90, 30)),
               ("MIDDLE EAST", 6, (122, 60, 160)), ("ASIA-PACIFIC", 6, (0, 130, 130)),
               ("AFRICA", 3, (160, 90, 0)), ("WORLD", 2, (90, 90, 90))]
    y = 155
    bh = 20
    x = M
    total = sum(r[1] for r in regions)
    for name, n, col in regions:
        w = (W - 2 * M) * n / total
        d.rectangle([x, y, x + w - 2, y + bh], fill=col)
        d.text((x + w / 2, y + 4), f"{name} {n}", font=font(F_SANSB, 10),
               fill=(255, 255, 255), anchor="ma")
        x += w

    # ---- UTC strip ----
    y = 180
    d.rectangle([M, y, W - M, y + 20], fill=NAVY)
    d.text((M + 6, y + 4), "THE DAY IN UTC", font=font(F_SANSB, 10), fill=(255, 210, 90))
    utc = "~00:00 ASIA OPENS  ·  06:30 KOSPI -3.3%  ·  ~09:00 SEOUL FUND  ·  14:30 WALL ST +3%  ·  ~16:00 GUTERRES  ·  ~21:00 FBI HACK  (~ = APPROX.)"
    d.text((M + 118, y + 5), utc, font=font(F_SANS, 9), fill=(255, 255, 255))

    # ---- hero scenes ----
    hy = 206
    hw = 326
    gap = 6
    heroes = [
        dict(num="#1", kick="ASIA · MARKETS", scene="kospi",
             title="AI ROUT HITS ASIA",
             body="Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%. AI sell-off spreads from Wall Street.",
             src="Yonhap · Korea JoongAng", chip="REPORTED", cfill=(0, 130, 60)),
        dict(num="#2", kick="WORLD · UNITED NATIONS", scene="guterres",
             title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
             src="UN News · Reuters", chip="REPORTED", cfill=(0, 130, 60)),
        dict(num="#3", kick="ASIA-PACIFIC · POWER", scene="power",
             title="US LEAD OVER CHINA AT RECORD LOW",
             body="Gap 5.3, narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
             src="Lowy Institute", chip="REPORTED", cfill=(0, 130, 60)),
    ]
    for i, h in enumerate(heroes):
        x = M + i * (hw + gap)
        # scene box
        d.rectangle([x, hy, x + hw, hy + 148], fill=(18, 30, 58))
        if h["scene"] == "kospi":
            # skyline
            for bx, bw_, bh_ in [(8, 34, 46), (48, 26, 70), (80, 30, 52), (116, 24, 78),
                                 (146, 32, 58), (184, 26, 84), (216, 30, 62), (252, 28, 74),
                                 (286, 30, 50)]:
                d.rectangle([x + bx, hy + 148 - bh_, x + bx + bw_, hy + 148], fill=(40, 52, 84))
                for wy in range(hy + 148 - bh_ + 8, hy + 140, 14):
                    for wx in range(x + bx + 5, x + bx + bw_ - 4, 10):
                        d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 205, 80))
            # falling chart
            pts = [(x + 12, hy + 28), (x + 70, hy + 36), (x + 130, hy + 34),
                   (x + 190, hy + 58), (x + 250, hy + 82), (x + 312, hy + 112)]
            d.line(pts, fill=(255, 80, 80), width=3)
            for px, py in pts:
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
            d.text((x + hw - 10, hy + 8), "-3.3%", font=font(F_SANSB, 30), fill=(255, 90, 90), anchor="ra")
            d.text((x + 10, hy + 8), "intraday -5.8%", font=font(F_SANSB, 11), fill=(255, 255, 255))
        elif h["scene"] == "guterres":
            # globe
            cx, cy, r = x + 62, hy + 74, 52
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 160, 210))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
            d.arc([cx - r + 14, cy - r, cx + r - 14, cy + r], 90, 270, fill=(255, 255, 255), width=1)
            d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
            # network nodes
            nodes = [(x + 150, hy + 30), (x + 205, hy + 22), (x + 260, hy + 44),
                     (x + 175, hy + 78), (x + 235, hy + 92), (x + 285, hy + 110),
                     (x + 160, hy + 122)]
            for a in range(len(nodes)):
                for b in range(a + 1, len(nodes)):
                    d.line([nodes[a], nodes[b]], fill=(120, 180, 230), width=1)
            for nx, ny in nodes:
                d.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(255, 205, 80))
            # podium silhouette
            d.ellipse([x + 288, hy + 96, x + 306, hy + 114], fill=(20, 20, 20))
            d.polygon([(x + 276, hy + 148), (x + 318, hy + 148), (x + 310, hy + 114),
                       (x + 284, hy + 114)], fill=(20, 20, 20))
            d.rectangle([x + 8, hy + 8, x + 118, hy + 26], fill=(255, 205, 80))
            d.text((x + 12, hy + 10), "150 DELEGATES", font=font(F_SANSB, 10), fill=(20, 20, 20))
            d.text((x + 8, hy + 128), "UN", font=font(F_SANSB, 12), fill=(255, 255, 255))
        else:
            # power bars
            d.rectangle([x, hy, x + hw, hy + 148], fill=(245, 240, 228))
            d.text((x + 10, hy + 8), "ASIA POWER INDEX 2026", font=font(F_SANSB, 11), fill=INK)
            d.text((x + 10, hy + 34), "US", font=font(F_SANSB, 13), fill=INK)
            d.rectangle([x + 62, hy + 32, x + 62 + 190, hy + 54], fill=(31, 90, 180))
            d.text((x + 258, hy + 34), "78.9", font=font(F_SANSB, 13), fill=INK)
            d.text((x + 10, hy + 64), "CHINA", font=font(F_SANSB, 13), fill=INK)
            d.rectangle([x + 62, hy + 62, x + 62 + 176, hy + 84], fill=(196, 40, 40))
            d.text((x + 244, hy + 64), "73.6", font=font(F_SANSB, 13), fill=INK)
            d.text((x + 10, hy + 94), "INDIA 3rd", font=font(F_SANSB, 11), fill=GREY)
            d.rectangle([x + 84, hy + 94, x + 84 + 96, hy + 112], fill=(140, 140, 140))
            d.text((x + 186, hy + 94), "40.5", font=font(F_SANSB, 11), fill=GREY)
            d.text((x + 10, hy + 122), "GAP 5.3", font=font(F_SANSB, 16), fill=RED)
            d.text((x + 96, hy + 126), "narrowest since 2018", font=font(F_SANS, 10), fill=INK)
        # hero text below scene
        ty = hy + 154
        d.text((x, ty), f"{h['num']} {h['kick']}", font=font(F_SANSB, 9), fill=RED)
        ty += 14
        tl = wrap(d, h["title"], font(F_SANSB, 16), hw)
        ty = draw_lines(d, tl[:2], x, ty, font(F_SANSB, 16), INK, 19)
        bl = wrap(d, h["body"], font(F_SANS, 10), hw)
        ty = draw_lines(d, bl[:3], x, ty + 2, font(F_SANS, 10), INK, 13)
        d.text((x, ty + 2), f"Source: {h['src']}", font=font(F_SANS, 8), fill=GREY)
        chip(d, x + hw - 62, ty + 1, h["chip"], h["cfill"])

    # ---- 10 small cards ----
    cards = [
        ("#4", "SPORT · US", "Skubal signs $450M Mets deal",
         "Two-time Cy Young winner, nine years — the largest ever for a pitcher.",
         "ESPN", "REPORTED", (0, 130, 60), (16, 42, 90)),
        ("#5", "TECH · US", "Anthropic IPO: $107.3B, largest ever",
         "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
         "Bloomberg", "REPORTED", (0, 130, 60), (0, 110, 110)),
        ("#6", "EUROPE · WAR", "Poland: 3 Russian missiles crossed airspace",
         "Kyiv says three Kh-101s entered Poland on Friday; Tusk: provocation.",
         "AP", "CLAIM", AMBER, (196, 40, 40)),
        ("#7", "EUROPE · SECURITY", "Intel warns of Russian nuclear satellite",
         "Moscow built a satellite to carry a nuclear warhead; launch possible next month.",
         "Bloomberg", "CLAIM", AMBER, (60, 60, 120)),
        ("#8", "EUROPE · ECONOMY", "Paris: 100+ back 2% billionaire tax",
         "Economists, politicians and unions rally behind France's 2% minimum wealth tax.",
         "AFP", "REPORTED", (0, 130, 60), (0, 130, 60)),
        ("#9", "EUROPE · UK", "Manchester: 12,000 cleared after scare",
         "Substance scare empties arena district; no casualties reported.",
         "AP", "REPORTED", (0, 130, 60), (122, 60, 160)),
        ("#10", "EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week",
         "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
         "Kyiv", "CLAIM", AMBER, (196, 40, 40)),
        ("#11", "WORLD · CLIMATE", "COP31: the day after",
         "Sunday's collapse — 194 nations reject the Antalya pact — draws fury; Guterres \"profoundly frustrated\".",
         "CNN", "REPORTED", (0, 130, 60), (0, 110, 110)),
        ("#12", "AFRICA · LIBYA", "Benghazi: UN demands probe of port attacks",
         "Drones hit two Russian ships; UN calls for an investigation.",
         "UN News", "CLAIM", AMBER, (160, 90, 0)),
        ("#13", "MIDDLE EAST · ISRAEL", "Israel unity talks resume",
         "Likud and Gantz's Yashar return to the table after Sunday's stall.",
         "Reuters", "ONGOING", (31, 90, 180), (31, 90, 180)),
    ]
    cy0 = 452
    chh, cwid = 106, 196
    for i, (num, kick, title, body, src, chip_lab, cfill, band) in enumerate(cards):
        row, col = divmod(i, 5)
        x = M + col * (cwid + 5)
        y = cy0 + row * (chh + 6)
        d.rectangle([x, y, x + cwid, y + chh], outline=(180, 170, 155), width=1, fill=(255, 255, 255))
        # illustration strip
        d.rectangle([x + 1, y + 1, x + cwid - 1, y + 24], fill=band)
        d.text((x + 6, y + 6), num, font=font(F_SANSB, 11), fill=(255, 255, 255))
        d.text((x + cwid - 6, y + 7), kick, font=font(F_SANSB, 8), fill=(255, 255, 255), anchor="ra")
        ty = y + 28
        tl = wrap(d, title, font(F_SANSB, 11), cwid - 10)
        ty = draw_lines(d, tl[:2], x + 5, ty, font(F_SANSB, 11), INK, 13)
        bl = wrap(d, body, font(F_SANS, 9), cwid - 10)
        ty = draw_lines(d, bl[:2], x + 5, ty + 2, font(F_SANS, 9), INK, 11)
        d.text((x + 5, y + chh - 14), src, font=font(F_SANS, 8), fill=GREY)
        chip(d, x + cwid - 58, y + chh - 15, chip_lab, cfill)

    # ---- map + ALSO ----
    my = 684
    d.text((M, my), "THE WORLD — WHERE IT HAPPENED", font=font(F_SANSB, 12), fill=RED)
    d.text((M + 520, my), "ALSO ON MONDAY — 18 MORE STORIES",
           font=font(F_SANSB, 12), fill=RED)
    map_x, map_y, map_w, map_h = M, my + 18, 496, 176
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(205, 225, 240),
                outline=(150, 160, 175), width=1)
    # grid
    for gx in range(map_x, map_x + map_w + 1, 41):
        d.line([(gx, map_y), (gx, map_y + map_h)], fill=(185, 205, 225), width=1)
    for gy in range(map_y, map_y + map_h + 1, 35):
        d.line([(map_x, gy), (map_x + map_w, gy)], fill=(185, 205, 225), width=1)

    continents = {
        "NA": [(-168, 66), (-158, 58), (-140, 60), (-130, 54), (-124, 42), (-120, 34),
               (-110, 24), (-100, 18), (-90, 14), (-83, 9), (-79, 9), (-84, 13),
               (-88, 18), (-91, 19), (-97, 16), (-97, 26), (-90, 30), (-81, 26),
               (-76, 35), (-70, 42), (-65, 44), (-60, 47), (-55, 52), (-60, 55),
               (-65, 60), (-72, 62), (-80, 63), (-90, 66), (-100, 68), (-120, 70),
               (-140, 70), (-158, 71), (-165, 68), (-168, 66)],
        "SA": [(-80, 9), (-77, 4), (-80, -3), (-77, -12), (-70, -23), (-72, -37),
               (-74, -50), (-66, -55), (-62, -45), (-52, -32), (-41, -23),
               (-35, -9), (-40, -3), (-50, 0), (-55, 6), (-62, 9), (-70, 11),
               (-77, 8), (-80, 9)],
        "AF": [(-17, 15), (-15, 27), (-5, 35), (10, 37), (20, 32), (32, 31),
               (35, 24), (39, 15), (43, 11), (51, 10), (48, 2), (40, -6),
               (36, -18), (32, -29), (20, -35), (15, -27), (12, -15), (9, -1),
               (9, 4), (-8, 5), (-15, 11), (-17, 15)],
        "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
               (12, 56), (18, 56), (24, 58), (21, 60), (12, 61), (5, 60),
               (10, 64), (18, 69), (28, 71), (32, 68), (28, 64), (24, 62),
               (22, 58), (28, 55), (24, 52), (19, 48), (14, 45), (8, 44),
               (3, 43), (-2, 37), (-9, 37), (-10, 36)],
        "AS": [(30, 36), (28, 41), (33, 46), (38, 50), (42, 55), (48, 60),
               (55, 65), (65, 69), (75, 73), (90, 75), (110, 76), (130, 72),
               (150, 70), (170, 67), (178, 65), (162, 58), (156, 50), (142, 42),
               (135, 35), (127, 34), (120, 32), (112, 22), (105, 10), (100, 7),
               (95, 15), (90, 22), (86, 20), (80, 13), (75, 12), (70, 20),
               (62, 25), (56, 27), (50, 29), (48, 33), (42, 37), (36, 36), (30, 36)],
        "AU": [(113, -22), (114, -30), (118, -35), (129, -32), (135, -35),
               (140, -38), (150, -37), (153, -27), (150, -22), (142, -11),
               (136, -12), (130, -13), (122, -17), (113, -22)],
        "GL": [(-45, 60), (-40, 65), (-32, 68), (-25, 70), (-20, 74), (-25, 78),
               (-35, 80), (-50, 78), (-58, 72), (-52, 64), (-45, 60)],
        "UK": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50), (-5, 50)],
        "JP": [(130, 31), (132, 33), (135, 34), (139, 35), (141, 41), (145, 44),
               (141, 38), (138, 34), (133, 34), (130, 31)],
    }
    lat_top, lat_bot = 83, -55

    def proj(lon, lat):
        px = map_x + (lon + 180) / 360 * map_w
        py = map_y + (lat_top - lat) / (lat_top - lat_bot) * map_h
        return (px, py)

    for poly in continents.values():
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(235, 220, 190),
                  outline=(180, 165, 140))

    # pins: (num, lon, lat, claim?)
    pins = [
        (1, 127.0, 37.5, False), (2, -59.6, 13.1, False), (3, -150.0, -25.0, False),
        (4, -74.0, 40.7, False), (5, -122.4, 37.8, False), (6, 21.0, 52.2, True),
        (7, 37.6, 55.7, True), (8, 2.35, 48.85, False), (9, -2.24, 53.48, False),
        (10, 30.5, 50.45, True), (11, 30.7, 36.9, False), (12, 20.1, 32.1, True),
        (13, 34.8, 32.1, False), (14, 34.45, 31.5, False), (15, 35.6, 31.9, False),
        (16, 51.4, 35.7, False), (17, 35.5, 33.9, False), (18, 50.6, 26.2, False),
        (19, 32.5, 15.6, False), (20, 29.0, 1.5, False), (21, 90.4, 23.8, False),
        (22, 129.5, 36.0, False), (23, 124.5, 39.0, False), (24, 116.4, 39.9, False),
        (25, 128.0, 39.5, False), (26, -77.0, 38.9, False), (27, -74.5, 40.5, False),
        (28, -79.5, 37.0, False), (29, -71.5, 42.5, False), (30, -105.0, 39.7, False),
        (31, -122.0, 45.0, False),
    ]
    for num, lon, lat, claim in pins:
        px, py = proj(lon, lat)
        col = AMBER if claim else RED
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(num), font=font(F_SANSB, 7), fill=(255, 255, 255), anchor="ma")
    d.text((map_x + 4, map_y + map_h - 12), "N ↑", font=font(F_SANSB, 9), fill=INK)
    d.text((map_x + map_w - 4, map_y + 4), "PIN = STORY NUMBER",
           font=font(F_SANSB, 8), fill=(70, 90, 110), anchor="ra")

    # ALSO list (right column, 2 sub-columns)
    also = [
        ("MIDDLE EAST", [("14", "Gaza: two killed in Israeli strike"),
                         ("15", "West Bank: settler attacks hit villages"),
                         ("16", "Iran war: no deal in sight"),
                         ("17", "Lebanon seizes 264 kg of explosives"),
                         ("18", "Bahrain: Iran strike hits plant, 2 hurt")]),
        ("AFRICA", [("19", "Sudan drones downed over Khartoum"),
                    ("20", "DRC: fighting traps Ebola teams")]),
        ("ASIA-PACIFIC", [("21", "Bangladesh: Hasina jailed if she returns"),
                          ("22", "Seoul minister quits over AI exam chaos"),
                          ("23", "SK Telecom -7.3% as Anthropic hype cools"),
                          ("24", "China eases margin rules to calm rout"),
                          ("25", "Seoul readies 10T-won stabilisation fund")]),
        ("NORTH AMERICA", [("26", "Bessent demands Nvidia answers"),
                           ("27", "FBI probes hack of police database"),
                           ("28", "Trump: Iran strikes may resume in New Year"),
                           ("29", "US futures jump 3% holiday week"),
                           ("30", "Tom Jackson dies at 75"),
                           ("31", "States sue SpaceX over AI safety claims")]),
    ]
    ax = M + 520
    ay = my + 18
    col_w = 235
    for ci, (region, items) in enumerate(also):
        x = ax + (ci % 2) * col_w
        y = ay + (ci // 2) * 92
        d.text((x, y), region, font=font(F_SANSB, 9), fill=RED)
        yy = y + 12
        for num, txt in items:
            d.text((x, yy), num, font=font(F_SANSB, 9), fill=RED)
            lines = wrap(d, txt, font(F_SANS, 9), col_w - 22)
            draw_lines(d, lines[:1], x + 20, yy, font(F_SANS, 9), INK, 11)
            yy += 13

    # ---- DATE CHECK ----
    dy = 884
    d.rectangle([M, dy, W - M, dy + 78], outline=RED, width=2, fill=(255, 240, 240))
    d.text((M + 8, dy + 6), "DATE CHECK", font=font(F_SANSB, 12), fill=RED)
    d.text((M + 96, dy + 7), "Every story above happened or was first reported on Monday 23 November 2026.",
           font=font(F_SANSB, 10), fill=INK)
    d.text((W - M - 8, dy + 7), "WIRES READ UP TO 23:00 UTC", font=font(F_SANSB, 9),
           fill=RED, anchor="ra")
    d.text((M + 8, dy + 28),
           "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
           font=font(F_SANS, 9), fill=INK)
    d.text((M + 8, dy + 41),
           "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).",
           font=font(F_SANS, 9), fill=INK)
    d.text((M + 8, dy + 58),
           "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
           font=font(F_SANS, 9), fill=INK)

    # ---- footer ----
    fy = 972
    d.text((M, fy), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
           font=font(F_SANS, 9), fill=GREY)
    d.text((M, fy + 13),
           "CONFIRMED = 2+ outlets · REPORTED = carried by the wires today · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified)",
           font=font(F_SANS, 9), fill=GREY)
    d.text((W - M, fy + 28), "Scenes are drawn illustrations, not photographs.",
           font=font(F_SANS, 9), fill=GREY, anchor="ra")
    d.text((M, fy + 28), "THE WORLD TODAY · 23 NOV 2026", font=font(F_SANSB, 9), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
