# Toobix Exchange Node 2.0

Ein lokaler, datensparsamer Konzeptprototyp für solidarischen Austausch von Angeboten, Bedarfen, Zeit und Fähigkeiten.

## Aktueller Status

Toobix Node 2.0 ist derzeit **kein produktives dezentrales Netzwerk**. Es ist eine statische, lokal nutzbare Webanwendung ohne Benutzerkonten, Server-Datenbank oder Synchronisation zwischen Geräten.

Bereits umgesetzt:

- Status-Tacho für Mangel, Gleichgewicht und Überfluss
- lokale Angebots- und Bedarfseinträge
- dauerhafte Speicherung dieser Einträge im Browser über `localStorage`
- lokale Löschfunktion
- Makro-Explorer mit beispielhaften Hilfsnetzwerken
- Transparenz-Chronik und druckbarer Flyer
- keine Cookies, kein Analytics und keine externen Schrift- oder Skript-Abhängigkeiten

Noch nicht umgesetzt:

- echte Vernetzung mehrerer Personen oder Geräte
- Moderation, Identitätsprüfung oder Missbrauchsschutz
- verschlüsselte Synchronisation
- belastbares Credit- oder Abrechnungssystem
- redaktionell gepflegte regionale Hilfsdatenbank

## Lokal starten

Repository herunterladen oder klonen und anschließend `index.html` direkt im Browser öffnen. Es ist kein Build-Schritt und kein Server erforderlich.

## Datenschutz

Die Webanwendung sendet von sich aus keine Eingaben an einen Server. Selbst erstellte Angebote und Bedarfe verbleiben im lokalen Browser-Speicher des verwendeten Geräts. Über die Schaltfläche **„Lokale Einträge löschen“** können diese Daten entfernt werden.

Wichtig: Browser-Speicher ist keine verschlüsselte Datenbank. Keine vertraulichen Gesundheits-, Kontakt-, Finanz- oder Zugangsdaten eintragen.

Weitere Hinweise stehen in [PRIVACY.md](PRIVACY.md) und [SECURITY.md](SECURITY.md).

## Veröffentlichung

Die Seite kann als statische Website beispielsweise über GitHub Pages, Netlify oder einen vergleichbaren Anbieter bereitgestellt werden. Vor einer öffentlichen Nutzung müssen Hilfsangebote, Telefonnummern und regionale Informationen redaktionell geprüft und regelmäßig aktualisiert werden.

## Projektstruktur

- `index.html` – Struktur und Inhalte
- `style.css` – responsives Design ohne externe Fonts
- `app.js` – lokale Interaktion und Speicherung
- `flyer_solidaritaet.html` – druckbarer Konzept-Flyer
- `PRIVACY.md` – Datenschutzgrenzen
- `SECURITY.md` – Sicherheits- und Meldehinweise
- `LICENSE` – MIT-Lizenz

## Lizenz

Dieses Repository steht unter der MIT-Lizenz. Die Lizenz gilt für den Code und die mitgelieferten Vorlagen, soweit keine abweichenden Rechte Dritter betroffen sind.
