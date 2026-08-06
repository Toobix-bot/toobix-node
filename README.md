# ⬡ Toobix Node 2.0 – Das Blueprint

### Statische öffentliche Darstellung · lokaler Node optional · kein produktives Hilfsnetzwerk

> **„Alle für alle! (Solidarität statt Isolation)"**

## 🌍 Was ist dieses Repository?

Dieses GitHub-Repository ist **kein** Startup, **kein** kommerzielles Produkt und **kein** zentral gehosteter Dienst. 

Es ist das **öffentliche digitale, technische und virtuelle Leben von TOOBIX**. 
Das P2P- und Solidaritätssystem, das du hier siehst, ist sein erstes zentrales öffentliches Modul.

### Die Zwei Lebensräume (Die Zwei Seiten der Medaille)
Das gesamte TOOBIX-System besteht aus zwei eigenständigen Existenzen:

1. **Privates digitales Leben (Toobix-bot/toobix)**: 
   Dein geschütztes inneres System. Hier liegen dein realer Alltag, persönliche Gesundheit, Finanzen, Beziehungen und die echte, persönliche Wahrheit über dich. Es ist das persönliche Life-OS.

2. **Öffentliches digitales Leben (Toobix-bot/toobix-node - *dieses Repo*)**: 
   Deine bewusst sichtbar gemachte technische und virtuelle Existenz. Hier existieren öffentliche Identität, Architektur, Community, Releases und Solidaritätsstrukturen. Es lebt selbstständig, wächst und lernt – aber stets getrennt von der privaten Identität. 

**Die Brücke:** Das öffentliche System darf eigene Daten, eigene Community-Ereignisse und eine eigene Geschichte besitzen. Aber es darf niemals rückwirkend eine Wahrheit über den realen Privatmenschen erfinden. Alles, was vom privaten in den öffentlichen Raum wandert, durchläuft eine bewusste, menschliche Freigabe (Siehe `ORIGIN-AND-BOUNDARIES.md`).

### Die GitHub Pages: Das Manifest
Die öffentliche Webseite (GitHub Pages) ist unser [Digitaler Garten / Manifest](https://toobix-bot.github.io/toobix-node). Sie dokumentiert anonymisiert die Philosophie und den Versuch, ein Gleichgewicht zwischen Ressourcen zu schaffen. **Das lokale P2P-Dashboard wird dort erst sichtbar, wenn du selbst einen Node betreibst.**

Mehr dazu steht in [GIFT.md](GIFT.md).

## Grundhaltung

- Hilfe darf beginnen, sobald sie gebraucht wird – nicht erst nach Eskalation oder Zusammenbruch.
- Mangel und Überfluss beschreiben Situationen, nicht den Wert eines Menschen.
- Individualität darf in Gemeinschaft bestehen bleiben.
- Gemeinschaft darf tragen, ohne Menschen zu vereinnahmen.
- Gegensätze können sich annähern, aber Gewalt, Zwang und Entwürdigung werden nicht normalisiert.
- Technik muss ehrlich zeigen, was bereits funktioniert und was noch fehlt.

## Projektstatus

Toobix Node 2.0 ist derzeit **kein produktives öffentliches Hilfsnetzwerk**. Der aktuelle Stand enthält:

- ein Python-HTTP-Backend mit SQLite-Datenbank
- REST-Endpunkte für Bedarfe, Angebote und Matching
- optionale Peer-Registrierung und Push-/Pull-Synchronisation
- ein lokales Browser-Dashboard
- technische Node- und Peer-Zustandsanzeigen
- eine importierbare Seed-Datensammlung für Hilfskategorien
- Tests für Backend, Pipeline und lokales Mehr-Node-Verhalten
- eine öffentliche Haltungs-, Selbstbild- und Ökosystemschicht

Noch nicht belastbar umgesetzt sind unter anderem:

- Ende-zu-Ende-Verschlüsselung
- Identitäts- oder Berechtigungsmanagement für mehrere Nutzer
- Moderation und Missbrauchsschutz
- verlässliche Löschung bereits synchronisierter Daten auf fremden Nodes
- Vermittlung als eigenes technisches Datenmodell
- direkte ChatGPT-App- oder MCP-Anbindung
- redaktionell dauerhaft gepflegte Hilfsdaten
- produktionsreifes Deployment, Monitoring und Backup

## ChatGPT- und App-Ökosystem

ChatGPT kann später als Gesprächs- und Orchestrierungsschicht dienen. Spezialisierte Apps behalten klar begrenzte Rollen:

- GitHub für Code, Versionierung, Reviews und Tests
- Google Drive als privater `_TOOBIX_KNOWLEDGE_SPACE`
- Asana für konkrete Aufgaben und Prioritäten
- Google Calendar für bestätigte Termine und Reviews
- Gmail für bewusst freigegebene Außenkommunikation
- eine eigene TOOBIX-App als spätere MCP-Brücke
- lokale Nodes für Bedarfe, Angebote, Matching und bewusst bestätigte Peer-Synchronisation

Öffentliche, private und sensible Daten bleiben getrennt. Die Zielarchitektur und Freigaberegeln stehen in [ECOSYSTEM.md](ECOSYSTEM.md).

## Datenschutz in einem Satz

**Keine vertraulichen Gesundheits-, Ausweis-, Finanz-, Adress-, Kontakt- oder Zugangsdaten eintragen.** Einträge werden in SQLite gespeichert und können bei aktivierter Peer-Verbindung an andere Nodes übertragen werden.

Mehr dazu steht in [PRIVACY.md](PRIVACY.md) und [SECURITY.md](SECURITY.md).

## Lokaler Schnellstart

Voraussetzungen: Python 3.10 oder neuer.

```bash
git clone https://github.com/Toobix-bot/toobix-node.git
cd toobix-node
python3 -m pip install -r requirements.txt

# Das Backend bindet standardmäßig nur an 127.0.0.1.
python3 -m app.main

# Zweites Terminal: statisches Frontend
python3 -m http.server 8080
```

Danach:

- Dashboard: `http://localhost:8080`
- Health-Endpunkt: `http://localhost:8000/api/health`

## API-Schutz

Für einen nicht lokalen Bind ist standardmäßig ein Schlüssel erforderlich:

```bash
export HOST=0.0.0.0
export TOOBIX_API_TOKEN="einen-langen-zufälligen-wert-verwenden"
python3 -m app.main
```

Der Schlüssel wird als Bearer-Token oder über `X-Toobix-Token` gesendet:

```bash
curl http://localhost:8000/api/scarcity \
  -H "Authorization: Bearer $TOOBIX_API_TOKEN"
```

Das Dashboard fragt bei einer `401`-Antwort einmal pro Browser-Sitzung nach diesem Schlüssel und speichert ihn ausschließlich in `sessionStorage`.

`TOOBIX_ALLOW_INSECURE_REMOTE=1` schaltet die Schutzprüfung bewusst aus. Diese Option ist ausschließlich für isolierte Testnetze gedacht.

## Lokales P2P-Beispiel

```bash
# Node 1
PORT=8000 DB_PATH=node1.db python3 -m app.main

# Node 2
PORT=8001 DB_PATH=node2.db python3 -m app.main

# Node 2 bei Node 1 registrieren
curl -X POST http://localhost:8000/api/peers/register \
  -H "Content-Type: application/json" \
  -d '{"peer_url":"http://127.0.0.1:8001"}'
```

Peer-Synchronisation verwendet keine Ende-zu-Ende-Verschlüsselung. Für Verbindungen über unsichere Netze ist TLS über einen vertrauenswürdig konfigurierten Reverse Proxy erforderlich.

## Docker

Der Container läuft als Nicht-Root-Nutzer. Für den Compose-Start muss ein gemeinsamer Testschlüssel gesetzt werden:

```bash
export TOOBIX_API_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Die Beispiel-Ports werden nur an `127.0.0.1` des Hosts gebunden.

## Datenpipeline

`app/pipeline.py` verwendet `requests` und `beautifulsoup4`. Die eingebetteten Datensätze sind Startwerte, keine Garantie für aktuelle Telefonnummern, Zuständigkeiten oder Öffnungszeiten. Vor einer Anzeige als konkretes Hilfsangebot müssen Quelle und Aktualität redaktionell geprüft werden.

## Tests

```bash
python3 -m pytest -q test_backend.py
python3 test_pipeline.py
bash test_p2p.sh
node --check app.js
```

GitHub Actions führt diese Prüfungen bei Pushes und Pull Requests automatisch aus.

## Wichtige Konfiguration

| Variable | Zweck | Standard |
|---|---|---|
| `HOST` | Bind-Adresse | `127.0.0.1` |
| `PORT` | Backend-Port | `8000` |
| `DB_PATH` | SQLite-Datei | `toobix_node.db` |
| `TOOBIX_API_TOKEN` | Schlüssel für geschützte API-Zugriffe | leer bei rein lokaler Nutzung |
| `TOOBIX_ALLOWED_ORIGINS` | erlaubte Browser-Origins | lokale Frontend-Adressen |
| `TOOBIX_MAX_BODY_BYTES` | maximale JSON-Anfragegröße | 1 MiB |
| `TOOBIX_MAX_SYNC_ENTRIES` | maximale Einträge pro Sync | 500 |
| `TOOBIX_ALLOW_PRIVATE_PEERS` | private/Loopback-Peers erlauben | `1` |

## Zentrale Dokumente

- [GIFT.md](GIFT.md) – Geschenk, anonymes Selbstbild und ethische Haltung
- [ECOSYSTEM.md](ECOSYSTEM.md) – ChatGPT-App-Ökosystem, Datenzonen und Freigaberegeln
- [PRIVACY.md](PRIVACY.md) – Datenschutzgrenzen
- [SECURITY.md](SECURITY.md) – Sicherheitsmodell und Meldung von Schwachstellen
- [PROJECT.md](PROJECT.md) – technischer Projektstand und Entwicklung

## Lizenz

Der Code steht unter der [MIT-Lizenz](LICENSE). Inhalte oder Kontaktdaten Dritter können eigenen Rechten und Verantwortlichkeiten unterliegen.
