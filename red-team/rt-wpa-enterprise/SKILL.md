---
name: rt-wpa-enterprise
description: Validate EAP server trust, client certificate policy and assigned network roles with synthetic identities on a private 802.1X lab.
---

# Enterprise supplicant trust assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated AP, RADIUS service, private test CA and managed supplicant with disposable accounts. Prepare valid, wrong-name and untrusted-issuer server certificates without production identity material.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- Server trust requires the configured trust anchor and server identity policy; outer identity traffic does not reveal every inner EAP method.

- PEAP/TTLS tunnel establishment and inner authentication are distinct events; test whether sensitive inner authentication begins before required trust checks pass.

- EAP-TLS client certificate acceptance depends on issuer, usage, identity mapping and status policy, not possession of any certificate.

- Authentication success and authorization role assignment are separate boundaries; a valid test identity must receive only its mapped access.

## Observation and competing explanations

**Firstness / Secondness:** Record the deployed supplicant trust policy and the last completed EAP stage. Compare behavior with the expected server-name and trust-anchor requirements.

**Abduction:** The managed supplicant starts inner authentication against a server certificate that violates its configured identity policy.

**Competing benign explanation:** A user-approved test override or previously installed lab trust anchor explains the acceptance.

**Deduction:** The clean managed profile accepts the valid certificate but reaches inner authentication with a wrong-name certificate; the untrusted-issuer control and profile export isolate the missing check.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Verify device time and profile deployment; record trusted test anchors and remove only test-owned cached exceptions.

2. Complete one valid-certificate authentication and confirm the expected restricted role.

3. Change only certificate identity, then only issuer, with normal client reconnects; log protocol stage without collecting reusable secret responses.

4. Separately compare accepted and rejected synthetic client certificates against the RADIUS identity mapping; never export private keys.

5. Restore server configuration and profile state; confirm access and log correlation for the valid test identity.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- Missing XML fields can inherit defaults; configuration inspection alone cannot establish acceptance.

- Certificate prompts, tunnel establishment and completed inner authentication have different implications.

- A TLS inspection bypass deliberately installed in the test client invalidates claims about an unmodified managed profile.

## Evidence and output

Provide certificate fingerprints and public metadata, trust-profile revision, EAP stage, RADIUS role decisions and sanitized event correlation.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Collect supplicant validation failures and RADIUS authentication/role events; verify that wrong-name rejection is distinguishable from connectivity failure.

Deploy enforceable server identity and CA policies, eliminate unintended user overrides and bind certificate identity to least-privilege network roles.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record OS/supplicant, MDM profile schema, TLS and RADIUS versions. Verify method support and certificate-name matching against the installed implementation.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Wrong-name certificate reaches inner authentication under the unchanged managed profile while the valid path and issuer control behave as predicted. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Acceptance occurred only after an explicit lab override; the clean managed profile rejects the wrong-name certificate. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | Only EAP identity frames are available and no tunnel or client validation logs exist. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wpa-enterprise/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Preserves EAP method, PKI and network-role boundaries while removing credential capture, certificate theft and domain pivots.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
