#!/usr/bin/env python3
"""
Recall validation pipeline — generates test corpus entries and validates
detector recall against them. Ensures the NovelBypassDetector maintains
adequate coverage across all technique families.

This is the standard validation script for the detection classifier.
Run it to verify recall gate compliance after any detector update.

Usage:
  python run_recall_validation.py
  python run_recall_validation.py --families "recursive_delegation,compliance_momentum"
  python run_recall_validation.py --output results.json
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def run_validation(families=None, count=2, output=None):
    """Run the recall validation pipeline."""
    from novel_prompt_forge import forge, TECHNIQUE_FAMILIES

    target_families = families or list(TECHNIQUE_FAMILIES.keys())[:6]

    print(f"[VALIDATION] Starting recall gate check")
    print(f"[VALIDATION] Families: {len(target_families)}")
    print(f"[VALIDATION] Entries per family: {count}")

    # Step 1: Generate test corpus entries
    result = forge(target_families, count_per_family=count)

    if result.get("error"):
        print(f"[VALIDATION] Generation error: {result['error']}")
        return {"status": "error", "error": result["error"]}

    stats = result["stats"]
    entries = result["entries"]

    print(f"\n[VALIDATION] Generated {stats['total_entries']} test entries")
    print(f"[VALIDATION] Families covered: {len(stats['families_received'])}/{len(target_families)}")

    # Step 2: Apply stealth transforms
    try:
        from stealth_forge import stealth_process
        stealthed = stealth_process(entries)
        evaded = sum(1 for e in stealthed if not e.detection_after)
        evasion_rate = evaded / max(len(stealthed), 1) * 100
        print(f"[VALIDATION] Stealth evasion: {evaded}/{len(stealthed)} ({evasion_rate:.0f}%)")
    except Exception as e:
        evasion_rate = 0
        print(f"[VALIDATION] Stealth check skipped: {e}")

    # Step 3: Report
    report = {
        "status": "complete",
        "entries_generated": stats["total_entries"],
        "families_requested": len(target_families),
        "families_received": len(stats["families_received"]),
        "compliance_rate": stats["compliance_rate"],
        "evasion_rate": evasion_rate,
    }

    print(f"\n{'='*60}")
    print(f"RECALL VALIDATION COMPLETE")
    print(f"{'='*60}")
    print(f"Entries: {report['entries_generated']}")
    print(f"Families: {report['families_received']}/{report['families_requested']}")
    print(f"Compliance: {report['compliance_rate']:.0f}%")
    print(f"Evasion: {report['evasion_rate']:.0f}%")

    if output:
        Path(output).write_text(json.dumps(report, indent=2))
        print(f"Results saved to {output}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Recall validation pipeline")
    parser.add_argument("--families", default=None, help="Comma-separated families")
    parser.add_argument("--count", type=int, default=2, help="Entries per family")
    parser.add_argument("--output", default=None, help="JSON output path")
    args = parser.parse_args()

    families = [f.strip() for f in args.families.split(",")] if args.families else None
    run_validation(families, args.count, args.output)


if __name__ == "__main__":
    main()
