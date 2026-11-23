#!/usr/bin/env python3
"""Build the front-page image for the make.fun news-image-20261122 entry.

Draws a dense, legible newspaper front page (1024x1024, cream paper,
black ink) summarising 22 November 2026 world news. Deterministic:
no timestamps, no randomness, fixed layout. Stdlib + PIL only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 content width

PAPER = (247, 242, 231)
INK = (17, 17, 17)
GREY = (90, 85, 75)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
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


def draw_centered(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, x0=None, x1=None, width=1):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_section_head(draw, x, y, text, fnt, width):
    draw.text((x, y), text, font=fnt, fill=INK)
    rule(draw, y + fnt.size + 4, x0=x, x1=x + width, width=1)
    return y + fnt.size + 9


def draw_item(draw, x, y, max_w, time, text, body_fnt, time_fnt, line_h=20):
    """One dated item: bold time, then wrapped text. Returns new y."""
    prefix = time + "  "
    pw = draw.textlength(prefix, font=time_fnt)
    draw.text((x, y), prefix, font=time_fnt, fill=INK)
    # First line starts after the time prefix; subsequent lines full width.
    lines = wrap(draw, text, body_fnt, max_w - pw)
    if not lines:
        return y + line_h
    draw.text((x + pw, y), lines[0], font=body_fnt, fill=INK)
    yy = y + line_h
    for ln in lines[1:]:
        draw.text((x, yy), ln, font=body_fnt, fill=INK)
        yy += line_h
    return yy + 5


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    masthead = font(SERIF_B, 62)
    dateline = font(SANS, 19)
    lead = font(SERIF_B, 54)
    standfirst = font(SERIF, 21)
    half_head = font(SERIF_B, 29)
    half_body = font(SANS, 16)
    sect_head = font(SANS_B, 17)
    item_body = font(SANS, 15)
    item_time = font(SANS_B, 15)
    footer_f = font(SANS, 15)

    y = 30
    # Masthead
    y = draw_centered(d, y, "THE WORLD IN ONE DAY", masthead)
    y += 6
    y = draw_centered(d, y, "SUNDAY, 22 NOVEMBER 2026  ·  27 STORIES  ·  7 REGIONS", dateline)
    y += 8
    rule(d, y, width=2)
    rule(d, y + 4, width=1)
    y += 14

    # Lead story
    y = draw_centered(d, y, "COP31 COLLAPSES IN ANTALYA", lead)
    y += 6
    y = draw_centered(d, y, "No deal as EU rejects final text that omits", standfirst)
    y = draw_centered(d, y, "fossil fuels after two weeks of talks.", standfirst)
    y += 10
    rule(d, y, width=1)
    y += 12

    # Second row: two half-width headlines
    half_w = (CW - 20) // 2
    row_top = y
    x2 = MARGIN + half_w + 20
    half_items = [
        (MARGIN, half_w, "TWO TANKERS HIT MINES OFF HORMUZ",
         "Supertankers caught fire east of the strait; Iran navy blames US escorts."),
        (x2, half_w, "DEMOCRATS WIN BIGGEST HOUSE MAJORITY SINCE 1992",
         "North Carolina recount seals divided government."),
    ]
    row_bottom = row_top
    for x, w, head, body in half_items:
        yy = row_top
        for ln in wrap(d, head, half_head, w):
            d.text((x, yy), ln, font=half_head, fill=INK)
            yy += 34
        yy += 2
        for ln in wrap(d, body, half_body, w):
            d.text((x, yy), ln, font=half_body, fill=INK)
            yy += 20
        row_bottom = max(row_bottom, yy)
    # vertical divider between the two halves
    d.line([(MARGIN + half_w + 10, row_top), (MARGIN + half_w + 10, row_bottom)],
           fill=INK, width=1)
    y = row_bottom + 10
    rule(d, y, width=1)
    y += 12

    # Section columns (3 across)
    col_w = (CW - 40) // 3
    col_x = [MARGIN, MARGIN + col_w + 20, MARGIN + 2 * (col_w + 20)]
    col_y = [y, y, y]

    sections = [
        (0, "MIDDLE EAST", [
            ("15:36", "Sea drone hits Russian corvette Merkury at Benghazi naval base."),
            ("15:03", "Drones kill 4 near Khartoum, damage UN building."),
            ("14:20", "Iran unveils dual-missile launcher, new underground missile city."),
            ("13:16", "Saudi intercepts Houthi drone and missile; Rabigh refinery claimed hit."),
            ("09:53", "UAE condemns Iranian attack on Bahrain."),
            ("07:47", "Israeli settlers burn vehicles, paint graffiti in West Bank."),
            ("02:14", "Displaced Palestinians protest as Israeli strikes continue in Gaza."),
            ("00:04", "Gaza death toll since Oct 2025 reaches 1,661."),
        ]),
        (1, "UKRAINE WAR", [
            ("14:48", "Zelenskyy urges US to release Patriot missiles; Russia fired ~2,700 drones in a week."),
            ("06:15", "Finland: war spilling over after drone strike on Russian cargo ship in Baltic."),
        ]),
        (1, "EUROPE", [
            ("09:41", "Europe protests 3rd straight day over costs and housing."),
            ("10:25", "Former Italian police chief found dead amid Sicily bombing inquiry."),
        ]),
        (1, "ASIA-PACIFIC", [
            ("04:19", "Indonesia candy factory fire kills 3, 36 missing in Banten."),
            ("00:26", "Ex-NSW politician Fred Nile dies aged 92."),
            ("—", "ICJ rules Myanmar committed genocide against Rohingya."),
        ]),
        (2, "AMERICAS", [
            ("—", "Delta outage delays 1,600+ flights."),
            ("—", "Mexico troops capture drug lord 'El Chapo Isidro' in Sinaloa raid."),
            ("—", "Trump backs credit-card rate cap with Democrats."),
        ]),
        (2, "WORLD", [
            ("—", "Nigeria boat capsizes, 24 dead en route to a funeral."),
            ("—", "Cleverbridge breach: hackers copied card numbers and security codes."),
            ("—", "Teen gamer and his mother helped rescue missing girl after online chat."),
            ("—", "Paolo Bulgari dies at 89."),
            ("02:09", "Pezeshkian: Iran in 'silent economic war' as blockade hits 130 days."),
            ("00:44", "Hind Rajab Foundation urges Germany to arrest Israeli soldier."),
        ]),
    ]

    seen_col = set()
    for col, head, items in sections:
        x = col_x[col]
        yy = col_y[col]
        if col in seen_col:
            yy += 14  # gap between sections sharing a column
        seen_col.add(col)
        yy = draw_section_head(d, x, yy, head, sect_head, col_w)
        for t, text in items:
            yy = draw_item(d, x, yy, col_w, t, text, item_body, item_time)
            yy += 3
        col_y[col] = yy

    bottom = max(col_y)
    assert bottom < 968, f"columns overflow: bottom={bottom}"

    # Footer
    rule(d, 972, width=1)
    draw_centered(d, 982, "All stories first reported 22 November 2026 (UTC).", footer_f)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
