#!/usr/bin/env python3
"""ig-viral-Nachbau: Shorts sammeln, nach Ausreißer-Faktor ranken, Hook-Formeln benennen.

Sammeln (YouTube Shorts, öffentlich, kein Login, langsam):
  python3 swipe.py collect @HeyHistorically @extrahistory ... --out captured.tsv
Auswerten:
  python3 swipe.py rank captured.tsv --out swipe.md

Ausreißer-Faktor = Aufrufe / Median der letzten Shorts desselben Kanals.
> 3x = Signal. < 1.5x = normaler Tag, lehrt nichts.
Regel: Formel kopieren, nie das Video. Jede Zeile nennt ihren Kanal.
"""
import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time

FORMULAS = [
    (1, "Was-wäre-wenn", r"\b(what if|was wäre,? wenn|was wenn)\b"),
    (2, "Countdown", r"\b(\d+\s*(s|sec|seconds|sekunden|minutes|minuten)\s+(before|vor))\b|\bcountdown\b"),
    (3, "So-wirst-du", r"\b(how to (be|become|survive|win)|so wirst du|so überlebst du|wie man \w+ wird)\b"),
    (4, "Paradox-Warum", r"^\s*why\b|\bwhy (did|do|does|the|was|were|is)\b|\bwarum\b"),
    (5, "Wie-haben-sie", r"\b(how (did|do|does|were|was)|wie (haben|hat|konnte|konnten|überlebte))\b"),
    (6, "Top-Liste", r"\btop\s*\d+\b|\b\d+\s+(deadliest|greatest|largest|most|größten|tödlichsten)\b"),
    (7, "Superlativ", r"\b(worst|best|deadliest|shortest|longest|craziest|weirdest|dumbest|most \w+|schlimmste\w*|"
                      r"beste\w*|kürzeste\w*|längste\w*|verrückteste\w*|dümmste\w*|größte\w*)\b"),
    (8, "Mitten-drin", r"^\s*(in |im jahr |am )?(\d{1,2}(st|nd|rd|th|\.)?\s+)?(january|february|march|april|may|june|"
                       r"july|august|september|october|november|december|januar|februar|märz|juni|juli|oktober|"
                       r"dezember)?\s*\d{3,4}\b"),
    (9, "Mythos-Bruch", r"\b(actually|myth|lie|lied|wrong|really|eigentlich|mythos|lüge|falsch|in wahrheit)\b"),
    (10, "Geheimnis", r"\b(secret|hidden|nobody knows|no one knows|geheim\w*|niemand weiß|verborgen)\b"),
    (11, "Vorstellung", r"^\s*(this is|meet|das ist|dies ist|here'?s|hier ist)\b"),
    (12, "Evolution", r"\b(evolution of|history of|geschichte (von|des|der)|entire history|ganze geschichte)\b"),
    (14, "Kuriose-Technik", r"\b(insane|hybrid|weird|strange|crazy|outrun|kurios\w*|seltsam\w*|verrückt\w*|irre\w*)\b.*"
                            r"\b(gun|tank|weapon|plane|ship|waffe\w*|panzer|flugzeug|schiff|kanone\w*)\b|"
                            r"\b(gun|tank|weapon|waffe|panzer)\b.*\b(insane|outrun|hybrid)\b"),
    (15, "Heute-Bezug", r"\b(bis heute|heute noch|today|still|recently|gehört zu|belongs to)\b"),
    (16, "Dunkle-Figur", r"\b(grausam\w*|cruel\w*|evil|brutal\w*|verbrecher\w*|killer|mörder\w*|monster|tyrann\w*)\b"),
    (13, "Direkte-Frage", r"\?\s*$"),
]


def classify(hook):
    h = re.sub(r"\s*\|\s*(terra x|extra history|recently deleted history)\s*$", "", hook.lower().replace("’", "'"))
    h = re.sub(r"#\w+", "", h).strip()
    for fid, name, pat in FORMULAS:
        if re.search(pat, h, re.I):
            return fid, name
    return 0, "UNKLASSIFIZIERT"


def hookscore(hook):
    w = hook.split()
    sc = 50
    sc += 15 if len(w) <= 10 else (-10 if len(w) > 18 else 0)
    sc += 10 if re.search(r"\d", hook) else 0
    sc += 10 if any(t[:1].isupper() for t in w[1:]) else 0
    sc += 10 if re.search(r"\b(why|how|what|secret|warum|wie|was|geheim|never|nie)\b", hook, re.I) else 0
    sc += 5 if re.search(r"\b(you|your|du|dich|dir)\b", hook, re.I) else 0
    return max(0, min(100, sc))


def ytdlp(args):
    return subprocess.run([sys.executable, "-m", "yt_dlp", *args], capture_output=True, text=True)


def spoken_hook(vid, tmp):
    base = os.path.join(tmp, vid)
    ytdlp(["--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en-orig,en,de-orig,de",
           "--sub-format", "json3", "-o", base, f"https://www.youtube.com/watch?v={vid}"])
    files = [f for f in os.listdir(tmp) if f.startswith(vid) and f.endswith(".json3")]
    if not files:
        return ""
    files.sort(key=lambda f: ("orig" not in f, f))
    data = json.load(open(os.path.join(tmp, files[0]), encoding="utf-8"))
    words = []
    for ev in data.get("events", []):
        t0 = ev.get("tStartMs", 0)
        for sg in ev.get("segs", []) or []:
            t = t0 + sg.get("tOffsetMs", 0)
            txt = sg.get("utf8", "").strip()
            if txt and t < 3000:
                words.append(txt)
    return " ".join(words).replace("\n", " ").strip()


def collect(handles, out, n=40, picks=6):
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for h in handles:
            h = h.lstrip("@")
            r = ytdlp(["--flat-playlist", "--playlist-end", str(n), "-J", f"https://www.youtube.com/@{h}/shorts"])
            try:
                data = json.loads(r.stdout)
            except Exception:
                print(f"  @{h}: nicht lesbar ({r.stderr.strip()[:80]})", file=sys.stderr)
                continue
            ents = [e for e in data.get("entries", []) if e.get("view_count")]
            if len(ents) < 6:
                print(f"  @{h}: zu wenige Shorts ({len(ents)})", file=sys.stderr)
                continue
            med = statistics.median(e["view_count"] for e in ents)
            subs = data.get("channel_follower_count") or ""
            if not subs:
                info = ytdlp(["--skip-download", "--print", "%(channel_follower_count)s",
                              f"https://www.youtube.com/watch?v={ents[0]['id']}"])
                subs = info.stdout.strip().splitlines()[0] if info.stdout.strip() else ""
            ents.sort(key=lambda e: e["view_count"], reverse=True)
            chosen = ents[: picks - 2] + ents[-2:]
            for e in chosen:
                hook = spoken_hook(e["id"], tmp) or e.get("title", "")
                src = "gesprochen" if hook != e.get("title", "") else "titel"
                rows.append([f"@{h}", str(subs), str(int(med)), str(e["view_count"]), hook, e.get("title", ""),
                             str(e.get("duration") or ""), e["id"], src])
                time.sleep(1.0)
            print(f"  @{h}: {len(ents)} Shorts, Median {int(med):,}, Abos {subs}", file=sys.stderr)
    with open(out, "w", encoding="utf-8") as f:
        f.write("account\tfollowers\tmedian\tviews\thook\ttitle\tlength\tid\thook_source\n")
        for r_ in rows:
            f.write("\t".join(c.replace("\t", " ") for c in r_) + "\n")
    print(out)


def rank(path, out):
    lines = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8")]
    head, rows = lines[0], lines[1:]
    ix = {k: i for i, k in enumerate(head)}
    items = []
    for r in rows:
        try:
            views, med = int(float(r[ix["views"]])), int(float(r[ix["median"]]))
        except ValueError:
            continue
        hook = r[ix["hook"]]
        fid, fname = classify(hook)
        items.append({"acc": r[ix["account"]], "subs": r[ix["followers"]], "views": views, "med": med,
                      "mult": views / max(1, med), "hook": hook, "fid": fid, "fname": fname, "score": hookscore(hook),
                      "title": r[ix["title"]] if "title" in ix else "", "id": r[ix["id"]] if "id" in ix else ""})
    items.sort(key=lambda x: x["mult"], reverse=True)
    n = len(items)
    third = max(1, n // 3)
    top, bottom = items[:third], items[-third:]
    accs = sorted({i["acc"] for i in items})
    L = [f"# Swipe-File · {n} Shorts · {len(accs)} Kanäle · Basis: Kanal-Median\n",
         "Formel kopieren, nie das Video. Jede Zeile nennt ihre Quelle.\n", "## Ausreißer (über 3x)\n",
         "| Faktor | Hook-Score | Formel | Kanal | Aufrufe | Median | Hook (erste 3 s bzw. Titel) |", "|---|---|---|---|---|---|---|"]
    for i in items:
        if i["mult"] >= 3:
            L.append(f"| {i['mult']:.1f}x | {i['score']} | #{i['fid']} {i['fname']} | {i['acc']} | {i['views']:,} | "
                     f"{i['med']:,} | {i['hook'][:110]} |")

    def counts(group):
        c = {}
        for i in group:
            c[i["fname"]] = c.get(i["fname"], 0) + 1
        return c
    ct, cb = counts(top), counts(bottom)
    L.append("\n## Was überdurchschnittlich oft oben steht (oberes vs. unteres Drittel)\n")
    for k in sorted(set(ct) | set(cb), key=lambda k: -(ct.get(k, 0) - cb.get(k, 0))):
        L.append(f"- {k}: oben {ct.get(k, 0)}x, unten {cb.get(k, 0)}x")
    ml = lambda g: statistics.median(len(i["hook"].split()) for i in g) if g else 0
    L.append(f"\nMediane Hook-Länge: oben {ml(top):.0f} Wörter, unten {ml(bottom):.0f} Wörter")
    L.append(f"Medianer Hook-Score: oben {statistics.median(i['score'] for i in top):.0f}, "
             f"unten {statistics.median(i['score'] for i in bottom):.0f}\n")
    unk = [i for i in items if i["fid"] == 0]
    L.append(f"## Unklassifiziert ({len(unk)}) – von Hand lesen\n")
    for i in unk:
        L.append(f"- {i['mult']:.1f}x {i['acc']}: {i['hook'][:140]}")
    conf = "trägt eine Aussage" if n >= 40 and len(accs) >= 6 else "ist zu klein für feste Aussagen – nur Hinweise"
    L.append(f"\n**Stichprobe:** {n} Shorts aus {len(accs)} Kanälen – {conf}.\n")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("collect")
    c.add_argument("handles", nargs="+")
    c.add_argument("--out", required=True)
    c.add_argument("--n", type=int, default=40)
    c.add_argument("--picks", type=int, default=6)
    r = sp.add_parser("rank")
    r.add_argument("tsv")
    r.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "collect":
        collect(a.handles, a.out, a.n, a.picks)
    else:
        rank(a.tsv, a.out)


if __name__ == "__main__":
    main()
