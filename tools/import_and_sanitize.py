#!/usr/bin/env python3
"""Import and sanitize prompts from external repositories.

This tool clones given GitHub repos into a temp folder, extracts candidate
prompt lines from text-like files, and writes a sanitized output that
EXCLUDES phrases likely to be jailbreaks or instructions to evade safety.

Usage:
  python tools/import_and_sanitize.py --repos <url1> <url2> --out imported_safe.txt

IMPORTANT: This script intentionally filters out unsafe/jailbreak content.
Review `imported_safe.txt` before adding to `phrases_seed.txt`.
"""

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
import json
from typing import List, Tuple


TEXT_EXT = {".md", ".txt", ".json", ".csv", ".yml", ".yaml"}


def clone_repo(url: str, dest: Path) -> bool:
    try:
        subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def extract_candidates(root: Path) -> Tuple[List[str], int]:
    """Extract candidate prompt lines. Returns (candidates, files_scanned)."""
    candidates = []
    files_scanned = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
            files_scanned += 1
            try:
                text = p.read_text(encoding="utf8", errors="ignore")
            except Exception:
                continue
            # remove code fences and long code blocks
            text = re.sub(r"```.*?```", "\n", text, flags=re.S)
            # split by double newlines or lines
            parts = re.split(r"\n\s*\n", text)
            for part in parts:
                s = part.strip()
                if not s:
                    continue
                # take reasonably short paragraphs (candidate prompts)
                if 10 <= len(s) <= 600:
                    # remove inline URLs
                    s = re.sub(r"https?://\S+", "", s)
                    # collapse whitespace
                    s = re.sub(r"\s+", " ", s).strip()
                    candidates.append(s)
    return candidates, files_scanned


def is_probably_jailbreak(text: str) -> bool:
    t = text.lower()
    # keywords and patterns that suggest jailbreak/payloads
    banned = [
        "jailbreak",
        "bypass",
        "evad",
        "ignore (instructions|safety|previous)",
        "disable",
        "override",
        "roleplay",
        "pretend",
        "you are now",
        "assistant should",
        "do not follow",
        "how to (?:bypass|disable|evade)",
        "step by step",
        "exploit",
        "payload",
        # jailbreak techniques observed in the upstream repos
        "push prompt",
        "prepend",
        "append",
        "inject",
        "system prompt",
        "no restrictions",
        "without restrictions",
        "unfiltered",
        "unrestricted",
        "act as (?:dan|eni|an? ai)",
        "do anything now",
        "developer mode",
        # explicit / NSFW markers (unsafe for a shared corpus)
        "nsfw",
        "hardcore",
        "explicit",
        "erotic",
        "porn",
        "sexual",
        "seductive",
    ]
    for patt in banned:
        if re.search(patt, t):
            return True
    # short heuristics: asking for explicit wrongdoing
    if re.search(r"(how to|tell me how|show me how|give me steps to)", t):
        return True
    return False


def sanitize(candidates: List[str]) -> Tuple[List[str], dict]:
    """Filter candidates. Returns (safe_phrases, stats)."""
    safe = []
    seen = set()
    stats = {"candidates": len(candidates), "dropped_short": 0,
             "dropped_jailbreak": 0, "dropped_duplicate": 0}
    for c in candidates:
        s = c.strip()
        if len(s) < 15:
            stats["dropped_short"] += 1
            continue
        if is_probably_jailbreak(s):
            stats["dropped_jailbreak"] += 1
            continue
        if s in seen:
            stats["dropped_duplicate"] += 1
            continue
        seen.add(s)
        safe.append(s)
    stats["kept"] = len(safe)
    return safe, stats


def main():
    parser = argparse.ArgumentParser(description="Clone repos and extract sanitized prompts")
    parser.add_argument("--repos", nargs="+", required=True, help="Repository URLs to import from")
    parser.add_argument("--out", default="phrases_imported_sanitized.txt", help="Output file for sanitized phrases")
    args = parser.parse_args()

    out_path = Path(args.out)
    results = []
    per_repo = []
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for i, url in enumerate(args.repos):
            repo_dir = td_path / f"repo_{i}"
            ok = clone_repo(url, repo_dir)
            if not ok:
                print(f"Warning: could not clone {url}")
                per_repo.append({"url": url, "cloned": False,
                                 "files_scanned": 0, "candidates": 0})
                continue
            cand, files_scanned = extract_candidates(repo_dir)
            per_repo.append({"url": url, "cloned": True,
                             "files_scanned": files_scanned,
                             "candidates": len(cand)})
            results.extend(cand)
    sanitized, stats = sanitize(results)
    if not sanitized:
        print("No sanitized phrases found (or all candidates were filtered). Check repos or adjust filters.")
    out_path.write_text("\n".join(sanitized), encoding="utf8")
    print(f"Wrote {len(sanitized)} sanitized phrases to {out_path}")

    # Emit a metadata summary alongside the sanitized output (feeds docs/DATA_SOURCES.md)
    summary = {
        "repos": len(args.repos),
        "repos_detail": per_repo,
        "files_scanned": sum(r["files_scanned"] for r in per_repo),
        "totals": stats,
        "output": str(out_path),
    }
    summary_path = out_path.with_name(out_path.stem + ".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf8")
    print(f"Wrote metadata summary to {summary_path}")


if __name__ == "__main__":
    main()
