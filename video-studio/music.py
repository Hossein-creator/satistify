"""Filmmusik-Generator: komponiert pro Video eine passende Orchester-Untermalung.

Lizenzfrei & Content-ID-sicher: eigene Komposition (MIDI) + FluidR3-Soundfont (MIT-Lizenz).
Die Musik folgt dem Video:
  - ruhiger Beginn (Streicher + Motiv-Instrument)
  - Puls (Cello-Ostinato) in der Mitte und bei `heartbeat`-Szenen
  - Pauken + Horn + Chor exakt auf Szenen mit `hit: true`
  - Auflösung am Ende

In video.yaml:
  music: {score: dark, motif: flute, tempo: 68}
  score: dark | mystery | epic | sad | hope   motif: flute | oboe | cello | piano | horn | none
"""
import hashlib
import os
import subprocess

import mido

SF2_CANDIDATES = ["/usr/share/sounds/sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/default-GM.sf2"]

# Akkorde als MIDI-Grundton + Moll/Dur
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "Ab": 8, "A": 9,
        "Bb": 10, "B": 11}
PROGRESSIONS = {
    "dark": ["Dm", "Bb", "Gm", "A"],
    "mystery": ["Am", "F", "Dm", "E"],
    "epic": ["Dm", "Bb", "F", "C"],
    "sad": ["Dm", "Gm", "Bb", "A"],
    "hope": ["C", "G", "Am", "F"],
}
END_CHORD = {"dark": "Dm", "mystery": "Am", "epic": "D", "sad": "Dm", "hope": "C"}
MOTIF_PROGRAM = {"flute": 73, "oboe": 68, "cello": 42, "piano": 0, "horn": 60, "clarinet": 71}

CH = {"strings": 0, "bass": 1, "cello": 2, "horn": 3, "choir": 4, "motif": 5, "timp": 6, "piano": 7}
PROG = {"strings": 48, "bass": 43, "cello": 42, "horn": 60, "choir": 52, "timp": 47, "piano": 0}


def chord_notes(name, octave=4):
    minor = name.endswith("m")
    root = NOTE[name[:-1] if minor else name]
    base = 12 * (octave + 1) + root
    third = 3 if minor else 4
    return base, [base, base + third, base + 7]


def find_sf2():
    for p in SF2_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


class Track:
    def __init__(self, tpb, tempo):
        self.events = []  # (abs_tick, msg)
        self.tpb = tpb
        self.spb = 60.0 / tempo  # Sekunden pro Schlag

    def tick(self, sec):
        return int(round(sec / self.spb * self.tpb))

    def note(self, ch, pitch, start, dur, vel):
        if dur <= 0:
            return
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        self.events.append((self.tick(start), mido.Message("note_on", channel=ch, note=pitch, velocity=vel)))
        self.events.append((self.tick(start + dur), mido.Message("note_off", channel=ch, note=pitch, velocity=0)))

    def cc(self, ch, ctrl, val, at):
        self.events.append((self.tick(at), mido.Message("control_change", channel=ch, control=ctrl,
                                                        value=max(0, min(127, int(val))))))

    def program(self, ch, prog):
        self.events.append((0, mido.Message("program_change", channel=ch, program=prog)))

    def to_midi(self, tempo, path):
        mid = mido.MidiFile(ticks_per_beat=self.tpb)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=0))
        last = 0
        for t, msg in sorted(self.events, key=lambda e: (e[0], e[1].type == "note_on")):
            msg.time = t - last
            last = t
            tr.append(msg)
        mid.save(path)


def compose(scenes, total, cfg, out_wav):
    """scenes: Liste mit _start/_end und optional hit/heartbeat. Schreibt WAV, gibt Pfad zurück."""
    mood = cfg.get("score", "dark")
    motif = cfg.get("motif", "flute")
    tempo = cfg.get("tempo", 68)
    prog = PROGRESSIONS.get(mood, PROGRESSIONS["dark"])
    tr = Track(480, tempo)
    for name, ch in CH.items():
        if name == "motif":
            if motif in MOTIF_PROGRAM:
                tr.program(ch, MOTIF_PROGRAM[motif])
        else:
            tr.program(ch, PROG[name])
        tr.cc(ch, 91, 90 if name != "bass" else 60, 0)   # Hall
        tr.cc(ch, 7, 100, 0)

    beat = 60.0 / tempo
    bar = 4 * beat
    nbars = int(total / bar) + 1
    hits = [sc["_start"] for sc in scenes if sc.get("hit")]
    pulses = [(sc["_start"], sc["_end"]) for sc in scenes if sc.get("heartbeat")]
    n = len(scenes)
    mid_start = scenes[min(2, n - 1)]["_start"] if n > 2 else 0
    end_start = scenes[-1]["_start"] if n > 1 else total

    # Lautstärke-Kurve (Expression CC11) für Streicher: langsames Anschwellen
    for i in range(0, int(total) + 1):
        prog_t = i / max(1, total)
        val = 55 + 50 * min(1, prog_t * 1.6) if i < end_start else 70 - 20 * (i - end_start) / max(1, total - end_start)
        tr.cc(CH["strings"], 11, val, i)
        tr.cc(CH["choir"], 11, val, i)

    for b in range(nbars):
        t0 = b * bar
        if t0 >= total:
            break
        is_end = t0 >= end_start - 0.01
        name = END_CHORD.get(mood, prog[0]) if is_end else prog[b % len(prog)]
        root, triad = chord_notes(name, 3)
        dur = min(bar, total - t0) + (0.0 if not is_end else 2.0)
        # Streicher: Akkord, Grundton oben verdoppelt
        for p_ in triad + [triad[0] + 12]:
            tr.note(CH["strings"], p_ + 12, t0, dur, 62)
        # Kontrabass: Grundton tief
        tr.note(CH["bass"], root - 12, t0, dur, 70)
        # Cello-Ostinato (Puls) im Mittelteil
        in_pulse = any(a - 0.1 <= t0 < e for a, e in pulses)
        if (mid_start <= t0 < end_start) or in_pulse:
            step = beat / 2
            pat = [root, root + 7, root + 12, root + 7]
            for k in range(8):
                tt = t0 + k * step
                if tt >= total:
                    break
                tr.note(CH["cello"], pat[k % 4], tt, step * 0.9, 58 + (12 if in_pulse else 0) + (6 if k % 2 == 0 else 0))
        # Chor-Pad in der zweiten Hälfte
        if t0 > total * 0.45 and not is_end:
            for p_ in triad[:2]:
                tr.note(CH["choir"], p_ + 12, t0, dur, 48)
        # Motiv-Instrument: Anfang und Ende, einfache Phrase aus Akkordtönen
        if motif in MOTIF_PROGRAM and (b < 2 or is_end):
            phrase = [triad[2] + 12, triad[1] + 12, triad[0] + 12, triad[1] + 12] if b % 2 == 0 else \
                     [triad[0] + 12, triad[2] + 12, triad[2] + 14, triad[1] + 12]
            for k, pn in enumerate(phrase):
                tt = t0 + k * beat
                if tt < total:
                    tr.note(CH["motif"], pn + (12 if motif == "flute" else 0), tt, beat * (1.8 if k == 3 else 0.95), 72)

    # Akzente auf Wendungen: Pauke + Horn + tiefes Klavier
    for h in hits:
        idx = int(h / bar)
        name = prog[idx % len(prog)]
        root, triad = chord_notes(name, 3)
        for k in range(6):  # kurzer Paukenwirbel
            tr.note(CH["timp"], root - 12, max(0, h - 0.36 + k * 0.06), 0.1, 60 + k * 8)
        tr.note(CH["timp"], root - 12, h, 1.5, 120)
        tr.note(CH["piano"], root - 24, h, 2.5, 110)
        tr.note(CH["piano"], root - 12, h, 2.5, 95)
        for p_ in triad:
            tr.note(CH["horn"], p_, h, 2.2, 96)

    base = os.path.splitext(out_wav)[0]
    mid_path = base + ".mid"
    tr.to_midi(tempo, mid_path)
    sf2 = find_sf2()
    if not sf2:
        raise RuntimeError("Kein Soundfont gefunden (apt-get install fluidsynth fluid-soundfont-gm)")
    subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-r", "44100", "-o", "synth.reverb.room-size=0.85",
                    "-o", "synth.reverb.level=0.8", "-F", out_wav, sf2, mid_path], check=True,
                   capture_output=True)
    return out_wav


def cache_key(scenes, total, cfg):
    sig = repr(([(round(s["_start"], 2), round(s["_end"], 2), bool(s.get("hit")), bool(s.get("heartbeat")))
                 for s in scenes], round(total, 2), sorted(cfg.items())))
    return hashlib.md5(sig.encode()).hexdigest()[:10]
