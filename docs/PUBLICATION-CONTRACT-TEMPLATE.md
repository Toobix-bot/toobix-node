# Toobix Publication Contract

Dieses Dokument definiert die strikten Regeln für den Export von Daten aus dem privaten Toobix-System in die öffentliche `toobix-node` Instanz.

## 1. Grundsätze der Veröffentlichung
* **Write Authority:** Nur der menschliche Guardian (Micha) hat die Autorität, Daten aus diesem privaten System für die Veröffentlichung freizugeben. KIs oder automatisierte Skripte dürfen niemals eigenmächtig Daten nach außen synchronisieren.
* **Keine automatische Brücke:** Es existiert kein Live-Sync. Veröffentlichungen finden ausschließlich über den Export eines validierten JSON-Snapshots (gemäß `PUBLIC-SNAPSHOT.schema.json`) statt.

## 2. Erlaubte Inhalte
Folgende Kategorien dürfen veröffentlicht werden:
* Abstrahierte, generische Code-Strukturen und Architektur-Designs.
* Philosophische Prinzipien und Lore (z.B. Mangel/Überfluss KLR).
* Fiktive oder stark anonymisierte Beispiele für "Bedarf" und "Angebot", die keine Rückschlüsse auf reale Personen zulassen.

## 3. Verbotene Inhalte (Strictly Private)
Folgende Daten dürfen **niemals** veröffentlicht oder exportiert werden:
* Echte gesundheitliche, emotionale oder finanzielle Statusdaten (Runtime State).
* Echtnamen, echte Wohnorte oder direkte Kontaktadressen aus dem privaten Umfeld.
* OAuth-Tokens, API-Keys oder Systempfade.

## 4. Der Freigabe-Prozess
1. **Entwurf:** Eine KI oder Skript generiert einen Export-Vorschlag.
2. **Prüfung:** Der Guardian (Micha) prüft den Vorschlag auf Einhaltung der Regeln in Sektion 2 und 3.
3. **Signatur:** Der Export erhält das Flag `"approved_by": "Micha"` und `"contains_personal_data": false`.
4. **Übertragung:** Der Snapshot wird manuell in das öffentliche Repo überführt.

## 5. Rücknahme (Revocation)
Sollte versehentlich eine Information veröffentlicht werden, die gegen Sektion 3 verstößt, wird sie umgehend aus dem öffentlichen System entfernt und die Git-Historie des öffentlichen Repos wird bereinigt (filter-repo).
