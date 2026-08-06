# Datenschutz und Datenflüsse

Toobix Node 2.0 ist ein experimenteller lokaler Prototyp. Er ist nicht für vertrauliche oder besonders schützenswerte personenbezogene Daten ausgelegt.

## Lokal gespeicherte Daten

Bedarfe, Angebote, Matches, Peer-Adressen und technische Reflexionsdaten werden in einer lokalen SQLite-Datei gespeichert. Der Pfad wird über `DB_PATH` festgelegt.

## Peer-Synchronisation

Bei registrierten Peers können Bedarfe und Angebote an andere Nodes übertragen werden. Ab diesem Zeitpunkt liegen Kopien außerhalb des ursprünglichen Geräts. Der aktuelle Prototyp bietet keine garantierte Fernlöschung, keine Ende-zu-Ende-Verschlüsselung und keine zentrale Einwilligungsverwaltung.

Deshalb keine vertraulichen Gesundheits-, Ausweis-, Finanz-, vollständigen Adress-, privaten Kontakt- oder Zugangsdaten eintragen.

## Browser-Dashboard

Das Dashboard verwendet keine Cookies und kein Analytics. Ein API-Schlüssel wird bei Bedarf ausschließlich im `sessionStorage` der laufenden Browser-Sitzung gespeichert. Er wird beim Schließen der Sitzung normalerweise entfernt und kann über die Oberfläche zurückgesetzt werden.

## Netzwerkdaten

Beim Betrieb eines HTTP-Servers fallen technisch Verbindungsdaten wie IP-Adresse und Zeitpunkt an. Die Anwendung unterdrückt normale Request-Logs standardmäßig, Betriebssystem, Reverse Proxy, Containerplattform oder Hosting-Anbieter können jedoch eigene Protokolle führen.

## Externe Verbindungen

- Der Browser lädt keine externen Schriftarten oder Analyseskripte.
- P2P-Funktionen verbinden sich nur mit ausdrücklich registrierten Peer-URLs.
- Die optionale Datenpipeline kann öffentliche Webseiten abrufen.
- Links zu GitHub oder offiziellen Hilfsseiten verlassen die lokale Anwendung.

## Hilfs- und Seed-Daten

Eingebettete Hilfsdaten sind Startwerte. Telefonnummern, Öffnungszeiten, Zielgruppen und regionale Zuständigkeiten müssen vor Veröffentlichung und Nutzung redaktionell anhand offizieller Quellen geprüft werden.
