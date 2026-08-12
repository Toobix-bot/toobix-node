---
title: "Needs, Resources & Gaps"
description: "Ein einfaches Modell, um Bedarf, vorhandene Kapazität, Dringlichkeit, Trend und Versorgungslücken auf verschiedenen Ebenen sichtbar zu machen."
permalink: /knowledge/needs-resources-gaps/
updated: "2026-08-12"
version: "0.1"
confidence: "mixed"
status: "experimental"
schema_type: "TechArticle"
sources:
  - title: "INFORM Risk"
    publisher: "European Commission Joint Research Centre"
    url: "https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk"
  - title: "Humanitarian API (HAPI)"
    publisher: "Humanitarian Data Exchange / OCHA"
    url: "https://hdx-hapi.readthedocs.io/"
  - title: "Human Services Data Specification"
    publisher: "Open Referral"
    url: "https://docs.openreferral.org/"
---

## Warum nicht nur Probleme kartieren?

Ein großes Problem kann bereits starke Hilfsstrukturen haben. Ein kleinerer Bedarf kann dagegen fast vollständig ohne Unterstützung bleiben. Deshalb betrachtet TOOBIX mindestens zwei Seiten gleichzeitig:

```text
PRESSURE / NEEDS  ↔  CAPACITY / RESOURCES
                         ↓
                        GAP
```

## Ein einfaches Raster

| Dimension | Frage |
|---|---|
| Severity | Wie schwer ist die Lage? |
| Urgency | Wie schnell ist Handeln nötig? |
| Scale | Wie viele bzw. welche besonders verletzlichen Gruppen sind betroffen? |
| Capacity | Welche geeignete Hilfe existiert bereits? |
| Trend | Verbessert oder verschlechtert sich die Lage? |
| Evidence | Wie sicher und aktuell sind die Informationen? |
| Connectability | Kann bessere Verbindung überhaupt sinnvoll helfen? |

## Zustände

- 🟢 **tragfähig** — vorhandene Kapazität deckt den Bedarf weitgehend.
- 🟡 **angespannt** — Druck oder Lücke wächst.
- 🟠 **überlastet** — Bedarf übersteigt vorhandene Kapazität deutlich.
- 🔴 **kritisch** — Grundbedarf, Sicherheit oder Funktionsfähigkeit sind akut gefährdet.
- ⚪ **unbekannt** — Daten reichen nicht für eine belastbare Einschätzung.

Diese Farben sind **Darstellungshilfen**, keine objektiven Naturkonstanten.

## Vier verschiedene Problemarten

### A. Ressourcenmangel
Eine notwendige Ressource existiert tatsächlich nicht in ausreichender Menge.

### B. Zugangs- oder Verteilungsproblem
Die Ressource existiert, erreicht Betroffene aber nicht zuverlässig.

### C. Koordinationsproblem
Bedarf und passende Ressource existieren, kennen oder erreichen sich jedoch nicht.

### D. Interessenkonflikt
Mehrere legitime Ziele stehen miteinander in Spannung; ein einfacher Match löst das Problem nicht.

🟣 **TOOBIX-Hypothese:** Besonders bei B und C kann eine gute Übersetzungs- und Verbindungsschicht vergleichsweise viel bewirken. Bei A und D braucht es häufig zusätzliche Ressourcen, Politik, Finanzierung, Fachwissen oder Aushandlung.

## Zoomstufen

Dasselbe Grundmodell kann theoretisch auf unterschiedlichen Maßstäben verwendet werden:

```text
Mensch → Haushalt → Nachbarschaft → Gemeinde → Region → Land → Kontinent → Welt
```

Je näher die Ebene an einzelnen Menschen liegt, desto stärker müssen Datenschutz, Einwilligung und Zugriffsbeschränkungen werden.

## Kein universeller Welt-Score

TOOBIX soll Länder, Städte oder Menschen nicht auf einen einzigen "Gut/Schlecht"-Wert reduzieren. Ein Ort kann gleichzeitig hohe Versorgung in einer Dimension und kritische Lücken in einer anderen haben.
