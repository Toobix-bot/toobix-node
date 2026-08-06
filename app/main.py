"""
REST HTTP backend server for Toobix Node 2.0.
Built using Python standard library http.server for 100% dependency-free operation.
Supports PORT, HOST, and DB_PATH environment variables.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os
import socket
import sys
import threading
from typing import Dict, Any, Optional, List, Tuple

from app.models import MangelEntry, UeberflussEntry, MatchResult, NodeReflection
from app.db import get_db, Database
from app.matching import find_matches
from app.reflection import generate_node_reflection
from app.p2p import (
    register_peer,
    unregister_peer,
    list_peers,
    ingest_p2p_entries,
    broadcast_entry_async,
    pull_sync_from_peers,
    get_peer_awareness,
)


class ToobixHTTPRequestHandler(BaseHTTPRequestHandler):
    db_path: Optional[str] = None

    def get_database(self) -> Database:
        return get_db(self.db_path)

    def _send_json(self, data: Any, status: int = 200) -> None:
        try:
            response_bytes = json.dumps(data, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(response_bytes)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, socket.error):
            pass

    def _parse_json_body(self) -> Any:
        raw_len = self.headers.get("Content-Length", 0)
        try:
            content_length = int(raw_len)
        except (ValueError, TypeError):
            raise ValueError("Invalid Content-Length header")

        if content_length <= 0:
            return {}

        body_bytes = self.rfile.read(content_length)
        if not body_bytes:
            return {}

        try:
            return json.loads(body_bytes.decode("utf-8"))
        except Exception:
            raise ValueError("Invalid JSON body payload")

    def do_OPTIONS(self) -> None:
        try:
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        except Exception as e:
            self._send_json({"error": str(e)}, status=500)

    def do_GET(self) -> None:
        try:
            self._handle_get()
        except ValueError as e:
            self._send_json({"error": str(e)}, status=400)
        except Exception as e:
            self._send_json({"error": f"Internal server error: {e}"}, status=500)

    def _handle_get(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")
        query_params = parse_qs(parsed_url.query)
        db = self.get_database()

        # Health endpoint
        if path == "/api/health" or path == "/health":
            self._send_json({"status": "ok", "node_id": "Toobix-Node-2.0"})
            return

        # Scarcity GET list or GET detail
        if path == "/api/scarcity" or path == "/scarcity":
            category = query_params.get("category", [None])[0]
            status = query_params.get("status", [None])[0]
            entries = db.list_mangel(category=category, status=status)
            self._send_json([e.to_dict() for e in entries])
            return

        if path.startswith("/api/scarcity/") or path.startswith("/scarcity/"):
            entry_id = path.split("/")[-1]
            entry = db.get_mangel(entry_id)
            if entry:
                self._send_json(entry.to_dict())
            else:
                self._send_json({"error": "Scarcity entry not found"}, status=404)
            return

        # Abundance GET list or GET detail
        if path == "/api/abundance" or path == "/abundance":
            category = query_params.get("category", [None])[0]
            status = query_params.get("status", [None])[0]
            entries = db.list_ueberfluss(category=category, status=status)
            self._send_json([e.to_dict() for e in entries])
            return

        if path.startswith("/api/abundance/") or path.startswith("/abundance/"):
            entry_id = path.split("/")[-1]
            entry = db.get_ueberfluss(entry_id)
            if entry:
                self._send_json(entry.to_dict())
            else:
                self._send_json({"error": "Abundance entry not found"}, status=404)
            return

        # Matches GET list
        if path == "/api/matches" or path == "/matches":
            scarcity_id = query_params.get("scarcity_id", [None])[0]
            abundance_id = query_params.get("abundance_id", [None])[0]
            matches = db.list_matches(scarcity_id=scarcity_id, abundance_id=abundance_id)
            self._send_json([m.to_dict() for m in matches])
            return

        # Reflection GET endpoint
        if path == "/api/reflection" or path == "/reflection":
            reflection = generate_node_reflection(db)
            self._send_json(reflection.to_dict())
            return

        # Peers GET list
        if path in ("/api/peers", "/peers"):
            self._send_json(list_peers(db))
            return

        # Peer Awareness GET
        if path in ("/api/peers/awareness", "/peers/awareness", "/api/p2p/awareness", "/p2p/awareness"):
            self._send_json(get_peer_awareness(db))
            return

        # P2P Pull Sync GET
        if path in ("/api/p2p/sync/pull", "/p2p/sync/pull"):
            self._send_json(pull_sync_from_peers(db))
            return

        self._send_json({"error": f"Endpoint GET {path} not found"}, status=404)

    def do_POST(self) -> None:
        try:
            self._handle_post()
        except ValueError as e:
            self._send_json({"error": str(e)}, status=400)
        except Exception as e:
            self._send_json({"error": f"Internal server error: {e}"}, status=500)

    def _handle_post(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")
        query_params = parse_qs(parsed_url.query)
        db = self.get_database()
        body = self._parse_json_body()

        # Scarcity POST create
        if path == "/api/scarcity" or path == "/scarcity":
            if not isinstance(body, dict):
                self._send_json({"error": "Request body must be a JSON object"}, status=400)
                return
            if not body:
                self._send_json({"error": "Request body must be non-empty JSON"}, status=400)
                return
            entry = MangelEntry.from_dict(body)
            saved = db.save_mangel(entry)
            broadcast_entry_async(db, "mangel", saved.to_dict())
            self._send_json(saved.to_dict(), status=201)
            return

        # Abundance POST create
        if path == "/api/abundance" or path == "/abundance":
            if not isinstance(body, dict):
                self._send_json({"error": "Request body must be a JSON object"}, status=400)
                return
            if not body:
                self._send_json({"error": "Request body must be non-empty JSON"}, status=400)
                return
            entry = UeberflussEntry.from_dict(body)
            saved = db.save_ueberfluss(entry)
            broadcast_entry_async(db, "ueberfluss", saved.to_dict())
            self._send_json(saved.to_dict(), status=201)
            return

        # Matches POST calculate
        if path == "/api/matches" or path == "/matches":
            if not isinstance(body, dict):
                self._send_json({"error": "Request body must be a JSON object"}, status=400)
                return
            scarcity_id = body.get("scarcity_id") or query_params.get("scarcity_id", [None])[0]
            min_score_val = body.get("min_score") or query_params.get("min_score", [0.30])[0]
            try:
                min_score = float(min_score_val)
            except (ValueError, TypeError):
                min_score = 0.30

            scarcities = db.list_mangel()
            if scarcity_id:
                scarcities = [s for s in scarcities if s.id == scarcity_id]

            abundances = db.list_ueberfluss()
            matches = find_matches(scarcities, abundances, min_score=min_score)

            saved_matches = db.save_matches(matches)

            self._send_json([m.to_dict() for m in saved_matches])
            return

        # Reflection POST endpoint
        if path == "/api/reflection" or path == "/reflection":
            reflection = generate_node_reflection(db)
            self._send_json(reflection.to_dict(), status=201)
            return

        # Peer Registration POST
        if path in ("/api/peers/register", "/peers/register"):
            if not isinstance(body, dict):
                self._send_json({"error": "Request body must be a JSON object"}, status=400)
                return
            peer_url = body.get("peer_url") or body.get("url")
            if not peer_url:
                self._send_json({"error": "peer_url is required"}, status=400)
                return
            res = register_peer(db, peer_url)
            self._send_json(res, status=201)
            return

        # Peer Unregister POST
        if path in ("/api/peers/unregister", "/peers/unregister"):
            if not isinstance(body, dict):
                self._send_json({"error": "Request body must be a JSON object"}, status=400)
                return
            peer_url = body.get("peer_url") or body.get("url")
            if not peer_url:
                self._send_json({"error": "peer_url is required"}, status=400)
                return
            res = unregister_peer(db, peer_url)
            self._send_json(res, status=200)
            return

        # P2P Ingest Sync POST
        if path in ("/api/p2p/sync", "/p2p/sync"):
            res = ingest_p2p_entries(db, body)
            self._send_json(res, status=200)
            return

        # P2P Pull Sync POST
        if path in ("/api/p2p/sync/pull", "/p2p/sync/pull"):
            res = pull_sync_from_peers(db)
            self._send_json(res, status=200)
            return

        self._send_json({"error": f"Endpoint POST {path} not found"}, status=404)

    def do_DELETE(self) -> None:
        try:
            self._handle_delete()
        except ValueError as e:
            self._send_json({"error": str(e)}, status=400)
        except Exception as e:
            self._send_json({"error": f"Internal server error: {e}"}, status=500)

    def _handle_delete(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")
        query_params = parse_qs(parsed_url.query)
        db = self.get_database()
        body = {}
        try:
            body = self._parse_json_body()
        except Exception:
            pass

        if path in ("/api/peers/unregister", "/peers/unregister", "/api/peers", "/peers"):
            peer_url = body.get("peer_url") or body.get("url") or query_params.get("peer_url", [None])[0]
            if not peer_url:
                self._send_json({"error": "peer_url is required"}, status=400)
                return
            res = unregister_peer(db, peer_url)
            self._send_json(res, status=200)
            return

        self._send_json({"error": f"Endpoint DELETE {path} not found"}, status=404)

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default stdout logging for clean test execution unless DEBUG is set."""
        if os.environ.get("DEBUG"):
            super().log_message(format, *args)


def create_server(
    host: str = "0.0.0.0", port: int = 8000, db_path: Optional[str] = None
) -> ThreadingHTTPServer:
    class ConfiguredHandler(ToobixHTTPRequestHandler):
        pass

    ConfiguredHandler.db_path = db_path or os.environ.get("DB_PATH", "toobix_node.db")

    class CustomThreadingHTTPServer(ThreadingHTTPServer):
        allow_reuse_address = True
        daemon_threads = True
        request_queue_size = 128

        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            super().server_bind()

    server = CustomThreadingHTTPServer((host, port), ConfiguredHandler)
    return server


def run_server_in_thread(
    host: str = "127.0.0.1", port: int = 8000, db_path: Optional[str] = None
) -> Tuple[ThreadingHTTPServer, threading.Thread]:
    server = create_server(host=host, port=port, db_path=db_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    db_path = os.environ.get("DB_PATH", "toobix_node.db")
    server = create_server(host=host, port=port, db_path=db_path)
    print(f"Starting Toobix Node 2.0 Backend on http://{host}:{port} (DB: {db_path})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
        server.shutdown()

