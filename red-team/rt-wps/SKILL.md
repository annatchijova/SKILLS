---
name: rt-wps
description: Measure WPS enrollment windows, disablement and PIN attempt controls on an owned AP without PIN recovery or brute force.
---

# WPS enrollment lifecycle validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated AP and disposable enrollee, known lab PIN, exported configuration and a fixed small invalid-attempt budget below disruption limits.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- PIN enrollment and push-button enrollment are different state machines with distinct authorization windows.

- A WPS information element or locked flag is an advertisement; prove actual enrollment acceptance or refusal.

- Rate control requires server-side failure counters and a defined unlock policy; silence may instead be packet loss.

- Historical weak-nonce families require implementation-specific evidence; chipset branding cannot establish predictable randomness.

## Observation and competing explanations

**Firstness / Secondness:** Record enrollment state, operator activation time and response status. Contrast the actual acceptance window with the configured policy.

**Abduction:** The AP accepts a fresh enrollee after its configured push-button window has closed.

**Competing benign explanation:** The observed client resumed an existing enrollment or another operator reopened the window.

**Deduction:** A new, unprovisioned lab enrollee is accepted after expiry without a new activation; an in-window control succeeds and a disabled-WPS control refuses it.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Record the AP clock, configuration and enrollment logs; ensure only the lab operator can activate the fixture.

2. Validate successful in-window enrollment, then remove that test enrollee using the supported interface.

3. After the documented window expires, try a fresh enrollee once and inspect server acceptance and issued configuration, without exporting the key.

4. In a separate PIN-control test, submit only the agreed invalid fixtures and stop on lockout; observe the documented recovery rather than bypassing it.

5. Disable WPS, verify refusal and restore the agreed final configuration while retaining logs.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A beacon locked flag need not cover push-button mode or all radios.

- Retry retransmissions are not necessarily independent PIN attempts.

- A PIN rejection does not validate random-number generation; nonce predictability remains untested without a suitable implementation harness.

## Evidence and output

Deliver activation/expiry timestamps, fresh enrollee identity, server decisions, mode-specific counters and disablement verification with secrets redacted.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Alert on enrollment outside operator windows, configuration re-enablement and unexpected reset of attempt counters; exercise these events with lab fixtures.

Disable unused enrollment modes, enforce finite operator-controlled windows and persistent documented attempt limits. Verify all radios and post-reboot policy.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record AP hardware revision and firmware, registrar/enrollee implementation and WPS mode. Verify tool behavior locally; avoid upstream chipset vulnerability tables.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | A fresh enrollee is accepted after expiry, with working in-window and disabled-mode controls and no new activation. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Only an already-authorized enrollment resumed; a fresh enrollee is rejected after expiry. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A WPS-capable beacon is visible but there are no enrollment decisions or time records. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wps/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Transforms PIN recovery and lockout evasion into bounded enrollment-state and attempt-policy validation.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
