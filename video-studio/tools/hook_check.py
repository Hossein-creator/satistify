#!/usr/bin/env python3
"""Hook-Prüfung für History-Shorts (Regeln aus playbook/HOOKS.md).

  python3 hook_check.py videos/<ordner>/video.yaml          # prüft Hook + Ende der video.yaml
  python3 hook_check.py --text "Dieser König wollte, dass man ihn bestiehlt."   # einzelne Hook-Zeile
  python3 hook_check.py --text "A" --text "B" --text "C"   # mehrere Varianten vergleichen (Rangliste)

Bewertet 0-100. PASS ab 75. Lokale Heuristik, kein Ersatz für echte Zahlen (Retention in YouTube Studio).
"""
import argparse
import re
import sys

import yaml

BANNED = ["hallo", "hey leute", "willkommen", "in diesem video", "heute schauen wir", "heute geht es",
          "lass uns", "abonnier", "wusstest du", "hast du dich jemals gefragt", "stell dir vor",
          "in der geschichte gab es", "es war einmal"]
TWIST = ["aber", "doch", "nur:", "sondern", "statt", "eigentlich", "trotzdem", "obwohl", "nicht um", "niemand",
         "keiner", "kein einziger", "falsch", "in wahrheit", "wollte, dass", "verboten", "geheim", "nie"]
DARK = ["tod", "starb", "tot", "hinricht", "folter", "strafe", "grausam", "mord", "gift", "pest", "hunger",
        "krieg", "leiche", "grab", "blut", "verbrann", "gestohlen", "bestiehlt", "stehlen", "dieb", "ekel", "gestank"]
WEAK_START = ["es ", "das ", "in ", "im ", "heute", "also", "so ", "ja", "okay"]


def words(s):
    return re.findall(r"[\wÄÖÜäöüß'-]+", s)


def first_sentence(s):
    m = re.split(r"(?<=[.!?:])\s+", s.strip())
    return m[0] if m else s


def score_line(line, scene0=None, last=None, spec=None):
    pts, notes = 0, []
    fs = first_sentence(line)
    n = len(words(fs))
    low = line.lower()
    # 1 Kürze: erster Satz <= 9 Wörter (~2,5 s gesprochen)
    if n <= 9:
        pts += 20
    elif n <= 12:
        pts += 10
        notes.append(f"Erster Satz hat {n} Wörter: auf höchstens 9 kürzen (unter 3 Sekunden).")
    else:
        notes.append(f"Erster Satz hat {n} Wörter: viel zu lang für die ersten 3 Sekunden.")
    # 2 Kein Anlauf / keine Floskel
    bad = [b for b in BANNED if b in low]
    if not bad and not any(low.startswith(w) for w in WEAK_START):
        pts += 15
    else:
        pts -= 10 if bad else 0
        notes.append("Anlauf/Floskel streichen: " + ", ".join(bad or ["schwacher erster Wortbeginn"]))
    # 3 Konkretheit: Zahl, Jahr, Name, oder "Dieser/Diese" + Person (zeigt aufs Bild)
    concrete = bool(re.search(r"\d", line)) or bool(re.search(r"\b(dieser|diese|dieses)\b", low)) or \
        len([w for w in words(fs)[1:] if w[:1].isupper()]) >= 1
    if concrete:
        pts += 15
    else:
        notes.append("Konkreter werden: Zahl, Jahr, Name oder 'Dieser König …' (zeigt auf das Bild).")
    # 4 Widerspruch / Neugier-Lücke
    if any(t in low for t in TWIST):
        pts += 20
    elif "?" in line:
        pts += 8
        notes.append("Nur eine Frage: stärker ist eine Behauptung mit Widerspruch.")
    else:
        notes.append("Es fehlt ein Widerspruch ('… aber', 'nicht um … sondern', 'wollte, dass …').")
    # 5 Dunkle / emotionale Fallhöhe (gewinnt laut Kanal-Analyse)
    if any(d in low for d in DARK):
        pts += 10
    else:
        notes.append("Fallhöhe fehlt: Tod, Strafe, Hunger, Verbot, Diebstahl … (dunkel schlägt nett).")
    # 6 Hook löst sich nicht sofort auf (offene Schleife)
    if not re.search(r"\b(weil|deshalb|denn)\b", first_sentence(line).lower()):
        pts += 10
    else:
        notes.append("Die Auflösung steht schon im ersten Satz: 'weil/denn' in den Mittelteil verschieben.")
    # 7 Bild + Ton im ersten Frame (nur mit video.yaml)
    if scene0 is not None:
        vis = scene0.get("visual", [])
        photo = next((v for v in vis if v.get("type") == "photo"), None)
        moving = photo is not None and (photo.get("ease") == "out" or photo.get("from") != photo.get("to"))
        if scene0.get("hit") and moving:
            pts += 5
        else:
            notes.append("Szene 1: 'hit: true' (Punch-In + Impact) und eine schnelle Kamerafahrt (ease: out).")
        if last is not None:
            lt = last.get("text", "").strip()
            if lt.endswith(":") or lt.endswith("…") or set(w.lower() for w in words(lt)) & \
                    set(w.lower() for w in words(line) if len(w) > 4):
                pts += 5
            else:
                notes.append("Loop fehlt: Der letzte Satz sollte in den ersten Satz überleiten (z. B. endet mit ':').")
    else:
        pts += 10
    return min(100, pts), notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--text", action="append")
    a = ap.parse_args()
    rows = []
    if a.spec:
        spec = yaml.safe_load(open(a.spec, encoding="utf-8"))
        sc = spec["scenes"]
        hook = sc[0]["text"] + " " + (sc[1]["text"] if len(sc) > 1 else "")
        sc_, notes = score_line(sc[0]["text"], sc[0], sc[-1], spec)
        # Szene 2 muss die Lücke öffnen, falls Szene 1 sie nicht schon öffnet
        if not any(t in hook.lower() for t in TWIST):
            notes.append("Bis Sekunde 5 kommt kein Widerspruch.")
        rows.append((sc_, sc[0]["text"], notes))
    for t in a.text or []:
        s, notes = score_line(t)
        rows.append((s, t, notes))
    rows.sort(key=lambda r: -r[0])
    ok = True
    for s, t, notes in rows:
        verdict = "PASS" if s >= 75 else "NACHBESSERN"
        ok &= s >= 75
        print(f"{s:3d}/100 {verdict:11s} {t}")
        for n_ in notes:
            print("        - " + n_)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
