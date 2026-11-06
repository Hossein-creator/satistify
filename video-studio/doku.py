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
RED = (178, 34, 34)
F_BLACK_WEIGHT = "Black"
TYPE_SPEED = 0.045   # Sekunden pro Buchstabe (Schreibmaschine)


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


def ease_out(p):  # schneller Start, weiches Ende (Hook-Kamerafahrt)
    p = min(1, max(0, p))
    return 1 - (1 - p) ** 3


EASES = {"inout": ease, "out": ease_out, "linear": lambda p: min(1, max(0, p))}


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
    p = EASES.get(el.get("ease", "inout"), ease)(local / max(0.1, dur))
    a = el.get("from", [0.5, 0.5, 1.0])
    b = el.get("to", [a[0], a[1], a[2] * 1.08])
    cx, cy, z = (a[i] + (b[i] - a[i]) * p for i in range(3))
    fit = el.get("fit", "cover")
    if fit == "contain":
        img.paste(blurred_cover(path, W, H), (0, 0))
        sc = min(W / im.width, H / im.height) * 0.94 * z
        tw, th = int(im.width * sc), int(im.height * sc)
        if tw <= W and th <= H:
            fr = im.resize((tw, th), Image.BILINEAR)
            img.paste(fr, ((W - tw) // 2, (H - th) // 2))
            return
    else:
        sc = max(W / im.width, H / im.height) * z
    # Handkamera: leichtes Atmen der Kamera (Position + Drehung), wirkt gefilmt statt animiert
    hh = el.get("_handheld", 0.0)
    rot = el.get("rot", [0, 0])
    ang = math.radians(rot[0] + (rot[1] - rot[0]) * p + hh * 0.35 * math.sin(0.7 * el.get("_t", 0) + 1.3))
    if ang:
        sc *= 1 + 1.05 * max(W / H, H / W) * abs(ang)
    cw, ch = W / sc, H / sc
    jx = hh * 0.004 * cw * (math.sin(1.1 * el.get("_t", 0)) + 0.5 * math.sin(2.7 * el.get("_t", 0) + 1))
    jy = hh * 0.004 * ch * (math.sin(0.9 * el.get("_t", 0) + 2) + 0.5 * math.sin(2.3 * el.get("_t", 0)))
    x0 = min(max(cx * im.width - cw / 2 + jx, 0), max(0, im.width - cw))
    y0 = min(max(cy * im.height - ch / 2 + jy, 0), max(0, im.height - ch))
    if not ang:
        fr = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    else:
        mx, my = x0 + cw / 2, y0 + ch / 2
        ca, sa = math.cos(ang) / sc, math.sin(ang) / sc
        # Ausgabe (u,v) -> Quelle: Mitte + R * (u - W/2, v - H/2) / sc
        data = (ca, -sa, mx - ca * W / 2 + sa * H / 2, sa, ca, my - sa * W / 2 - ca * H / 2)
        fr = im.transform((W, H), Image.AFFINE, data, Image.BILINEAR)
    if el.get("night"):   # Tag-Gemälde nachts wirken lassen (dunkel, kühl)
        a = np.asarray(fr, np.float32) * np.array([0.62, 0.68, 0.88], np.float32)
        fr = Image.fromarray(a.clip(0, 255).astype(np.uint8))
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
    since = el.get("_since", 1.0)
    alpha = min(1, since / 0.5)
    track = 6 * s + 34 * s * (1 - ease_out(since / 0.9))   # Buchstaben ziehen sich zusammen
    y = el.get("y", 0.42) * H

    def fn(d):
        f = vfont(F_SERIF, el.get("size", 92) * s, "Bold")
        lines = el["text"].split("\n")
        yy = y - len(lines) * f.size * 0.6
        widest = 0
        for ln in lines:
            widest = max(widest, spaced(d, (W / 2, yy), ln, f, (245, 238, 225, 255), track))
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
        shown = txt
        if el.get("typewriter", True):
            nchar = int(el.get("_since", 99) / TYPE_SPEED) + 1
            shown = txt[:nchar]
            # Breite des fertigen Texts, damit nichts springt
            full = sum(d.textlength(ch, font=f) for ch in txt) + 8 * s * (len(txt) - 1)
            part = sum(d.textlength(ch, font=f) for ch in shown) + 8 * s * (len(shown) - 1)
            spaced(d, (W / 2 - full / 2 + part / 2, y), shown, f, (245, 238, 225, 255), 8 * s)
            if nchar <= len(txt) and int(el.get("_since", 0) * 4) % 2 == 0:
                d.rectangle((W / 2 - full / 2 + part + 6 * s, y + f.size * 0.15, W / 2 - full / 2 + part + 10 * s,
                             y + f.size * 1.1), fill=GOLD + (255,))
            tw = full * min(1, nchar / max(1, len(txt)))
        else:
            tw = spaced(d, (W / 2, y), txt, f, (245, 238, 225, 255), 8 * s)
        d.line([(W / 2 - tw / 2, y + f.size * 1.35), (W / 2 + tw / 2, y + f.size * 1.35)], fill=GOLD + (255,),
               width=max(1, int(2 * s)))
    _overlay(pen.img, fn, 1.0 if el.get("typewriter", True) else min(1, k))


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


# ------------------------------------------------------------------ Neue Effekt-Elemente

@lru_cache(maxsize=16)
def stamp_layer(text, size, color, s):
    f = vfont(F_SANS, size, "Black")
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = text.split("\n")
    tw = max(tmp.textlength(ln, font=f) for ln in lines)
    th = f.size * 1.15 * len(lines)
    pad = int(36 * s)
    Wl, Hl = int(tw + 2 * pad), int(th + 2 * pad)
    lay = Image.new("RGBA", (Wl, Hl), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = tuple(color) + (255,)
    bw = max(3, int(9 * s))
    d.rectangle((bw, bw, Wl - bw, Hl - bw), outline=c, width=bw)
    d.rectangle((bw * 3, bw * 3, Wl - bw * 3, Hl - bw * 3), outline=c, width=max(2, bw // 2))
    y = pad - f.size * 0.08
    for ln in lines:
        d.text(((Wl - tmp.textlength(ln, font=f)) / 2, y), ln, font=f, fill=c)
        y += f.size * 1.15
    # Stempel-Textur: unregelmäßige Farbe (zufällig ausgefranst)
    rng = np.random.default_rng(3)
    a = np.asarray(lay.getchannel("A")).astype(np.float32)
    mask = rng.random((Hl // 3 + 1, Wl // 3 + 1))
    mask = np.kron(mask, np.ones((3, 3)))[:Hl, :Wl]
    a *= np.where(mask < 0.18, 0.15, 1.0) * (0.82 + 0.18 * rng.random((Hl, Wl)))
    lay.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return lay


def draw_stamp(pen, el, W, H, k, t, pal):
    """Stempel, der aufs Bild knallt (z. B. NICHT BELEGT, LEGENDE, WAHR)."""
    s = pen.s
    since = el.get("_since", 1.0)
    p = min(1, since / 0.16)
    scale = 2.3 - 1.3 * ease_out(p)
    size = int(el.get("size", 110) * s)
    lay = stamp_layer(el["text"].upper(), size, tuple(el.get("color", RED)), s)
    if lay.width > W * 0.8:   # zu breit -> kleiner stempeln
        size = int(size * W * 0.8 / lay.width)
        lay = stamp_layer(el["text"].upper(), size, tuple(el.get("color", RED)), s)
    lay = lay.rotate(el.get("angle", -9), resample=Image.BICUBIC, expand=True)
    w, h = int(lay.width * scale), int(lay.height * scale)
    lay = lay.resize((w, h), Image.BILINEAR)
    if p < 1:
        a = lay.getchannel("A").point(lambda v: int(v * p))
        lay.putalpha(a)
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.42) * H
    pen.img.paste(lay, (int(cx - w / 2), int(cy - h / 2)), lay)


def draw_embers(pen, el, W, H, k, t, pal):
    """Glühende Funken, die aufsteigen (Krieg, Feuer, Revolution)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rnd = random.Random(23)
    s = pen.s
    for i in range(el.get("n", 45)):
        x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
        sp = rnd.uniform(40, 140) * s
        life = (t * sp + y0) % (H * 1.1)
        y = H - life
        x = x0 + math.sin(t * rnd.uniform(0.8, 2.0) + i) * 40 * s
        r = rnd.uniform(1.5, 4.5) * s
        fl = 0.55 + 0.45 * math.sin(t * rnd.uniform(6, 12) + i)
        fade = min(1, life / (H * 0.25)) * min(1, (H * 1.1 - life) / (H * 0.3))
        a = int(255 * fl * fade)
        d.ellipse((x - r * 3, y - r * 3, x + r * 3, y + r * 3), fill=(255, 120, 30, a // 6))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 120, a))
    pen.img.paste(lay, (0, 0), lay)


@lru_cache(maxsize=4)
def fog_texture(W, H):
    rng = np.random.default_rng(9)
    w, h = W // 8, H // 8
    acc = np.zeros((h, w * 2), np.float32)
    for octv, amp in ((4, 1.0), (8, 0.5), (16, 0.25)):
        n = rng.random((octv * 2, octv * 2 * 2))
        im = Image.fromarray((n * 255).astype(np.uint8)).resize((w * 2, h), Image.BICUBIC)
        acc += np.asarray(im, np.float32) / 255 * amp
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    return acc ** 2


def draw_fog(pen, el, W, H, k, t, pal):
    """Langsam ziehender Nebel/Rauch."""
    tex = fog_texture(W, H)
    h, w2 = tex.shape
    w = w2 // 2
    off = int((t * el.get("speed", 6)) % w)
    part = tex[:, off:off + w]
    a = Image.fromarray((part * 255 * el.get("strength", 0.35)).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    col = Image.new("RGB", (W, H), tuple(el.get("color", (200, 196, 190))))
    pen.img.paste(col, (0, 0), a)


@lru_cache(maxsize=8)
def _radial(W, H):
    yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32) * 4
    return xx, yy


def draw_spotlight(pen, el, W, H, k, t, pal):
    """Dunkelt alles außer einem Kreis ab: lenkt den Blick auf ein Bilddetail."""
    since = el.get("_since", 1.0)
    p = ease_out(since / 0.7)
    xx, yy = _radial(W, H)
    cx, cy = el.get("x", 0.5) * W, el.get("y", 0.5) * H
    r = el.get("r", 0.22) * W * (2.6 - 1.6 * p)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((dist - r) / (r * 0.5), 0, 1) * el.get("dark", 0.72) * min(1, since / 0.3)
    a = Image.fromarray((m * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    pen.img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), a)


DRAWERS_FX = {"stamp": draw_stamp, "embers": draw_embers, "fog": draw_fog, "spotlight": draw_spotlight}


# ------------------------------------------------------------------ Nachbearbeitung pro Bild

def chroma(img, px):
    """Chromatische Aberration (RGB-Versatz) für Treffer-Momente."""
    px = int(px)
    if px < 1:
        return img
    a = np.asarray(img)
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], px, axis=1)
    out[..., 2] = np.roll(a[..., 2], -px, axis=1)
    return Image.fromarray(out)


def zoom_blur(img, amount):
    """Radiale Bewegungsunschärfe (Zoom-Punch)."""
    if amount < 0.004:
        return img
    W, H = img.size
    acc = np.asarray(img, np.float32)
    n = 1
    for f in (amount * 0.5, amount):
        cw, ch = W / (1 + f), H / (1 + f)
        z = img.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
        acc += np.asarray(z, np.float32)
        n += 1
    return Image.fromarray((acc / n).astype(np.uint8))


def hblur(a, r):
    """Horizontale Bewegungsunschärfe über kumulative Summe (schnell)."""
    r = int(r)
    if r < 2:
        return a
    c = np.cumsum(np.pad(a.astype(np.float32), ((0, 0), (r, r), (0, 0)), mode="edge"), axis=1)
    return ((c[:, 2 * r:] - c[:, :-2 * r]) / (2 * r))[:, :a.shape[1]]


def whip(prev, new, p):
    """Whip-Pan: altes Bild fliegt nach links raus, neues kommt von rechts, mit Bewegungsunschärfe."""
    W, H = new.size
    e = ease(p)
    off = int(W * e)
    a = np.zeros((H, W, 3), np.float32)
    pa, na = np.asarray(prev, np.float32), np.asarray(new, np.float32)
    if off < W:
        a[:, :W - off] = pa[:, off:]
    if off > 0:
        a[:, W - off:] = na[:, :off]
    blur = math.sin(math.pi * p) * W * 0.09
    return Image.fromarray(hblur(a, blur).clip(0, 255).astype(np.uint8))


@lru_cache(maxsize=4)
def leak_texture(W, H):
    w, h = W // 6, H // 6
    yy, xx = np.mgrid[0:h, 0:w * 2].astype(np.float32)
    a = np.zeros((h, w * 2, 3), np.float32)
    for (cx, cy, r, col) in ((0.25, 0.3, 0.55, (255, 140, 50)), (0.9, 0.7, 0.45, (255, 70, 30)),
                             (1.5, 0.2, 0.6, (255, 190, 110)), (1.8, 0.85, 0.5, (240, 90, 40))):
        d = np.sqrt((xx - cx * w) ** 2 + ((yy - cy * h) * 0.8) ** 2) / (r * w)
        g = np.clip(1 - d, 0, 1) ** 2
        a += g[..., None] * np.array(col, np.float32)
    return np.clip(a, 0, 255)


def light_leak(img, strength, t):
    """Warmer Lichteinfall wie bei altem Film (Screen-Blend)."""
    if strength < 0.01:
        return img
    W, H = img.size
    tex = leak_texture(W, H)
    h, w2, _ = tex.shape
    w = w2 // 2
    off = int((t * 20) % w)
    part = Image.fromarray(tex[:, off:off + w].astype(np.uint8)).resize((W, H), Image.BILINEAR)
    a = np.asarray(img, np.float32) / 255
    b = np.asarray(part, np.float32) / 255 * strength
    return Image.fromarray(((1 - (1 - a) * (1 - b)) * 255).astype(np.uint8))


DRAWERS = {"title": draw_title, "date": draw_date, "lower": draw_lower, "mark": draw_mark, "dust": draw_dust, **DRAWERS_FX}


# ------------------------------------------------------------------ Look (Farbkorrektur, Korn, Vignette)

_grade_cache = {}


def grade(img, t, strength=1.0, warm=True, flicker=0.0):
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
    if flicker:
        a = a * (1 + flicker * (math.sin(t * 37.0) * 0.5 + math.sin(t * 13.3 + 1) * 0.5))
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
        jump = -7 * s * max(0, 1 - (local - ws) / 0.12) if active else 0
        d.text((x, y + jump), txt, font=f, fill=colr)
        x += tw + space
