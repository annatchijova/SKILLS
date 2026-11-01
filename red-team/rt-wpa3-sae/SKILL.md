---
name: rt-wpa3-sae
description: Assess WPA3 SAE profile enforcement, transition policy and bounded authentication-resource behavior on isolated fixtures.
---

# SAE negotiation and resource controls

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated AP/client pair with controlled pure-SAE and transition profiles, known lab secrets, CPU telemetry and an association deadline. Resource tests need an explicit load ceiling.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- SAE authenticates before the subsequent key handshake; do not describe it as removing every four-way exchange.

- Transition advertisement permits multiple AKMs, but acceptance depends on the saved client profile and negotiated state.

- H2E advertisement is not proof that every implementation path is constant-time or that legacy fallback is disabled.

- Anti-clogging behavior, authentication quotas and scheduling affect legitimate association availability under bounded load.

## Observation and competing explanations

**Firstness / Secondness:** Record RSN/RSNXE advertisement, client policy and negotiated AKM separately. Compare them to the approved profile and service budget.

**Abduction:** A client configured to require SAE accepts a PSK-only lab profile without an approved policy change.

**Competing benign explanation:** The client profile intentionally permits transition mode, or the display is reporting advertised rather than negotiated security.

**Deduction:** With the SAE-only client profile unchanged, the PSK-only case establishes a data session; a compliant SAE association works and a mismatched secret is rejected.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Export client profiles and confirm an ordinary SAE association with server-side and client-side logs.

2. Change only the isolated AP authentication profile to the comparison case, without spoofing public networks or forcing nearby clients off APs.

3. Initiate one normal client connection per case and verify negotiated AKM and a harmless canary exchange.

4. For a separate resource hypothesis, use the vendor test harness below the agreed request and CPU ceiling; compare legitimate association latency with an idle control and stop at the ceiling.

5. Restore pure-SAE policy, clear test sessions and verify normal association. Keep negotiation and load findings separate.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A saved alternate profile can explain fallback; profile identity must travel with every result.

- Radio contention and CPU load can mimic timing leakage; no password-side-channel claim follows from raw latency variance.

- H2E support and a vendor version string alone do not prove patch status or resistance to all SAE defects.

## Evidence and output

Deliver profile diffs, AKM/session logs, supported group and H2E configuration, control outcomes and load-budget measurements where executed.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Monitor unexpected negotiated AKMs, profile changes and authentication saturation; verify useful alerts before resource limits are exceeded.

Enforce required AKMs on managed clients and APs, remove unauthorized fallback, update the affected implementation and validate bounded admission controls.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record supplicant/AP build, crypto library, firmware and certification/profile revision. Treat historical Dragonblood version claims as research leads requiring advisory verification.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | An unchanged SAE-required client completes a PSK session, with working SAE and wrong-secret controls. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The observed fallback uses a separately approved transition profile; the SAE-required profile refuses the PSK-only fixture. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | Only beacon H2E capability and uncalibrated timing samples are available. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wpa3-sae/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Replaces downgrade and flooding chains with negotiation-policy discriminators and measured resource controls; rejects universal patch and H2E claims.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
