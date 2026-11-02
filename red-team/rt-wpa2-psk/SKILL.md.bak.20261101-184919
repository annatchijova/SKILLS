---
name: rt-wpa2-psk
description: Validate WPA2 personal key provisioning and synthetic handshake evidence without recovering production credentials.
---

# WPA2 personal key-policy validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an owned AP/client and synthetic PSKs supplied by the operator, including one deliberately weak fixture and one independently generated secret. Never import real credential captures into external services.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- PSK provisioning quality is distinct from four-way-handshake correctness; a transcript alone does not prove a weak secret.

- A valid EAPOL verification fixture binds the SSID, peer addresses, nonces and integrity check to one known lab secret.

- PMKID availability depends on implementation and negotiation; an empty conversion can mean missing capture data.

- Fast-transition and caching paths require separate evidence; do not infer recoverable master-key material from roaming.

## Observation and competing explanations

**Firstness / Secondness:** Record provisioning rule output and transcript completeness. Contrast a claim of weak generated keys with the documented entropy and uniqueness requirements.

**Abduction:** The provisioning workflow accepts a prohibited low-entropy test secret or repeats a key across distinct lab devices.

**Competing benign explanation:** The visible value is an example configuration, while deployment generates unique secrets and rejects the fixture.

**Deduction:** The actual lab provisioning path accepts the prohibited fixture; a compliant secret succeeds and a deliberately invalid configuration is rejected by the same path.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Snapshot the lab configuration and identify where generation, validation and per-device assignment occur.

2. Submit the synthetic weak and compliant fixtures through the supported provisioning interface; cap attempts to the defined case set.

3. Associate the owned client normally, without induced disconnects; retain only the synthetic session transcript needed for validation.

4. If validating transcript parsing, compare verification using the supplied correct secret with one supplied wrong secret; do not run guessing campaigns.

5. Restore the original lab secret and prove authorized reconnection; report policy failure independently of transcript-parser behavior.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- Offline verification of a known lab key does not measure the cost of recovering an unknown production key.

- Handshake labels from conversion tools can hide incomplete or mixed-session frames.

- A PMKID is not the PSK, and a capture failure is not evidence that a network resists every offline test.

## Evidence and output

Provide the provisioning rule, synthetic case identifiers, accepted/rejected outputs, transcript digest and parser controls without exporting secret values.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Audit key provisioning exceptions, shared-key assignments and rotation events; distinguish collection traffic from offline analysis that has no network event.

Generate unique high-entropy credentials under a documented policy, restrict overrides and rotate exposed credentials through the normal lifecycle.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record AP/supplicant and parser versions and the exact supported transcript format. Confirm FT/PMKID behavior on the actual implementation before making a claim.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | The deployed provisioning path accepts the prohibited synthetic key while valid and invalid configuration controls behave correctly. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Only the example file contains the weak value; actual provisioning rejects it and assigns distinct generated keys. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A partial production handshake exists but provisioning behavior and secret provenance are unavailable. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wpa2-psk/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Preserves PSK, EAPOL, PMKID and roaming distinctions while replacing password recovery with synthetic provisioning and parser validation.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
