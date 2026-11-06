# Skript, Storytelling und Retention bei faceless History-Videos (Shorts und Langform, Stand 2025–2026)

> Recherche-Notizen vom 06.11.2026. **Hinweis zur Methode:** In dieser Sitzung konnte WebFetch fast keine Seiten öffnen, weil die Domains im Netzwerk gesperrt waren (u. a. vidiq.com, 1of10.com, outlierkit.com, bytecap.io, overseeros.com, thenextweb.com, tbreak.com, rosetta.to, humaninvariant.com). Die Web-Befunde stammen deshalb aus den **Zusammenfassungen der Suchmaschine** und nicht aus gelesenen Volltexten. Sie sind als „sekundär“ zu werten.
> **Eigene Primärdaten:** Mit `yt-dlp` habe ich die Video-Listen von 6 Kanälen gezogen: je die letzten 40 langen Videos (bei OverSimplified alle 33) sowie je 30 Shorts von Simple History, Kings and Generals und MagnatesMedia. Dazu kommen 4 Transkripte. Die Rohdateien liegen in `/tmp/claude-0/research_yt/`, nicht im Repo. Die Transkripte von OverSimplified, Fall of Civilizations und eines langen Kings-and-Generals-Videos waren nicht abrufbar, weil YouTube eine Bot-Prüfung („Sign in to confirm you're not a bot“) verlangte.

**Eigene Datenbasis (Kanal-Listen, abgerufen 06.11.2026):**

| Kanal | Videos in Stichprobe | Median-Aufrufe lang | Median-Länge lang | Spanne | Shorts-Median |
|---|---|---|---|---|---|
| OverSimplified | 33 (alle) | 40 Mio. | 18 Min. | 2–49 Min. | – |
| Fall of Civilizations | 40 | 3,75 Mio. | 149 Min. | 64–408 Min. | – |
| MagnatesMedia | 40 | 875K | 31 Min. | 15–125 Min. | (2 Ausreißer 2–4 Mio., sonst ~200K) |
| Kings and Generals | 40 | 332K | 21 Min. | 16–341 Min. | 90K |
| Simple History | 40 | 206K | 10 Min. | 8–136 Min. | 23K |
| Sleepless Historian | 40 | 20K | 130 Min. | 119–140 Min. | – |

Quellen: [OverSimplified](https://www.youtube.com/@OverSimplified/videos), [Fall of Civilizations](https://www.youtube.com/@FallofCivilizations/videos), [MagnatesMedia](https://www.youtube.com/@MagnatesMedia/videos), [Kings and Generals](https://www.youtube.com/@KingsandGenerals/videos), [Simple History](https://www.youtube.com/@SimpleHistory/videos), [Sleepless Historian](https://www.youtube.com/@SleeplessHistorian/videos), dazu die Shorts-Tabs von [Simple History](https://www.youtube.com/@SimpleHistory/shorts) und [Kings and Generals](https://www.youtube.com/@KingsandGenerals/shorts).

**Analysierte Transkripte:**
1. Kings and Generals, Short: „Why Rome's Greatest Threat Was Its Own Settler Legions“. 74 Sek., 474K Aufrufe, hochgeladen 14.09.2026. [Video](https://www.youtube.com/watch?v=wirKMAMC2YA)
2. Simple History: „This Gas Mask Has a Rhino Horn, and Changed Everything“. 9:12 Min., 1,08 Mio. Aufrufe, hochgeladen 20.10.2026. [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)
3. MagnatesMedia: „Rockefeller: The World's First Billionaire“. 49:32 Min., 7,77 Mio. Aufrufe, 123K Likes, hochgeladen 19.11.2023. [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
4. Sleepless Historian: „15 Hidden Gaps In History We Still Don't Understand“. 2:01 Std., 86K Aufrufe, hochgeladen 06.10.2026. [Video](https://www.youtube.com/watch?v=KQuFPyGaJnI)

---

## 1. Hooks (Shorts: Sek. 1–3, Langform: erste 30 Sek.) und Retention-Benchmarks

### Takeaway
YouTube veröffentlicht **keine offiziellen Richtwerte**. Die Werte aus der Creator-Szene sind daher nur Heuristiken:
- **Shorts:** etwa 70–80 % „angesehen“ statt „weggewischt“ gilt als stark, 50/50 als Durchschnitt, unter 30 % als Fehlschlag.
- **Langform:** Fast jedes Video verliert in den ersten 30 Sekunden 30–50 % der Zuschauer. Bildungsinhalte erreichen im Schnitt etwa 40–50 % durchschnittliche Wiedergabedauer (AVD %). Bei Videos über 20 Minuten gelten schon 30–40 % als gut.

Die erfolgreichen History-Videos steigen alle **ohne Begrüßung** ein: mit der Titel-Behauptung, einer Person mit Einsatz („stakes“) oder einem Problem, das der Rest des Videos löst.

### Cited Findings
**Benchmarks Shorts („Viewed vs. Swiped Away“)**
- YouTube veröffentlicht für „viewed vs swiped away“, für die Retention und für alle anderen Shorts-Kennzahlen **keine offiziellen Benchmarks**. Alle Zieltabellen beruhen auf Angaben von Creatorn. — [Creator Essentials Glossar](https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/); [Suchüberblick inkl. bytecap](https://www.bytecap.io/research/youtube-shorts-retention-benchmarks)
- Subscribr empfiehlt als Ziel 75–80 % „viewed“ zu 20–25 % „swiped“. — [Subscribr](https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-viral)
- Gyre nennt 70 %+ „viral territory“, 50/50 durchschnittlich und unter 30 % „stirbt im Feed“. — [Gyre](https://gyre.pro/blog/youtube-shorts-view-count-update-impact-strategy-what-to-do-next)
- Thunderbit nennt etwa 85 % als viral. Eine weitere Quelle teilt so ein: 70–79 % mittel, ab 80 % stark. — [Thunderbit 2025–2026](https://thunderbit.com/blog/youtube-shorts-statistics-engagement-metrics)
- Die Werte schwanken nach Thema, Publikum, Länge, Traffic-Mix, Bekanntheit des Kanals sowie Sprache und Region. Empfehlung: mit den **eigenen ähnlichen Shorts** vergleichen statt mit einer allgemeinen Zahl. — [Creator Essentials](https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/); [1of10 Shorts Analytics 2026](https://1of10.com/blog/youtube-shorts-analytics/)
- Seit dem **31.03.2025** zählt YouTube Shorts-Aufrufe anders: Auch ein kurzes Anspielen mit sofortigem Wegwischen kann als öffentlicher View zählen. „Viewed vs swiped“ ist damit das bessere Hook-Signal als die Aufrufzahl. — [Gyre](https://gyre.pro/blog/youtube-shorts-view-count-update-impact-strategy-what-to-do-next); [Creator Essentials „Engaged Views“](https://www.creatoressentials.com/glossary/shorts-engaged-views/)
- Laut einer vidIQ-Zusammenfassung einer Creator-Studie über 3,3 Mrd. Aufrufe haben Shorts, die **mindestens 60 % der Zuschauer über die ersten Sekunden hinaus halten**, eine deutlich höhere Chance auf viralen Erfolg. Die Studie wird z. T. Paddy Galloway zugeschrieben, der Name ist dort aber als „Patty“ geschrieben, die Zuordnung ist also unsicher. — [pulse.bot „This Is Why Your Shorts FAIL“](https://www.pulse.bot/creator-economy/video/this-is-why-your-shorts-fail-d9584254-4b96-4ba2-8769-314731b083ae/)
- Zum Entscheidungsfenster gibt es viele widersprüchliche Vendor-Zahlen. Beispiele: Rund 70 % entscheiden in den ersten 2–3 Sekunden. Laut selbst erhobenen Daten auf dev.to liegt die mittlere Entscheidungszeit bei 2,3 Sek. auf YouTube Shorts, 1,7 Sek. auf TikTok und 1,4 Sek. auf Reels. Zebracat (2025) meldet für Shorts mit Hook in den ersten 2 Sekunden 19 % mehr gehaltene Zuschauer. ⚠ Alles Vendor- oder Blogdaten. — [dev.to Hook Engineering 2026](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9); [Opus](https://www.opus.pro/blog/youtube-shorts-hook-formulas); [go-viral](https://www.go-viral.app/blog/hook-first-3-seconds/)

**Benchmarks Langform**
- Ein vidIQ-Video sagt: Fast jedes YouTube-Video verliert in den ersten 30 Sekunden 30 %, 40 % oder mehr als die Hälfte der Zuschauer. Ein starker Abfall in dieser Phase ist ein Hook-Problem. — [vidIQ via rosetta.to](https://rosetta.to/u/vidiq/if-your-small-channel-isn-t-getting-views-fix-this); [1of10: Hook in den ersten 30 Sekunden](https://1of10.com/blog/how-to-hook-viewers-in-the-first-30-seconds-of-a-youtube-video)
- Laut vidIQ gibt es **keine allgemeingültige „gute“ AVD**. Man soll mit eigenen Videos ähnlicher Länge und ähnlichen Formats vergleichen. — [vidIQ AVD](https://vidiq.com/blog/post/average-view-duration/)
- Werte aus Vendor-Blogs, die sich widersprechen:
  - Bildungs- und Finanzvideos erreichen oft 40–50 % AVD, Unterhaltung 60–70 %.
  - Ein „Retention Rabbit“-Report über mehr als 10.000 Videos nennt für Bildung/How-to 42,1 %. Der Report ließ sich nicht prüfen.
  - Langform liegt allgemein bei 40–60 %. Bei 20+ Minuten gelten 30–40 % schon als „high-performing“.
  - Für den Durchschnitt aller Videos 2025 kursieren unbelegt 23,7 %.
  — [tubelab 2026](https://tubelab.net/blog/youtube-audience-retention); [humbleandbrag](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks); [fluxnote AVD 2026](https://fluxnote.io/guides/youtube-average-view-duration-2026); [wildandfreetools](https://wildandfreetools.com/blog/good-average-watch-time-youtube-by-niche/); [mysocial](https://mysocial.io/blog/make-youtube-script/)
- **Paddy Galloway** (in einer sekundären KI-Zusammenfassung eines Interviews): Thumbnail und erste Zeile sind entscheidend. Man soll nicht auf kleine Retention-Dellen überreagieren. Sein Test lautet: **Würden die ersten ~30 Sekunden als eigenständiger Short funktionieren?** Wenn ja, ist das Intro stark. — [youtubesummary „Meet MrBeast's Secret YouTube Consultant“](https://youtubesummary.com/summary/AX3dEGjBg6w)

**Hook-Muster aus den Transkripten (eigene Analyse)**
- **Kings and Generals Short (74 Sek., 474K):** Das Video hat keine Frage als Hook. Der Titel trägt die Spannung („Rome's Greatest Threat Was Its Own Settler Legions“). Der erste Satz nennt den Ausgangszustand („During the early expansionist stages … legions were intentionally recruited … far from home“). Danach folgt die Wende („By the third and fourth centuries, this system had shifted“), am Ende eine These als Pointe („A locally rooted army is not simply stationed in its province. They belonged to it.“). Das ist ein Vorher-nachher-Bogen mit Folge. — [Video](https://www.youtube.com/watch?v=wirKMAMC2YA)
- **Simple History (9 Min., 1,08 Mio. in ~2,5 Wochen):** Satz 1 nennt Funktion und Stakes („A gas mask has one vital job, keep poisonous gas out and keep its wearer alive.“). Satz 2 bringt die Wendung („But engineers have devised some remarkably clever attachments …“). Satz 3 gibt das Versprechen („Here are some of the most useful and sometimes downright bizarre gadgets …“). Nach etwa 15 Sekunden beginnt der Inhalt. Es gibt keine Begrüßung und keinen Abo-Aufruf. — [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)
- **MagnatesMedia (49 Min., 7,8 Mio.):** Der Einstieg ist eine „Legende plus Schatten“-Montage in etwa 60 Sekunden: „there was a time when anyone would tremble upon hearing the name John D Rockefeller“. Es folgen Superlative (erster Milliardär, dominantestes Monopol), Konflikte (Rivalität mit Carnegie, Kämpfe gegen US-Präsidenten) und dann der Kontrast „but before he was the Titan … Rockefeller was at the very bottom of society“. Darauf kommen eine moralische Frage („at times inspiring and at times chilling … what happens when greed and ambition go completely unchecked“) und ein Zeitsprung ins Kapitel 1 („so let me take you back to 1839“). Das erste Kapitel führt sofort eine skurrile Figur ein („Devil Bill“, Hochstapler mit Doppelleben). — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **Sleepless Historian (2 Std., Schlaf-Format):** Das ist das bewusste Gegenmodell. Der Einstieg ist ruhig und warm („Hey guys, tonight we're stepping into …“), dann kommen Like/Abo und eine Kommentarfrage („where you're tuning in from and what time it is“), Spotify und „dim the lights“. Erst danach beginnt der Inhalt mit trockenem Humor („nobody left us a proper explanation … Instead, historians received ruins. Very considerate.“). Bei Schlaf-Content ist das Ziel, dass Zuschauer **dabei bleiben und einschlafen**, nicht Spannung. — [Video](https://www.youtube.com/watch?v=KQuFPyGaJnI)
- Vergleich mit den früheren Analysen (Historically, Extra History): Bei den Top-Shorts wiederholt der erste Satz die Titelfrage, bei langen Videos stehen Datum oder Szene und dann die Stakes („July 7th, 1683 …“, „How long can they hold?“). — [eigene Analyse vom 06.11.2026 im Repo: `dokumente/2026-11-06-analyse-history-kanaele.md`](https://www.youtube.com/@HeyHistorically)

### Inferences
- **Checkliste Short-Hook (0–3 Sek.):** (1) Der erste Satz ist die Titel-Behauptung oder -Frage, ohne Begrüßung. (2) Er enthält einen konkreten Gegenstand, eine Person oder eine Zahl. (3) Er deutet einen Widerspruch oder ein Paradox an („Roms größte Gefahr waren die eigenen Legionen“). (4) Bild und Ton beginnen mitten in der Handlung. Zielwert: über 70 % „angesehen“. Unter 50 % heißt, dass Hook oder Thumbnail-Frame nicht zum Thema passen.
- **Checkliste Langform-Intro (0–30/60 Sek.):** In dieser Reihenfolge: (1) die Legende oder der Superlativ, (2) der dunkle Kontrast bzw. die Stakes, (3) die zentrale Frage, die erst am Ende beantwortet wird, (4) ein Zeitsprung an den Anfang („Lass mich dich ins Jahr 1839 mitnehmen“). Mit Galloways Test prüfen: Funktionieren die ersten 30 Sekunden als eigener Short? Bei 15–60 Minuten Länge ist eine AVD von 30–45 % ein realistisches Ziel. Mehr als 50 % sind bei dieser Länge selten.
- **Ausnahme Schlaf-History:** Hier bremsen Hooks eher. Ruhe, ein Ritual und gleichförmige Kapitel sind wichtiger. Das ist ein eigenes Format mit eigener Metrik (Gesamt-Watchtime statt AVD %).

### Gaps
- Es gibt keine offiziellen YouTube-Werte und keine Retention-Zahlen von den genannten History-Kanälen selbst. Kein Kanal hat Studio-Screenshots oder Retention-Kurven veröffentlicht, die ich finden konnte.
- Den Originalartikel von bytecap, die eventuelle Galloway-Studie und den Volltext von 1of10 konnte ich nicht lesen (Domains gesperrt).
- Ob „mindestens 50 % nach 30 Sekunden“ als Zielwert für Langform belegt ist, ließ sich nicht prüfen. Ich habe keine belastbare Quelle dafür gefunden.

---

## 2. Skript-Struktur: Open Loops, Re-Hooks, Stakes, Figuren, Humor, Pattern Interrupts, Bögen, Loop-Enden, CTA-Platzierung

### Takeaway
Die Top-Langformen verbinden Kapitel wie eine Kette: Jedes Kapitel endet mit einer offenen Frage oder Wendung („But before we get to that …“). Sponsoren werden genau an solchen Cliffhangern platziert. Den Rhythmus von **„Re-Hook alle 60–90 Sekunden“** empfehlen viele Ratgeber, empirisch belegt ist er aber nicht. Er ist ein Schnitt-Werkzeug und keine Plattformregel. Shorts brauchen **genau einen Bogen** und eine Pointe. Loops helfen der Wiedergabezeit, ihr Effekt auf die Views ist umstritten.

### Cited Findings
**Re-Hooks und Open Loops (Ratgeber-Lage)**
- Die meisten Guides empfehlen alle 60–90 Sekunden einen Pattern Interrupt oder Re-Hook. YouTube schreibt dafür **kein Intervall** vor. Fixe Intervalle können zu Over-Editing führen. Andere Guides nennen 30–60 Sek. fürs Intro oder 2–3 Min. für den Hauptteil. Die Belege sind überwiegend anekdotisch. — [Creator Essentials „Pattern Interrupt“](https://www.creatoressentials.com/glossary/pattern-interrupt/); [Joyspace 2026](https://joyspace.ai/pattern-interrupt-reset-attention-span); [River Editor 2026](https://rivereditor.com/guides/how-to-script-youtube-videos-2026)
- Bei der Zahl der Open Loops widersprechen sich die Ratgeber: 1–2 Open Loops pro Video, damit das Publikum nicht das Vertrauen verliert, oder immer einen neuen Loop öffnen, sobald einer schließt. — [mysocial](https://mysocial.io/blog/make-youtube-script/); [hooked.so](https://www.hooked.so/blog/script-for-youtube-video)
- Freelancer, die den MagnatesMedia-Stil anbieten, beschreiben ihn mit „strong hooks, clean pacing, curiosity loops“. Das ist eine Fremdbeschreibung. — [Upwork-Listing](https://www.upwork.com/services/product/writing-translation-engaging-explainer-scripts-like-magnatesmedia-1722752238050648064)

**Beobachtete Struktur MagnatesMedia (eigene Analyse, Rockefeller, 49 Min.)**
- **Aufbau:** chronologische Biografie als Rise-and-Fall/Legacy-Bogen. Kindheit in Armut → erster Job (er feierte den „Job Day“ jedes Jahr am 26. September) → Ölboom in Cleveland → Monopol → Kritik in der Presse → Philanthropie → zwiespältiges Erbe. — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **Sponsor-Slots:** zwei Stück, bei ca. **62 % (Min. 31)** und **92 % (Min. 45/46)**. Beide stehen direkt hinter einem Cliffhanger: „this was exactly the crisis he'd been waiting for **but before we get to that** let's talk about an opportunity …“ und „just one question remained: what was he going to do with all that money? **But before we get to the next chapter** …“. Der Sponsor sitzt also im Open Loop. Wer weiterschauen will, muss durch die Werbung. — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **Wendungsmarker:** „however“ kommt etwa 20-mal vor, „secret“ etwa 22-mal (Wortzählung im Transkript). Das Wort „Geheimnis“ dient als wiederkehrendes Neugier-Signal. — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **Ende:** ein zweiseitiges Urteil mit Biografen-Zitat („his good side was every bit as good as his bad side was bad“), eine letzte Anekdote zum Tod (97 Jahre) und dann ein **End-Screen-CTA als Teaser fürs nächste Video**: „if you think Rockefeller's story was controversial, wait until you see the scandals Andrew Carnegie was involved with, just click the thumbnail on screen now“. Am Anfang gibt es keinen Abo-Aufruf. — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)

**Beobachtete Struktur Simple History (eigene Analyse, 9 Min.)**
- **Format:** eine Liste, die als **Kette von Problem und Lösung** gebaut ist. Die Übergänge sind fast immer Fragen oder neue Probleme: „Finger inserts are fine, but there's got to be a better way …“, „Foggy lenses aren't the only problem …“, „Gas masks filter out toxins, but what about air flowing the other way?“, „War is thirsty work …“, „What about more advanced communication?“. Jeder Abschnitt öffnet damit einen Mikro-Loop, der etwa alle 45–75 Sekunden kommt. — [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)
- **Steigerung zum Ende:** Der kurioseste Fakt kommt zuletzt, als **emotionaler Höhepunkt**. Walt Disney entwarf eine Mickey-Mouse-Gasmaske für Kinder, und es gab den britischen Baby-Schutzhelm „C3“ mit Blasebalg. Der Schluss ist eine schlichte Zusammenfassung ohne CTA. — [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)
- **Humor:** trocken und beiläufig („soldiers who can't see are a bit of a liability“, „some may sound a bit like a kazoo“). Es gibt keine Meme-Sprache wie bei Historically. — [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)

**Beobachtete Struktur Sleepless Historian (eigene Analyse, 2 Std.)**
- **Aufbau:** 15 gleichförmige Kapitel („15 Hidden Gaps“). Jedes hat den Ablauf Ausgangslage → Zusammenbruch → mögliche Ursachen → „And that is the gap“ als ritueller Abschluss. Der Humor ist leise und ironisch („It was essentially globalization, Bronze Age edition. Except when the supply chain collapsed, nobody could refresh the tracking page.“). Das letzte Kapitel endet mit einem nachdenklichen Satz und ohne CTA, weil der Zuschauer schläft. Alle CTAs stehen im Intro. — [Video](https://www.youtube.com/watch?v=KQuFPyGaJnI)

**Loop-Enden bei Shorts**
- Die Technik: das Ende zuerst planen, damit es in den Anfang fließt. Erster und letzter Frame sollen passen, der Ton soll sauber loopen. Man kann den ersten Satz am Ende wiederholen oder mitten im Satz schneiden. vidIQ beruft sich auf einen YouTube-Shorts-Report von **2021**. — [vidIQ Looping Shorts](https://vidiq.com/blog/post/double-youtube-watch-time-looping-shorts/); [Crayo](https://crayo.ai/blog/how-to-make-looping-content-for-tiktok); [CapCut](https://www.capcut.com/create/seamless-loop-videos-continuity-techniques)
- **Strittig:** Virvid behauptet, seit dem 31.03.2025 zähle jeder Loop als zusätzlicher View. vidIQ sagt, Replays bringen Wiedergabezeit, aber nicht automatisch zusätzliche „engaged views“. Retention über 100 % entsteht durch Rewatches innerhalb einer Session. Das ist eine Vendor-Aussage. — [Virvid 2026](https://virvid.ai/blog/looping-structure-shorts-retention-2026); [vidIQ](https://vidiq.com/blog/post/double-youtube-watch-time-looping-shorts/); [Fluxnote](https://fluxnote.io/guides/faceless-shorts-retention-tips-2026)
- Der Kings-and-Generals-Short (474K) nutzt **keinen Loop**. Er endet mit einem Satz, der die These abrundet: „it was a regional military society acting in what it believed to be its collective interest“. — [Video](https://www.youtube.com/watch?v=wirKMAMC2YA)

**Narrative Bögen (aus der früheren Analyse und den Kanal-Listen)**
- Bewährte Bögen bei den Top-Shorts von Historically/Extra History: „What if …?“, ein Countdown aus der Sicht von Menschen, „How to become X“ in der Du-Form, eine paradoxe Behauptung, „Wie haben sie … gekontert?“ und Serien mit Familien-Rahmen („Worst Moms in History“). — [Historically](https://www.youtube.com/@HeyHistorically/shorts); [Extra History](https://www.youtube.com/@extrahistory/shorts)
- In der Langform dominiert der **Rise-and-Fall-Bogen**. Fall of Civilizations hat ihn im Kanalnamen. Die Top-Videos sind „The Sumerians – Fall of the First Cities“ (41 Mio., 2:28 Std.) und „The Assyrians – Empire of Iron“ (22 Mio., 3:05 Std.). MagnatesMedia nutzt ihn für Firmen und Personen („The Secret Chinese Company That Owns Everything“, 12 Mio.). — [Fall of Civilizations](https://www.youtube.com/@FallofCivilizations/videos); [MagnatesMedia](https://www.youtube.com/@MagnatesMedia/videos)
- Kings and Generals setzt bei Shorts auf **Paradox- und Zahlen-Titel**: „Why England Banned Peasants from Wearing Pointy Shoes“ (423K) und „The 3,000 vs 60,000 'Battle' That Conquered India“ (250K). — [K&G Shorts](https://www.youtube.com/@KingsandGenerals/shorts)

### Inferences
- **Skript-Gerüst Langform (15–60 Min.):**
  1. **Cold Open** (0:00–1:00): Legende, Kontrast, Frage, Zeitsprung.
  2. **Kapitel von 3–6 Minuten**, jedes mit eigener Mini-Frage. Das letzte Drittel eines Kapitels endet mit „Aber …“ oder „Doch was niemand wusste …“.
  3. **Etwa alle 60–90 Sekunden ein Mikro-Re-Hook**: eine neue Frage, ein neues Problem, eine Figur oder ein Zahlen-Schock. Das muss kein Schnitt-Effekt sein, auch eine Frage im Text reicht wie bei Simple History.
  4. **Sponsor oder Eigen-CTA an einem Cliffhanger** etwa bei 40–65 % der Laufzeit, nicht im Intro.
  5. **Finale:** Urteil oder Erbe mit Gegenpositionen, dann eine letzte menschliche Anekdote.
  6. **End-Screen-Teaser** auf ein konkretes nächstes Video („Wenn du X schon krass fandest …“).
- **Figuren und Perspektive:** Jedes Thema braucht eine Hauptfigur mit Wunsch und Gegner, z. B. Rockefeller gegen Konkurrenten und Präsidenten. Nebenfiguren mit Spitznamen („Devil Bill“) machen sie einprägsam. Bei Sachthemen wie Gasmasken übernimmt das **Problem** die Rolle des Gegners.
- **Humor dosieren:** Je nach Marke trocken (Simple History, Sleepless Historian) oder frech (Historically, OverSimplified). Die Witze sollen aus den Fakten selbst kommen, nicht aus angehängten Gags.
- **Shorts:** ein Bogen (Vorher, Wende, Folge oder Pointe), eine überraschende Zahl, die Pointe im letzten Satz. Ein Loop ist optional. Wenn, dann sollte der letzte Satz grammatisch in den ersten führen. Den CTA nicht ans Ende hängen, er tötet den Loop. Stattdessen eine Kommentarfrage stellen oder den Rahmen einer Serie nennen.

### Gaps
- Für den 60–90-Sekunden-Rhythmus gibt es keine kontrollierte Studie.
- Ich konnte nicht messen, wo in den Videos tatsächlich Zuschauer abspringen, weil Retention-Kurven nicht öffentlich sind. Die Abschnittsdauern stammen nur aus dem Transkript-Text, nicht aus Zeitstempeln je Kapitel.
- OverSimplified und Fall of Civilizations ließen sich nicht als Transkript auswerten (Bot-Prüfung). Über deren Hooks kann ich nur anhand der Titel und Längen urteilen.

---

## 3. Wörter pro Minute, Skriptlänge, Satzstil

### Takeaway
Die gemessenen Sprechtempi in History-Videos liegen bei **140–200 Wörtern pro Minute (WPM)**:
- Schlaf-Content: ca. 140
- Shorts und Doku: 150–170
- schneller „Mini-Movie“-Stil (MagnatesMedia): ca. 196

Für die Planung auf Deutsch gilt: **ca. 130–150 Wörter pro Minute**, weil deutsche Wörter länger sind (eigene Ableitung, siehe Inferences). Ein 10-Minuten-Video braucht damit etwa 1.300–1.500 Wörter, ein 60-Sekunden-Short etwa 140–160.

### Cited Findings
- **Gemessen (eigene Auswertung der Transkripte):**
  - MagnatesMedia, Rockefeller: 9.689 Wörter in 49,5 Min. ≈ **196 WPM**. [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
  - Simple History, Gasmasken: 1.558 Wörter in 9,2 Min. ≈ **169 WPM**, im Schnitt ca. 19 Wörter pro Satz. [Video](https://www.youtube.com/watch?v=HKYQqRcAeEU)
  - Kings and Generals Short: 189 Wörter in 74 Sek. ≈ **153 WPM**. [Video](https://www.youtube.com/watch?v=wirKMAMC2YA)
  - Sleepless Historian: 16.972 Wörter in 121,5 Min. ≈ **140 WPM**, im Schnitt ca. 12 Wörter pro Satz. Die Sätze sind kurz und oft Fragmente („Invaders? Migrants? Refugees? Mercenaries?“). [Video](https://www.youtube.com/watch?v=KQuFPyGaJnI)
  - Methodischer Hinweis: Die Zeiten sind Gesamtlängen inklusive Musik- und Sprechpausen. Das reine Sprechtempo ist also etwas höher.
- **Ratgeber:** 150 WPM ergeben 1.500 Wörter für 10 Minuten. Faustformel: Minuten × 140 = Wortziel. Doku-Stil liest man langsamer. Bei viel B-Roll braucht man weniger Wörter. Ein Vendor-Sample von 53 langen Voiceovers hat einen Median von 166,5 WPM, das wären ca. 1.650 Wörter für 10 Minuten. — [Overseeros Skriptlänge](https://www.overseeros.com/blog/youtube-script-length-word-count); [text-tools Guide](https://text-tools-bm9.pages.dev/blog/word-count-for-youtube-video-script/); [invideo](https://invideo.io/faq/how-many-words-is-a-10-minute-youtube-video-script/)
- **Frühere Analyse:** Die Shorts von Historically und Extra History (50–90 Sek.) haben ca. 200–300 Wörter, also ca. 180–200 WPM, mit schnellem Comedy-Tempo. — [eigene Analyse, Historically-Shorts](https://www.youtube.com/@HeyHistorically/shorts)
- **Satzstil (eigene Beobachtung):**
  - MagnatesMedia erzählt lange, verkettete Sätze mit „and“/„so“ wie ein mündlicher Erzähler, mit vielen konkreten Details (gestohlene Truthahn-Eier, „Job Day“ am 26. September).
  - Simple History verbindet sachliche Sätze mit einem ironischen Nachsatz.
  - Sleepless Historian nutzt kurze Hauptsätze, Reihen mit dem Muster „A could mean B. B could mean C.“ und trockene Einwortsätze („Very considerate.“).
  — [Rockefeller](https://www.youtube.com/watch?v=fNh_GyRbJDA); [Gasmasken](https://www.youtube.com/watch?v=HKYQqRcAeEU); [Hidden Gaps](https://www.youtube.com/watch?v=KQuFPyGaJnI)

### Inferences
- **Planungstabelle Deutsch** (Annahme 130–150 WPM, weil deutsche Wörter im Schnitt länger sind; das ist eine Ableitung, nicht gemessen):

| Videolänge | Wörter (Deutsch, ca.) |
|---|---|
| Short 45 Sek. | 100–115 |
| Short 60 Sek. | 130–150 |
| Short 90 Sek. | 200–225 |
| Short 2–3 Min. | 260–450 |
| 10 Min. | 1.300–1.500 |
| 20 Min. | 2.600–3.000 |
| 30 Min. | 3.900–4.500 |
| 45 Min. | 5.800–6.700 |
| 60 Min. | 7.800–9.000 |
| Schlaf-Format 2 Std. (ca. 120 WPM) | 14.000–16.000 |

- **Regeln für den Sprechtext:** Sätze für das Ohr schreiben, im Schnitt 10–18 Wörter. Ein Gedanke pro Satz. Zahlen runden („über 100.000“). Jahreszahlen nur als Anker verwenden. Jeden zweiten bis dritten Absatz mit „Aber“, „Doch“ oder „Und dann“ beginnen, weil das Wendungen anzeigt. Fachbegriffe sofort in Alltagssprache übersetzen. Pointen ans Satzende stellen.

### Gaps
- Für deutsche Sprecher, etwa bei MrWissen2go Geschichte oder Terra X, habe ich keine WPM-Messung. Deren Transkripte habe ich aus Zeitgründen nicht gezogen.

---

## 4. Ideale Längen 2026 (Shorts und Langform) und Folgen der YPP-Änderung (8.000 Std. ab 01.02.2027)

### Takeaway
- **Shorts** dürfen seit Oktober 2024 bis zu 3 Minuten lang sein. Die Daten sprechen eher für **50–90 Sekunden**, 3 Minuten sind eine Obergrenze und kein Ziel.
- **Langform:** Die erfolgreichsten History-Kanäle liegen bei 15–50 Min. (OverSimplified, MagnatesMedia, Kings and Generals) bzw. bei 2–3 Std. (Fall of Civilizations, Schlaf-Formate).
- **YPP:** Neue Kanäle brauchen ab dem 01.02.2027 laut Sekundärquellen **8.000 Stunden Wiedergabezeit in 365 Tagen oder 20 Mio. Shorts-Views in 90 Tagen**, dazu 1.000 Abos. Das spricht für Langform als Motor für die Wiedergabezeit.

### Cited Findings
- **Shorts-Limit:** Im Oktober 2024 stieg es von 60 Sek. auf 3 Min. Mit urheberrechtlich geschützter Musik gilt teils weiter ein 60-Sek.-Limit bzw. ein Risiko für Claims. Die Quellen sind sich bei der Musik-Regel uneinig. — [Piktochart 2026](https://piktochart.com/blog/how-long-youtube-shorts/); [adcreate 2026](https://adcreate.com/blog/youtube-shorts-length-guide-2026); [Klap](https://embed.klap.app/blog/how-long-can-youtube-shorts-be)
- **Längen-Daten Shorts:**
  - OverseerOS hat 16.537 Shorts von 1.137 Kanälen analysiert (Views 7–30 Tage nach Upload). Die kürzesten Videos hatten nicht die höchsten Median-Views.
  - Eine Inflow-Network-Studie 2025 fand: 50–60 Sek. bekamen fast 22-mal mehr Views als Shorts unter 10 Sek.
  - Durchschnittlich ~33 Sek. sind ein Wert von 2023, also vor dem 3-Minuten-Limit.
  ⚠ Alles Vendor-Daten, die Volltexte waren nicht lesbar. — [Overseeros](https://www.overseeros.com/blog/best-youtube-shorts-length); [Quso](https://quso.ai/research/youtube-shorts-length); [Adobe Shorts-Längen-Studie](https://www.adobe.com/express/learn/blog/youtube-shorts-length-study)
- **Shorts der History-Kanäle (eigene Daten):** Der K&G-Short mit den meisten Views ist 74 Sek. lang. Die früher analysierten Top-Shorts von Historically und Extra History liegen bei 50–90 Sek. Bei Simple History (Median 23K) und Kings and Generals (Median 90K) bringen Shorts **deutlich weniger** als die eigenen langen Videos (Median 206K bzw. 332K). Bei Historically und Extra History ist es umgekehrt. — [Simple History Shorts](https://www.youtube.com/@SimpleHistory/shorts); [K&G Shorts](https://www.youtube.com/@KingsandGenerals/shorts)
- **Langform-Längen (eigene Daten):**
  - OverSimplified: Median 18 Min. Die Folgen wurden über die Jahre immer länger: WW1 Teil 1 (ca. 2016/17) 6 Min., WW2 Teil 1 14 Min., Napoleonic Wars Teil 1 30 Min., Second Punic War Teil 3 49 Min.
  - Fall of Civilizations: Median 149 Min., Spanne 64–408 Min., Median-Views 3,75 Mio.
  - MagnatesMedia: Median 31 Min.
  - Kings and Generals: Median 21 Min. Das „FULL DOCUMENTARY“ zum Spanischen Erbfolgekrieg (4:50 Std.) ist mit 1 Mio. das meistgesehene der letzten 40 Videos.
  - Simple History: Median 10 Min.
  - Sleepless Historian: 2–2:20 Std.
  — [OverSimplified](https://www.youtube.com/@OverSimplified/videos); [Fall of Civilizations](https://www.youtube.com/@FallofCivilizations/videos); [K&G](https://www.youtube.com/@KingsandGenerals/videos)
- **Schlaf-History:** Diese Kanäle positionieren lange Dokus als Einschlafhilfe und holen so viel Wiedergabezeit. Laut einer vidIQ-Zusammenfassung von Daten der Little Dot Studios brachten Uploads über 30 Min. überproportional viel Wiedergabezeit und Umsatz. Ultra-lange Videos (2–3 Std.+) liefen **2023–2024 besonders gut und kühlten danach ab**. Der Markt gilt als stark umkämpft, mit vielen Nachahmern und KI-Anleitungen. — [vidIQ via rosetta.to](https://rosetta.to/u/vidiq/the-youtube-cheat-code-blowing-up-small-channels); [autonolab 2026](https://blog.autonolab.com/niches/2026-02-06-faceless-youtube-sleep/); [Recapio KI-Guide Sleepless-Historian-Klone](https://recapio.com/digest/viral-ai-hack-create-million-view-sleepless-historian-videos-with-just-capcut-by-av-ai-agent)
- **YPP ab 01.02.2027** (nur Sekundärquellen, keine offizielle YouTube-Seite gefunden):
  - Neue Bewerber brauchen 8.000 „qualified“ Wiedergabestunden in 365 Tagen **oder** 20 Mio. „qualified“ Shorts-Views in 90 Tagen, dazu wie bisher 1.000 Abos.
  - Für bestehende Partner wird von einer rollierenden Untergrenze berichtet: 10 Mio. Shorts-Views pro 90 Tage, sonst endet die Shorts-Umsatzbeteiligung.
  - Die neuen Bedingungen müssen bis 31.01.2027 im Studio akzeptiert werden, sonst endet das Fan-Funding.
  - Es ist die erste große Änderung der Eintrittskriterien seit 2018.
  — [Gulf News](https://gulfnews.com/technology/youtube-raises-monetisation-requirements-for-new-creators-from-2027-1.500637658); [Shacknews](https://www.shacknews.com/article/150324/youtube-partner-program-minimum-qualified-public-watch-hours-shorts-views); [ppc.land](https://ppc.land/youtube-doubles-monetization-thresholds-and-adds-a-rolling-shorts-test/); [OutlierKit „Two Clauses Nobody Reported“](https://outlierkit.com/resources/youtube-partner-program-changes-2027/); [vidIQ](https://vidiq.com/es/blog/post/youtube-partner-program-changes-2027/)

### Inferences
- **Empfehlung Shorts:** Standard 45–75 Sek., also ein Bogen und ca. 110–170 deutsche Wörter. 90–180 Sek. nur für Countdown- oder Mini-Story-Formate mit echter Spannungskurve. Die 3 Minuten nicht ausreizen, weil die Rate „angesehen“ dann tendenziell sinkt (Vermutung, nicht gemessen).
- **Empfehlung Langform:**
  - Einstieg mit **15–25 Min.**, weil das Schreiben noch beherrschbar ist und Mid-Rolls ab 8 Min. möglich sind.
  - Flaggschiffe „Die GANZE Geschichte von …“ mit **30–50 Min.**
  - Später „Complete“- oder Schlaf-Kompilationen mit **1,5–3 Std.** aus vorhandenem Material.
  - Ein Rechenbeispiel zur YPP-Hürde: 8.000 Std. = 480.000 Minuten. Bei 20 Min. Länge und 35 % AVD (7 Min. pro View) sind das etwa **69.000 Views im Jahr**. Bei 40 Min. und 30 % AVD (12 Min. pro View) sind es etwa **40.000 Views**. Bisher zählt die Wiedergabezeit von Shorts nach der geltenden YPP-Regel nicht zu den öffentlichen Wiedergabestunden (Wissen aus dem Training, in dieser Sitzung nicht neu geprüft). Ob das für die neuen „qualified“ Stunden genauso gilt, ist offen. Der Shorts-Weg mit 20 Mio. Views in 90 Tagen ist für einen neuen deutschen Kanal unrealistisch.
- Die YPP-Änderung spricht also **für lange Videos als Kernprodukt** und Shorts als Zubringer.

### Gaps
- Die offizielle Ankündigung von YouTube (Datum, genauer Wortlaut, Definition von „qualified“) konnte ich nicht direkt verifizieren.
- Es gibt keine Studie, die die Länge von History-Langform mit RPM oder Watchtime in Beziehung setzt.

---

## 5. Serien- und Franchise-Formate, Binge-Mechanik (Playlists, „Complete“-Kompilationen, End Screens)

### Takeaway
Alle großen Kanäle arbeiten mit **wiedererkennbaren Serien-Marken**:
- OverSimplified: „Teil 1/2/3“
- Fall of Civilizations: nummerierte Episoden
- Extra History: mehrteilige Serien plus spätere „Complete“-Kompilation
- Kings and Generals: „FULL DOCUMENTARY“
- Historically/Extra History: wiederkehrende Shorts-Rahmen

Teil 2 erreicht bei OverSimplified typischerweise **55–70 % der Views von Teil 1**. Serien „verlieren“ also, bringen aber verlässlich Folge-Watchtime.

### Cited Findings
- **OverSimplified, Views Teil 1 gegenüber Teil 2 (eigene Daten):**
  - WW2: 105 Mio. → 68 Mio. (65 %)
  - Cold War: 75 → 48 (64 %)
  - Am. Civil War: 72 → 39 (54 %)
  - Napoleonic Wars: 69 → 42 (61 %)
  - American Revolution: 64 → 40 (63 %)
  - WW1: 57 → 40 (70 %)
  - French Revolution: 51 → 34 (67 %)
  - Russian Revolution: 49 → 34 (69 %)
  - Hitler: 47 → 31 (66 %)
  - First Punic War: 37 → 24 (65 %)
  - Ausnahme Second Punic War: Teil 1–3 je ca. 20–21 Mio. (ca. 100 %).
  OverSimplified hat insgesamt nur **33 Videos** und einen Median von 40 Mio. Views. — [OverSimplified](https://www.youtube.com/@OverSimplified/videos)
- **Extra History:** „Extra History Complete“-Kompilationen fassen mehrteilige Serien zu 1–2-stündigen Omnibus-Videos zusammen, z. B. Vlad the Impaler und Joan of Arc, und erreichen 1 Mio.+ Views. Die Pipeline: Serien mit 3–5 Teilen, später neu verpackt. Risiko: Die Views fallen von Teil 1 zum Finale. Das ist eine Ableitung eines Drittanbieter-Tools, keine Kanaldaten. — [OutlierKit Extra History](https://outlierkit.com/channel/extrahistory); [Class Central Playlists](https://www.classcentral.com/classroom/youtube-extra-history-the-bronze-age-collapse-90002/6284253328326)
- **Kings and Generals:** Das 4:50-Std.-Video „War of the Spanish Succession: All Battles and Events – FULL DOCUMENTARY“ ist mit 1 Mio. das stärkste der letzten 40 Uploads (Median 332K). Die Kompilation schlägt also die Einzelfolgen. — [K&G](https://www.youtube.com/@KingsandGenerals/videos)
- **Fall of Civilizations:** nummerierte Episoden („7. The Songhai Empire“, „8. The Sumerians“, „13. The Assyrians“, „18. Egypt“). Laut Interviews arbeitet Paul Cooper 2–3 Monate an jeder Episode, die Skripte wurden später zum Buch. — [Fall of Civilizations](https://www.youtube.com/@FallofCivilizations/videos); [Explaining History Podcast 2024](https://explaininghistory.org/2024/07/20/the-fall-of-civilisations/); [Buchrezension 2025](https://triumphofthenow.com/2025/09/29/fall-of-civilizations-sic-by-paul-cooper/)
- **End Screen als Binge-Brücke:** MagnatesMedia beendet das Rockefeller-Video mit einem Teaser auf das Carnegie-Video, das thematisch verwandt ist („wait until you see the scandals … click the thumbnail on screen now“). — [Video](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **Schlaf-Channels:** Sie empfehlen Kompilationen wie „10 Hours of Ancient History for Sleep“, um die Session-Länge zu erhöhen. — [Suchüberblick Schlaf-History](https://blog.autonolab.com/niches/2026-02-06-faceless-youtube-sleep/)
- **Terra X / MrWissen2go Geschichte:**
  - Seit März 2017 erscheint dort wöchentlich ein Geschichtsvideo mit Mirko Drotschmann, seit 2023 als Teil von Terra X.
  - Die vier History- und Wissenschaftskanäle von Terra X kamen 2024 zusammen auf ca. 170 Mio. YouTube-Aufrufe.
  - Die Serie „Unterwegs in der Weltgeschichte“ gilt laut ZDF als eine der erfolgreichsten der Terra-X-Geschichte.
  Feste Rhythmen und Serienmarken funktionieren also auch im DACH-Raum. — [ZDF Public Value „Terra X auf Social Media“](https://www.zdf.de/unternehmen/dein-zdf/programm/public-value/terra-x-auf-social-media-102.html); [ZDF Terra X FAQ](https://www.zdf.de/unternehmen/dein-zdf/programm/public-value/terra-x-faq-100.html)

### Inferences
- **Binge-Bauplan:**
  1. Eine Serie mit einem festen Titel-Schema planen, z. B. „Der Aufstieg und Fall von …“ oder „Die GANZE Geschichte von … (Teil 1/2)“.
  2. Jede Folge endet mit einem Teaser auf die nächste und hat einen End Screen auf Folge und Playlist.
  3. Nach 3–5 Teilen eine „Komplett“-Fassung mit Kapitelmarken veröffentlichen. Für Schlaf-Zuschauer eine leise „zum Einschlafen“-Version aus demselben Material.
  4. Shorts als Trailer: ein Kapitel-Highlight mit Verweis auf das lange Video als verlinktes „Related Video“.
- Teil 1 sollte das stärkste Thema mit dem bekanntesten Hook bekommen. Man sollte mit 30–45 % weniger Views für Teil 2 rechnen.

### Gaps
- Es gibt keine öffentlichen Daten zu Klickraten auf End Screens oder Playlists bei History-Kanälen und keine Studio-Daten zur Session-Watchtime.

---

## 6. Historische Genauigkeit: Quellen und Fact-Check, Umgang mit Legenden und Mythen, Wirkung von Fehlern auf Vertrauen und Kommentare

### Takeaway
Die glaubwürdigsten Kanäle **legen ihre Quellen offen** und lassen Experten gegenlesen. Kurzgesagt hat mehrere Fact-Checker im Haus und Quellen-Dokumente mit bis zu 60 Seiten. Fall of Civilizations liest Primärquellen in Übersetzung. Legenden werden **als Legende markiert**, wirken aber trotzdem als Story-Element. Kings and Generals wird in Communitys wie r/badhistory wiederholt für Vereinfachungen kritisiert, wächst aber dennoch. Fehler kosten vor allem bei der Kern-Fangemeinde Vertrauen. Einen messbaren Effekt auf die Views konnte ich nicht belegen.

### Cited Findings
- **Kurzgesagt** (Reddit-Aussagen der Mitarbeiter von 2023 und Video von 2019, also älter): Es gibt sechs Fact-Checker in Vollzeit, drei prüfen jedes Video. Die Quellenlisten haben bis zu 60 Seiten. Man sucht immer Primärquellen und peer-reviewte Paper und schickt Skripte an Wissenschaftler, die oft Fehler oder widersprechende Forschung finden. Viele Skripte werden verworfen oder stark überarbeitet. Kurzgesagt sagt selbst: „just citing sources doesn't make your work accurate“. Das Video zu Rat Park wurde überarbeitet, nachdem man eingeräumt hatte, eine These als Fakt dargestellt zu haben. — [Reddit r/kurzgesagt 2023 (Mirror)](https://lr.eu.psf.lt/r/kurzgesagt/comments/10jlyyk/kurzgesagt_statement_to_the_conflict_of_interest/j7c6zbi); [„Can You Trust Kurzgesagt Videos?“ (2019)](https://rosetta.to/u/kurzgesagt/can-you-trust-kurzgesagt-videos); [Zusammenfassung gist.ly](https://gist.ly/youtube-summarizer/can-you-trust-kurzgesagt-behind-the-research-integrity)
- **Fall of Civilizations / Paul Cooper:** Er recherchiert überwiegend in den Bibliotheken der University of East Anglia und liest Primärquellen in Übersetzung, weil er kein Linguist ist. Pro Episode braucht er 2–3 Monate für Schreiben und Aufnahme. — [Middle East Eye](https://www.middleeasteye.net/discover/fall-of-civilizations-podcast-book-decline-fall-history); [Rezension 2025](https://triumphofthenow.com/2025/09/29/fall-of-civilizations-sic-by-paul-cooper/); [Explaining History 2024](https://explaininghistory.org/2024/07/20/the-fall-of-civilisations/)
- **Kritik an Kings and Generals:**
  - In einem Reddit-Thread wird das Marengo-Video als „simplistic“ mit „basic factual errors“ bezeichnet.
  - r/badhistory (2019) wirft dem Kanal vor, bei iranischer Geschichte eine Interpretation als Fakt darzustellen.
  - Ein promovierter Mediävist hat das Feudalismus-Video als zu flach kritisiert.
  Daneben gibt es verteidigende Stimmen. ⚠ Das ist anekdotisch, es gibt keinen systematischen Fact-Check. — [r/badhistory 2019](https://lr.eu.psf.lt/r/badhistory/comments/cubueq/kings_and_generals_gets_iranian_history_wrong); [Schwerpunkt-Kommentar zu „Feudalism“](https://recapio.com/digest/commentary-on-kings-generals-what-everyone-gets-wrong-about-feudalism-by-schwerpunkt); [r/badhistory 2020](https://nyc1.lr.ggtyler.dev/r/badhistory/comments/f22g32/youtube_historians_you_dont_like/fh9zpqv)
- **Community-Konsens:** Zwischen Unterhaltung und Genauigkeit gibt es eine Spannung. Sorgfältige Quellenarbeit und das Vermeiden von Fehlinformation gelten als Hauptmerkmale vertrauenswürdiger Kanäle. Über OverSimplified fand ich wenig konkrete Genauigkeitskritik, die Berichterstattung ist überwiegend positiv. — [twcenter Forum](https://www.twcenter.net/threads/history-channels.766521/); [Arcadia Quill](https://arcadiaquill.com/17797/performing-arts/oversimplified)
- **Umgang mit Mythen (eigene Transkript-Beobachtung):**
  - Sleepless Historian macht Unsicherheit zum Inhalt: „nobody is completely certain who they were. Invaders? Migrants? Refugees?“, „Most historians therefore suspect there was no single cause.“
  - MagnatesMedia gibt beim Vorwurf gegen den Vater ausdrücklich an: „even though nothing was proven“. Am Ende zitiert er den Biografen, statt selbst zu urteilen.
  - Historically spielt in der früheren Analyse mit dem Mythos-Status („It's literally the myth.“).
  — [Hidden Gaps](https://www.youtube.com/watch?v=KQuFPyGaJnI); [Rockefeller](https://www.youtube.com/watch?v=fNh_GyRbJDA)
- **KI-Massenware als Vertrauensproblem:** Es gibt viele KI-Anleitungen für Klone im Stil von Sleepless Historian („million view … with just CapCut“) und für „Boring History for Sleep AI“. Das spricht für eine Flut austauschbarer, schwach geprüfter Inhalte in diesem Segment. Historically setzt mit „[No AI]“ im Titel ein Gegensignal (frühere Analyse). — [Recapio Sleepless-KI-Hack](https://recapio.com/digest/viral-ai-hack-create-million-view-sleepless-historian-videos-with-just-capcut-by-av-ai-agent); [Recapio Boring History AI](https://recapio.com/digest/how-to-create-long-boring-history-for-sleep-ai-videos-by-murray-frost)
- **Ratgeber-Hinweis:** Pro Episode eine Quellenliste für den Fact-Check-Durchgang führen. Das stammt aus einem allgemeinen Ratgeber und beschreibt nicht den Workflow eines bestimmten Kanals. — [Suchüberblick Simple-History-Recherche](https://async.com/blog/faceless-history-youtube-channe/)

### Inferences
- **Fact-Check-Protokoll für den Kanal:**
  1. Jede Zahl, jedes Datum und jedes Zitat im Skript mit Quelle markieren. Bevorzugt Fachliteratur und Primärquellen in Übersetzung, Wikipedia nur als Einstieg.
  2. Drei Stufen der Gewissheit sprachlich trennen: „belegt“, „Historiker vermuten …“, „der Legende nach …“.
  3. Die Quellenliste in die Videobeschreibung oder in ein Google-Doc wie bei Kurzgesagt.
  4. Einen angepinnten Korrektur-Kommentar für Fehler nach der Veröffentlichung.
  5. Einen Experten bzw. Historiker gegenlesen lassen, wenn möglich bei den Flaggschiff-Videos.
- Mythen nicht weglassen, sondern **als Twist nutzen**: „Das kennst du als … aber die Quellen sagen …“. Das ist zugleich ein Hook-Typ („Mythos gegen Wahrheit“).
- Im KI-gesättigten Markt sind nachweisbare Sorgfalt und eine eigene Stimme ein Unterscheidungsmerkmal. Das passt zum „[Ohne KI]“-Markenversprechen aus der Nutzer-Analyse.

### Gaps
- Zum Recherche-Workflow von Simple History, OverSimplified, The Infographics Show und MagnatesMedia habe ich keine Primärquelle (Interview, FAQ) gefunden. Bei OverSimplified ist selbst die Identität des Machers in den Quellen widersprüchlich.
- Ich habe keine Daten gefunden, die zeigen, wie sich Fehler messbar auf Views, Abos oder Kommentar-Stimmung auswirken.
- Daten zu Terra X / MrWissen2go Geschichte über Shorts und Retention gab es nicht. Die ZDF-Seiten liefern nur Reichweiten-Summen.
- Zu The Infographics Show habe ich keine Transkripte oder Daten erhoben (Zeitbudget).
