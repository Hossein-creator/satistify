"""Bunter Cartoon-Stil: farbige Figuren mit großen Köpfen, Hintergründe, Effekte.

Ersetzt die blassen Strichmännchen. Element-Typ "figure"/"person" zeichnet eine Cartoon-Figur,
"stick" weiterhin das alte Strichmännchen.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

import doodle
from doodle import col, font, FONT_BOLD, FONT_HAND

INK = (28, 24, 30)

ROLES = {
    "king": {"coat": (38, 66, 145), "trim": (238, 186, 40), "pants": (240, 232, 205), "hair": (205, 205, 210),
             "props": ["crown"], "cape": (190, 35, 45)},
    "soldier": {"coat": (40, 64, 135), "trim": (230, 60, 50), "pants": (238, 236, 225), "hair": (90, 60, 40),
                "props": ["tricorn", "spear"]},
    "farmer": {"coat": (150, 105, 60), "trim": (110, 75, 40), "pants": (95, 120, 65), "hair": (120, 80, 40),
               "props": ["farmer"]},
    "noble": {"coat": (140, 40, 75), "trim": (238, 186, 40), "pants": (60, 50, 70), "hair": (235, 235, 235),
              "props": ["wig"]},
    "monk": {"coat": (110, 80, 55), "trim": (70, 50, 35), "pants": (110, 80, 55), "hair": (100, 70, 45),
             "props": []},
    "woman": {"coat": (200, 70, 110), "trim": (255, 220, 120), "pants": (200, 70, 110), "hair": (150, 85, 40),
              "props": [], "dress": True},
    "child": {"coat": (240, 170, 50), "trim": (200, 120, 30), "pants": (70, 90, 160), "hair": (90, 55, 30),
              "props": [], "scale": 0.72},
    "knight": {"coat": (165, 170, 180), "trim": (200, 40, 40), "pants": (130, 135, 145), "hair": (90, 60, 40),
               "props": ["helmet", "sword"]},
    "roman": {"coat": (185, 40, 40), "trim": (238, 186, 40), "pants": (225, 190, 140), "hair": (60, 40, 30),
              "props": []},
    "citizen": {"coat": (70, 130, 120), "trim": (40, 90, 85), "pants": (80, 70, 60), "hair": (60, 40, 30),
                "props": []},
}
SKIN = (255, 214, 175)


def _limb(d, a, b, color, w, s):
    w = max(2, int(w * s))
    o = w + max(4, int(6 * s))
    d.line([a, b], fill=INK, width=o)
    for p in (a, b):
        d.ellipse((p[0] - o / 2, p[1] - o / 2, p[0] + o / 2, p[1] + o / 2), fill=INK)
    d.line([a, b], fill=color, width=w)
    for p in (a, b):
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=color)


def _blob(d, cx, cy, rx, ry, fill, s, outline=6):
    o = outline * s
    d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=INK)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill)


def _poly(d, pts, fill, s, outline=6):
    d.polygon(pts, fill=fill)
    d.line(list(pts) + [pts[0]], fill=INK, width=max(2, int(outline * s)), joint="curve")


def draw_person(pen, el, W, H, k, t, pal):
    role = ROLES.get(el.get("role", "citizen"), ROLES["citizen"])
    sz = el.get("size", 1.0) * role.get("scale", 1.0)
    s = pen.s * sz * k
    if s <= 0.02:
        return
    d = pen.d
    seed = int(el.get("x", 0.5) * 977 + el.get("y", 0.5) * 131)
    bob = math.sin(t * 3.0 + seed) * 4 * pen.s
    fx, fy = el.get("x", 0.5) * W, el.get("y", 0.62) * H
    face = -1 if el.get("face") == "left" else 1
    coat = col(el.get("coat"), role["coat"])
    trim = col(el.get("trim"), role["trim"])
    pants = col(el.get("pants"), role["pants"])
    hair = col(el.get("hair"), role["hair"])
    skin = col(el.get("skin"), SKIN)
    mood = el.get("mood", "neutral")
    if mood == "sick":
        skin = (180, 215, 140)
    pose = el.get("pose", "normal")
    props = el.get("props", role["props"])

    hr = 88 * s
    leg = 125 * s
    body = 175 * s
    hip_y = fy - leg + bob
    neck_y = hip_y - body
    head = (fx, neck_y - hr * 0.78)

    # Umhang hinten
    if role.get("cape") and "nocape" not in props:
        c = role["cape"]
        _poly(d, [(fx - 70 * s, neck_y + 10 * s), (fx + 70 * s, neck_y + 10 * s), (fx + 105 * s - face * 25 * s, hip_y + 60 * s),
                  (fx - 105 * s - face * 25 * s, hip_y + 60 * s)], c, s)

    # Beine
    if pose == "run":
        sw = math.sin(t * 13) * 45 * s
        feet = [(fx - 40 * s + sw, fy), (fx + 40 * s - sw, fy - abs(sw) * 0.3)]
    else:
        feet = [(fx - 38 * s, fy), (fx + 38 * s, fy)]
    for fpt, hx in zip(feet, (-28, 28)):
        _limb(d, (fx + hx * s, hip_y), fpt, pants, 30, s)
        _blob(d, fpt[0] + face * 14 * s, fpt[1] + 6 * s, 30 * s, 15 * s, (45, 35, 30), s, 4)

    # Körper (Mantel / Kleid)
    if role.get("dress"):
        _poly(d, [(fx - 62 * s, neck_y + 8 * s), (fx + 62 * s, neck_y + 8 * s), (fx + 120 * s, fy - 10 * s),
                  (fx - 120 * s, fy - 10 * s)], coat, s)
    else:
        _poly(d, [(fx - 72 * s, neck_y + 8 * s), (fx + 72 * s, neck_y + 8 * s), (fx + 88 * s, hip_y + 38 * s),
                  (fx - 88 * s, hip_y + 38 * s)], coat, s)
        d.line([(fx, neck_y + 14 * s), (fx, hip_y + 34 * s)], fill=trim, width=max(2, int(9 * s)))
        for i in range(3):
            by = neck_y + 45 * s + i * 45 * s
            d.ellipse((fx - 9 * s + 18 * s, by - 7 * s, fx + 9 * s + 18 * s, by + 7 * s), fill=trim)
        d.rectangle((fx - 86 * s, hip_y - 4 * s, fx + 86 * s, hip_y + 12 * s), fill=INK)

    # Arme
    sh_l, sh_r = (fx - 66 * s, neck_y + 30 * s), (fx + 66 * s, neck_y + 30 * s)
    front, back = (sh_r, sh_l) if face > 0 else (sh_l, sh_r)
    wav = math.sin(t * 7) * 18 * s
    if pose == "up":
        hands = [(sh_l[0] - 50 * s, sh_l[1] - 150 * s + wav), (sh_r[0] + 50 * s, sh_r[1] - 150 * s - wav)]
        pairs = [(sh_l, hands[0]), (sh_r, hands[1])]
    elif pose == "point":
        hands = [(back[0] - face * 10 * s, back[1] + 130 * s), (front[0] + face * 150 * s, front[1] - 40 * s)]
        pairs = [(back, hands[0]), (front, hands[1])]
    elif pose == "shrug":
        hands = [(sh_l[0] - 80 * s, sh_l[1] - 40 * s), (sh_r[0] + 80 * s, sh_r[1] - 40 * s)]
        pairs = [(sh_l, hands[0]), (sh_r, hands[1])]
    elif pose == "hold":
        hands = [(back[0] + face * 60 * s, back[1] + 85 * s), (front[0] + face * 90 * s, front[1] + 60 * s)]
        pairs = [(back, hands[0]), (front, hands[1])]
    elif pose == "think":
        hands = [(back[0], back[1] + 130 * s), (fx + face * 30 * s, head[1] + hr * 0.9)]
        pairs = [(back, hands[0]), (front, hands[1])]
    elif pose == "run":
        sw = math.sin(t * 13) * 60 * s
        hands = [(sh_l[0] - 20 * s + sw, sh_l[1] + 110 * s), (sh_r[0] + 20 * s - sw, sh_r[1] + 110 * s)]
        pairs = [(sh_l, hands[0]), (sh_r, hands[1])]
    elif pose == "hips":
        hands = [(fx - 82 * s, hip_y - 5 * s), (fx + 82 * s, hip_y - 5 * s)]
        pairs = [(sh_l, (sh_l[0] - 55 * s, sh_l[1] + 80 * s)), (sh_r, (sh_r[0] + 55 * s, sh_r[1] + 80 * s))]
        for a, b in pairs:
            _limb(d, a, b, coat, 30, s)
        pairs = [((sh_l[0] - 55 * s, sh_l[1] + 80 * s), hands[0]), ((sh_r[0] + 55 * s, sh_r[1] + 80 * s), hands[1])]
    else:
        hands = [(sh_l[0] - 22 * s, sh_l[1] + 135 * s), (sh_r[0] + 22 * s, sh_r[1] + 135 * s)]
        pairs = [(sh_l, hands[0]), (sh_r, hands[1])]
    for a, b in pairs:
        _limb(d, a, b, coat, 30, s)
    for h in hands:
        _blob(d, h[0], h[1], 17 * s, 17 * s, skin, s, 4)

    # Kopf
    _blob(d, head[0], head[1], hr, hr * 0.96, skin, s, 6)
    # Haare
    if "helmet" not in props and "bald" not in props:
        d.chord((head[0] - hr * 1.02, head[1] - hr * 1.05, head[0] + hr * 1.02, head[1] + hr * 0.6), 190, 350,
                fill=hair)
        if role.get("dress"):
            _blob(d, head[0] - face * hr * 0.85, head[1] + hr * 0.5, hr * 0.38, hr * 0.8, hair, s, 4)
    # Gesicht
    _face(d, head, hr, s, face, mood, t, seed, el)

    # Requisiten
    top = head[1] - hr
    for p in props:
        if p == "crown":
            g = (245, 195, 40)
            w2 = 62 * s
            pts = [(head[0] - w2, top + 18 * s), (head[0] - w2, top - 42 * s), (head[0] - w2 / 2, top - 12 * s),
                   (head[0], top - 55 * s), (head[0] + w2 / 2, top - 12 * s), (head[0] + w2, top - 42 * s),
                   (head[0] + w2, top + 18 * s)]
            _poly(d, pts, g, s, 5)
            for gx in (-w2 / 2, 0, w2 / 2):
                d.ellipse((head[0] + gx - 7 * s, top + 2 * s - 7 * s, head[0] + gx + 7 * s, top + 2 * s + 7 * s),
                          fill=(210, 40, 60))
        elif p == "tricorn":
            pts = [(head[0] - 112 * s, top + 22 * s), (head[0] - 30 * s, top - 40 * s), (head[0] + 30 * s, top - 40 * s),
                   (head[0] + 112 * s, top + 22 * s), (head[0], top + 6 * s)]
            _poly(d, pts, (30, 30, 38), s, 5)
            d.line([(head[0] - 100 * s, top + 18 * s), (head[0], top + 2 * s), (head[0] + 100 * s, top + 18 * s)],
                   fill=(238, 186, 40), width=max(2, int(6 * s)))
        elif p == "farmer":
            _blob(d, head[0], top + 16 * s, 130 * s, 22 * s, (230, 195, 110), s, 5)
            _poly(d, [(head[0] - 62 * s, top + 12 * s), (head[0] - 48 * s, top - 42 * s), (head[0] + 48 * s, top - 42 * s),
                      (head[0] + 62 * s, top + 12 * s)], (230, 195, 110), s, 5)
            d.rectangle((head[0] - 58 * s, top - 2 * s, head[0] + 58 * s, top + 8 * s), fill=(190, 60, 50))
        elif p == "helmet":
            d.chord((head[0] - hr * 1.08, top - 20 * s, head[0] + hr * 1.08, head[1] + hr * 0.5), 180, 360,
                    fill=(170, 175, 185), outline=INK, width=max(2, int(6 * s)))
            d.rectangle((head[0] - 8 * s, head[1] - hr * 0.3, head[0] + 8 * s, head[1] + hr * 0.15), fill=(150, 155, 165))
        elif p == "wig":
            for dx in (-1, 1):
                for i in range(3):
                    _blob(d, head[0] + dx * hr * 0.98, head[1] - 25 * s + i * 32 * s, 24 * s, 20 * s,
                          (240, 240, 240), s, 3)
        elif p == "spear":
            hx = hands[1][0] if face > 0 else hands[0][0]
            hy = hands[1][1] if face > 0 else hands[0][1]
            d.line([(hx, fy + 10 * s), (hx, neck_y - 200 * s)], fill=INK, width=max(2, int(16 * s)))
            d.line([(hx, fy + 10 * s), (hx, neck_y - 200 * s)], fill=(150, 100, 55), width=max(2, int(9 * s)))
            _poly(d, [(hx - 20 * s, neck_y - 195 * s), (hx, neck_y - 265 * s), (hx + 20 * s, neck_y - 195 * s)],
                  (200, 205, 215), s, 4)
            _blob(d, hx, hy, 17 * s, 17 * s, skin, s, 4)
        elif p == "sword":
            h = hands[1] if face > 0 else hands[0]
            tip = (h[0] + face * 50 * s, h[1] - 190 * s)
            d.line([h, tip], fill=INK, width=max(2, int(20 * s)))
            d.line([h, tip], fill=(215, 220, 230), width=max(2, int(12 * s)))
            d.line([(h[0] - 30 * s, h[1] - 10 * s), (h[0] + 30 * s, h[1] - 10 * s)], fill=(160, 120, 40),
                   width=max(2, int(12 * s)))
        elif p == "potato":
            h = hands[1] if face > 0 else hands[0]
            draw_potato(pen, {"x": h[0] / W, "y": (h[1] - 20 * s) / H, "size": 0.6 * sz}, W, H, k, t, pal)
        elif p == "scroll":
            h = hands[1] if face > 0 else hands[0]
            _poly(d, [(h[0] - 10 * s, h[1] - 90 * s), (h[0] + face * 120 * s, h[1] - 90 * s),
                      (h[0] + face * 120 * s, h[1] + 30 * s), (h[0] - 10 * s, h[1] + 30 * s)], (245, 230, 190), s, 4)
            for i in range(4):
                yy = h[1] - 65 * s + i * 22 * s
                d.line([(h[0] + face * 15 * s, yy), (h[0] + face * 100 * s, yy)], fill=(120, 100, 70),
                       width=max(1, int(4 * s)))

    if el.get("label"):
        f = font(FONT_BOLD, 50 * pen.s * sz * min(1, k))
        tw = d.textlength(el["label"], font=f)
        ly = fy + 32 * pen.s
        pad = 14 * pen.s
        d.rounded_rectangle((fx - tw / 2 - pad, ly - 4 * pen.s, fx + tw / 2 + pad, ly + f.size * 1.25),
                            radius=12 * pen.s, fill=INK)
        d.text((fx - tw / 2, ly), el["label"], font=f, fill=(255, 255, 255))
    if el.get("emote"):
        draw_emote(pen, {"kind": el["emote"], "x": (head[0] + face * hr * 1.1) / W, "y": (head[1] - hr) / H,
                         "size": sz}, W, H, 1, t, pal)
    if el.get("bubble"):
        doodle.draw_bubble(pen, el["bubble"], head[0] + face * 40 * s, top - 40 * s, s, INK, face)


def _face(d, head, hr, s, face, mood, t, seed, el):
    cx, cy = head[0] + face * 16 * s, head[1] + 4 * s
    blink = (t + seed % 7 * 0.37) % 3.7 < 0.13
    talking = el.get("_talking", False)
    ew, eh = 19 * s, 24 * s
    for dx in (-30, 30):
        ex = cx + dx * s
        if mood in ("sleep",) or (blink and mood not in ("dead", "surprised")):
            d.arc((ex - ew, cy - eh * 0.6, ex + ew, cy + eh * 0.6), 20, 160, fill=INK, width=max(2, int(5 * s)))
        elif mood == "dead":
            for a, b in (((-1, -1), (1, 1)), ((-1, 1), (1, -1))):
                d.line([(ex + a[0] * 13 * s, cy - 18 * s + a[1] * 13 * s), (ex + b[0] * 13 * s, cy - 18 * s + b[1] * 13 * s)],
                       fill=INK, width=max(2, int(6 * s)))
        else:
            big = 1.25 if mood == "surprised" else 1.0
            d.ellipse((ex - ew * big - 3 * s, cy - 22 * s - eh * big - 3 * s, ex + ew * big + 3 * s, cy - 22 * s + eh * big + 3 * s), fill=INK)
            d.ellipse((ex - ew * big, cy - 22 * s - eh * big, ex + ew * big, cy - 22 * s + eh * big), fill=(255, 255, 255))
            pr = 10 * s * (0.8 if mood == "surprised" else 1)
            px = ex + face * 7 * s
            d.ellipse((px - pr, cy - 18 * s - pr, px + pr, cy - 18 * s + pr), fill=INK)
            d.ellipse((px - pr * 0.35 + 3 * s, cy - 22 * s - pr * 0.35, px + pr * 0.35 + 3 * s, cy - 22 * s + pr * 0.35),
                      fill=(255, 255, 255))
    # Augenbrauen
    bw = max(2, int(7 * s))
    by = cy - 58 * s
    if mood == "angry":
        d.line([(cx - 52 * s, by - 8 * s), (cx - 12 * s, by + 10 * s)], fill=INK, width=bw)
        d.line([(cx + 52 * s, by - 8 * s), (cx + 12 * s, by + 10 * s)], fill=INK, width=bw)
    elif mood in ("sad", "sick"):
        d.line([(cx - 50 * s, by + 8 * s), (cx - 12 * s, by - 6 * s)], fill=INK, width=bw)
        d.line([(cx + 50 * s, by + 8 * s), (cx + 12 * s, by - 6 * s)], fill=INK, width=bw)
    elif mood == "smug":
        d.line([(cx - 48 * s, by + 4 * s), (cx - 14 * s, by + 4 * s)], fill=INK, width=bw)
        d.line([(cx + 14 * s, by - 10 * s), (cx + 48 * s, by - 2 * s)], fill=INK, width=bw)
    elif mood == "surprised":
        d.arc((cx - 52 * s, by - 20 * s, cx - 10 * s, by + 4 * s), 200, 340, fill=INK, width=bw)
        d.arc((cx + 10 * s, by - 20 * s, cx + 52 * s, by + 4 * s), 200, 340, fill=INK, width=bw)
    # Mund
    my = cy + 30 * s
    mw = max(2, int(6 * s))
    if talking and int(t * 9) % 2 == 0 and mood not in ("dead", "sleep"):
        d.ellipse((cx - 16 * s, my - 10 * s, cx + 16 * s, my + 18 * s), fill=(120, 30, 40), outline=INK, width=mw)
    elif mood in ("happy",):
        d.chord((cx - 32 * s, my - 22 * s, cx + 32 * s, my + 22 * s), 0, 180, fill=(120, 30, 40), outline=INK, width=mw)
        for dx in (-58, 58):
            d.ellipse((cx + dx * s - 13 * s, cy + 6 * s, cx + dx * s + 13 * s, cy + 22 * s), fill=(255, 150, 150))
    elif mood == "smug":
        d.arc((cx - 28 * s, my - 22 * s, cx + 28 * s, my + 12 * s), 20, 120, fill=INK, width=mw)
    elif mood in ("sad", "sick"):
        d.arc((cx - 24 * s, my, cx + 24 * s, my + 30 * s), 200, 340, fill=INK, width=mw)
        if mood == "sad":
            tx = cx - 34 * s
            ty = cy + ((t * 60) % 40) * s
            d.ellipse((tx - 7 * s, ty - 10 * s, tx + 7 * s, ty + 10 * s), fill=(110, 180, 255))
    elif mood == "angry":
        d.chord((cx - 26 * s, my - 4 * s, cx + 26 * s, my + 30 * s), 180, 360, fill=(120, 30, 40), outline=INK, width=mw)
    elif mood == "surprised":
        d.ellipse((cx - 15 * s, my - 8 * s, cx + 15 * s, my + 26 * s), fill=(120, 30, 40), outline=INK, width=mw)
    elif mood == "sleep":
        d.line([(cx - 12 * s, my + 6 * s), (cx + 12 * s, my + 6 * s)], fill=INK, width=mw)
        f = font(FONT_BOLD, 60 * s)
        z = int(t * 2) % 3 + 1
        d.text((head[0] + hr * 0.8, head[1] - hr * 1.7 - z * 8 * s), "Z" * z, font=f, fill=(255, 255, 255),
               stroke_width=max(1, int(5 * s)), stroke_fill=INK)
    elif mood != "dead":
        d.line([(cx - 18 * s, my + 4 * s), (cx + 18 * s, my + 4 * s)], fill=INK, width=mw)


def draw_potato(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.02:
        return
    d = pen.d
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.5) * H
    if el.get("glow"):
        draw_rays(d, cx, cy, 185 * s, t, (255, 230, 120), 12)
    cy += math.sin(t * 4 + cx) * 5 * pen.s
    _blob(d, cx, cy, 95 * s, 66 * s, (205, 155, 90), s, 6)
    d.ellipse((cx - 70 * s, cy - 50 * s, cx - 10 * s, cy - 20 * s), fill=(225, 185, 120))
    rnd = random.Random(int(el.get("x", 0) * 1000 + el.get("y", 0) * 7))
    for _ in range(5):
        ex = cx + rnd.uniform(-60, 60) * s
        ey = cy + rnd.uniform(-30, 35) * s
        d.ellipse((ex - 6 * s, ey - 4 * s, ex + 6 * s, ey + 4 * s), fill=(140, 95, 50))
    if el.get("face"):
        _face(d, (cx - 10 * s, cy + 15 * s), 60 * s, s * 0.75, 1, el["face"], t, 3, el)


def draw_rays(d, cx, cy, r, t, color, n=14, speed=0.4):
    for i in range(n):
        a0 = 2 * math.pi * i / n + t * speed
        a1 = a0 + math.pi / n
        d.polygon([(cx, cy), (cx + math.cos(a0) * r, cy + math.sin(a0) * r),
                   (cx + math.cos(a1) * r, cy + math.sin(a1) * r)], fill=color)


def draw_burst(pen, el, W, H, k, t, pal):
    """Comic-Explosion mit Text (BÄM!, WAS?!)."""
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.02:
        return
    d = pen.d
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.3) * H
    pts = []
    n = 14
    for i in range(n * 2):
        a = math.pi * i / n + 0.2
        r = (230 if i % 2 == 0 else 150) * s * (1 + 0.04 * math.sin(t * 20 + i))
        pts.append((cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r))
    _poly(d, pts, col(el.get("color"), (255, 210, 30)), s, 8)
    inner = [(cx + (x - cx) * 0.78, cy + (y - cy) * 0.78) for x, y in pts]
    d.polygon(inner, fill=(255, 120, 40))
    f = font(FONT_BOLD, el.get("text_size", 110) * s)
    tw = d.textlength(el.get("text", "BÄM!"), font=f)
    d.text((cx - tw / 2, cy - f.size * 0.62), el.get("text", "BÄM!"), font=f, fill=(255, 255, 255),
           stroke_width=max(2, int(9 * s)), stroke_fill=INK)


def draw_emote(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.02:
        return
    d = pen.d
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.3) * H
    kind = el.get("kind", "anger")
    if kind == "anger":
        c = (230, 40, 40)
        for a in range(4):
            ang = a * math.pi / 2 + math.pi / 4
            x1, y1 = cx + math.cos(ang) * 14 * s, cy + math.sin(ang) * 14 * s
            x2, y2 = cx + math.cos(ang) * 40 * s, cy + math.sin(ang) * 40 * s
            d.line([(x1, y1), (x2, y2)], fill=c, width=max(2, int(12 * s)))
    elif kind == "sweat":
        y = cy + (t * 40 % 30) * s
        _blob(d, cx, y, 14 * s, 22 * s, (120, 190, 255), s, 3)
    elif kind == "sparkle":
        for i, (dx, dy) in enumerate(((0, 0), (40, -30), (-35, -40))):
            r = (22 + 8 * math.sin(t * 8 + i)) * s
            x, y = cx + dx * s, cy + dy * s
            d.polygon([(x, y - r), (x + r * 0.3, y - r * 0.3), (x + r, y), (x + r * 0.3, y + r * 0.3),
                       (x, y + r), (x - r * 0.3, y + r * 0.3), (x - r, y), (x - r * 0.3, y - r * 0.3)],
                      fill=(255, 225, 60), outline=INK)
    elif kind == "heart":
        r = 26 * s * (1 + 0.1 * math.sin(t * 9))
        d.ellipse((cx - r * 1.4, cy - r, cx, cy + r * 0.4), fill=(230, 50, 80))
        d.ellipse((cx, cy - r, cx + r * 1.4, cy + r * 0.4), fill=(230, 50, 80))
        d.polygon([(cx - r * 1.35, cy - r * 0.1), (cx + r * 1.35, cy - r * 0.1), (cx, cy + r * 1.5)], fill=(230, 50, 80))
    elif kind in ("question", "exclaim"):
        f = font(FONT_BOLD, 110 * s)
        ch = "?" if kind == "question" else "!"
        d.text((cx - 20 * s, cy - 70 * s + math.sin(t * 6) * 6 * s), ch, font=f, fill=(255, 210, 30),
               stroke_width=max(2, int(7 * s)), stroke_fill=INK)


def draw_sticker(pen, el, W, H, k, t, pal):
    """Schräger Text-Sticker mit Farbe (Jahreszahlen, Orte, Fakten)."""
    if k <= 0.02:
        return
    s = pen.s
    f = font(FONT_BOLD if el.get("bold", True) else FONT_HAND, el.get("size", 90) * s)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = doodle.wrap(el["text"], f, el.get("width", 0.85) * W - 80 * s, tmp)
    asc, desc = f.getmetrics()
    lh = (asc + desc) * 1.02
    bw = int(max(tmp.textlength(l, font=f) for l in lines) + 80 * s)
    bh = int(lh * len(lines) + 50 * s)
    layer = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    fill = col(el.get("box"), (255, 210, 30))
    ld.rounded_rectangle((26, 26, bw + 14, bh + 14), radius=int(18 * s), fill=(0, 0, 0, 90))
    ld.rounded_rectangle((20, 20, bw + 8, bh + 8), radius=int(18 * s), fill=fill, outline=INK, width=max(2, int(7 * s)))
    y = 20 + 25 * s
    tc = col(el.get("color"), INK)
    for ln in lines:
        w = ld.textlength(ln, font=f)
        ld.text((20 + (bw - 12) / 2 - w / 2, y), ln, font=f, fill=tc)
        y += lh
    ang = el.get("angle", -4) + math.sin(t * 2) * 1.2
    sc = k
    layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
    if sc != 1:
        layer = layer.resize((max(1, int(layer.width * sc)), max(1, int(layer.height * sc))))
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.15) * H
    pen.img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


def draw_castle(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.02:
        return
    d = pen.d
    cx, by = el.get("x", 0.5) * W, el.get("y", 0.6) * H
    wall = col(el.get("color"), (190, 180, 165))
    _poly(d, [(cx - 170 * s, by), (cx - 170 * s, by - 190 * s), (cx + 170 * s, by - 190 * s), (cx + 170 * s, by)], wall, s)
    for tx in (-200, 200):
        _poly(d, [(cx + tx * s - 55 * s, by), (cx + tx * s - 55 * s, by - 300 * s), (cx + tx * s + 55 * s, by - 300 * s),
                  (cx + tx * s + 55 * s, by)], wall, s)
        _poly(d, [(cx + tx * s - 70 * s, by - 300 * s), (cx + tx * s, by - 400 * s), (cx + tx * s + 70 * s, by - 300 * s)],
              col(el.get("roof"), (60, 80, 150)), s)
    for i in range(5):
        x = cx - 150 * s + i * 75 * s
        d.rectangle((x, by - 225 * s, x + 40 * s, by - 190 * s), fill=wall, outline=INK, width=max(2, int(5 * s)))
    d.chord((cx - 55 * s, by - 130 * s, cx + 55 * s, by + 40 * s), 180, 360, fill=(80, 55, 40), outline=INK,
            width=max(2, int(6 * s)))
    if el.get("flag"):
        fx, fy = cx + 200 * s, by - 400 * s
        d.line([(fx, fy), (fx, fy - 110 * s)], fill=INK, width=max(2, int(7 * s)))
        wave = math.sin(t * 5) * 8 * s
        cols = [col(c) for c in el["flag"]]
        n = len(cols)
        for i, c in enumerate(cols):  # senkrechte Streifen
            xa, xb = fx + 100 * s * i / n, fx + 100 * s * (i + 1) / n
            wa, wb = wave * i / n, wave * (i + 1) / n
            d.polygon([(xa, fy - 110 * s + wa), (xb, fy - 110 * s + wb), (xb, fy - 50 * s + wb), (xa, fy - 50 * s + wa)], fill=c)


def draw_tree(pen, el, W, H, k, t, pal):
    s = pen.s * el.get("size", 1.0) * k
    if s <= 0.02:
        return
    d = pen.d
    cx, by = el.get("x", 0.5) * W, el.get("y", 0.6) * H
    _poly(d, [(cx - 22 * s, by), (cx - 16 * s, by - 160 * s), (cx + 16 * s, by - 160 * s), (cx + 22 * s, by)],
          (120, 80, 45), s, 5)
    sway = math.sin(t * 1.5 + cx) * 6 * s
    for dx, dy, r in ((-60, -190, 80), (60, -195, 85), (0, -260, 95)):
        _blob(d, cx + dx * s + sway, by + dy * s, r * s, r * s * 0.9, (70, 150, 70), s, 5)


# ------------------------------------------------------------------ Hintergründe

def _grad(W, H, top, bottom, split=1.0):
    y = np.linspace(0, 1, H)[:, None]
    t = np.clip(y / split, 0, 1)
    arr = (np.array(top)[None, None, :] * (1 - t[..., None]) + np.array(bottom)[None, None, :] * t[..., None])
    return np.repeat(arr, W, axis=1)


def make_background(name, W, H):
    s = min(W, H) / 1080
    gy = int(H * (0.62 if H > W else 0.72))   # Horizont/Bodenlinie
    if name in ("sky", "field", "village", "battle", "palace", "night", "dramatic", "map", "sea", "throne"):
        pass
    if name == "night":
        arr = _grad(W, H, (12, 18, 45), (45, 50, 95), 0.62)
    elif name == "dramatic":
        arr = _grad(W, H, (120, 15, 20), (40, 5, 10))
    elif name == "battle":
        arr = _grad(W, H, (240, 150, 70), (150, 60, 50), 0.62)
    elif name in ("palace", "throne"):
        arr = _grad(W, H, (120, 45, 55), (85, 30, 40))
    elif name == "map":
        arr = _grad(W, H, (240, 222, 180), (220, 195, 150))
    elif name == "sea":
        arr = _grad(W, H, (120, 190, 240), (210, 235, 250), 0.62)
    else:
        arr = _grad(W, H, (95, 170, 235), (200, 230, 250), 0.62)
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    rnd = random.Random(hash(name) % 1000)
    if name in ("sky", "field", "village", "night", "battle"):
        hill = (85, 160, 75) if name != "night" else (35, 60, 55)
        hill2 = (110, 185, 90) if name != "night" else (45, 75, 65)
        if name == "battle":
            hill, hill2 = (120, 105, 70), (145, 125, 85)
        for i, (c, off) in enumerate(((hill, -60), (hill2, 0))):
            pts = [(0, H)]
            for x in range(0, W + 40, 40):
                pts.append((x, gy + off * s - 50 * s * math.sin(x / (W / (2.3 + i)) + i * 2) - 30 * s * math.sin(x / 97)))
            pts.append((W, H))
            d.polygon(pts, fill=c)
        d.rectangle((0, gy + 30 * s, W, H), fill=hill2)
        if name == "field":
            for r in range(6):
                yy = gy + 60 * s + r * 55 * s
                d.line([(0, yy), (W, yy)], fill=(130, 95, 60), width=max(2, int(14 * s)))
        if name == "village":
            for i in range(4):
                x = W * (0.1 + i * 0.27)
                d.rectangle((x - 70 * s, gy - 90 * s, x + 70 * s, gy + 20 * s), fill=(220, 195, 160), outline=INK,
                            width=max(2, int(5 * s)))
                d.polygon([(x - 90 * s, gy - 90 * s), (x, gy - 170 * s), (x + 90 * s, gy - 90 * s)], fill=(180, 75, 55),
                          outline=INK)
    if name in ("palace", "throne"):
        for x in range(0, W, int(120 * s)):
            d.rectangle((x + 10 * s, 0, x + 50 * s, gy), fill=(135, 55, 65))
        d.rectangle((0, gy - 30 * s, W, gy), fill=(238, 186, 40))
        for i in range(0, W, int(110 * s)):
            for j in range(gy, H, int(110 * s)):
                c = (225, 210, 190) if ((i + j) // int(110 * s)) % 2 == 0 else (160, 120, 90)
                d.rectangle((i, j, i + 110 * s, j + 110 * s), fill=c)
        if name == "throne":
            cx = W / 2
            d.rectangle((cx - 150 * s, gy - 420 * s, cx + 150 * s, gy), fill=(200, 40, 50), outline=INK, width=max(2, int(8 * s)))
            d.rectangle((cx - 190 * s, gy - 160 * s, cx + 190 * s, gy), fill=(238, 186, 40), outline=INK, width=max(2, int(8 * s)))
    if name == "map":
        d.rectangle((30 * s, 30 * s, W - 30 * s, H - 30 * s), outline=(150, 110, 70), width=max(2, int(10 * s)))
        for _ in range(40):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            r = rnd.uniform(10, 60) * s
            d.ellipse((x - r, y - r, x + r, y + r), fill=(225, 205, 160))
    if name == "sea":
        for r in range(8):
            yy = gy + r * 70 * s
            d.rectangle((0, yy, W, H), fill=(40 + r * 5, 110 + r * 4, 180 - r * 6))
    if name == "night":
        for _ in range(90):
            x, y = rnd.uniform(0, W), rnd.uniform(0, gy * 0.9)
            r = rnd.uniform(1.5, 4) * s
            d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 245, 220))
        mx, my = W * 0.8, H * 0.1
        d.ellipse((mx - 80 * s, my - 80 * s, mx + 80 * s, my + 80 * s), fill=(250, 240, 190))
        d.ellipse((mx - 40 * s, my - 100 * s, mx + 110 * s, my + 50 * s), fill=(18, 25, 55))
    # leichte Papier-Körnung
    a = np.asarray(img).astype(np.int16)
    noise = np.random.default_rng(3).integers(-5, 6, size=(H // 3 + 1, W // 3 + 1), dtype=np.int16)
    noise = np.kron(noise, np.ones((3, 3), dtype=np.int16))[:H, :W]
    a = (a + noise[..., None]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(a)


def draw_clouds(img, name, W, H, t):
    if name not in ("sky", "field", "village", "sea"):
        return
    d = ImageDraw.Draw(img)
    s = min(W, H) / 1080
    for i, (y, sp, sc) in enumerate(((0.07, 18, 1.0), (0.17, 11, 0.8), (0.3, 25, 0.65))):
        x = ((i * 0.37 * W + t * sp * s * 3) % (W + 500 * s)) - 250 * s
        for dx, dy, r in ((0, 0, 70), (70, -25, 85), (150, 0, 65)):
            rr = r * s * sc
            d.ellipse((x + dx * s * sc - rr, y * H + dy * s * sc - rr, x + dx * s * sc + rr, y * H + dy * s * sc + rr),
                      fill=(255, 255, 255))


DRAWERS = {
    "figure": draw_person, "person": draw_person, "potato": draw_potato, "burst": draw_burst,
    "emote": draw_emote, "sticker": draw_sticker, "castle": draw_castle, "tree": draw_tree,
}
