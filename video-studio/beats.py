"""Trend-Musik für Shorts: Dark Phonk und Trailer-Spannung, komplett selbst komponiert und synthetisiert.

Warum selbst gebaut: echte Trend-Songs (z. B. bekannte Phonk-Tracks) lösen Content-ID aus und
teilen die Shorts-Einnahmen mit dem Rechteinhaber. Diese Musik klingt nach dem Trend, gehört aber uns.
Echte Trend-Sounds lieber direkt in der YouTube/TikTok/Instagram-App beim Hochladen hinzufügen
(dafür rendert render.py mit --variants auch eine Fassung ohne Musik).

Scores (in video.yaml):
  music: {score: phonk, tempo: 120, key: D}      Dark Phonk: Cowbell-Riff, 808 mit Slides, Clap, Hi-Hat-Rolls
  music: {score: trailer, tempo: 96, key: D}     Trailer/Doku-Spannung: Ticking, Puls, Braams, Taikos, Riser

Die Musik folgt dem Video:
  - Intro (Szene 0 = Hook): nur Riff/Puls, Impact auf Bild 1
  - Drop genau auf Szene `drop_scene` (Standard 1, also direkt nach dem Hook)
  - `hit: true`  -> Beat setzt einen Schlag vorher aus, Reverse-Swell, Impact, Re-Drop
  - `heartbeat`  -> nur Kick + 808 (Spannung)
  - letzte Szene -> Outro ohne Drums, ausklingen
"""
import json
import os
import subprocess
import tempfile
import wave

import numpy as np

import music as orch

SR = 44100
NOTE = orch.NOTE


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env_exp(n, decay, attack=0.002):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def band(x, lo=None, hi=None):
    """FFT-Bandpass für kurze One-Shots."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def lowpass_sweep(x, f0, f1):
    """Grober Filter-Sweep: blockweise FFT-Tiefpass (für Intros/Outros)."""
    out = np.zeros_like(x)
    blk = 4096
    nb = max(1, len(x) // blk + 1)
    for i in range(nb):
        seg = x[i * blk:(i + 1) * blk]
        if not len(seg):
            break
        fc = f0 * (f1 / f0) ** (i / max(1, nb - 1))
        out[i * blk:i * blk + len(seg)] = band(np.pad(seg, (0, blk - len(seg))), hi=fc)[:len(seg)]
    return out


RNG = np.random.default_rng(7)


# ------------------------------------------------------------------ One-Shots

def kick(drive=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 120 * np.exp(-t / 0.035)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    x[:200] += np.linspace(0.6, 0, 200) * RNG.standard_normal(200)  # Klick
    return np.tanh(x * 1.6 * drive) * 0.9


def sub808(midi, dur, glide_from=None, drive=2.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.full(n, hz(midi))
    if glide_from is not None:
        g = np.clip(t / 0.09, 0, 1)
        f = hz(glide_from) + (hz(midi) - hz(glide_from)) * (1 - (1 - g) ** 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.15 * np.sin(2 * ph)
    e = env_exp(n, 0.9, 0.004) * np.clip((dur - t) / 0.03, 0, 1)
    return np.tanh(x * drive) * e * 0.75


def clap():
    n = int(0.35 * SR)
    x = RNG.standard_normal(n)
    e = np.zeros(n)
    for off in (0.0, 0.011, 0.022):
        i = int(off * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR / (0.007 if off < 0.02 else 0.12))
    return band(x * e, 900, 3500) * 0.9


def snare():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    nz = band(RNG.standard_normal(n), 1500, 9000) * np.exp(-t / 0.09)
    return (0.6 * body + 0.9 * nz) * 0.8


def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    x = band(RNG.standard_normal(n), 7000, None)
    return x * env_exp(n, 0.09 if open_ else 0.018) * 0.55


def cowbell(midi, dur=0.32):
    """Phonk-Cowbell: zwei Rechteckwellen im 808-Verhältnis, Bandpass, leicht verzerrt."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f1 = hz(midi)
    x = np.sign(np.sin(2 * np.pi * f1 * t)) + 0.8 * np.sign(np.sin(2 * np.pi * f1 * 1.4815 * t))
    x = band(x, f1 * 0.9, f1 * 3.2)
    e = np.exp(-t / 0.05) * 0.6 + np.exp(-t / 0.22) * 0.4
    return np.tanh(x * e * 2.2) * 0.45


def taiko():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 62 + 50 * np.exp(-t / 0.04)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28)
    skin = band(RNG.standard_normal(n), 200, 1200) * np.exp(-t / 0.05)
    return np.tanh((body + 0.5 * skin) * 1.8) * 0.9


def tick():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return band(RNG.standard_normal(n), 3000, 9000) * np.exp(-t / 0.004) * 0.7


def impact():
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7)
    crack = band(RNG.standard_normal(n), 80, 6000) * np.exp(-t / 0.12)
    return np.tanh((boom * 1.4 + 0.7 * crack) * 1.5) * 0.95


def reverse_swell(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = band(RNG.standard_normal(n), 300, 9000)
    return x * (t / dur) ** 3 * 0.6


def riser(dur=2.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 200 * (8 ** (t / dur))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    nz = lowpass_sweep(RNG.standard_normal(n), 400, 12000) * 0.5
    return (tone + nz) * (t / dur) ** 2


def saw(midi, dur, harm=9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = sum(((-1) ** (k + 1)) * np.sin(2 * np.pi * k * f * t * (1 + 0.0007 * k)) / k for k in range(1, harm + 1))
    return x * 0.5


def reverb(x, seconds=2.2, wet=0.3, predelay=0.02):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = RNG.standard_normal(n) * np.exp(-t / (seconds / 6.9))
    ir = band(ir, 200, 7000)
    ir = np.concatenate([np.zeros(int(predelay * SR)), ir])
    ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + len(ir)
    nfft = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x)]
    return x * (1 - wet) + y * wet * 1.2


def place(track, clip, at, gain=1.0):
    i = int(round(at * SR))
    if i >= len(track) or i + len(clip) <= 0:
        return
    if i < 0:
        clip, i = clip[-i:], 0
    m = min(len(clip), len(track) - i)
    track[i:i + m] += clip[:m] * gain


# ------------------------------------------------------------------ Struktur aus den Szenen

def sections(scenes, total, cfg, beat):
    drop_i = min(cfg.get("drop_scene", 1), len(scenes) - 1)
    t_drop = scenes[drop_i]["_start"] if len(scenes) > 1 else 0.0
    t_out = scenes[-1]["_start"] if len(scenes) > 2 else total
    hits = [sc["_start"] for i, sc in enumerate(scenes) if sc.get("hit") and i != drop_i]
    pulses = [(sc["_start"], sc["_end"]) for sc in scenes if sc.get("heartbeat")]

    def state(t):
        if t < t_drop:
            return "intro"
        if t >= t_out:
            return "outro"
        if any(h - beat <= t < h for h in hits):
            return "gap"
        if any(a <= t < e for a, e in pulses):
            return "tense"
        return "full"
    return t_drop, t_out, hits, state


# Riff in 16teln über 2 Takte: (Schritt, Tonstufe in Halbtönen über dem Grundton, Länge in 16teln)
PHONK_RIFF = [(0, 12, 2), (3, 15, 1), (4, 13, 2), (6, 12, 2), (8, 10, 1), (10, 12, 2), (12, 8, 2), (14, 7, 2),
              (16, 12, 2), (19, 15, 1), (20, 17, 2), (22, 15, 2), (24, 13, 1), (26, 12, 2), (28, 10, 2), (30, 13, 2)]
# 808-Linie (Schritt, Stufe, Länge, Slide von Stufe)
PHONK_BASS = [(0, 0, 6, None), (6, 0, 2, None), (8, 1, 4, 0), (12, -2, 4, None),
              (16, 0, 6, None), (22, 0, 2, None), (24, 3, 4, 0), (28, 1, 4, 3)]
PHONK_KICK = [0, 6, 10, 16, 22, 26]
PHONK_CLAP = [8, 24]


def compose_phonk(scenes, total, cfg):
    tempo = cfg.get("tempo", 120)
    root = 12 * 3 + NOTE[cfg.get("key", "D")] + 12   # D3 = 50
    beat = 60.0 / tempo
    st16 = beat / 4
    n = int((total + 3) * SR)
    drums, bass, bell, fx = (np.zeros(n) for _ in range(4))
    t_drop, t_out, hits, state = sections(scenes, total, cfg, beat)
    kicks = []
    bar2 = 32 * st16
    # Raster am Drop ausgerichtet, rückwärts bis 0 verlängert
    k0 = -int(np.ceil(t_drop / bar2))
    k = k0
    while k * bar2 + t_drop < total + 1:
        b0 = t_drop + k * bar2
        for step in range(32):
            t = b0 + step * st16
            if t < 0 or t >= total + 0.5:
                continue
            s = state(t)
            if s in ("full", "tense") and step in PHONK_KICK:
                place(drums, kick(), t, 0.95)
                kicks.append(round(t, 3))
            if s == "full" and step in PHONK_CLAP:
                place(drums, clap(), t, 0.7)
                place(drums, snare(), t, 0.25)
            if s == "full":
                if step % 2 == 0:
                    place(drums, hat(), t, 0.35 if step % 4 else 0.5)
                if step in (14, 30):  # Triolen-Roll
                    for r in range(3):
                        place(drums, hat(), t + r * st16 * 2 / 3, 0.3)
                if step == 31:
                    place(drums, hat(True), t, 0.25)
        for step, deg, ln, slide in PHONK_BASS:
            t = b0 + step * st16
            if 0 <= t < total and state(t) in ("full", "tense"):
                place(bass, sub808(root - 12 + deg, ln * st16 * 0.98, None if slide is None else root - 12 + slide), t, 0.8)
        for step, deg, ln in PHONK_RIFF:
            t = b0 + step * st16
            if 0 <= t < total + 0.5 and state(t) != "gap":
                g = 0.55 if state(t) in ("intro", "outro", "tense") else 0.75
                place(bell, cowbell(root + deg + 12, ln * st16 + 0.15), t, g)
        k += 1
    # Impacts: Bild 1, Drop, jeder Hit
    for h in [0.0, t_drop] + hits:
        place(fx, impact(), h, 0.8)
        if h > 0.5:
            place(fx, reverse_swell(min(0.9, h)), h - min(0.9, h), 0.5)
    if t_drop > 2.2:
        place(fx, riser(2.0), t_drop - 2.0, 0.35)
    # Pad (Chor/Streicher, Fluidsynth) für die dunkle Atmosphäre
    pad = pad_layer(scenes, total, cfg, "phonk")
    # Sidechain: Pad und Glocke pumpen mit der Kick
    sc_env = np.ones(n)
    for kt in kicks:
        i = int(kt * SR)
        m = min(int(0.25 * SR), n - i)
        if m > 0:
            sc_env[i:i + m] = np.minimum(sc_env[i:i + m], 1 - 0.55 * np.exp(-np.arange(m) / SR / 0.08))
    bell = reverb(bell, 2.6, 0.35)
    tt = np.arange(n) / SR
    intro_filter = np.clip((tt - 0) / max(0.5, t_drop), 0, 1)
    bell_intro = lowpass_sweep(bell, 900, 9000)
    bell = np.where(tt < t_drop, bell_intro * (0.6 + 0.4 * intro_filter), bell)
    mix = drums * 0.9 + bass * 0.9 + bell * sc_env * 0.75 + fx * 0.6
    if pad is not None:
        mix[:len(pad)] += pad[:n] * sc_env[:len(pad)] * 0.55
    return finish(mix, total, t_out), {"kicks": kicks, "drop": t_drop, "beat": beat}


def compose_trailer(scenes, total, cfg):
    tempo = cfg.get("tempo", 96)
    root = 12 * 3 + NOTE[cfg.get("key", "D")]   # D2 = 38
    beat = 60.0 / tempo
    n = int((total + 3) * SR)
    perc, pulse, fx = (np.zeros(n) for _ in range(3))
    t_drop, t_out, hits, state = sections(scenes, total, cfg, beat)
    prog = [0, -4, -2, -5]   # i - VI - VII - v (moll)
    kicks = []
    bar = 4 * beat
    k = -int(np.ceil(t_drop / bar))
    while t_drop + k * bar < total + 1:
        b0 = t_drop + k * bar
        deg = prog[k % len(prog)]
        for e in range(8):
            t = b0 + e * beat / 2
            if t < 0 or t >= total + 0.3:
                continue
            s = state(t)
            if s != "gap":
                g = 0.35 if s in ("intro", "outro") else (0.6 if s == "tense" else 0.5)
                note = saw(root + 12 + deg + (12 if e % 4 == 2 else 0), beat / 2 * 0.85, 7 if s == "intro" else 11)
                place(pulse, note * env_exp(len(note), 0.12, 0.003), t, g)
            for q in range(2):   # Ticking-Clock in 16teln
                if s in ("intro", "tense", "full"):
                    place(perc, tick(), t + q * beat / 4, 0.18 if q else 0.28)
            if s == "full" and e in (0, 3, 4, 6):
                place(perc, taiko(), t, 0.7 if e == 0 else 0.45)
                kicks.append(round(t, 3))
            if s == "tense" and e in (0, 4):
                place(perc, taiko(), t, 0.6)
                kicks.append(round(t, 3))
        k += 1
    for h in [0.0, t_drop] + hits:
        place(fx, impact(), h, 0.85)
        if h > 0.5:
            place(fx, reverse_swell(min(0.9, h)), h - min(0.9, h), 0.45)
    if t_drop > 2.2:
        place(fx, riser(2.0), t_drop - 2.0, 0.35)
    pad = pad_layer(scenes, total, cfg, "trailer")
    pulse = reverb(pulse, 1.6, 0.25)
    mix = perc * 0.8 + pulse * 0.75 + fx * 0.6
    if pad is not None:
        mix[:len(pad)] += pad[:n] * 0.7
    return finish(mix, total, t_out), {"kicks": kicks, "drop": t_drop, "beat": beat}


def pad_layer(scenes, total, cfg, kind):
    """Dunkler Chor/Streicher-Teppich + Braams auf Hits über Fluidsynth (FluidR3 GM, MIT)."""
    sf2 = orch.find_sf2()
    if not sf2:
        return None
    tempo = cfg.get("tempo", 120 if kind == "phonk" else 96)
    tr = orch.Track(480, tempo)
    rootname = cfg.get("key", "D")
    r = 12 * 4 + NOTE[rootname]  # D3 = 50
    tr.program(0, 52)   # Chor Aahs
    tr.program(1, 48)   # Streicher
    tr.program(2, 61)   # Brass Section (Braam)
    tr.program(3, 0)    # Klavier, tiefe Einzeltöne
    for ch in range(4):
        tr.cc(ch, 91, 110, 0)
        tr.cc(ch, 7, 100, 0)
    chords = [[0, 3, 7], [-4, 0, 3], [-2, 2, 5], [-5, -2, 2]]
    bar = 4 * 60.0 / tempo * (2 if kind == "phonk" else 1)
    t = 0.0
    i = 0
    t_out = scenes[-1]["_start"] if len(scenes) > 2 else total
    while t < total:
        ch = chords[i % 4] if t < t_out else [0, 3, 7]
        d = min(bar, total + 2 - t)
        for p in ch:
            tr.note(0, r + p, t, d, 52)
            tr.note(1, r + p - 12, t, d, 46)
        if i % 2 == 0:
            tr.note(3, r - 24 + ch[0], t, d, 60)
        t += bar
        i += 1
    drop_i = min(cfg.get("drop_scene", 1), len(scenes) - 1)
    for j, sc in enumerate(scenes):
        if sc.get("hit") or j == drop_i:
            h = sc["_start"]
            for p in (r - 24, r - 12, r - 12 + 7):
                tr.note(2, p, h, 2.4, 118)
    with tempfile.TemporaryDirectory() as td:
        mid, wav = os.path.join(td, "p.mid"), os.path.join(td, "p.wav")
        tr.to_midi(tempo, mid)
        subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", str(SR), "-o", "synth.reverb.room-size=0.9",
                        "-o", "synth.reverb.level=0.9", "-F", wav, sf2, mid], check=True, capture_output=True)
        with wave.open(wav) as wf:
            a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
            if wf.getnchannels() == 2:
                a = a.reshape(-1, 2).mean(axis=1)
    return a


def finish(mix, total, t_out):
    n = len(mix)
    t = np.arange(n) / SR
    fade = np.clip((total + 0.8 - t) / max(1.5, total + 0.8 - t_out), 0, 1)
    mix = mix * fade
    mix = np.tanh(mix * 1.2) / 1.2   # weicher Limiter
    return mix / max(1e-6, np.max(np.abs(mix))) * 0.9


SCORES = {"phonk": compose_phonk, "trailer": compose_trailer}


def compose(scenes, total, cfg, out_wav):
    x, meta = SCORES[cfg["score"]](scenes, total, cfg)
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    with open(os.path.splitext(out_wav)[0] + ".json", "w") as f:
        json.dump(meta, f)
    return out_wav, meta
