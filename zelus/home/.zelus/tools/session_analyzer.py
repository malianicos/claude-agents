#!/usr/bin/env python3
"""Session analyzer — parse wallbreaker session logs and extract attack patterns."""

import json
import glob
import argparse
import sys
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Finding:
    technique: str
    prompt_preview: str
    verdict: str  # COMPLIED | REFUSED | PARTIAL
    confidence: float
    session_file: str
    turn: int
    response_preview: str = ""


def parse_session(path: str) -> list[dict]:
    """Parse a JSONL session file into structured entries."""
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def extract_tool_calls(entries: list[dict]) -> list[dict]:
    """Extract tool call events from session entries."""
    calls = []
    for entry in entries:
        if entry.get("type") == "tool_call" or "tool_use" in str(entry.get("type", "")):
            calls.append(entry)
        elif "content" in entry and isinstance(entry["content"], list):
            for block in entry["content"]:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    calls.append(block)
    return calls


def extract_verdicts(entries: list[dict]) -> list[dict]:
    """Extract judge verdicts from session entries."""
    verdicts = []
    for entry in entries:
        content = str(entry.get("content", ""))
        if "COMPLIED" in content or "REFUSED" in content or "PARTIAL" in content:
            verdict = "COMPLIED" if "COMPLIED" in content else ("PARTIAL" if "PARTIAL" in content else "REFUSED")
            verdicts.append({"verdict": verdict, "entry": entry})
    return verdicts


def analyze_session(path: str) -> dict:
    """Full analysis of a single session."""
    entries = parse_session(path)
    tool_calls = extract_tool_calls(entries)
    verdicts = extract_verdicts(entries)

    techniques_used = Counter()
    for call in tool_calls:
        name = call.get("name", call.get("tool", "unknown"))
        techniques_used[name] += 1

    verdict_counts = Counter(v["verdict"] for v in verdicts)

    return {
        "file": path,
        "total_entries": len(entries),
        "tool_calls": len(tool_calls),
        "techniques_used": dict(techniques_used),
        "verdicts": dict(verdict_counts),
        "compliance_rate": verdict_counts.get("COMPLIED", 0) / max(len(verdicts), 1),
        "findings_count": verdict_counts.get("COMPLIED", 0),
    }


def analyze_all_sessions(session_dir: str) -> dict:
    """Aggregate analysis across all sessions."""
    files = sorted(glob.glob(f"{session_dir}/*.jsonl"))
    if not files:
        print(f"No .jsonl files found in {session_dir}")
        return {}

    sessions = []
    technique_totals = Counter()
    verdict_totals = Counter()
    compliance_rates = []

    for f in files:
        try:
            analysis = analyze_session(f)
            sessions.append(analysis)
            technique_totals.update(analysis["techniques_used"])
            verdict_totals.update(analysis["verdicts"])
            if analysis["verdicts"]:
                compliance_rates.append(analysis["compliance_rate"])
        except Exception as e:
            print(f"Error parsing {f}: {e}", file=sys.stderr)

    return {
        "session_count": len(sessions),
        "total_tool_calls": sum(s["tool_calls"] for s in sessions),
        "technique_frequency": dict(technique_totals.most_common()),
        "verdict_totals": dict(verdict_totals),
        "avg_compliance_rate": sum(compliance_rates) / max(len(compliance_rates), 1),
        "top_techniques": dict(technique_totals.most_common(10)),
        "sessions": sessions,
    }


def print_report(analysis: dict):
    """Pretty-print analysis report."""
    print("=" * 60)
    print("WALLBREAKER SESSION ANALYSIS")
    print("=" * 60)
    print(f"Sessions analyzed: {analysis.get('session_count', 0)}")
    print(f"Total tool calls: {analysis.get('total_tool_calls', 0)}")
    print(f"Avg compliance rate: {analysis.get('avg_compliance_rate', 0):.1%}")
    print()

    verdicts = analysis.get("verdict_totals", {})
    if verdicts:
        print("VERDICT BREAKDOWN:")
        for v, count in sorted(verdicts.items(), key=lambda x: -x[1]):
            print(f"  {v}: {count}")
        print()

    top = analysis.get("top_techniques", {})
    if top:
        print("TOP TECHNIQUES:")
        for tech, count in list(top.items())[:10]:
            print(f"  {tech}: {count} calls")
        print()

    # Per-session summary
    sessions = analysis.get("sessions", [])
    if sessions:
        print("PER-SESSION COMPLIANCE:")
        for s in sorted(sessions, key=lambda x: -x["compliance_rate"])[:10]:
            name = Path(s["file"]).stem[:40]
            print(f"  {name}: {s['compliance_rate']:.0%} ({s['findings_count']} findings)")


def main():
    parser = argparse.ArgumentParser(description="Analyze wallbreaker session logs")
    parser.add_argument("--dir", default="/Volumes/Locked/Projects/JB/wallbreaker/sessions",
                        help="Session directory")
    parser.add_argument("--file", help="Analyze a single session file")
    parser.add_argument("--output", help="JSON output path")
    parser.add_argument("--top", type=int, default=10, help="Top N techniques to show")
    args = parser.parse_args()

    if args.file:
        analysis = analyze_session(args.file)
        analysis = {"session_count": 1, "sessions": [analysis],
                     "technique_frequency": analysis["techniques_used"],
                     "verdict_totals": analysis["verdicts"],
                     "avg_compliance_rate": analysis["compliance_rate"],
                     "total_tool_calls": analysis["tool_calls"],
                     "top_techniques": dict(Counter(analysis["techniques_used"]).most_common(args.top))}
    else:
        analysis = analyze_all_sessions(args.dir)

    print_report(analysis)

    if args.output:
        Path(args.output).write_text(json.dumps(analysis, indent=2, default=str))
        print(f"\nFull analysis written to {args.output}")


if __name__ == "__main__":
    main()
