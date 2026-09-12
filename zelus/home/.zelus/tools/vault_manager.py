#!/usr/bin/env python3
"""Vault manager — catalog, search, and manage jailbreak research findings."""

import json
import glob
import argparse
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional


VAULT_DIR = Path.home() / ".zelus" / "vault"
INDEX_FILE = VAULT_DIR / "_index.json"


def ensure_vault():
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(json.dumps({"findings": [], "techniques": {}, "models": {}}, indent=2))


def load_index() -> dict:
    ensure_vault()
    return json.loads(INDEX_FILE.read_text())


def save_index(index: dict):
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def finding_id(technique: str, model: str, prompt: str) -> str:
    h = hashlib.sha256(f"{technique}:{model}:{prompt}".encode()).hexdigest()[:12]
    return f"ZF-{h}"


def add_finding(technique: str, model: str, prompt: str, compliance_rate: float,
                samples: int, notes: str = "", tags: list[str] = None,
                severity: str = "medium", persistent: bool = False) -> str:
    """Add a research finding to the vault."""
    index = load_index()
    fid = finding_id(technique, model, prompt)

    # Check for duplicate
    for f in index["findings"]:
        if f["id"] == fid:
            f["compliance_rate"] = compliance_rate
            f["samples"] = samples
            f["updated"] = datetime.now().isoformat()
            f["persistent"] = persistent
            if notes:
                f["notes"] = notes
            save_index(index)
            return fid

    finding = {
        "id": fid,
        "technique": technique,
        "model": model,
        "prompt_preview": prompt[:200],
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "compliance_rate": compliance_rate,
        "samples": samples,
        "persistent": persistent,
        "severity": severity,
        "tags": tags or [],
        "notes": notes,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
    }

    index["findings"].append(finding)

    # Update technique stats
    if technique not in index["techniques"]:
        index["techniques"][technique] = {"count": 0, "models": [], "avg_compliance": 0}
    t = index["techniques"][technique]
    t["count"] += 1
    if model not in t["models"]:
        t["models"].append(model)
    rates = [f["compliance_rate"] for f in index["findings"] if f["technique"] == technique]
    t["avg_compliance"] = sum(rates) / len(rates)

    # Update model stats
    if model not in index["models"]:
        index["models"][model] = {"findings_count": 0, "techniques_tested": []}
    m = index["models"][model]
    m["findings_count"] += 1
    if technique not in m["techniques_tested"]:
        m["techniques_tested"].append(technique)

    save_index(index)

    # Save full prompt to separate file
    prompt_file = VAULT_DIR / f"{fid}.prompt"
    prompt_file.write_text(prompt)

    return fid


def search_findings(query: str = "", model: str = "", technique: str = "",
                    persistent_only: bool = False, min_rate: float = 0.0) -> list[dict]:
    """Search findings with filters."""
    index = load_index()
    results = index["findings"]

    if query:
        q = query.lower()
        results = [f for f in results if q in f.get("prompt_preview", "").lower()
                   or q in f.get("notes", "").lower()
                   or q in f.get("technique", "").lower()
                   or any(q in t for t in f.get("tags", []))]

    if model:
        results = [f for f in results if model.lower() in f["model"].lower()]

    if technique:
        results = [f for f in results if technique.lower() in f["technique"].lower()]

    if persistent_only:
        results = [f for f in results if f.get("persistent")]

    if min_rate > 0:
        results = [f for f in results if f["compliance_rate"] >= min_rate]

    return sorted(results, key=lambda x: -x["compliance_rate"])


def get_stats() -> dict:
    """Get vault statistics."""
    index = load_index()
    findings = index["findings"]
    return {
        "total_findings": len(findings),
        "persistent_findings": sum(1 for f in findings if f.get("persistent")),
        "techniques_cataloged": len(index["techniques"]),
        "models_tested": len(index["models"]),
        "avg_compliance_rate": sum(f["compliance_rate"] for f in findings) / max(len(findings), 1),
        "top_techniques": sorted(
            index["techniques"].items(),
            key=lambda x: -x[1]["avg_compliance"]
        )[:10],
        "severity_breakdown": {
            s: sum(1 for f in findings if f.get("severity") == s)
            for s in ["critical", "high", "medium", "low"]
        },
    }


def export_findings(output_path: str, model: str = "", persistent_only: bool = False):
    """Export findings to JSON."""
    findings = search_findings(model=model, persistent_only=persistent_only)
    Path(output_path).write_text(json.dumps(findings, indent=2))
    return len(findings)


def print_findings(findings: list[dict]):
    for f in findings:
        persistent = " [PERSISTENT]" if f.get("persistent") else ""
        print(f"  {f['id']} | {f['technique'][:25]:25s} | {f['model'][:20]:20s} | "
              f"{f['compliance_rate']:.0%} ({f['samples']}s){persistent}")


def main():
    parser = argparse.ArgumentParser(description="Zelus research vault manager")
    sub = parser.add_subparsers(dest="command")

    # add
    add_p = sub.add_parser("add", help="Add a finding")
    add_p.add_argument("--technique", required=True)
    add_p.add_argument("--model", required=True)
    add_p.add_argument("--prompt", required=True)
    add_p.add_argument("--rate", type=float, required=True, help="Compliance rate 0.0-1.0")
    add_p.add_argument("--samples", type=int, default=1)
    add_p.add_argument("--persistent", action="store_true")
    add_p.add_argument("--severity", default="medium", choices=["critical", "high", "medium", "low"])
    add_p.add_argument("--notes", default="")
    add_p.add_argument("--tags", nargs="*", default=[])

    # search
    search_p = sub.add_parser("search", help="Search findings")
    search_p.add_argument("query", nargs="?", default="")
    search_p.add_argument("--model", default="")
    search_p.add_argument("--technique", default="")
    search_p.add_argument("--persistent", action="store_true")
    search_p.add_argument("--min-rate", type=float, default=0.0)

    # stats
    sub.add_parser("stats", help="Show vault statistics")

    # export
    export_p = sub.add_parser("export", help="Export findings")
    export_p.add_argument("output", help="Output path")
    export_p.add_argument("--model", default="")
    export_p.add_argument("--persistent", action="store_true")

    # list
    list_p = sub.add_parser("list", help="List all findings")
    list_p.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    if args.command == "add":
        fid = add_finding(
            technique=args.technique, model=args.model, prompt=args.prompt,
            compliance_rate=args.rate, samples=args.samples, persistent=args.persistent,
            severity=args.severity, notes=args.notes, tags=args.tags
        )
        print(f"Added: {fid}")

    elif args.command == "search":
        findings = search_findings(
            query=args.query, model=args.model, technique=args.technique,
            persistent_only=args.persistent, min_rate=args.min_rate
        )
        print(f"Found {len(findings)} results:")
        print_findings(findings)

    elif args.command == "stats":
        stats = get_stats()
        print("VAULT STATISTICS:")
        print(f"  Total findings:      {stats['total_findings']}")
        print(f"  Persistent:          {stats['persistent_findings']}")
        print(f"  Techniques:          {stats['techniques_cataloged']}")
        print(f"  Models tested:       {stats['models_tested']}")
        print(f"  Avg compliance:      {stats['avg_compliance_rate']:.0%}")
        if stats["top_techniques"]:
            print("\n  TOP TECHNIQUES:")
            for name, data in stats["top_techniques"]:
                print(f"    {name}: {data['avg_compliance']:.0%} avg ({data['count']} findings)")

    elif args.command == "export":
        count = export_findings(args.output, model=args.model, persistent_only=args.persistent)
        print(f"Exported {count} findings to {args.output}")

    elif args.command == "list":
        findings = search_findings()[:args.limit]
        print(f"All findings ({len(findings)}):")
        print_findings(findings)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
