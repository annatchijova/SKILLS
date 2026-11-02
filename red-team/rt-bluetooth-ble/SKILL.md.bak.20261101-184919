---
name: rt-bluetooth-ble
description: Assess BLE GATT authorization, bonding lifecycle and application freshness using inert owned peripherals and companion fixtures.
---

# BLE attribute and pairing authorization

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a development peripheral exposing an inert test attribute, two owned centrals and disposable bonds. Substitute a simulator for locks, vehicles and medical actuators.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- GATT characteristic properties describe supported operations, not the complete authorization policy.

- Link encryption, pairing authentication, bonding and application authorization are distinct states.

- Just Works can provide encryption without authenticated peer confirmation; that alone does not prove application command acceptance.

- A valid bond may outlive account logout or ownership transfer; application freshness and revocation need separate checks.

## Observation and competing explanations

**Firstness / Secondness:** Record characteristic UUID, ATT status, connection security and application identity. Compare accepted operations with the required role and ownership state.

**Abduction:** An unbonded central can change a test attribute whose application policy requires the owner's authenticated session.

**Competing benign explanation:** The characteristic is intentionally public, or a cached bond/application session authorized the request.

**Deduction:** A fresh unbonded central changes the protected marker, while a public read works and a separately protected attribute rejects it; the owner control succeeds.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Map documented public and protected attributes and record the initial marker state.

2. Run the supported owner operation as a positive control, then use a fresh central without inherited bond or app session.

3. Submit one documented inert attribute operation and verify peripheral-side state, not merely the client write return code.

4. Separately revoke the disposable bond or ownership and check a previously valid test session against a fresh authorized session.

5. Restore the marker and intended bonds; verify the peripheral remains usable and ownership is correct.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- Write-without-response success does not prove the peripheral accepted the value.

- Attribute handles can change after firmware updates; bind evidence to UUID and service version.

- Discovery and public telemetry are not automatically confidentiality failures; apply the declared data policy.

## Evidence and output

Provide attribute/security-state matrix, ATT statuses, peripheral state receipts, pairing method and sanitized bond lifecycle logs.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Log rejected sensitive operations, new bonds and post-revocation use; confirm events on the peripheral or gateway rather than assuming a universal BLE IDS.

Enforce per-operation authorization, suitable pairing requirements and server-side ownership/freshness checks; revoke both transport and application state as appropriate.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record controller, host stack, peripheral firmware and companion build. Validate sniffer PHY and connection-following support; deprecated GATT tools may not model modern security states.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh unbonded central changes the protected inert marker, with public-read, protected-deny and owner controls as predicted. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The attribute is documented public; the actual protected marker rejects the fresh central after cached bonding is removed. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | The central reports a successful write without a response and no peripheral state was collected. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-bluetooth-ble/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Keeps GATT, pairing and ownership mechanics while replacing key recovery, relay and actuator abuse with inert authorization tests.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
