"""Doodle-Zeichenbibliothek: handgezeichnet wirkende Strichmännchen, Objekte und Texte.

Alle Koordinaten in den Element-Specs sind normiert (0..1) relativ zur Bildgröße.
Jede Linie "zittert" leicht (Boil-Effekt), damit es wie von Hand gezeichnet wirkt.
"""
import math
import os
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_HAND = os.path.join(HERE, "fonts", "PatrickHand-Regular.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "Anton-Regular.ttf")

PALETTES = {
    "paper": {"bg": (246, 241, 231), "ink": (27, 27, 27), "soft": (120, 112, 100)},
    "night": {"bg": (28, 34, 52), "ink": (240, 236, 226), "soft": (150, 160, 185)},
    "red": {"bg": (120, 22, 22), "ink": (250, 240, 230), "soft": (230, 160, 150)},
}

COLORS = {
    "gold": (238, 186, 40), "red": (205, 45, 40), "blue": (45, 90, 190),
    "green": (70, 150, 70), "brown": (160, 110, 60), "potato": (196, 150, 90),
    "skin": (255, 255, 255), "white": (255, 255, 255), "black": (20, 20, 20),
    "grey": (150, 150, 150), "yellow": (255, 212, 0), "sick": (170, 210, 120),
    "stone": (175, 175, 170), "dirt": (125, 90, 55), "night": (28, 34, 52),
}


def col(c, default=None):
    if c is None:
        return default
    if isinstance(c, (list, tuple)):
        return tuple(c)
    if isinstance(c, str) and c.startswith("#"):
        c = c.lstrip("#")
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return COLORS.get(c, default)


@lru_cache(maxsize=256)
def font(path, size):
    return ImageFont.truetype(path, max(8, int(size)))


class Pen:
    """Zeichnet wackelige Linien. rng bestimmt das Zittern (pro Boil-Schritt neu)."""

    def __init__(self, draw, rng, scale, ink, amp=2.2):
        self.d = draw
        self.rng = rng
        self.s = scale
        self.ink = ink
        self.amp = amp * scale

    def j(self, a=None):
        a = self.amp if a is None else a
        return self.rng.uniform(-a, a)

    def line(self, pts, width=7, color=None, closed=False, amp=None):
        color = color or self.ink
        w = max(1, int(width * self.s))
        if closed:
            pts = list(pts) + [pts[0]]
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / (38 * self.s)))
            for i in range(n):
                t = i / n
                out.append((x0 + (x1 - x0) * t + self.j(amp), y0 + (y1 - y0) * t + self.j(amp)))
        out.append((pts[-1][0] + self.j(amp), pts[-1][1] + self.j(amp)))
        if len(out) >= 2:
            self.d.line(out, fill=color, width=w, joint="curve")
            r = w / 2
            for (x, y) in (out[0], out[-1]):
                self.d.ellipse((x - r, y - r, x + r, y + r), fill=color)

    def ellipse(self, cx, cy, rx, ry, width=7, color=None, fill=None, seg=28, amp=None):
        pts = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            k = 1 + self.j(0.025) if amp is None else 1 + self.j(amp)
            pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
        if fill is not None:
            self.d.polygon(pts, fill=fill)
        if width:
            self.line(pts, width=width, color=color, closed=True)

    def poly(self, pts, width=7, color=None, fill=None):
        jp = [(x + self.j(), y + self.j()) for x, y in pts]
        if fill is not None:
            self.d.polygon(jp, fill=fill)
        if width:
            self.line(jp, width=width, color=color, closed=True)


def wrap(text, fnt, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, cx, cy, text, fnt, fill, max_w, stroke=0, stroke_fill=None, line_gap=1.08, anchor_top=False):
    lines = wrap(text, fnt, max_w, draw)
    asc, desc = fnt.getmetrics()
    lh = (asc + desc) * line_gap
    total = lh * len(lines)
    y = cy if anchor_top else cy - total / 2
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text((cx - w / 2, y), ln, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        y += lh
    return total


# ---------------------------------------------------------------- Elemente

def draw_figure(pen, el, W, H, k, t, pal):
    """Strichmännchen. el: x, y (Fußpunkt), size, pose, mood, props, face(left/right), label, bubble, color."""
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    bob = math.sin(t * 3.2 + el.get("x", 0) * 9) * 3 * pen.s if el.get("idle", True) else 0
    fx, fy = el.get("x", 0.5) * W, el.get("y", 0.75) * H + bob
    face = -1 if el.get("face") == "left" else 1
    ink = col(el.get("color"), pal["ink"])
    lw = 8
    hr = 62 * s                       # Kopfradius
    leg, body, arm = 150 * s, 170 * s, 120 * s
    hip = (fx, fy - leg)
    neck = (fx, hip[1] - body)
    head = (fx, neck[1] - hr * 0.95)
    pose = el.get("pose", "normal")

    # Beine
    if pose == "run":
        sw = math.sin(t * 14) * 40 * s
        pen.line([hip, (fx - 45 * s + sw, fy)], lw, ink)
        pen.line([hip, (fx + 45 * s - sw, fy)], lw, ink)
    else:
        pen.line([hip, (fx - 48 * s, fy)], lw, ink)
        pen.line([hip, (fx + 48 * s, fy)], lw, ink)
    # Körper
    pen.line([neck, hip], lw, ink)
    # Arme
    sh = (fx, neck[1] + 22 * s)
    hands = []
    if pose == "up":
        hands = [(fx - 95 * s, sh[1] - 110 * s), (fx + 95 * s, sh[1] - 110 * s)]
    elif pose == "point":
        hands = [(fx - face * 60 * s, sh[1] + 100 * s), (fx + face * 135 * s, sh[1] - 25 * s)]
    elif pose == "shrug":
        hands = [(fx - 105 * s, sh[1] - 45 * s), (fx + 105 * s, sh[1] - 45 * s)]
        pen.line([sh, (fx - 70 * s, sh[1] + 25 * s), hands[0]], lw, ink)
        pen.line([sh, (fx + 70 * s, sh[1] + 25 * s), hands[1]], lw, ink)
        hands = []
    elif pose == "hold":
        hands = [(fx + face * 95 * s, sh[1] + 40 * s), (fx + face * 105 * s, sh[1] + 20 * s)]
    elif pose == "hips":
        pen.line([sh, (fx - 70 * s, sh[1] + 55 * s), (fx - 8 * s, hip[1] - 10 * s)], lw, ink)
        pen.line([sh, (fx + 70 * s, sh[1] + 55 * s), (fx + 8 * s, hip[1] - 10 * s)], lw, ink)
    elif pose == "think":
        hands = [(fx - face * 60 * s, sh[1] + 100 * s)]
        pen.line([sh, (fx + face * 70 * s, sh[1] + 45 * s), (fx + face * 28 * s, head[1] + hr * 0.75)], lw, ink)
    elif pose == "run":
        sw = math.sin(t * 14) * 50 * s
        hands = [(fx - 80 * s + sw, sh[1] + 70 * s), (fx + 80 * s - sw, sh[1] + 70 * s)]
    else:
        hands = [(fx - 70 * s, sh[1] + arm * 0.9), (fx + 70 * s, sh[1] + arm * 0.9)]
    for hnd in hands:
        pen.line([sh, hnd], lw, ink)

    # Kopf
    mood = el.get("mood", "neutral")
    skin = col("sick") if mood == "sick" else col(el.get("skin"), (255, 255, 255))
    pen.ellipse(head[0], head[1], hr, hr, lw, ink, fill=skin)
    ex = head[0] + face * 14 * s
    ey = head[1] - 8 * s
    er = 6.5 * s
    if mood in ("sleep", "dead"):
        if mood == "dead":
            for dx in (-20, 20):
                cx = ex + dx * s
                pen.line([(cx - 8 * s, ey - 8 * s), (cx + 8 * s, ey + 8 * s)], 5, ink)
                pen.line([(cx - 8 * s, ey + 8 * s), (cx + 8 * s, ey - 8 * s)], 5, ink)
        else:
            for dx in (-20, 20):
                pen.line([(ex + dx * s - 9 * s, ey), (ex + dx * s + 9 * s, ey)], 5, ink)
    else:
        for dx in (-20, 20):
            pen.d.ellipse((ex + dx * s - er, ey - er, ex + dx * s + er, ey + er), fill=ink)
    my = head[1] + 26 * s
    if mood in ("happy", "smug"):
        pen.line([(ex - 22 * s, my - 4 * s), (ex, my + 10 * s), (ex + 22 * s, my - 4 * s)], 5, ink)
        if mood == "smug":
            pen.line([(ex + 10 * s, ey - 22 * s), (ex + 30 * s, ey - 28 * s)], 5, ink)
    elif mood in ("sad", "sick"):
        pen.line([(ex - 20 * s, my + 8 * s), (ex, my - 4 * s), (ex + 20 * s, my + 8 * s)], 5, ink)
    elif mood == "angry":
        pen.line([(ex - 20 * s, my + 4 * s), (ex + 20 * s, my + 4 * s)], 5, ink)
        pen.line([(ex - 32 * s, ey - 24 * s), (ex - 10 * s, ey - 14 * s)], 5, ink)
        pen.line([(ex + 32 * s, ey - 24 * s), (ex + 10 * s, ey - 14 * s)], 5, ink)
    elif mood == "surprised":
        pen.ellipse(ex, my + 4 * s, 10 * s, 13 * s, 5, ink)
    elif mood == "sleep":
        f = font(FONT_HAND, 54 * s)
        z = int(t * 2) % 3 + 1
        pen.d.text((head[0] + hr * 0.9, head[1] - hr * 1.6), "Z" * z, font=f, fill=ink)
    elif mood != "dead":
        pen.line([(ex - 15 * s, my + 2 * s), (ex + 15 * s, my + 2 * s)], 5, ink)

    # Requisiten
    props = el.get("props", [])
    top = head[1] - hr
    for p in props:
        if p == "crown":
            g = col("gold")
            w2 = 48 * s
            pts = [(head[0] - w2, top + 6 * s), (head[0] - w2, top - 40 * s), (head[0] - w2 / 2, top - 15 * s),
                   (head[0], top - 48 * s), (head[0] + w2 / 2, top - 15 * s), (head[0] + w2, top - 40 * s),
                   (head[0] + w2, top + 6 * s)]
            pen.poly(pts, 5, ink, fill=g)
        elif p == "tricorn":
            pts = [(head[0] - 80 * s, top + 14 * s), (head[0], top - 48 * s), (head[0] + 80 * s, top + 14 * s),
                   (head[0], top + 2 * s)]
            pen.poly(pts, 5, ink, fill=col("black"))
        elif p == "farmer":
            pen.ellipse(head[0], top + 8 * s, 95 * s, 16 * s, 5, ink, fill=(222, 190, 110))
            pen.poly([(head[0] - 45 * s, top + 6 * s), (head[0] - 35 * s, top - 32 * s),
                      (head[0] + 35 * s, top - 32 * s), (head[0] + 45 * s, top + 6 * s)], 5, ink, fill=(222, 190, 110))
        elif p == "helmet":
            pen.d.pieslice((head[0] - hr * 1.05, top - 10 * s, head[0] + hr * 1.05, top + hr * 1.3), 180, 360,
                           fill=(110, 110, 110))
            pen.line([(head[0], top - 10 * s), (head[0], top - 46 * s)], 7, ink)
        elif p == "spear":
            hx = fx + face * 105 * s
            pen.line([(hx, fy + 5 * s), (hx, neck[1] - 170 * s)], 6, col("brown"))
            pen.poly([(hx - 14 * s, neck[1] - 165 * s), (hx, neck[1] - 215 * s), (hx + 14 * s, neck[1] - 165 * s)],
                     4, ink, fill=(190, 190, 190))
            pen.line([sh, (hx, sh[1] + 30 * s)], lw, ink)
        elif p == "wig":
            for dx in (-1, 1):
                pen.ellipse(head[0] + dx * hr * 0.95, head[1] + 10 * s, 20 * s, 34 * s, 4, ink, fill=(235, 235, 235))
        elif p == "potato":
            hnd = hands[-1] if hands else (fx + face * 90 * s, sh[1] + 60 * s)
            draw_potato(pen, {"x": hnd[0] / W, "y": hnd[1] / H, "size": 0.55 * el.get("size", 1.0)}, W, H, k, t, pal)
        elif p == "sword":
            hnd = hands[-1] if hands else (fx + face * 90 * s, sh[1] + 60 * s)
            pen.line([hnd, (hnd[0] + face * 30 * s, hnd[1] - 150 * s)], 7, (170, 170, 175))
            pen.line([(hnd[0] - 25 * s, hnd[1] - 12 * s), (hnd[0] + 25 * s, hnd[1] - 12 * s)], 7, ink)

    if el.get("label"):
        f = font(FONT_HAND, 58 * pen.s * el.get("size", 1.0) * min(1, k))
        text_block(pen.d, fx, fy + 18 * pen.s, el["label"], f, ink, 420 * pen.s, anchor_top=True)
    if el.get("bubble"):
        draw_bubble(pen, el["bubble"], head[0] + face * 40 * s, top - 30 * s, s, ink, face)


def draw_bubble(pen, text, x, y, s, ink, face=1):
    f = font(FONT_HAND, 50 * pen.s)
    max_w = 440 * pen.s
    lines = wrap(text, f, max_w, pen.d)
    asc, desc = f.getmetrics()
    lh = (asc + desc) * 1.02
    bw = max(pen.d.textlength(l, font=f) for l in lines) + 60 * pen.s
    bh = lh * len(lines) + 40 * pen.s
    bx = x + face * 30 * pen.s - (0 if face > 0 else bw)
    by = y - bh - 40 * pen.s
    bx = max(20 * pen.s, min(bx, pen.img.size[0] - bw - 20 * pen.s))
    by = max(20 * pen.s, by)
    pen.poly([(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh)], 5, ink, fill=(255, 255, 255))
    tx = min(max(x, bx + 30 * pen.s), bx + bw - 30 * pen.s)
    pen.poly([(tx - 18 * pen.s, by + bh - 3), (tx + 18 * pen.s, by + bh - 3), (x, y)], 5, ink, fill=(255, 255, 255))
    ty = by + 20 * pen.s
    for ln in lines:
        w = pen.d.textlength(ln, font=f)
        pen.d.text((bx + bw / 2 - w / 2, ty), ln, font=f, fill=(20, 20, 20))
        ty += lh


def draw_potato(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.5) * H
    if el.get("glow"):
        r = 150 * s * (1 + 0.06 * math.sin(t * 5))
        pen.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 236, 150))
    pen.ellipse(cx, cy, 90 * s, 62 * s, 6, pal["ink"], fill=col("potato"), amp=0.06)
    rnd = random.Random(int(el.get("x", 0) * 1000 + el.get("y", 0) * 7))
    for _ in range(5):
        ex = cx + rnd.uniform(-55, 55) * s
        ey = cy + rnd.uniform(-30, 30) * s
        pen.d.ellipse((ex - 5 * s, ey - 4 * s, ex + 5 * s, ey + 4 * s), fill=(120, 85, 45))
    if el.get("face"):
        draw_face(pen, cx, cy - 5 * s, s, el.get("face"), pal)


def draw_face(pen, cx, cy, s, mood, pal):
    ink = (40, 30, 20)
    for dx in (-22, 22):
        pen.d.ellipse((cx + dx * s - 7 * s, cy - 14 * s, cx + dx * s + 7 * s, cy), fill=ink)
    if mood == "happy":
        pen.line([(cx - 20 * s, cy + 14 * s), (cx, cy + 26 * s), (cx + 20 * s, cy + 14 * s)], 5, ink)
    else:
        pen.line([(cx - 20 * s, cy + 26 * s), (cx, cy + 14 * s), (cx + 20 * s, cy + 26 * s)], 5, ink)


def draw_field(pen, el, W, H, k, t, pal):
    s = pen.s * k
    if s <= 0.01:
        return
    x0, x1 = el.get("x0", 0.08) * W, el.get("x1", 0.92) * W
    y = el.get("y", 0.8) * H
    rows = el.get("rows", 3)
    for r in range(rows):
        yy = y + r * 70 * pen.s
        pen.line([(x0 + r * 20 * pen.s, yy), (x1 - r * 20 * pen.s, yy)], 6, col("dirt"))
        n = int((x1 - x0) / (95 * pen.s))
        for i in range(n):
            px = x0 + 40 * pen.s + i * 95 * pen.s + r * 20 * pen.s
            if px > x1 - 30 * pen.s:
                break
            h = 34 * s
            pen.line([(px, yy - 4), (px, yy - h)], 5, col("green"))
            pen.line([(px, yy - h * 0.7), (px - 16 * s, yy - h * 1.1)], 5, col("green"))
            pen.line([(px, yy - h * 0.7), (px + 16 * s, yy - h * 1.1)], 5, col("green"))
    if el.get("fence"):
        for i in range(int((x1 - x0) / (60 * pen.s)) + 1):
            px = x0 + i * 60 * pen.s
            pen.line([(px, y - 120 * pen.s), (px, y - 40 * pen.s)], 5, col("brown"))
        pen.line([(x0, y - 100 * pen.s), (x1, y - 100 * pen.s)], 5, col("brown"))


def draw_text(pen, el, W, H, k, t, pal):
    if k <= 0.01:
        return
    size = el.get("size", 90) * pen.s * k
    f = font(FONT_BOLD if el.get("bold") else FONT_HAND, size)
    color = col(el.get("color"), pal["ink"])
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.3) * H
    max_w = el.get("width", 0.86) * W
    box = el.get("box")
    if box:
        lines = wrap(el["text"], f, max_w - 60 * pen.s, pen.d)
        asc, desc = f.getmetrics()
        lh = (asc + desc) * 1.08
        bw = max(pen.d.textlength(l, font=f) for l in lines) + 70 * pen.s
        bh = lh * len(lines) + 50 * pen.s
        fill = col(box, (255, 255, 255)) if box is not True else (255, 255, 255)
        pen.poly([(cx - bw / 2, cy - bh / 2), (cx + bw / 2, cy - bh / 2), (cx + bw / 2, cy + bh / 2),
                  (cx - bw / 2, cy + bh / 2)], 6, pal["ink"], fill=fill)
        if el.get("color") is None:
            color = (20, 20, 20)
    stroke = int(el.get("stroke", 0) * pen.s)
    total = text_block(pen.d, cx, cy, el["text"], f, color, max_w, stroke=stroke, stroke_fill=(20, 20, 20))
    if el.get("underline"):
        uy = cy + total / 2 + 8 * pen.s
        uw = min(max_w, pen.d.textlength(el["text"], font=f)) / 2
        pen.line([(cx - uw, uy), (cx + uw, uy)], 7, col(el.get("underline"), col("red")))


def draw_grave(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, by = el.get("x", 0.5) * W, el.get("y", 0.8) * H
    w, h = 170 * s, 300 * s
    pts = [(cx - w, by)] + [(cx - w * math.cos(a), by - h + w - w * math.sin(a))
                            for a in [i * math.pi / 12 for i in range(13)]] + [(cx + w, by)]
    pen.poly(pts, 7, pal["ink"], fill=col("stone"))
    f = font(FONT_HAND, 48 * s)
    text_block(pen.d, cx, by - h * 0.45, el.get("text", "R.I.P."), f, (40, 40, 40), w * 1.7)
    pen.line([(cx - w * 1.6, by), (cx + w * 1.6, by)], 7, col("dirt"))


def draw_celestial(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, cy = el.get("x", 0.8) * W, el.get("y", 0.12) * H
    if el["type"] == "sun":
        pen.ellipse(cx, cy, 70 * s, 70 * s, 6, pal["ink"], fill=col("yellow"))
        for i in range(10):
            a = i * math.pi / 5 + t * 0.4
            pen.line([(cx + math.cos(a) * 95 * s, cy + math.sin(a) * 95 * s),
                      (cx + math.cos(a) * 130 * s, cy + math.sin(a) * 130 * s)], 6, pal["ink"])
    else:
        pen.ellipse(cx, cy, 70 * s, 70 * s, 0, fill=(245, 235, 180))
        pen.d.ellipse((cx - 30 * s, cy - 85 * s, cx + 110 * s, cy + 55 * s), fill=pal["bg"])
        rnd = random.Random(3)
        for _ in range(14):
            sx, sy = rnd.uniform(0.05, 0.95) * W, rnd.uniform(0.03, 0.4) * H
            r = rnd.uniform(3, 7) * pen.s * (0.7 + 0.3 * math.sin(t * 3 + sx))
            pen.d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(245, 240, 210))


def draw_house(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, by = el.get("x", 0.5) * W, el.get("y", 0.8) * H
    w, h = 150 * s, 170 * s
    pen.poly([(cx - w, by), (cx - w, by - h), (cx + w, by - h), (cx + w, by)], 6, pal["ink"], fill=(225, 200, 160))
    pen.poly([(cx - w - 25 * s, by - h), (cx, by - h - 130 * s), (cx + w + 25 * s, by - h)], 6, pal["ink"],
             fill=col(el.get("roof"), (175, 70, 50)))
    pen.poly([(cx - 30 * s, by), (cx - 30 * s, by - 90 * s), (cx + 30 * s, by - 90 * s), (cx + 30 * s, by)], 5,
             pal["ink"], fill=(120, 80, 50))


def draw_arrow(pen, el, W, H, k, t, pal):
    if k <= 0.01:
        return
    x0, y0 = el["from"][0] * W, el["from"][1] * H
    x1, y1 = el["to"][0] * W, el["to"][1] * H
    x1 = x0 + (x1 - x0) * min(1, k)
    y1 = y0 + (y1 - y0) * min(1, k)
    c = col(el.get("color"), col("red"))
    pen.line([(x0, y0), (x1, y1)], 9, c)
    a = math.atan2(y1 - y0, x1 - x0)
    L = 45 * pen.s
    for da in (2.6, -2.6):
        pen.line([(x1, y1), (x1 + math.cos(a + da) * L, y1 + math.sin(a + da) * L)], 9, c)


def draw_mark(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.5) * H
    r = 120 * s
    if el["type"] == "cross":
        c = col(el.get("color"), col("red"))
        pen.line([(cx - r, cy - r), (cx + r, cy + r)], 16, c)
        pen.line([(cx - r, cy + r), (cx + r, cy - r)], 16, c)
    elif el["type"] == "check":
        c = col(el.get("color"), col("green"))
        pen.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.8)], 16, c)
    else:  # question / exclaim
        f = font(FONT_BOLD, 260 * s)
        ch = "?" if el["type"] == "question" else "!"
        w = pen.d.textlength(ch, font=f)
        pen.d.text((cx - w / 2, cy - 170 * s), ch, font=f, fill=col(el.get("color"), col("red")),
                   stroke_width=int(6 * pen.s), stroke_fill=pal["ink"])


def draw_flag(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.01:
        return
    cx, by = el.get("x", 0.5) * W, el.get("y", 0.6) * H
    pen.line([(cx, by), (cx, by - 380 * s)], 8, col("brown"))
    stripes = [col(c) for c in el.get("colors", ["black", "white"])]
    fw, fh = 260 * s, 170 * s
    top = by - 380 * s
    vertical = el.get("vertical", False)
    n = len(stripes)
    for i, c in enumerate(stripes):
        wave = lambda xx: math.sin(xx / (60 * s) + t * 4) * 8 * s
        if vertical:
            xa, xb = cx + fw * i / n, cx + fw * (i + 1) / n
            pts = [(xa, top + wave(xa - cx)), (xb, top + wave(xb - cx)), (xb, top + fh + wave(xb - cx)),
                   (xa, top + fh + wave(xa - cx))]
        else:
            ya, yb = top + fh * i / n, top + fh * (i + 1) / n
            pts = [(cx, ya), (cx + fw, ya + wave(fw)), (cx + fw, yb + wave(fw)), (cx, yb)]
        pen.d.polygon(pts, fill=c)
    pen.line([(cx, top), (cx + fw, top + math.sin(fw / (60 * s) + t * 4) * 8 * s),
              (cx + fw, top + fh + math.sin(fw / (60 * s) + t * 4) * 8 * s), (cx, top + fh)], 5, pal["ink"])


def draw_image(pen, el, W, H, k, t, pal, base_dir="."):
    if k <= 0.01:
        return
    path = el["path"] if os.path.isabs(el["path"]) else os.path.join(base_dir, el["path"])
    img = _load_img(path)
    tw = int(el.get("width", 0.8) * W * k)
    th = int(img.height * tw / img.width)
    im = img.resize((tw, th))
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.4) * H
    b = int(18 * pen.s)
    pen.d.rectangle((cx - tw / 2 - b, cy - th / 2 - b, cx + tw / 2 + b, cy + th / 2 + b * 3), fill=(255, 255, 255))
    pen.img.paste(im, (int(cx - tw / 2), int(cy - th / 2)))
    if el.get("caption"):
        f = font(FONT_HAND, 40 * pen.s)
        text_block(pen.d, cx, cy + th / 2 + b * 0.6, el["caption"], f, (40, 40, 40), tw, anchor_top=True)


@lru_cache(maxsize=32)
def _load_img(path):
    return Image.open(path).convert("RGB")


DRAWERS = {
    "figure": draw_figure, "potato": draw_potato, "field": draw_field, "text": draw_text,
    "grave": draw_grave, "sun": draw_celestial, "moon": draw_celestial, "house": draw_house,
    "arrow": draw_arrow, "cross": draw_mark, "check": draw_mark, "question": draw_mark,
    "exclaim": draw_mark, "flag": draw_flag, "image": draw_image,
}
