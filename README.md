# Toobix Exchange Node 2.0 – Anleitung für Veröffentlichung & Hosting (0 € Kosten)

Dieses Paket enthält die vollständige, anonymisierte und datenschutzkonforme Webanwendung **Toobix Node 2.0**.

## 1. Woraus besteht dieses Paket?

*   `index.html`: Das barrierefreie HTML5-Grundgerüst mit Manifest, Status-Tacho, Tauschbörse, Makro-Explorer, KLR-Chronik und anonymisiertem SOS-Netzwerk.
*   `style.css`: Das moderne Vanilla CSS Design im Dark Mode / Glassmorphismus-Stil.
*   `app.js`: Die interaktive JavaScript-Logik für den Slider, das lokale Hinzufügen von Einträgen, die Filterung von Netzwerken und das Rendern der Chronik.

## 2. Wie teste ich es lokal?

Öffne einfach die Datei `index.html` in deinem Browser (z.B. per Doppelklick oder per Eingabe von `file:///home/michael-horn/.gemini/antigravity/scratch/ToobixWeb/index.html` in der Adresszeile).

## 3. Wie mache ich die Seite kostenlos für die ganze Welt öffentlich?

Da die Webseite komplett statisch ist (keine Datenbank-Server erforderlich, 100% datenschutzfreundlich), kann sie über mehrere plattformunabhängige Anbieter **dauerhaft kostenlos** gehostet werden:

### Option A: Netlify Drop (Einfachste Methode, dauert 30 Sekunden)
1. Gehe auf [app.netlify.com/drop](https://app.netlify.com/drop).
2. Ziehe den gesamten Ordner `ToobixWeb` per Drag & Drop in das Browserfenster.
3. Netlify generiert dir sofort eine kostenlose, SSL-verschlüsselte Webadresse (z.B. `https://toobix-node.netlify.app`).

### Option B: GitHub Pages (Ideal für Open Source)
1. Erstelle ein kostenloses Repository auf GitHub.
2. Lade `index.html`, `style.css` und `app.js` hoch.
3. Aktiviere *GitHub Pages* in den Repository-Einstellungen. Die Seite ist unter `https://dein-name.github.io/toobix-node` erreichbar.

### Option C: Vercel / Render
Funktioniert genauso einfach über Import des Ordners oder Repositories.

## 4. Datenschutz & Sicherheit

*   **Keine Klarnamen:** Alle vertraulichen Personenbezüge wurden anonymisiert.
*   **Keine Cookies / Kein Tracking:** Es werden keinerlei personenbezogene Daten gesammelt oder verarbeitet.
*   **Keine externen Server-Abhängigkeiten:** Keine externen Analytics-Skripte.

Viel Erfolg beim Verbinden von Mangel, Gleichgewicht und Überfluss!
