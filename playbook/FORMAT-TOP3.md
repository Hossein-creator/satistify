# Format „Top 3 / Countdown“ (Referenz: @surprising.facts6)

Stand: 07.11.2026. Vom Nutzer als Vorbild geschickt („genau solche Videos will ich auch“). Analysiert: 98 s, 9:16, englisch.
Inhalt des Vorbilds: „The 3 historical events that changed the world“ → Platz 3 Entdeckung Amerikas 1492 → Platz 2 Industrielle Revolution → (Abo-Bitte vor Platz 1) → Platz 1 Zweiter Weltkrieg → Schluss mit Frage an die Zuschauer.

## Welche Nische ist das?
**History-Countdown / „Surprising Facts“**: faceless Bildungs-Kanal mit **Ranglisten (Top 3) über Geschichte**. KI-Bilder, KI-Stimme, Musik, große Wort-für-Wort-Untertitel.
Für uns: **gehört zur Säule „historische Fakten“** und ist ab jetzt ein **drittes Format** neben Story-Doku und Fakten-Short.
Warum es funktioniert: Die Zahl im Titel verspricht ein klares Ende (Platz 1). Wer Platz 3 gesehen hat, will Platz 1 sehen → hohe Wiedergabe bis zum Ende.

## Aufbau (für 70–75 s, unser Ziel)
| Zeit | Teil | Vorbild | Unsere Version |
|---|---|---|---|
| 0–4 s | **Titel-Hook** | „The 3 historical events that changed the world.“ (schwach) | Zahl + Widerspruch: „3 Ereignisse, die die Welt veränderten. Platz 1 hat fast keiner auf dem Schirm.“ |
| 4–24 s | **Platz 3** | Kapitel-Bild + „Number 3: …“, dann 2–3 Bilder | Rang-Karte „PLATZ 3“ (`title`, groß) + `counter: "PLATZ 3/3"`, Datum, 3–4 Slides, ein Detail-Effekt |
| 24–46 s | **Platz 2** | gleich | gleich, steigende Dramatik (`mood`) |
| ~46 s | **Zurückhalten** | „Before revealing number 1, remember to subscribe …“ | Kurz und ohne Abo-Betteln: „Und Platz 1? Der war am tödlichsten.“ (Teaser statt Bitte) |
| 47–68 s | **Platz 1** | gleich | stärkster Fall, `hit`, evtl. Schwarzbild (`blackcard`) |
| 68–75 s | **Schluss + Frage** | „What's the most significant event for you? Let me know in the comments.“ | Frage an die Zuschauer, die zum Kommentieren reizt (eine Bitte, keine Abo-Bitte) |

## Schnitt, Bild, Ton (Vorbild → unsere Regel)
- **Kapitel-Bild:** Vor jedem „Platz“ kommt immer **dasselbe Trenn-Bild** (Wiedererkennung). → Bei uns: dasselbe Bild mit `title: "PLATZ 3"` usw. und `transition: flash`.
- **Bildwechsel:** Vorbild nur alle ~7 s mit langsamer Zoom-Fahrt (mit Spiegel-Fehlern am Rand). → Bei uns besser: alle 2–3 s ein neues Bild (`slides`), unsere Kamerafahrten ohne Fehler.
- **Untertitel:** 1–2 Wörter, GROSSBUCHSTABEN, weiß mit dicker schwarzer Kontur, gesprochenes Wort/Schlüsselwort **gelb**, mittig (~60 % Höhe), springt rein. → **`caption_style: pop`** (neu im Renderer), `caption_words: 2`, `caption_y: 0.6`.
- **Ton:** durchgehend laut, Stimme + Musik ohne Pausen. → Bei uns: Musik bleibt leise (Nutzer-Wunsch), Stimme George.
- **Bilder:** Vorbild nutzt KI-Bilder (Mischung aus Foto, Gemälde, Stich). → Bei uns echte gemeinfreie Gemälde/Fotos (Met), passend zur Epoche jedes Platzes. Jeder Platz bekommt **seine eigene Epochen-Farbe** (`mood`).

## Schwächen des Vorbilds, die wir besser machen
1. Hook ohne Widerspruch → bei uns `hook_check.py` ≥ 75.
2. Lexikon-Sätze ohne Details → bei uns ein konkretes Detail pro Platz (Zahl, Datum, Name) mit Effekt.
3. Keine Quellen, vage Aussagen → bei uns Fakten geprüft, Quellen in der Beschreibung.
4. Abo-Bitte mitten im Video → bei uns ein Teaser auf Platz 1.

## Themen-Ideen (nur Geschichte, Deutsch)
- 3 Ereignisse, die die Welt veränderten
- 3 Erfindungen, die aus Versehen entstanden
- 3 Herrscher, die auf absurde Weise starben
- Die 3 tödlichsten Seuchen der Geschichte
- 3 Schlachten, die in wenigen Minuten entschieden waren
- 3 Irrtümer aus dem Geschichtsunterricht
- 3 Schätze, die bis heute verschwunden sind
- 3 Gefängnisse, aus denen niemand entkam
- 3 Berufe im Mittelalter, die du nicht machen wolltest

## YAML-Vorlage (Ausschnitt)
```yaml
caption_style: pop
caption_words: 2
caption_y: 0.6
scenes:
  - text: "3 Ereignisse, die die Welt veränderten. Platz 1 hat fast keiner auf dem Schirm."
    hit: true
    visual: [{type: photo, src: assets/kapitel.jpg, from: [0.5, 0.5, 1.6], to: [0.5, 0.5, 1.2], ease: out}]
  - text: "Platz 3."
    transition: flash
    visual:
      - {type: photo, src: assets/kapitel.jpg, from: [0.5, 0.5, 1.2], to: [0.5, 0.5, 1.3]}
      - {type: title, text: "Platz 3", y: 0.4, size: 150}
      - {type: counter, text: "Platz 3 / 3"}
```
Rotation in der täglichen Aufgabe: Story-Doku, historischer Fakt, Top-3-Countdown (siehe `playbook/DAILY.md`).
