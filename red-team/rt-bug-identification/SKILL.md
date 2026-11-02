---
name: rt-bug-identification
description: "Red-team / research assessment that turns raw fuzzing or crash output into identified, deduplicated, root-caused bugs: stack/coverage-based deduplication, minimization, root-cause localization (sanitizer reports, reverse execution, taint), and bug-class assignment. Re-expressed as scoped triage on owned crash corpora that produces a deduplicated, root-caused finding set with exploitability deferred to crash analysis."
---

# Bug Identification and Triage

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the triage below.
This revision restores the upstream's bug-identification craft as disciplined triage: it deduplicates, minimizes and root-causes a crash corpus into real bugs, deferring exploitability to `rt-crash-analysis` rather than conflating "crash" with "vulnerability".

## Scope and prerequisites

Fuzzing produces many crashes that collapse into few bugs. This skill identifies the distinct, root-caused defects. Work on owned crash corpora against an owned/symbolized target. The deliverable is a deduplicated, root-caused bug set with class labels — not exploit development.

Declare the target, the corpus source, and symbol availability, attempt budget, stop condition. Unsymbolized black-box crashes yield weaker root-cause confidence — mark it.

## Mechanism and observation

Trace each crash from the input to the root-cause code, and group crashes that share a root cause.

**Firstness:** Record the crash signature (faulting instruction, sanitizer report, stack), the minimized input, and the root-cause site. **Secondness:** State the intended behavior at that site and the deviation. **Thirdness:** Infer the bug class only after the root cause is localized, not from the stack top alone.

## Abduction and refutation

**Hypothesis:** N raw crashes correspond to M distinct bugs (M << N), each with a locatable root cause and a class.

**Competing benign explanation:** Several "distinct" crashes are the same bug at different stacks; a crash is a harness/oracle artifact; the "bug" is intended behavior under an invalid input the real caller prevents; two inputs crash at the same site for different root causes (under-dedup).

## Deduction and controls

A known-good input does not crash (positive control). A correctly identified bug has a minimized input that reliably reproduces, a localized root cause, and a class; duplicates collapse to one. Predeclare the dedup key (coverage/root-cause, not just stack-top). Reproducing the minimized input is the confirmation; a non-reproducing crash is CANDIDATE.

## Induction: bounded triage procedure

Owned corpus; symbols where possible.

1. **Reproduce & minimize.** Confirm each crash reproduces; minimize the input to the essential bytes.
2. **Deduplicate.** Group by root-cause site and coverage, not just the faulting frame (stack-top dedup over- and under-counts).
3. **Root-cause.** Use the sanitizer report (ASan/UBSan allocation/free/use sites), reverse/backward slicing, and taint to the first wrong operation — not merely where it crashed.
4. **Classify.** Assign a bug class (see `rt-vuln-classes`): OOB read/write, UAF, type confusion, integer error, uninitialized, logic.
5. **Hand off exploitability.** Route each to `rt-crash-analysis` for the exploitability verdict; do not assert it here.
6. **Record** the deduplicated, root-caused finding set.

Record results including refutations. Keep bug-identity status separate from exploitability (which this skill defers).

## Craft notes (leads)

ASan/MSan/UBSan reports give allocation and free sites directly — the fastest path to root cause. Stack-top dedup is the classic over/under-count error; dedup on the root-cause site. Minimization (afl-tmin/`-minimize`) both speeds triage and clarifies the root cause. The first wrong operation (where the invariant broke) is usually above the crash site.

## Domain-specific failure modes

The crash site is rarely the bug — root-cause above it. Stack-top dedup inflates or collapses counts. Harness/oracle artifacts masquerade as target bugs. A non-reproducing crash is not yet a bug. Assigning exploitability here (instead of deferring to `rt-crash-analysis`) is the overclaiming trap.

## Evidence and deliverable

Provide, per identified bug: the minimized reproducer, the root-cause site, the bug class, the dedup key, and a pointer to its exploitability triage. Attach expected/observed, rival explanation (dup/artifact), falsifier, crashes not yet resolved.

## Versions and tool limitations

Pin the sanitizer, compiler and triage-tool versions. Root-cause confidence depends on symbols. No target behavior was verified by this content beyond the reproductions; confirm independently.

## Remediation and detection

Fix each root cause, add the minimized reproducer as a regression test, and feed it back into the corpus. Prioritize by class and (from `rt-crash-analysis`) exploitability, not by raw crash count. Track root-cause recurrence across releases.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A minimized input reliably reproduces, root cause localized and classified: CONFIRMED bug (exploitability deferred). |
| Benign refutation | Crashes collapse to a known bug / are harness artifacts / are intended-under-invalid-input: REFUTED (dup or non-bug). |
| Insufficient evidence | A crash that does not reliably reproduce or cannot be root-caused: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/fuzzing/offensive-bug-identification/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's dedup/minimization/root-cause/classification craft, re-expressed as scoped triage over owned corpora producing a deduplicated root-caused bug set, deferring exploitability to crash analysis. Composes with `fuzz-campaign-design`, `rt-crash-analysis`, `rt-vuln-classes`, `finding-custody`.
