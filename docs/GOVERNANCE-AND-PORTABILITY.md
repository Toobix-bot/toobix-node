# TOOBIX Governance & Portability

Dieses Dokument definiert die Rollen, die Portabilität und die Governance-Struktur des TOOBIX-Ökosystems. Es stellt sicher, dass das Projekt eine transparente Infrastruktur bleibt und nicht von einzelnen Personen oder privaten Datenräumen abhängig ist.

## 1. Rollen im TOOBIX-Ökosystem

Um Vermischungen von Interessen und Architektur zu vermeiden, trennt TOOBIX strikt zwischen folgenden Rollen:

*   **Der Mensch (z. B. Michael):** Eine physische Person in der realen Welt. Ein Mensch hat unveräußerliche Rechte (Menschenwürde, Datenschutz) und existiert völlig unabhängig von TOOBIX.
*   **Die Entity:** Die digitale Repräsentation eines Akteurs innerhalb von TOOBIX (kann ein Mensch, eine Organisation oder eine Gemeinschaft sein). Eine Entity hat `Needs` (Bedürfnisse) und `Offers` (Angebote). Auch *Michael* ist im System lediglich eine reguläre Entity. Auch *TOOBIX* als Projekt kann eine Entity mit eigenen Needs und Offers sein.
*   **Das Projekt (TOOBIX):** Das Open-Source-Gemeingut (Commons), bestehend aus den Konzepten, der Verfassung, den Schemas und der Community.
*   **Die Runtime (Der Orchestrator):** Der laufende Software-Code (das Backend), der die JSON-Schemas durchsetzt, Matches berechnet und die Policy-Regeln anwendet. Die Runtime ist **nicht wertneutral**, sondern ein **regelgebundener, transparenter Orchestrator**, der ethische Normen (kein Social Scoring, Freiwilligkeit) in Code gießt.
*   **Der Operator (Node-Betreiber):** Eine Person oder Organisation (z. B. eine NGO), die eine eigene Instanz der Runtime betreibt.

## 2. Unabhängigkeit und Portabilität

TOOBIX ist so konzipiert, dass es **dezentral und unabhängig** betrieben werden kann.

*   **Daten-Souveränität:** Die TOOBIX-Runtime benötigt zu keinem Zeitpunkt Zugriff auf den privaten Datenraum (z. B. das private Asana, lokale Notizen oder private Kalender) des Gründers oder eines anderen Operators.
*   **Portabilität:** Jede Organisation kann das `toobix-node` Repository klonen und einen eigenen, unabhängigen Vermittlungs-Node betreiben. Die Regeln der Verfassung bleiben im Code verankert, aber die Datenhoheit liegt beim lokalen Operator und seinen lokalen Entities.
*   **Die Public/Private Bridge:** TOOBIX respektiert die absolute Trennung zwischen dem privaten Lebensraum (Private Life OS) und dem öffentlichen Austausch (Public Node). Daten fließen nur durch explizite menschliche Freigabe (Consent) von Privat nach Öffentlich.

## 3. Keine Neutralität, sondern klare Regeln

TOOBIX behauptet nicht, ein "neutrales" Technologie-Werkzeug zu sein. Es trifft bewusst normative Entscheidungen, die in der Architektur (`app/policy.py`) und den Schemas hart kodiert sind:

*   **Menschenwürde vor Effizienz:** Kein automatisches Sanktionieren, kein "Scoring" von Menschen, kein Zwang.
*   **Wirkung (LIFE) ist kein Geld:** LIFE-Punkte dürfen niemals die Priorität bei zukünftigen Matches beeinflussen. Hilfe bleibt bedingungslos.
*   **Transparenz der Entscheidung:** Jede KI-Entscheidung und jeder Match muss verständliche `reason_codes` ausgeben und steht unter dem Vorbehalt menschlicher Zustimmung (Human Gate).

Diese Governance stellt sicher, dass TOOBIX auch dann seinen Prinzipien treu bleibt, wenn es von unterschiedlichsten Akteuren in der Gesellschaft eingesetzt wird.
