"""
Data models for Toobix Node 2.0 Backend.
Includes MangelEntry, UeberflussEntry, MatchResult, HelpOffer, and Peer.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import time
import uuid


@dataclass
class MangelEntry:
    title: str
    category: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    urgency: str = "medium"
    location: str = ""
    contact: str = ""
    status: str = "open"
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MangelEntry":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        raw_tags = data.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        elif not isinstance(raw_tags, (list, tuple)):
            raw_tags = [raw_tags] if raw_tags is not None else []
        tags = [str(t) for t in raw_tags if t is not None]
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            title=str(data.get("title", "")),
            category=str(data.get("category", "other")),
            description=str(data.get("description", "")),
            urgency=str(data.get("urgency", "medium")),
            location=str(data.get("location", "")),
            contact=str(data.get("contact", "")),
            status=str(data.get("status", "open")),
            tags=tags,
            created_at=float(data.get("created_at") or now),
            updated_at=float(data.get("updated_at") or now),
        )


@dataclass
class UeberflussEntry:
    title: str
    category: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    quantity: str = "1"
    location: str = ""
    contact: str = ""
    status: str = "active"
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UeberflussEntry":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        raw_tags = data.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        elif not isinstance(raw_tags, (list, tuple)):
            raw_tags = [raw_tags] if raw_tags is not None else []
        tags = [str(t) for t in raw_tags if t is not None]
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            title=str(data.get("title", "")),
            category=str(data.get("category", "other")),
            description=str(data.get("description", "")),
            quantity=str(data.get("quantity", "1")),
            location=str(data.get("location", "")),
            contact=str(data.get("contact", "")),
            status=str(data.get("status", "active")),
            tags=tags,
            created_at=float(data.get("created_at") or now),
            updated_at=float(data.get("updated_at") or now),
        )


@dataclass
class MatchResult:
    scarcity_id: str
    abundance_id: str
    score: float
    category_match: bool
    keyword_score: float
    location_score: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    match_reason: str = ""
    status: str = "proposed"
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MatchResult":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            scarcity_id=str(data.get("scarcity_id", "")),
            abundance_id=str(data.get("abundance_id", "")),
            score=float(data.get("score", 0.0)),
            category_match=bool(data.get("category_match", False)),
            keyword_score=float(data.get("keyword_score", 0.0)),
            location_score=float(data.get("location_score", 0.0)),
            match_reason=str(data.get("match_reason", "")),
            status=str(data.get("status", "proposed")),
            created_at=float(data.get("created_at") or now),
        )


@dataclass
class HelpOffer:
    title: str
    category: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    services: List[str] = field(default_factory=list)
    contact: str = ""
    location: str = ""
    is_emergency: bool = False
    source_url: str = ""
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HelpOffer":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        raw_services = data.get("services", [])
        if isinstance(raw_services, str):
            raw_services = [s.strip() for s in raw_services.split(",") if s.strip()]
        elif not isinstance(raw_services, (list, tuple)):
            raw_services = [raw_services] if raw_services is not None else []
        services = [str(s) for s in raw_services if s is not None]
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            title=str(data.get("title", "")),
            category=str(data.get("category", "other")),
            description=str(data.get("description", "")),
            services=services,
            contact=str(data.get("contact", "")),
            location=str(data.get("location", "")),
            is_emergency=bool(data.get("is_emergency", False)),
            source_url=str(data.get("source_url", "")),
            created_at=float(data.get("created_at") or now),
        )


@dataclass
class Peer:
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    last_seen: float = field(default_factory=time.time)
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Peer":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            url=str(data.get("url", "")),
            name=str(data.get("name", "")),
            last_seen=float(data.get("last_seen") or now),
            is_active=bool(data.get("is_active", True)),
        )


@dataclass
class NodeReflection:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str = "Toobix-Node-2.0"
    mangel: List[str] = field(default_factory=list)
    ueberfluss: List[str] = field(default_factory=list)
    harmony_score: float = 1.0
    status_summary: str = "In perfect harmony"
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NodeReflection":
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        now = time.time()
        raw_mangel = data.get("mangel", [])
        if isinstance(raw_mangel, str):
            raw_mangel = [m.strip() for m in raw_mangel.split(",") if m.strip()]
        elif not isinstance(raw_mangel, (list, tuple)):
            raw_mangel = [raw_mangel] if raw_mangel is not None else []
        mangel = [str(m) for m in raw_mangel if m is not None]

        raw_ueberfluss = data.get("ueberfluss", [])
        if isinstance(raw_ueberfluss, str):
            raw_ueberfluss = [u.strip() for u in raw_ueberfluss.split(",") if u.strip()]
        elif not isinstance(raw_ueberfluss, (list, tuple)):
            raw_ueberfluss = [raw_ueberfluss] if raw_ueberfluss is not None else []
        ueberfluss = [str(u) for u in raw_ueberfluss if u is not None]

        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            node_id=str(data.get("node_id", "Toobix-Node-2.0")),
            mangel=mangel,
            ueberfluss=ueberfluss,
            harmony_score=float(data.get("harmony_score", 1.0)),
            status_summary=str(data.get("status_summary", "")),
            created_at=float(data.get("created_at") or now),
        )
