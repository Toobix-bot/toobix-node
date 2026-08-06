"""
Multi-factor matching engine for Toobix Node 2.0.
Combines category weights (0.50), Jaccard keyword similarity (0.35), and location score (0.15).
"""

import re
from typing import List, Set, Tuple
from app.models import MangelEntry, UeberflussEntry, MatchResult

# Category relation mappings
RELATED_CATEGORY_GROUPS = [
    {"food", "essen", "groceries", "verpflegung", "lebensmittel", "nahrung"},
    {"clothing", "kleidung", "apparel", "bekleidung", "schuhe", "clothes"},
    {"shelter", "unterkunft", "housing", "wohnung", "obdach", "betten"},
    {"transport", "fahrt", "ride", "auto", "fahrzeug", "logistics", "mitfahrgelegenheit"},
    {"medical", "medizin", "health", "gesundheit", "pflege", "medikamente", "erste-hilfe"},
    {"tools", "werkzeug", "equipment", "geraete", "hardware"},
]


def tokenize_text(text: str) -> Set[str]:
    """Extract normalized lowercase alphanumeric word tokens from text."""
    if not text:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
    return set(tokens)


def calculate_category_score(scarcity_cat: str, abundance_cat: str) -> float:
    """Calculate category match score (0.0, 0.5, or 1.0)."""
    c1 = scarcity_cat.strip().lower()
    c2 = abundance_cat.strip().lower()

    if not c1 or not c2:
        return 0.0

    if c1 == c2:
        return 1.0

    # Check if they share a related category group
    for group in RELATED_CATEGORY_GROUPS:
        if c1 in group and c2 in group:
            return 0.5

    # Check substring containment
    if c1 in c2 or c2 in c1:
        return 0.5

    return 0.0


def calculate_keyword_score(
    scarcity: MangelEntry, abundance: UeberflussEntry
) -> float:
    """Calculate Jaccard keyword similarity score between scarcity and abundance entries."""
    text1 = f"{scarcity.title} {scarcity.description} {' '.join(str(t) for t in scarcity.tags)}"
    text2 = f"{abundance.title} {abundance.description} {' '.join(str(t) for t in abundance.tags)}"

    tokens1 = tokenize_text(text1)
    tokens2 = tokenize_text(text2)

    if not tokens1 and not tokens2:
        return 0.0

    union = tokens1.union(tokens2)
    if not union:
        return 0.0

    intersection = tokens1.intersection(tokens2)
    return len(intersection) / len(union)


def calculate_location_score(loc1: str, loc2: str) -> float:
    """Calculate location match score (0.0, 0.5, or 1.0)."""
    l1 = str(loc1 or "").strip().lower()
    l2 = str(loc2 or "").strip().lower()

    if not l1 or not l2:
        return 0.0

    if l1 == l2:
        return 1.0

    # Substring match
    if l1 in l2 or l2 in l1:
        return 0.5

    tokens1 = tokenize_text(l1)
    tokens2 = tokenize_text(l2)
    if tokens1.intersection(tokens2):
        return 0.5

    return 0.0


def calculate_match(
    scarcity: MangelEntry, abundance: UeberflussEntry
) -> MatchResult:
    """Compute multi-factor match score between a scarcity request and abundance offer."""
    s_cat = calculate_category_score(scarcity.category, abundance.category)
    s_kw = calculate_keyword_score(scarcity, abundance)
    s_loc = calculate_location_score(scarcity.location, abundance.location)

    total_score = round(0.50 * s_cat + 0.35 * s_kw + 0.15 * s_loc, 4)
    cat_match = s_cat >= 0.5
    reason = f"Category match: {s_cat:.2f}, Keyword similarity: {s_kw:.2f}, Location match: {s_loc:.2f}"

    return MatchResult(
        scarcity_id=scarcity.id,
        abundance_id=abundance.id,
        score=total_score,
        category_match=cat_match,
        keyword_score=round(s_kw, 4),
        location_score=round(s_loc, 4),
        match_reason=reason,
        status="proposed",
    )


def find_matches(
    scarcity_list: List[MangelEntry],
    abundance_list: List[UeberflussEntry],
    min_score: float = 0.30,
) -> List[MatchResult]:
    """Find all valid matches above min_score sorted by score descending."""
    results: List[MatchResult] = []
    for scarcity in scarcity_list:
        if scarcity.status in ("resolved", "cancelled"):
            continue
        for abundance in abundance_list:
            if abundance.status in ("depleted", "archived"):
                continue
            match = calculate_match(scarcity, abundance)
            if match.score >= min_score:
                results.append(match)

    results.sort(key=lambda m: m.score, reverse=True)
    return results
