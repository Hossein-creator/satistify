# Video-Playbook: History / Doku / True History (Deutsch)

Stand: 06.11.2026. Pflichtlektüre vor jedem neuen Video. Quellen: Kanal-Analyse, drei Recherchen und die Swipe-File (Links unten).

## 0. Entscheidungen des Nutzers (nicht neu verhandeln)
- **Nische:** History, Doku, True (Crime) History, Fakten-History.
- **Stil:** **realistisch und ernst, im Doku-Look.** Echte historische Gemälde, Karten und Stiche, filmische Farbe, ruhige Kamerafahrten. Die Zuschauer sollen sofort neugierig werden. **Kein Cartoon, keine Strichmännchen.** Der Nutzer hat beides abgelehnt.
- **Skills immer verwenden:** `ig-viral` (Recherche), `ig-human` (jeder Text), `ig-caption` (Beschreibung/Caption).
- **Sprache:** Deutsch (DACH). Englisch nur auf Wunsch.

## 1. Ablauf für jedes Video

| Schritt | Was | Werkzeug |
|---|---|---|
| 1 | **ig-viral:** monatlich bzw. vor jeder Ideen-Runde virale History-Shorts sammeln und nach Ausreißer-Faktor ranken | `python3 video-studio/tools/swipe.py collect @kanal … --out recherche/swipe/DATUM-captured.tsv`, dann `rank … --out recherche/swipe/DATUM-swipe.md` |
| 2 | **Thema und Formel wählen** aus der Swipe-File (Abschnitt „Deine Versionen“) | `recherche/swipe/` |
| 3 | **Fakten prüfen** mit Wikipedia und Primärquellen; Legenden als Legenden kennzeichnen | Wikipedia-API (siehe §6) |
| 4 | **Skript schreiben** (§3) in `videos/DATUM-titel/video.yaml` | Vorlage: `videos/2026-11-06-kartoffel-trick/video.yaml` |
| 5 | **ig-human:** Skript, Beschreibung und angehefteten Kommentar prüfen; erst bei PASS weiter | `python3 video-studio/tools/human_check.py skript.txt` |
| 6 | **Bilder holen:** nur gemeinfrei (PD/CC0) | `python3 video-studio/tools/commons.py search "…"` / `get "File:…" --dir videos/…/assets` |
| 7 | **Vorschau** prüfen (Bildausschnitte, Texte, Untertitel) | `python3 video-studio/render.py videos/…/video.yaml --stills` |
| 8 | **Rendern** | `python3 video-studio/render.py videos/…/video.yaml` |
| 9 | **ig-caption:** Beschreibung bzw. Caption mit 2–3 Suchbegriffen, ≤ 5 Hashtags, genau einer Bitte | `python3 video-studio/tools/caption_check.py caption.txt --keywords "…" --platform youtube` |
| 10 | **Speichern:** committen und pushen; Erkenntnisse in `memory/` ergänzen | git |

Die Original-Skripte der Skills (`humanize.py`, `detect.py`, `caption.py`, `swipe.py`) sind in dieser Umgebung nicht vorhanden. Die Werkzeuge in `video-studio/tools/` bauen sie nach den Regeln der Skills nach, auf Deutsch angepasst. Es sind lokale Heuristiken, keine KI-Detektoren.

## 2. Format und Länge
- **Shorts:** 45–75 s, 9:16 (1080×1920), 120–170 Wörter. Shorts bringen vor allem Abonnenten; ihr RPM liegt bei nur 3–14 % des Langform-RPM.
- **Langform** ab 2027 wichtiger, denn **ab 01.02.2027 verlangt das Partnerprogramm 8.000 Stunden Wiedergabezeit** (oder 20 Mio. Shorts-Aufrufe in 90 Tagen). Gute Formate sind 20–40 Min. „Die ganze Geschichte von …“ und „Complete“-Zusammenschnitte von Serien.
- Rechenbeispiel: 20 Min. bei 35 % Wiedergabedauer brauchen ca. 69.000 Aufrufe pro Jahr, um 8.000 Stunden zu erreichen.
- Sprechtempo Deutsch: **130–150 Wörter/Min.**

## 3. Skript-Regeln (aus Kanal-Analyse und Recherche)
1. **Der erste Satz ist der Hook** und sagt die Titelbehauptung. Keine Begrüßung, kein „In diesem Video“.
2. **Ein Bogen pro Short:** Ausgangslage, Problem, Wendung, Pointe oder Twist.
3. **Konkrete Zahlen, Namen und Daten** wie „15 Erlasse“, „24. März 1756“.
4. **Ernster, ruhiger Erzählton** wie bei Terra X oder MrWissen2go. Spannung entsteht durch Fakten und Stakes, nicht durch Witze.
5. **Re-Hook alle 20–30 s** bei Shorts und alle 45–90 s bei Langform (offene Frage, „Doch …“, „Und hier beginnt …“).
6. **Legenden ehrlich als Legenden markieren.** Das ist selbst ein starker Twist („Nur: Belegt ist er nicht.“).
7. **Ende:** genau eine Frage an die Zuschauer (bringt Kommentare). Ideal ist ein Loop zurück zum Anfang.
8. **Langform:** Sponsor bzw. Pause direkt nach einem Cliffhanger („Doch bevor wir dazu kommen …“). Am Ende auf das nächste passende Video verweisen statt um Abos zu bitten.

### Hook-Formeln, die bei seriösen History-Kanälen funktionieren (Swipe 06.11.2026)
| Formel | Beispiel (Kanal, Ausreißer-Faktor) | Unsere Version |
|---|---|---|
| Paradox/Warum | „Warum das alte Königsberg zu Russland gehört“ (MrWissen2go, 4,1x) | „Warum Friedrich der Große Kartoffeln bewachen ließ“ |
| Dunkle Figur | „War Amon Göth noch grausamer als im Film?“ (MrWissen2go, 6,5x) | „Fritz Haarmann: Wie konnte die Polizei ihn so lange übersehen?“ |
| Genialer Gauner | „Der Hauptmann von Köpenick: Genialer Verbrecher?“ (Terra X, 5,0x) | „Ein Schuster in Uniform: Wie der Hauptmann von Köpenick ein Rathaus eroberte“ |
| Kuriose Technik | „Maus Tank: Outrun by a Jogging Soldier“ (Simple History, 16,5x) | „Die Dicke Bertha: Das Geschütz, das Festungen zerlegte“ |
| Heute-Bezug | „Was hat die Schweiz gegen Liechtenstein?“ (Terra X, 7,9x) | „Warum Kaliningrad einmal Königsberg hieß“ |
| Was-wäre-wenn / Countdown | „What if Germany won WW2“, „60s before NUKE“ (Historically, je 28 Mio.) | „60 Sekunden vor dem Ausbruch des Vesuvs“ |

**Deutsches Titel-Muster:** `Thema: provokante Frage?`, z. B. „Kartoffelbefehl: Was an der Legende wirklich dran ist“. Titel kurz halten; oben in der Swipe-File haben Hooks im Median 6 Wörter.

## 4. Bild und Ton (Doku-Stil, `style: doku`)
- **Bilder:** gemeinfreie Gemälde, Stiche, Karten und Porträts von Wikimedia Commons. Wechsel alle 3–6 s, dazu langsame Kamerafahrten auf Details (Gesichter, Hände, Gegenstände).
- **Look:** leicht entsättigt, mehr Kontrast, warme Lichter und kühle Schatten, Vignette, Filmkorn, Staub. Macht `doku.grade` automatisch.
- **Typografie:** Cinzel für Orte, Daten und Titelkarten; Bauchbinde für Personen (Name plus Funktion und Lebensdaten); Untertitel in Montserrat, weiß, aktives Wort gold.
- **Übergänge:** Überblendung 0,45 s. Bei Twists `transition: flash` plus `hit: true` (tiefer Schlag). Für Spannung `heartbeat: true`.
- **Musik:** dunkler, synthetischer Klangteppich (`music: dark`, lizenzfrei). Eigene Musik nur aus der YouTube Audio Library, oder Epidemic Sound mit verknüpftem Kanal.
- **Ton:** um −14 LUFS, True Peak −1,5 dB. `render.py` normalisiert automatisch.
- **Stimme:** Die eingebaute „Thorsten“-Stimme (CC0) ist nur ein **Entwurf**. Für den Upload besser die **eigene Stimme** über `aufnahme/szene_XX.wav`, siehe `output/aufnahme-skript.md` (menschlicher, sicherer bei der „inauthentic content“-Regel) oder eine hochwertige Sprecherstimme per API. Die englische Piper-Stimme „Ryan“ ist **nicht kommerziell** nutzbar (CC BY-NC-SA).

## 5. Verpackung (Titel, Thumbnail, Beschreibung)
- **Test & Compare:** bis zu 3 Titel- bzw. Thumbnail-Varianten. Gewinner ist die Variante mit dem größten Anteil an Wiedergabezeit, nicht die höchste CTR.
- **CTR:** meist 2–10 %; für Doku gelten 3,5–8 % als normal.
- **Thumbnail (Langform):** höchstens 3 Bildelemente, ein Gesicht mit Emotion (Gemälde-Porträt), 2–4 Wörter, muss den „Glance Test“ bestehen.
- **Shorts:** erstes Bild nie leer, Hook in den ersten 1–3 s. Der Anteil „angesehen statt weggewischt“ sollte über 70 % liegen; unter 50 % den Einstieg ändern.
- **Beschreibung:** Suchbegriffe als normale Sätze in den ersten Zeilen, Quellen und Bildnachweise am Ende (schreibt `render.py` in `upload.md`), höchstens 5 Hashtags. Tags spielen kaum eine Rolle.
- **Kapitel** (Langform): 00:00 als Start, mindestens 3 Kapitel, jedes mindestens 10 s.
- **Mehrsprachige Tonspur und Auto-Dubbing:** großer Reichweiten-Hebel für einen deutschen Kanal. Affiliate-Links funktionieren in Dub-Spuren aber nicht.

## 6. Recht und Richtlinien (Deutschland, keine Rechtsberatung)
- **„Inauthentic content“** (seit 15.07.2025): YouTube bestraft Massenware nach Schablone, bei der nur das Thema wechselt. Deshalb pro Video eigene Recherche, eigener Erzählbogen und wechselnde Formeln. Faceless und KI-Werkzeuge sind erlaubt, Fließband-Videos nicht.
- **KI-Kennzeichnung:** nötig für realistische KI-Bilder, -Videos oder -Stimmen echter Personen. Bei Gemälden und eigener Stimme ist keine Kennzeichnung nötig. Seit 02.08.2026 gilt zusätzlich Art. 50 EU AI Act für Deepfakes.
- **Bildrechte:** Ein Werk ist 70 Jahre nach dem Tod des Urhebers gemeinfrei (§ 64 UrhG). Originalgetreue Fotos gemeinfreier 2D-Werke sind seit 2021 frei (§ 68 UrhG). **CC BY-SA vermeiden**, wegen Weitergabe-Pflicht und Namensnennung.
- **§ 86a StGB:** Hakenkreuz und andere NS-Kennzeichen nur mit eindeutig ablehnender, aufklärender Einordnung (§ 86 Abs. 4). **Nie im Thumbnail oder ohne Kontext in Shorts.**
- **Werbefreundlichkeit:** Seit Januar 2026 können nicht-grafische Darstellungen sensibler Themen wieder voll monetarisiert werden. Grafische Gewalt im Bild vermeiden; True Crime sachlich erzählen.
- **True Crime:** Bei jüngeren Fällen Persönlichkeitsrechte von Opfern und Angehörigen beachten. Lieber historische Fälle (vor 1950).
- **Impressum** (§ 5 DDG), sobald der Kanal monetarisiert ist. Werbung und Affiliate-Links kennzeichnen.

## 7. Technik-Notizen
- Umgebung „satistify“ (Cloud): erlaubt YouTube, Wikimedia, Wikipedia und support.google.com. Das Setup-Skript installiert yt-dlp, piper-tts, pyyaml und die Stimme.
- Wikimedia drosselt schnelle Anfragen; `commons.py` wartet automatisch. Bilder kommen über upload.wikimedia.org.
- Stile im Renderer: `style: doku` (Standard für diesen Kanal), Cartoon (abgelehnt, nur als Fallback).

## Quellen dieses Playbooks
- Kanal-Analyse: `dokumente/2026-11-06-analyse-history-kanaele.md`
- Recherche Nischen und Geld: `dokumente/reports/Profitabelste faceless YouTube Nischen.md`
- Recherche Erfolgskriterien: `dokumente/research_notes/Erfolgskriterien für History Videos/` (Skript/Retention, Packaging/Algorithmus, Produktion/Recht)
- Swipe-File: `recherche/swipe/2026-11-06-swipe.md`
