# TOOBIX im ChatGPT-App-Ökosystem

## Zielbild

TOOBIX soll kein weiteres isoliertes Ablagesystem werden. ChatGPT kann als Gesprächs- und Orchestrierungsschicht dienen, während spezialisierte Apps jeweils eine klar begrenzte Aufgabe übernehmen.

Die öffentliche Webseite bleibt bewusst datensparsam. Persönliche und sensible Informationen werden nicht automatisch veröffentlicht oder zwischen Apps weitergereicht.

## Rollen der Komponenten

### ChatGPT – Gespräch und Orchestrierung

- natürliche Sprache, Zusammenhänge und nächste Schritte klären
- Bedarf, Angebot, Grenzen und Vermittlung verständlich strukturieren
- ausdrücklich freigegebene Informationen aus verbundenen Apps lesen
- bestätigte Aktionen an die dafür geeignete App übergeben
- keine fachliche, medizinische, rechtliche oder menschliche Verantwortung ersetzen

### TOOBIX-Webseite – öffentliche und lokale Oberfläche

- anonymes öffentliches Selbstbild und Manifest
- transparente Darstellung von Projektstatus und Grenzen
- lokales Dashboard für den eigenen Node
- Oberfläche für Bedarfe und Angebote
- keine automatische Veröffentlichung privater Node-Daten

### TOOBIX-Backend – lokaler Daten- und Vermittlungskern

- SQLite-Datenbank
- REST-Endpunkte für Bedarfe, Angebote und Matching
- optionale Synchronisation mit ausdrücklich registrierten Peers
- Schutz durch lokale Bindung oder API-Token
- derzeit keine Ende-zu-Ende-Verschlüsselung und kein Mehrbenutzer-Rechtesystem

### GitHub – technisches Fundament

- Quellcode und Versionsgeschichte
- Pull Requests, Reviews und automatische Tests
- öffentliche Nachvollziehbarkeit der Projektentwicklung
- keine persönlichen Lebens-, Gesundheits- oder Kontaktdaten

### Google Drive – privater Knowledge Space

- bestehender `_TOOBIX_KNOWLEDGE_SPACE` bleibt führende Dokumentenstruktur
- Konzepte, Entscheidungen, Dokumente und Arbeitsstände
- klare Trennung zwischen öffentlich freigegebenen und privaten Inhalten
- keine unnötige parallele Wissensablage

### Asana – operative Aufgaben

- konkrete nächste Schritte, Prioritäten und Verantwortlichkeiten
- keine vollständigen sensiblen Falldaten in Aufgabentiteln oder öffentlichen Projekten

### Google Calendar – Zeit und Verbindlichkeit

- Termine, Reviews und freiwillige Nachverfolgung
- keine automatische Terminplanung ohne Bestätigung

### Gmail – bewusste Außenkommunikation

- Kontakt mit Menschen, Trägern und möglichen Partnern
- Entwürfe und Versand nur nach bewusster Freigabe
- keine unkontrollierten Seriennachrichten

### Eigene TOOBIX-App – spätere MCP-Brücke

Eine eigene ChatGPT-App könnte über das Model Context Protocol wenige, klar definierte Werkzeuge bereitstellen. Sie sollte mit Leserechten beginnen und Schreibrechte nur schrittweise erhalten.

Mögliche erste Werkzeuge:

- `get_public_manifest` – öffentliche Haltung und Projektstatus lesen
- `get_local_node_status` – technischen Node-Zustand lesen
- `list_bridge_entries` – freigegebene Bedarfe und Angebote lesen
- `save_project_note_to_drive` – geprüfte Projektinformation in Drive ablegen
- `create_follow_up_task` – bestätigten nächsten Schritt in Asana anlegen
- `schedule_review` – nach Bestätigung einen Kalendertermin erstellen
- `draft_outreach` – einen Kommunikationsentwurf vorbereiten
- `publish_public_snapshot` – ausschließlich bewusst freigegebene Inhalte veröffentlichen

## Drei Datenzonen

### Öffentlich

- Manifest und Werte
- anonymes Selbstbild
- Quellcode und technische Dokumentation
- bewusst veröffentlichte Projektstände
- redaktionell geprüfte allgemeine Ressourcen

### Privat

- persönliche Planung
- lokale Node-Daten
- Arbeitsnotizen und Entwürfe
- Asana-Aufgaben und Kalenderplanung
- nicht veröffentlichte Drive-Dokumente

### Sensibel

- Gesundheit und Diagnosen
- Krisen- und Notfalldaten
- Klarnamen und Kontaktdaten Dritter
- Adressen, Zugangsdaten, Finanz- und Ausweisdaten
- vertrauliche Nachrichten

Sensible Daten dürfen nicht automatisch in die Webseite, GitHub, öffentliche Aufgaben, Peer-Synchronisation oder ungeschützte Exporte gelangen.

## Freigaberegeln

1. Jede Quelle und jedes Ziel müssen erkennbar sein.
2. Lesen wird je Datenquelle gezielt erlaubt.
3. Schreiben benötigt einen nachvollziehbaren Zweck und eine klare Ziel-App.
4. Veröffentlichung benötigt eine zusätzliche bewusste Freigabe.
5. Löschen, Versenden, Synchronisieren und Terminieren werden nicht still ausgeführt.
6. Eine fehlgeschlagene Verbindung darf nicht durch erfundene Daten ersetzt werden.
7. Peer-Synchronisation und App-Synchronisation sind getrennte Vorgänge und benötigen getrennte Zustimmung.

## Praktischer Ablauf heute

1. Bedarfe und Angebote zunächst im eigenen lokalen Node erfassen.
2. Vor jeder Synchronisation prüfen, ob personenbezogene oder sensible Angaben enthalten sind.
3. In ChatGPT gemeinsam klären, welcher nächste Schritt sinnvoll ist.
4. Eine passende Ziel-App bewusst auswählen:
   - Dokument oder Entscheidung in Drive
   - Aufgabe in Asana
   - Termin in Calendar
   - Nachrichtenentwurf in Gmail
   - technische Änderung über GitHub
5. Nur ausdrücklich freigegebene Bestandteile veröffentlichen oder an Peers übertragen.

## Ausbaupfad

### Phase 1 – sicherer lokaler Node

- Backend und Frontend stabilisieren
- lokale Datenhaltung und API-Schutz
- klare Datenschutz- und Sicherheitsdokumentation
- manuell bestätigte Übergaben

### Phase 2 – private TOOBIX-App

- MCP-Server mit wenigen lesenden Werkzeugen
- Drive und Asana als erste kontrollierte Ziele
- Protokollierung und Bestätigung jeder Schreibaktion

### Phase 3 – koordinierter Workflow

- Kalender und Gmail nach bewusster Freigabe
- Vermittlung als eigenes Datenmodell
- Rollen- und Berechtigungssystem
- redaktionell gepflegte Ressourcen

### Phase 4 – mögliche Öffentlichkeit

- freiwillige Accounts oder Pseudonyme
- Moderation und Missbrauchsschutz
- getrennte öffentliche und private Profile
- keine Veröffentlichung ohne ausdrückliches Einverständnis
