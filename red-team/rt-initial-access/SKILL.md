---
name: rt-initial-access
description: "Red-team assessment of initial-access exposure in an authorized engagement: phishing/social delivery, public-facing exploitation, valid-account abuse, exposed services and supply-chain entry. Re-expressed as a scoped exposure-and-detection exercise that maps and tests entry vectors against owned/consented assets with a benign marker and detection measurement, not a live intrusion or mass phishing playbook."
---

# Initial-Access Exposure Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the exercise below.
This revision restores the upstream's initial-access craft as a scoped exposure-and-detection exercise: it maps the entry vectors and tests one against consented assets with a benign marker, measuring detection, rather than running a live intrusion or mass phishing campaign.

## Scope and prerequisites

Initial access is the first foothold from outside. Test only against assets in the engagement scope, with the client's authorization and (for social vectors) consented recipients or an approved simulation. Prove reach with a benign marker (an owned-collector callback, a tracked test credential), never real credential theft at scale or malware delivery.

Declare the scoped assets, the vectors authorized (especially social), attempt budget, stop condition. Recon-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Phishing / social delivery** — credential-capture or payload links to consented recipients (see `rt-phishing`, `rt-social-engineering`).
- **Public-facing exploitation** — a vulnerable exposed app/service (route to the relevant web/infra skill).
- **Valid accounts** — leaked/sprayed credentials (lockout-safe; see `rt-netexec`).
- **Exposed services** — RDP/SMB/VPN/management interfaces reachable from outside.
- **Supply chain** — a dependency/update path (see `rt-supply-chain`).

## Mechanism and observation

Map exposure first, then test one vector to a benign foothold marker.

**Firstness:** Record the reachable entry and whether the benign marker achieved a foothold signal (callback, authenticated session on a test account). **Secondness:** State the intended perimeter (no external exploitation, MFA on accounts, no exposed management) and the deviation. **Thirdness:** Infer an initial-access path only after a controlled test reaches the marker.

## Abduction and refutation

**Hypothesis:** An external entry vector reaches a foothold on a scoped asset.

**Competing benign explanation:** The exposed service requires MFA/VPN and the test credential fails; the public app is patched; the phishing link is blocked by mail security and sandboxing; egress controls stop the callback; the "exposure" is a decoy/honeypot.

## Deduction and controls

A normal external user cannot gain a foothold (positive control = perimeter holds). A confirmed path reaches the benign marker via the vector where perimeter controls would stop it. Predeclare the foothold signal. MFA / patching / mail security / egress control defeating the vector are PASS controls.

## Induction: bounded procedure

Scoped/consented assets; benign marker.

1. **Map exposure.** Enumerate external surface (services, apps, accounts, delivery paths) within scope.
2. **Select one vector.** Choose the highest-likelihood authorized vector.
3. **Test to a marker.** e.g. a consented phishing simulation capturing a tracked test credential; or a public-app PoC reaching an owned callback; or a lockout-safe spray against a test account. Stop at the foothold signal.
4. **Measure detection.** Did mail security/EDR/NDR/auth logging catch it?
5. **Control.** Confirm the perimeter control (MFA, patch, egress) defeats the vector.

Record results including refutations. Keep finding status separate from detection/control status. Do not expand the foothold; initial access is the deliverable.

## Craft notes (leads)

The highest-yield modern vectors are valid-account abuse (leaked creds + no MFA) and public-facing exploitation of an unpatched edge device. Phishing effectiveness depends on mail security and user training — measure both. Exposed management interfaces (RDP/VPN/panels) are recurring footholds. Each vector routes to a specialized skill for depth.

## Domain-specific failure modes

MFA defeats most valid-account paths — a PASS. A patched edge service refutes the exploitation vector. Mail security + sandboxing blocks many phishing payloads. Egress control stops the callback even if delivery succeeds. A consented simulation is required for social vectors; real mass phishing is out of scope.

## Evidence and deliverable

Provide the vector, the exposure mapped, the benign foothold marker, the detection result, and the perimeter-control outcome. Use consented assets/recipients; keep real credentials out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, vectors not tested.

## Versions and tool limitations

Pin the exposed service/app and mail-security versions. No perimeter behavior was verified by this content; confirm the live exposure first.

## Remediation and detection

MFA everywhere, patch external services, remove exposed management interfaces (VPN/ZTNA-gate them), mail security + sandboxing + user training, egress control, and supply-chain controls. Add detections for external exploitation, impossible-travel/auth anomalies, and phishing clicks. Add a regression that the vector is refused.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A vector reaches a benign foothold marker on a scoped asset where perimeter controls would stop it: CONFIRMED; FAIL (scope to the foothold). |
| Benign refutation | MFA/patch/mail-security/egress defeats the vector: REFUTED; PASS for the control. |
| Insufficient evidence | A reachable surface without a confirmed foothold: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-initial-access/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's initial-access vector map, re-expressed as a scoped exposure-and-detection exercise with a benign marker and perimeter controls, replacing live intrusion and mass phishing with bounded foothold proof. Composes with `rt-phishing`, `rt-social-engineering`, `rt-netexec`, `rt-supply-chain`, `rt-advanced-redteam`.
