---
name: rt-anti-forensics
description: "Blue/purple-team assessment of forensic-integrity controls and anti-forensic detectability: whether timestomping, log tampering/clearing, artifact wiping and secure-deletion attempts are detected, attributable and recoverable. Re-expressed as a detection-and-recovery measurement on an owned lab host that emulates anti-forensic actions under authorization and scores whether logging/EDR/forensic controls hold, rather than teaching evidence destruction."
---

# Forensic-Integrity and Anti-Forensic-Detectability Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the detection measurement below.
This revision reframes the upstream's anti-forensics material toward its defensive purpose: understanding the techniques to detect them and to measure whether forensic-integrity controls hold. It emulates anti-forensic actions on an owned lab host to score detection and recovery, and does not provide an evidence-destruction playbook. Compose with `forensic-logging-design` and `detection-engineering`.

## Scope and prerequisites

The question is defensive: if an adversary tried to hide activity, would the environment detect it, attribute it, and recover the evidence? Emulate the actions only on an owned, instrumented lab host that you are authorized to tamper with, with central logging in place. Never run these to hide activity on a system you do not own, and never to impede an actual investigation.

Declare the lab host, the logging/EDR stack, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Technique classes (as detection targets)

- **Timestomping** — altering MACB timestamps; detectable via `$STANDARD_INFORMATION` vs `$FILE_NAME` discrepancy, journal records.
- **Log tampering/clearing** — clearing or editing event logs; detectable via clear events (e.g. 1102/104), central-log gaps, sequence-number breaks.
- **Artifact wiping** — removing prefetch, shellbags, browser/history, bash history; detectable via absence-where-presence-is-expected and backups.
- **Secure deletion** — overwriting files; detectable via slack/journal/shadow-copy remnants and central telemetry already shipped off-host.
- **Tooling/process hiding** — detectable via EDR process telemetry independent of on-host logs.

## Mechanism and observation

Emulate one technique, then measure whether detection fired and whether evidence survives off-host.

**Firstness:** Record what the technique changed/removed on-host and what the central logging/EDR captured. **Secondness:** State the integrity invariant (actions are logged off-host; tampering is itself an event; evidence is recoverable) and the deviation. **Thirdness:** Infer a control gap only after an emulated action is shown to evade detection/recovery under control.

## Abduction and refutation

**Hypothesis:** An anti-forensic action can remove or alter evidence without being detected or recoverable (a forensic-integrity gap).

**Competing benign explanation:** Central logging already shipped the records off-host before tampering; the clear/edit is itself logged; EDR captured the process independently; file-system journals/shadow copies retain remnants; the tampering raises an integrity alert.

## Deduction and controls

A normal action leaves complete, tamper-evident evidence (positive control = integrity holds). A confirmed gap shows an emulated anti-forensic action that leaves no detectable trace and no recoverable evidence where a hardened logging/forensic posture would retain both. Predeclare the detection signal and the recovery source. Off-host logging / tamper-evident audit / EDR independence / journal retention defeating the action are PASS controls.

## Induction: bounded laboratory procedure

Owned instrumented lab host; emulation under authorization.

1. **Baseline.** Perform a normal action; confirm complete on-host and central evidence.
2. **Emulate one technique** (e.g. a log clear or a timestamp alteration) on the lab host.
3. **Measure detection.** Did a clear/integrity event fire? Did central logging retain the pre-tamper record? Did EDR capture it independently?
4. **Measure recovery.** Can the evidence be reconstructed from journals/shadow copies/central store/backups?
5. **Score.** PASS (detected and recoverable), WARN (one of the two), FAIL (neither).
6. **Control.** Compare against a hardened posture (immutable off-host logging, tamper-evident chain) and confirm it retains.

Record results including refutations. Keep finding status separate from the control score. The goal is the score, not successful hiding.

## Craft notes (leads)

The durable defense is that evidence leaves the host immediately and the audit chain is tamper-evident — then on-host anti-forensics cannot erase what is already shipped. Timestomp detection relies on the two timestamp sets diverging and on the journal. Log-clear events are themselves high-signal. File-system journals and shadow copies are recovery sources. EDR provides an on-host-independent record. (See `tamper-evident-audit-chain`, `forensic-persistence`.)

## Domain-specific failure modes

If logs ship off-host in real time, on-host tampering is largely moot — a PASS. A clear event that is itself logged defeats silent clearing. EDR independence means on-host wiping does not erase the central record. Running these techniques to actually impede an investigation is out of scope and unlawful; the only purpose here is measuring and improving detection.

## Evidence and deliverable

Provide the technique emulated, the detection signals observed (or their absence), the recovery sources that retained evidence, and the PASS/WARN/FAIL. Keep this to the owned lab. Attach minimal replay, expected/observed, rival explanation, falsifier, techniques not assessed.

## Versions and tool limitations

Pin the OS, logging stack and EDR versions — detection and recovery behavior are product-specific. No host behavior was verified by this content; reproduce on the lab first.

## Remediation and detection

Ship logs off-host in real time to an append-only/immutable store, make the audit chain tamper-evident, deploy EDR with independent telemetry, retain file-system journals and shadow copies, and alert on log-clear/integrity events. Add a regression that an emulated clear is both alerted and recoverable from the central store.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An emulated anti-forensic action evades detection and recovery on the lab host where a hardened posture retains both: CONFIRMED integrity gap; control FAIL. |
| Benign refutation | Off-host logging / clear-event / EDR / journal retains evidence and alerts: REFUTED; control PASS. |
| Insufficient evidence | Detection fires but recovery is unverified (or vice versa): CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/forensics/offensive-anti-forensics/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's anti-forensic techniques as a defensive detection-and-recovery measurement on an owned lab, scoring forensic-integrity controls PASS/WARN/FAIL, rather than providing an evidence-destruction playbook. Composes with `forensic-logging-design`, `tamper-evident-audit-chain`, `forensic-persistence`, `detection-engineering`.
