#!/usr/bin/env python3
"""Nachbau der ig-human-Prüfung (Deutsch + Englisch).

  python3 human_check.py text.txt --clean out.txt   # säubern + Bericht
  python3 human_check.py text.txt                   # nur bewerten
  python3 human_check.py vorher.txt nachher.txt     # Vergleich

Fünf lokale Heuristiken (0-100, höher = menschlicher). KEIN GPTZero o. Ä.
Urteil: 60 % Mittelwert + 40 % schwächster Wert. PASS = >= 70 und kein Wert < 55.
"""
import argparse
import re
import statistics
import sys
import unicodedata

INVISIBLE = re.compile("[​‌‍⁠­﻿⁣⁢⁡᠎    \U000e0000-\U000e007f]")
TYPO = [("—", ", "), ("–", "-"), ("“", '"'), ("”", '"'), ("„", '"'), ("‟", '"'), ("’", "'"), ("‘", "'"),
        ("‚", "'"), ("…", "..."), ("•", "-"), ("«", '"'), ("»", '"')]

# Stock-Vokabular -> Ersatz ("" = streichen). Darf ergänzt/gekürzt werden.
SLOP = {
    # Deutsch
    "tauchen wir ein": "schauen wir rein", "lass uns eintauchen": "schauen wir rein", "eintauchen": "reinschauen",
    "in der heutigen schnelllebigen welt": "heute", "es ist wichtig zu beachten, dass": "", "es ist wichtig zu beachten": "",
    "nahtlos": "glatt", "bahnbrechend": "neu", "revolutionär": "neu", "atemberaubend": "stark", "faszinierend": "spannend",
    "zweifellos": "", "letztendlich": "am Ende", "im wesentlichen": "", "ein zeugnis für": "ein Beweis für",
    "meilenstein": "Schritt", "unvergesslich": "", "gamechanger": "Wende", "ganzheitlich": "", "maßgeschneidert": "passend",
    "vielfältig": "verschieden", "spannende welt": "Welt", "reise durch die zeit": "Blick zurück",
    "begleite mich auf einer reise": "", "in diesem video": "", "willkommen zurück": "", "hallo zusammen": "",
    "hey leute": "", "vergiss nicht zu abonnieren": "", "folge für mehr": "", "markiere jemanden": "",
    "lass ein like da": "", "like und abonnieren": "", "zusammenfassend lässt sich sagen": "", "fazit:": "",
    "spannend, oder?": "", "unglaublich, aber wahr": "", "du wirst nicht glauben": "",
    # Englisch
    "delve": "dig", "leverage": "use", "robust": "strong", "seamless": "smooth", "crucial": "key",
    "testament to": "proof of", "in today's fast-paced world": "today", "stop scrolling": "", "in today's video": "",
    "follow for more": "", "tag someone who needs this": "", "the algorithm loves": "", "run don't walk": "",
    "game-changer": "shift", "unlock": "open", "embark": "start", "tapestry": "mix", "realm": "area",
}

STRUCT = [
    (r"\bnicht nur\b.{1,60}\bsondern auch\b", "'nicht nur ... sondern auch'"),
    (r"\bes ist nicht (nur )?\w+.{0,30}, (es ist|sondern)\b", "'Es ist nicht X, es ist Y'"),
    (r"\bit'?s not (just )?\w+.{0,30}, it'?s\b", "'It's not X, it's Y'"),
    (r"\bnot only\b.{1,60}\bbut also\b", "'not only ... but also'"),
    (r"(?m)^\s*(das ergebnis|die antwort|der grund|the result|the answer)\?\s*$", "Ein-Wort-Fragezeile"),
    (r"\b(in diesem video (zeige|erkläre)|in this video i'?m going to)\b", "Video-Vorrede"),
    (r"(?m)^\s*[\U0001F300-\U0001FAFF☀-➿]\s", "Emoji-Aufzählung"),
    (r"\b([A-ZÄÖÜ]{3,}\s+){2,}[A-ZÄÖÜ]{3,}\b", "3+ geschriebene Großwörter am Stück"),
    (r"(#\w+\s*){6,}", "Hashtag-Wand (>5)"),
    (r"\b(folge für mehr|markiere jemanden|doppelklick wenn|follow for more|tag someone who|double tap if)\b", "Reflex-Köder"),
]
TRIAD = re.compile(r"\b\w+, \w+(,)? und \w+\b")
ARTICLES = set("der die das den dem des ein eine einen einem einer eines kein keine keinen meine mein sein seine ihr ihre "
               "unser unsere dieser diese dieses jeder jede jedes alle viele manche zum zur im am vom beim the a an".split())
YOU = re.compile(r"\b(du|dich|dir|dein\w*|ihr|euch|euer|you|your)\b", re.I)
CONTR = re.compile(r"\b\w+'s\b|\b(gibt's|geht's|wie's|schreib's|hab|nen|'n|mal|halt|eben|ja|doch|ok)\b", re.I)


def clean(text):
    report = []
    n = len(INVISIBLE.findall(text))
    text = INVISIBLE.sub(lambda m: " " if m.group() in "    " else "", text)
    extra = sum(1 for ch in text if unicodedata.category(ch) == "Cf")
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    if n + extra:
        report.append(f"unsichtbare Zeichen entfernt: {n + extra}")
    for a, b in TYPO:
        c = text.count(a)
        if c:
            text = text.replace(a, b)
            report.append(f"Typografie {a!r} -> {b!r}: {c}x")
    text = re.sub(r" ,", ",", text)
    text = re.sub(r",\s*([.,!?])", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    for k, v in SLOP.items():
        pat = re.compile(r"(?<![\w/])" + re.escape(k) + r"(?![\w])", re.I)
        def sub(m):
            w = m.group()
            if not v:
                return ""
            return v[0].upper() + v[1:] if w[0].isupper() else v
        text, c = pat.subn(sub, text)
        if c:
            report.append(f"Floskel '{k}' -> '{v or '(gestrichen)'}': {c}x")
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^ +", "", text)
    return text, report


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p for p in (x.strip() for x in parts) if len(p.split()) >= 1]


def score(text):
    words = re.findall(r"[\wÄÖÜäöüß'-]+", text)
    nw = max(1, len(words))
    sents = sentences(text)
    lens = [len(s.split()) for s in sents] or [1]
    cv = statistics.pstdev(lens) / max(1, statistics.mean(lens)) if len(lens) > 1 else 0
    burst = min(100, int(cv * 160))
    # Spezifität: Zahlen + Eigennamen (groß, nicht satzinitial, kein Artikel davor)
    spec = len(re.findall(r"\b\d[\d.,]*\b", text))
    for s in sents:
        toks = s.split()
        for i in range(1, len(toks)):
            w = re.sub(r"[^\wÄÖÜäöüß]", "", toks[i])
            prev = re.sub(r"[^\wäöüß]", "", toks[i - 1].lower())
            if w[:1].isupper() and prev not in ARTICLES and len(w) > 2 and not w.isupper():
                spec += 0.5
    specificity = min(100, int(spec / nw * 100 * 12.5))
    low = text.lower()
    hits = sum(len(re.findall(r"(?<![\w])" + re.escape(k) + r"(?![\w])", low)) for k in SLOP)
    slop = max(0, 100 - int(hits / nw * 100 * 25))
    fp_hits = len(INVISIBLE.findall(text)) + text.count("—") + sum(text.count(c) for c in "“”„’‘") + text.count("…")
    fingerprint = max(0, 100 - int(fp_hits / max(1, len(text)) * 1000 * 20))
    flags = [label for pat, label in STRUCT if re.search(pat, text, 0 if "A-Z" in pat else re.I)]
    triads = len(TRIAD.findall(text))
    if triads >= 2:
        flags.append(f"Dreier-Aufzählungen: {triads}")
    you = len(YOU.findall(text))
    contr = len(CONTR.findall(text))
    qs = text.count("?")
    voice = min(100, 45 + int((you + contr + qs) / nw * 100 * 6)) - 12 * len(flags)
    voice = max(0, voice)
    checks = {"BURSTINESS": burst, "SPECIFICITY": specificity, "SLOP DENSITY": slop, "FINGERPRINT": fingerprint,
              "VOICE": voice}
    mean = sum(checks.values()) / len(checks)
    weakest = min(checks.values())
    overall = int(0.6 * mean + 0.4 * weakest)
    verdict = "PASS" if overall >= 70 and weakest >= 55 else ("REVIEW" if overall >= 50 else "FAIL")
    return checks, overall, verdict, flags


def show(name, text):
    checks, overall, verdict, flags = score(text)
    print(f"== {name}")
    for k, v in checks.items():
        print(f"  {k:<13}{v:>4}  {'#' * (v // 5)}")
    print(f"  GESAMT {overall}  ->  {verdict}")
    weakest = min(checks, key=checks.get)
    if verdict != "PASS":
        print(f"  schwächster Wert: {weakest}")
    for f in flags:
        print(f"  ! Struktur: {f}  (von Hand umschreiben)")
    return verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--clean", help="gesäuberten Text hierhin schreiben")
    a = ap.parse_args()
    texts = [open(f, encoding="utf-8").read() for f in a.files]
    if a.clean:
        out, rep = clean(texts[0])
        open(a.clean, "w", encoding="utf-8").write(out)
        print("Änderungen:" if rep else "Keine automatischen Änderungen nötig.")
        for r in rep:
            print("  -", r)
        show(a.files[0] + " (vorher)", texts[0])
        v = show(a.clean + " (nachher)", out)
    else:
        for f, t in zip(a.files, texts):
            v = show(f, t)
    sys.exit(0 if v == "PASS" else 1)


if __name__ == "__main__":
    main()
