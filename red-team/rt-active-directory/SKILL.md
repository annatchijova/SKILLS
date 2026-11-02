---
name: rt-active-directory
description: "Red-team assessment of Active Directory authority paths in an authorized engagement: BloodHound/PowerView attack-path enumeration, coercion+relay (PetitPotam, PrinterBug, ESC8), Kerberoasting/ASREProasting, ACL abuse (GenericAll/WriteDacl/WriteOwner), Kerberos delegation (unconstrained/constrained/RBCD), and ADCS templates (ESC1-ESC8). Re-expressed as a scoped lab experiment that proves one authority-path edge with a planted principal and negative controls, emphasizing detection."
---

# Active Directory Authority-Path Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's AD craft as a scoped authority-path experiment: it names the real edges and primitives, and proves one of them against a planted principal in an authorized lab, with detection as a first-class deliverable, rather than running a full domain-takeover chain.

## Scope and prerequisites

AD compromise is a graph of authority edges from a low-privilege principal to Domain Admin / DCSync. Carry the engagement's authorization: scope which hosts, which collection methods, and the stop condition (prove the edge, do not ransack the domain). Use planted synthetic principals/objects where possible and a lab DC you are authorized to touch. Collection and coercion generate noise and can disrupt production — throttle and get explicit sign-off.

Declare target domain, functional level, attempt budget, stop condition. Source/config-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Recon** — attack-path graph (BloodHound via SharpHound/bloodhound.py, PowerView, offline ADExplorer snapshot).
- **Credential capture** — LLMNR/NBT-NS/mDNS poisoning → NetNTLMv2, NTLM relay (to LDAP/ADCS), Kerberoasting (SPN TGS), ASREProasting (no-preauth), LSASS/SAM (on owned host).
- **ACL abuse** — GenericAll/GenericWrite, WriteDacl (grant DCSync), WriteOwner, AllExtendedRights, AddMember, targeted Kerberoast via WriteSPN.
- **Delegation** — unconstrained (coerce DC auth → TGT), constrained (S4U2self/proxy), RBCD (write `msDS-AllowedToActOnBehalfOfOtherIdentity`).
- **Coercion** — PetitPotam (MS-EFSRPC), PrinterBug (MS-RPRN), DFSCoerce, ShadowCoerce, WebDAV; chain coerce+relay.
- **ADCS** — ESC1-ESC8 certificate-template and enrollment misconfigurations.

## Mechanism and observation

Pick one edge; trace the precondition (which right on which object) to the effect (which new authority).

**Firstness:** Record the concrete capability gained against a planted principal (a TGS obtained, an ACL edge exercised, a cert issued with a chosen UPN). **Secondness:** State the intended authority boundary and the deviation. **Thirdness:** Infer the authority-escalation class only after the edge is exercised under control.

## Abduction and refutation

**Mechanism hypothesis:** A specific misconfiguration (an ACL edge, a delegation attribute, a vulnerable cert template) lets a low-privilege principal obtain authority it should not have.

**Competing benign explanation:** SMB/LDAP signing is enforced (relay fails); the SPN account has a strong AES key (roast infeasible); the template requires manager approval or lacks client-auth EKU; the coercion target is patched; the "edge" requires rights the test principal does not actually hold.

## Deduction and controls

A principal acting within its rights succeeds (positive control); the escalation edge must fail if the misconfig is absent. A confirmed finding exercises the edge against a planted principal (e.g. WriteDacl → self-grant DCSync on a lab object) where a correctly-configured control object refuses. Predeclare the capability that confirms it. Signing enforced / template hardened / coercion patched are PASS controls.

## Induction: bounded laboratory procedure

Authorized lab; planted principals; throttled collection.

1. **Map.** Collect the graph (stealth/DC-only where required) and identify one short path to high authority.
2. **Verify preconditions.** Confirm the test principal actually holds the claimed right and the target's control state (signing, template flags).
3. **Exercise one edge (planted target).** e.g. Kerberoast a planted SPN account; or WriteDacl→DCSync on a lab object; or RBCD on a lab computer; or request an ESC1 cert with a planted UPN.
4. **Prove capability, stop.** Demonstrate the new authority once against the planted object; do not pivot to the real DA.
5. **Controls.** Show a correctly-configured sibling object refuses the same edge; confirm signing/approval/EKU where claimed.
6. **Detection.** Record the telemetry each step produced.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

The highest-yield modern chains are coerce+relay to ADCS (ESC8) and RBCD via a writable computer object. AES-only Kerberoast is harder but worth attempting. Unconstrained delegation + coercion yields a DC TGT. ADExplorer enables offline graph analysis from any low-priv user. Each is an authority-boundary edge — demonstrate the edge, not a full breach.

## Domain-specific failure modes

Signing enforcement silently defeats relay. A graphed edge may require rights the principal lacks — verify, do not assume the collector's inference. Collection and coercion are noisy and can disrupt production. A patched coercion vector or hardened template is a refutation. Proving one edge is the deliverable; chaining to DA is out of scope unless explicitly authorized.

## Evidence and deliverable

Provide the edge (precondition→effect), the planted principal/object, the capability obtained, the control object's refusal, and the detection telemetry. Keep real credentials/hashes out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered paths.

## Versions and tool limitations

Pin domain functional level, DC OS/patch level, and ADCS configuration — edges and coercion vectors are version/patch-bound. BloodHound/impacket/Certipy/netexec default to active operations; run within scope against lab targets. No AD behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

Enforce SMB/LDAP signing and channel binding, harden ADCS templates (remove ENROLLEE_SUPPLIES_SUBJECT/Any-Purpose, require approval), tier admin accounts, remove dangerous ACL edges and unconstrained delegation, patch coercion vectors, and use AES/strong SPN passwords. Add detections: Kerberoast TGS bursts, DCSync from non-DCs, ACL changes on privileged objects, coercion RPC calls, cert requests with unusual SANs. Add a regression that the control object refuses the edge.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | One authority edge is exercised against a planted principal in the lab where a hardened control object refuses: CONFIRMED; FAIL (scope to the edge shown). |
| Benign refutation | Signing enforced / template hardened / coercion patched defeats the edge: REFUTED for that edge; PASS for the control. |
| Insufficient evidence | A graphed edge whose preconditions are not verified: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/active-directory/offensive-active-directory/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's attack-path, ACL, delegation, coercion and ADCS craft, re-expressed as a scoped authorized-lab experiment that proves one edge against a planted principal with detection telemetry, replacing full domain-takeover chains with bounded authority-edge proof. Compose with `rt-netexec` (protocol tooling) and `authorization-surface-mapping`.
