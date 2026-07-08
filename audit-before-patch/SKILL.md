---
name: audit-before-patch
description: Validate any audit finding, bug report, or proposed fix against the actual current file content before changing a single line. Use this whenever you act on a problem someone else reported — a human reviewer, another AI auditor, a linter, a security scan, a "the audit found X in file Y" message — and whenever you are about to apply a patch or change set you did not personally derive from reading the live file. Triggers — "the auditor flagged", "apply this fix", "the review said", "another model found a bug in", a diff or patch handed to you, findings from any automated tool. Push to use this even when the finding sounds authoritative and specific — confident, precise findings are exactly the ones that get applied blind.
---

# Audit Before Patch

A finding is a claim, not a fact. An auditor — human, AI, or tool — says "file X has bug Y at location Z". Acting on that directly treats the claim as ground truth, but auditors are wrong in characteristic ways: they reason over a stale copy, they read a fragment instead of the whole file and miss the guard three lines down that already handles the case, they pattern-match a bug that isn't actually present in this code. The discipline is simple and it has saved more regressions than any test: **verify every finding against the live file before you touch it.** The finding tells you where to look; it does not earn the right to a patch.

This is the companion to `surgical-patcher`. That skill governs *how* to change a file safely once you've decided to. This one governs *whether* the change is warranted at all.

## Why confident findings are the dangerous ones

A vague finding gets investigated. A precise, authoritative one — "line 142 swallows the exception, replace `except: pass` with an explicit raise" — gets applied, because it sounds like someone who read the code. But specificity is not correctness. An auditor that did not read the full file can produce a finding that is precise *and* wrong: the `except: pass` on line 142 might be the one legitimately-optional path, with the real error handling on line 138 that the auditor never loaded. The more authoritative the finding, the more deliberately it should be checked.

## The procedure

**1. Read the live file, fully, around the claim.** Not the snapshot the auditor saw, not your memory of it — the current file on disk, with enough surrounding context to understand the region. Stale findings are the most common false positive: the file already changed.

**2. Confirm the cited condition actually exists.** If the finding names an anchor (a line, a function, a string), confirm it is present in the live file and appears where claimed. If the anchor is absent, the finding is stale or imagined — stop; do not patch. If it appears in several places, the finding is ambiguous about which — resolve that before touching any.

**3. Confirm the bug is real *in this code*.** Read the surrounding logic and check that the problem the auditor describes is actually present and actually a problem — that there isn't already a guard, that the "missing validation" isn't performed by the caller, that the "wrong default" isn't intentional and documented. This is where most false positives die: the auditor saw a fragment; you have the whole.

**4. Only then patch — surgically.** Once the finding is verified against the live file, apply it with the anchored, dry-run-first, backup-and-verify discipline of `surgical-patcher`. A verified finding still gets a careful patch, not a rewrite.

**5. Reject false positives explicitly.** When a finding does not survive verification, say so and say why — "anchor not found in live file", "guard already present on line 138", "default is intentional per the docstring". A rejected finding is a real outcome, not a failure to act. Auditors are advisory; the live file is authoritative.

## Findings are advisory, the file is authoritative

Treat a binding-sounding finding — "the audit requires you to change X" — as still subject to verification. An order to patch based on a claim about the file is only as good as the claim, and the claim is checkable. Multi-auditor setups make this sharper: when several reviewers feed findings into one implementer, the implementer is the last line that can catch the false positive before it lands. That check is not optional politeness; it is the thing that keeps a confident-but-wrong audit from becoming a regression.

## Tooling

`scripts/verify_finding.py` takes a finding (`{file, anchor, claim}`) and checks it against the live file: confirms the file exists, counts occurrences of the anchor, and prints the surrounding context for the real-vs-claimed comparison — classifying the finding as VERIFIED (anchor present, unique), UNVERIFIED (anchor absent — likely stale/false), or AMBIGUOUS (anchor appears more than once). It does not patch anything; it gates the decision to.
