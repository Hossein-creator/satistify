# Referenz-Analyse: „This man built the largest empire …“ (Dschingis Khan, TikTok)

Stand: 07.11.2026. Vom Nutzer geschickt als Vorbild (82 s, 9:16, englisch, KI-Illustrationen).
Analyse: Einzelbilder alle 0,5 s, Schnittzeitpunkte, Lautstärkeverlauf und Frequenzen. Den Ton konnte Claude nicht hören, nur messen.
**Übernommen werden Aufbau, Schnitt, Rhythmus und Effekte, aber in unserem Stil:** echte gemeinfreie Gemälde, ernst, keine KI-Comic-Bilder, keine Emojis.

## 1. Aufbau der Geschichte (Aufstieg und Fall, 80 s)
| Zeit | Teil | Original | Unsere Umsetzung |
|---|---|---|---|
| 0–5 s | **Hook: Wer + Ausmaß** | Reiter in Großaufnahme, „This man built the largest empire the world had ever seen“ | Porträt, `hit: true`, Satz mit Superlativ |
| 5–8 s | **Schwarzbild-Punchline** | ~1 s Stille, dann „AND WIPED OUT 10% OF THE HUMAN RACE“ weiß auf Schwarz, Bass-Schlag | Szene mit `blackcard: true`, `silence: 0.8` |
| 8–15 s | **Herkunft / Ort** | „It's the 12th century. Mongolia. A land of frozen winds and endless violence“ | Datum + Ort (`date`), Landschaft, `mood: cold` |
| 15–35 s | **Kindheit und Trauma** | „No tribe. No safety.“ Gefangen. Familie verloren. Flucht bei Nacht | Kurze Satzfetzen, Gesicht in Großaufnahme, `mood: night`/`sad`, `heartbeat` |
| ~33 s | **Schwur** | „From that moment he made a promise: He will never serve anyone again.“ → Schwarzbild „THE WORLD WILL SERVE HIM“ → Schnitt auf glühende Augen | zweites `blackcard`, danach `hit` + Punch-In auf ein Gesicht |
| 38–55 s | **Aufstieg und Grauen** | Heer in einer Linie, brennende Reiche, Karte, auf der sich Feuer ausbreitet, Geister der Toten | `slides`, `triptych`, `spread` auf alter Karte, `ghost`, `mood: blood` |
| 55–62 s | **Wende** | „But even the strongest fall.“ Schock-Gesicht | `transition: flash`, `stamp` oder `title` |
| 62–72 s | **Ironischer Tod** | „In 1227 he dies from a fall off his horse. No grand battle. No final war.“ | Datum, Satzfetzen-Rhythmus |
| 72–78 s | **Rätsel** | „Buried in secret. His tomb never found.“ | `mood: mystery`, `stamp: "Nie gefunden"` |
| 78–82 s | **Vermächtnis** | „But the empire he built changed the world forever.“ Abblende auf Schwarz | Loop-Satz oder Schlusssatz + Schwarz |

## 2. Schnitt und Rhythmus
- **Ein Bild pro Satz oder Satzfetzen, etwa 2–3 s pro Einstellung**, also 30+ Einstellungen in 80 s. → Bei uns: Szenen kurz halten, `slides` mit 2–3 Bildern pro Satz.
- **Satzfetzen-Rhythmus:** „No tribe. No safety.“ / „No grand battle. No final war.“ Zwei gleich gebaute Mini-Sätze, dann ein harter Satz. → Deutsch: „Kein Stamm. Kein Schutz.“
- **Stille ist ein Effekt:** Vor beiden Schwarzbildern ist der Ton ~0,8–1,5 s fast weg (gemessen −56 dB). Danach kommt der Satz mit einem tiefen Schlag.
- **Nach dem Schwarzbild knallt das nächste Bild rein:** Großaufnahme mit schnellem Zoom (bei uns `hit: true`).
- Überall leichte Bewegung: langsamer Zoom, Nebel, Funken, Feuer flackert. Kein Bild steht still.

## 3. Look
- **Zweiton-Farben:** fast alles grau-grün entsättigt, nur Rot leuchtet (Feuer, Blut, Fahnen, Augen). → neuer Look `mood: blood` (Rot bleibt, Rest wird grau-grün).
- **Wiederkehrendes Motiv:** rote Sonne bzw. großer Mond hinter der Figur. → Bei uns: dasselbe Leitbild am Anfang und Ende (Loop), rote Glut (`glow`) bei Feuer und Kerzen.
- Starke Vignette, Filmkorn, Nebel. Haben wir schon (`grade`, `fog`).

## 4. Texte im Bild
- Untertitel: weiß, fett, Großbuchstaben, 2 Zeilen, mittig im unteren Drittel, Satzstück für Satzstück. → Wir bleiben bei unseren Wort-für-Wort-Untertiteln (bessere Bindung). Für Punchlines gibt es das Schwarzbild.
- **Schwarzbild-Karte:** großer weißer Satz in Großbuchstaben, sonst nichts.

## 5. Neue Effekte (jetzt im Renderer)
| Effekt | YAML | Wann |
|---|---|---|
| **Schwarzbild-Punchline** | Szene: `blackcard: true`, `silence: 0.8` (Stille vorher; Musik setzt aus), optional `card: "…"` (anderer Text als gesprochen), `card_size: 96` | Höchstens 2× pro Video: nach dem Hook und beim Wendepunkt. Die Szene danach bekommt `hit: true`. |
| **Split-Screen (Triptychon)** | `{type: triptych, src: [a.jpg, b.jpg, c.jpg], crops: [[x, y, zoom], …]}` | Aufzählungen in drei Teilen: „Drei Städte. Drei Feuer.“ Oder dasselbe Bild in 3 Details. |
| **Zweiton-Look** | `mood: blood` | Gewalt, Krieg, Seuche, Blut. Sparsam, nicht im ganzen Video. |
| **Ausbreitung auf Karte** | `{type: spread, points: [[x, y, verzögerung], …], dur: 3, r_max: 0.35}` auf einem Kartenbild | Reich, Seuche, Feuer, Krieg breitet sich aus. |
| **Geister** (Nutzer fand Demo schlecht – nur sehr sparsam) | `{type: ghost, src: gesicht.jpg, crop: [x, y, zoom], x: 0.3, y: 0.3, size: 0.3}` | Opfer, Tote, Erinnerung. Am besten auf dunklen Bildern (`mood: night`/`blood`). |
| **Glut / Leuchtpunkte** (nie auf Porträts – Nutzer fand Demo schlecht) | `{type: glow, points: [[x, y], …], r: 0.02, color: [255, 60, 30]}` | Kerzen, Glut, Fackeln. Leuchtende Augen nur bei Dämonen/Bösewicht-Karikaturen, nie auf echten Porträts (wirkt billig). |

Test-Video mit allen Effekten: `videos/_demo-referenz/video.yaml` (wird nicht gepostet).

## 6. Nicht übernehmen
- KI-Comic-Bilder (Nutzer will realistisch; außerdem wären es erfundene Bilder historischer Personen).
- Unbelegte Zahlen als Fakt („10 % der Menschheit“ ist eine grobe Schätzung → bei uns mit „Schätzungen zufolge“ oder Stempel).
- Werbe-Einblendungen („Want to make videos like this?“).
