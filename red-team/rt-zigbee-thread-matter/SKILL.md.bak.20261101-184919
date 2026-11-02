---
name: rt-zigbee-thread-matter
description: Assess Zigbee, Thread and Matter commissioning boundaries separately with disposable fabrics, inert endpoints and explicit ownership controls.
---

# Mesh commissioning and application authority

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a disposable coordinator or border router, two test commissioners/fabrics and an inert endpoint. Export intended ownership and commissioning-window policy before testing.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- Zigbee network admission, link/application keys and ZCL command authorization are related but distinct controls.

- Thread network credentials, commissioner authorization and application authorization are not interchangeable; PSKc is not the entire operational dataset.

- Matter runs over IP transports including Thread and Wi-Fi; it is not a universal Zigbee commissioning layer.

- Matter commissioning sessions, operational certificates, fabrics and access-control entries must be evaluated separately; possession of a setup code alone does not prove access.

## Observation and competing explanations

**Firstness / Secondness:** Identify the exact stack, transport, commissioning state and application principal. Compare the operation with the intended fabric or network authorization.

**Abduction:** A Matter principal from test fabric B can change an endpoint marker reserved for fabric A.

**Competing benign explanation:** The endpoint is intentionally shared through a documented ACL, or the client still uses a fabric A session.

**Deduction:** A fresh fabric B operational session changes the restricted marker despite the exported ACL; fabric A succeeds and an unauthenticated comparison is rejected.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Map protocol layers explicitly and establish a normal owner operation on the inert endpoint.

2. Close commissioning using the supported interface and verify its reported state before any new enrollment test.

3. For the fabric-boundary case, use fresh sessions and a single documented marker operation for each principal; inspect device-side fabric and ACL decisions.

4. For Zigbee or Thread enrollment, run separate fresh-device cases inside and outside the operator window; do not reset unrelated nodes or extract network keys.

5. Remove only disposable fabrics/nodes, restore the ownership configuration and verify owner access and closed-window rejection.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- An 802.15.4 packet capture cannot by itself prove Matter ACL behavior or reveal every application key context.

- Border-router reachability is not proof of application authorization.

- Device labels and USB adapter names can misidentify chipsets; inspect actual radio/firmware support.

## Evidence and output

Provide protocol-layer map, fabric/network IDs, principal and ACL snapshots, commissioning timestamps and endpoint receipts, excluding secret datasets.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate events for window opening, unexpected enrollment, fabric additions and rejected application commands; tie them to the responsible principal.

Restrict commissioning windows and commissioner authority, apply per-fabric ACLs and separate network membership from sensitive application permissions.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record Zigbee/Thread/Matter specification and SDK revisions, bridge behavior and radio support. Verify each protocol's credential roles against its versioned implementation before testing.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh fabric B session changes the fabric A-only marker while owner and unauthenticated controls behave correctly. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The client was using fabric A; fresh fabric B access is rejected and the ACL matches the declared sharing policy. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | Only a mesh join was observed; no operational application session or ACL evidence exists. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-zigbee-thread-matter/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Corrects conflated protocol layers and key roles while preserving commissioning, mesh membership and application authority as distinct experiments.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
