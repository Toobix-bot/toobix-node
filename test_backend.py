"""
Comprehensive Backend Verification Test Suite for Toobix Node 2.0.
Verifies R1 Acceptance Criteria:
- GET /api/health returns 200 OK
- POST and GET /api/scarcity
- POST and GET /api/abundance
- POST /api/matches matching logic and scoring
- DB persistence across operations
- Matching engine multi-factor components (category 0.50, keyword 0.35, location 0.15)
"""

import unittest
import urllib.request
import urllib.error
import json
import os
import sys
import time
import tempfile
import socket

# Ensure app package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import MangelEntry, UeberflussEntry, MatchResult
from app.db import Database
from app.matching import (
    calculate_match,
    find_matches,
    calculate_category_score,
    calculate_keyword_score,
    calculate_location_score,
)
from app.main import run_server_in_thread


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestToobixBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = os.path.join(cls.temp_dir.name, "test_toobix.db")
        cls.port = get_free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.server, cls.thread = run_server_in_thread(
            host="127.0.0.1", port=cls.port, db_path=cls.db_path
        )
        time.sleep(0.2)  # Allow server thread to initialize

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.temp_dir.cleanup()

    def _make_request(
        self, path: str, method: str = "GET", data: dict = None
    ) -> tuple[int, dict]:
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}
        req_data = json.dumps(data).encode("utf-8") if data is not None else None

        request = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request) as response:
                status = response.status
                body = json.loads(response.read().decode("utf-8"))
                return status, body
        except urllib.error.HTTPError as e:
            body = json.loads(e.read().decode("utf-8"))
            return e.code, body

    # 1. Health Endpoint Test
    def test_health_endpoint(self):
        status, body = self._make_request("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(body.get("status"), "ok")
        self.assertEqual(body.get("node_id"), "Toobix-Node-2.0")

    # 2. Scarcity API Endpoints Test
    def test_scarcity_crud(self):
        scarcity_payload = {
            "title": "Need Emergency Food Package",
            "category": "food",
            "description": "Family of 4 needs fresh vegetables and canned bread in Berlin Mitte",
            "urgency": "high",
            "location": "Berlin Mitte",
            "contact": "alice@example.org",
            "tags": ["food", "emergency", "berlin"],
        }
        status, body = self._make_request("/api/scarcity", method="POST", data=scarcity_payload)
        self.assertEqual(status, 201)
        self.assertTrue("id" in body)
        scarcity_id = body["id"]
        self.assertEqual(body["title"], scarcity_payload["title"])

        # GET List
        status, list_body = self._make_request("/api/scarcity")
        self.assertEqual(status, 200)
        self.assertTrue(isinstance(list_body, list))
        found = any(item["id"] == scarcity_id for item in list_body)
        self.assertTrue(found)

        # GET Detail
        status, detail_body = self._make_request(f"/api/scarcity/{scarcity_id}")
        self.assertEqual(status, 200)
        self.assertEqual(detail_body["id"], scarcity_id)

        # GET Non-existent
        status, not_found_body = self._make_request("/api/scarcity/nonexistent-id-999")
        self.assertEqual(status, 404)

    # 3. Abundance API Endpoints Test
    def test_abundance_crud(self):
        abundance_payload = {
            "title": "Fresh Vegetables and Bread Available",
            "category": "food",
            "description": "Warm food packages and canned bread available for pickup in Berlin",
            "quantity": "10 packages",
            "location": "Berlin Mitte",
            "contact": "bob@example.org",
            "tags": ["food", "bread", "berlin"],
        }
        status, body = self._make_request("/api/abundance", method="POST", data=abundance_payload)
        self.assertEqual(status, 201)
        self.assertTrue("id" in body)
        abundance_id = body["id"]
        self.assertEqual(body["title"], abundance_payload["title"])

        # GET List
        status, list_body = self._make_request("/api/abundance")
        self.assertEqual(status, 200)
        self.assertTrue(isinstance(list_body, list))
        found = any(item["id"] == abundance_id for item in list_body)
        self.assertTrue(found)

        # GET Detail
        status, detail_body = self._make_request(f"/api/abundance/{abundance_id}")
        self.assertEqual(status, 200)
        self.assertEqual(detail_body["id"], abundance_id)

        # GET Non-existent
        status, not_found_body = self._make_request("/api/abundance/nonexistent-id-999")
        self.assertEqual(status, 404)

    # 4. Matches Calculation and API Test
    def test_matches_calculation_and_retrieval(self):
        # Create matching Pair
        m_payload = {
            "title": "Winter Jacket Need",
            "category": "clothing",
            "description": "Seeking warm winter jacket size L in Hamburg",
            "location": "Hamburg",
            "contact": "charlie@example.org",
        }
        status, m_resp = self._make_request("/api/scarcity", method="POST", data=m_payload)
        self.assertEqual(status, 201)
        m_id = m_resp["id"]

        a1_payload = {
            "title": "Warm Winter Jacket L",
            "category": "clothing",
            "description": "Offering warm L size winter jacket good condition Hamburg",
            "location": "Hamburg",
            "contact": "dave@example.org",
        }
        status, a1_resp = self._make_request("/api/abundance", method="POST", data=a1_payload)
        self.assertEqual(status, 201)
        a1_id = a1_resp["id"]

        # Create completely unrelated entry
        a2_payload = {
            "title": "Power Drill Kit",
            "category": "tools",
            "description": "Drill tools available for rent in Munich",
            "location": "Munich",
            "contact": "eve@example.org",
        }
        status, a2_resp = self._make_request("/api/abundance", method="POST", data=a2_payload)
        self.assertEqual(status, 201)

        # POST /api/matches
        status, matches_resp = self._make_request(
            "/api/matches", method="POST", data={"scarcity_id": m_id, "min_score": 0.30}
        )
        self.assertEqual(status, 200)
        self.assertTrue(isinstance(matches_resp, list))
        self.assertGreaterEqual(len(matches_resp), 1)

        best_match = matches_resp[0]
        self.assertEqual(best_match["scarcity_id"], m_id)
        self.assertEqual(best_match["abundance_id"], a1_id)
        self.assertGreaterEqual(best_match["score"], 0.70)
        self.assertTrue(best_match["category_match"])

        # GET /api/matches
        status, get_matches = self._make_request(f"/api/matches?scarcity_id={m_id}")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(get_matches), 1)
        self.assertEqual(get_matches[0]["scarcity_id"], m_id)

    # 5. DB Persistence Test
    def test_db_persistence(self):
        db_file = os.path.join(self.temp_dir.name, "persistence_test.db")
        db1 = Database(db_file)

        m_entry = MangelEntry(
            title="Medical Supplies Need",
            category="medical",
            description="First aid kit required",
            location="Leipzig",
        )
        db1.save_mangel(m_entry)

        u_entry = UeberflussEntry(
            title="First Aid Kits",
            category="medical",
            description="Unopened first aid kit",
            location="Leipzig",
        )
        db1.save_ueberfluss(u_entry)

        match = calculate_match(m_entry, u_entry)
        db1.save_match(match)

        # Close/re-open second database instance pointing to the same file
        db2 = Database(db_file)
        retrieved_mangel = db2.get_mangel(m_entry.id)
        self.assertIsNotNone(retrieved_mangel)
        self.assertEqual(retrieved_mangel.title, "Medical Supplies Need")

        retrieved_ueberfluss = db2.get_ueberfluss(u_entry.id)
        self.assertIsNotNone(retrieved_ueberfluss)
        self.assertEqual(retrieved_ueberfluss.title, "First Aid Kits")

        matches = db2.list_matches(scarcity_id=m_entry.id)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].id, match.id)

    # 6. Multi-Factor Matching Algorithm Direct Component Tests
    def test_matching_components(self):
        # Category scores: exact=1.0, related=0.5, mismatch=0.0
        self.assertEqual(calculate_category_score("food", "food"), 1.0)
        self.assertEqual(calculate_category_score("food", "essen"), 0.5)
        self.assertEqual(calculate_category_score("food", "tools"), 0.0)

        # Location scores: exact/both empty=1.0, partial/contained=0.5, different=0.0
        self.assertEqual(calculate_location_score("Berlin Mitte", "Berlin Mitte"), 1.0)
        self.assertEqual(calculate_location_score("Berlin Mitte", "Berlin"), 0.5)
        self.assertEqual(calculate_location_score("Berlin", "Hamburg"), 0.0)

        # Multi-factor weights verification
        m_entry = MangelEntry(
            title="Transport Ride",
            category="transport",
            description="Need ride from Berlin to Dresden on Monday",
            location="Berlin",
        )
        u_entry = UeberflussEntry(
            title="Car Ride Berlin to Dresden",
            category="transport",
            description="Offering passenger ride from Berlin to Dresden",
            location="Berlin",
        )

        match = calculate_match(m_entry, u_entry)
        # Category=1.0 (0.50), Location=1.0 (0.15), Keyword > 0.5 (>= 0.175) -> score >= 0.82
        self.assertEqual(match.category_match, True)
        self.assertGreaterEqual(match.score, 0.75)

    # 7. Node Self-Reflection Test (Requirement R4)
    def test_node_self_reflection(self):
        status, body = self._make_request("/api/reflection")
        self.assertEqual(status, 200)
        self.assertEqual(body.get("node_id"), "Toobix-Node-2.0")
        self.assertIn("mangel", body)
        self.assertIn("ueberfluss", body)
        self.assertIn("harmony_score", body)
        self.assertIn("status_summary", body)
        self.assertGreaterEqual(len(body["mangel"]), 1)
        self.assertGreaterEqual(len(body["ueberfluss"]), 1)

        # Check self Mangel and Ueberfluss entries exist in DB
        status, mangel_list = self._make_request("/api/scarcity")
        self.assertEqual(status, 200)
        self.assertTrue(any("Self-Need" in m["title"] for m in mangel_list))

        status, ueberfluss_list = self._make_request("/api/abundance")
        self.assertEqual(status, 200)
        self.assertTrue(any("Self-Offer" in u["title"] for u in ueberfluss_list))


if __name__ == "__main__":
    unittest.main()
