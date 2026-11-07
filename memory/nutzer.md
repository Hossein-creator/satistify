# Nutzer

- Sprache: Deutsch
- Wunsch (2026-11-06): Dieses Repo dient als Claudes Speicherplatz – alles Geschriebene wird hier gespeichert.

## Laufende Projekte / Interessen
- 2026-11-06: Interesse an einem **faceless YouTube-Kanal**, Ziel: schnell Abonnenten und schnell Geld.
  Recherche-Bericht: `dokumente/reports/Profitabelste faceless YouTube Nischen.md`
  (Notizen in `dokumente/research_notes/Profitabelste faceless YouTube Nischen/`).
  Kernempfehlung: Deutsch als Hauptsprache, Nischen mit Kaufabsicht (1. Finanzen DACH,
  2. Software-/KI-Tool-Tutorials, 3. Bildungs-/Business-Dokus), Affiliate vor Werbung,
  Langform statt Shorts (YPP ab 01.02.2027: 8.000 Std.).
  Offen: Hat der Nutzer Finanz-Fachwissen? Welche Nische wird gewählt? Zeit/Budget pro Woche?

## Entscheidung Nische (2026-11-06)
- Gewählt: **History / Doku / True (Crime) History / Fakten-History**.
- Vorbild-Kanäle: Extra History, Historically (@HeyHistorically), Build A Better You, Mapfusion.
- Analyse: `dokumente/2026-11-06-analyse-history-kanaele.md` (Rohdaten in `dokumente/daten/2026-11-06-history-kanaele/`).
- Kern: Story statt Liste, Humor, Serien, Shorts für Abos + lange „Die GANZE Geschichte von …“-Videos fürs Geld, „[Ohne KI]“ als Markenversprechen.
- Offen: Zeit/Budget pro Woche, eigene Stimme ja/nein.

## Technik-Notiz
- `yt-dlp` funktioniert hier für Metadaten und Untertitel; Videostreams sind gesperrt.

## Video-Produktion (Stand 2026-11-06)
- Nutzer will, dass Claude die Videos **selbst generiert**. Ablauf und Regeln: `playbook/VIDEO-PLAYBOOK.md` (in CLAUDE.md verankert).
- **Stil-Entscheidung:** realistisch, ernst, Doku-Vibe (echte gemeinfreie Gemälde, filmischer Look). Abgelehnt: Strichmännchen ("langweilig") und bunter Cartoon.
- **Skills immer nutzen:** ig-viral, ig-human, ig-caption (letzte Nachricht endete mit "und …" – evtl. ein vierter Skill gemeint, nachfragen).
- Erstes Video: `videos/2026-11-06-kartoffel-trick/` (Friedrich der Große & Kartoffelbefehl, Doku-Short).
- Eigene Cloud-Umgebung "satistify" angelegt (Wikimedia/Wikipedia freigeschaltet, Setup-Skript installiert Tools + Stimme).
- 2026-11-06: Weitere Vorbild-Kanäle vom Nutzer: Absolute History, Extra History (Shorts), InfiniteCracker → Analyse `dokumente/2026-11-06-analyse-kanaele-2.md`. Kern: feste Serien + makabre Themen; Serien-Ideen ins Playbook übernommen.
- 2026-11-06 Feedback zum Kartoffel-Video: „sieht gut aus“, Stil behalten. Musik war **zu laut** → jetzt `music_db: 17.5` + `duck: 0.45` (≈6 dB leiser). Musik muss **Trend** sein → selbst komponierte Trend-Sounds (`video-studio/beats.py`: Dark Phonk / Trailer). **Mehr Effekte und Motion** (Punch-In, Whip, Stempel, Schreibmaschine, Nebel, Spotlight, Handkamera, Beat-Pulse). **Hook weiter verbessern** → `playbook/HOOKS.md` + `tools/hook_check.py`.
- 2026-11-06 Feedback v4: Video „sehr gut“, Effekte/Hook bleiben. **Phonk passte gar nicht zum Thema** → Regel: **Musik, Figuren und Bilder immer an Thema/Epoche anpassen** (`era:` + `video-studio/epochen.py`, Tabelle im Playbook §4a). Musik **noch leiser**: jetzt `music_db: 21`, `duck: 0.5`.
- 2026-11-06 Wunsch: mehr Spannung bis zum Ende → B-Roll-Slides, Dialogfenster mit Emotion, Farbstimmung pro Szene, Neugier-Leiste, Blur-Reveal, Kino-Balken (Playbook §4b). Bildquelle zusätzlich: The Met Open Access.
- 2026-11-06 Wunsch: auf Kleinigkeiten achten – jedes genannte Detail bekommt Effekt/Emoji/Szene, „richtig unterhaltsam“ → emoji/count-Elemente + auto_emoji (Playbook §4b).
- 2026-11-06 Korrektur: **KEINE Emojis** im Video. Details stattdessen mit ernsten Effekten (count, Bildwechsel beim Wort, dialog, stamp, mark).
- 2026-11-06: **History-Fakten** als zweite Nischen-Säule hinzugefügt (Fakten-Shorts neben Story-Dokus). Formate A/B/C im Playbook §2a.
- 2026-11-06: Ablauf bei „generiere“ als Schrittliste gespeichert: `playbook/GENERIERE.md`.
- 2026-11-06: **Bestehende Accounts (über Metricool, Brand-ID 7558808):** Instagram `silent.stickman`, TikTok `the.silent.stickman`, YouTube-Kanal `UC4FOhemWxnUaBZMC9kNwOvA`.
  Inhalt dort: **englische Strichmännchen-Reels zu Liebe/Beziehung/Motivation** (nicht History!). Seit 23.10.2026: 1 → ca. 2.700 Follower; Top-Reel 7,7 Mio. Aufrufe (27.10.), mehrere 200–500 Tsd.
  **REGEL (Nutzer, 06.11.2026): Stickman-Accounts NICHT anfassen** – nichts ändern, nichts posten, nicht bewerten.
  Für History hat der Nutzer einen **neuen Account** angelegt: **„Was wirklich geschah“** – Instagram `waswirklich.geschah`, TikTok „Was wirklich geschah | History“, YouTube `UCZdQXYT8J0nuppF8BjVrxbg`. Seit 06.11. in derselben Metricool-Brand 7558808 verbunden (Stickman ist dort nicht mehr verbunden).
- 2026-11-06: Wunsch **Daily Task: 4 Videos pro Tag, je 1:10–1:15 Min., über Metricool auf YouTube, Instagram, TikTok posten.** Zeiten: `playbook/POSTING-ZEITEN.md` (10, 12, 16, 18 Uhr).
- 2026-11-06 Klarstellung: Fakten = **nur historische Fakten** (keine allgemeinen Fakten).
- 2026-11-06 Entscheidungen Daily Task: **3 Videos pro Tag** (nicht 4). **Stimme: ElevenLabs**, aber die Stimme lässt der Nutzer vorher **genehmigen** (Hörproben schicken). **Videos in eigenem GitHub-Repo** ablegen (öffentlicher Link für Metricool).
- 2026-11-06 **Stimme: ElevenLabs „George“ – nach Testvideo vom Nutzer GENEHMIGT („ja“)** (voice_id JBFqnCBsd6RMkjVDRZzb, Standard-Stimme, Modell eleven_multilingual_v2), im yaml `voice: "eleven:george"`. Nutzer bleibt vorerst im **Gratis-Plan** (10.000 Zeichen/Monat ≈ 8 Videos). Empfehlung Claude: Creator-Plan + deutsche Stimme „Alexander – Deep TV Narrator“ (kkJxCnlRCckmfFvzDW5Q, nur Bezahl-Plan). Key ist als **Netzwerk-Secret der Cloud-Umgebung „satistify“** gespeichert (Host api.elevenlabs.io, Header xi-api-key, Proxy setzt ihn ein); **nie im Repo**. Renderer nutzt Platzhalter `proxy-injected`. Host api.elevenlabs.io in Umgebung „satistify“ freigeschaltet.
- 2026-11-06: Video-Ablage **Hossein-creator/waswirklich-videos** (öffentlich, Push geht). Raw-Link `https://raw.githubusercontent.com/Hossein-creator/waswirklich-videos/main/<pfad>.mp4` wird von Metricool angenommen; **Metricool kopiert das Video auf static.metricool.com** → Datei im Repo darf nach dem Einplanen gelöscht werden. Videos für Upload mit crf 24 / maxrate 3M komprimieren (~28 MB pro 70 s). Test-Entwurf in Metricool: Post-ID 419428043 (08.11., Entwurf, privat) – Nutzer soll ihn löschen.
- 2026-11-06: George-Test: Kartoffel-Video mit George = 69,2 s (George spricht langsamer als Thorsten).
- **2026-11-07 FREIGABE: Claude postet ab jetzt selbstständig und regelmäßig, OHNE Rückfrage** („ab jetzt brauchst du meine ja nicht mehr und frage mich auch nicht mehr“). Gilt für die tägliche Aufgabe (3 Videos/Tag über Metricool).
- 2026-11-07: Erste 3 Videos eingeplant (Metricool-IDs 419830990 Napoleon 12:30, 419831054 Mumia 16:00, 419831126 Tanzwut 18:00). ElevenLabs danach: 4.437 / 10.000 Zeichen verbraucht.
- 2026-11-07: **Tägliche Aufgabe** angelegt: „Taegliche History-Videos“ (trig_0115RRkWZGXF2QRWx1NJ62P2), jeden Tag 04:37 Uhr Berlin, läuft in der Sitzung session_01CRoryTSAfZb5YsHu1gsecv (nur dort ist der Metricool-Connector verfügbar; Trigger mit neuer Sitzung pro Lauf bekommen in dieser Organisation keine Connectoren). Anweisung: nur nach Repo arbeiten (playbook/DAILY.md).
- 2026-11-07: ElevenLabs-Gratis-Kontingent reicht noch für ca. 4–5 Videos (Reset erst 07.12.2026). Danach braucht es Bezahl-Plan oder neuen Key (Hinweis an Nutzer: mehrere Gratis-Konten verstoßen gegen ElevenLabs-Regeln).
- 2026-11-07: Nutzer schickte Referenzvideo (Dschingis Khan, TikTok, KI-Illustration). Regeln + neue Effekte übernommen und in unseren realistischen Stil übertragen: `playbook/REFERENZ-DSCHINGIS.md` (blackcard, triptych, spread, ghost, glow, mood blood).
- 2026-11-07: Zweites Referenzvideo (@surprising.facts6, „The 3 historical events that changed the world“) = Nische **History-Countdown / Top 3** (Teil von „historische Fakten“). Nutzer will genau solche Videos auch → Format D, `playbook/FORMAT-TOP3.md`, neuer Untertitel-Stil `caption_style: pop`. Tägliche Rotation jetzt: Story-Doku + Fakt + Top-3.
- 2026-11-07: Demo-Video der Referenz-Effekte (Entwurfsstimme, gemischte Bilder, rote Augen, Geister, brennende Karte) hat dem Nutzer **gar nicht gefallen** (Stimme und alles). Diese Effekte nicht ungefragt einsetzen; Glow auf Porträts und Geister vermeiden. Nie wieder Demos mit Entwurfsstimme zeigen.
