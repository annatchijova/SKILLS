---
name: rt-iot
description: Assess firmware provenance, update validation, debug exposure and device authorization using supplied images and recoverable embedded lab fixtures.
---

# Embedded trust and recovery validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a spare non-actuating device, supplied firmware and documented recovery path. Keep analysis offline; unpack images in a sandbox without executing extracted binaries or privileged mounts.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- Image signatures, secure boot and anti-rollback enforce different points in the boot/update chain; one enabled feature does not prove the others.

- UART/JTAG/SWD accessibility depends on production lifecycle state and permissions; pad presence is not confirmed privileged access.

- Firmware strings and component banners require reachability and configuration evidence before becoming vulnerability findings.

- MQTT topic ACLs, CoAP resource authorization and cloud device ownership must be tested per principal, not inferred from network access.

## Observation and competing explanations

**Firstness / Secondness:** Record artifact digest, hardware revision, lifecycle state and update verifier decision. Compare the accepted image and version against the signed update and rollback policy.

**Abduction:** The production-equivalent update verifier accepts an image that fails the required signature policy.

**Competing benign explanation:** The fixture is in a documented development mode, or the UI stages the image but boot-time verification rejects it.

**Deduction:** The production-equivalent verifier marks the invalid test artifact executable while a valid signed reference succeeds and a deliberately wrong-device artifact fails.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Inventory supplied images and device state; record hashes and confirm recovery on the spare before changing state.

2. Analyze boot/update configuration and image metadata without running image contents. Separate public trust anchors from secret key material.

3. Use a vendor-supported validation-only harness with known valid and invalid fixtures; require verifier and activation decisions rather than an upload response.

4. If actual activation is separately authorized, use only the documented inert vendor test image on the spare; stop at abnormal power, boot or recovery behavior.

5. For service authorization, use one inert MQTT topic or CoAP resource with owner/other-device principals; restore configuration and verify boot and normal telemetry.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- High entropy does not distinguish compression from encryption without additional structure.

- A debug development build cannot establish exposure in shipped production lifecycle state.

- A staging success is not signature bypass; anti-rollback rejection is not signature failure. Keep these results separate.

## Evidence and output

Deliver image digests, chain-of-trust diagram, exact hardware/firmware revisions, verifier/activation logs, principal-resource decisions and observed recovery result.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate update rejection, rollback, debug-state and unauthorized-topic events; ensure telemetry survives a failed update without discarding audit records.

Verify signed images before activation, bind model/version policy, enforce rollback controls and production debug restrictions, and scope device identities to required resources.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record boot ROM/bootloader, RTOS/kernel, update library, analysis-tool and filesystem parser versions. Legacy package names and CVE strings are unverified leads.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Production-equivalent verifier accepts the invalid signature fixture for execution while valid and wrong-device controls isolate the signature failure. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Upload staging succeeds but the production verifier rejects the artifact before activation; only documented development mode accepts it. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A firmware string suggests a vulnerable package but no reachable service or exact build mapping is established. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/iot/offensive-iot/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Preserves hardware, firmware, update and IoT service boundaries while replacing chip-off, fault injection, destructive flashing and pivot chains with recoverable validation.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
