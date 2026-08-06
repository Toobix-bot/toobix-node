"""REST backend for the experimental Toobix Node 2.0 prototype."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import hmac
import json
import os
import socket
import threading
from typing import Any, Optional, Tuple

from app.models import MangelEntry, UeberflussEntry
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


DEFAULT_MAX_BODY_BYTES = 1_048_576
DEFAULT_ALLOWED_ORIGINS = "http://localhost:8080,http://127.0.0.1:8080"


def _env_int(name: str, default: int) -> int:
    try:
        return max(1, int(os.environ.get(name, str(default))))
    except ValueError:
        return default


def _is_loopback_host(host: str) -> bool:
    return host.strip().lower() in {"127.0.0.1", "localhost", "::1"}


class ToobixHTTPRequestHandler(BaseHTTPRequestHandler):
    db_path: Optional[str] = None

    def get_database(self) -> Database:
        return get_db(self.db_path)

    def _allowed_origins(self) -> set[str]:
        raw = os.environ.get("TOOBIX_ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS)
        return {item.strip() for item in raw.split(",") if item.strip()}

    def _request_origin(self) -> Optional[str]:
        value = self.headers.get("Origin")
        return value.strip() if value else None

    def _origin_allowed(self) -> bool:
        origin = self._request_origin()
        return origin is None or origin in self._allowed_origins()

    def _send_security_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")

        origin = self._request_origin()
        if origin and origin in self._allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def _send_json(self, data: Any, status: int = 200) -> None:
        try:
            response_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self._send_security_headers()
            self.end_headers()
            self.wfile.write(response_bytes)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, socket.error):
            pass

    def _authorized(self) -> bool:
        configured_token = os.environ.get("TOOBIX_API_TOKEN", "")
        if not configured_token:
            return True

        supplied = self.headers.get("X-Toobix-Token", "")
        auth_header = self.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            supplied = auth_header[7:].strip()

        return bool(supplied) and hmac.compare_digest(supplied, configured_token)

    def _require_authorization(self) -> bool:
        if self._authorized():
            return True
        self._send_json({"error": "Authentication required"}, status=401)
        return False

    def _parse_json_body(self) -> Any:
        raw_len = self.headers.get("Content-Length", "0")
        try:
            content_length = int(raw_len)
        except (ValueError, TypeError) as exc:
            raise ValueError("Invalid Content-Length header") from exc

        if content_length < 0:
            raise ValueError("Invalid Content-Length header")
        if content_length == 0:
            return {}

        max_body = _env_int("TOOBIX_MAX_BODY_BYTES", DEFAULT_MAX_BODY_BYTES)
        if content_length > max_body:
            raise ValueError(f"Request body exceeds the {max_body}-byte limit")

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            raise ValueError("Content-Type must be application/json")

        body_bytes = self.rfile.read(content_length)
        if not body_bytes:
            return {}

        try:
            return json.loads(body_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON body payload") from exc

    def _handle_exception(self, error: Exception) -> None:
        if os.environ.get("DEBUG") == "1":
            self._send_json({"error": f"Internal server error: {error}"}, status=500)
        else:
            self._send_json({"error": "Internal server error"}, status=500)

    def do_OPTIONS(self) -> None:
        if not self._origin_allowed():
            self._send_json({"error": "Origin not allowed"}, status=403)
            return

        self.send_response(204)
        self._send_security_headers()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, X-Toobix-Token",
        )
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self) -> None:
        try:
            self._handle_get()
        except ValueError as error:
            self._send_json({"error": str(error)}, status=400)
        except Exception as error:
            self._handle_exception(error)

    def _handle_get(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/") or "/"
        query_params = parse_qs(parsed_url.query)

        if path in ("/api/health", "/health"):
            self._send_json({"status": "ok", "node_id": "Toobix-Node-2.0"})
            return

        if not self._require_authorization():
            return

        db = self.get_database()

        if path in ("/api/scarcity", "/scarcity"):
            category = query_params.get("category", [None])[0]
            status = query_params.get("status", [None])[0]
            entries = db.list_mangel(category=category, status=status)
            self._send_json([entry.to_dict() for entry in entries])
            return

        if path.startswith("/api/scarcity/") or path.startswith("/scarcity/"):
            entry = db.get_mangel(path.split("/")[-1])
            self._send_json(entry.to_dict() if entry else {"error": "Scarcity entry not found"}, 200 if entry else 404)
            return

        if path in ("/api/abundance", "/abundance"):
            category = query_params.get("category", [None])[0]
            status = query_params.get("status", [None])[0]
            entries = db.list_ueberfluss(category=category, status=status)
            self._send_json([entry.to_dict() for entry in entries])
            return

        if path.startswith("/api/abundance/") or path.startswith("/abundance/"):
            entry = db.get_ueberfluss(path.split("/")[-1])
            self._send_json(entry.to_dict() if entry else {"error": "Abundance entry not found"}, 200 if entry else 404)
            return

        if path in ("/api/matches", "/matches"):
            scarcity_id = query_params.get("scarcity_id", [None])[0]
            abundance_id = query_params.get("abundance_id", [None])[0]
            matches = db.list_matches(scarcity_id=scarcity_id, abundance_id=abundance_id)
            self._send_json([match.to_dict() for match in matches])
            return

        if path in ("/api/reflection", "/reflection"):
            self._send_json(generate_node_reflection(db).to_dict())
            return

        if path in ("/api/peers", "/peers"):
            self._send_json(list_peers(db))
            return

        if path in (
            "/api/peers/awareness",
            "/peers/awareness",
            "/api/p2p/awareness",
            "/p2p/awareness",
        ):
            self._send_json(get_peer_awareness(db))
            return

        if path in ("/api/p2p/sync/pull", "/p2p/sync/pull"):
            self._send_json(pull_sync_from_peers(db))
            return

        self._send_json({"error": f"Endpoint GET {path} not found"}, status=404)

    def do_POST(self) -> None:
        if not self._require_authorization():
            return
        try:
            self._handle_post()
        except ValueError as error:
            self._send_json({"error": str(error)}, status=400)
        except Exception as error:
            self._handle_exception(error)

    def _handle_post(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/") or "/"
        query_params = parse_qs(parsed_url.query)
        db = self.get_database()
        body = self._parse_json_body()

        if path in ("/api/scarcity", "/scarcity"):
            if not isinstance(body, dict) or not body:
                raise ValueError("Request body must be a non-empty JSON object")
            saved = db.save_mangel(MangelEntry.from_dict(body))
            broadcast_entry_async(db, "mangel", saved.to_dict())
            self._send_json(saved.to_dict(), status=201)
            return

        if path in ("/api/abundance", "/abundance"):
            if not isinstance(body, dict) or not body:
                raise ValueError("Request body must be a non-empty JSON object")
            saved = db.save_ueberfluss(UeberflussEntry.from_dict(body))
            broadcast_entry_async(db, "ueberfluss", saved.to_dict())
            self._send_json(saved.to_dict(), status=201)
            return

        if path in ("/api/matches", "/matches"):
            if not isinstance(body, dict):
                raise ValueError("Request body must be a JSON object")
            scarcity_id = body.get("scarcity_id") or query_params.get("scarcity_id", [None])[0]
            min_score_value = body.get("min_score") or query_params.get("min_score", [0.30])[0]
            try:
                min_score = min(max(float(min_score_value), 0.0), 1.0)
            except (ValueError, TypeError):
                min_score = 0.30

            scarcities = db.list_mangel()
            if scarcity_id:
                scarcities = [item for item in scarcities if item.id == scarcity_id]
            matches = find_matches(scarcities, db.list_ueberfluss(), min_score=min_score)
            self._send_json([item.to_dict() for item in db.save_matches(matches)])
            return

        if path in ("/api/reflection", "/reflection"):
            self._send_json(generate_node_reflection(db).to_dict(), status=201)
            return

        if path in ("/api/peers/register", "/peers/register"):
            if not isinstance(body, dict):
                raise ValueError("Request body must be a JSON object")
            peer_url = body.get("peer_url") or body.get("url")
            if not peer_url:
                raise ValueError("peer_url is required")
            self._send_json(register_peer(db, peer_url), status=201)
            return

        if path in ("/api/peers/unregister", "/peers/unregister"):
            if not isinstance(body, dict):
                raise ValueError("Request body must be a JSON object")
            peer_url = body.get("peer_url") or body.get("url")
            if not peer_url:
                raise ValueError("peer_url is required")
            self._send_json(unregister_peer(db, peer_url))
            return

        if path in ("/api/p2p/sync", "/p2p/sync"):
            self._send_json(ingest_p2p_entries(db, body))
            return

        if path in ("/api/p2p/sync/pull", "/p2p/sync/pull"):
            self._send_json(pull_sync_from_peers(db))
            return

        self._send_json({"error": f"Endpoint POST {path} not found"}, status=404)

    def do_DELETE(self) -> None:
        if not self._require_authorization():
            return
        try:
            self._handle_delete()
        except ValueError as error:
            self._send_json({"error": str(error)}, status=400)
        except Exception as error:
            self._handle_exception(error)

    def _handle_delete(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/") or "/"
        query_params = parse_qs(parsed_url.query)
        db = self.get_database()

        body: Any = {}
        raw_length = self.headers.get("Content-Length", "0")
        if raw_length not in ("", "0"):
            body = self._parse_json_body()

        if path in ("/api/peers/unregister", "/peers/unregister", "/api/peers", "/peers"):
            if not isinstance(body, dict):
                body = {}
            peer_url = body.get("peer_url") or body.get("url") or query_params.get("peer_url", [None])[0]
            if not peer_url:
                raise ValueError("peer_url is required")
            self._send_json(unregister_peer(db, peer_url))
            return

        self._send_json({"error": f"Endpoint DELETE {path} not found"}, status=404)

    def log_message(self, format_string: str, *args: Any) -> None:
        if os.environ.get("DEBUG") == "1":
            super().log_message(format_string, *args)


def create_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    db_path: Optional[str] = None,
) -> ThreadingHTTPServer:
    if (
        not _is_loopback_host(host)
        and not os.environ.get("TOOBIX_API_TOKEN")
        and os.environ.get("TOOBIX_ALLOW_INSECURE_REMOTE") != "1"
    ):
        raise RuntimeError(
            "A non-loopback bind requires TOOBIX_API_TOKEN. "
            "Set TOOBIX_ALLOW_INSECURE_REMOTE=1 only for isolated test networks."
        )

    class ConfiguredHandler(ToobixHTTPRequestHandler):
        pass

    ConfiguredHandler.db_path = db_path or os.environ.get("DB_PATH", "toobix_node.db")

    class CustomThreadingHTTPServer(ThreadingHTTPServer):
        allow_reuse_address = True
        daemon_threads = True
        request_queue_size = 128

        def server_bind(self) -> None:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            super().server_bind()

    return CustomThreadingHTTPServer((host, port), ConfiguredHandler)


def run_server_in_thread(
    host: str = "127.0.0.1",
    port: int = 8000,
    db_path: Optional[str] = None,
) -> Tuple[ThreadingHTTPServer, threading.Thread]:
    server = create_server(host=host, port=port, db_path=db_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    db_path = os.environ.get("DB_PATH", "toobix_node.db")
    server = create_server(host=host, port=port, db_path=db_path)
    print(f"Starting Toobix Node 2.0 Backend on http://{host}:{port} (DB: {db_path})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
        server.shutdown()
