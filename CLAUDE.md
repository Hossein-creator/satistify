# Anweisungen für Claude

Dieses Repository ist Claudes **dauerhafter Speicherplatz** für diesen Nutzer.

## Grundregel
Alles, was Claude in einer Sitzung schreibt oder erstellt (Texte, Notizen, Dokumente,
Code, Ergebnisse, Zusammenfassungen), wird **in diesem Repo gespeichert, committet und gepusht**.
Cloud-Sitzungen sind flüchtig – was nicht gepusht ist, geht verloren.

## Ablage
- `notizen/`   – kurze Notizen, Ideen, Gesprächszusammenfassungen
- `dokumente/` – längere Texte, Berichte, ausgearbeitete Inhalte
- `memory/`    – Wissen über den Nutzer und laufende Projekte (Vorlieben, Kontext, offene Aufgaben)
- Code/Projekte bekommen bei Bedarf einen eigenen Ordner auf oberster Ebene.

Dateinamen: `JJJJ-MM-TT-kurzer-titel.md` (z. B. `2026-11-06-projektidee.md`).

## Ablauf in jeder Sitzung
1. Zu Beginn `memory/` lesen, um den Kontext zu kennen.
2. Neue Inhalte in den passenden Ordner schreiben.
3. Wichtige neue Erkenntnisse über den Nutzer/Projekte in `memory/` ergänzen.
4. Am Ende (oder nach jedem größeren Schritt) committen und pushen.

## Sprache
Der Nutzer schreibt Deutsch – Antworten und Dateien standardmäßig auf Deutsch.

## Videos generieren (YouTube-Kanal: History / Doku / True History)
Wenn der Nutzer ein Video, eine Videoidee, ein Skript oder eine Caption will:
1. **Zuerst `playbook/VIDEO-PLAYBOOK.md` lesen** – dort stehen Stil, Ablauf, Regeln und Werkzeuge.
2. **Immer diese Skills verwenden** (Wunsch des Nutzers):
   - `/anthropic-skills:ig-viral` – virale Shorts/Reels der Nische finden & nach Ausreißer-Faktor ranken (monatlich / vor Ideen-Runden)
   - `/anthropic-skills:ig-human` – jedes Skript, jede Beschreibung, jeden Kommentar prüfen, bevor der Nutzer ihn sieht
   - `/anthropic-skills:ig-caption` – Beschreibung/Caption, Suchbegriffe, Hashtags
   Deren Prüf-Skripte fehlen in dieser Umgebung → Nachbauten in `video-studio/tools/` nutzen (`swipe.py`, `human_check.py`, `caption_check.py`).
3. **Stil: realistisch & ernst (Doku)** – echte gemeinfreie Gemälde/Karten, `style: doku`. Kein Cartoon (vom Nutzer abgelehnt).
4. Fakten mit Wikipedia/Primärquellen prüfen; Legenden als Legenden kennzeichnen.
4b. **Hook** nach `playbook/HOOKS.md` (5 Varianten, `tools/hook_check.py`), viele Effekte und Bewegung (Playbook §4). Immer mit `--variants` rendern.
4d. **Spannung:** B-Roll-Slides, Dialogfenster, `mood:` pro Szene, Teaser, Blur-Reveal (Playbook §4b). **Jede genannte Kleinigkeit bekommt einen Effekt** (Zähler, Bildwechsel/Großaufnahme beim Wort, Dialog, Stempel), **aber KEINE Emojis** (Nutzer-Wunsch); etwa alle 2 s passiert etwas.
4c. **Musik, Figuren und Bilder IMMER an das Thema anpassen** (Playbook §4a): `era:` festlegen → `music: {score: epoche, era: …}`, echte Porträts der genannten Personen, Bilder aus derselben Zeit und Region. Musik leise (`music_db: 21`, `duck: 0.5`). Phonk unter einem Barock-Thema hat dem Nutzer nicht gefallen.
5. Videos liegen in `videos/JJJJ-MM-TT-titel/` (video.yaml, assets/, output/). Renderer: `video-studio/render.py`.
