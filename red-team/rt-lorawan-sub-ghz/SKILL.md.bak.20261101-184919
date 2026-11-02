---
name: rt-lorawan-sub-ghz
description: Validate LoRaWAN session/counter handling and proprietary sub-GHz command freshness using contained test networks and inert receivers.
---

# LoRaWAN and sub-GHz freshness assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a private network/application server, owned node and inert counter receiver inside RF containment. Use synthetic keys, no public network identifiers and no connected actuators.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- LoRa is a physical modulation; LoRaWAN adds activation, integrity, counters and key roles. Proprietary LoRa framing need not implement LoRaWAN.

- OTAA and ABP have different session lifecycles; nonce, frame-counter and key semantics depend on the protocol revision.

- Repeated delivery across gateways or confirmed-message retries is not necessarily duplicate application processing.

- For proprietary receivers, identical transmitted bits alone do not establish acceptance of a stale command; the receiver's freshness state is the oracle.

## Observation and competing explanations

**Firstness / Secondness:** Record session identifier, protocol version, counter, join state and application receipt ID. Contrast radio receptions with distinct accepted application operations.

**Abduction:** A server or receiver processes a previously accepted synthetic operation again after a device reboot that should preserve freshness state.

**Competing benign explanation:** Multiple gateways reported the same reception but the application deduplicated it, or a new authorized session permits the new operation.

**Deduction:** The same-session stale fixture increments the application counter twice after restart; a fresh operation succeeds and an unchanged-session stale control is rejected before restart.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Record session and persistent counter state, then send one normal test operation to establish a single application receipt.

2. Use the vendor's offline integration harness to resubmit the previously accepted synthetic fixture without constructing over-air payloads.

3. Restart only the disposable node or receiver using supported controls and repeat the same bounded fixture while retaining session identity.

4. Compare transport delivery, network-server rejection and application-side deduplication; for proprietary protocols use an inert simulator with equivalent persistent state.

5. Restore node/session configuration and confirm fresh traffic works without accepting the stale fixture.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A join request is not simply an encrypted packet; avoid importing the source's blanket key and encryption descriptions.

- A counter reset under a new session is different from reuse under the same key context.

- Region, modulation and decoder support constrain observations; inability to decode is not evidence of encryption strength.

## Evidence and output

Provide protocol/session revision, counter persistence records, duplicate receipt identifiers, receiver state and harness fixture digests; omit key values.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate alerts for rejected stale counters, repeated join state and application duplicates; correlate gateway copies instead of counting each as a new attack.

Persist freshness state correctly, enforce session separation and application idempotency, use device-unique keys and document safe reactivation.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record LoRaWAN regional parameters, stack/server revisions and ABP/OTAA mode. Verify SDR/decoder support offline; do not copy regional frequency permissions from source tables.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Same-session stale fixture increments the application counter again only after restart, while fresh and pre-restart controls work. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Several gateways report one frame but the application records exactly one operation and rejects the stale fixture. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | Only undecoded RF samples exist; session identity and receiver effects are absent. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-lorawan-sub-ghz/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Separates LoRaWAN session semantics from proprietary receiver freshness and removes key extraction, downlink injection and access-control replay recipes.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
