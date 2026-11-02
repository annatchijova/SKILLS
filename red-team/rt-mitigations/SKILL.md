---
name: rt-mitigations
description: "Red-team / research assessment of exploit-mitigation effectiveness: understanding and measuring KASLR, KPTI, SMAP/SMEP, PAN, stack canaries, NX/DEP, CFI/CET shadow stacks, MTE, LAM, memory sealing, KDP/HVCI and hardened usercopy, including the conditions under which each is bypassable. Re-expressed as scoped experiments on an owned target that score whether a mitigation holds against a specific primitive (PASS/WARN/FAIL) rather than delivering bypass weaponization."
---

# Exploit-Mitigation Effectiveness Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's mitigation craft as effectiveness measurement: it explains each mitigation and the precondition under which it is bypassable, scoring whether it holds against a given primitive on an owned target rather than shipping a bypass weapon. This is the defender-facing framing of the exploit-dev family.

## Scope and prerequisites

A mitigation does not make a bug unexploitable in the abstract; it raises a specific precondition (needs a leak, needs a controlled object, needs a specific primitive). The question is: against *this* primitive on *this* build, does the mitigation hold? Work on an owned target with a known primitive. The deliverable is a per-mitigation PASS/WARN/FAIL with the precondition, not a generic bypass.

Declare the target, architecture, and enabled mitigations, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mitigation surface (and the precondition each needs to bypass)

- **ASLR/KASLR** — bypassed only with an info leak (or low entropy / brute on 32-bit).
- **NX/DEP** — forces code reuse (ROP/JOP) instead of injected shellcode.
- **Stack canary** — bypassed by a canary leak, a brute (forking servers), or a write that skips it.
- **CFI / CET** — distinct controls. CFI constrains selected control-flow transfers according to its policy; Intel CET includes shadow stack for return integrity and Indirect Branch Tracking (IBT) for selected indirect branches. Do not treat either as a universal ROP/JOP blocker; state architecture, enabled feature and protected transfer type.
- **SMAP/SMEP/PAN** — block kernel use of user pages; bypass needs a kernel-space primitive or ret2dir-class.
- **KPTI** — isolates page tables (Meltdown-era); bypass is side-channel/implementation-specific.
- **MTE** — architecture-specific memory tagging that detects selected tag mismatches under the configured mode; assess tag knowledge, coverage and fault behavior. **Intel LAM** exposes selected upper pointer bits for software metadata and masks them for address translation; it is not a memory-safety mitigation equivalent to MTE. Do not score LAM as a mitigation that blocks memory corruption without a specific software policy using it.
- **KDP / HVCI (Memory Integrity), memory sealing, RODATA, hardened usercopy** — protect specific structures; bypass needs a primitive outside the protected set.

## Mechanism and observation

Pair the primitive with the mitigation and test whether the precondition for bypass is reachable.

**Firstness:** Record whether the mitigation stopped the step (abort, non-control) or the bypass precondition was met (leak obtained, CFI-valid chain ran). **Secondness:** State what the mitigation is designed to prevent and the observed deviation. **Thirdness:** Infer "mitigation ineffective against this primitive" only after the bypass precondition is demonstrably met under control.

## Abduction and refutation

**Mechanism hypothesis:** The available primitive satisfies the precondition that bypasses the mitigation (e.g. an OOB read provides the ASLR leak).

**Competing benign explanation:** No leak is available so ASLR holds; CET rejects the chain; the canary cannot be leaked; MTE tags are not leakable; the primitive is outside the protected structure set so KDP/HVCI is irrelevant (and the mitigation is effective for this primitive).

## Deduction and controls

With the precondition met the step succeeds; without it the mitigation holds. A confirmed "ineffective" result shows the bypass precondition met on the owned target where a configuration lacking that precondition blocks it. Predeclare the precondition and the success signal. The mitigation blocking the step (no reachable precondition) is a PASS/WARN.

## Induction: bounded laboratory procedure

Owned target; benign marker.

1. **Inventory.** Enumerate enabled mitigations (`checksec`, kernel config) and the available primitive.
2. **Pair & hypothesize.** For each relevant mitigation, state the precondition a bypass needs.
3. **Test the precondition.** Attempt only to meet the precondition (obtain a leak, find a CFI-valid gadget) and reach the benign marker; stop there.
4. **Score.** PASS (mitigation holds, precondition unreachable), WARN (precondition partially reachable / unverified), FAIL (precondition met, mitigation bypassed for this primitive).
5. **Control.** Compare against a configuration where the precondition is removed.

Record results including refutations. Keep finding status separate from the per-mitigation control score.

## Craft notes (leads)

The recurring theme: modern mitigations convert "bug" into "bug + required precondition." ASLR needs a leak; NX needs code reuse; CET needs a shadow-stack gap; MTE needs a tag leak. Document the precondition, because the mitigation's effectiveness is exactly whether that precondition is reachable with the available primitive.

## Domain-specific failure modes

Claiming a mitigation is "bypassed" in general is wrong — bypass is always relative to a primitive and a precondition. A mitigation irrelevant to the primitive class (e.g. KDP when the target is unprotected) is neither PASS nor FAIL for that primitive; say so. Reaching the marker proves the precondition; going further is out of scope.

## Evidence and deliverable

Provide the primitive, each mitigation, its bypass precondition, whether the precondition was met, and the PASS/WARN/FAIL. Keep work on the owned target. Attach minimal replay, expected/observed, rival explanation, falsifier, mitigations not assessed.

## Versions and tool limitations

Pin architecture, kernel/compiler and mitigation versions — effectiveness is version- and config-specific (e.g. CET availability, MTE mode). No mitigation behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

Enable applicable mitigations supported by the target architecture, operating system and workload (for example ASLR, NX, canaries, RELRO, a specified CFI/CET feature, MTE where supported, HVCI/KDP or hardened usercopy where applicable), and eliminate preconditions such as reachable information leaks. Treat LAM as pointer-metadata support unless the target software uses it in a defined security policy; do not present it as a drop-in memory-safety mitigation. Add a regression asserting the precondition remains unreachable. Detect leak primitives and code-reuse execution.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A bypass precondition is met on the owned target, reaching the marker, where removing it blocks the step: CONFIRMED mitigation-ineffective-for-this-primitive; control FAIL. |
| Benign refutation | No reachable precondition (no leak / CET holds / no tag leak): REFUTED; control PASS. |
| Insufficient evidence | Precondition partially reachable, not demonstrated: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/exploit-dev/offensive-mitigations/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's mitigation catalog and bypass-precondition knowledge, re-expressed as owned-target effectiveness measurement scored PASS/WARN/FAIL per primitive, replacing bypass weaponization with precondition-reachability assessment. Composes with `rt-exploit-development`, `rt-basic-exploitation`, `control-effectiveness-vs-existence`.
