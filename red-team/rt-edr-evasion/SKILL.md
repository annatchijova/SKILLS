---
name: rt-edr-evasion
description: "Blue/purple-team assessment of EDR/telemetry detection coverage: understanding evasion categories (unhooking, direct/indirect syscalls, AMSI/ETW tampering, process injection variants, LOLBins) so defenders can detect them, and measuring whether the EDR detects an authorized emulation in a lab. Re-expressed as a detection-coverage exercise scored PASS/WARN/FAIL with a sanctioned emulation profile, not an evasion how-to for defeating a third party's EDR."
---

# EDR Detection-Coverage Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the detection exercise below.
This revision reframes the upstream's EDR-evasion material toward detection coverage: it names evasion categories so a defender can recognize them and measures whether the EDR catches an authorized emulation in a lab. It is a purple-team coverage exercise, not instructions for defeating someone else's EDR. Compose with `purple-team-exercise` and `detection-engineering`.

## Scope and prerequisites

The question is defensive: which evasion categories does the EDR catch, and where are the telemetry blind spots? Emulate only with a sanctioned profile on an owned lab host, defender informed. Do not run these to disable or bypass protection on a system you do not own; the deliverable is detection coverage, not a bypass.

Declare the lab host, EDR product/version, the emulation profile, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Evasion categories (as detection targets)

- **Userland unhooking** — restoring clean ntdll; detectable by image-load/integrity telemetry and kernel callbacks.
- **Direct/indirect syscalls** — bypassing userland hooks; detectable by kernel-level ETW/Threat-Intelligence providers and call-stack anomalies.
- **AMSI/ETW tampering** — patching in-process telemetry; detectable by integrity checks and the tampering event itself.
- **Process injection** — CreateRemoteThread, APC, process hollowing, mapping; detectable by cross-process memory/thread telemetry.
- **LOLBins** — living-off-the-land binaries; detectable by command-line and parent-child anomaly analysis.

## Mechanism and observation

Emulate one category, then measure which telemetry source detected it.

**Firstness:** Record what the emulated action did and which EDR telemetry/alert fired. **Secondness:** State the expected detection (kernel callback, ETW-TI, integrity alert) and the deviation. **Thirdness:** Infer a coverage gap only after an emulated category evades the sources that should catch it, under control.

## Abduction and refutation

**Hypothesis:** A given evasion category produces activity the EDR does not detect (a telemetry blind spot).

**Competing benign explanation:** Kernel-level telemetry (callbacks, ETW-TI) catches it despite userland evasion; the AMSI/ETW patch is itself detected; behavioral analytics flag the injection/LOLBin; the emulation did not actually run as intended; the profile is unrealistic.

## Deduction and controls

Normal activity produces no evasion alert (positive control = no false positive). A confirmed gap shows an emulated category undetected by any source where a tuned EDR would catch it. Predeclare the telemetry signal. Kernel-callback / ETW-TI / integrity / behavioral detection catching it are PASS controls.

## Induction: bounded purple-team procedure

Owned lab host; sanctioned profile; defender informed.

1. **Baseline.** Run normal workload; confirm no false alerts and capture telemetry.
2. **Emulate one category** with the sanctioned profile.
3. **Measure per source.** Userland hook, kernel callback, ETW/ETW-TI, image-load, behavioral — which detected it?
4. **Score coverage.** PASS/WARN/FAIL per category and per telemetry source.
5. **Tune and re-test.** Add detections (kernel telemetry, call-stack analysis, integrity monitoring) for gaps; confirm closure.
6. **Control.** Confirm normal workload still does not alert.

Record results including refutations. Keep finding status separate from the per-source coverage score.

## Craft notes (leads)

The durable lesson: userland-only telemetry is evadable, so coverage depends on kernel-level sources (callbacks, ETW-TI) and behavioral analytics that survive unhooking and syscall tricks. AMSI/ETW patching is itself a high-signal event. Injection variants share cross-process telemetry signatures. LOLBins need command-line/parent-child analytics, not file signatures.

## Domain-specific failure modes

An undetected emulation may be an unrealistic profile, not a real gap. Kernel telemetry can catch what userland evasion defeats — score per source. Behavioral detection may fire late (WARN) rather than not at all. A false positive on normal activity is its own finding. The goal is coverage; actually disabling protection is out of scope.

## Evidence and deliverable

Provide the emulated category, the telemetry sources that did/did not detect it, the coverage score, and the tuning that closed gaps. Keep to the owned lab; share with the defender. Attach minimal replay, expected/observed, rival explanation (unrealistic profile), falsifier, categories not assessed.

## Versions and tool limitations

Pin the EDR product/version, the OS build and the emulation profile — detection is product- and version-specific. No EDR behavior was verified by this content; reproduce on the lab first.

## Remediation and detection

Prefer kernel-level and ETW-TI telemetry, monitor AMSI/ETW integrity, deploy behavioral analytics for injection and LOLBins, and alert on ntdll integrity/unhooking. Add detections per gap and a regression that the emulated category now alerts. Defense in depth: assume userland telemetry can be evaded.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A sanctioned emulated category goes undetected across sources where a tuned EDR would catch it: CONFIRMED coverage gap; control FAIL. |
| Benign refutation | Kernel/ETW-TI/behavioral telemetry detects it (or the profile was unrealistic): REFUTED; control PASS. |
| Insufficient evidence | Late/partial detection or unvalidated profile: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-edr-evasion/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's EDR-evasion categories as a defender-facing detection-coverage exercise with a sanctioned emulation profile and PASS/WARN/FAIL scoring, replacing an evasion how-to with telemetry blind-spot measurement. Composes with `purple-team-exercise`, `detection-engineering`, `rt-c2-frameworks`.
