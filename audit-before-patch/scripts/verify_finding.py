#!/usr/bin/env python3
"""
verify_finding.py — Gate an audit finding against the LIVE file before patching.

A finding is a claim. This checks the claim against the current file on disk and
classifies it, so a stale or fragment-based false positive never becomes a patch:

  VERIFIED    anchor present exactly once — safe to investigate the claim and,
              if the bug is real in context, patch surgically.
  UNVERIFIED  anchor absent — the finding is stale or imagined; do NOT patch.
  AMBIGUOUS   anchor appears more than once — resolve which site before patching.

It prints the surrounding context so a human can compare claimed-vs-actual.
It never modifies anything; it only gates the decision to.

CLI:
    python verify_finding.py <file> "<anchor>" ["<claim>"]
Library:
    from verify_finding import verify_finding
    verdict = verify_finding("pipeline.py", "except: pass", "swallows errors")
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict


def verify_finding(file: str, anchor: str, claim: str = "", context_lines: int = 4) -> Dict:
    path = Path(file)
    if not path.exists():
        return {
            "status": "UNVERIFIED",
            "reason": f"file does not exist: {file} (finding is stale or misattributed)",
            "occurrences": 0,
        }

    text = path.read_text(encoding="utf-8", errors="replace")
    count = text.count(anchor)

    if count == 0:
        status, reason = "UNVERIFIED", (
            "anchor not found in live file — finding is stale (file changed) or "
            "the auditor reasoned over a fragment/snapshot. Do NOT patch."
        )
    elif count > 1:
        status, reason = "AMBIGUOUS", (
            f"anchor appears {count} times — the finding does not say which. "
            "Resolve the exact site before patching."
        )
    else:
        status, reason = "VERIFIED", (
            "anchor present exactly once. Now read the surrounding logic and "
            "confirm the bug is REAL in context (no existing guard, default not "
            "intentional) before applying a surgical patch."
        )

    # Show context around the first occurrence for claimed-vs-actual comparison.
    contexts = []
    if count >= 1:
        lines = text.splitlines()
        joined = "\n".join(lines)
        idx = joined.find(anchor)
        line_no = joined[:idx].count("\n")
        lo = max(0, line_no - context_lines)
        hi = min(len(lines), line_no + context_lines + 1)
        contexts = [(i + 1, lines[i]) for i in range(lo, hi)]

    return {
        "status": status,
        "reason": reason,
        "occurrences": count,
        "claim": claim,
        "context": contexts,
    }


def _print(v: Dict) -> None:
    print(f"STATUS: {v['status']}  (occurrences: {v['occurrences']})")
    if v.get("claim"):
        print(f"CLAIM : {v['claim']}")
    print(f"REASON: {v['reason']}")
    if v.get("context"):
        print("CONTEXT (live file — compare against the claim):")
        for n, line in v["context"]:
            print(f"  {n:>5}\u2502 {line}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(1)
    verdict = verify_finding(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    _print(verdict)
    # Exit non-zero unless VERIFIED, so this can gate a patch script in a pipeline.
    raise SystemExit(0 if verdict["status"] == "VERIFIED" else 2)
