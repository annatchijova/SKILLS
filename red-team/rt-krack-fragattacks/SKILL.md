---
name: rt-krack-fragattacks
description: Assess key reinstallation and fragment-reassembly regression evidence using pinned laboratory conformance fixtures and non-sensitive canaries.
---

# Wi-Fi key-state and reassembly regression assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use an isolated AP/client, owned synthetic traffic, a pinned reviewed regression harness and known affected and fixed reference fixtures when available.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- A retransmitted handshake message is legitimate; reinstalling the same key with reset nonce or replay state is the disputed behavior.

- Packet-number reuse must be scoped to the same key and relevant traffic context; key rotation changes interpretation.

- Fragment caches must preserve security context and avoid accepting fragments across incompatible key or association state.

- Aggregation parsing and plaintext acceptance are distinct variants; one result does not confirm an entire CVE family.

## Observation and competing explanations

**Firstness / Secondness:** Record the exact variant, state transition, key-context identifier and canary delivery. Contrast with expected monotonic counters or reassembly rejection.

**Abduction:** The target resets replay or nonce state after a legitimate handshake retransmission in the same key context.

**Competing benign explanation:** A new key was negotiated or the capture merged multiple links or traffic contexts.

**Deduction:** The target repeats counter state under the same key context after the specific regression case; a no-retransmission control stays monotonic and a fixed reference rejects the condition.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Identify one variant and inspect the existing harness documentation and fixture behavior before execution.

2. Establish canary delivery and capture completeness using a normal exchange, without production payloads.

3. Execute the reviewed finite regression case inside the enclosure; inspect key-state instrumentation and endpoint receipts rather than a headline tool label.

4. For fragment variants, use the harness's inert marker and compare same-context acceptance with incompatible-context rejection; keep the variant results separate.

5. Restore the clean association, rerun the ordinary canary and retain failed as well as successful cases.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- KRACK evidence does not establish PSK recovery or arbitrary application plaintext access.

- A WPA3 or PMF label does not alone prove fragment processing is correct.

- Missing fragments, retransmission duplication and decoder errors can imitate counter or reassembly defects.

## Evidence and output

Provide per-variant case IDs, harness revision, key-context and counter records, capture digests, endpoint receipts and actual affected/fixed build evidence.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Evaluate telemetry for repeated key-state transitions and invalid reassembly; establish sensor visibility using the reference fixture.

Apply implementation-specific fixes for idempotent key installation and security-context-bound reassembly. Rerun the same failing case and normal retransmission compatibility controls.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record chip firmware, driver, supplicant and AP builds separately. Verify advisory applicability; release year and broad OS-family labels are not patch attestations.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Counter reset is instrumented in the same key context after the regression case, with monotonic baseline and fixed-reference controls. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The repeated counter belongs to a newly established key; same-key retransmission leaves state unchanged. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | The harness reports a variant name but key context, frame delivery and reference behavior are unavailable. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-krack-fragattacks/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Retains two implementation defect families with per-variant proof and rejects blanket patch claims, password-recovery implications and crafted-frame chains.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
