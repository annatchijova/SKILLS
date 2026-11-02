---
name: rt-lateral-movement
description: "Red-team assessment of lateral-movement boundaries in an authorized engagement: credential reuse/pass-the-hash/pass-the-ticket, remote-execution services (SMB/WMI/WinRM/SSH/RDP), trust and segmentation traversal, and session/credential harvesting. Re-expressed as scoped experiments across owned/planted hosts that prove one hop with a benign marker, measure detection, and respect segmentation controls instead of free-roaming a live network."
---

# Lateral-Movement Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's lateral-movement craft as scoped experiments across owned/planted hosts: it names the reuse and remote-exec techniques, proving one hop with a benign marker and measuring detection, rather than free-roaming a production network.

## Scope and prerequisites

Lateral movement spreads from one host to another using harvested credentials/tickets and remote-exec services. Carry the engagement authorization; move only between in-scope/planted hosts; prove a hop with a benign marker (an owned-collector callback or a planted file on the next host). Deconflict and respect segmentation.

Declare the scoped hosts, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Credential reuse** — reused local-admin passwords, pass-the-hash (NTLM), pass-the-ticket / overpass-the-hash (Kerberos).
- **Remote execution** — SMB (admin shares/service create), WMI, WinRM, SSH, RDP, DCOM.
- **Trust/segmentation** — crossing network segments, domain trusts, jump hosts.
- **Harvesting** — session tokens, cached creds, SSH keys, ticket caches on a compromised owned host.

## Mechanism and observation

Pick one hop; trace the credential/service to execution on the next host.

**Firstness:** Record the benign marker on the next host (callback, planted file) and the credential/service used. **Secondness:** State the intended boundary (unique local creds, no admin reuse, segmentation, signing) and the deviation. **Thirdness:** Infer the lateral path only after the hop reaches the marker under control.

## Abduction and refutation

**Hypothesis:** A harvested credential/ticket plus a remote-exec service lets execution move to another in-scope host.

**Competing benign explanation:** LAPS gives unique local-admin passwords (reuse fails); SMB signing blocks relay; the service requires MFA; segmentation/firewall blocks the path; the credential lacks rights on the target; EDR blocks the remote-exec technique.

## Deduction and controls

A legitimate admin action to an owned host succeeds (positive control); the lateral hop must fail if controls hold. A confirmed hop reaches the benign marker on the next host where LAPS/segmentation/signing/MFA would stop it. Predeclare the marker. Those controls defeating the hop are PASS controls.

## Induction: bounded procedure

Owned/planted hosts; benign marker; deconflicted.

1. **Harvest (owned host).** From a compromised owned host, collect a credential/hash/ticket/key in scope.
2. **Pick one hop.** Choose an in-scope/planted target the credential should reach.
3. **Execute one hop.** Pass-the-hash/ticket or reuse via SMB/WMI/WinRM/SSH to drop a benign marker on the next host; stop.
4. **Measure detection.** Did auth logging / EDR / NDR catch the technique (e.g. Kerberos anomalies, service creation, remote WMI)?
5. **Controls.** Confirm LAPS/signing/segmentation/MFA would block the hop.

Record results including refutations. Keep finding status separate from detection/control status. Prove one hop; do not sprawl.

## Craft notes (leads)

Pass-the-hash works where NTLM and reused local-admin passwords exist; LAPS kills password reuse. Pass-the-ticket/overpass-the-hash uses Kerberos (see `rt-active-directory`). SMB service-create and remote WMI/WinRM are the common exec vectors, each with distinct telemetry (service 7045, WMI operational logs). Segmentation and tiered admin are the structural defenses. Harvest only on the owned compromised host.

## Domain-specific failure modes

LAPS/unique local creds defeat reuse and pass-the-hash to local admin. SMB signing blocks relay. Segmentation/firewall can make the path unreachable regardless of credentials. A credential without rights on the target fails. Sprawling across the network instead of proving one hop is scope creep.

## Evidence and deliverable

Provide the credential/ticket, the service, the benign marker on the next host, the detection result, and the control (LAPS/segmentation/signing) outcome. Keep real credentials out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, hops not tested.

## Versions and tool limitations

Pin OS/domain versions and the remote-exec tooling. Techniques and telemetry are version-specific. No host behavior was verified by this content; confirm on the scoped hosts first.

## Remediation and detection

LAPS/unique local-admin passwords, SMB/LDAP signing, network segmentation and tiered admin, MFA on remote access, disable NTLM where possible, and credential-guard. Detect pass-the-hash/ticket anomalies, remote service creation (7045), remote WMI/WinRM, and anomalous admin logons. Add a regression that the hop is refused under controls.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | One lateral hop reaches a benign marker on the next in-scope host where LAPS/segmentation/signing/MFA would stop it: CONFIRMED; FAIL (scope to the hop). |
| Benign refutation | A control defeats the hop (unique creds / signing / segmentation / MFA): REFUTED; PASS for the control. |
| Insufficient evidence | A harvested credential without a confirmed hop: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/post-exploitation/offensive-lateral-movement/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's credential-reuse, remote-exec and trust-traversal craft, re-expressed as scoped owned/planted-host experiments with a benign marker, detection measurement and segmentation controls, replacing network free-roaming with bounded single-hop proof. Composes with `rt-active-directory`, `rt-netexec`, `rt-advanced-redteam`.
