# Ablauf bei „generiere“

Stand: 06.11.2026. Wenn der Nutzer „generiere“ sagt, geht Claude genau so vor.
Details zu jedem Schritt: `VIDEO-PLAYBOOK.md`, `HOOKS.md`.

1. **Kontext lesen:** `memory/nutzer.md`, `playbook/VIDEO-PLAYBOOK.md`, `playbook/HOOKS.md`.
2. **Format wählen:** Story-Doku oder History-Fakten (A: ein Fakt, B: drei Fakten, C: Mythos oder Wahrheit). Abwechseln, etwa 1:1 pro Woche.
3. **Thema wählen:** dunkel, wahr, überraschend. Ideen aus der Swipe-File (`ig-viral`, sonst `tools/swipe.py`) und den Serien.
4. **Fakten prüfen:** nur Belegtes, jede Quelle in `quellen.md`. Legende wird im Video als Legende markiert.
5. **Epoche festlegen:** `era:` bestimmt Musik, Bilder und Farbe (Playbook §4a).
6. **Bilder holen:** gemeinfrei, The Met Open Access oder Wikimedia Commons. Zu jedem Satz ein passendes Bild, mehrere Slides pro Szene.
7. **Hook schreiben:** 5 Varianten, höchstens 9 Wörter, mit Widerspruch.
8. **Hook prüfen:** `tools/hook_check.py`, die beste ab 75/100 kommt durch.
9. **Skript schreiben:** kurze Sätze, du-Form, eine Frage. Das Ende führt zurück zum Anfang (Loop).
10. **Skript prüfen:** `ig-human` (sonst `tools/human_check.py`), keine KI-Wörter, PASS nötig.
11. **Szenen bauen:** etwa alle 2 Sekunden passiert etwas. **Keine Emojis.**
    - Zahl gesagt → Zähler (`count`)
    - Name oder Ding gesagt → Bildwechsel genau beim Wort (`reveal_word`)
    - Gefühl → Dialogfenster mit Emotion
    - Wichtig → Stempel, Spotlight, Kino-Balken
    - Fakten-Format → Zähler „Fakt 1/3“ und Steckbrief-Karte
12. **Farbe pro Szene:** `mood` (gold, kalt, Nacht, Gefahr, traurig, Rätsel).
13. **Musik:** passend zur Epoche (`score: epoche`), leise (`music_db: 21`, `duck: 0.5`).
14. **Rendern:** `render.py --variants` → `video.mp4` und `video_ohne_musik.mp4` (für Trend-Sound in der App).
15. **Selbst prüfen:** Einzelbilder ansehen, Lautstärke messen, Länge 30–60 s.
16. **Caption:** `ig-caption` (sonst `tools/caption_check.py`), 3 Hashtags, Suchbegriffe.
17. **Speichern:** Commit und Push auf den Arbeits-Branch.
18. **Abgeben:** Video schicken, kurzer Bericht mit Hook, Quellen und offenen Punkten.
