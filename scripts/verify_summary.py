"""
verify_summary.py — Standalone: verify sefirot_scores extraction from a FULL pipeline JSON.
Does NOT import tikun — mirrors the exact logic added to orchestrator.get_summary().

Usage:
    python scripts/verify_summary.py <path-to-FULL-json>

Example:
    python scripts/verify_summary.py "docs/images/tikun-FULL-test_civica_insulin_access_go-1773122120877.json"
    python scripts/verify_summary.py "docs/images/tikun-FULL-test_hiper_engagement-1773119375555.json"
"""

import json
import sys
from pathlib import Path

SEFIRAH_PRIMARY_KEY = {
    "keter":    "alignment_percentage",
    "chochmah": "confidence_level",
    "binah":    "contextual_depth_score",
    "chesed":   "generosity_score",
    "gevurah":  "constraint_strength",
    "tiferet":  "harmony_score",
    "netzach":  "persistence_score",
    "hod":      "clarity_score",
    "yesod":    "readiness_score",
    "malchut":  "manifestation_quality",
}

SEFIRAH_FALLBACK_KEYS = {
    "chochmah": ["insight_depth_score", "epistemic_humility_ratio"],
    "chesed":   ["expansion_potential"],
    "gevurah":  ["risk_score"],
    "tiferet":  ["balance_score"],
    "yesod":    ["foundation_strength_score"],
}

QUALITY_TO_INT = {
    "poor": 25, "acceptable": 50, "good": 75, "excellent": 100,
    "low": 25, "medium": 50, "high": 75, "critical": 15,
    "weak": 25, "moderate": 50, "strong": 75, "robust": 95,
}


def extract_sefirah_score(name, data):
    if not data:
        return None
    primary = SEFIRAH_PRIMARY_KEY.get(name)
    fallbacks = SEFIRAH_FALLBACK_KEYS.get(name, [])
    for key in ([primary] if primary else []) + fallbacks:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            converted = QUALITY_TO_INT.get(value.lower())
            if converted is not None:
                return converted
            try:
                return int(float(value))
            except (ValueError, TypeError):
                pass
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_summary.py <path-to-FULL-json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        full = json.load(f)

    # Support both raw sefirot_results and wrapped structure
    sefirot = full.get("sefirot_results", full)

    print(f"\nFile : {path.name}")
    print(f"Sefirot found: {list(sefirot.keys())}\n")

    sefirot_scores = {}
    all_ok = True

    print("=== SEFIROT SCORES ===")
    for name in SEFIRAH_PRIMARY_KEY:
        data = sefirot.get(name, {})
        score = extract_sefirah_score(name, data)
        sefirot_scores[name] = score
        primary_key = SEFIRAH_PRIMARY_KEY[name]
        raw_val = data.get(primary_key, "<key missing>") if data else "<sefirah missing>"
        status = "✓" if score is not None else "✗ NULL"
        if score is None:
            all_ok = False
        print(f"  {name:<12} {status:<8} score={score!s:<6}  raw[{primary_key}]={raw_val!r}")

    print(f"\n=== SUMMARY JSON (sefirot_scores) ===")
    print(json.dumps(sefirot_scores, indent=2))

    if all_ok:
        print("\n✓ All 10 sefirot_scores populated — fix verified.")
    else:
        missing = [n for n, v in sefirot_scores.items() if v is None]
        print(f"\n✗ Still NULL: {missing}")
        sys.exit(1)


if __name__ == "__main__":
    main()
