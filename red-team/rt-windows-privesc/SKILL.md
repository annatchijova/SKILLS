---
name: rt-windows-privesc
description: "Red-team assessment of Windows local privilege-escalation boundaries: weak service permissions and unquoted service paths, token-privilege abuse (SeImpersonate/SeBackup/SeDebug), AlwaysInstallElevated, DLL search-order and COM hijack, scheduled-task and autorun misconfigurations, and credential harvesting. Re-expressed as scoped experiments on an owned host that prove one SYSTEM-reaching vector against a planted fixture with hardened-config controls and servicing-status awareness instead of live escalation."
---

# Windows Privilege-Escalation Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's Windows-privesc craft as scoped experiments on an owned host: it names the SYSTEM-reaching vectors, proving one against a planted fixture while noting which crossings Microsoft services as boundaries (see `rt-windows-boundaries`).

## Scope and prerequisites

Local privesc moves from a standard/service account to SYSTEM via a misconfiguration. Work on an owned host; prove against a planted fixture (a lab weak-permission service, a lab writable autorun) where possible, with a benign marker (a SYSTEM-owned marker file). Note whether each vector is a serviced boundary or a by-design/non-boundary case.

Declare the Windows build, attempt budget, stop condition. Enumeration-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Service misconfig** — weak service DACL (reconfigure binPath), weak binary/dir permissions, unquoted service path with a writable intermediate dir.
- **Token privileges** — SeImpersonate (Potato-class to SYSTEM, often by-design for service accounts), SeBackup/SeRestore, SeDebug, SeTakeOwnership.
- **AlwaysInstallElevated** — MSI installs as SYSTEM.
- **Hijacks** — DLL search-order, COM, scheduled-task/autorun writable targets.
- **Credentials** — cached creds, SAM/LSASS (on owned host), unattend/GPP passwords.

## Mechanism and observation

Pick one vector; trace the misconfiguration/privilege to SYSTEM execution.

**Firstness:** Record the SYSTEM capability against the planted fixture (reconfigured a lab service to run a marker as SYSTEM, impersonated a planted SYSTEM token). **Secondness:** State the intended boundary and the deviation. **Thirdness:** Infer the vector only after SYSTEM execution is exercised under control — and classify whether it is a serviced boundary.

## Abduction and refutation

**Hypothesis:** A specific misconfiguration or over-granted privilege lets a low-trust principal run as SYSTEM.

**Competing benign explanation:** The service DACL does not allow reconfigure; the unquoted path has no writable intermediate; SeImpersonate on a service account is by design (the finding is the account placement, not the technique); AlwaysInstallElevated is off; the DLL/COM path is not writable/hijackable; credentials are not exposed.

## Deduction and controls

A standard user cannot reach SYSTEM on a hardened host (positive control). A confirmed finding reaches SYSTEM via the vector against the planted fixture where hardening refuses. Predeclare the SYSTEM marker. Restrictive service DACLs / quoted paths / no AlwaysInstallElevated / non-writable hijack paths / least-privilege tokens are PASS controls.

## Induction: bounded procedure

Owned host; planted fixture where possible.

1. **Enumerate.** Service permissions/paths, token privileges (`whoami /priv`), AlwaysInstallElevated, writable autoruns/tasks, hijackable DLL/COM, exposed creds (WinPEAS/PowerUp as aids).
2. **Pick one vector.** Choose the clearest against a planted fixture.
3. **Exercise once.** e.g. reconfigure a planted weak-DACL service to run a marker as SYSTEM; or SeImpersonate → planted SYSTEM token; confirm SYSTEM; stop.
4. **Classify.** Is it a serviced boundary (weak DACL = yes) or by-design (SeImpersonate on a service account)?
5. **Controls.** Harden the fixture and confirm the vector fails.

Record results including refutations. Keep finding status separate from control and servicing status.

## Craft notes (leads)

Weak service DACLs (reconfigure binPath) and unquoted paths with writable intermediate dirs are classic serviced findings. SeImpersonate→SYSTEM (Potato family) is frequently by-design for service accounts — the finding is the account's placement/over-privilege, not the technique (see `rt-windows-boundaries`). AlwaysInstallElevated is a pure misconfiguration. GPP passwords and unattend files are credential findings. DLL search-order/COM hijacks need a writable path in the search order.

## Domain-specific failure modes

A by-design SeImpersonate on a service account is a configuration note unless the principal should not hold it. An unquoted path with no writable intermediate is not exploitable. A service the user cannot reconfigure is safe. UAC-only "escalation" is not a serviced boundary. Classify before scoring; prove against a planted fixture.

## Evidence and deliverable

Provide the vector, its servicing status, the SYSTEM marker against the planted fixture, and the hardened-config control result. Keep to the owned host; keep credentials out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, vectors not assessed.

## Versions and tool limitations

Pin the Windows build — vectors and servicing stance are version-specific. Enumeration tools are aids, not verdicts. No host behavior was verified by this content; confirm on the owned host first.

## Remediation and detection

Restrictive service DACLs and quoted paths, least-privilege tokens (remove SeImpersonate/SeDebug from low-trust accounts), disable AlwaysInstallElevated, fix writable autorun/DLL/COM paths, and remove credential artifacts (GPP/unattend). Add a regression that the vector fails. Detect service reconfiguration, token impersonation to SYSTEM, and MSI-as-SYSTEM.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A vector reaches SYSTEM against a planted fixture over a serviced boundary where hardening refuses: CONFIRMED; FAIL. |
| Benign refutation | Non-reconfigurable service / no writable intermediate / by-design privilege / UAC-only: REFUTED (or note as config); PASS for serviced controls. |
| Insufficient evidence | A suspicious config without confirmed SYSTEM: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/privesc/offensive-windows-privesc/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's service/token/MSI/hijack/credential craft, re-expressed as owned-host experiments against planted fixtures with hardened controls and Microsoft servicing-status awareness, replacing live escalation with bounded, contained SYSTEM-reach proof. Composes with `rt-windows-boundaries`, `rt-active-directory`, `rt-advanced-redteam`.
