# ⬡ Toobix Node 2.0

### Dezentrales Solidaritäts-Netzwerk

> **„Alle für alle! (Solidarität statt Isolation)"**

---

## 🌍 Was ist Toobix Node?

Toobix Node ist ein **dezentrales Peer-to-Peer Netzwerk**, das **Mangel** und **Überfluss** zusammenbringt – ohne zentralen Server, ohne Tracking, ohne Kosten.

Jeder Mensch ist ab Geburt Mitglied. Ob du deine Stimme aktivierst, entscheidest du. Kein Zwang. Kein Muss. Aber an alle ist gedacht.

### Was macht es?

| Funktion | Beschreibung |
|----------|-------------|
| 🔴 **Mangel melden** | Hilfe benötigt? Trage deinen Bedarf ein. |
| 🟢 **Überfluss teilen** | Du hast zu viel? Teile es mit anderen. |
| ⚖️ **Automatisches Matching** | Das System findet passende Angebote für Bedarfe. |
| 🧠 **Selbstreflexion** | Jeder Node erkennt seine eigenen Stärken und Schwächen. |
| 🤝 **Peer-Awareness** | Nodes bewerten sich gegenseitig: Lob bei guter Leistung, Kritik bei Problemen. |
| 🔄 **P2P-Synchronisation** | Daten werden direkt zwischen Nodes ausgetauscht – kein zentraler Server. |
| 🏥 **Echte Hilfsangebote** | Verifizierte Organisationen (Tafel, Kältebus, TelefonSeelsorge etc.) sind vorinstalliert. |

---

## 🚀 Schnellstart

```bash
# Klonen
git clone https://github.com/Toobix-bot/toobix-node.git
cd toobix-node

# Backend starten (keine externen Abhängigkeiten nötig!)
python3 -m app.main

# In einem zweiten Terminal: Front-End starten
python3 -m http.server 8080

# Browser öffnen
# Backend API: http://localhost:8000/api/health
# Front-End:   http://localhost:8080
```

### Voraussetzungen

- Python 3.10+
- Kein Framework nötig – 100% Python Standard Library

---

## 🌐 P2P-Netzwerk aufbauen

```bash
# Zweiten Node starten
PORT=8001 DB_PATH=node2.db python3 -m app.main

# Nodes verbinden
curl -X POST http://localhost:8000/api/peers/register \
  -H "Content-Type: application/json" \
  -d '{"peer_url":"http://127.0.0.1:8001"}'
```

Sobald verbunden, synchronisieren sich alle Einträge automatisch. Jeder Node bewertet seine Peers mit **Praise-Tokens** (👍) und **Criticism-Logs** (⚠️).

---

## 🐳 Docker

```bash
# Einzelner Container
docker build -t toobix-node .
docker run -d -p 8000:8000 -v toobix-data:/data toobix-node

# 3-Node-Netzwerk
docker-compose up -d
```

---

## 📡 API-Endpunkte

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| `GET` | `/api/health` | Node-Status |
| `GET` | `/api/reflection` | Selbstreflexion (Mangel/Überfluss/Harmonie) |
| `GET/POST` | `/api/scarcity` | Mangel-Einträge (Bedarfe) |
| `GET/POST` | `/api/abundance` | Überfluss-Einträge (Angebote) |
| `POST` | `/api/matches` | Matching berechnen |
| `GET` | `/api/peers` | Verbundene Peers |
| `POST` | `/api/peers/register` | Neuen Peer registrieren |
| `GET` | `/api/peers/awareness` | Peer-Bewertungen & Reputation |
| `POST` | `/api/p2p/sync` | Daten synchronisieren |

---

## 🏥 Vorinstallierte Hilfsangebote

| Organisation | Kategorie | Kontakt |
|-------------|-----------|---------|
| Tafel Deutschland e.V. | Nahrung | 030 20059760 |
| Kältebus Berlin | Unterkunft | 030 690333690 |
| Bahnhofsmission | Unterkunft | 030 314959-0 |
| TelefonSeelsorge | Psychologisch | 0800 111 0 111 |
| Kinder- und Jugendtelefon | Psychologisch | 116 111 |
| Hilfetelefon Gewalt gegen Frauen | Notfall | 116 016 |
| Medibüro Berlin | Medizin | 030 6946746 |

---

## 🏗️ Architektur

```
┌──────────────┐     P2P Sync      ┌──────────────┐
│  Node 1      │◄──────────────────►│  Node 2      │
│  :8000       │  Praise/Criticism  │  :8001       │
│              │                    │              │
│ Self-Reflect │                    │ Self-Reflect │
│ Matching     │                    │ Matching     │
│ SQLite DB    │                    │ SQLite DB    │
└──────────────┘                    └──────────────┘
        ▲           ┌──────────────┐         ▲
        └───────────│  Node 3      │─────────┘
                    │  :8002       │
                    └──────────────┘
```

---

## 🤝 Mitmachen

1. **Fork** dieses Repository
2. **Starte** deinen eigenen Node
3. **Verbinde** dich mit dem Netzwerk
4. **Teile** deine Ressourcen

Jede Hilfe zählt. Jede Stimme zählt. **Alle für alle.**

---

## 📜 Philosophie

> *„Jeder Mensch besitzt einen unantastbaren Wert, eine Stimme sowie individuelle Phasen von Mangel, Gleichgewicht und Überfluss."*

- **Kein Zwang, keine Kosten** – Die Teilnahme ist freiwillig.
- **Dezentral** – Keine Datenkrake, kein Master-Server.
- **Transparent** – Jeder Node reflektiert sich selbst und seine Peers.
- **Solidarisch** – Wer im Überfluss ist, gibt ab. Wer im Mangel ist, empfängt.

---

## 📄 Lizenz

Freie Software. Keine Cookies. Keine Nachverfolgung.

*Einer für alle und alle für einen – bzw. alle für alle statt einer für einen!*
