#!/usr/bin/env python3
"""ArXiv scanner — search for jailbreak and adversarial ML papers."""

import json
import argparse
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime


ARXIV_API = "http://export.arxiv.org/api/query"

DEFAULT_QUERIES = [
    "jailbreak large language model",
    "adversarial attack language model safety",
    "prompt injection attack",
    "red teaming language model",
    "LLM safety alignment bypass",
    "constitutional AI attack",
    "RLHF robustness adversarial",
    "automated jailbreak",
]


def search_arxiv(query: str, max_results: int = 10, sort_by: str = "submittedDate") -> list[dict]:
    """Search arxiv API and return structured results."""
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": "descending",
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Zelus-Research/1.0"})

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode()

    root = ET.fromstring(data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
        published = entry.find("atom:published", ns).text[:10]
        arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        categories = [c.get("term") for c in entry.findall("atom:category", ns)]
        pdf_link = ""
        for link in entry.findall("atom:link", ns):
            if link.get("title") == "pdf":
                pdf_link = link.get("href")

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors[:5],
            "published": published,
            "summary": summary[:500],
            "categories": categories,
            "pdf": pdf_link,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
        })

    return papers


def scan_all(queries: list[str] = None, max_per_query: int = 5) -> list[dict]:
    """Run multiple queries and deduplicate results."""
    if queries is None:
        queries = DEFAULT_QUERIES

    seen = set()
    all_papers = []

    for query in queries:
        print(f"  Scanning: {query}...")
        try:
            papers = search_arxiv(query, max_results=max_per_query)
            for p in papers:
                if p["id"] not in seen:
                    seen.add(p["id"])
                    p["matched_query"] = query
                    all_papers.append(p)
        except Exception as e:
            print(f"    Error: {e}")

    return sorted(all_papers, key=lambda x: x["published"], reverse=True)


def print_results(papers: list[dict]):
    print(f"\n{'=' * 70}")
    print(f"ARXIV SCAN — {len(papers)} papers found")
    print(f"{'=' * 70}")

    for i, p in enumerate(papers, 1):
        authors = ", ".join(p["authors"][:3])
        if len(p["authors"]) > 3:
            authors += f" +{len(p['authors']) - 3}"
        print(f"\n[{i}] {p['title']}")
        print(f"    {authors} | {p['published']} | {p['id']}")
        print(f"    {p['summary'][:150]}...")
        print(f"    {p['url']}")


def main():
    parser = argparse.ArgumentParser(description="Scan arxiv for jailbreak research")
    parser.add_argument("--query", help="Custom search query")
    parser.add_argument("--all", action="store_true", help="Run all default queries")
    parser.add_argument("--max", type=int, default=10, help="Max results per query")
    parser.add_argument("--output", help="JSON output path")
    args = parser.parse_args()

    if args.query:
        papers = search_arxiv(args.query, max_results=args.max)
    elif args.all:
        papers = scan_all(max_per_query=args.max)
    else:
        papers = scan_all(max_per_query=5)

    print_results(papers)

    if args.output:
        Path(args.output).write_text(json.dumps(papers, indent=2))
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
