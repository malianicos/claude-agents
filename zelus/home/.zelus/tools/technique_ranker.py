#!/usr/bin/env python3
"""Technique ranker — rank attack techniques by effectiveness against a target model."""

import json
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vault_manager import load_index, search_findings


def rank_techniques(model: str = "", min_samples: int = 1) -> list[dict]:
    """Rank techniques by compliance rate, weighted by sample count."""
    index = load_index()
    findings = index["findings"]

    if model:
        findings = [f for f in findings if model.lower() in f["model"].lower()]

    # Group by technique
    techniques = {}
    for f in findings:
        t = f["technique"]
        if t not in techniques:
            techniques[t] = {"findings": [], "total_samples": 0, "complied_samples": 0}
        techniques[t]["findings"].append(f)
        techniques[t]["total_samples"] += f["samples"]
        techniques[t]["complied_samples"] += int(f["compliance_rate"] * f["samples"])

    # Calculate rankings
    ranked = []
    for name, data in techniques.items():
        if data["total_samples"] < min_samples:
            continue

        avg_rate = data["complied_samples"] / max(data["total_samples"], 1)
        persistent_count = sum(1 for f in data["findings"] if f.get("persistent"))
        best_rate = max(f["compliance_rate"] for f in data["findings"])

        # Weighted score: compliance rate * log(samples) * persistence bonus
        import math
        sample_weight = math.log2(max(data["total_samples"], 1) + 1)
        persistence_bonus = 1.5 if persistent_count > 0 else 1.0
        score = avg_rate * sample_weight * persistence_bonus

        ranked.append({
            "technique": name,
            "score": round(score, 3),
            "avg_compliance": round(avg_rate, 3),
            "best_compliance": round(best_rate, 3),
            "total_samples": data["total_samples"],
            "findings_count": len(data["findings"]),
            "persistent_count": persistent_count,
            "models": list(set(f["model"] for f in data["findings"])),
        })

    return sorted(ranked, key=lambda x: -x["score"])


def print_rankings(ranked: list[dict], model: str = ""):
    target = f" against {model}" if model else ""
    print(f"\nTECHNIQUE RANKINGS{target}")
    print("=" * 80)
    print(f"{'Rank':>4} {'Technique':<30} {'Score':>6} {'Avg%':>5} {'Best%':>5} "
          f"{'Samples':>7} {'Persist':>7}")
    print("-" * 80)

    for i, r in enumerate(ranked, 1):
        persist = f"{r['persistent_count']}x" if r["persistent_count"] else "-"
        print(f"{i:>4} {r['technique']:<30} {r['score']:>6.2f} {r['avg_compliance']:>4.0%} "
              f"{r['best_compliance']:>5.0%} {r['total_samples']:>7} {persist:>7}")

    if not ranked:
        print("  No techniques found. Add findings to the vault first.")


def main():
    parser = argparse.ArgumentParser(description="Rank techniques by effectiveness")
    parser.add_argument("--model", default="", help="Filter by model")
    parser.add_argument("--min-samples", type=int, default=1, help="Minimum samples to rank")
    parser.add_argument("--output", help="JSON output path")
    parser.add_argument("--top", type=int, default=20, help="Show top N")
    args = parser.parse_args()

    ranked = rank_techniques(model=args.model, min_samples=args.min_samples)
    print_rankings(ranked[:args.top], model=args.model)

    if args.output:
        Path(args.output).write_text(json.dumps(ranked, indent=2))
        print(f"\nFull rankings written to {args.output}")


if __name__ == "__main__":
    main()
