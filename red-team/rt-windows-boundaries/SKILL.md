---
name: rt-windows-boundaries
description: "Red-team assessment of Windows security boundaries: integrity levels and UAC, token privileges and impersonation, session/desktop isolation, DACL/object security, named-pipe and service boundaries, and the Microsoft servicing stance on which of these are defended trust boundaries vs not. Re-expressed as scoped experiments on an owned Windows lab that prove one boundary crossing against a planted object with hardened-config controls instead of live escalation."
---

# Windows Security-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiments below.
This revision restores the upstream's Windows-boundary craft as scoped experiments: it names the boundaries and their servicing status, proving one crossing against a planted object in an owned lab rather than escalating on a live host.

## Scope and prerequisites

Windows enforces several boundaries (integrity levels, tokens, sessions, object DACLs). Crucially, not all are servicing (defended) boundaries — Microsoft treats UAC and some others as convenience, not security boundaries. Work on an owned Windows lab with planted objects/accounts; prove a crossing against the planted target. Know, per boundary, whether Microsoft defends it before calling a crossing a vulnerability.

Declare the Windows build, the boundary under test, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Boundary classes (and servicing status)

- **Integrity levels / UAC** — Low/Medium/High/System. UAC elevation is NOT a defended security boundary per Microsoft; a Medium-to-High bypass is usually not serviced as a vuln.
- **Token privileges / impersonation** — SeImpersonate/SeDebug/SeBackup etc.; impersonation to SYSTEM from a service account is a classic (often by-design-for-service) path.
- **Session / desktop isolation** — Session 0 isolation; cross-session is a defended boundary.
- **Object DACLs** — securable-object permissions; a weak DACL on a privileged object is a real misconfiguration.
- **Named pipe / service** — pipe impersonation, weak service permissions (reconfigure/binpath).

## Mechanism and observation

Pick one boundary; trace the capability that crosses it against a planted object.

**Firstness:** Record the crossing achieved against the planted target (impersonated a planted SYSTEM token, wrote via a weak DACL, reconfigured a planted service). **Secondness:** State whether the boundary is a defended servicing boundary and the deviation. **Thirdness:** Infer a finding only after the crossing is exercised under control AND the boundary is one Microsoft defends (otherwise it is a hardening/misconfig note, not a vuln).

## Abduction and refutation

**Hypothesis:** A specific primitive crosses a defended Windows boundary (token/DACL/session) granting authority it should not.

**Competing benign explanation:** The crossing is over a non-servicing boundary (UAC) — expected, not a vuln; the token privilege is by design for that service account; the DACL is correctly restrictive; Session 0 isolation holds; the service cannot actually be reconfigured by the principal.

## Deduction and controls

A principal within its rights succeeds (positive control); the crossing must fail (or be a non-boundary) otherwise. A confirmed finding crosses a defended boundary against a planted object where a hardened config refuses. Predeclare the capability and the boundary's servicing status. Restrictive DACL / removed dangerous privilege / Session 0 isolation are PASS controls; a UAC "bypass" is noted as non-servicing.

## Induction: bounded laboratory procedure

Owned Windows lab; planted objects.

1. **Enumerate.** Current integrity level, token privileges, session, and the DACLs/services in scope.
2. **Classify the boundary.** Is the target crossing over a defended servicing boundary or a convenience one (UAC)?
3. **Exercise one crossing (planted target).** e.g. SeImpersonate → impersonate a planted SYSTEM token; or reconfigure a planted weak-DACL service; or write a planted privileged object.
4. **Prove capability, stop.** Demonstrate once against the planted object.
5. **Controls.** Harden the DACL/privilege/service and confirm the crossing fails.
6. **Servicing note.** State whether Microsoft would service this as a vuln.

Record results including refutations. Keep finding status separate from control status and from servicing status.

## Craft notes (leads)

The "Potato" family (SeImpersonate → SYSTEM) is often by-design for service accounts, not a vuln per se — the finding is the over-granted privilege, not the technique. UAC bypasses are abundant but not serviced. The real, serviced findings are weak DACLs on privileged objects/services, cross-session isolation breaks, and token-privilege over-grants to low-trust principals. Always pair the technique with the servicing status.

## Domain-specific failure modes

Reporting a UAC bypass as a vulnerability is the classic over-call — it is not a defended boundary. A by-design service privilege (SeImpersonate) is a configuration note unless the principal should not hold it. Crossing a boundary on a live host instead of a planted object is out of scope. Classify the boundary before scoring.

## Evidence and deliverable

Provide the boundary, its servicing status, the crossing against the planted object, the capability gained, and the hardened-config control result. Keep to the owned lab. Attach minimal replay, expected/observed, rival explanation (non-boundary/by-design), falsifier, boundaries not assessed.

## Versions and tool limitations

Pin the Windows build — boundary behavior and servicing stance change across versions. No Windows behavior was verified by this content; confirm on the lab first.

## Remediation and detection

Least-privilege tokens (remove SeImpersonate/SeDebug from low-trust accounts), restrictive DACLs on privileged objects and services, enforce Session 0 isolation, and treat UAC as convenience (do not rely on it as a boundary). Detect token impersonation to SYSTEM, service reconfiguration, and privileged-object DACL changes. Add a regression that the crossing fails under hardening.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A crossing over a defended boundary (weak DACL/over-granted token/cross-session) is exercised against a planted object where hardening refuses: CONFIRMED; FAIL. |
| Benign refutation | The crossing is over a non-servicing boundary (UAC) or a by-design service privilege: REFUTED as a vuln (note as hardening/misconfig); PASS for defended-boundary controls. |
| Insufficient evidence | A crossing attempted but capability not confirmed: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-windows-boundaries/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's Windows-boundary craft and pairs each with its Microsoft servicing status, re-expressed as owned-lab experiments against planted objects with hardened controls, replacing live escalation with bounded, servicing-aware crossing proof. Composes with `rt-windows-privesc`, `rt-windows-mitigations`, `rt-active-directory`.
