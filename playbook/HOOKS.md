# Hook-Regeln für History-Shorts

Stand: 06.11.2026. Grundlage: 21 Transkripte und rund 600 Shorts-Titel aus den Kanälen Extra History, Historically, Build A Better You, Mapfusion, Absolute History und InfiniteCracker (`dokumente/daten/`), außerdem die Swipe-File und die Recherche.
Prüfwerkzeug: `python3 video-studio/tools/hook_check.py videos/<ordner>/video.yaml` (PASS ab 75/100).

## Die 3 Sekunden
| Zeit | Was passiert | Umsetzung im Renderer |
|---|---|---|
| Bild 1 (0,0 s) | **Gesicht oder Detail in Großaufnahme**, schon in Bewegung. Nie schwarz, nie Titelkarte | `hit: true` auf Szene 1 → Punch-In, Zoom-Unschärfe, RGB-Versatz, Impact-Schlag; Foto mit `ease: out` und `rot` |
| 0–2,5 s | **Ein Satz, höchstens 9 Wörter**, der etwas Widersprüchliches behauptet | Text von Szene 1 |
| 2,5–5 s | **Die Lücke wird größer** statt geschlossen: Wie? Warum? Was passierte dann? | Szene 2 mit `transition: whip`; die Musik setzt hier ein (Drop, `drop_scene: 1`) |
| 20–30 s | **Re-Hook:** „Doch …“, „Und hier beginnt …“, ein Stempel, eine Titelkarte | `title`, `stamp`, `transition: flash` |
| letzte 3 s | **Loop:** der letzte Satz führt grammatisch in den ersten. Das letzte Bild ist das erste | Satz endet mit „:“, gleiches Foto wie Szene 1 |

## Was die erfolgreichen Kanäle im ersten Satz machen (echte Beispiele)
| Muster | Original (Aufrufe) | Unsere Schablone |
|---|---|---|
| **Serienname + Versprechen** | „These are three of the weirdest deaths in history.“ (24 Mio.) / „The worst ways to die in history, episode 4“ (11 Mio.) | „Drei der seltsamsten Tode der Geschichte.“ |
| **Provokante Verallgemeinerung + Rücknahme** | „French people hate potatoes, or at least used to.“ (Extra History) | „Die Deutschen hassten Kartoffeln. Zumindest bis 1756.“ |
| **Countdown / Zeitdruck** | „60 seconds before the nuke detonates.“ (28 Mio.) | „Zehn Minuten, bevor der Vesuv ausbricht.“ |
| **Exaktes Datum + Alltag vor der Katastrophe** | „July 7th, 1683. Emperor Leopold heard mass that morning …“ | „31. Oktober 1517. Ein Mönch hängt einen Zettel an eine Tür.“ |
| **Objekt zeigen** | „This is how tea was produced back in the 1600s.“ (13,5 Mio.) | „Das hier ist ein Brot aus Pompeji. 2000 Jahre alt.“ |
| **Anleitung mit absurdem Ziel** | „Here's how to guarantee to become a pope in about 55 years.“ | „So wurdest du im Mittelalter Henker.“ |
| **Schlimmste/Beste + Rolle** | „Worst dads in history.“ (9 Mio.) | „Die schlimmsten Väter der Geschichte: Friedrich Wilhelm I.“ |
| **Ort mit Ekel/Rätsel** | „London was once one of the worst smelling places in the world. Here's why.“ (5,9 Mio.) | „Berlin stank 1870 schlimmer als jede Stadt Europas.“ |
| **Paradoxer Wunsch** (unser Kartoffel-Hook) | — | „Dieser König wollte, dass man ihn bestiehlt.“ |

## Die 8 Regeln
1. **Behaupten statt fragen.** „Wusstest du …?“ und „Hast du dich je gefragt …?“ sind abgenutzt. Eine Behauptung mit eingebautem Widerspruch wirkt stärker.
2. **Höchstens 9 Wörter im ersten Satz**, gesprochen unter 3 Sekunden.
3. **Konkret:** „Dieser König“ (zeigt auf das Bild), ein Name, eine Zahl, ein Datum.
4. **Widerspruch einbauen:** wollte-dass, nicht-um-sondern, aber, niemand, kein einziger, verboten.
5. **Fallhöhe:** Tod, Strafe, Hunger, Diebstahl, Ekel. Dunkle Themen holen 7- bis 16-mal so viele Aufrufe wie nette (Analyse 2).
6. **Nicht sofort auflösen:** kein „weil“ im ersten Satz. Die Auflösung kommt frühestens nach 70 % des Videos.
7. **Ehrlich bleiben:** Ein Hook darf eine Legende erzählen, wenn das Video sie danach klar als Legende markiert. Das „Nicht belegt“ ist selbst der zweite Twist.
8. **Kein Anlauf:** kein „Hallo“, kein „Heute“, kein „In diesem Video“, kein Kanalname, keine Abo-Bitte.

## Vorgehen
1. Für jedes Video **mindestens 5 Hook-Varianten** schreiben, aus verschiedenen Mustern der Tabelle.
2. Alle mit `hook_check.py --text "…" --text "…"` bewerten und die beste nehmen.
3. Den Titel aus dem Hook ableiten, aber nicht wortgleich (der Titel steht auf YouTube unter dem Video).
4. Nach dem Upload in YouTube Studio den Anteil **„angesehen statt weggewischt“** prüfen. Unter 60 % bekommt das nächste Video einen anderen Hook-Typ.

## Beispiel: Kartoffel-Video v3 → v4
| | v3 | v4 |
|---|---|---|
| Satz 1 | „Dieser König ließ ein Kartoffelfeld von Soldaten bewachen.“ (65/100) | „Dieser König wollte, dass man ihn bestiehlt.“ (100/100) |
| Bild 1 | Gemälde in der Totalen, sanfte Fahrt | Gesicht in Großaufnahme, Punch-In, Impact |
| Musik | Streicher von Anfang an | Riff allein, der Beat setzt bei Satz 2 ein |
| Ende | „Legende oder Wahrheit? Was glaubst du?“ | „Ob wahr oder nicht, erzählt wird es bis heute:“ → Loop in Satz 1 |
