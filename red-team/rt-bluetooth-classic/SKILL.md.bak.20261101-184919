---
name: rt-bluetooth-classic
description: Validate Bluetooth Classic profile authorization and negotiated security on owned audio, serial or input test fixtures.
---

# BR/EDR service and pairing policy

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use two owned peers and an inert serial echo or disposable object fixture. Disable real keyboard input, call audio and physical device controls.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- SDP service discovery indicates availability, not permission to use a profile.

- BR/EDR remains relevant beyond Bluetooth 4.0; protocol role and enabled profiles matter more than marketing generation.

- Pairing, bonding, encryption-key strength and profile-level authorization are separate controls.

- SPP, OBEX, HID and audio profiles expose different operations; service success must be measured at its own endpoint.

## Observation and competing explanations

**Firstness / Secondness:** Record SDP advertisement, pairing state, negotiated security and profile operation result against the service authorization policy.

**Abduction:** An unbonded peer can invoke a protected SPP diagnostic operation that requires an approved bond.

**Competing benign explanation:** SDP listing was mistaken for profile access, or a stale bond grants legitimate permission.

**Deduction:** A fresh peer receives the protected echo marker without a bond; the approved peer succeeds and an unauthenticated protected comparison service rejects access.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Export profile policy and controller/host security settings, then verify the approved peer's inert service operation.

2. Query only the owned peer's advertised services and separate discovery from use.

3. With a fresh lab identity, attempt one documented harmless profile operation; inspect receiver-side authorization and output.

4. For key-strength concerns, inspect negotiated values through supported controller diagnostics and compare against the configured minimum; do not patch firmware to weaken negotiation.

5. Remove temporary bonds and objects and verify the intended peer's service after restoration.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A known device address is not an authenticated identity; neither is failure to appear in inquiry.

- A scanner's historic CVE match establishes a lead, not reachable profile exploitation.

- A controller diagnostic limitation can hide negotiated security; mark that field unknown.

## Evidence and output

Deliver per-profile discovery/use decisions, host/controller builds, bond state and endpoint marker receipt. Keep audio and human input outside the evidence set.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate visibility of new bonds, rejected profile connections and weak-security negotiation events on the actual stack.

Require suitable security at profile use, remove unused diagnostic services and update controller and host components implicated by evidence.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record BR/EDR features and profile versions explicitly. Check support for SDP and controller diagnostics locally; old scanner or adapter compatibility claims require verification.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh unbonded peer receives the protected SPP marker, while approved-peer and protected-deny controls isolate authorization failure. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | SDP advertises SPP but the protected operation is denied until the approved bond is present. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A historic scanner warning exists with no exact firmware revision or negotiated-security evidence. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-bluetooth-classic/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Preserves Classic profile and key-policy distinctions without HID injection, audio interception, address brute force or firmware weakening.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
