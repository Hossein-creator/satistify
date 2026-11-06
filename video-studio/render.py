#!/usr/bin/env python3
"""Rendert ein Doodle-History-Video aus einer video.yaml.

Aufruf:
  python3 video-studio/render.py videos/<ordner>/video.yaml            # volles Video
  python3 video-studio/render.py videos/<ordner>/video.yaml --stills   # nur Vorschaubilder je Szene
  python3 video-studio/render.py videos/<ordner>/video.yaml --scale 0.5  # schneller Test in halber Größe

Eigene Stimme: Lege Aufnahmen als videos/<ordner>/aufnahme/szene_01.wav, szene_02.wav ... ab.
Vorhandene Aufnahmen ersetzen automatisch die Computerstimme der jeweiligen Szene.
"""
import argparse
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import wave

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doodle  # noqa: E402
import cartoon  # noqa: E402
import doku  # noqa: E402
import music as score_music  # noqa: E402
import beats  # noqa: E402
import epochen  # noqa: E402

DARK_BGS = {"night", "dramatic", "palace", "throne", "red"}
ROLE_BY_PROP = [("crown", "king"), ("tricorn", "soldier"), ("farmer", "farmer"), ("wig", "noble"), ("helmet", "knight")]


def drawer(el):
    if el["type"] == "stick":
        return doodle.draw_figure
    return doku.DRAWERS.get(el["type"]) or cartoon.DRAWERS.get(el["type"]) or doodle.DRAWERS[el["type"]]


def palette(name):
    if name in ("paper",):
        return doodle.PALETTES["paper"]
    ink = (245, 240, 230) if name in DARK_BGS else (28, 24, 30)
    return {"bg": (0, 0, 0), "ink": ink, "soft": ink}

FPS = 30
SR = 44100
SIZES = {"short": (1080, 1920), "long": (1920, 1080)}


# ------------------------------------------------------------------ Audio

def ffmpeg_to_mono(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def trim_silence(x, thr=0.012, margin=0.04):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    m = int(margin * SR)
    return x[max(0, idx[0] - m): min(len(x), idx[-1] + m)]


_voices = {}


def tts(text, voice_name, length_scale, out_path):
    from piper import PiperVoice, SynthesisConfig
    if voice_name not in _voices:
        p = os.path.join(HERE, "voices", voice_name + ".onnx")
        if not os.path.exists(p):
            sys.exit(f"Stimme fehlt: {p} – bitte zuerst video-studio/setup.sh ausführen.")
        _voices[voice_name] = PiperVoice.load(p)
    with wave.open(out_path, "wb") as wf:
        _voices[voice_name].synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=length_scale))


# ElevenLabs: Stimmen-Kürzel -> voice_id (nur vom Nutzer genehmigte Stimmen eintragen)
ELEVEN_VOICES = {
    "george": "JBFqnCBsd6RMkjVDRZzb",  # genehmigt 06.11.2026 (Gratis-Plan)
}


def tts_eleven(text, voice_name, out_path, prev_text="", next_text="", model="eleven_multilingual_v2", speed=1.0):
    """ElevenLabs mit Zeitstempeln. Schreibt out_path (mp3) und out_path + '.json' (Zeichen-Zeiten).
    Key nur aus der Umgebung (ELEVENLABS_API_KEY), nie im Repo speichern."""
    import base64
    import json as _json
    import urllib.request
    # Key liegt als Netzwerk-Secret in der Cloud-Umgebung; der Proxy setzt den Header ein.
    # Lokal ohne Proxy: ELEVENLABS_API_KEY setzen. Key nie ins Repo schreiben.
    key = os.environ.get("ELEVENLABS_API_KEY") or "proxy-injected"
    vid = ELEVEN_VOICES.get(voice_name, voice_name)
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "speed": speed}}
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128",
        data=_json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        d = _json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs-Fehler {e.code}: {e.read()[:300]!r} (Kontingent leer? Neuer Key nötig?)")
    open(out_path, "wb").write(base64.b64decode(d["audio_base64"]))
    _json.dump(d.get("alignment") or {}, open(out_path + ".json", "w"))


def eleven_word_timings(text, align, offset):
    """Wort-Zeiten aus der Zeichen-Ausrichtung von ElevenLabs (offset = abgeschnittene Stille am Anfang)."""
    chars = align.get("characters") or []
    st, en = align.get("character_start_times_seconds") or [], align.get("character_end_times_seconds") or []
    out, i = [], 0
    for w in text.split():
        # nächstes Nicht-Leerzeichen suchen
        while i < len(chars) and chars[i].isspace():
            i += 1
        j = min(len(chars), i + len(w)) - 1
        if i >= len(chars):
            break
        out.append((w, float(max(0.0, st[i] - offset)), float(max(0.0, en[max(i, j)] - offset))))
        i = j + 1
    return out if len(out) == len(text.split()) else None


def sfx(kind):
    """Synthetische, lizenzfreie Soundeffekte."""
    if kind == "pop":
        n = int(0.07 * SR)
        t = np.arange(n) / SR
        f = 520 + 900 * t / t[-1]
        return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
    if kind == "whoosh":
        n = int(0.32 * SR)
        rng = np.random.default_rng(1)
        x = rng.standard_normal(n)
        x = np.convolve(x, np.ones(25) / 25, mode="same")
        env = np.sin(np.linspace(0, np.pi, n)) ** 2
        return 0.9 * x * env
    if kind == "boom":
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        rng = np.random.default_rng(2)
        noise = np.convolve(rng.standard_normal(n), np.ones(60) / 60, mode="same")
        return (0.9 * np.sin(2 * np.pi * (55 - 20 * t) * t) + 1.5 * noise) * np.exp(-t * 3)
    if kind == "hit":
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        rng = np.random.default_rng(4)
        noise = np.convolve(rng.standard_normal(n), np.ones(200) / 200, mode="same")
        return (np.sin(2 * np.pi * (48 - 12 * t) * t) + 3 * noise) * np.exp(-t * 2.2) * 0.9
    if kind == "heartbeat":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        beat = lambda t0: np.sin(2 * np.pi * 50 * (t - t0)) * np.exp(-np.clip(t - t0, 0, None) * 18) * (t >= t0)
        return 0.9 * (beat(0.0) + 0.7 * beat(0.28))
    if kind == "ding":
        n = int(0.8 * SR)
        t = np.arange(n) / SR
        return 0.35 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1975 * t)) * np.exp(-t * 6)
    if kind == "tick":
        n = int(0.04 * SR)
        t = np.arange(n) / SR
        return 0.6 * np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120)
    return np.zeros(1)


def ambient_pad(total, mood="mystery"):
    """Leiser, lizenzfreier Klangteppich (synthetisch)."""
    n = int(total * SR)
    t = np.arange(n) / SR
    chords = {"dark": [73.42, 87.31, 110.0, 146.83], "mystery": [110.0, 130.81, 164.81], "epic": [98.0, 146.83, 196.0], "light": [130.81, 164.81, 196.0]}
    freqs = chords.get(mood, chords["mystery"])
    x = np.zeros(n)
    for i, f in enumerate(freqs):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + 0.02 * i) * t)
        x += lfo * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t))
    fade = np.minimum(1, np.minimum(t / 2.0, (total - t) / 2.0))
    return x / len(freqs) * fade


def add(track, clip, at, gain):
    i = int(at * SR)
    if i >= len(track) or i < 0:
        return
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i] * gain


# ------------------------------------------------------------------ Timeline

PUNCT = ",.;:!?…"


def word_timings(text, dur):
    words = text.split()
    weights = [len(w) + 2 + (4 if w[-1] in PUNCT else 0) for w in words]
    total = sum(weights) or 1
    out, t = [], 0.0
    for w, wt in zip(words, weights):
        d = dur * wt / total
        out.append((w, t, t + d))
        t += d
    return out


def chunk_words(timed, max_words=3, max_chars=18):
    chunks, cur = [], []
    for w in timed:
        cur.append(w)
        chars = sum(len(x[0]) for x in cur)
        if len(cur) >= max_words or chars >= max_chars or w[0][-1] in PUNCT:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def build_timeline(spec, base_dir, build_dir, use_tts=True):
    voice = spec.get("voice", "de-thorsten-low")
    ls = spec.get("speed", 1.0)
    t = spec.get("lead_in", 0.0)
    scenes = spec["scenes"]
    for i, sc in enumerate(scenes):
        rec = os.path.join(base_dir, "aufnahme", f"szene_{i + 1:02d}.wav")
        if os.path.exists(rec):
            src, sc["_voice_src"] = rec, "eigene Aufnahme"
        elif use_tts and str(voice).startswith("eleven:"):
            say = sc.get("say", sc["text"])
            vname = voice.split(":", 1)[1]
            prev_t = scenes[i - 1].get("say", scenes[i - 1]["text"]) if i > 0 else ""
            next_t = scenes[i + 1].get("say", scenes[i + 1]["text"]) if i + 1 < len(scenes) else ""
            h = hashlib.md5(f"{voice}|{ls}|{say}|{prev_t}|{next_t}".encode()).hexdigest()[:10]
            src = os.path.join(build_dir, f"el_{i + 1:02d}_{h}.mp3")
            if not os.path.exists(src):
                tts_eleven(say, vname, src, prev_t, next_t, spec.get("eleven_model", "eleven_multilingual_v2"),
                           spec.get("eleven_speed", 1.0))
            sc["_voice_src"] = f"KI-Stimme ElevenLabs ({vname})"
            sc["_align"] = src + ".json"
        elif use_tts:
            say = sc.get("say", sc["text"])
            h = hashlib.md5(f"{voice}|{ls}|{say}".encode()).hexdigest()[:10]
            src = os.path.join(build_dir, f"tts_{i + 1:02d}_{h}.wav")
            if not os.path.exists(src):
                tts(say, voice, ls, src)
            sc["_voice_src"] = f"Computerstimme ({voice})"
        else:
            src = None
        lead = 0.0
        if src:
            raw = ffmpeg_to_mono(src)
            nz = np.where(np.abs(raw) > 0.012)[0]
            lead = float(max(0, int(nz[0]) - int(0.04 * SR)) / SR) if len(nz) else 0.0
            audio = trim_silence(raw)
        else:
            audio = np.zeros(int(max(1.5, len(sc["text"]) / 14) * SR))
        sc["_audio"] = audio
        vd = len(audio) / SR
        sc["_start"] = t
        sc["_vdur"] = vd
        sc["_end"] = t + vd + sc.get("pause", 0.22)
        sc["_words"] = None
        if sc.get("_align") and os.path.exists(sc["_align"]) and sc.get("say", sc["text"]) == sc["text"]:
            import json as _json
            sc["_words"] = eleven_word_timings(sc["text"], _json.load(open(sc["_align"])), lead)
        if not sc["_words"]:
            sc["_words"] = word_timings(sc["text"], vd)
        t = sc["_end"]
        if sc.get("slides") and not sc.get("_slides_done"):
            # B-Roll: mehrere Bilder pro Szene, gleichmäßig verteilt, Übergänge abwechselnd
            sl = sc["slides"]
            span = vd + sc.get("pause", 0.22)
            enters = sc.get("slide_enter", ["slide", "zoom", "fade"])
            ph = []
            for k, item in enumerate(sl):
                item = dict(item) if isinstance(item, dict) else {"src": item}
                item.setdefault("type", "photo")
                item.setdefault("at", round(k * span / len(sl), 3))
                item.setdefault("enter", enters[(k - 1) % len(enters)] if k else "fade")
                ph.append(item)
            sc["visual"] = ph + [e for e in sc.get("visual", []) if e.get("type") != "photo"]
            sc["_slides_done"] = True
        if spec.get("auto_emoji") and sc.get("auto_emoji", True) and not sc.get("_emoji_done"):
            have = {e.get("at_word", "").lower() for e in sc.get("visual", []) if e.get("type") == "emoji"}
            n_have = sum(1 for e in sc.get("visual", []) if e.get("type") in ("emoji", "dialog", "stamp", "count"))
            if n_have == 0:
                side = [0.8, 0.2][i % 2]
                for e in doku.auto_emojis(sc["_words"], have, spec.get("auto_emoji_max", 1)):
                    e.update({"x": side, "y": 0.63, "at": round(e.pop("_auto_at"), 2)})
                    sc.setdefault("visual", []).append(e)
            sc["_emoji_done"] = True
        for el in sc.get("visual", []):
            if el.get("src") and el["type"] == "dialog":
                el["src_abs"] = os.path.join(base_dir, el["src"])
            if "reveal_word" in el:
                key = el["reveal_word"].lower()
                w = next((w for w in sc["_words"] if key in w[0].lower()), None)
                el["_reveal"] = w[1] if w else 0.0
        for j, el in enumerate(sc.get("visual", [])):
            if "at_word" in el:
                key = el["at_word"].lower()
                hit = next((w for w in sc["_words"] if key in w[0].lower()), None)
                el["_at"] = hit[1] if hit else 0.0
            elif "at" in el:
                el["_at"] = float(el["at"])
            else:
                el["_at"] = 0.0 if j == 0 else min(vd * 0.8, 0.35 * j)
            if i == 0 and el["_at"] <= 0.0:
                el["_at"] = -1.0  # sofort sichtbar: erster Frame ist nie leer
    total = t + spec.get("tail", 0.5)
    return total


# ------------------------------------------------------------------ Bild

def ease_out_back(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


_bg_cache = {}


def background(pal_name, W, H):
    key = (pal_name, W, H)
    if key not in _bg_cache:
        pal = doodle.PALETTES[pal_name]
        img = Image.new("RGB", (W, H), pal["bg"])
        rng = np.random.default_rng(7)
        noise = (rng.standard_normal((H // 4, W // 4)) * 6).astype(np.int16)
        noise = np.kron(noise, np.ones((4, 4), dtype=np.int16))[:H, :W]
        arr = np.asarray(img).astype(np.int16) + noise[..., None]
        yy, xx = np.mgrid[0:H, 0:W]
        vign = 1 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        arr = (arr * vign[..., None]).clip(0, 255).astype(np.uint8)
        _bg_cache[key] = Image.fromarray(arr)
    return _bg_cache[key]


def background_any(name, W, H):
    if name == "paper":
        return background("paper", W, H)
    key = ("c", name, W, H)
    if key not in _bg_cache:
        _bg_cache[key] = cartoon.make_background(name, W, H)
    return _bg_cache[key]


def draw_captions(img, sc, local, W, H, s, fmt, spec):
    if spec.get("captions", True) is False:
        return
    words = sc["_words"]
    chunks = chunk_words(words, spec.get("caption_words", 3))
    cur = None
    for ch in chunks:
        if ch[0][1] <= local < ch[-1][2] + 0.05:
            cur = ch
            break
    if cur is None:
        return
    if spec.get("style") == "doku":
        doku.captions(img, cur, local, W, H, s, spec.get("caption_y", 0.76 if fmt == "short" else 0.85),
                      [h.lower() for h in sc.get("highlight", [])])
        return
    d = ImageDraw.Draw(img)
    size = (100 if fmt == "short" else 74) * s
    p = min(1, (local - cur[0][1]) / 0.12)
    size *= 0.85 + 0.15 * p
    f = doodle.font(doodle.FONT_BOLD, size)
    hl = [h.lower() for h in sc.get("highlight", [])]
    parts = [w[0].upper() for w in cur]
    space = d.textlength(" ", font=f) * 1.7
    widths = [d.textlength(p_, font=f) for p_ in parts]
    total = sum(widths) + space * (len(parts) - 1)
    if total > W * 0.9:  # zu breit -> verkleinern
        f = doodle.font(doodle.FONT_BOLD, size * W * 0.9 / total)
        space = d.textlength(" ", font=f) * 1.7
        widths = [d.textlength(p_, font=f) for p_ in parts]
        total = sum(widths) + space * (len(parts) - 1)
    y = H * (spec.get("caption_y", 0.745 if fmt == "short" else 0.84))
    x = W / 2 - total / 2
    for (w, ws, we), txt, tw in zip(cur, parts, widths):
        active = ws <= local < we + 0.02
        key = w.lower().strip(PUNCT)
        colr = (255, 212, 0) if active else ((120, 230, 255) if key in hl else (255, 255, 255))
        d.text((x, y), txt, font=f, fill=colr, stroke_width=int(10 * s), stroke_fill=(15, 15, 15))
        x += tw + space


def render_frame(spec, scenes, t, W, H, s, fmt, base_dir, shakes):
    sc_i = next((i for i, sc in enumerate(scenes) if t < sc["_end"]), len(scenes) - 1)
    sc = scenes[sc_i]
    local = t - sc["_start"]
    doku_style = spec.get("style") == "doku"
    if doku_style:
        pal = {"bg": (0, 0, 0), "ink": (245, 240, 230), "soft": (200, 200, 200)}
        img = Image.new("RGB", (W, H), (8, 8, 10))
        photos = [e for e in sc.get("visual", []) if e["type"] == "photo" and e["_at"] <= local]
        for ph in photos:
            ph["_t"] = t
            ph["_handheld"] = ph.get("handheld", sc.get("handheld", spec.get("handheld", 0.7)))
        def shot(ph):
            st = max(0.0, ph["_at"])
            lay = Image.new("RGB", (W, H), (8, 8, 10))
            doku.draw_photo(lay, ph, W, H, local - st, sc["_end"] - sc["_start"] - st + 0.4, base_dir)
            if "_reveal" in ph:   # unscharf bis zum Schlüsselwort -> Neugier
                q = (local - ph["_reveal"]) / 0.45
                if q < 1:
                    lay = doku.blur_fast(lay, 26 * s * (1 - max(0, q)) ** 2)
                    if q < 0:
                        lay = Image.blend(lay, Image.new("RGB", (W, H), (0, 0, 0)), 0.35)
            return lay
        if photos:
            cur = photos[-1]
            img = shot(cur)
            if len(photos) > 1 and cur["_at"] >= 0:
                q = (local - cur["_at"]) / 0.32
                if q < 1:
                    prev = shot(photos[-2])
                    enter = cur.get("enter", "fade")
                    if enter == "slide":
                        img = doku.whip(prev, img, q)
                    elif enter == "zoom":
                        pz = prev.resize((W, H), Image.BILINEAR, box=(W * q * 0.12, H * q * 0.12, W * (1 - q * 0.12), H * (1 - q * 0.12)))
                        img = Image.blend(doku.zoom_blur(pz, 0.1), doku.zoom_blur(img, 0.1 * (1 - q)), doku.ease(q))
                    elif enter != "cut":
                        img = Image.blend(prev, img, doku.ease(q))
    else:
        pal_name = sc.get("bg", spec.get("bg", "sky"))
        pal = palette(pal_name)
        img = background_any(pal_name, W, H).copy()
        cartoon.draw_clouds(img, pal_name, W, H, t)
    d = ImageDraw.Draw(img)
    boil = int(t * FPS) // 3
    for j, el in enumerate(sc.get("visual", [])):
        at = el["_at"]
        if el["type"] in ("photo", "emoji", "count") or local < at or ("until" in el and local > float(el["until"])):
            continue
        p = 1.0 if at < 0 else min(1.0, (local - at) / 0.28)
        k = (ease_out_back(p) if not doku_style else p) if p < 1 else 1.0
        rng = random.Random(sc_i * 100003 + boil * 131 + j)
        pen = doodle.Pen(d, rng, s, pal["ink"])
        pen.img = img
        if el["type"] in ("figure", "person") and "role" not in el:
            el["role"] = next((r for p_, r in ROLE_BY_PROP if p_ in el.get("props", [])), "citizen")
        el["_talking"] = bool(el.get("talk")) and local < sc["_vdur"]
        el["_since"] = local - max(0.0, at) if at >= 0 else local + 1.0
        fn = drawer(el)
        if el["type"] == "image":
            fn(pen, el, W, H, k, t, pal, base_dir=base_dir)
        else:
            fn(pen, el, W, H, k, t, pal)
    # Kamera
    cam = sc.get("camera", "none" if doku_style else "in")
    dur = sc["_end"] - sc["_start"]
    prog = min(1, max(0, local / max(0.1, dur)))
    z = {"in": 1 + 0.07 * prog, "out": 1.07 - 0.07 * prog, "none": 1.0}.get(cam, 1.0)
    fx, fy = sc.get("focus", [0.5, 0.5])
    # Mini-Schnitte: alle ~1.8 s abwechselnd Totale und Nahaufnahme des zuletzt erschienenen Elements
    if sc.get("cuts", spec.get("cuts", fmt == "short" and not doku_style)) and cam != "none":
        seg = int(local / 1.8)
        if seg % 2 == 1:
            shown = [e for e in sc.get("visual", []) if e["_at"] <= local and "x" in e and e["type"] not in ("sticker", "text")]
            if shown:
                tgt = max(shown, key=lambda e: e["_at"])
                fx, fy = tgt["x"], tgt.get("y", 0.5) - (0.12 if tgt["type"] in ("figure", "person") else 0)
                z *= 1.16
    ox = oy = 0.0
    shake_amp = 12 if doku_style else 22
    for st in shakes:
        if 0 <= t - st < 0.4:
            a = (1 - (t - st) / 0.4) ** 2 * shake_amp * s
            rr = random.Random(int(t * FPS))
            ox, oy = rr.uniform(-a, a), rr.uniform(-a, a)
            z = max(z, 1.03)
    punch = 0.0
    if doku_style and sc.get("hit", False) and local < 0.45:   # Punch-In: Bild knallt rein
        punch = (1 - local / 0.45) ** 3 * (0.16 if sc_i == 0 else 0.10)
        z *= 1 + punch
    for kt in spec.get("_kicks", []):                           # Bild pulsiert mit dem Beat
        if 0 <= t - kt < 0.25:
            z *= 1 + spec.get("beat_bump", 0.012) * math.exp(-(t - kt) / 0.07)
            break
    if z != 1.0 or ox or oy:
        cw, ch = W / z, H / z
        cx = min(max(fx * W + ox, cw / 2), W - cw / 2)
        cy = min(max(fy * H + oy, ch / 2), H - ch / 2)
        img = img.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    if doku_style:
        img = doku.grade(img, t, spec.get("grade", 1.0), flicker=spec.get("flicker", 0.025),
                         mood=sc.get("mood", spec.get("mood", "cinematic")), bloom=spec.get("bloom", 0.35))
        if punch > 0.01:
            img = doku.zoom_blur(img, punch * 0.6)
            img = doku.chroma(img, punch * 70 * s)
        leak = spec.get("leaks", 0.0) * max(0.0, 1 - local / 0.8) if sc_i > 0 else 0.0
        if sc.get("transition") == "burn":
            leak = max(leak, math.sin(math.pi * min(1, local / 0.9)) * 0.9)
        img = doku.light_leak(img, leak, t)
        if sc.get("transition") == "flash" and local < 0.3:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 250, 240)), 1 - local / 0.3)
    # Emojis und Zähler NACH der Farbkorrektur: sie sollen knallen, nicht im Look untergehen
    pops = [e for e in sc.get("visual", []) if e["type"] in ("emoji", "count") and local >= e["_at"]]
    if pops:
        pen = doodle.Pen(ImageDraw.Draw(img), random.Random(0), s, (255, 255, 255))
        pen.img = img
        for el in pops:
            el["_since"] = local - max(0.0, el["_at"]) if el["_at"] >= 0 else local + 1.0
            doku.DRAWERS[el["type"]](pen, el, W, H, 1.0, t, None)
    draw_captions(img, sc, local, W, H, s, fmt, spec)
    return img


# ------------------------------------------------------------------ Ausgaben

def fmt_ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60)
    sec = x % 60
    return f"{h:02d}:{m:02d}:{int(sec):02d},{int((sec % 1) * 1000):03d}"


def write_srt(scenes, path, spec):
    n, out = 1, []
    for sc in scenes:
        for ch in chunk_words(sc["_words"], spec.get("caption_words", 3) + 3, 40):
            a, b = sc["_start"] + ch[0][1], sc["_start"] + ch[-1][2]
            out.append(f"{n}\n{fmt_ts(a)} --> {fmt_ts(b)}\n{' '.join(w[0] for w in ch)}\n")
            n += 1
    open(path, "w", encoding="utf-8").write("\n".join(out))


def write_docs(spec, scenes, out_dir, total):
    meta = spec.get("meta", {})
    lines = [f"# {spec.get('title', 'Video')}\n", f"Länge: {total:.1f} s · Format: {spec.get('format', 'short')}\n"]
    if meta.get("titles"):
        lines.append("## Titel-Optionen\n" + "\n".join(f"- {t}" for t in meta["titles"]) + "\n")
    if meta.get("description"):
        lines.append("## Beschreibung (zum Kopieren)\n```\n" + meta["description"].strip())
        if meta.get("sources"):
            lines.append("\nQuellen:\n" + "\n".join(f"- {q}" for q in meta["sources"]))
        credits = []
        used = {el.get("src") for sc in scenes for el in sc.get("visual", []) if el.get("type") == "photo"}
        for src in sorted(x for x in used if x):
            mp = os.path.join(os.path.dirname(out_dir), src + ".json")
            if os.path.exists(mp):
                m = json.load(open(mp, encoding="utf-8"))
                credits.append(f"- {m['title'][5:]} – {m['artist'] or 'unbekannt'} – {m['license']} – {m['page']}")
        if credits:
            lines.append("\nBildnachweise (Wikimedia Commons):\n" + "\n".join(credits))
        lines.append("```\n")
    if meta.get("pinned_comment"):
        lines.append("## Angehefteter Kommentar\n" + meta["pinned_comment"] + "\n")
    if meta.get("tags"):
        lines.append("## Tags\n" + ", ".join(meta["tags"]) + "\n")
    if meta.get("notes"):
        lines.append("## Hinweise\n" + meta["notes"].strip() + "\n")
    lines.append("## Stimme je Szene\n" + "\n".join(
        f"- Szene {i + 1}: {sc.get('_voice_src', '-')}" for i, sc in enumerate(scenes)) + "\n")
    open(os.path.join(out_dir, "upload.md"), "w", encoding="utf-8").write("\n".join(lines))

    rec = ["# Aufnahme-Skript\n",
           "Sprich jede Szene einzeln ein und speichere sie als `aufnahme/szene_XX.wav` im Videoordner.",
           "Danach `render.py` erneut ausführen – deine Stimme ersetzt automatisch die Computerstimme.\n",
           "Tipps: ruhiger Raum, Handy/Mikro 15–20 cm vom Mund, lebendig erzählen wie einem Freund.\n"]
    for i, sc in enumerate(scenes):
        rec.append(f"**Szene {i + 1}** → `szene_{i + 1:02d}.wav` (ca. {sc['_vdur']:.1f} s)\n> {sc['text']}\n")
    open(os.path.join(out_dir, "aufnahme-skript.md"), "w", encoding="utf-8").write("\n".join(rec))

def lufs(x):
    """Integrierte Lautheit (EBU R128) eines Signals über ffmpeg."""
    if not np.any(np.abs(x) > 1e-4):
        return -70.0
    raw = (np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", "ebur128", "-f", "null", "-"], input=raw, capture_output=True)
    txt = r.stderr.decode(errors="ignore")
    try:
        return float(txt.split("Summary:")[1].split("I:")[1].split("LUFS")[0])
    except Exception:
        return -70.0


def type_ticks():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(12)
    return (np.sin(2 * np.pi * 1800 * t) * 0.4 + rng.standard_normal(n) * 0.5) * np.exp(-t * 160)


def make_music(spec, scenes, total, build_dir, music):
    """Gibt (Musik-Signal mit RMS ~1, Metadaten) zurück; nutzt Cache in .build/."""
    key = score_music.cache_key(scenes, total, music)
    mpath = os.path.join(build_dir, f"score_{music['score']}_{key}.wav")
    meta = {}
    if music["score"] == "epoche":
        if not os.path.exists(mpath):
            print(f"  komponiere Epochen-Musik ({music.get('era', 'barock')}) …", flush=True)
            epochen.compose(scenes, total, music, mpath)
        meta = json.load(open(os.path.splitext(mpath)[0] + ".json"))
    elif music["score"] in beats.SCORES:
        if not os.path.exists(mpath):
            print(f"  komponiere Trend-Musik ({music['score']}) …", flush=True)
            beats.compose(scenes, total, music, mpath)
        mj = os.path.splitext(mpath)[0] + ".json"
        if os.path.exists(mj):
            meta = json.load(open(mj))
    else:
        if not os.path.exists(mpath):
            print("  komponiere Filmmusik …", flush=True)
            score_music.compose(scenes, total, music, mpath)
    return ffmpeg_to_mono(mpath), meta


def mix_audio(spec, scenes, total, base_dir, build_dir, wav_path, music_override="__spec__"):
    n = int(total * SR) + SR
    voice = np.zeros(n)
    fx = np.zeros(n)
    doku_style = spec.get("style") == "doku"
    for i, sc in enumerate(scenes):
        add(voice, sc["_audio"], sc["_start"], 1.0)
        tr = sc.get("transition")
        if i > 0 and spec.get("sfx", True):
            g = 0.22 if tr in ("whip", "zoom") else (0.06 if doku_style else 0.18)
            add(fx, sfx("whoosh"), sc["_start"] - 0.12, g)
        if sc.get("hit"):
            add(fx, sfx("hit"), sc["_start"], 0.5)
        if sc.get("heartbeat"):
            for b in np.arange(0, sc["_end"] - sc["_start"], 1.0):
                add(fx, sfx("heartbeat"), sc["_start"] + b, 0.35)
        for el in sc.get("visual", []):
            at = max(0.0, el["_at"])
            if el["type"] == "stamp":
                add(fx, sfx("boom"), sc["_start"] + at, 0.55)
                continue
            if el["type"] == "emoji":
                add(fx, sfx("pop"), sc["_start"] + at, 0.14)
                continue
            if el["type"] == "count":
                for c in range(0, 12):
                    add(fx, type_ticks(), sc["_start"] + at + c * el.get("run", 0.9) / 12, 0.08)
                add(fx, sfx("ding"), sc["_start"] + at + el.get("run", 0.9), 0.18)
                continue
            if el["type"] == "dialog":
                add(fx, sfx("pop"), sc["_start"] + at, 0.12)
                for c in range(0, len(el["text"]), 3):
                    add(fx, type_ticks(), sc["_start"] + at + 0.15 + c * doku.DIALOG_SPEED, 0.05)
                if el.get("emotion") in ("angry", "fear"):
                    add(fx, sfx("hit"), sc["_start"] + at, 0.25)
                continue
            if el["type"] == "photo" and el.get("enter") in ("slide", "zoom") and el["_at"] > 0:
                add(fx, sfx("whoosh"), sc["_start"] + at - 0.1, 0.12)
                continue
            if el["type"] == "date" and el.get("typewriter", True) and el["_at"] >= 0:
                for c in range(len(el["text"])):
                    if el["text"][c] != " ":
                        add(fx, type_ticks(), sc["_start"] + at + c * doku.TYPE_SPEED, 0.12)
                continue
            kind = el.get("sfx", None if doku_style else "pop")
            if kind and el["_at"] > 0.05 and spec.get("sfx", True):
                add(fx, sfx(kind), sc["_start"] + el["_at"], 0.22 if kind == "pop" else 0.45)
    music = spec.get("music") if music_override == "__spec__" else music_override
    mus = np.zeros(n)
    if isinstance(music, dict) and music.get("score"):
        m, meta = make_music(spec, scenes, total, build_dir, music)
        spec["_kicks"] = meta.get("kicks", []) if music_override == "__spec__" else spec.get("_kicks", [])
        mus[: min(n, len(m))] = m[:n]
        # Lautstärke relativ zur Stimme (in LU): music_db = wie viele dB die Musik unter der Stimme liegt
        v_l, m_l = lufs(voice), lufs(mus[: int(total * SR)])
        gain_db = (v_l - spec.get("music_db", 21.0)) - m_l
        mus *= 10 ** (gain_db / 20)
        # Ducking: Musik wird leiser, wenn gesprochen wird
        win = int(0.35 * SR)
        env = np.convolve(np.abs(voice), np.ones(win) / win, mode="same")
        act = np.clip(env / 0.03, 0, 1)
        act = np.convolve(act, np.ones(int(0.5 * SR)) / int(0.5 * SR), mode="same")
        mus *= 1 - spec.get("duck", 0.5) * act
        fade = np.minimum(1, (total - np.arange(n) / SR) / 2.0).clip(0, 1)
        mus *= fade
        print(f"  Lautheit: Stimme {v_l:.1f} LUFS, Musik {m_l + gain_db:.1f} LUFS "
              f"({spec.get('music_db', 21.0):.0f} dB darunter, beim Sprechen weitere "
              f"{-20 * np.log10(1 - spec.get('duck', 0.45)):.1f} dB)", flush=True)
    elif music:
        if isinstance(music, str) and os.path.exists(os.path.join(base_dir, music)):
            m = ffmpeg_to_mono(os.path.join(base_dir, music))
            reps = int(np.ceil(n / len(m)))
            mus = np.tile(m, reps)[:n] * spec.get("music_volume", 0.12)
        else:
            pad = ambient_pad(total, music if isinstance(music, str) else "mystery")
            mus[: len(pad)] = pad * spec.get("music_volume", 0.06)
    mix = voice + fx + mus
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.95)
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((mix[: int(total * SR)] * 32767).astype(np.int16).tobytes())
    return wav_path


def remux(video_in, wav_path, out_path, build_dir):
    tmp = os.path.join(build_dir, "remux.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video_in, "-i", wav_path, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out_path)


def make_variants(spec, scenes, total, base_dir, build_dir, out_dir):
    out_mp4 = os.path.join(out_dir, "video.mp4")
    w0 = os.path.join(build_dir, "mix_ohne_musik.wav")
    mix_audio(spec, scenes, total, base_dir, build_dir, w0, music_override=None)
    remux(out_mp4, w0, os.path.join(out_dir, "video_ohne_musik.mp4"), build_dir)
    print("Variante:", os.path.join(out_dir, "video_ohne_musik.mp4"))
    m = spec.get("music")
    if isinstance(m, dict) and m.get("score") in beats.SCORES:
        other = "trailer" if m["score"] == "phonk" else "phonk"
        alt = {"score": other, "key": m.get("key", "D")}
        w1 = os.path.join(build_dir, f"mix_{other}.wav")
        mix_audio(spec, scenes, total, base_dir, build_dir, w1, music_override=alt)
        remux(out_mp4, w1, os.path.join(out_dir, f"video_{other}.mp4"), build_dir)
        print("Variante:", os.path.join(out_dir, f"video_{other}.mp4"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--stills", action="store_true", help="nur ein Vorschaubild pro Szene")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--audio-only", action="store_true", help="nur Ton neu mischen, Bild aus output/video.mp4 übernehmen")
    ap.add_argument("--variants", action="store_true",
                    help="zusätzlich video_ohne_musik.mp4 (für Trend-Sounds in der App) und die zweite Trend-Musik")
    args = ap.parse_args()

    spec_path = os.path.abspath(args.spec)
    base_dir = os.path.dirname(spec_path)
    spec = yaml.safe_load(open(spec_path, encoding="utf-8"))
    fmt = spec.get("format", "short")
    W, H = SIZES[fmt]
    W, H = int(W * args.scale) // 2 * 2, int(H * args.scale) // 2 * 2
    s = min(W, H) / 1080
    out_dir = os.path.join(base_dir, "output")
    build_dir = os.path.join(base_dir, ".build")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    scenes = spec["scenes"]
    total = build_timeline(spec, base_dir, build_dir)
    shakes = [sc["_start"] + max(0, el["_at"]) for sc in scenes for el in sc.get("visual", [])
              if el.get("shake") or el["type"] == "stamp"]
    shakes += [sc["_start"] for sc in scenes if sc.get("hit")]

    if args.stills:
        frames = []
        for sc in scenes:
            t = sc["_start"] + min(sc["_vdur"] * 0.85, max(el["_at"] for el in sc.get("visual", [{"_at": 0}])) + 0.5)
            frames.append(render_frame(spec, scenes, t, W, H, s, fmt, base_dir, []))
        cols = min(5, len(frames))
        rows = math.ceil(len(frames) / cols)
        tw, th = W // 3, H // 3
        sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
        for i, fr in enumerate(frames):
            sheet.paste(fr.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        p = os.path.join(out_dir, "vorschau.jpg")
        sheet.save(p, quality=85)
        print(p)
        return

    wav_path = os.path.join(build_dir, "mix.wav")
    mix_audio(spec, scenes, total, base_dir, build_dir, wav_path)

    # Video
    out_mp4 = os.path.join(out_dir, "video.mp4")
    if args.audio_only and os.path.exists(out_mp4):
        remux(out_mp4, wav_path, out_mp4, build_dir)
        write_docs(spec, scenes, out_dir, total)
        print("Ton neu gemischt:", out_mp4)
        if args.variants:
            make_variants(spec, scenes, total, base_dir, build_dir, out_dir)
        return
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav_path, "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "8M",
           "-bufsize", "16M", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", out_mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    thumb_t = spec.get("meta", {}).get("thumbnail_time", 0.0)
    last_of = {}
    xfade = spec.get("crossfade", 0.4 if spec.get("style") == "doku" else 0.0)
    for fi in range(nframes):
        t = fi / FPS
        fr = render_frame(spec, scenes, t, W, H, s, fmt, base_dir, shakes)
        si = next((i for i, sc in enumerate(scenes) if t < sc["_end"]), len(scenes) - 1)
        loc = t - scenes[si]["_start"]
        trn = scenes[si].get("transition", "fade")
        prev = last_of.get(si - 1)
        if si > 0 and prev is not None and trn == "whip" and loc < 0.24:
            fr = doku.whip(prev, fr, loc / 0.24)
        elif si > 0 and prev is not None and trn == "zoom" and loc < 0.3:
            p = loc / 0.3
            pz = doku.zoom_blur(prev.resize((W, H), Image.BILINEAR, box=(W * p * 0.15, H * p * 0.15,
                                                                         W * (1 - p * 0.15), H * (1 - p * 0.15))), 0.12)
            fr = Image.blend(pz, doku.zoom_blur(fr, 0.12 * (1 - p)), doku.ease(p))
        elif xfade and si > 0 and prev is not None and loc < xfade and trn in ("fade", "burn"):
            fr = Image.blend(prev, fr, loc / xfade)
        else:
            last_of[si] = fr
        if abs(t - thumb_t) < 0.5 / FPS:
            fr.save(os.path.join(out_dir, "thumbnail.jpg"), quality=92)
        proc.stdin.write(fr.tobytes())
        if fi % (FPS * 10) == 0:
            print(f"  {t:5.1f}s / {total:.1f}s", flush=True)
    proc.stdin.close()
    proc.wait()
    write_srt(scenes, os.path.join(out_dir, "untertitel.srt"), spec)
    write_docs(spec, scenes, out_dir, total)
    print("fertig:", out_mp4, f"({total:.1f}s)")
    if args.variants:
        make_variants(spec, scenes, total, base_dir, build_dir, out_dir)


if __name__ == "__main__":
    main()
