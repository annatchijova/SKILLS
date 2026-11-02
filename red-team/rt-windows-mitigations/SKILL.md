---
name: rt-windows-mitigations
description: "Red-team / research assessment of Windows exploit-mitigation effectiveness: Control Flow Guard (CFG), xFG, CET/shadow stack, Arbitrary Code Guard (ACG), Code Integrity Guard (CIG), DEP/ASLR/high-entropy ASLR, CFG-aware heap, EAF/IAF and HVCI/Credential Guard, including the precondition each needs to be bypassed. Re-expressed as scoped experiments on an owned Windows target that score whether a mitigation holds against a given primitive (PASS/WARN/FAIL) rather than delivering bypasses."
---

# Windows Exploit-Mitigation Effectiveness Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiments below.
This revision restores the upstream's Windows-mitigation craft as effectiveness measurement: it explains each mitigation and the precondition under which it is bypassable, scoring whether it holds against a given primitive on an owned target rather than shipping a bypass. This is the Windows counterpart to `rt-mitigations`.

## Scope and prerequisites

As with all mitigations, a Windows mitigation raises a specific precondition for bypass (an indirect-call gadget for CFG, a shadow-stack gap for CET, a data-only path for ACG). The question is: against this primitive on this build, does the mitigation hold? Work on an owned Windows target with a known primitive. Deliverable: per-mitigation PASS/WARN/FAIL with the precondition.

Declare the Windows build, the enabled mitigations, the primitive, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mitigation surface (and bypass precondition)

- **DEP/ASLR/HEASLR** — code reuse + an info leak needed (as elsewhere).
- **CFG / xFG** — guards indirect calls; bypass needs a CFG-valid target, a non-guarded call site, or a data-only/return-based path (CFG does not protect returns — hence CET).
- **CET / shadow stack** — protects returns; bypass needs a shadow-stack gap or a non-CET module.
- **ACG (Arbitrary Code Guard)** — no new executable memory; forces data-only/ROP (no dynamic codegen).
- **CIG (Code Integrity Guard)** — only signed images load; bypass needs a signed-but-vulnerable module or a non-image path.
- **EAF/IAF** — export/import address filtering (EMET-lineage); complicates address resolution.
- **CFG-aware heap, HVCI, Credential Guard** — structure/credential protections; bypass needs a primitive outside the protected set.

## Mechanism and observation

Pair the primitive with the mitigation and test whether the bypass precondition is reachable.

**Firstness:** Record whether the mitigation stopped the step (guard check failure, non-execution) or the precondition was met (CFG-valid chain ran, leak obtained). **Secondness:** State what the mitigation prevents and the deviation. **Thirdness:** Infer "ineffective against this primitive" only after the precondition is met, under control.

## Abduction and refutation

**Hypothesis:** The available primitive satisfies the precondition that bypasses the Windows mitigation.

**Competing benign explanation:** CFG/xFG rejects the indirect call; CET catches the return; ACG blocks new code so shellcode cannot run; CIG blocks the unsigned module; no info leak so ASLR holds; the primitive is outside HVCI/Credential-Guard's protected set so those are irrelevant (and the relevant mitigation is effective).

## Deduction and controls

With the precondition met the step succeeds; without it the mitigation holds. A confirmed "ineffective" result meets the precondition on the owned target where a config lacking it blocks the step. Predeclare the precondition and the success signal (benign marker). The mitigation blocking the step is a PASS/WARN.

## Induction: bounded laboratory procedure

Owned Windows target; benign marker.

1. **Inventory.** Enumerate enabled mitigations (process mitigation policy) and the primitive.
2. **Pair & hypothesize.** For each relevant mitigation, state the precondition a bypass needs.
3. **Test the precondition.** Attempt only to meet it (obtain a leak, find a CFG-valid/non-guarded call site, a data-only path) and reach a benign marker; stop.
4. **Score.** PASS (precondition unreachable), WARN (partial/unverified), FAIL (precondition met, mitigation bypassed for this primitive).
5. **Control.** Compare against a build where the precondition is removed.

Record results including refutations. Keep finding status separate from the per-mitigation control score.

## Craft notes (leads)

CFG protects forward-edge (indirect calls) but not returns — CET/shadow stack covers returns; together they constrain ROP/JOP heavily. ACG forbids dynamic codegen, pushing toward data-only exploitation. CIG requires signed modules — a signed-but-vulnerable module is the usual precondition. The recurring theme: each mitigation converts "bug" into "bug + required precondition"; document the precondition.

## Domain-specific failure modes

Claiming a Windows mitigation is "bypassed" in general is wrong — bypass is relative to a primitive and precondition. A mitigation irrelevant to the primitive (HVCI when the target is user-mode data-only) is neither PASS nor FAIL for it. Reaching the benign marker proves the precondition; going further is out of scope.

## Evidence and deliverable

Provide the primitive, each mitigation, its bypass precondition, whether it was met, and the PASS/WARN/FAIL. Keep to the owned target. Attach minimal replay, expected/observed, rival explanation, falsifier, mitigations not assessed.

## Versions and tool limitations

Pin the Windows build and per-process mitigation policy — availability (CET, HVCI) and behavior are version- and hardware-specific. No Windows behavior was verified by this content; confirm the live config first.

## Remediation and detection

Enable the full policy (CFG + xFG, CET/shadow stack, ACG, CIG, HEASLR, EAF/IAF, HVCI, Credential Guard) per process where supported, and eliminate info leaks that unlock bypasses. Add a regression asserting the precondition stays unreachable. Detect leak primitives and code-reuse/data-only execution patterns.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A bypass precondition is met on the owned target (benign marker reached) where removing it blocks the step: CONFIRMED mitigation-ineffective-for-this-primitive; control FAIL. |
| Benign refutation | CFG/CET/ACG/CIG/no-leak prevents the step: REFUTED; control PASS. |
| Insufficient evidence | Precondition partially reachable, not demonstrated: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-windows-mitigations/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's CFG/CET/ACG/CIG/HVCI catalog and bypass-precondition knowledge, re-expressed as owned-target effectiveness measurement scored PASS/WARN/FAIL per primitive, replacing bypass weaponization with precondition-reachability assessment. Composes with `rt-mitigations`, `rt-exploit-development`, `rt-windows-boundaries`, `control-effectiveness-vs-existence`.
