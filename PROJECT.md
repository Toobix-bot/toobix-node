# Project: Toobix Node 2.0 Backend

## Architecture
"Toobix Node 2.0" is a decentralized, peer-to-peer (P2P) resource distribution backend designed for solidarity-driven allocation ("Alle für alle!").
The architecture consists of three core subsystems:
1. **Backend Engine**: REST API for registering and matching local needs ("Mangel") and abundance offers ("Überfluss") using multi-factor matching algorithms (Category, Jaccard Keyword Similarity, Location). Built using Python standard library / FastAPI compatible HTTP routing and SQLite database storage (`toobix_node.db`).
2. **Automated Data Pipeline (Scraper)**: 5-stage ETL pipeline (Fetch -> Parse -> Clean -> Validate -> Ingest) that extracts emergency contact networks and solidarity help offers from live public sources and embedded fallback seeds, populating the local node database.
3. **P2P Synchronization Engine**: Serverless peer-to-peer sync engine using HTTP REST endpoints (`/api/peers/register`, `/api/peers`, `/api/p2p/sync`), push/pull synchronization, UUID primary keys, and Last-Write-Wins (LWW) timestamp conflict resolution.

## Code Layout
```
toobix_node_backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # Main application entry point & HTTP server
│   ├── models.py          # Data models (MangelEntry, UeberflussEntry, HelpOffer, Peer)
│   ├── db.py              # SQLite database storage & query layer
│   ├── matching.py        # Multi-factor matching logic engine
│   ├── pipeline.py        # Automated scraper & data pipeline
│   └── p2p.py             # P2P peer discovery and state synchronization
├── pytest                 # Executable shim script for running pytest in isolated environments
├── pytest.py              # Python module shim for pytest compatibility
├── fastapi/               # Pure-Python compatibility shim module for FastAPI if missing
├── pydantic/              # Pure-Python compatibility shim module for Pydantic if missing
├── test_backend.py        # Backend verification suite (pytest test_backend.py)
├── test_pipeline.py       # Pipeline verification suite (test_pipeline.py)
├── test_p2p.sh            # P2P multi-node verification bash script (test_p2p.sh)
└── PROJECT.md             # Architecture, feature inventory, milestones, interface contracts
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Mangel Data Model & API | Record, store, retrieve scarcity requests (Mangel) | M1 | Survey R1 |
| 2 | Überfluss Data Model & API | Record, store, retrieve abundance offers (Überfluss) | M1 | Survey R1 |
| 3 | Matching Logic Engine | Multi-factor category/keyword/location matching algorithm | M1 | Survey R1 |
| 4 | Backend Verification Suite | `pytest test_backend.py` verifying backend operations | M1 | Survey R1 |
| 5 | Solidarity Data Scraper | Extract emergency contacts & solidarity networks | M2 | Survey R2 |
| 6 | Data Pipeline Ingestion | ETL pipeline storing >= 5 structured help offers | M2 | Survey R2 |
| 7 | Pipeline Verification Suite | `test_pipeline.py` outputting >= 5 offers with exit code 0 | M2 | Survey R2 |
| 8 | Multi-Node Port Binding | Configurable port binding (8001, 8002) & database isolated paths | M3 | Survey R3 |
| 9 | P2P Peer Discovery & REST | Peer registration endpoints (`/api/peers/register`, `/api/peers`) | M3 | Survey R3 |
| 10| P2P State Synchronization | Push/pull sync of Mangel/Überfluss entries with UUID & LWW resolution | M3 | Survey R3 |
| 11| P2P Verification Script | `test_p2p.sh` spawning 2 nodes, posting to Node 1, verifying on Node 2 | M3 | Survey R3 |
| 12| Node Self-Reflection Engine | Self-monitoring generating self-Mangel (needs) & self-Überfluss (offers) | M1 | Requirement R4 |
| 13| Multi-Perspective Environment Awareness | Peer reputation, praising/criticism metrics, mutual peer observation | M3 | Requirement R5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Automated Verifiable Backend | Implement FastAPI-compatible backend, matching engine, self-reflection engine (R4), and `pytest test_backend.py` | none | DONE |
| 2 | M2: Automated Data Pipeline | Implement scraper ETL pipeline, seed fallback dataset, and `test_pipeline.py` | M1 | DONE |
| 3 | M3: P2P Synchronization & Peer Awareness | Implement P2P endpoints, multi-node port config, state sync, peer awareness (R5), and `test_p2p.sh` | M1 | DONE |
| 4 | M4: E2E Integration & Verification | Run full E2E test suite across all acceptance criteria (Tiers 1-5) | M1, M2, M3 | IN_PROGRESS |

## Interface Contracts

### Backend API (M1)
- `POST /api/scarcity` (Payload: `{ "title": str, "category": str, "description": str, "location": str, "contact": str }`) -> returns `201 Created` with full `MangelEntry` JSON (including `id`, `created_at`).
- `GET /api/scarcity` -> returns `200 OK` list of `MangelEntry` objects.
- `POST /api/abundance` (Payload: `{ "title": str, "category": str, "description": str, "location": str, "contact": str }`) -> returns `201 Created` with full `UeberflussEntry` JSON (including `id`, `created_at`).
- `GET /api/abundance` -> returns `200 OK` list of `UeberflussEntry` objects.
- `POST /api/matches` (Payload: `{ "scarcity_id": str }` or query all) -> returns `200 OK` list of `MatchResult` objects (`scarcity_id`, `abundance_id`, `score`, `match_reason`).
- `GET /api/health` -> returns `200 OK` `{ "status": "ok", "node_id": str }`.
- `POST /api/reflection` or `GET /api/reflection` -> triggers self-monitoring evaluation of node state (RAM/CPU/errors vs uptime/idle resources), posts self-Mangel/self-Überfluss entries to DB, and returns `200 OK` JSON `{ "generated_mangel": List[dict], "generated_ueberfluss": List[dict] }`.

### Data Pipeline (M2)
- Entry point: `app/pipeline.py` function `run_pipeline() -> List[HelpOffer]`.
- Output Schema `HelpOffer`: `{ "id": str, "title": str, "category": str, "description": str, "services": List[str], "contact": str, "location": str, "is_emergency": bool, "source_url": str }`.
- Automatically ingests into backend database as `UeberflussEntry` records.

### P2P Sync API (M3)
- `POST /api/peers/register` (Payload: `{ "peer_url": str }`) -> registers external peer node URL.
- `GET /api/peers` -> returns list of known peer node URLs.
- `POST /api/p2p/sync` (Payload: `{ "type": "mangel" | "ueberfluss", "entries": List[dict] }`) -> ingests remote entries, deduplicating by `id` using Last-Write-Wins based on `updated_at`.
- Node Port & DB configuration via environment variables: `PORT` (default: 8000), `DB_PATH` (default: `toobix_node.db`).
