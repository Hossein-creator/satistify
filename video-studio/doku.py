"""Doku-Stil: echte historische Bilder mit Kamerafahrt, filmische Farbe, ernste Typografie.

Element-Typen (in scenes[].visual):
  photo     – Vollbild-Gemälde/Foto mit Kamerafahrt (Ken Burns)
              {type: photo, src: assets/bild.jpg, from: [cx, cy, zoom], to: [cx, cy, zoom], fit: cover|contain}
              cx/cy = Bildpunkt (0..1) in der Mitte, zoom 1 = bildschirmfüllend
  title     – große Titelkarte (Cinzel), optional sub
  date      – Ort/Datum oben (z. B. "POTSDAM · 1756")
  lower     – Bauchbinde unten links ("Friedrich II." / "König von Preußen")
  mark      – Kreis/Rahmen zum Hervorheben eines Bilddetails (Bildschirm-Koordinaten)
  dust      – schwebende Staubpartikel
"""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F_SERIF = os.path.join(HERE, "fonts", "Cinzel.ttf")
F_SANS = os.path.join(HERE, "fonts", "Montserrat.ttf")
GOLD = (214, 178, 102)


@lru_cache(maxsize=128)
def vfont(path, size, weight="Bold"):
    f = ImageFont.truetype(path, max(8, int(size)))
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


@lru_cache(maxsize=16)
def load(path):
    im = Image.open(path).convert("RGB")
    return im


@lru_cache(maxsize=16)
def blurred_cover(path, W, H):
    im = load(path)
    sc = max(W / im.width, H / im.height)
    bg = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.BILINEAR)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(28))
    return Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)


def ease(p):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, p)))


def draw_photo(img, el, W, H, local, dur, base_dir):
    path = el["src"] if os.path.isabs(el["src"]) else os.path.join(base_dir, el["src"])
    if not os.path.exists(path) and el.get("fallback"):  # Ersatzbild, bis das eigentliche geladen ist
        fb = el["fallback"]
        el = {**el, "src": fb["src"], "from": fb.get("from", el.get("from")), "to": fb.get("to", el.get("to")),
              "fit": fb.get("fit", "cover")}
        path = os.path.join(base_dir, el["src"])
    if not os.path.exists(path):
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, W, H), fill=(30, 28, 26))
        d.text((40, H / 2), "Bild fehlt: " + os.path.basename(path)[:40], fill=(200, 80, 80),
               font=vfont(F_SANS, 34 * W / 1080, "Bold"))
        return
    im = load(path)
    p = ease(local / max(0.1, dur))
    a = el.get("from", [0.5, 0.5, 1.0])
    b = el.get("to", [a[0], a[1], a[2] * 1.08])
    cx, cy, z = (a[i] + (b[i] - a[i]) * p for i in range(3))
    fit = el.get("fit", "cover")
    if fit == "contain":
        img.paste(blurred_cover(path, W, H), (0, 0))
        sc = min(W / im.width, H / im.height) * 0.94 * z
    else:
        sc = max(W / im.width, H / im.height) * z
    cw, ch = W / sc, H / sc
    x0 = cx * im.width - cw / 2
    y0 = cy * im.height - ch / 2
    if fit == "contain":
        tw, th = int(im.width * sc), int(im.height * sc)
        if tw <= W and th <= H:
            fr = im.resize((tw, th), Image.BILINEAR)
            img.paste(fr, ((W - tw) // 2, (H - th) // 2))
            return
    x0 = min(max(x0, 0), max(0, im.width - cw))
    y0 = min(max(y0, 0), max(0, im.height - ch))
    fr = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    img.paste(fr, (0, 0))


def _overlay(img, draw_fn, alpha):
    if alpha <= 0.01:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    if alpha < 1:
        a = lay.getchannel("A").point(lambda v: int(v * alpha))
        lay.putalpha(a)
    img.paste(lay, (0, 0), lay)


def spaced(d, xy, text, font, fill, spacing, anchor_center=True, shadow=True):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        if shadow:
            d.text((x + 3, y + 4), ch, font=font, fill=(0, 0, 0, 160))
        d.text((x, y), ch, font=font, fill=fill)
        x += w + spacing
    return total


def draw_title(pen, el, W, H, k, t, pal):
    s = pen.s
    alpha = min(1, k)
    y = el.get("y", 0.42) * H

    def fn(d):
        f = vfont(F_SERIF, el.get("size", 92) * s, "Bold")
        lines = el["text"].split("\n")
        yy = y - len(lines) * f.size * 0.6
        widest = 0
        for ln in lines:
            widest = max(widest, spaced(d, (W / 2, yy), ln, f, (245, 238, 225, 255), 6 * s))
            yy += f.size * 1.15
        lw = min(W * 0.8, widest * (0.6 + 0.4 * alpha))
        d.line([(W / 2 - lw / 2, yy + 14 * s), (W / 2 + lw / 2, yy + 14 * s)], fill=GOLD + (255,), width=max(1, int(3 * s)))
        if el.get("sub"):
            fs = vfont(F_SANS, el.get("sub_size", 40) * s, "Medium")
            spaced(d, (W / 2, yy + 40 * s), el["sub"].upper(), fs, GOLD + (255,), 5 * s)
    _overlay(pen.img, fn, alpha)


def draw_date(pen, el, W, H, k, t, pal):
    s = pen.s

    def fn(d):
        size = el.get("size", 58) * s
        txt = el["text"].upper()
        f = vfont(F_SERIF, size, "Bold")
        est = sum(d.textlength(ch, font=f) for ch in txt) + 8 * s * (len(txt) - 1)
        if est > W * 0.88:  # zu breit -> verkleinern
            f = vfont(F_SERIF, size * W * 0.88 / est, "Bold")
        y = el.get("y", 0.09) * H
        tw = spaced(d, (W / 2, y), txt, f, (245, 238, 225, 255), 8 * s)
        d.line([(W / 2 - tw / 2, y + f.size * 1.35), (W / 2 + tw / 2, y + f.size * 1.35)], fill=GOLD + (255,),
               width=max(1, int(2 * s)))
    _overlay(pen.img, fn, min(1, k))


def draw_lower(pen, el, W, H, k, t, pal):
    s = pen.s
    slide = (1 - min(1, k)) * 60 * s

    def fn(d):
        x = el.get("x", 0.07) * W - slide
        y = el.get("y", 0.6) * H
        f1 = vfont(F_SERIF, el.get("size", 60) * s, "Bold")
        f2 = vfont(F_SANS, el.get("size", 60) * 0.55 * s, "Medium")
        w1 = d.textlength(el["text"], font=f1)
        w2 = d.textlength(el.get("sub", "").upper(), font=f2) if el.get("sub") else 0
        bw = max(w1, w2) + 60 * s
        bh = f1.size * 1.3 + (f2.size * 1.6 if el.get("sub") else 0) + 20 * s
        d.rectangle((x, y, x + bw, y + bh), fill=(10, 10, 12, 170))
        d.rectangle((x, y, x + 8 * s, y + bh), fill=GOLD + (255,))
        d.text((x + 30 * s, y + 10 * s), el["text"], font=f1, fill=(245, 238, 225, 255))
        if el.get("sub"):
            d.text((x + 30 * s, y + 10 * s + f1.size * 1.3), el["sub"].upper(), font=f2, fill=GOLD + (255,))
    _overlay(pen.img, fn, min(1, k))


def draw_mark(pen, el, W, H, k, t, pal):
    s = pen.s
    p = min(1, k)

    def fn(d):
        cx, cy = el.get("x", 0.5) * W, el.get("y", 0.5) * H
        r = el.get("r", 0.12) * W
        c = tuple(el.get("color", [200, 40, 40])) + (255,)
        w = max(2, int(7 * s))
        if el.get("shape", "circle") == "circle":
            d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * p, fill=c, width=w)
        else:
            d.rectangle((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), outline=c, width=w)
        if el.get("label") and p >= 1:
            f = vfont(F_SANS, 40 * s, "Bold")
            tw = d.textlength(el["label"].upper(), font=f)
            ly = cy + r + 16 * s
            d.rectangle((cx - tw / 2 - 14 * s, ly, cx + tw / 2 + 14 * s, ly + f.size * 1.4), fill=c)
            d.text((cx - tw / 2, ly + 4 * s), el["label"].upper(), font=f, fill=(255, 255, 255, 255))
    _overlay(pen.img, fn, 1)


def draw_dust(pen, el, W, H, k, t, pal):
    d = pen.d
    rnd = random.Random(11)
    for i in range(el.get("n", 40)):
        x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
        sp = rnd.uniform(6, 22)
        x = (x0 + math.sin(t * 0.3 + i) * 30 + t * sp * 0.4) % W
        y = (y0 - t * sp) % H
        r = rnd.uniform(1.2, 3.6) * pen.s
        a = int(90 + 80 * math.sin(t * 1.5 + i))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 245, 220))


DRAWERS = {"title": draw_title, "date": draw_date, "lower": draw_lower, "mark": draw_mark, "dust": draw_dust}


# ------------------------------------------------------------------ Look (Farbkorrektur, Korn, Vignette)

_grade_cache = {}


def grade(img, t, strength=1.0, warm=True):
    W, H = img.size
    key = (W, H)
    if key not in _grade_cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        v = 1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
        vign = np.clip(v, 0.25, 1)[..., None]
        rng = np.random.default_rng(5)
        grains = [rng.normal(0, 7, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
        grains = [np.kron(g, np.ones((2, 2), np.float32))[:H, :W][..., None] for g in grains]
        _grade_cache[key] = (vign, grains)
    vign, grains = _grade_cache[key]
    a = np.asarray(img).astype(np.float32)
    gray = a.mean(axis=2, keepdims=True)
    a = gray + (a - gray) * (1 - 0.18 * strength)            # leicht entsättigt
    a = (a - 128) * (1 + 0.12 * strength) + 122               # mehr Kontrast, etwas dunkler
    if warm:
        lum = gray / 255.0
        a[..., 0] += 10 * lum[..., 0] * strength               # Lichter warm
        a[..., 2] += 12 * (1 - lum[..., 0]) * strength          # Schatten kühl
        a[..., 2] -= 6 * lum[..., 0] * strength
    a = a * vign + grains[int(t * 24) % len(grains)] * strength
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def captions(img, words_chunk, local, W, H, s, y_rel, hl):
    d = ImageDraw.Draw(img, "RGBA")
    f = vfont(F_SANS, 64 * s, "ExtraBold")
    parts = [w[0] for w in words_chunk]
    space = d.textlength(" ", font=f)
    widths = [d.textlength(p, font=f) for p in parts]
    total = sum(widths) + space * (len(parts) - 1)
    if total > W * 0.88:
        f = vfont(F_SANS, 64 * s * W * 0.88 / total, "ExtraBold")
        space = d.textlength(" ", font=f)
        widths = [d.textlength(p, font=f) for p in parts]
        total = sum(widths) + space * (len(parts) - 1)
    x = W / 2 - total / 2
    y = H * y_rel
    pad = 18 * s
    d.rounded_rectangle((x - pad, y - pad * 0.5, x + total + pad, y + f.size * 1.25 + pad * 0.5), radius=10 * s,
                        fill=(0, 0, 0, 120))
    for (w, ws, we), txt, tw in zip(words_chunk, parts, widths):
        active = ws <= local < we + 0.02
        key = w.lower().strip(",.;:!?…")
        colr = GOLD if (active or key in hl) else (245, 240, 230)
        d.text((x, y), txt, font=f, fill=colr)
        x += tw + space
