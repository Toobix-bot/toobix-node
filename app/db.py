"""
SQLite database storage layer for Toobix Node 2.0.
Supports configurable DB path via DB_PATH environment variable.
"""

import sqlite3
import json
import os
import threading
from typing import List, Optional, Dict, Any
from app.models import MangelEntry, UeberflussEntry, MatchResult, HelpOffer, Peer, NodeReflection

DEFAULT_DB_PATH = "toobix_node.db"


def get_db_path(db_path: Optional[str] = None) -> str:
    if db_path:
        return db_path
    return os.environ.get("DB_PATH", DEFAULT_DB_PATH)


class Database:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = get_db_path(db_path)
        self._write_lock = threading.Lock()
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA busy_timeout=10000;")
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS mangel (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    urgency TEXT DEFAULT 'medium',
                    location TEXT DEFAULT '',
                    contact TEXT DEFAULT '',
                    status TEXT DEFAULT 'open',
                    tags_json TEXT DEFAULT '[]',
                    created_at REAL,
                    updated_at REAL
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ueberfluss (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    quantity TEXT DEFAULT '1',
                    location TEXT DEFAULT '',
                    contact TEXT DEFAULT '',
                    status TEXT DEFAULT 'active',
                    tags_json TEXT DEFAULT '[]',
                    created_at REAL,
                    updated_at REAL
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id TEXT PRIMARY KEY,
                    scarcity_id TEXT NOT NULL,
                    abundance_id TEXT NOT NULL,
                    score REAL NOT NULL,
                    category_match INTEGER NOT NULL,
                    keyword_score REAL NOT NULL,
                    location_score REAL NOT NULL,
                    match_reason TEXT DEFAULT '',
                    status TEXT DEFAULT 'proposed',
                    created_at REAL
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS help_offers (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    services_json TEXT DEFAULT '[]',
                    contact TEXT DEFAULT '',
                    location TEXT DEFAULT '',
                    is_emergency INTEGER DEFAULT 0,
                    source_url TEXT DEFAULT '',
                    created_at REAL
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS peers (
                    id TEXT PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    name TEXT DEFAULT '',
                    last_seen REAL,
                    is_active INTEGER DEFAULT 1
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS reflections (
                    id TEXT PRIMARY KEY,
                    node_id TEXT NOT NULL,
                    mangel_json TEXT DEFAULT '[]',
                    ueberfluss_json TEXT DEFAULT '[]',
                    harmony_score REAL NOT NULL,
                    status_summary TEXT DEFAULT '',
                    created_at REAL
                )
                """)
                conn.commit()

    # Mangel Operations
    def save_mangel(self, entry: MangelEntry) -> MangelEntry:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO mangel (id, title, category, description, urgency, location, contact, status, tags_json, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title=excluded.title,
                        category=excluded.category,
                        description=excluded.description,
                        urgency=excluded.urgency,
                        location=excluded.location,
                        contact=excluded.contact,
                        status=excluded.status,
                        tags_json=excluded.tags_json,
                        created_at=excluded.created_at,
                        updated_at=excluded.updated_at
                    """,
                    (
                        entry.id,
                        entry.title,
                        entry.category,
                        entry.description,
                        entry.urgency,
                        entry.location,
                        entry.contact,
                        entry.status,
                        json.dumps(entry.tags),
                        entry.created_at,
                        entry.updated_at,
                    ),
                )
                conn.commit()
            return entry

    def get_mangel(self, entry_id: str) -> Optional[MangelEntry]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mangel WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return MangelEntry.from_dict({
                "id": row["id"],
                "title": row["title"],
                "category": row["category"],
                "description": row["description"],
                "urgency": row["urgency"],
                "location": row["location"],
                "contact": row["contact"],
                "status": row["status"],
                "tags": json.loads(row["tags_json"] or "[]"),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            })

    def list_mangel(
        self, category: Optional[str] = None, status: Optional[str] = None
    ) -> List[MangelEntry]:
        query = "SELECT * FROM mangel WHERE 1=1"
        params: List[Any] = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                MangelEntry.from_dict({
                    "id": row["id"],
                    "title": row["title"],
                    "category": row["category"],
                    "description": row["description"],
                    "urgency": row["urgency"],
                    "location": row["location"],
                    "contact": row["contact"],
                    "status": row["status"],
                    "tags": json.loads(row["tags_json"] or "[]"),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                })
                for row in rows
            ]

    # Ueberfluss Operations
    def save_ueberfluss(self, entry: UeberflussEntry) -> UeberflussEntry:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO ueberfluss (id, title, category, description, quantity, location, contact, status, tags_json, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title=excluded.title,
                        category=excluded.category,
                        description=excluded.description,
                        quantity=excluded.quantity,
                        location=excluded.location,
                        contact=excluded.contact,
                        status=excluded.status,
                        tags_json=excluded.tags_json,
                        created_at=excluded.created_at,
                        updated_at=excluded.updated_at
                    """,
                    (
                        entry.id,
                        entry.title,
                        entry.category,
                        entry.description,
                        entry.quantity,
                        entry.location,
                        entry.contact,
                        entry.status,
                        json.dumps(entry.tags),
                        entry.created_at,
                        entry.updated_at,
                    ),
                )
                conn.commit()
            return entry

    def get_ueberfluss(self, entry_id: str) -> Optional[UeberflussEntry]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ueberfluss WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return UeberflussEntry.from_dict({
                "id": row["id"],
                "title": row["title"],
                "category": row["category"],
                "description": row["description"],
                "quantity": row["quantity"],
                "location": row["location"],
                "contact": row["contact"],
                "status": row["status"],
                "tags": json.loads(row["tags_json"] or "[]"),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            })

    def list_ueberfluss(
        self, category: Optional[str] = None, status: Optional[str] = None
    ) -> List[UeberflussEntry]:
        query = "SELECT * FROM ueberfluss WHERE 1=1"
        params: List[Any] = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                UeberflussEntry.from_dict({
                    "id": row["id"],
                    "title": row["title"],
                    "category": row["category"],
                    "description": row["description"],
                    "quantity": row["quantity"],
                    "location": row["location"],
                    "contact": row["contact"],
                    "status": row["status"],
                    "tags": json.loads(row["tags_json"] or "[]"),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                })
                for row in rows
            ]

    # Match Operations
    def save_match(self, match: MatchResult) -> MatchResult:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO matches (id, scarcity_id, abundance_id, score, category_match, keyword_score, location_score, match_reason, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        scarcity_id=excluded.scarcity_id,
                        abundance_id=excluded.abundance_id,
                        score=excluded.score,
                        category_match=excluded.category_match,
                        keyword_score=excluded.keyword_score,
                        location_score=excluded.location_score,
                        match_reason=excluded.match_reason,
                        status=excluded.status,
                        created_at=excluded.created_at
                    """,
                    (
                        match.id,
                        match.scarcity_id,
                        match.abundance_id,
                        match.score,
                        1 if match.category_match else 0,
                        match.keyword_score,
                        match.location_score,
                        match.match_reason,
                        match.status,
                        match.created_at,
                    ),
                )
                conn.commit()
            return match

    def save_matches(self, matches: List[MatchResult]) -> List[MatchResult]:
        if not matches:
            return []
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(
                    """
                    INSERT INTO matches (id, scarcity_id, abundance_id, score, category_match, keyword_score, location_score, match_reason, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        scarcity_id=excluded.scarcity_id,
                        abundance_id=excluded.abundance_id,
                        score=excluded.score,
                        category_match=excluded.category_match,
                        keyword_score=excluded.keyword_score,
                        location_score=excluded.location_score,
                        match_reason=excluded.match_reason,
                        status=excluded.status,
                        created_at=excluded.created_at
                    """,
                    [
                        (
                            m.id,
                            m.scarcity_id,
                            m.abundance_id,
                            m.score,
                            1 if m.category_match else 0,
                            m.keyword_score,
                            m.location_score,
                            m.match_reason,
                            m.status,
                            m.created_at,
                        )
                        for m in matches
                    ],
                )
                conn.commit()
        return matches

    def list_matches(
        self, scarcity_id: Optional[str] = None, abundance_id: Optional[str] = None
    ) -> List[MatchResult]:
        query = "SELECT * FROM matches WHERE 1=1"
        params: List[Any] = []
        if scarcity_id:
            query += " AND scarcity_id = ?"
            params.append(scarcity_id)
        if abundance_id:
            query += " AND abundance_id = ?"
            params.append(abundance_id)
        query += " ORDER BY score DESC"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                MatchResult.from_dict({
                    "id": row["id"],
                    "scarcity_id": row["scarcity_id"],
                    "abundance_id": row["abundance_id"],
                    "score": row["score"],
                    "category_match": bool(row["category_match"]),
                    "keyword_score": row["keyword_score"],
                    "location_score": row["location_score"],
                    "match_reason": row["match_reason"],
                    "status": row["status"],
                    "created_at": row["created_at"],
                })
                for row in rows
            ]

    # HelpOffer Operations
    def save_help_offer(self, offer: HelpOffer) -> HelpOffer:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO help_offers (id, title, category, description, services_json, contact, location, is_emergency, source_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title=excluded.title,
                        category=excluded.category,
                        description=excluded.description,
                        services_json=excluded.services_json,
                        contact=excluded.contact,
                        location=excluded.location,
                        is_emergency=excluded.is_emergency,
                        source_url=excluded.source_url,
                        created_at=excluded.created_at
                    """,
                    (
                        offer.id,
                        offer.title,
                        offer.category,
                        offer.description,
                        json.dumps(offer.services),
                        offer.contact,
                        offer.location,
                        1 if offer.is_emergency else 0,
                        offer.source_url,
                        offer.created_at,
                    ),
                )
                conn.commit()
            return offer

    def list_help_offers(self) -> List[HelpOffer]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM help_offers ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [
                HelpOffer.from_dict({
                    "id": row["id"],
                    "title": row["title"],
                    "category": row["category"],
                    "description": row["description"],
                    "services": json.loads(row["services_json"] or "[]"),
                    "contact": row["contact"],
                    "location": row["location"],
                    "is_emergency": bool(row["is_emergency"]),
                    "source_url": row["source_url"],
                    "created_at": row["created_at"],
                })
                for row in rows
            ]

    # Peer Operations
    def save_peer(self, peer: Peer) -> Peer:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO peers (id, url, name, last_seen, is_active)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                        name=excluded.name,
                        last_seen=excluded.last_seen,
                        is_active=excluded.is_active
                    """,
                    (
                        peer.id,
                        peer.url,
                        peer.name,
                        peer.last_seen,
                        1 if peer.is_active else 0,
                    ),
                )
                conn.commit()
            return peer

    def list_peers(self) -> List[Peer]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peers WHERE is_active = 1 ORDER BY last_seen DESC")
            rows = cursor.fetchall()
            return [
                Peer.from_dict({
                    "id": row["id"],
                    "url": row["url"],
                    "name": row["name"],
                    "last_seen": row["last_seen"],
                    "is_active": bool(row["is_active"]),
                })
                for row in rows
            ]

    # Reflection Operations
    def save_reflection(self, reflection: NodeReflection) -> NodeReflection:
        with self._write_lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO reflections (id, node_id, mangel_json, ueberfluss_json, harmony_score, status_summary, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        node_id=excluded.node_id,
                        mangel_json=excluded.mangel_json,
                        ueberfluss_json=excluded.ueberfluss_json,
                        harmony_score=excluded.harmony_score,
                        status_summary=excluded.status_summary,
                        created_at=excluded.created_at
                    """,
                    (
                        reflection.id,
                        reflection.node_id,
                        json.dumps(reflection.mangel),
                        json.dumps(reflection.ueberfluss),
                        reflection.harmony_score,
                        reflection.status_summary,
                        reflection.created_at,
                    ),
                )
                conn.commit()
            return reflection

    def list_reflections(self) -> List[NodeReflection]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reflections ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [
                NodeReflection.from_dict({
                    "id": row["id"],
                    "node_id": row["node_id"],
                    "mangel": json.loads(row["mangel_json"] or "[]"),
                    "ueberfluss": json.loads(row["ueberfluss_json"] or "[]"),
                    "harmony_score": row["harmony_score"],
                    "status_summary": row["status_summary"],
                    "created_at": row["created_at"],
                })
                for row in rows
            ]


# Default Singleton Database Instance helper
_db_instances: Dict[str, Database] = {}

def get_db(db_path: Optional[str] = None) -> Database:
    path = get_db_path(db_path)
    if path not in _db_instances:
        _db_instances[path] = Database(path)
    return _db_instances[path]
