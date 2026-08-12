---
title: "Build your own Knowledge Node"
description: "Ein möglichst einfacher Einstieg, um TOOBIX zu forken, anzupassen und als eigenen offenen Wissensknoten für eine Region, ein Thema oder eine Gemeinschaft weiterzubauen."
permalink: /knowledge/build-your-own/
updated: "2026-08-12"
version: "0.1"
confidence: "project-guide"
status: "experimental"
schema_type: "HowTo"
---

## Idee

TOOBIX soll nicht nur benutzt werden können. **Es soll kopierbar, veränderbar und weiterbaubar sein.**

Du musst weder TOOBIX übernehmen noch dieselben Begriffe verwenden. Der Baukasten soll dir den Einstieg erleichtern, wenn du ebenfalls Bedürfnisse, Ressourcen, Wissen oder Hilfsstrukturen verständlicher verbinden möchtest.

Das Repository steht unter der MIT-Lizenz. Dadurch darfst du Code und zugehörige Dokumentation verwenden, kopieren, verändern und weitergeben, solange der Lizenzhinweis erhalten bleibt.

## Minimaler Start

### 1. Repository forken

Forke `Toobix-bot/toobix-node` auf GitHub oder klone es lokal.

### 2. Eigene Fragestellung wählen

Starte klein, zum Beispiel:

- Hilfsangebote in einer Gemeinde,
- Barrierefreiheit in einer Stadt,
- lokale Bildungsressourcen,
- offene Reparatur- und Leihangebote,
- Ressourcen für pflegende Angehörige,
- Umwelt- oder Klimaanpassungsangebote,
- bestehende Organisationen rund um ein klar begrenztes Thema.

### 3. Eigene Knowledge-Seite anlegen

Verwende dieses Frontmatter-Muster:

```yaml
---
title: "Dein Thema"
description: "Eine präzise Beschreibung."
permalink: /knowledge/dein-thema/
updated: "YYYY-MM-DD"
version: "0.1"
confidence: "mixed"
status: "experimental"
schema_type: "Article"
sources:
  - title: "Originalquelle"
    publisher: "Herausgeber"
    url: "https://..."
---
```

Danach sollte jede Seite möglichst beantworten:

1. Was wissen wir?
2. Woher wissen wir es?
3. Was ist Interpretation oder Hypothese?
4. Was wissen wir noch nicht?
5. Welche Ressourcen existieren bereits?
6. Welche konkrete Lücke könnte bestehen?
7. Was wäre ein kleiner, überprüfbarer nächster Schritt?

### 4. Datenschutz vor Vollständigkeit

Veröffentliche keine privaten Adressen, Diagnosen, Zugangsdaten, vertraulichen Nachrichten oder andere sensible personenbezogene Daten, nur weil sie für ein Modell nützlich wären.

Für lokale Hilfsangebote gilt möglichst:

```text
öffentliche Originalquelle
→ grobe, notwendige Information
→ Link zur zuständigen Stelle
```

statt private Kontaktdaten zu kopieren.

### 5. Unsicherheit sichtbar lassen

Nutze beispielsweise:

- 🟢 belegt
- 🟡 plausible Interpretation
- 🟣 offene Hypothese
- ⚪ unbekannt

Ein ehrliches `unknown` ist besser als eine erfundene Antwort.

### 6. Veröffentlichen

GitHub Pages kann Markdown mit YAML Frontmatter über Jekyll als statische Website ausgeben. Passe `_config.yml` an deinen Repository-Namen und deine Domain an.

### 7. Wirkung prüfen

Ein Knowledge Node ist nicht automatisch hilfreich, nur weil er online steht. Frage später:

- Wird die Information gefunden?
- Wird sie korrekt verstanden?
- Ist sie aktuell?
- Verweist sie auf die richtige Originalquelle?
- Hat jemand dadurch eine bessere Entscheidung oder Verbindung gefunden?

## Du darfst TOOBIX verändern

Du kannst:

- andere Kategorien verwenden,
- neue Datenquellen integrieren,
- nur einen kleinen lokalen Ausschnitt betreiben,
- LIFE komplett weglassen,
- andere Designs bauen,
- andere Sprachen verwenden,
- TOOBIX als Ausgangspunkt für ein eigenes Projekt nutzen.

Was wir uns wünschen: **Bewahre Transparenz, Datenschutz, Korrigierbarkeit und menschliche Würde als starke Designziele – und dokumentiere klar, wo dein Fork andere Entscheidungen trifft.**

## Verbesserungen zurückgeben

Wenn du etwas findest, das auch dem ursprünglichen Projekt hilft, kannst du freiwillig ein Issue oder einen Pull Request öffnen. Ein Fork muss aber nicht zentral kontrolliert werden, um nützlich zu sein.

> Nimm, was dir hilft. Prüfe es. Verändere es. Bau etwas Sinnvolles daraus. Und lass anderen dieselbe Freiheit.
