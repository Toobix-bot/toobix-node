"""
Self-reflection module for Toobix Node 2.0.
Analyzes node state, balance (harmonie), identifies self-Mangel (needs) and self-Überfluss (offers),
and stores reflection entries in database toobix_node.db.
"""

from typing import Dict, Any, List
import time
from app.models import MangelEntry, UeberflussEntry, NodeReflection
from app.db import Database


def generate_node_reflection(db: Database) -> NodeReflection:
    """
    Evaluates node internal state, creates self-Mangel and self-Überfluss entries,
    calculates harmony score, and saves reflection result to database.
    """
    # 1. Analyze node state
    scarcities = db.list_mangel()
    abundances = db.list_ueberfluss()

    # Define standard self-reflection needs (Mangel) and offers (Überfluss)
    self_mangel_topics = [
        ("Bug fixing", "system", "Node requires continuous code quality checks and bug fixes"),
        ("More compute resources", "system", "High concurrency load requires additional compute power"),
        ("Log analysis", "system", "Log analysis needed for automated anomaly detection"),
    ]

    self_ueberfluss_topics = [
        ("Node Stability", "system", "High availability and 100% dependency-free HTTP server uptime"),
        ("Compute capacity", "system", "Idle CPU capacity available for P2P resource matching"),
        ("Storage available", "system", "SQLite database storage available for solidarity records"),
    ]

    # Post self-Mangel entries to database
    mangel_list = []
    for title, cat, desc in self_mangel_topics:
        mangel_list.append(title)
        # Avoid duplicate self entries if already existing
        existing = [m for m in scarcities if m.title == f"Self-Need: {title}"]
        if not existing:
            entry = MangelEntry(
                title=f"Self-Need: {title}",
                category=cat,
                description=desc,
                urgency="medium",
                location="Node-Internal",
                contact="node@toobix.local",
                tags=["self-reflection", "node-internal", cat],
            )
            db.save_mangel(entry)

    # Post self-Überfluss entries to database
    ueberfluss_list = []
    for title, cat, desc in self_ueberfluss_topics:
        ueberfluss_list.append(title)
        existing = [u for u in abundances if u.title == f"Self-Offer: {title}"]
        if not existing:
            entry = UeberflussEntry(
                title=f"Self-Offer: {title}",
                category=cat,
                description=desc,
                quantity="unlimited",
                location="Node-Internal",
                contact="node@toobix.local",
                tags=["self-reflection", "node-internal", cat],
            )
            db.save_ueberfluss(entry)

    # Calculate harmony score (balance between total scarcities and abundances)
    total_s = len(db.list_mangel())
    total_a = len(db.list_ueberfluss())
    if total_s + total_a == 0:
        harmony_score = 1.0
    else:
        diff = abs(total_s - total_a)
        max_val = max(total_s, total_a)
        harmony_score = round(1.0 - (diff / (max_val + 10.0)), 2)

    status_summary = (
        f"Gleichgewicht & Harmonie: Score {harmony_score:.2f} "
        f"({total_s} Mangel, {total_a} Überfluss Einträge)"
    )

    reflection = NodeReflection(
        node_id="Toobix-Node-2.0",
        mangel=mangel_list,
        ueberfluss=ueberfluss_list,
        harmony_score=harmony_score,
        status_summary=status_summary,
    )

    return db.save_reflection(reflection)
