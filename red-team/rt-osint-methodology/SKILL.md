---
name: rt-osint-methodology
description: "Methodology for disciplined OSINT in an authorized engagement: scoping and legal/ethical boundaries, the collection cycle (plan, collect, process, corroborate, analyze, report), source reliability grading, provenance and freshness tracking, and privacy minimization. Re-expressed as a process contract that governs rt-osint collection with explicit source-evaluation and scope limits rather than a tool list."
---

# OSINT Methodology

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract across the collection cycle below.
This revision restores the upstream's OSINT-methodology material as a process contract: it governs how `rt-osint` collection is planned, corroborated, graded and bounded, rather than listing tools. Compose with `intel-source-evaluation` and `claim-provenance-discipline`.

## Scope and prerequisites

Methodology turns raw collection into a defensible intelligence picture. Carry the engagement's authorization and legal boundary; collect only what the objective needs; respect privacy for individuals. Every datum carries a source, a reliability grade, and a timestamp.

Declare the intelligence requirements (what the engagement needs to know), the authorized sources, and the privacy/legal boundary before collecting.

## The collection cycle

1. **Plan.** Derive specific intelligence requirements from the engagement objective; identify authorized sources; set the passive/active boundary.
2. **Collect.** Gather from `rt-osint` surfaces, recording provenance and timestamp per datum.
3. **Process.** Normalize, deduplicate, and structure (asset inventory, relationships).
4. **Corroborate.** Confirm each significant datum across independent sources; flag single-source claims.
5. **Analyze.** Build the picture (attack surface, relationships) and the gaps; separate fact from inference.
6. **Report.** Deliver with provenance, reliability grades, freshness, and scope/privacy notes; feed `attack-surface-triage`.

## Source reliability grading

Grade each source and each datum (in the spirit of an admiralty-style scale): source reliability (reliable → unreliable) and information credibility (confirmed → doubtful). Record both. A high-confidence claim needs a reliable source and corroboration; a single doubtful source is a lead, not a fact.

## Method discipline

Run the cycle through the methodology: observe the datum (Firstness), compare to the expected/known baseline (Secondness), infer the intelligence conclusion (Thirdness); and refute the benign explanation (stale record, misattribution, intentional publication) before asserting an exposure. Use CANDIDATE/CONFIRMED/REFUTED/NOT TESTED for intelligence claims, with the source grade attached.

## Provenance and freshness (compose with claim-provenance-discipline)

- Every datum: source, collection method, timestamp.
- Recon data ages — mark live-vs-historical and re-confirm before acting.
- Never launder a single unverified source into a confident claim; the grade travels with the datum into the report.

## Privacy and legal boundary

- Collect the minimum personal data the objective requires; prefer organizational over individual data.
- Stay within the authorized sources and the passive/active boundary; unauthorized active collection is out of scope.
- Document the boundary honored in the report.

## Domain-specific failure modes

The dominant errors: single-source confidence (no corroboration), stale data treated as live, misattribution across shared infrastructure, and scope/privacy creep (collecting individuals' data beyond need). Treating OSINT output as fact without grades and provenance makes downstream decisions unaccountable.

## Deliverable

A graded, provenance-tracked intelligence product: the requirements, the corroborated findings with source grades and freshness, the gaps, and the scope/privacy boundary honored. The output drives `attack-surface-triage`; it is not raw dumps.

## Provenance and treatment

Upstream research: `Skills/recon/offensive-osint-methodology/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's OSINT-process material as a collection-cycle contract with source grading, provenance/freshness and privacy minimization, replacing a tool list with a defensible methodology. Composes with `rt-osint`, `intel-source-evaluation`, `claim-provenance-discipline`, `attack-surface-triage`.
