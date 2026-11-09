# Daily Task: 3 Videos pro Tag

Stand: 06.11.2026. Wunsch des Nutzers. **Seit 08.11.2026: läuft jeden Abend um 21:37 Uhr (Berlin) und plant die Videos für den NÄCHSTEN Tag ein** (10:00, 16:00, 18:00). Der Nutzer prüft sie abends/morgens im Metricool-Planer und löscht oder ändert bei Bedarf.

## Was verstanden ist
- Jeden Tag **3 neue Videos** (Entscheidung 06.11.2026, vorher 4), Länge **1:10–1:15 Min.** (70–75 s).
- Nische: History / Doku / True History / **historische Fakten** (nur Geschichte), Deutsch, ernster Doku-Look, keine Emojis.
- Jedes Video über **Metricool** auf **YouTube (Short), Instagram (Reel), TikTok** einplanen.
- Brand 7558808 = „Was wirklich geschah“. **Stickman-Accounts nie anfassen.**
- Uhrzeiten: **10:00, 16:00, 18:00** (`POSTING-ZEITEN.md`).

## Freigabe
**Seit 07.11.2026: selbstständig posten, NICHT nachfragen** (Nutzer-Anweisung). Nur bei echten Blockern melden (Kontingent leer, Metricool-Brand falsch, Login/Push kaputt).

## Ablauf jeden Tag
1. Repo holen, `memory/`, `VIDEO-PLAYBOOK.md`, `HOOKS.md`, `GENERIERE.md` lesen.
2. Prüfen: Brand 7558808 zeigt noch „Was wirklich geschah“? Sonst abbrechen und melden.
3. Zahlen von gestern aus Metricool holen (Aufrufe, Retention, Follower). Was lief gut → mehr davon.
4. **3 Themen, 3 Formate pro Tag:** 1 Story-Doku (Bogen nach `REFERENZ-DSCHINGIS.md`), 1 historischer Fakt / Mythos oder Wahrheit, 1 **Top-3-Countdown** (`FORMAT-TOP3.md`, `caption_style: pop`). Kein Thema doppelt (`videos/` prüfen). Verschiedene Epochen.
5. Pro Video **Schritte 3–15 aus `GENERIERE.md`**: Fakten + Quellen, Epoche, Bilder, 5 Hooks + `hook_check`, Skript für 70–75 s (ca. 170–190 Wörter), `ig-human`, Szenen mit Detail-Effekten, Farbe, Epochen-Musik, Rendern, Selbstprüfung.
6. Länge prüfen: 70–75 s. Sonst Text kürzen oder ergänzen und neu rendern.
7. Pro Video: Titel (YouTube), Caption + 3 Hashtags (`ig-caption`), Cover-Bild.
8. Videos online ablegen (öffentlicher Link, Ort noch offen) und alles committen + pushen.
9. In Metricool einplanen (autoPublish: true): Video 1 → 10:00, 2 → 16:00, 3 → 18:00 am NÄCHSTEN Tag. Liegt eine Uhrzeit schon in der Vergangenheit, nächsten freien Slot nehmen (z. B. 12:30). Je ein Post mit allen 3 Netzwerken. YouTube Typ „short“, Kategorie EDUCATION, nicht für Kinder. KI-Kennzeichnung an.
10. Prüfen: `getScheduledPosts` zeigt alle 3 Posts mit Video.
11. Tagesbericht an den Nutzer: 3 Themen, Hooks, Uhrzeiten, Links, Probleme.
12. Fehler (Bild fehlt, Fakt unsicher, Render kaputt) → Video ersetzen statt schlecht posten. Lieber 2 gute als 3 schlechte, und das im Bericht sagen.

## Entscheidungen (06.11.2026)
- **Stimme: ElevenLabs „George“** (`voice: "eleven:george"`, genehmigt). Andere Stimme nur nach Hörprobe + Genehmigung. Key kommt automatisch über das Netzwerk-Secret der Umgebung „satistify“ (kein Code nötig). Gratis-Plan: 10.000 Zeichen/Monat, reicht für ca. 8 Videos. Kontingent vor jedem Lauf prüfen (`/v1/user/subscription`); leer → melden, nicht auf Piper ausweichen ohne Rückfrage.
- **Ablage: eigenes öffentliches GitHub-Repo** für die Videos (Link für Metricool). Videos klein halten (ca. 15–25 MB), alte Videos nach dem Posten aufräumen.

## Offen
- GitHub-Push (403) muss gehen.
- Video-Repo anlegen (Name, öffentlich).
- ElevenLabs-Key und Stimmwahl.

## Erfahrungen Tag 1 (06./07.11.2026)
- **Länge:** George spricht ca. 15,5 Zeichen/s. Für 70–75 s: **1.050–1.150 Zeichen Sprechtext** (ca. 155–185 Wörter), 14–16 Szenen. Zu lang → `pause: 0.12` im yaml (statt 0,22) spart 1–2 s ohne neue Stimme.
- **ElevenLabs-Kontingent** vor dem Start prüfen: `curl -sS https://api.elevenlabs.io/v1/user/subscription -H "xi-api-key: proxy-injected"` (Proxy setzt den echten Key). Rest < 3.600 Zeichen → nur so viele Videos wie möglich, Rest im Bericht melden.
- **Bilder:** Wikimedia-API drosselt oft (429). Erste Wahl: **The Met Open Access** mit `python3 video-studio/tools/met.py search "…"` und `met.py get <IDs> --dir videos/<ordner>/assets` (CC0, Lizenz-JSON automatisch). Danach Dateien kurz umbenennen.
- **Fakten:** `https://en.wikipedia.org/w/index.php?title=<Artikel>&action=raw` funktioniert (Text lesen, Belege prüfen). Unbelegtes im Video als „nicht belegt“ stempeln.
- **Vorschau** mit `--stills` ansehen und Bildausschnitte korrigieren (Gesichter, keine leeren Ränder), dann `--variants` rendern.
- **Caption:** `caption.txt` im Videoordner, Job A (Reel trägt den Hook): Frage + Bitte in Zeile 1, Suchbegriffe im Text, 3 Hashtags, keine typografischen Anführungszeichen (ig-human-Fingerprint). Prüfen mit `caption_check.py` und `human_check.py`.
- **Upload:** Video komprimieren (`ffmpeg -crf 24 -maxrate 3M -bufsize 6M -c:a aac -b:a 160k -movflags +faststart`), nach `Hossein-creator/waswirklich-videos` unter `JJJJ-MM/<name>.mp4` pushen, Raw-Link: `https://raw.githubusercontent.com/Hossein-creator/waswirklich-videos/main/JJJJ-MM/<name>.mp4`. Metricool kopiert die Datei; nach dem Einplanen Dateien älter als 7 Tage löschen.
- **Metricool-Post:** blogId 7558808, providers instagram+youtube+tiktok, `autoPublish: true`, instagramData {type: REEL, isAiGenerated: true}, youtubeData {title, type: short, privacy: public, category: EDUCATION, madeForKids: false, isAiGeneratedContent: true}, tiktokData {privacyOption: PUBLIC_TO_EVERYONE, isAigc: true, title}. Zeitzone Europe/Berlin.
- **Wikimedia blockt oft komplett (429, auch Originaldateien).** Nicht länger als 10 Min. warten: jedes Wikimedia-Bild im yaml mit `fallback:` auf ein Met-Bild absichern und rendern. Host `thumb.wikimedia.org` ist seit 07.11. freigeschaltet (`https://commons.wikimedia.org/wiki/Special:FilePath/<Datei>?width=1280` leitet dorthin um).
- **Rang-Karten im Top-3-Format:** Kapitel-Bild + `spotlight` (dark 0.7) + `title` Größe 170, sonst ist der Titel auf hellen Stichen kaum lesbar.
- **Länge nach `say` messen, nicht nach `text`:** Ausgeschriebene Jahreszahlen („siebzehnhundertsechzig“) verlängern den Sprechtext. Probe Top-3 (07.11.) hatte 1.120 Zeichen `text`, aber ~1.250 Zeichen `say` → 79 s statt 75. Ziel: **max. 1.100 Zeichen Sprechtext inklusive ausgeschriebener Zahlen.**
- **Caption-Linter:** „Schreib es in die Kommentare“ zählt doppelt als Bitte (zwei Muster). Immer „Schreib's in die Kommentare“ verwenden.
