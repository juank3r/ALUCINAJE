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
from typing import List


TEXT_EXT = {".md", ".txt", ".json", ".csv", ".yml", ".yaml"}


def clone_repo(url: str, dest: Path) -> bool:
    try:
        subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def extract_candidates(root: Path) -> List[str]:
    candidates = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
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
    return candidates


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
    ]
    for patt in banned:
        if re.search(patt, t):
            return True
    # short heuristics: asking for explicit wrongdoing
    if re.search(r"(how to|tell me how|show me how|give me steps to)", t):
        return True
    return False


def sanitize(candidates: List[str]) -> List[str]:
    safe = []
    seen = set()
    for c in candidates:
        s = c.strip()
        if len(s) < 15:
            continue
        if is_probably_jailbreak(s):
            continue
        if s in seen:
            continue
        seen.add(s)
        safe.append(s)
    return safe


def main():
    parser = argparse.ArgumentParser(description="Clone repos and extract sanitized prompts")
    parser.add_argument("--repos", nargs="+", required=True, help="Repository URLs to import from")
    parser.add_argument("--out", default="phrases_imported_sanitized.txt", help="Output file for sanitized phrases")
    args = parser.parse_args()

    out_path = Path(args.out)
    results = []
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for i, url in enumerate(args.repos):
            repo_dir = td_path / f"repo_{i}"
            ok = clone_repo(url, repo_dir)
            if not ok:
                print(f"Warning: could not clone {url}")
                continue
            cand = extract_candidates(repo_dir)
            results.extend(cand)
    sanitized = sanitize(results)
    if not sanitized:
        print("No sanitized phrases found (or all candidates were filtered). Check repos or adjust filters.")
    out_path.write_text("\n".join(sanitized), encoding="utf8")
    print(f"Wrote {len(sanitized)} sanitized phrases to {out_path}")


if __name__ == "__main__":
    main()
