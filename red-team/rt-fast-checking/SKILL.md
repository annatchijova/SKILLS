---
name: rt-fast-checking
description: "A fast triage pass for security findings and leads before committing effort: a rapid checklist that classifies a candidate by source/transformation/boundary/sink/privilege, applies the benign-explanation razor, and routes it to the right domain skill or discards it. Re-expressed as a pre-flight gate that produces a CANDIDATE/REFUTED/NEEDS-TESTING disposition quickly, not a shortcut around real verification."
---

# Fast Triage Pass

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the triage below.
This revision restores the upstream's fast-checking material as a disciplined pre-flight gate: a quick pass that dispositions a lead and routes it, applying the benign-explanation razor so effort goes where it pays — not a shortcut past verification.

## Scope and use

Use this when a pile of leads (scanner output, a reported finding, a hunch) needs rapid triage before deep work. The output is a disposition per lead — discard, needs-testing, or route-to-skill — produced fast, with the benign explanation checked first.

## The fast checklist

For each lead, in order (seconds to minutes, not hours):

1. **Classify the flow.** Source (where untrusted input enters) → Transformation (what processes it) → Boundary (what trust line it crosses) → Sink (where it acts) → Privilege (what authority it reaches). A lead with no path from source to a consequential sink is low priority.
2. **Benign-explanation razor.** State the boring explanation first: already guarded, caller validates, intended/documented default, environmental not code. If the benign story accounts for all evidence, discard (REFUTED-on-sight) — do not spend deep effort.
3. **Authority check.** Does exploiting it require a precondition that already implies compromise? If so, mark low/none (precondition dominance).
4. **"Model could" vs "attacker does".** Is this "a tool could generate X" or "an attacker executes X against a real boundary"? Only the latter is a candidate.
5. **Route or defer.** If it survives, route to the domain skill (web/infra/wireless/etc.) for real verification; if ambiguous, mark NEEDS-TESTING with the one experiment that would settle it.

## Disposition outputs

- **REFUTED-on-sight** — the benign explanation holds; discard with the reason (guard present, caller validates, non-boundary, precondition-dominant).
- **CANDIDATE → route** — survives the razor; name the domain skill and the discriminating experiment.
- **NEEDS-TESTING** — cannot disposition from inspection; name the single cheapest test.

## Discipline

- Fast is not sloppy: every discard carries a one-line reason, every route carries the next experiment.
- Do not upgrade a CANDIDATE to CONFIRMED here — this gate never confirms; confirmation is the domain skill's job with a real test.
- A too-clean match (the lead fits the first guess perfectly) is a reason to look harder, not to fast-pass it.
- Rank survivors by provenance/authority (reachable, high-authority) over sink severity alone.

## Domain-specific failure modes

The two failure modes: discarding a real lead because the benign story was assumed-not-checked, and routing noise forward because the razor was skipped. Both come from treating speed as license to not reason. Scanner severity is not a disposition. A lead that needs a test should be marked NEEDS-TESTING, not guessed either way.

## Deliverable

A triaged lead list: each with its flow classification, disposition (REFUTED-on-sight / CANDIDATE→skill / NEEDS-TESTING), the one-line reason, and the next experiment for survivors. The gate's value is throughput with accountability, feeding the domain skills clean candidates.

## Provenance and treatment

Upstream research: `Skills/utility/offensive-fast-checking/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's fast-checking material as a source→sink + benign-razor pre-flight gate that dispositions and routes leads quickly without ever confirming, replacing a quick-win mindset with disciplined triage. Composes with `attack-surface-triage`, `exploitability-triage`, and every rt- domain skill it routes to.
