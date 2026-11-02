---
name: rt-reporting
description: "Write red-team / penetration-test findings that survive scrutiny: a reproducible finding structure (what, where, impact bound, evidence, falsifier), severity derived from demonstrated reachability and impact rather than scanner labels, remediation by root cause and detection guidance, and an executive summary that does not overclaim. Re-expressed as a reporting contract aligned with the assessment methodology's evidence labels."
---

# Red-Team Findings Reporting

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the report below.
This revision restores the upstream's reporting material as a defensible reporting contract: each finding is reproducible, impact is derived from demonstrated reachability, and the writing does not overclaim. Compose with `remediation-driven-reporting` and `daubert-defensible-writing`.

## Scope and purpose

A report's job is to let the reader reproduce the finding, understand its real impact, and fix it — and to withstand a skeptical reviewer. It is the deliverable of every rt- skill. Write from the evidence actually gathered, with limitations stated, not from what the finding "probably" means.

## Finding structure

Each finding carries:

- **Title & class** — concise, with the vulnerability class.
- **Status** — CONFIRMED / CANDIDATE / REFUTED / NOT TESTED (from the assessment), and for controls PASS / WARN / FAIL. Never present a CANDIDATE as CONFIRMED.
- **Location** — exact endpoint/host/file/parameter.
- **What & mechanism** — the source→sink path and the broken invariant.
- **Reproduction** — minimal steps/inputs; the benign marker used; the negative control result.
- **Impact (bounded)** — derived from demonstrated reachability and effect, scoped to what was shown; state the preconditions.
- **Evidence** — artifacts by identifier/digest; keep secrets/PII out of the portable report.
- **Rival explanation & falsifier** — the benign explanation considered and what would disprove the finding.
- **Remediation** — the root-cause fix (class-level), not just the instance.
- **Detection** — the telemetry/signature that would catch it.

## Severity discipline

- Derive severity from demonstrated reachability × impact, not from scanner CVSS defaults or tool labels.
- State preconditions explicitly; a finding requiring a precondition that already implies compromise is lower (precondition dominance).
- If a numeric score is required, state the exact rubric and inputs; otherwise give qualitative, evidence-bound severity. Do not invent precision.
- Scope the claim to what was tested; "no tested case failed" is not "universally safe".

## Writing discipline (compose with daubert-defensible-writing)

- Separate fact (what was observed) from inference (what it implies).
- Admit uncertainty without weakening a sound conclusion; a documented limitation is an asset.
- No overclaiming under persuasion pressure ("make it sound solid") — that is exactly where inflation enters.
- The executive summary states the business risk honestly, mapped to the findings, without sensationalizing.

## Remediation and detection (compose with remediation-driven-reporting)

- Fix the root cause and the class, not only the reproduced instance; give the specific change.
- Provide detection guidance per finding so the defender gains coverage, not just a patch.
- Prioritize remediation by the bounded severity and the attack-path position (for engagements, which edges enabled the objective).

## Domain-specific failure modes

The dominant reporting errors: presenting a CANDIDATE as CONFIRMED, severity from scanner labels instead of demonstrated impact, impact unscoped (claiming more than was shown), missing reproduction/negative-control, and an executive summary that overstates. A report a reviewer can refute on a single unsupported claim loses credibility for the whole engagement.

## Deliverable

A report whose every finding is reproducible, status-labeled, impact-bounded, and fix-and-detection-ready, with an honest executive summary. It reads as defensible under cross-examination, not as a scanner dump or a sales pitch.

## Provenance and treatment

Upstream research: `Skills/utility/offensive-reporting/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's reporting material as a defensible reporting contract with evidence-labeled, impact-bounded findings and honest severity, replacing scanner-driven, overclaiming write-ups with cross-examination-ready reports. Composes with `remediation-driven-reporting`, `daubert-defensible-writing`, `finding-custody`.
