# Sicherheitsrichtlinien (Security Policy)

Toobix Node 2.0 ist ein Open-Source-Projekt, das sich noch in der Prototyp-Phase befindet. Wir nehmen Sicherheit ernst, aber als dezentrales Netzwerk ohne zentrale Moderation gibt es bestimmte Risiken, derer sich jeder Betreiber eines Nodes bewusst sein muss.

## Unterstützte Versionen

| Version | Unterstützt |
| ------- | ------------------ |
| >= 2.0.0 | :white_check_mark: |
| < 2.0.0  | :x:                |

## Schwachstellen melden

Bitte melde Sicherheitslücken **nicht** über öffentliche GitHub Issues. 

Da dieses Projekt auf Anonymität und Dezentralität ausgelegt ist, gibt es kein zentrales "SecOps"-Team. Wenn du einen kritischen Bug in der P2P-Synchronisation (z.B. Injection-Gefahr durch böswillige Peers) findest, empfehlen wir, einen entsprechenden Patch per Pull Request einzureichen. Wir vertrauen auf das Prinzip "Fix it, don't just report it".

## Sicherheit im Toobix P2P Netzwerk

### 1. Daten-Validierung
Das aktuelle Backend validiert und bereinigt P2P-Synchronisationseingaben (Input Sanitization). Zudem bereinigt das Frontend HTML-Eingaben über `escapeHtml()`, um grundlegende XSS-Angriffe zu verhindern. Da du dich mit unbekannten Peers verbinden könntest, achte immer darauf, ob sich Nodes "harmonisch" verhalten (Reputation / Praise / Criticism im Peer-Awareness Dashboard).

### 2. Keine Authentifizierung (By Design)
Toobix Node 2.0 besitzt bewusst keine Benutzer-Authentifizierung oder Login-Schranken. Jeder kann den lokalen Node abfragen. Wenn du deinen Node öffentlich (z.B. auf einem VPS) ins Internet stellst, ist die API (`/api/scarcity`, `/api/abundance`) für jeden erreichbar.

### 3. Keine verschlüsselten Nachrichten
Derzeit gibt es keine Ende-zu-Ende-Verschlüsselung (E2EE) für Einträge, da alles öffentlich als Bedarf/Angebot publiziert wird. Teile niemals geheime oder hochsensible Daten.
