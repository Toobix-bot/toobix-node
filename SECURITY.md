# Sicherheit

## Unterstützter Stand

Toobix Node 2.0 ist ein früher Prototyp und derzeit nicht für unkontrollierten öffentlichen Betrieb oder sensible personenbezogene Daten freigegeben.

## Sichere Grundeinstellungen

- Das Backend bindet standardmäßig nur an `127.0.0.1`.
- Ein Bind an andere Interfaces erfordert `TOOBIX_API_TOKEN`.
- Browser-Zugriffe sind auf konfigurierte Origins beschränkt.
- JSON-Anfragen und Peer-Antworten besitzen Größenlimits.
- Peer-URLs werden vor ausgehenden Requests validiert.
- Docker läuft als Nicht-Root-Nutzer.

## Für Netzwerkbetrieb erforderlich

- langer, zufälliger API-Schlüssel
- TLS über einen korrekt konfigurierten Reverse Proxy
- Firewall- oder VPN-Begrenzung
- getrennte Testdaten statt realer vertraulicher Daten
- regelmäßige SQLite-Backups und Wiederherstellungstests
- Prüfung jedes registrierten Peers

`TOOBIX_ALLOW_INSECURE_REMOTE=1` darf nur in einem isolierten Testnetz verwendet werden.

## Bekannte Grenzen

- keine Ende-zu-Ende-Verschlüsselung der synchronisierten Inhalte
- gemeinsamer API-Schlüssel statt Nutzer- und Rollenmodell
- keine garantierte Fernlöschung bereits replizierter Daten
- keine Moderation, Spam-Abwehr oder belastbare Identitätsprüfung
- Last-Write-Wins ist kein Schutz gegen absichtlich manipulierte Zeitstempel
- Seed-Hilfsdaten können veralten

## Sicherheitsproblem melden

Keine Zugangsdaten, personenbezogenen Datensätze oder direkt ausnutzbaren Details in ein öffentliches Issue schreiben. Zunächst eine private Kontaktmöglichkeit des Repository-Inhabers verwenden und nur die zur Reproduktion notwendigen Informationen teilen.

## Notfälle

Dieses Projekt ist kein medizinisches Produkt und kein Krisendienst. Bei unmittelbarer Gefahr in Deutschland und der EU gilt 112.
