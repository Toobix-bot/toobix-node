"""
P2P Peer Discovery, Synchronization, and Multi-Perspective Peer Awareness Engine.
Supports peer registration, push/pull state sync with UUID deduplication and LWW conflict resolution,
infinite loop prevention, and multi-perspective peer reputation/praise/criticism tracking (Requirement R5).
"""

import json
import logging
import threading
import time
import urllib.request
import urllib.error
import uuid
from typing import Dict, Any, List, Optional

from app.db import Database
from app.models import MangelEntry, UeberflussEntry, Peer

logger = logging.getLogger(__name__)


class PeerAwarenessEngine:
    """
    Multi-Perspective Environment Awareness Engine (Requirement R5).
    Evaluates peer health, uptime, response time, payload validity,
    maintains reputation scores, generates praise/criticism tokens and logs.
    """
    def __init__(self):
        self._lock = threading.Lock()
        # peer_url -> dict of metrics
        self.peer_metrics: Dict[str, Dict[str, Any]] = {}
        # List of praise/criticism log events
        self.history: List[Dict[str, Any]] = []

    def evaluate_peer(self, peer_url: str) -> Dict[str, Any]:
        """
        Evaluate a single peer by pinging its health endpoint.
        Generate Praise token on fast/valid response (+1 reputation, status='praised').
        Generate Criticism/Warning token on slow/invalid/unresponsive response (-1 reputation, status='criticized'/'questioned').
        """
        clean_url = peer_url.strip().rstrip("/")
        if not clean_url:
            return {}

        health_url = f"{clean_url}/api/health"
        
        start_time = time.time()
        success = False
        response_time_ms = 0.0
        error_msg = None
        payload = None

        try:
            req = urllib.request.Request(health_url, headers={"User-Agent": "Toobix-Node-P2P/2.0"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                response_time_ms = (time.time() - start_time) * 1000.0
                if resp.status == 200:
                    body = resp.read().decode("utf-8")
                    payload = json.loads(body)
                    if isinstance(payload, dict) and (payload.get("status") == "ok" or "node_id" in payload):
                        success = True
                    else:
                        error_msg = "Malformed health response"
                else:
                    error_msg = f"HTTP status {resp.status}"
        except urllib.error.URLError as e:
            response_time_ms = (time.time() - start_time) * 1000.0
            error_msg = f"Connection error: {e.reason}"
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000.0
            error_msg = f"Error: {e}"

        now = time.time()
        with self._lock:
            if clean_url not in self.peer_metrics:
                self.peer_metrics[clean_url] = {
                    "url": clean_url,
                    "reputation_score": 0,
                    "status": "neutral",
                    "praise_count": 0,
                    "criticism_count": 0,
                    "last_seen": now,
                    "last_response_time_ms": round(response_time_ms, 2),
                    "health": "unknown"
                }

            metrics = self.peer_metrics[clean_url]
            metrics["last_seen"] = now
            metrics["last_response_time_ms"] = round(response_time_ms, 2)

            if success and response_time_ms < 2000.0:
                metrics["reputation_score"] += 1
                metrics["status"] = "praised"
                metrics["praise_count"] += 1
                metrics["health"] = "healthy"
                token = f"PRAISE-{uuid.uuid4().hex[:8].upper()}"
                event = {
                    "timestamp": now,
                    "peer_url": clean_url,
                    "type": "praise",
                    "token": token,
                    "reason": f"Peer responsive ({response_time_ms:.1f}ms) with valid health payload",
                    "response_time_ms": round(response_time_ms, 2),
                    "reputation_after": metrics["reputation_score"]
                }
                self.history.append(event)
            else:
                metrics["reputation_score"] -= 1
                metrics["status"] = "criticized" if error_msg else "questioned"
                metrics["criticism_count"] += 1
                metrics["health"] = "degraded" if success else "unresponsive"
                reason_str = error_msg or f"Slow response time ({response_time_ms:.1f}ms)"
                token = f"CRITICISM-{uuid.uuid4().hex[:8].upper()}"
                event = {
                    "timestamp": now,
                    "peer_url": clean_url,
                    "type": "criticism",
                    "token": token,
                    "reason": f"Peer warning/criticism: {reason_str}",
                    "response_time_ms": round(response_time_ms, 2),
                    "reputation_after": metrics["reputation_score"]
                }
                self.history.append(event)

            if len(self.history) > 200:
                self.history = self.history[-200:]

            return dict(metrics)

    def get_awareness_summary(self, peers: List[Peer]) -> Dict[str, Any]:
        """
        Evaluate active peers and generate full multi-perspective network awareness summary.
        """
        for peer in peers:
            self.evaluate_peer(peer.url)

        with self._lock:
            reputation_scores = {url: m["reputation_score"] for url, m in self.peer_metrics.items()}
            total_peers = len(peers)
            praised_count = sum(1 for m in self.peer_metrics.values() if m["status"] == "praised")
            criticized_count = sum(1 for m in self.peer_metrics.values() if m["status"] in ("criticized", "questioned"))

            overall_status = "harmonious"
            if praised_count == 0 and total_peers > 0:
                overall_status = "degraded"
            elif criticized_count > praised_count:
                overall_status = "tense"

            return {
                "peers": {url: dict(m) for url, m in self.peer_metrics.items()},
                "reputation_scores": reputation_scores,
                "reputation": reputation_scores,
                "history": list(self.history),
                "praise_criticism_history": list(self.history),
                "network_awareness_summary": {
                    "total_peers": total_peers,
                    "praised_peers": praised_count,
                    "criticized_peers": criticized_count,
                    "overall_status": overall_status
                }
            }


# Singleton peer awareness engine instance
awareness_engine = PeerAwarenessEngine()


def register_peer(db: Database, peer_url: str) -> Dict[str, Any]:
    """Register a new peer URL in local database."""
    if not peer_url or not isinstance(peer_url, str):
        raise ValueError("peer_url string is required")
    clean_url = peer_url.strip().rstrip("/")
    if not clean_url:
        raise ValueError("peer_url cannot be empty")

    peer = Peer(url=clean_url, last_seen=time.time(), is_active=True)
    db.save_peer(peer)

    threading.Thread(target=awareness_engine.evaluate_peer, args=(clean_url,), daemon=True).start()

    active_peers = db.list_peers()
    return {
        "status": "registered",
        "peer_url": clean_url,
        "total_peers": len(active_peers),
        "peers": [p.url for p in active_peers]
    }


def unregister_peer(db: Database, peer_url: str) -> Dict[str, Any]:
    """Unregister a peer URL in local database."""
    if not peer_url or not isinstance(peer_url, str):
        raise ValueError("peer_url string is required")
    clean_url = peer_url.strip().rstrip("/")

    peers = db.list_peers()
    target_peer = None
    for p in peers:
        if p.url.rstrip("/") == clean_url:
            target_peer = p
            break

    if target_peer:
        target_peer.is_active = False
        db.save_peer(target_peer)

    active_peers = db.list_peers()
    return {
        "status": "unregistered",
        "peer_url": clean_url,
        "total_peers": len(active_peers)
    }


def list_peers(db: Database) -> Dict[str, Any]:
    """Return list of registered active peer URLs."""
    peers = db.list_peers()
    urls = [p.url for p in peers]
    return {
        "peers": urls,
        "peer_details": [p.to_dict() for p in peers]
    }


def ingest_p2p_entries(db: Database, payload: Any) -> Dict[str, Any]:
    """
    Ingest pushed or pulled P2P entries into local DB with deduplication and Last-Write-Wins (LWW) resolution.
    Prevent sync loops: saved locally without re-broadcasting.
    """
    if not isinstance(payload, dict):
        if isinstance(payload, list):
            payload = {"entries": payload}
        else:
            raise ValueError("Payload must be a JSON object or list")

    entries_list: List[Dict[str, Any]] = []

    if "entries" in payload and isinstance(payload["entries"], list):
        entries_list.extend(payload["entries"])
    elif "entry" in payload and isinstance(payload["entry"], dict):
        entries_list.append(payload["entry"])
    elif "mangel" in payload or "ueberfluss" in payload or "scarcity" in payload or "abundance" in payload:
        for k in ["mangel", "scarcity"]:
            val = payload.get(k)
            if isinstance(val, list):
                for e in val:
                    if isinstance(e, dict):
                        e_copy = dict(e)
                        e_copy["_forced_type"] = "mangel"
                        entries_list.append(e_copy)
            elif isinstance(val, dict):
                val_copy = dict(val)
                val_copy["_forced_type"] = "mangel"
                entries_list.append(val_copy)

        for k in ["ueberfluss", "abundance"]:
            val = payload.get(k)
            if isinstance(val, list):
                for e in val:
                    if isinstance(e, dict):
                        e_copy = dict(e)
                        e_copy["_forced_type"] = "ueberfluss"
                        entries_list.append(e_copy)
            elif isinstance(val, dict):
                val_copy = dict(val)
                val_copy["_forced_type"] = "ueberfluss"
                entries_list.append(val_copy)
    elif "title" in payload and "category" in payload:
        entries_list.append(payload)

    forced_type = payload.get("type")

    received = len(entries_list)
    added = 0
    updated = 0
    skipped = 0

    for raw_entry in entries_list:
        if not isinstance(raw_entry, dict):
            skipped += 1
            continue

        entry_type = (
            raw_entry.get("_forced_type")
            or forced_type
            or raw_entry.get("type")
        )

        if not entry_type:
            if "quantity" in raw_entry:
                entry_type = "ueberfluss"
            elif "urgency" in raw_entry:
                entry_type = "mangel"
            else:
                entry_type = "mangel"

        entry_type = str(entry_type).lower()

        if entry_type in ("mangel", "scarcity"):
            entry_obj = MangelEntry.from_dict(raw_entry)
            existing = db.get_mangel(entry_obj.id)
            if existing is None:
                db.save_mangel(entry_obj)
                added += 1
            else:
                # Last-Write-Wins (LWW) resolution
                if entry_obj.updated_at > existing.updated_at:
                    db.save_mangel(entry_obj)
                    updated += 1
                else:
                    skipped += 1
        elif entry_type in ("ueberfluss", "abundance"):
            entry_obj = UeberflussEntry.from_dict(raw_entry)
            existing = db.get_ueberfluss(entry_obj.id)
            if existing is None:
                db.save_ueberfluss(entry_obj)
                added += 1
            else:
                # LWW
                if entry_obj.updated_at > existing.updated_at:
                    db.save_ueberfluss(entry_obj)
                    updated += 1
                else:
                    skipped += 1
        else:
            skipped += 1

    return {
        "status": "synced",
        "received": received,
        "added": added,
        "updated": updated,
        "skipped": skipped
    }


def broadcast_entry_to_peer(peer_url: str, entry_type: str, entry_dict: Dict[str, Any]) -> bool:
    """Send a sync push payload to a peer URL."""
    clean_url = peer_url.rstrip("/")
    sync_url = f"{clean_url}/api/p2p/sync"

    payload = {
        "type": entry_type,
        "entries": [entry_dict]
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            sync_url,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Toobix-Node-P2P/2.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status in (200, 201):
                awareness_engine.evaluate_peer(clean_url)
                return True
    except Exception as e:
        logger.warning(f"Broadcast to peer {clean_url} failed: {e}")
        awareness_engine.evaluate_peer(clean_url)
    return False


def broadcast_entry_async(db: Database, entry_type: str, entry_dict: Dict[str, Any]) -> None:
    """Asynchronously broadcast an entry created locally to all active registered peers."""
    peers = db.list_peers()
    if not peers:
        return

    def _do_broadcast():
        for peer in peers:
            broadcast_entry_to_peer(peer.url, entry_type, entry_dict)

    threading.Thread(target=_do_broadcast, daemon=True).start()


def pull_sync_from_peers(db: Database) -> Dict[str, Any]:
    """Pull state from all registered peers."""
    peers = db.list_peers()
    peers_queried = 0
    total_added = 0
    total_updated = 0

    for peer in peers:
        clean_url = peer.url.rstrip("/")
        peers_queried += 1

        try:
            req = urllib.request.Request(f"{clean_url}/api/scarcity")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    res = ingest_p2p_entries(db, {"type": "mangel", "entries": data if isinstance(data, list) else []})
                    total_added += res.get("added", 0)
                    total_updated += res.get("updated", 0)
        except Exception:
            pass

        try:
            req = urllib.request.Request(f"{clean_url}/api/abundance")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    res = ingest_p2p_entries(db, {"type": "ueberfluss", "entries": data if isinstance(data, list) else []})
                    total_added += res.get("added", 0)
                    total_updated += res.get("updated", 0)
        except Exception:
            pass

        awareness_engine.evaluate_peer(clean_url)

    return {
        "status": "completed",
        "peers_queried": peers_queried,
        "new_entries": total_added,
        "updated_entries": total_updated
    }


def get_peer_awareness(db: Database) -> Dict[str, Any]:
    """Get network peer awareness, reputation scores, and praise/criticism history."""
    peers = db.list_peers()
    return awareness_engine.get_awareness_summary(peers)
