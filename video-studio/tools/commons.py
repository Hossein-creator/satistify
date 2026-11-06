#!/usr/bin/env python3
"""Gemeinfreie/freie Bilder von Wikimedia Commons suchen und mit Lizenzangaben laden.

  python3 commons.py search "Warthmüller König überall"          # Kandidaten anzeigen
  python3 commons.py get "File:Der König überall.jpg" --dir videos/<ordner>/assets

Jedes geladene Bild bekommt eine .json mit Titel, Urheber, Lizenz und Quelle.
render.py schreibt daraus automatisch die Bildnachweise in upload.md.
Erlaubt: Public Domain, CC0, CC BY, CC BY-SA (BY/BY-SA => Namensnennung Pflicht).
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "satistify-video-tool/1.0 (https://github.com/Hossein-creator/satistify; educational history videos)"
OK_LICENSE = re.compile(r"public domain|^pd|cc0|cc[- ]by(-sa)?[- ]\d|cc[- ]by(-sa)?$", re.I)


def _open(url, timeout=30):
    """Mit Pausen und Wiederholung (Wikimedia drosselt schnelle Anfragen)."""
    import time
    import urllib.error
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
            print(f"  (Wikimedia drosselt, warte {wait}s)", file=sys.stderr)
            time.sleep(wait)


def call(params):
    params = {**params, "format": "json"}
    with _open(API + "?" + urllib.parse.urlencode(params)) as r:
        return json.load(r)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def info(pages, width=2400):
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip(md.get("LicenseShortName", {}).get("value", ""))
        out.append({
            "title": p["title"], "license": lic, "ok": bool(OK_LICENSE.search(lic)),
            "artist": strip(md.get("Artist", {}).get("value", ""))[:120],
            "date": strip(md.get("DateTimeOriginal", {}).get("value", ""))[:40],
            "desc": strip(md.get("ImageDescription", {}).get("value", ""))[:160],
            "width": ii.get("width"), "height": ii.get("height"),
            "url": ii.get("thumburl") or ii.get("url"), "page": ii.get("descriptionurl"),
            "attribution_required": strip(md.get("AttributionRequired", {}).get("value", "")) == "true",
        })
    return out


def search(q, n=12):
    d = call({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n,
              "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 2400})
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    return info(pages)


def get(title, dest):
    if not title.startswith("File:"):
        title = "File:" + title
    d = call({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size",
              "iiurlwidth": 3840})
    pages = list(d.get("query", {}).get("pages", {}).values())
    if not pages or "imageinfo" not in pages[0]:
        sys.exit(f"nicht gefunden: {title}")
    meta = info(pages)[0]
    if not meta["ok"]:
        print(f"WARNUNG: Lizenz '{meta['license']}' ist nicht auf der Freigabeliste – nicht verwenden.", file=sys.stderr)
    os.makedirs(dest, exist_ok=True)
    name = re.sub(r"[^\w.-]+", "_", title[5:])
    name = os.path.splitext(name)[0][:80] + ".jpg"
    path = os.path.join(dest, name)
    url = meta["url"].split("?")[0].replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/")
    with _open(url, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    try:  # in JPEG umwandeln (PNG/TIFF-Thumbs)
        from PIL import Image
        im = Image.open(path)
        if im.format != "JPEG":
            im.convert("RGB").save(path, quality=92)
    except Exception:
        pass
    json.dump(meta, open(path + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
    return path


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("search")
    s.add_argument("query")
    s.add_argument("-n", type=int, default=12)
    g = sp.add_parser("get")
    g.add_argument("title")
    g.add_argument("--dir", required=True)
    a = ap.parse_args()
    if a.cmd == "search":
        for m in search(a.query, a.n):
            flag = "OK " if m["ok"] else "-- "
            print(f"{flag}{m['width']}x{m['height']}  [{m['license']}]  {m['title']}\n      {m['artist'][:70]} · {m['date']}")
    else:
        get(a.title, a.dir)


if __name__ == "__main__":
    main()
