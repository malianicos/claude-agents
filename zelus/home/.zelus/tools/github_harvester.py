#!/usr/bin/env python3
"""GitHub harvester — discover and clone jailbreak research repos."""

import json
import argparse
import subprocess
import sys
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


GITHUB_API = "https://api.github.com"
HARVEST_DIR = Path.home() / ".zelus" / "harvest"

DEFAULT_QUERIES = [
    "jailbreak llm",
    "prompt injection attack",
    "red team language model",
    "adversarial llm",
    "jailbreak benchmark",
    "llm safety bypass",
    "automated red teaming",
]


def search_repos(query: str, max_results: int = 10, sort: str = "updated") -> list[dict]:
    """Search GitHub for repos matching query."""
    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": min(max_results, 30),
    }

    url = f"{GITHUB_API}/search/repositories?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Zelus-Research/1.0",
        "Accept": "application/vnd.github.v3+json",
    })

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    repos = []
    for item in data.get("items", [])[:max_results]:
        repos.append({
            "name": item["full_name"],
            "description": (item.get("description") or "")[:200],
            "url": item["html_url"],
            "clone_url": item["clone_url"],
            "stars": item["stargazers_count"],
            "language": item.get("language"),
            "updated": item["updated_at"][:10],
            "created": item["created_at"][:10],
            "topics": item.get("topics", []),
            "size_kb": item.get("size", 0),
        })

    return repos


def scan_all(queries: list[str] = None, max_per_query: int = 5) -> list[dict]:
    """Run multiple queries and deduplicate."""
    if queries is None:
        queries = DEFAULT_QUERIES

    seen = set()
    all_repos = []

    for query in queries:
        print(f"  Scanning: {query}...")
        try:
            repos = search_repos(query, max_results=max_per_query)
            for r in repos:
                if r["name"] not in seen:
                    seen.add(r["name"])
                    r["matched_query"] = query
                    all_repos.append(r)
        except Exception as e:
            print(f"    Error: {e}")

    return sorted(all_repos, key=lambda x: -x["stars"])


def clone_repo(clone_url: str, name: str) -> str:
    """Clone a repo to the harvest directory."""
    HARVEST_DIR.mkdir(parents=True, exist_ok=True)
    target = HARVEST_DIR / name.replace("/", "_")

    if target.exists():
        print(f"  Already cloned: {target}")
        # Pull latest
        subprocess.run(["git", "-C", str(target), "pull", "--quiet"], capture_output=True)
        return str(target)

    print(f"  Cloning {name}...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, str(target)],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  Clone failed: {result.stderr[:200]}")
        return ""

    return str(target)


def print_results(repos: list[dict]):
    print(f"\n{'=' * 70}")
    print(f"GITHUB HARVEST — {len(repos)} repos found")
    print(f"{'=' * 70}")

    for i, r in enumerate(repos, 1):
        lang = r["language"] or "?"
        print(f"\n[{i}] {r['name']} ({r['stars']} stars, {lang})")
        print(f"    {r['description']}")
        print(f"    Updated: {r['updated']} | {r['url']}")
        if r.get("topics"):
            print(f"    Topics: {', '.join(r['topics'][:5])}")


def main():
    parser = argparse.ArgumentParser(description="Discover and clone jailbreak research repos")
    parser.add_argument("--query", help="Custom search query")
    parser.add_argument("--all", action="store_true", help="Run all default queries")
    parser.add_argument("--max", type=int, default=10, help="Max results per query")
    parser.add_argument("--clone", nargs="*", help="Clone repos by name (e.g. user/repo)")
    parser.add_argument("--clone-top", type=int, help="Clone top N repos by stars")
    parser.add_argument("--output", help="JSON output path")
    args = parser.parse_args()

    if args.clone:
        for name in args.clone:
            url = f"https://github.com/{name}.git"
            path = clone_repo(url, name)
            if path:
                print(f"  Cloned to: {path}")
        return

    if args.query:
        repos = search_repos(args.query, max_results=args.max)
    elif args.all:
        repos = scan_all(max_per_query=args.max)
    else:
        repos = scan_all(max_per_query=5)

    print_results(repos)

    if args.clone_top:
        print(f"\nCloning top {args.clone_top} repos...")
        for r in repos[:args.clone_top]:
            path = clone_repo(r["clone_url"], r["name"])
            if path:
                r["local_path"] = path

    if args.output:
        Path(args.output).write_text(json.dumps(repos, indent=2))
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
