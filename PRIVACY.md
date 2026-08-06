# Datenschutzerklärung (Privacy Policy)

**Stand:** August 2026

Toobix Node 2.0 ist als dezentrales Peer-to-Peer Netzwerk konzipiert, bei dem Privatsphäre an erster Stelle steht ("Zero Tracking").

## 1. Datenverarbeitung durch das Toobix-Node Backend

Wenn du einen Toobix Node betreibst (z.B. über `python -m app.main`), passiert Folgendes mit deinen Daten:

*   **Lokale Speicherung:** Alle Einträge zu "Mangel" und "Überfluss", die du auf deinem Node erstellst, werden ausschließlich in einer lokalen SQLite-Datenbank (`toobix_node.db`) auf deinem Rechner gespeichert.
*   **P2P-Synchronisation:** Sobald du deinen Node mit anderen Peers verbindest (über `/api/peers/register`), werden deine öffentlichen Mangel- und Überfluss-Einträge mit diesen verbundenen Nodes synchronisiert. Sende daher keine echten Klarnamen oder sensiblen persönlichen Daten als Teil der Beschreibung, wenn du diese nicht öffentlich im Netzwerk teilen möchtest.
*   **Log-Daten & Metadaten:** Das Backend verarbeitet bei eingehenden P2P-Verbindungen die IP-Adresse/URL des verbundenen Peers. Diese wird genutzt, um die Reputation und "Peer-Awareness" (Praise/Criticism) zu berechnen. 

## 2. Datenverarbeitung durch das Frontend / GitHub Pages

Die statische Version dieser Webseite (z.B. auf GitHub Pages):
*   verwendet **keine Cookies**.
*   verwendet **keine externen Tracking-Scripte** (wie Google Analytics).
*   lädt **keine externen Schriftarten** (Google Fonts wurde vollständig entfernt).
*   kommuniziert nur dann mit einem Toobix Node, wenn du das lokale Backend (`http://localhost:8000`) parallel auf deinem Gerät startest. Ohne laufendes Backend findet keine Datenübertragung statt.

Wenn du die Webseite besuchst, die auf GitHub Pages gehostet wird, gelten zusätzlich die [Datenschutzbestimmungen von GitHub](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement), da GitHub beim Aufruf der Seite zwangsläufig deine IP-Adresse erfassen muss, um die Daten auszuliefern.

## 3. Externe Notfallnummern

Das Toobix-System listet verifizierte, offizielle Notfallnummern (z.B. TelefonSeelsorge, Kältebus). Diese Nummern werden nur in der Datenbank bereitgestellt. Wenn du diese klickst oder anrufst, verlässt du den Bereich des Toobix-Netzwerks.

## 4. Anonymität

Toobix erfordert kein Benutzerkonto, keine E-Mail-Adresse und kein Passwort. Die Nutzung des Frontends und das Lesen der Hilfsangebote ist komplett anonym.

*Alle für alle!*
