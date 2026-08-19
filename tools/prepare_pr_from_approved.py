#!/usr/bin/env python3
"""Append approved phrases to `phrases_seed.txt` and prepare a branch for PR.

Usage:
  python tools/prepare_pr_from_approved.py --approved approved_phrases.txt

The script will:
 - Read approved phrases file (one phrase per line)
 - Compare with existing `phrases_seed.txt` and append only new lines
 - Create a git branch named `chore/imported-phrases-<timestamp>` and commit the change
 - Print the git push and PR commands to run locally (requires git auth)

Run the printed commands to push and open a PR.
"""

import argparse
import datetime
import subprocess
from pathlib import Path


BASE = Path(__file__).parent
SEED = BASE.parent / "phrases_seed.txt"


def read_lines(p: Path):
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text(encoding="utf8").splitlines() if l.strip() and not l.strip().startswith("#")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--approved", required=True, help="File with approved phrases (one per line)")
    args = parser.parse_args()

    approved_p = Path(args.approved)
    if not approved_p.exists():
        print(f"Approved file not found: {approved_p}")
        return

    seed_lines = read_lines(SEED)
    approved_lines = [l for l in read_lines(approved_p) if l]

    new_lines = [l for l in approved_lines if l not in seed_lines]
    if not new_lines:
        print("No new phrases to add.")
        return

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    branch = f"chore/imported-phrases-{timestamp}"

    # Create branch
    subprocess.run(["git", "checkout", "-b", branch], check=True)

    # Append new lines to seed file
    with SEED.open("a", encoding="utf8") as f:
        for l in new_lines:
            f.write(l.rstrip() + "\n")

    subprocess.run(["git", "add", str(SEED)], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: add {len(new_lines)} approved imported phrases"], check=True)

    print("Branch prepared:", branch)
    print("Next steps: push and create PR (run these commands locally):")
    print()
    print(f"git push -u origin {branch}")
    print(f"gh pr create --title 'chore: add approved imported phrases' --body 'Imported + sanitized prompts (reviewed)' --base main --head {branch}")


if __name__ == '__main__':
    main()
