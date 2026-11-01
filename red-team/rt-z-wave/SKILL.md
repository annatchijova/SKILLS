---
name: rt-z-wave
description: Validate Z-Wave inclusion security classes, device verification and command enforcement with a disposable controller and inert nodes.
---

# Z-Wave inclusion and command security

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated controller and simulator or harmless indicator node, disposable network keys and a documented minimum inclusion class. Exclude locks and alarm actuators.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- S0 bootstrap exposure and operational network keys are distinct; do not describe all S0 keys as a single fixed derived network key.

- S2 security classes have different authentication properties; recording only 'S2' hides the actual granted class.

- Controller inclusion policy and device-specific verification determine whether a reduced class is accepted.

- Home ID and node ID are routing identifiers, not authentication secrets; command-class enforcement must be checked at the receiving node.

## Observation and competing explanations

**Firstness / Secondness:** Record requested, granted and reported security classes plus user confirmation. Compare them with the controller's configured inclusion policy.

**Abduction:** The controller silently completes inclusion below the required security class and permits a protected test operation.

**Competing benign explanation:** The operator explicitly approved a documented legacy exception, or the UI label omits a stronger negotiated class.

**Deduction:** A fresh inclusion without an exception grants the lower class and the node accepts the restricted marker; compliant inclusion succeeds and a prohibited clear operation is rejected.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Export controller policy and verify compliant inclusion of the owned reference node.

2. Use supported test-device capability settings to present the comparison class; do not alter over-air negotiation or recover keys.

3. Complete the defined inclusion attempt with the recorded operator actions and inspect controller and node security state.

4. Send one documented inert operation through the legitimate test controller and verify receiver-side class enforcement.

5. Exclude disposable nodes using supported controls, close inclusion and verify the retained reference node still works.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- An inclusion warning with explicit consent differs from silent policy violation.

- A secure controller session does not establish that every command class on the node requires equivalent security.

- A hub configuration finding is not a radio cryptography finding; keep the boundaries separate.

## Evidence and output

Provide inclusion event IDs, class negotiation and confirmation records, receiver operation result and restoration state without network keys or DSK secrets.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Exercise alerts for reduced-class inclusion, prolonged inclusion windows and sensitive commands below required security.

Enforce minimum classes and explicit exceptions, verify device identity during inclusion, close enrollment windows and enforce security per command class.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record controller SDK, node firmware, regional radio variant and command-class versions. Check tool support locally rather than relying on upstream hardware lists or blanket certification dates.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh inclusion silently grants a prohibited lower class and the restricted marker is accepted, with compliant and clear-deny controls. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The lower class was an explicitly approved legacy exception; normal policy rejects the same inclusion without that exception. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | The hub UI says 'secure' but no granted-class or receiver-side record is available. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-z-wave/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Replaces S0 key recovery and hub pivots with inclusion policy and receiver enforcement, correcting routing-ID and key-role confusion.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
