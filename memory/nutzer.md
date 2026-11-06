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
