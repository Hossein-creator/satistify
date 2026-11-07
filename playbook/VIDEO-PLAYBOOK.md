# Video-Playbook: History / Doku / True History (Deutsch)

Stand: 06.11.2026. Pflichtlektüre vor jedem neuen Video. Quellen: Kanal-Analyse, drei Recherchen und die Swipe-File (Links unten).

## 0. Entscheidungen des Nutzers (nicht neu verhandeln)
- **Nische:** History, Doku, True (Crime) History und **historische Fakten** (History-Fakten: nur Fakten aus der Geschichte, keine allgemeinen Fakten; eigene Säule seit 06.11.2026, siehe §2a).
- **Stil:** **realistisch und ernst, im Doku-Look.** Echte historische Gemälde, Karten und Stiche, filmische Farbe, ruhige Kamerafahrten. Die Zuschauer sollen sofort neugierig werden. **Kein Cartoon, keine Strichmännchen.** Der Nutzer hat beides abgelehnt.
- **Skills immer verwenden:** `ig-viral` (Recherche), `ig-human` (jeder Text), `ig-caption` (Beschreibung/Caption).
- **Sprache:** Deutsch (DACH). Englisch nur auf Wunsch.
- **Alles passt zum Thema (Regel vom 06.11.2026):** Musik, Figuren und Bilder werden **für jedes Video an Thema, Epoche und Ort angepasst**. Phonk unter Friedrich dem Großen passte laut Nutzer „gar nicht“. Siehe §4a.

## 1. Ablauf für jedes Video

| Schritt | Was | Werkzeug |
|---|---|---|
| 1 | **ig-viral:** monatlich bzw. vor jeder Ideen-Runde virale History-Shorts sammeln und nach Ausreißer-Faktor ranken | `python3 video-studio/tools/swipe.py collect @kanal … --out recherche/swipe/DATUM-captured.tsv`, dann `rank … --out recherche/swipe/DATUM-swipe.md` |
| 2 | **Thema und Formel wählen** aus der Swipe-File (Abschnitt „Deine Versionen“) | `recherche/swipe/` |
| 3 | **Fakten prüfen** mit Wikipedia und Primärquellen; Legenden als Legenden kennzeichnen | Wikipedia-API (siehe §6) |
| 4 | **Skript schreiben** (§3) in `videos/DATUM-titel/video.yaml` | Vorlage: `videos/2026-11-06-kartoffel-trick/video.yaml` |
| 4b | **Hook:** 5 Varianten schreiben, bewerten, die beste nehmen (Regeln: `playbook/HOOKS.md`) | `python3 video-studio/tools/hook_check.py video.yaml --text "…"` |
| 5 | **ig-human:** Skript, Beschreibung und angehefteten Kommentar prüfen; erst bei PASS weiter | `python3 video-studio/tools/human_check.py skript.txt` |
| 6 | **Bilder holen:** nur gemeinfrei (PD/CC0) | `python3 video-studio/tools/commons.py search "…"` / `get "File:…" --dir videos/…/assets` |
| 7 | **Vorschau** prüfen (Bildausschnitte, Texte, Untertitel) | `python3 video-studio/render.py videos/…/video.yaml --stills` |
| 8 | **Rendern** (mit Varianten: ohne Musik und zweite Trend-Musik) | `python3 video-studio/render.py videos/…/video.yaml --variants` |
| 9 | **ig-caption:** Beschreibung bzw. Caption mit 2–3 Suchbegriffen, ≤ 5 Hashtags, genau einer Bitte | `python3 video-studio/tools/caption_check.py caption.txt --keywords "…" --platform youtube` |
| 10 | **Speichern:** committen und pushen; Erkenntnisse in `memory/` ergänzen | git |

Die Original-Skripte der Skills (`humanize.py`, `detect.py`, `caption.py`, `swipe.py`) sind in dieser Umgebung nicht vorhanden. Die Werkzeuge in `video-studio/tools/` bauen sie nach den Regeln der Skills nach, auf Deutsch angepasst. Es sind lokale Heuristiken, keine KI-Detektoren.

## 2. Format und Länge
- **Shorts:** 45–75 s, 9:16 (1080×1920), 120–170 Wörter. Shorts bringen vor allem Abonnenten; ihr RPM liegt bei nur 3–14 % des Langform-RPM.
- **Langform** ab 2027 wichtiger, denn **ab 01.02.2027 verlangt das Partnerprogramm 8.000 Stunden Wiedergabezeit** (oder 20 Mio. Shorts-Aufrufe in 90 Tagen). Gute Formate sind 20–40 Min. „Die ganze Geschichte von …“ und „Complete“-Zusammenschnitte von Serien.
- Rechenbeispiel: 20 Min. bei 35 % Wiedergabedauer brauchen ca. 69.000 Aufrufe pro Jahr, um 8.000 Stunden zu erreichen.
- Sprechtempo Deutsch: **130–150 Wörter/Min.**

## 3. Skript-Regeln (aus Kanal-Analyse und Recherche)
1. **Der erste Satz ist der Hook** und sagt die Titelbehauptung. Keine Begrüßung, kein „In diesem Video“. **Alle Hook-Regeln: `playbook/HOOKS.md`.**
2. **Ein Bogen pro Short:** Ausgangslage, Problem, Wendung, Pointe oder Twist.
3. **Konkrete Zahlen, Namen und Daten** wie „15 Erlasse“, „24. März 1756“.
4. **Ernster, ruhiger Erzählton** wie bei Terra X oder MrWissen2go. Spannung entsteht durch Fakten und Stakes, nicht durch Witze.
5. **Re-Hook alle 20–30 s** bei Shorts und alle 45–90 s bei Langform (offene Frage, „Doch …“, „Und hier beginnt …“).
6. **Legenden ehrlich als Legenden markieren.** Das ist selbst ein starker Twist („Nur: Belegt ist er nicht.“).
7. **Ende = Loop:** Der letzte Satz führt in den ersten (endet z. B. mit „:“), das letzte Bild gleicht dem ersten. Die Frage an die Zuschauer steht dann als Titelkarte im Bild und im angehefteten Kommentar.
9. **Sprech-Stil:** ab und zu „du“, eine echte Frage, Umgangssprache („gibt's“, „ja“, „mal“). Sonst fällt das Skript bei ig-human durch (VOICE).
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

### Serien sind der stärkste Hebel (Analyse 2: Absolute History, Extra History, InfiniteCracker)
Details: `dokumente/2026-11-06-analyse-kanaele-2.md`
- **Feste Serien mit Namen und Teilnummer** bringen bei allen drei Kanälen 7x bis 16x des Kanal-Medians. Beispiele: „Worst ways to die (part N)“ mit bis zu 36 Mio. Aufrufen, „One bizarre fact about every US president“, „Worst Dads in History“, „Countries Now vs Then“.
- **Dunkel, makaber und eklig schlägt positiv und romantisch:** „Best Days in History“ liegt bei 0,4x, Romantik bei 0,4x.
- **Werbe-Shorts und Kooperationen** liegen bei 0,2x. Sponsoren gehören in die Beschreibung oder ins lange Video.
- **Aufbau Serien-Short:** Serienname plus Versprechen im 1. Satz, dann 3 Fälle mit konkreten Fakten und einer trockenen Pointe je Fall. Nach jedem Fall eine **wiederkehrende Steckbrief-Karte** („ERFURT · 1184 · TOD IN DER LATRINE“). Am Ende Pointe oder Meinungsfrage.
- **Titel-Schema:** `Kurzer provokanter Titel | Serienname`. In der Beschreibung immer auf Teil 2 bzw. die lange Folge verweisen.
- **Unsere Serien:** „Die seltsamsten Tode der Geschichte“, „Die grausamsten Strafen der Geschichte“ (ohne grafische Bilder), „Ein kurioser Fakt über jeden preußischen König“, „Die schlimmsten Väter der Geschichte“, „Das ist …“ (Objekt mit Museumsfoto), „Damals vs. heute“ (Karte), „Ekel-Geschichte“.
- **Nicht übernehmen:** parteiische Tagespolitik (Extra History „Recently Deleted“), Like-Köder („Like if your country is here“) und Countryballs (0,3x).

### §2a History-Fakten (zweite Säule, Wunsch vom 06.11.2026)
Kurze Shorts mit **historischen Fakten** neben den Story-Dokus. **Nur Geschichte:** keine Wissenschafts-, Tier-, Psycho- oder Allgemein-Fakten. Jeder Fakt hat ein Datum oder eine Epoche, einen Ort oder eine historische Person. Gleicher Stil: echt, ernst, Doku-Look, keine Emojis.
- **Format A, ein Fakt (20–35 s):** Behauptung als Hook, dann Beweis mit Bild oder Objekt, Datum und Ort. Am Ende ein Twist oder Loop. Beispiel: „Napoleon war nicht klein.“ → Maße in Zoll und cm → Grund der Legende.
- **Format B, drei Fakten (35–55 s):** „3 historische Fakten über …, die dir keiner erzählt“. Jeder Fakt hat eine eigene Steckbrief-Karte und einen Zähler (`counter` „Fakt 1/3“). Der stärkste Fakt kommt zuletzt.
- **Format C, Mythos oder Wahrheit:** Mythos nennen, Stempel `Falsch` / `Wahr` / `Nicht belegt`, dann die echte Geschichte.
- **Pflicht:** Jeder Fakt hat eine Quelle in `quellen.md` (Museum, Wikipedia mit Beleg, Fachbuch). Was nicht belegt ist, wird nicht als Fakt gezeigt.
- **Serien:** „History-Fakten (Teil N)“, „Mythos oder Wahrheit?“, „Ein Fakt über jeden preußischen König“, „Das ist …“ (Objekt).
- **Titel-Schema:** `Behauptung | History-Fakten`.
- **Mischung pro Woche:** etwa 1 Fakten-Short auf 1 Story-Doku, danach nach den Zahlen in YouTube Studio anpassen.


**Deutsches Titel-Muster:** `Thema: provokante Frage?`, z. B. „Kartoffelbefehl: Was an der Legende wirklich dran ist“. Titel kurz halten; oben in der Swipe-File haben Hooks im Median 6 Wörter.

## 4. Bild und Ton (Doku-Stil, `style: doku`)
- **Bilder:** gemeinfreie Gemälde, Stiche, Karten und Porträts von Wikimedia Commons. Wechsel alle 3–6 s, dazu langsame Kamerafahrten auf Details (Gesichter, Hände, Gegenstände).
- **Look:** leicht entsättigt, mehr Kontrast, warme Lichter und kühle Schatten, Vignette, Filmkorn, Staub. Macht `doku.grade` automatisch.
- **Typografie:** Cinzel für Orte, Daten und Titelkarten; Bauchbinde für Personen (Name plus Funktion und Lebensdaten); Untertitel in Montserrat, weiß, aktives Wort gold.
- **Bewegung (immer an):** Handkamera (`handheld: 0.7`), leichte Drehung (`rot: [a, b]` in Grad), Projektor-Flackern (`flicker`), Lichteinfall bei Szenenwechseln (`leaks: 0.1`). Beim Hook `ease: out` (schneller Start).
- **Treffer (`hit: true`):** Punch-In-Zoom, Zoom-Unschärfe, RGB-Versatz, Kamerawackler, Impact-Schlag, und die Musik setzt einen Schlag vorher aus.
- **Übergänge (`transition:`):** `fade` (Standard), `whip` (Wischschwenk mit Bewegungsunschärfe), `zoom` (Zoom-Durchflug), `burn` (Filmbrand/Lichteinfall), `flash` (weißer Blitz, für Twists), `cut`. Abwechseln, etwa alle 2–3 Szenen ein `whip` oder `zoom`.
- **Effekt-Elemente (`visual:`):** `stamp` (Stempel knallt aufs Bild: NICHT BELEGT, ECHT, LEGENDE), `date` (Schreibmaschine mit Tippgeräusch), `title` (Buchstaben ziehen sich zusammen), `lower` (Bauchbinde), `spotlight` (Blick auf ein Detail lenken), `fog` (Nebel/Rauch), `embers` (Glut/Funken bei Krieg und Feuer), `dust`, `mark`. Foto mit `night: true` wirkt wie bei Nacht.
- **Beat-Sync:** Bei Trend-Musik pulsiert das Bild leicht auf der Kick (`beat_bump: 0.01`).
- **Musik zuerst nach Thema wählen (§4a, `epochen.py`).** Trend-Sounds (`beats.py`) nur, wenn sie zum Thema passen:
  - `music: {score: phonk, tempo: 118, key: D, drop_scene: 1}`: **Dark Phonk**, 2025/26 der meistgenutzte Sound in Shorts-Edits (Cowbell-Riff, 808 mit Slides, Hi-Hat-Rolls). Standard für Hook-starke Shorts.
  - `music: {score: trailer, tempo: 96}`: **Trailer/Doku-Spannung** (Ticken, Puls, Braams, Taikos). Für ernste Themen wie Krieg, Tod oder True Crime.
  - `music: {score: dark|mystery|epic|sad|hope}`: alte Orchester-Variante (`music.py`).
  - Die Musik folgt dem Video: Hook nur Riff → **Drop auf Szene 2** → Pause vor jedem `hit` → nur Kick bei `heartbeat` → Ausklang in der letzten Szene.
  - **Lautstärke:** Standard `music_db: 21` (Musik 21 dB unter der Stimme, gemessen in LUFS) plus `duck: 0.5` (beim Sprechen weitere 6 dB leiser). Nutzer-Feedback 06.11.: 12 dB und 17,5 dB waren beide noch zu laut. Nicht lauter machen.
  - **Echte Trend-Songs** (z. B. ein aktueller Phonk-Hit) nur **in der App** hinzufügen: `output/video_ohne_musik.mp4` hochladen und in YouTube Shorts, TikTok oder Instagram den Sound dort wählen. Dann ist er lizenziert. Bei YouTube Shorts geht dafür ein Teil der Einnahmen an die Musikrechte. Nie einen fremden Song in die Datei mischen (Content ID).
- **Ton:** um −14 LUFS, True Peak −1,5 dB. `render.py` normalisiert automatisch.
- **Stimme:** Die eingebaute „Thorsten“-Stimme (CC0) ist nur ein **Entwurf**. Für den Upload besser die **eigene Stimme** über `aufnahme/szene_XX.wav`, siehe `output/aufnahme-skript.md` (menschlicher, sicherer bei der „inauthentic content“-Regel) oder eine hochwertige Sprecherstimme per API. Die englische Piper-Stimme „Ryan“ ist **nicht kommerziell** nutzbar (CC BY-NC-SA).

## 4b. Spannung bis zum Ende (Regel vom 06.11.2026, Nutzerwunsch)
- **Mehr Bilder, mehr B-Roll:** Bildwechsel alle 1,5–3 s. Pro Szene `slides:` mit 2–3 Bildern (verschiedene Ausschnitte, Objekte, Münzen, Karten). Eintritt wechselt automatisch: `slide`, `zoom`, `fade`.
- **Bildquellen:** Wikimedia Commons (`commons.py`), **The Met Open Access** (`collectionapi.metmuseum.org/public/collection/v1.1/search?isPublicDomain=true&q=…`, CC0, gut für Objekte wie Münzen und Medaillen). Wikimedia drosselt stark, deshalb Met parallel nutzen.
- **Neugier-Leiste** (`teaser`) in Szene 2: verspricht, was am Ende kommt („Am Ende: …“). Das Versprechen wird in der vorletzten Szene eingelöst.
- **Blur-Reveal** (`reveal_word:` am Foto): Das Bild bleibt unscharf, bis das Schlüsselwort fällt.
- **Dialogfenster** (`dialog`) für Emotionen: Porträt im Kreis, Name, Text tippt sich ein. `emotion: angry | fear | sad | proud | sly` ändert Farbe, Wackeln und Ton. Erfundene Sätze bekommen `note: "nachgestellt"`, Sprichwörter `note: "Sprichwort"`. Echte Zitate nur geprüft.
- **Farbstimmung pro Szene** (`mood:`): `gold` (Macht, Hook), `sad` (Not), `warm`, `mystery` (Wende), `danger` (Gefahr), `night`, `cold` (Enttäuschung, Mythos-Bruch), Grundton `cinematic` (Teal & Orange). Dazu `bloom` (Glühen).
- **Kino-Balken** (`bars`) im spannenden Mittelteil, **Fall-Zähler** (`counter`) für Serien („Fall 1/3“).
- **Jede Kleinigkeit bekommt einen Effekt, aber KEINE Emojis** (Nutzer 06.11.2026: „lasse die Emojis weg“). Wird ein Ding, eine Zahl, Person oder Emotion genannt, passiert im Bild genau dann etwas, im ernsten Doku-Stil:
  - Zahl → `count` (zählt hoch, Tick-Geräusch, „Ding“ am Ziel).
  - Gegenstand/Detail → neues `slides`-Bild oder Großaufnahme genau beim Wort, `mark` (Kreis) oder `spotlight`.
  - Person → echtes Porträt + `lower`; Emotion → `dialog`; Urteil → `stamp`; Datum/Ort → `date`.
  - Ziel: etwa alle 2 Sekunden passiert etwas Neues.
  - `emoji` und `auto_emoji` gibt es im Renderer noch, **nicht benutzen**.

## 4a. Thema → Musik, Figuren, Bilder (Pflicht für jedes Video)
Vor dem Skript wird `era:` in der video.yaml festgelegt. Danach richten sich Musik, Bilder und Figuren.

| Epoche / Thema | `era` | Musik (`score: epoche`) | Bilder & Figuren |
|---|---|---|---|
| Antike (Rom, Griechenland, Ägypten) | `antike` | Hörner, Chor, Kriegstrommeln | Fresken, Statuen, Mosaike, Gemälde des 18./19. Jh. über Rom (Gérôme, Alma-Tadema, David) |
| Mittelalter (500–1450) | `mittelalter` | Flöte, Mönchschor, Orgel-Bordun, Rahmentrommel | Buchmalerei, Handschriften, Teppich von Bayeux, Holzschnitte |
| Renaissance / Reformation (1450–1600) | `renaissance` | Blockflöte, Laute, Streicher | Dürer, Cranach (Luther), Holbein, Stiche |
| Barock / Absolutismus / Preußen (1600–1790) | `barock` | Flöte, Cembalo, Streicher, Pauken | Porträts der Herrscher (Graff, Pesne), Menzel, Warthmüller, Schlachtengemälde |
| Napoleon / Revolution / 19. Jh. Kriege (1790–1870) | `napoleon` | Trompete, Marschtrommel, Tuba, Pauke | David, Gros, Meissonier; Karikaturen; Schlachtenpläne |
| Viktorianisch / Kaiserreich / True Crime 19. Jh. | `viktorianisch` | Celesta/Spieluhr, Pizzicato, Uhrticken (unheimlich) | Zeitungsstiche (Illustrated Police News), frühe Fotos, Stadtpläne |
| Weltkriege (1914–1945) | `weltkrieg` | einzelne Klaviertöne, Streicher, tiefe Trommeln, Posaune | gemeinfreie Fotos (Bundesarchiv nur mit passender Lizenz, US-Archive PD), Karten. Keine NS-Symbole ohne Einordnung (§ 6) |
| Kalter Krieg / DDR / Raumfahrt | `kalterkrieg` | Synth-Pad, Synth-Bass, Ticken | NASA-Fotos (PD), US-Regierungsfotos, Karten |
| Orient / Osmanen / Seidenstraße | `orient` | Flöte, Hackbrett, Rahmentrommel | Orientalisten-Gemälde, osmanische Miniaturen, Karten |
| Freie Wahl (ohne Epoche) | — | `score: trailer` (Spannung) oder `phonk` nur für bewusst „edgy“ Edits | — |

**Figuren und Bilder:**
1. **Jede genannte Person bekommt ihr echtes Porträt** (zeitgenössisch, wenn möglich) und beim ersten Auftritt eine Bauchbinde mit Name, Rolle und Lebensdaten.
2. **Bilder aus derselben Zeit und Region** wie die Geschichte. Kein Mittelalter-Bild in einem Barock-Video, kein französisches Motiv für eine preußische Szene, außer der Text spricht genau davon.
3. **Szenen-Stimmung = Bild-Stimmung:** Bei Hunger arme Bauern (Van Gogh, Millet), nachts `night: true`, bei Krieg `embers`, bei Rätseln `fog`.
4. **Wechsel zum Hauptgesicht** in Hook, Wende und Ende. Der Loop endet auf demselben Gesicht.
5. Fehlt ein passendes gemeinfreies Bild, dann lieber ein Detail aus einem passenden Gemälde als ein unpassendes ganzes Bild. Es wird nichts erfunden und keine KI-Figur einer echten Person erzeugt.

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
- Renderzeit: etwa 0,3–0,5 s pro Bild in 1080×1920, also 10–15 Min. für 60 s. `--stills` für eine schnelle Vorschau, `--audio-only` mischt nur den Ton neu (z. B. nach einer Änderung der Lautstärke).

## Quellen dieses Playbooks
- Kanal-Analyse: `dokumente/2026-11-06-analyse-history-kanaele.md`
- Recherche Nischen und Geld: `dokumente/reports/Profitabelste faceless YouTube Nischen.md`
- Recherche Erfolgskriterien: `dokumente/research_notes/Erfolgskriterien für History Videos/` (Skript/Retention, Packaging/Algorithmus, Produktion/Recht)
- Swipe-File: `recherche/swipe/2026-11-06-swipe.md`

### §4c Referenz-Regeln (Dschingis-Khan-Video, 07.11.2026) – Details: `playbook/REFERENZ-DSCHINGIS.md`
- **Story-Dokus nach dem Bogen Aufstieg → Trauma → Schwur → Aufstieg/Grauen → Wende → ironisches Ende → Rätsel → Vermächtnis/Loop.**
- **Schwarzbild-Punchline** (`blackcard: true`, `silence: 0.8`) höchstens 2× pro Video: direkt nach dem Hook (Sekunde 4–7) und am Wendepunkt. Danach `hit: true`.
- **Satzfetzen-Paare:** „Kein Stamm. Kein Schutz.“ – mindestens einmal pro Video.
- **2–3 s pro Einstellung**: lieber mehr `slides` als lange Standbilder.
- Neue Effekte: `triptych` (Dreier-Aufzählung), `spread` (Ausbreitung auf Karte), `ghost` (Opfer/Erinnerung), `glow` (Glut, Kerzen), `mood: blood` (Zweiton-Look für Gewalt/Krieg/Seuche).
