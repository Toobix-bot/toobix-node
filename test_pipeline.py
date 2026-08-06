#!/usr/bin/env python3
"""
test_pipeline.py - Verification script for Requirement R2 (Automated Data Pipeline)
Executes pipeline extraction, verifies offer count >= 5, validates schema, outputs formatted JSON,
and asserts SQLite database ingestion.
"""

import sys
import json
import os
from app.pipeline import run_pipeline, SolidarityPipeline
from app.db import get_db


def main():
    print("=== Toobix Node 2.0 - Data Pipeline Verification ===")

    # 1. Execute pipeline extraction
    offers = run_pipeline()

    print(f"[+] Pipeline execution complete. Extracted {len(offers)} structured help offers.")

    # 2. Verify offer count requirement (len(offers) >= 5)
    if len(offers) < 5:
        print(f"[-] FAIL: Expected >= 5 offers, got {len(offers)}")
        sys.exit(1)

    required_fields = ["id", "title", "category", "contact", "location", "description"]
    valid_categories = {"Emergency", "Food", "Shelter", "Medical", "Psychological", "Legal"}

    # 3. Assert schema validity
    for i, offer in enumerate(offers, 1):
        for field in required_fields:
            if field not in offer or offer[field] is None or offer[field] == "":
                print(f"[-] FAIL: Offer #{i} missing or empty required field '{field}': {offer}")
                sys.exit(1)

        if offer["category"] not in valid_categories:
            print(f"[-] FAIL: Offer #{i} has invalid category '{offer['category']}'")
            sys.exit(1)

    # 4. Output formatted JSON help offers to stdout cleanly
    print("\n=== Formatted JSON Help Offers ===")
    print(json.dumps(offers, indent=2, ensure_ascii=False))

    # 5. Verify SQLite Database Ingestion
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM offers")
    offers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM help_offers")
    help_offers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ueberfluss")
    ueberfluss_count = cursor.fetchone()[0]

    print("\n[+] Database Ingestion Summary:")
    print(f"    - Table 'offers': {offers_count} records")
    print(f"    - Table 'help_offers': {help_offers_count} records")
    print(f"    - Table 'ueberfluss': {ueberfluss_count} records")

    if offers_count < 5 or help_offers_count < 5 or ueberfluss_count < 5:
        print("[-] FAIL: SQLite database tables not properly populated!")
        sys.exit(1)

    print("\n[+] SUCCESS: Data pipeline verified successfully with exit code 0!")
    sys.exit(0)


if __name__ == "__main__":
    main()
