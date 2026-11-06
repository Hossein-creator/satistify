#!/usr/bin/env python3
"""Gemeinfreie Bilder (CC0) von The Met Open Access suchen und laden.

  python3 met.py search "Gillray Napoleon" [n]
  python3 met.py get 391822 [391212 ...] --dir videos/<ordner>/assets

Jedes Bild bekommt eine .json (Titel, Künstler, Datum, Lizenz, Quelle) für die Bildnachweise in upload.md.
Große Bilder werden auf max. 3000 px Kante verkleinert.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "satistify-video-tool/1.0 (educational history videos)"}
BASE = "https://collectionapi.metmuseum.org/public/collection"


def get(u, raw=False):
    for a in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60)
            return r.read() if raw else json.load(r)
        except Exception as e:
            err = e
            time.sleep(2 + 2 * a)
    print(f"Fehler: {u}: {err}", file=sys.stderr)
    return b"" if raw else {}


def obj(i):
    return get(f"{BASE}/v1/objects/{i}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "get"])
    ap.add_argument("args", nargs="+")
    ap.add_argument("--dir", default=".")
    a = ap.parse_args()
    if a.cmd == "search":
        n = int(a.args[1]) if len(a.args) > 1 else 12
        d = get(f"{BASE}/v1.1/search?hasImages=true&isPublicDomain=true&limit={n}&q={urllib.parse.quote(a.args[0])}")
        for i in (d.get("objectIDs") or [])[:n]:
            o = obj(i)
            if o.get("isPublicDomain"):
                print(i, "|", o.get("title", "")[:70], "|", o.get("artistDisplayName", "")[:30], "|", o.get("objectDate", ""))
        return
    os.makedirs(a.dir, exist_ok=True)
    from PIL import Image
    for i in a.args:
        o = obj(int(i))
        if not o.get("isPublicDomain") or not o.get("primaryImage"):
            print(f"{i}: nicht gemeinfrei oder kein Bild – übersprungen", file=sys.stderr)
            continue
        name = re.sub(r"[^\w\-]+", "_", o["title"])[:60].strip("_") + f"_Met{i}.jpg"
        path = os.path.join(a.dir, name)
        if not os.path.exists(path):
            open(path, "wb").write(get(o["primaryImage"], raw=True))
            im = Image.open(path)
            if max(im.size) > 3000:
                im.thumbnail((3000, 3000))
                im.convert("RGB").save(path, quality=92)
        meta = {"title": o["title"], "license": "Public domain (CC0, The Met Open Access)", "ok": True,
                "artist": o.get("artistDisplayName") or "unbekannt", "date": o.get("objectDate", ""),
                "page": o.get("objectURL", f"https://www.metmuseum.org/art/collection/search/{i}"),
                "url": o["primaryImage"], "attribution_required": False}
        json.dump(meta, open(path + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, h = Image.open(path).size
        print(f"{name}  {w}x{h}")


if __name__ == "__main__":
    main()
