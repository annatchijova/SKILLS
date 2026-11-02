---
name: rt-crash-analysis
description: "Red-team / research assessment of crash exploitability: triaging a fault into non-exploitable, denial-of-service, or controllable-primitive, using faulting-instruction and register/memory-control analysis, taint/backward slicing, and heuristics in the spirit of !exploitable / exploitable.py. Re-expressed as scoped experiments on owned crashing inputs that assign a defensible exploitability verdict with explicit uncertainty instead of asserting RCE from a stack trace."
---

# Crash Exploitability Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's crash-analysis craft as a disciplined exploitability triage: it names the signals that separate a non-exploitable crash from a controllable primitive, assigning a verdict with stated uncertainty rather than overclaiming RCE.

## Scope and prerequisites

Crash triage answers: is this fault non-exploitable, a DoS, or a controllable primitive? Work on owned crashing inputs (from fuzzing or a report) against an owned binary with symbols where possible. The deliverable is a defensible verdict, not a weaponized exploit.

Declare the target, architecture, build/mitigation state, and the crash corpus, attempt budget, stop condition. Report-only input yields a hypothesis marked NOT TESTED.

## Classes of verdict

- **Non-exploitable** — NULL deref, read of unmapped data with no attacker control, pure assertion.
- **DoS** — reliable crash, no control (availability impact only).
- **Controllable primitive** — attacker controls PC, a write address/value, or object type; candidate for escalation.
- **Unknown** — insufficient evidence; needs more triage (a valid, honest verdict).

## Mechanism and observation

Trace the fault back to the attacker-controlled input and forward to what it corrupts.

**Firstness:** Record the faulting instruction, the fault type (read/write/exec), the register/memory state, and whether the faulting operand is attacker-controlled. **Secondness:** State what a benign input does at that site and the deviation. **Thirdness:** Infer the exploitability class only after control (or its absence) is demonstrated, not inferred from the signature alone.

## Abduction and refutation

**Mechanism hypothesis:** The crash reflects attacker control over a code pointer or a write primitive (exploitable).

**Competing benign explanation:** The fault is a NULL/near-NULL deref with no control; the corrupted value is bounded/non-pointer; a mitigation (canary/guard page) caught it pre-control; the crash depends on an environment artifact, not the input.

## Deduction and controls

A benign input does not fault (positive control). A confirmed controllable primitive shows attacker-controlled PC/write on the owned crash where the input directly determines the controlled value. Predeclare the control signal (e.g. "RIP = 0x41414141 from input bytes N-M"). A near-NULL fault or bounded value is evidence of non-exploitability.

## Induction: bounded laboratory procedure

Owned crashes; symbols where possible.

1. **Reproduce.** Confirm the crash is deterministic from the input; minimize the input.
2. **Characterize the fault.** Faulting instruction, access type, address, registers; is the faulting address/value derived from input?
3. **Control analysis.** Backward-slice/taint from the faulting operand to input bytes; determine controllability of PC / write-what-where / object type.
4. **Assign verdict.** Non-exploitable / DoS / controllable-primitive / unknown, with the evidence that supports it and the heuristic used.
5. **Bound, do not weaponize.** If controllable, note the primitive class and stop; escalation is `rt-exploit-development`.
6. **Mitigation context.** Note which mitigations would block escalation.

Record results including refutations. Keep the exploitability verdict separate from any control/mitigation note.

## Craft notes (leads)

Classic heuristics (Microsoft `!exploitable`, `exploitable.py`) classify by faulting-instruction and access type, but they over- and under-call — treat their label as a lead, not a verdict. Write faults near controlled addresses, PC control, and call/jmp through controlled pointers rank high; reads of unmapped memory and NULL derefs rank low. Minimization and taint make the verdict defensible.

## Domain-specific failure modes

A crash is not exploitability — the single biggest error is asserting RCE from a stack trace. Automated classifiers are noisy; corroborate with control analysis. A fault behind a mitigation may be exploitable on an unmitigated build and not otherwise — scope the verdict to the build. "Unknown" is a legitimate, honest outcome; prefer it to a false CONFIRMED.

## Evidence and deliverable

Provide the minimized input, the faulting instruction and access type, the control/taint analysis, the assigned verdict with its basis and uncertainty, and the heuristic used. Attach minimal replay, expected/observed, rival explanation, falsifier, crashes not yet triaged.

## Versions and tool limitations

Pin the architecture, build/mitigations and debugger/tooling versions. Exploitability heuristics are approximate; state their limits. No crash behavior was verified by this content; reproduce on the owned binary first.

## Remediation and detection

Fix the root-cause memory error (bounds/lifetime), add a sanitizer/fuzz regression for the crashing input, and enable mitigations that block escalation. Prioritize fixes by verdict, not by crash count. Detect repeated controllable-fault signatures in telemetry.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Taint/control analysis shows attacker-controlled PC/write on the owned crash: CONFIRMED controllable-primitive; (escalation deferred to `rt-exploit-development`). |
| Benign refutation | The fault is a near-NULL deref / bounded non-pointer value: REFUTED for exploitability; classify as DoS or non-exploitable. |
| Insufficient evidence | Controllability not established either way: UNKNOWN; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/exploit-dev/offensive-crash-analysis/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's crash-triage craft, re-expressed as a defensible exploitability verdict with explicit uncertainty and control analysis, replacing RCE-from-a-stack-trace overclaiming with a bounded, evidence-based classification. Composes with `rt-basic-exploitation`, `rt-exploit-development`, `exploitability-triage`.
