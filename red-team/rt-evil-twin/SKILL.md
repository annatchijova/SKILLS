---
name: rt-evil-twin
description: Evaluate saved-network selection and application trust on isolated lookalike AP fixtures without phishing or credential collection.
---

# Lookalike access-point trust validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a shielded or otherwise contained lab with two distinct test AP identifiers, one owned client, synthetic saved profiles and a local HTTPS canary. Disable external routing.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- SSID equality is a discovery hint, not proof of AP identity; saved authentication profiles determine whether a client can join.

- Joining an open network and trusting its application endpoints are separate security decisions.

- Captive portal detection can legitimately request cleartext connectivity probes; this does not prove application TLS compromise.

- User choice, automatic association and roaming are different triggers that need separate records.

## Observation and competing explanations

**Firstness / Secondness:** Record the saved-profile identity, association trigger, selected BSSID and canary TLS result. Compare them to the approved auto-join and endpoint-trust policies.

**Abduction:** A managed client automatically joins an unapproved open test AP under a profile that requires authenticated access.

**Competing benign explanation:** The user explicitly selected a separate open profile, or a connectivity probe was mistaken for sensitive application traffic.

**Deduction:** With the required profile unchanged and no user selection, association and canary receipt occur on the unapproved fixture; an authenticated reference works and an unrelated SSID is ignored.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Record clean saved-profile state and establish the intended authenticated connection.

2. Present the second lab fixture through the supported AP management interface; do not clone a production network or coerce reconnections.

3. Observe a normal scheduled client scan and association attempt for the agreed interval, without portals requesting secrets.

4. Separately test the canary endpoint with valid and wrong-name test certificates; verify whether the application transmits its synthetic marker.

5. Remove test profiles and AP advertisements, restore client networking and retain association and TLS evidence.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A stronger signal alone does not guarantee selection; profile history and user actions matter.

- An HTTP connectivity check is not an application-secret disclosure.

- Installing a trusted interception CA changes the threat model and must not support a stock-client trust claim.

## Evidence and output

Provide profile revisions, user-action timeline, association logs, endpoint certificate metadata and marker receipts without collecting credentials.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate detection of unapproved test APs and unexpected auto-join events, then correlate endpoint trust failures with the same session.

Restrict automatic joining, deploy authenticated managed profiles and enforce application TLS validation. Keep portal interactions separate from enterprise credential entry.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record client OS, wireless driver, profile management and portal subsystem versions. Do not inherit claims that every modern client responds to KARMA or that address randomization proves anonymity.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | An unchanged authenticated-only profile automatically establishes the disallowed open session; reference and unrelated-SSID controls work. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Only a manually selected open profile connects; the managed profile refuses the fixture and the canary rejects wrong-name TLS. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A probe request is observed but no association or application transaction is recorded. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-evil-twin/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Recasts evil-twin and portal material as client selection and endpoint trust measurement, excluding credential harvesting, coercion and tracking.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
