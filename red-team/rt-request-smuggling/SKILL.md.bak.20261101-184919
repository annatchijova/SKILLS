---
name: rt-request-smuggling
description: "Measure request-boundary agreement across isolated HTTP proxies and backends with inert conformance fixtures and connection-level traces."
---

# HTTP Framing Agreement

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess parser agreement in an isolated chain. Never test ambiguous framing on shared production connections or supply a queued request targeting another user.

Clone the relevant proxy/backend configuration into a dedicated lab with no real traffic. Obtain owner-approved inert framing fixtures, per-hop captures and a strict connection/time budget.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Record each protocol hop, TLS termination, HTTP version translation, buffering policy, upgrade path and backend connection reuse. An advertised HTTP/3 endpoint does not imply backend desynchronization.

**Firstness:** Count parsed request boundaries and associate each response with a fixture request ID on each hop. Compare with the expectation that both endpoints agree on message completion.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** The front and back parsers disagree about message length or completion and associate subsequent inert messages with different boundaries.

**Competing benign explanation:** A timeout may be expected rejection, buffering, connection closure or an incomplete fixture. A client may normalize ambiguity before transmission.

## Deduction and controls

A conformance case yields a reproducible parser-boundary difference on the same bytes; an ordinary request sequence preserves one-to-one association. Rejection that closes the connection must not be called smuggling.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Run two ordinary inert requests over the lab connection and establish matching request/response IDs at both hops.

2. Replay one approved non-destructive framing conformance fixture and capture bytes before normalization and after each protocol translation.

3. Compare parser events and connection closure; do not infer disagreement solely from timing or status.

4. Test a second inert fixture message on the same dedicated connection only when allowed by the lab harness; observe response association.

5. Repeat with connection reuse disabled as a diagnostic control, then close lab connections and verify no queued fixture work remains.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A proxy may rewrite length metadata safely. Different HTTP versions require different framing rules; do not transpose HTTP/1 assumptions onto HTTP/2 or HTTP/3. Scanner heuristics can confuse slow backends with disagreement.

## Evidence and deliverable

Deliver topology/configuration digest, protocol versions, byte captures, parser boundary events, connection IDs and response association. Treat captures as evidence and omit operational malicious framing recipes from reports.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin proxy, backend and client builds plus buffering/translation settings. Inspect replay-tool normalization and protocol support. Historical server/version tables are leads, not current proof.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Reject ambiguous framing consistently, align front/back parser policy and close unsafe connections. Verify translation behavior and regression-test the exact failed inert case across supported hops.

Correlate framing rejections, unexpected backend request counts, response association errors and connection resets. Validate signals against the baseline to avoid alerting on ordinary timeouts.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Identical captured bytes produce different request boundaries and misassociate two inert lab responses: CONFIRMED; FAIL. |
| Benign refutation | Both parsers reject the ambiguous fixture and close the connection with no queued message: REFUTED; PASS. |
| Insufficient evidence | A scanner reports only a timeout without per-hop bytes or parser events: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-request-smuggling/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains desynchronization, connection reuse and protocol translation analysis without smuggled payload construction, queue poisoning or bypass guidance.

