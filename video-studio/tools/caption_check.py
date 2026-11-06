#!/usr/bin/env python3
"""Nachbau der ig-caption-Prüfung.

  python3 caption_check.py caption.txt --keywords "friedrich der große,preußen" [--platform instagram|youtube]

Zeigt die ersten 125 Zeichen wie im Feed (Rest hinter "mehr") und prüft die Regeln:
kein Gruß/Hashtag/Emoji am Anfang, genau eine Bitte (Ask), max. 5 Hashtags,
kein Link (Instagram), Emoji-Dichte <= 4 pro 100 Zeichen, Suchbegriffe im Fließtext.
"""
import argparse
import re
import sys

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]")
ASKS = [r"\bkommentier\w*", r"\bschreib(e|')?s?\b.{0,25}\bkommentar", r"\bspeicher\w*", r"\bschick\w* (das|es|mir)\b",
        r"\bteil\w* (das|es)\b", r"\babonnier\w*", r"\bfolg\w* (mir|uns)\b", r"\bcomment\b", r"\bsave this\b",
        r"\bdm me\b", r"\bsubscribe\b", r"\bschreib\w* (mir|es|uns)\b"]
GREET = re.compile(r"^\s*(hallo|hey|hi|servus|moin|willkommen|hello)\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--platform", default="instagram", choices=["instagram", "youtube"])
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read().strip()
    first = text[:125]
    print("┌" + "─" * 64)
    for i in range(0, len(first), 62):
        print("│ " + first[i:i + 62])
    print("└" + "─" * 64 + f"  … mehr  ({len(text)} Zeichen gesamt)")
    res = []

    def r(level, msg):
        res.append((level, msg))

    body_wo_tags = re.sub(r"#\w+", "", text)
    if text[:1] == "#" or EMOJI.match(text[:2] or " "):
        r("FAIL", "Erstes Zeichen ist Hashtag oder Emoji")
    if GREET.match(text):
        r("FAIL", "Beginnt mit einem Gruß")
    tags = re.findall(r"#\w+", text)
    if len(tags) > 5:
        r("FAIL", f"{len(tags)} Hashtags (max. 5)")
    dead = [t for t in tags if t.lower() in ("#viral", "#fyp", "#foryou", "#explorepage", "#fürdich", "#fy")]
    if dead:
        r("FAIL", "Nichtssagende Hashtags: " + ", ".join(dead))
    links = re.findall(r"https?://\S+|www\.\S+", text)
    if links and a.platform == "instagram":
        r("FAIL", "Link in Instagram-Caption (nicht klickbar) -> Bio oder erster Kommentar")
    asks = sum(1 for p in ASKS if re.search(p, text, re.I))
    if asks == 0:
        r("WARN", "Keine Bitte/Ask gefunden")
    elif asks > 1:
        r("FAIL", f"{asks} Bitten gefunden – genau eine")
    em = len(EMOJI.findall(text))
    if em / max(1, len(text)) * 100 > 4:
        r("WARN", f"Emoji-Dichte {em / len(text) * 100:.1f} pro 100 Zeichen (> 4)")
    limit = 2200 if a.platform == "instagram" else 5000
    if len(text) > limit:
        r("FAIL", f"Länger als {limit} Zeichen")
    for kw in [k.strip() for k in a.keywords.split(",") if k.strip()]:
        if kw.lower() in body_wo_tags.lower():
            line = next(i + 1 for i, l in enumerate(text.splitlines()) if kw.lower() in l.lower())
            r("OK", f"Suchbegriff '{kw}' in Zeile {line}")
        else:
            r("FAIL", f"Suchbegriff '{kw}' fehlt im Fließtext")
    for lvl, msg in res:
        print(f"  {lvl:<5} {msg}")
    status = "READY" if not any(l == "FAIL" for l, _ in res) else "FIX"
    print(f"\nlinter: {status}  · sichtbar: {min(125, len(text))} von 125 · Bitten: {asks} · Hashtags: {len(tags)}")
    sys.exit(0 if status == "READY" else 1)


if __name__ == "__main__":
    main()
