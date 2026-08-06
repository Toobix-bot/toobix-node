# Toobix Node 2.0 – Engineering Status

## Zweck

Toobix Node 2.0 ist ein experimenteller lokaler Prototyp für:

- strukturierte Bedarfe und Angebote
- einfaches regelbasiertes Matching
- Speicherung in SQLite
- optionale Synchronisation zwischen ausdrücklich registrierten Nodes
- technische Zustands- und Erreichbarkeitsanzeigen

Die Software ist noch kein produktives öffentliches Hilfsnetzwerk.

## Architektur

### Backend

`app/main.py` stellt eine kleine REST-API mit Python `http.server` bereit. Die API bindet standardmäßig nur lokal. Ein nicht lokaler Bind verlangt einen API-Schlüssel, sofern die Schutzprüfung nicht ausdrücklich für ein isoliertes Testnetz deaktiviert wird.

### Datenhaltung

`app/db.py` nutzt SQLite. Bedarfe, Angebote, Matches, Peers und technische Zustandswerte liegen in einer konfigurierbaren Datenbankdatei.

### Matching

`app/matching.py` gewichtet Kategorie, Schlüsselwörter und Ort. Das Ergebnis ist ein technischer Vorschlagswert und keine soziale, medizinische oder rechtliche Entscheidung.

### Peer-Synchronisation

`app/p2p.py` unterstützt ausdrücklich registrierte HTTP(S)-Peers, Push-/Pull-Synchronisation, Größenlimits und Last-Write-Wins anhand von Zeitstempeln. Es existiert keine Ende-zu-Ende-Verschlüsselung, keine garantierte Fernlöschung und noch kein Nutzer-/Rollenmodell.

### Datenpipeline

`app/pipeline.py` kann Seed-Daten und konfigurierte Webquellen verarbeiten. Importierte Kontakte sind erst nach redaktioneller Prüfung als aktuell oder verifiziert zu bezeichnen.

### Frontend

`index.html`, `style.css` und `app.js` bilden ein statisches lokales Dashboard. Bei gesicherter API wird der Schlüssel für die Browser-Sitzung im `sessionStorage` gehalten.

## Aktueller Reifegrad

| Bereich | Stand | Grenze |
|---|---|---|
| Datenmodelle und SQLite | Prototyp umgesetzt | Migrationen und Backupstrategie fehlen |
| REST-API | Prototyp umgesetzt | kein Rollenmodell, kein Rate Limiting |
| Matching | Prototyp umgesetzt | keine fachliche Wirksamkeitsprüfung |
| P2P-Sync | lokaler Teststand | kein E2EE, kein Vertrauensnetz |
| Peer-Zustand | technische Metriken | keine Bewertung von Menschen |
| Hilfsdaten-Pipeline | Seed-/Teststand | Quellenpflege und Verifikation fehlen |
| Dashboard | lokaler Teststand | kein produktives Deployment |
| Tests/CI | automatisiert angelegt | Security- und Lasttests ausbaufähig |

## Sicherheitsprinzipien

- lokal binden, bevor Netzwerkzugriff freigegeben wird
- Remote-Zugriff nur mit langem zufälligem API-Schlüssel
- TLS und Firewall/VPN für Verbindungen über Geräte- oder Netzgrenzen
- keine sensiblen personenbezogenen Daten
- nur bewusst registrierte und geprüfte Peer-URLs
- begrenzte Request-, Response- und Sync-Größen
- keine generierten Binärdateien, Datenbanken oder Geheimnisse committen

## Nächste belastbare Meilensteine

1. **CI vollständig grün:** Backend-, Pipeline-, P2P- und Frontend-Prüfungen.
2. **Datenminimierung:** Pflichtfelder reduzieren, Lösch- und Aufbewahrungskonzept definieren.
3. **Authentifizierung V2:** individuelle Schlüssel/Rollen statt gemeinsamem Node-Schlüssel.
4. **Transport-Sicherheit:** dokumentierte TLS-Konfiguration und gegenseitige Peer-Authentisierung.
5. **Synchronisationsmodell:** nachvollziehbare Einwilligung, Herkunft und Löschweitergabe.
6. **Hilfsdaten-Redaktion:** ausschließlich offizielle Quellen, Prüfdatum und Zuständigkeit.
7. **Moderation und Missbrauchsschutz:** bevor fremde Personen Einträge veröffentlichen dürfen.
8. **Pilotbetrieb:** erst in einem kleinen kontrollierten Testkreis mit synthetischen Daten.

## API-Oberfläche

- `GET /api/health` – technische Erreichbarkeit
- `GET/POST /api/scarcity` – Bedarfe
- `GET/POST /api/abundance` – Angebote
- `GET/POST /api/matches` – Match-Vorschläge
- `GET/POST /api/reflection` – technische Node-Zustandsdaten
- `GET /api/peers` – registrierte Peers
- `POST /api/peers/register` – validierten Peer registrieren
- `POST /api/p2p/sync` – begrenzte Synchronisationsdaten annehmen

Details zu Betrieb und Konfiguration stehen in `README.md`, `PRIVACY.md` und `SECURITY.md`.
