"""Epochen-Musik: Die Musik passt zum Thema des Videos (Zeit, Ort, Stimmung).

Regel des Nutzers (06.11.2026): Musik, Figuren und Bilder IMMER an das Thema anpassen.
Ein Video über Friedrich den Großen klingt nach Barock (Cembalo, Streicher, Flöte),
eins über Napoleon nach Marsch (Trommel, Trompete), eins über Rom nach Antike (Taikos, Hörner, Chor).

In video.yaml:
  music: {score: epoche, era: barock}            # tempo/key optional
  era:  antike | mittelalter | renaissance | barock | napoleon | viktorianisch | weltkrieg | kalterkrieg | orient

Aufbau wie bei der Trend-Musik: Hook = nur Melodie, voller Einsatz auf Szene `drop_scene` (Standard 1),
Pause vor jedem `hit` mit Impact, bei `heartbeat` nur Bass + Pauke, Ausklang in der letzten Szene.
Instrumente: FluidR3-GM-Soundfont (MIT), eigene Komposition -> kein Content-ID-Risiko.
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

import beats
import music as orch

SR = 44100
DRUM = 9

# Akkordfolgen als (Halbtöne über Grundton, Moll?)
PROG = {
    "barock": [(0, 1), (5, 1), (7, 0), (0, 1), (8, 0), (5, 1), (7, 0), (0, 1)],       # i iv V i VI iv V i
    "moll_epic": [(0, 1), (8, 0), (10, 0), (7, 1)],                                  # i VI VII v
    "march": [(0, 1), (7, 0), (0, 1), (5, 1), (0, 1), (7, 0), (8, 0), (7, 0)],
    "dorisch": [(0, 1), (5, 0), (0, 1), (10, 0)],                                    # i IV i VII
    "lament": [(0, 1), (8, 0), (5, 1), (7, 0)],
}

# Jede Stimme: (Rolle, GM-Programm, Muster, Oktave, Lautstärke, ab Abschnitt)
# Abschnitte: "intro" = schon im Hook, "full" = erst ab dem Drop
PRESETS = {
    "barock": dict(tempo=100, prog="barock", parts=[
        ("lead", 73, "melodie", 5, 82, "intro"),          # Querflöte (Friedrich spielte selbst Flöte)
        ("harm", 6, "arpeggio16", 4, 62, "full"),          # Cembalo
        ("pad", 48, "pad", 4, 50, "intro"),                # Streicher
        ("bass", 42, "walking", 2, 72, "full"),            # Cello/Continuo
        ("timp", 47, "pauke", 2, 88, "full"),
    ]),
    "renaissance": dict(tempo=92, prog="dorisch", parts=[
        ("lead", 74, "melodie", 5, 80, "intro"),           # Blockflöte
        ("harm", 24, "arpeggio8", 4, 60, "full"),          # Laute (Nylon-Gitarre)
        ("pad", 48, "pad", 4, 45, "intro"),
        ("bass", 32, "grundton", 2, 70, "full"),
        ("drum", 0, "rahmentrommel", 0, 70, "full"),
    ]),
    "mittelalter": dict(tempo=84, prog="dorisch", parts=[
        ("lead", 74, "melodie", 5, 80, "intro"),           # Flöte
        ("pad", 52, "pad", 4, 55, "intro"),                # Mönchschor
        ("drone", 19, "bordun", 3, 50, "intro"),           # Kirchenorgel als Bordun
        ("bass", 43, "grundton", 2, 65, "full"),
        ("drum", 0, "rahmentrommel", 0, 78, "full"),
    ]),
    "antike": dict(tempo=90, prog="moll_epic", parts=[
        ("lead", 60, "fanfare", 4, 86, "intro"),           # Horn
        ("pad", 52, "pad", 4, 58, "intro"),                # Chor
        ("bass", 43, "ostinato", 2, 74, "full"),
        ("taiko", 116, "taiko", 2, 100, "full"),           # Kriegstrommeln
        ("brass", 61, "stoss", 3, 80, "full"),
    ]),
    "napoleon": dict(tempo=108, prog="march", parts=[
        ("lead", 56, "fanfare", 5, 84, "intro"),           # Trompete
        ("pad", 48, "pad", 4, 48, "intro"),
        ("bass", 58, "marschbass", 2, 76, "full"),         # Tuba
        ("drum", 0, "marschtrommel", 0, 85, "full"),
        ("timp", 47, "pauke", 2, 80, "full"),
    ]),
    "viktorianisch": dict(tempo=96, prog="lament", parts=[
        ("lead", 8, "arpeggio8", 5, 70, "intro"),          # Celesta (Spieluhr, unheimlich)
        ("pizz", 45, "pizzicato", 4, 70, "full"),
        ("pad", 49, "pad", 4, 42, "intro"),
        ("bass", 43, "grundton", 2, 66, "full"),
        ("drum", 0, "uhr", 0, 60, "intro"),                # Holzblock-Ticken
    ]),
    "weltkrieg": dict(tempo=76, prog="lament", parts=[
        ("lead", 0, "klavier_einzel", 5, 70, "intro"),     # einzelne Klaviertöne
        ("pad", 48, "pad", 4, 52, "intro"),
        ("bass", 42, "ostinato", 2, 66, "full"),
        ("drum", 0, "kriegstrommel", 0, 80, "full"),
        ("brass", 57, "stoss", 3, 70, "full"),             # tiefe Posaune
    ]),
    "kalterkrieg": dict(tempo=88, prog="moll_epic", parts=[
        ("lead", 81, "klavier_einzel", 5, 62, "intro"),    # Synth-Lead, kühl
        ("pad", 89, "pad", 4, 55, "intro"),                # Synth-Pad
        ("bass", 38, "ostinato", 2, 74, "full"),           # Synth-Bass
        ("drum", 0, "uhr", 0, 55, "intro"),
        ("taiko", 116, "taiko", 2, 70, "full"),
    ]),
    "orient": dict(tempo=92, prog="moll_epic", parts=[
        ("lead", 72, "melodie", 5, 80, "intro"),           # Ney-artige Flöte (Klarinette weich)
        ("harm", 15, "arpeggio8", 4, 58, "full"),          # Hackbrett (Dulcimer)
        ("pad", 48, "pad", 4, 45, "intro"),
        ("bass", 43, "grundton", 2, 66, "full"),
        ("drum", 0, "rahmentrommel", 0, 76, "full"),
    ]),
}
HARMONIC_MINOR = [0, 2, 3, 5, 7, 8, 11]
NATURAL_MINOR = [0, 2, 3, 5, 7, 8, 10]
MELODY = [  # Motiv in Tonleiterstufen (0 = Grundton des Akkords), (Stufe, Dauer in Vierteln)
    [(4, 1), (3, 0.5), (2, 0.5), (3, 1), (0, 1)],
    [(2, 0.5), (3, 0.5), (4, 1), (5, 1), (4, 1)],
    [(7, 1.5), (6, 0.5), (4, 1), (2, 1)],
    [(4, 1), (2, 1), (1, 1), (0, 1)],
]


def scale_note(root, step, scale=HARMONIC_MINOR):
    o, i = divmod(step, 7)
    return root + 12 * o + scale[i]


def chord(root, off, minor):
    r = root + off
    return [r, r + (3 if minor else 4), r + 7]


def bar_notes(pattern, ch_notes, t0, beat, oct_shift, vel, bar_i, key_root):
    """Gibt [(Zeit, Tonhöhe, Dauer, Lautstärke)] für einen Takt."""
    r, third, fifth = (n + 12 * oct_shift for n in ch_notes)
    out = []
    if pattern == "pad":
        for n in (r, third, fifth):
            out.append((t0, n, 4 * beat, vel))
    elif pattern == "arpeggio16":
        seq = [r, third, fifth, r + 12, fifth, third] * 3
        for k in range(16):
            out.append((t0 + k * beat / 4, seq[k], beat / 4 * 0.9, vel - (0 if k % 4 == 0 else 10)))
    elif pattern == "arpeggio8":
        seq = [r, fifth, r + 12, third + 12, r + 12, fifth, third, fifth]
        for k in range(8):
            out.append((t0 + k * beat / 2, seq[k], beat / 2 * 0.95, vel - (0 if k % 2 == 0 else 8)))
    elif pattern == "walking":
        seq = [r, r + 12, fifth, r + 12, third, r + 12, fifth - 12 + 12, r + 11]
        for k in range(8):
            out.append((t0 + k * beat / 2, seq[k], beat / 2 * 0.85, vel))
    elif pattern == "grundton":
        out += [(t0, r, 2 * beat, vel), (t0 + 2 * beat, fifth - 12, 2 * beat, vel - 8)]
    elif pattern == "bordun":
        out += [(t0, r, 4 * beat, vel), (t0, fifth, 4 * beat, vel - 8)]
    elif pattern == "ostinato":
        seq = [r, r, r + 12, r, r, fifth, r + 12, r]
        for k in range(8):
            out.append((t0 + k * beat / 2, seq[k], beat / 2 * 0.8, vel + (8 if k % 4 == 0 else 0)))
    elif pattern == "marschbass":
        for k, n in enumerate([r, fifth - 12, r, fifth - 12]):
            out.append((t0 + k * beat, n, beat * 0.7, vel))
    elif pattern == "pizzicato":
        for k, n in enumerate([r, third, fifth, third]):
            out.append((t0 + k * beat, n, beat * 0.3, vel))
    elif pattern == "melodie":
        mot = MELODY[bar_i % len(MELODY)]
        t = t0
        off = (ch_notes[0] - key_root) % 12
        # über dem Dur-Akkord der V. Stufe harmonisch Moll (Leitton), sonst natürlich Moll
        sc = HARMONIC_MINOR if (off == 7 and ch_notes[1] - ch_notes[0] == 4) else NATURAL_MINOR
        deg = sc.index(off) if off in sc else 0
        for st, d in mot:
            n = scale_note(key_root + 12 * oct_shift, deg + st, sc)
            out.append((t, n, d * beat * 0.95, vel))
            t += d * beat
    elif pattern == "fanfare":
        out += [(t0, r, beat * 0.45, vel), (t0 + beat * 0.5, r, beat * 0.2, vel - 10),
                (t0 + beat * 0.75, r, beat * 0.2, vel - 10), (t0 + beat, fifth, beat * 1.4, vel),
                (t0 + beat * 2.5, third, beat * 0.45, vel - 6), (t0 + beat * 3, r + 12, beat * 0.95, vel)]
    elif pattern == "klavier_einzel":
        out += [(t0, fifth + 12, beat * 1.9, vel), (t0 + 2 * beat, third + 12, beat * 1.9, vel - 10)]
    elif pattern == "stoss":
        out += [(t0, r, beat * 0.9, vel), (t0, fifth, beat * 0.9, vel - 10)]
    elif pattern == "pauke":
        out += [(t0, r, beat * 0.9, vel), (t0 + 2 * beat, fifth - 12, beat * 0.9, vel - 12)]
    elif pattern == "taiko":
        for k, a in enumerate([1, 0, 0.6, 0, 1, 0.5, 0.7, 0.5]):
            if a:
                out.append((t0 + k * beat / 2, 50, beat / 2, int(vel * a)))
    return out


DRUM_PATTERNS = {   # (16tel-Schritt, GM-Drum-Note, Lautstärke)
    "marschtrommel": [(0, 38, 100), (2, 38, 60), (3, 38, 60), (4, 38, 90), (6, 38, 60), (8, 38, 100), (10, 38, 60),
                      (11, 38, 60), (12, 38, 90), (13, 38, 55), (14, 38, 65), (15, 38, 75), (0, 36, 90), (8, 36, 80)],
    "rahmentrommel": [(0, 41, 100), (6, 41, 70), (8, 43, 85), (12, 54, 55), (14, 41, 60)],
    "kriegstrommel": [(0, 41, 110), (3, 41, 70), (8, 41, 100), (14, 38, 50)],
    "uhr": [(0, 76, 70), (4, 77, 55), (8, 76, 70), (12, 77, 55)],
}


def compose(scenes, total, cfg, out_wav):
    era = cfg.get("era", "barock")
    pre = PRESETS.get(era, PRESETS["barock"])
    tempo = cfg.get("tempo", pre["tempo"])
    beat = 60.0 / tempo
    bar = 4 * beat
    key_root = 12 * 3 + orch.NOTE[cfg.get("key", "D")]   # D2 = 38
    prog = PROG[pre["prog"]]
    t_drop, t_out, hits, state = beats.sections(scenes, total, cfg, beat)
    tr = orch.Track(480, tempo)
    chans = {}
    for i, (role, program, *_r) in enumerate(pre["parts"]):
        ch = DRUM if role == "drum" else (i if i < DRUM else i + 1)
        chans[role] = ch
        if ch != DRUM:
            tr.program(ch, program)
        tr.cc(ch, 91, 85, 0)
        tr.cc(ch, 7, 100, 0)
    kicks = []
    k = -int(np.ceil(t_drop / bar))
    while t_drop + k * bar < total + 1:
        b0 = t_drop + k * bar
        idx = k % len(prog)
        off, minor = prog[idx]
        if b0 >= t_out:
            off, minor = 0, 1
        ch_notes = chord(key_root, off, minor)
        for role, program, pat, octv, vel, start in pre["parts"]:
            ch = chans[role]
            if role == "drum":
                for step, note, v in DRUM_PATTERNS[pat]:
                    t = b0 + step * beat / 4
                    s = state(t) if t >= 0 else "intro"
                    if t < 0 or t >= total or s in ("gap", "outro"):
                        continue
                    if start == "full" and s == "intro":
                        continue
                    if s == "tense" and note not in (36, 41, 76, 77):
                        continue
                    tr.note(ch, note, t, beat / 4, int(v * vel / 100))
                    if note in (36, 41) or (note == 38 and v >= 100):
                        kicks.append(round(t, 3))
                continue
            for t, n, d, v in bar_notes(pat, ch_notes, b0, beat, octv - 2, vel, k, key_root):
                if t < 0 or t >= total + 0.5:
                    continue
                s = state(t)
                if s == "gap":
                    continue
                if s == "intro" and start == "full":
                    continue
                if s == "tense" and role not in ("bass", "pad", "timp", "taiko", "drone"):
                    continue
                if s == "outro" and role not in ("lead", "pad", "drone"):
                    continue
                tr.note(ch, n, t, d, v - (12 if s in ("intro", "outro") else 0))
                if role in ("timp", "taiko") and s != "intro":
                    kicks.append(round(t, 3))
        k += 1
    # Pauken-/Blechakzent auf Drop und Hits
    acc = chans.get("timp", chans.get("taiko", chans.get("brass")))
    for h in [t_drop] + hits:
        if acc is not None:
            for j in range(6):
                tr.note(acc, key_root, max(0, h - 0.33 + j * 0.055), 0.08, 50 + 9 * j)
            tr.note(acc, key_root, h, 1.4, 120)
    with tempfile.TemporaryDirectory() as td:
        mid, wav = os.path.join(td, "e.mid"), os.path.join(td, "e.wav")
        tr.to_midi(tempo, mid)
        subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", str(SR), "-o", "synth.reverb.room-size=0.8",
                        "-o", "synth.reverb.level=0.7", "-F", wav, orch.find_sf2(), mid], check=True,
                       capture_output=True)
        with wave.open(wav) as wf:
            a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
            if wf.getnchannels() == 2:
                a = a.reshape(-1, 2).mean(axis=1)
    n = int((total + 3) * SR)
    mix = np.zeros(n)
    mix[:min(n, len(a))] = a[:n]
    # moderner Kino-Impact (dezent) auf Bild 1, Drop und Hits
    fx = np.zeros(n)
    for h in [0.0, t_drop] + hits:
        beats.place(fx, beats.impact(), h, 0.45)
        if h > 0.5:
            beats.place(fx, beats.reverse_swell(min(0.8, h)), h - min(0.8, h), 0.25)
    mix = mix / max(1e-6, np.sqrt(np.mean(mix[:int(total * SR)] ** 2))) * 0.12 + fx * 0.5
    mix = beats.finish(mix, total, t_out)
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    import json
    meta = {"kicks": sorted(set(kicks)), "drop": t_drop, "beat": beat}
    with open(os.path.splitext(out_wav)[0] + ".json", "w") as f:
        json.dump(meta, f)
    return out_wav, meta
