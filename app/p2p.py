"""P2P synchronization helpers for the experimental Toobix Node prototype."""

import ipaddress
import json
import logging
import os
import socket
import threading
import time
import urllib.error
import urllib.request
import uuid
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from app.db import Database
from app.models import MangelEntry, Peer, UeberflussEntry

logger = logging.getLogger(__name__)
DEFAULT_MAX_PEER_RESPONSE_BYTES = 2_097_152


def _env_int(name: str, default: int) -> int:
    try:
        return max(1, int(os.environ.get(name, str(default))))
    except ValueError:
        return default


def _request_headers(include_json: bool = False) -> Dict[str, str]:
    headers = {"User-Agent": "Toobix-Node-P2P/2.0"}
    if include_json:
        headers["Content-Type"] = "application/json"
    token = os.environ.get("TOOBIX_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _resolved_addresses(hostname: str) -> List[ipaddress._BaseAddress]:
    addresses: List[ipaddress._BaseAddress] = []
    try:
        for result in socket.getaddrinfo(hostname, None):
            raw = result[4][0]
            try:
                address = ipaddress.ip_address(raw)
            except ValueError:
                continue
            if address not in addresses:
                addresses.append(address)
    except socket.gaierror as exc:
        raise ValueError(f"Peer hostname cannot be resolved: {hostname}") from exc
    return addresses


def normalize_peer_url(peer_url: str) -> str:
    """Validate and normalize a peer base URL before any outbound request."""
    if not isinstance(peer_url, str) or not peer_url.strip():
        raise ValueError("peer_url string is required")

    clean_url = peer_url.strip().rstrip("/")
    parsed = urlparse(clean_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("peer_url must use http or https")
    if not parsed.hostname:
        raise ValueError("peer_url must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("peer_url must not contain embedded credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("peer_url must not contain a query or fragment")
    if parsed.path not in ("", "/"):
        raise ValueError("peer_url must be a base URL without a path")

    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError("peer_url contains an invalid port") from exc

    allow_private = os.environ.get("TOOBIX_ALLOW_PRIVATE_PEERS", "1") == "1"
    if not allow_private:
        for address in _resolved_addresses(parsed.hostname):
            if (
                address.is_private
                or address.is_loopback
                or address.is_link_local
                or address.is_reserved
                or address.is_unspecified
                or address.is_multicast
            ):
                raise ValueError(
                    "Private, loopback, link-local and reserved peer addresses are disabled"
                )

    return clean_url


def _read_json_response(response: Any) -> Any:
    max_bytes = _env_int(
        "TOOBIX_MAX_PEER_RESPONSE_BYTES", DEFAULT_MAX_PEER_RESPONSE_BYTES
    )
    raw = response.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError("Peer response exceeds configured size limit")
    return json.loads(raw.decode("utf-8"))


def _get_json(url: str, timeout: float = 3.0) -> Any:
    request = urllib.request.Request(url, headers=_request_headers())
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError(f"Peer returned HTTP {response.status}")
        return _read_json_response(response)


def _post_json(url: str, payload: Dict[str, Any], timeout: float = 3.0) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=_request_headers(include_json=True),
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status not in (200, 201):
            raise ValueError(f"Peer returned HTTP {response.status}")
        return _read_json_response(response)


class PeerAwarenessEngine:
    """Technical peer-health metrics; this does not evaluate people."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.peer_metrics: Dict[str, Dict[str, Any]] = {}
        self.history: List[Dict[str, Any]] = []

    def evaluate_peer(self, peer_url: str) -> Dict[str, Any]:
        clean_url = normalize_peer_url(peer_url)
        start_time = time.time()
        success = False
        error_message: Optional[str] = None

        try:
            payload = _get_json(f"{clean_url}/api/health", timeout=2.5)
            success = isinstance(payload, dict) and (
                payload.get("status") == "ok" or "node_id" in payload
            )
            if not success:
                error_message = "Malformed health response"
        except Exception as exc:
            error_message = str(exc)

        response_time_ms = (time.time() - start_time) * 1000.0
        now = time.time()

        with self._lock:
            metrics = self.peer_metrics.setdefault(
                clean_url,
                {
                    "url": clean_url,
                    "reputation_score": 0,
                    "status": "neutral",
                    "praise_count": 0,
                    "criticism_count": 0,
                    "last_seen": now,
                    "last_response_time_ms": 0.0,
                    "health": "unknown",
                },
            )
            metrics["last_seen"] = now
            metrics["last_response_time_ms"] = round(response_time_ms, 2)

            if success and response_time_ms < 2000.0:
                metrics["reputation_score"] += 1
                metrics["status"] = "healthy"
                metrics["praise_count"] += 1
                metrics["health"] = "healthy"
                event_type = "healthy"
                reason = f"Valid health response in {response_time_ms:.1f}ms"
            else:
                metrics["reputation_score"] -= 1
                metrics["status"] = "degraded"
                metrics["criticism_count"] += 1
                metrics["health"] = "unresponsive" if not success else "slow"
                event_type = "warning"
                reason = error_message or f"Slow response in {response_time_ms:.1f}ms"

            self.history.append(
                {
                    "timestamp": now,
                    "peer_url": clean_url,
                    "type": event_type,
                    "token": f"PEER-{uuid.uuid4().hex[:8].upper()}",
                    "reason": reason,
                    "response_time_ms": round(response_time_ms, 2),
                    "reputation_after": metrics["reputation_score"],
                }
            )
            self.history = self.history[-200:]
            return dict(metrics)

    def get_awareness_summary(self, peers: List[Peer]) -> Dict[str, Any]:
        for peer in peers:
            try:
                self.evaluate_peer(peer.url)
            except ValueError as exc:
                logger.warning("Skipped invalid peer URL: %s", exc)

        with self._lock:
            scores = {
                url: metrics["reputation_score"]
                for url, metrics in self.peer_metrics.items()
            }
            healthy = sum(
                1 for metrics in self.peer_metrics.values() if metrics["health"] == "healthy"
            )
            degraded = sum(
                1 for metrics in self.peer_metrics.values() if metrics["health"] != "healthy"
            )
            overall = "healthy" if healthy and degraded == 0 else "degraded" if peers else "idle"
            return {
                "peers": {url: dict(value) for url, value in self.peer_metrics.items()},
                "reputation_scores": scores,
                "reputation": scores,
                "history": list(self.history),
                "praise_criticism_history": list(self.history),
                "network_awareness_summary": {
                    "total_peers": len(peers),
                    "healthy_peers": healthy,
                    "degraded_peers": degraded,
                    "overall_status": overall,
                },
            }


awareness_engine = PeerAwarenessEngine()


def register_peer(db: Database, peer_url: str) -> Dict[str, Any]:
    clean_url = normalize_peer_url(peer_url)
    peer = Peer(url=clean_url, last_seen=time.time(), is_active=True)
    db.save_peer(peer)
    threading.Thread(
        target=awareness_engine.evaluate_peer,
        args=(clean_url,),
        daemon=True,
    ).start()
    active_peers = db.list_peers()
    return {
        "status": "registered",
        "peer_url": clean_url,
        "total_peers": len(active_peers),
        "peers": [item.url for item in active_peers],
    }


def unregister_peer(db: Database, peer_url: str) -> Dict[str, Any]:
    clean_url = normalize_peer_url(peer_url)
    for peer in db.list_peers():
        if peer.url.rstrip("/") == clean_url:
            peer.is_active = False
            db.save_peer(peer)
            break
    return {
        "status": "unregistered",
        "peer_url": clean_url,
        "total_peers": len(db.list_peers()),
    }


def list_peers(db: Database) -> Dict[str, Any]:
    peers = db.list_peers()
    return {
        "peers": [peer.url for peer in peers],
        "peer_details": [peer.to_dict() for peer in peers],
    }


def ingest_p2p_entries(db: Database, payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        if isinstance(payload, list):
            payload = {"entries": payload}
        else:
            raise ValueError("Payload must be a JSON object or list")

    entries: List[Dict[str, Any]] = []
    if isinstance(payload.get("entries"), list):
        entries.extend(payload["entries"])
    elif isinstance(payload.get("entry"), dict):
        entries.append(payload["entry"])
    else:
        for key, forced_type in (
            ("mangel", "mangel"),
            ("scarcity", "mangel"),
            ("ueberfluss", "ueberfluss"),
            ("abundance", "ueberfluss"),
        ):
            value = payload.get(key)
            values = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
            for item in values:
                copy = dict(item)
                copy["_forced_type"] = forced_type
                entries.append(copy)
        if not entries and "title" in payload and "category" in payload:
            entries.append(payload)

    if len(entries) > _env_int("TOOBIX_MAX_SYNC_ENTRIES", 500):
        raise ValueError("Sync payload contains too many entries")

    forced_type = payload.get("type")
    added = updated = skipped = 0

    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            skipped += 1
            continue

        entry_type = str(
            raw_entry.get("_forced_type")
            or forced_type
            or raw_entry.get("type")
            or ("ueberfluss" if "quantity" in raw_entry else "mangel")
        ).lower()

        if entry_type in ("mangel", "scarcity"):
            entry = MangelEntry.from_dict(raw_entry)
            existing = db.get_mangel(entry.id)
            if existing is None:
                db.save_mangel(entry)
                added += 1
            elif entry.updated_at > existing.updated_at:
                db.save_mangel(entry)
                updated += 1
            else:
                skipped += 1
        elif entry_type in ("ueberfluss", "abundance"):
            entry = UeberflussEntry.from_dict(raw_entry)
            existing = db.get_ueberfluss(entry.id)
            if existing is None:
                db.save_ueberfluss(entry)
                added += 1
            elif entry.updated_at > existing.updated_at:
                db.save_ueberfluss(entry)
                updated += 1
            else:
                skipped += 1
        else:
            skipped += 1

    return {
        "status": "synced",
        "received": len(entries),
        "added": added,
        "updated": updated,
        "skipped": skipped,
    }


def broadcast_entry_to_peer(
    peer_url: str,
    entry_type: str,
    entry_dict: Dict[str, Any],
) -> bool:
    clean_url = normalize_peer_url(peer_url)
    try:
        _post_json(
            f"{clean_url}/api/p2p/sync",
            {"type": entry_type, "entries": [entry_dict]},
        )
        awareness_engine.evaluate_peer(clean_url)
        return True
    except Exception as exc:
        logger.warning("Broadcast to peer %s failed: %s", clean_url, exc)
        try:
            awareness_engine.evaluate_peer(clean_url)
        except Exception:
            pass
        return False


def broadcast_entry_async(
    db: Database,
    entry_type: str,
    entry_dict: Dict[str, Any],
) -> None:
    peers = db.list_peers()
    if not peers:
        return

    def _broadcast() -> None:
        for peer in peers:
            broadcast_entry_to_peer(peer.url, entry_type, entry_dict)

    threading.Thread(target=_broadcast, daemon=True).start()


def pull_sync_from_peers(db: Database) -> Dict[str, Any]:
    peers = db.list_peers()
    total_added = total_updated = 0

    for peer in peers:
        clean_url = normalize_peer_url(peer.url)
        for endpoint, entry_type in (
            ("scarcity", "mangel"),
            ("abundance", "ueberfluss"),
        ):
            try:
                payload = _get_json(f"{clean_url}/api/{endpoint}")
                result = ingest_p2p_entries(
                    db,
                    {
                        "type": entry_type,
                        "entries": payload if isinstance(payload, list) else [],
                    },
                )
                total_added += result.get("added", 0)
                total_updated += result.get("updated", 0)
            except Exception as exc:
                logger.warning("Pull from peer %s failed: %s", clean_url, exc)
        try:
            awareness_engine.evaluate_peer(clean_url)
        except Exception:
            pass

    return {
        "status": "completed",
        "peers_queried": len(peers),
        "new_entries": total_added,
        "updated_entries": total_updated,
    }


def get_peer_awareness(db: Database) -> Dict[str, Any]:
    return awareness_engine.get_awareness_summary(db.list_peers())
