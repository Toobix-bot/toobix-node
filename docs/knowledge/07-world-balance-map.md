---
layout: knowledge
title: "World Balance Map"
permalink: /knowledge/07-world-balance-map/
---

# The World Balance Map

TOOBIX verwendet ein universelles, fraktales Datenmodell, um die Verteilung von Bedürfnissen (Needs), Ressourcen und Lücken (Gaps) zu kartieren. Anstatt für jede Ebene – von der lokalen Nachbarschaft bis zur globalen Weltbühne – ein eigenes System zu entwickeln, nutzen wir dasselbe hierarchiefreie Schema für jede Größenordnung.

Dieses Konzept nennen wir die **World Balance Map**.

## Ein Graph, kein starrer Baum

Die Realität lässt sich nicht immer sauber in administrative Ebenen wie *Stadt → Region → Land → Welt* einteilen. Ein Flusseinzugsgebiet ist keine politische Verwaltungsebene, ein Krankenhaus versorgt Menschen aus mehreren Regionen, und Krisen machen nicht an Grenzen halt.

Deshalb modelliert TOOBIX die Welt als **Graph**. 
Jeder "Balance Node" (Knoten) hat einen eigenen Gültigkeitsbereich (`scope`) und verbindet sich über Relationen (`relations`) wie `within`, `overlaps` oder `serves` mit anderen Knoten. 

*Hinweis: Die öffentliche World Balance Map fokussiert sich auf aggregierte Ebenen (ab der Community-Ebene) und klammert persönliche Einzeldaten bewusst aus (Privacy by Design).*

## Das Balance Node Schema

Jeder Knoten im Netzwerk beantwortet dieselben universellen Kernfragen:

*   **Needs**: Was braucht dieses System?
*   **Resources / Capacities**: Was hat es bereits? (z.B. Hilfsorganisationen, Budgets)
*   **Gaps**: Wo herrscht Mangel oder Überlastung? (Zusammen mit der Angabe, ob es an *Scarcity*, *Distribution* oder *Coordination* liegt).
*   **Risks**: Welche Gefahren und Verwundbarkeiten bestehen? 
*   **Evidence**: Wie verlässlich, aktuell und aussagekräftig sind unsere Daten?

Die Risiko-Observationen können dabei an internationale Standards wie **INFORM Risk** anknüpfen, ohne dass TOOBIX seine eigene neutrale Bewertungssprache verliert.

## Reality Bridge (Beispiel)

Ein beispielhafter globaler Knoten könnte so aussehen, um globale Dürre und Ernährungsunsicherheit zu modellieren:

```yaml
scope:
  kind: "world"
  name: "Global Food Security Observation"
relations:
  - type: "within"
    target: "universe"
need_refs:
  - "need:global_food_123"
resource_refs:
  - "resource:wfp_budget_2026"
gap_assessments:
  - type: "absolute scarcity"
    severity: "high"
    basis: "derived"
    need_refs: ["need:global_food_123"]
    resource_refs: ["resource:wfp_budget_2026"]
    reason: "Global grain shortage due to consecutive droughts"
risk_observations:
  pressure:
    description: "Climate change induced severe weather patterns"
  vulnerability:
    description: "High reliance on rainfed agriculture in vulnerable regions"
  capacity:
    description: "International aid and strategic grain reserves"
  external_metrics:
    inform_risk_2026:
      hazard_and_exposure: 7.2
      vulnerability: 5.1
      lack_of_coping_capacity: 6.4
      scale: "0-10"
      source_methodology: "INFORM Risk"
evidence:
  confidence: "medium"
  freshness: "current"
  coverage: "comprehensive"
  source_count: 5
  observed_at: "2026-08-01"
  method: "aggregated_reports"
references:
  sdg: ["2.1", "2.2"]
```

Mit diesem Modell kann TOOBIX Daten von NGOs, Institutionen und lokalen Trackern aufnehmen und als verbundene Map darstellen – um Lücken sichtbar zu machen und Ressourcen dorthin zu lenken, wo sie wirklich gebraucht werden.
