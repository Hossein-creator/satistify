# Daily Task: 3 Videos pro Tag

Stand: 06.11.2026. Wunsch des Nutzers. Läuft als geplante Aufgabe, jeden Tag früh (Vorschlag 05:00 Uhr Berlin), damit alles vor 10:00 eingeplant ist.

## Was verstanden ist
- Jeden Tag **3 neue Videos** (Entscheidung 06.11.2026, vorher 4), Länge **1:10–1:15 Min.** (70–75 s).
- Nische: History / Doku / True History / **historische Fakten** (nur Geschichte), Deutsch, ernster Doku-Look, keine Emojis.
- Jedes Video über **Metricool** auf **YouTube (Short), Instagram (Reel), TikTok** einplanen.
- Brand 7558808 = „Was wirklich geschah“. **Stickman-Accounts nie anfassen.**
- Uhrzeiten: **10:00, 16:00, 18:00** (`POSTING-ZEITEN.md`).

## Ablauf jeden Tag
1. Repo holen, `memory/`, `VIDEO-PLAYBOOK.md`, `HOOKS.md`, `GENERIERE.md` lesen.
2. Prüfen: Brand 7558808 zeigt noch „Was wirklich geschah“? Sonst abbrechen und melden.
3. Zahlen von gestern aus Metricool holen (Aufrufe, Retention, Follower). Was lief gut → mehr davon.
4. **3 Themen** wählen: abwechselnd 2 Story-Dokus + 1 historische Fakten oder umgekehrt. Kein Thema doppelt (`videos/` prüfen). Verschiedene Epochen.
5. Pro Video **Schritte 3–15 aus `GENERIERE.md`**: Fakten + Quellen, Epoche, Bilder, 5 Hooks + `hook_check`, Skript für 70–75 s (ca. 170–190 Wörter), `ig-human`, Szenen mit Detail-Effekten, Farbe, Epochen-Musik, Rendern, Selbstprüfung.
6. Länge prüfen: 70–75 s. Sonst Text kürzen oder ergänzen und neu rendern.
7. Pro Video: Titel (YouTube), Caption + 3 Hashtags (`ig-caption`), Cover-Bild.
8. Videos online ablegen (öffentlicher Link, Ort noch offen) und alles committen + pushen.
9. In Metricool einplanen: Video 1 → 10:00, 2 → 16:00, 3 → 18:00. Je ein Post mit allen 3 Netzwerken. YouTube Typ „short“, Kategorie EDUCATION, nicht für Kinder. KI-Kennzeichnung an.
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
