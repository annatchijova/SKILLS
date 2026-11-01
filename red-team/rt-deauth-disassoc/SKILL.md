---
name: rt-deauth-disassoc
description: Validate negotiated PMF and bounded disconnect recovery using an isolated AP/client pair and a reviewed conformance harness.
---

# Management-frame resilience validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated radio enclosure, owned AP/client and an approved conformance fixture with a finite test-case count. Record maximum permitted outage and an immediate stop control.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- PMF capability advertisement differs from negotiated protection for a particular association.

- Protection of robust management frames is not a promise against all RF interference, authentication load or every action-frame class.

- Disconnection can result from legitimate controller policy, inactivity, radio loss or client power management.

- Recovery includes reassociation, service restoration and state continuity; a connected icon is not a service oracle.

## Observation and competing explanations

**Firstness / Secondness:** Record the negotiated PMF state, management-frame class and both endpoint state transitions against a stable baseline.

**Abduction:** A PMF-negotiated association processes an invalid unprotected robust management-frame test case as an authenticated disconnect.

**Competing benign explanation:** The disconnect was a legitimate protected AP event or unrelated RF loss.

**Deduction:** The reviewed invalid-frame case produces a correlated endpoint disconnect while a no-stimulus control remains connected and a legitimate protected disconnect follows the expected path.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Establish a stable PMF association and periodic harmless service canaries; collect endpoint and capture timestamps.

2. Confirm the conformance fixture reaches the intended association using a benign supported case.

3. Run only the reviewed single-case fixture, below the agreed case and outage budget; do not construct attack frames or run broadcast floods.

4. Compare invalid-frame handling with the no-stimulus baseline and an operator-issued protected disconnect; stop if service fails to recover.

5. Restore association and confirm service state and policy; report recovery time separately from PMF handling.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- No observed disconnect can mean the fixture never reached the target; require delivery evidence.

- Pre-association frames and non-robust action frames have different protection rules.

- PMF optional on an AP does not tell whether the observed client negotiated protection.

## Evidence and output

Provide negotiated security, conformance case identifier, delivery evidence, endpoint reason codes, service timeline and outage bounds.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate alerts for invalid management frames and correlate them with endpoint reasons; distinguish ordinary roaming from rejected conformance stimuli.

Require PMF where supported, update affected client/AP code and test recovery budgets; document incompatible clients rather than claiming universal coverage.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Pin firmware, driver and harness revision. Verify case applicability to the exact management-frame class; generic tool attack-mode labels are not protocol evidence.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Delivered invalid robust-management fixture disconnects a PMF association while the no-stimulus and protected-event controls isolate the cause. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The endpoint logs a legitimate protected controller disconnect before the test case arrives; invalid cases are rejected in the matched run. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | The client stays connected but no capture or fixture log proves delivery. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-deauth-disassoc/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Preserves PMF, frame-class and recovery analysis while replacing coercion and denial-of-service recipes with bounded conformance validation.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
