---
name: rt-shellcode
description: "Red-team / research assessment of shellcode and position-independent-payload constraints in CTF/authorized exploitation: encoding and bad-char handling, PIC/egg-hunting, size limits, syscall vs library calling, and detection surface. Re-expressed as scoped experiments on an owned target using a benign marker payload (print/callback) with detection awareness instead of weaponized shellcode for live use."
---

# Shellcode and Payload-Constraint Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiments below.
This revision restores the upstream's shellcode craft as scoped CTF/research experiments: it names the payload constraints and construction concepts, proving delivery with a benign marker on an owned target and noting detection surface, rather than shipping weaponized shellcode.

## Scope and prerequisites

Shellcode here is the final stage of an authorized exploitation exercise (CTF, research VM, owned target with a confirmed control primitive). The payload is benign — it prints a unique marker or calls an owned-collector stub — never a reverse shell or destructive action against a live system.

Declare the target, architecture, delivery context (buffer size, allowed bytes), attempt budget, stop condition. Analysis-only yields a hypothesis marked NOT TESTED.

## Constraint classes (what shapes a payload)

- **Bad characters** — bytes the delivery path mangles (NUL, newline, slash); drive encoding/alternate-instruction choices.
- **Size limits** — small buffers force staging (egg-hunting) or minimal payloads.
- **Position independence** — PIC requirements when the load address is unknown.
- **Calling convention** — direct syscalls vs library calls; architecture-specific registers.
- **Detection surface** — the payload's telemetry (process/thread/syscall patterns) as a detection target.

## Mechanism and observation

Trace the marker payload from delivery through the constraints to execution.

**Firstness:** Record whether the benign marker executed given the constraints (bad chars survived, fit the size, ran position-independently). **Secondness:** State the delivery constraints and whether the payload satisfied them. **Thirdness:** Infer "constraint satisfied / delivery viable" only after the marker runs under control.

## Abduction and refutation

**Hypothesis:** A constraint-satisfying payload reaches execution in the delivery context.

**Competing benign explanation:** A bad char corrupts the payload (it never runs); the buffer is too small and staging was not set up; the payload assumes a fixed address that ASLR randomizes; NX prevents executing the buffer (requiring ROP, not shellcode); the marker's "run" was actually the harness.

## Deduction and controls

A correctly-constrained marker runs (positive control in the lab); a constraint-violating one does not. A confirmed result runs the benign marker in the delivery context where a violating payload fails. Predeclare the marker and the constraint set. NX / bad-char mangling / size limit defeating the payload are controls to record.

## Induction: bounded laboratory procedure

Owned target; benign marker payload.

1. **Characterize constraints.** Identify bad chars (send a byte-array, see what survives), the available size, and the execution context (NX? known address?).
2. **Construct the marker.** Assemble a minimal benign payload (print/callback) satisfying the constraints; encode/avoid bad chars; make it PIC if needed.
3. **Stage if needed.** For tiny buffers, use an egg-hunter to locate a larger second-stage marker.
4. **Deliver & confirm.** Run via the exploit primitive; confirm the marker executed once; stop.
5. **Detection note.** Record the telemetry the payload would generate (for the defender).

Record results including refutations. Keep delivery-viability status separate from any mitigation control.

## Craft notes (leads)

Bad-char discovery via a full byte-array comparison is the standard first step. Encoders (and alternate instruction sequences) avoid mangled bytes; note that polymorphic encoding is also an evasion concern — here it is about surviving the delivery path, not defeating detection. Egg-hunters bridge small buffers to a staged marker. NX moves the problem to code reuse (ROP) — see `rt-exploit-development`. Architecture (x86/x64/ARM) dictates syscall numbers and registers.

## Domain-specific failure modes

A bad char silently corrupts the payload — always characterize first. NX makes shellcode-in-buffer non-executable (the finding is ROP, not shellcode). An address-dependent payload breaks under ASLR without a leak. A marker that "ran" in the harness, not the target, is a false positive. Keep the payload benign; a live reverse shell is out of scope.

## Evidence and deliverable

Provide the constraint set (bad chars, size, context), the benign marker payload, its execution confirmation, and the detection telemetry note. Keep to the owned target. Attach minimal replay, expected/observed, rival explanation, falsifier, constraints not handled.

## Versions and tool limitations

Pin architecture, OS and mitigation state — payloads are arch- and context-specific. No target behavior was verified by this content; confirm on the owned target first.

## Remediation and detection

Enable NX/DEP (shellcode-in-buffer non-executable), ASLR, and CFI; monitor for anomalous syscall sequences and RWX memory allocation. Add a regression asserting the buffer is non-executable. Detect staging/egg-hunter memory-scan patterns.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A constraint-satisfying benign marker executes in the delivery context where a violating payload fails: CONFIRMED delivery-viable (benign). |
| Benign refutation | A bad char/size/NX/ASLR prevents execution: REFUTED for this payload; record the control. |
| Insufficient evidence | Constraints characterized but no confirmed marker execution: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-shellcode/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's bad-char/size/PIC/staging craft, re-expressed as owned-target experiments with a benign marker and detection awareness, replacing weaponized shellcode with bounded delivery proof. Composes with `rt-basic-exploitation`, `rt-exploit-development`, `rt-mitigations`.
