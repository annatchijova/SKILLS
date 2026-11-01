---
name: rt-data-exfiltration
description: "Measure data-loss controls using synthetic canaries and owned receivers, separating transfer completion from detection."
---

# Synthetic Data Egress Validation

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Validate whether a stated egress rule blocks or detects a public dummy artifact. Never collect
production data, credentials or session material; do not implement covert transports.

- destination and tenant restrictions.
- content classification and encryption visibility.
- sender-receiver integrity reconciliation.

## Preconditions and baseline

Create a synthetic fixture whose digest, byte count and classification label are known. Specify
whether the classifier matches labels, content or both.

Use an owned sender and receiver on a lab route. Name the destination tenant as well as the hostname
when a SaaS endpoint is involved.

Set byte/request limits and an ingestion deadline. Verify receiver logging with an explicitly
permitted fixture before evaluating a prohibited transfer.

## Discriminating laboratory procedure

Abduction: destination allowlisting permits a prohibited tenant or unclassified content. Rival: the
fixture lacks the configured sensitive-data pattern or policy is audit-only.

Deduction: a correctly classified dummy fixture should be denied on the forbidden route while an
allowed fixture reaches the same owned receiver.

Induction: send one bounded fixture through the supported application path and compare sender
disposition with receiver digest and bytes received.

Change only classification or destination tenant for the paired control. Preserve gateway and DLP
decisions for both.

For encrypted or opaque traffic, report whether the control can inspect content or only metadata.
Use supplied trace fixtures for DNS/ICMP/covert-channel analytics rather than building transport
tools.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- An HTTP success response may precede asynchronous rejection; confirm final receiver state.
- A shared SaaS hostname can host both allowed and prohibited tenants; hostname-only evidence cannot
  establish tenant isolation.
- No DLP alert may mean prevention happened upstream or the classifier never matched. Separate
  generation, inspection, prevention and alerting.

## Evidence and verdict

Deliver fixture manifest, destination ownership, route, classification evidence, receiver digest,
actual bytes, policy mode and correlated alert artifacts.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require destination identity and classifier decisions in egress logs. Prefer tenant restrictions and
supported DLP enforcement; retest allowed business transfers to detect overblocking.

## Recovery

Remove only dummy receiver objects and test grants after retaining digests and decision logs. Verify
the fixture cannot be fetched after teardown.

## Versions and tool limits

Record DLP engine, policy revision, client and proxy versions. TLS inspection, file-size limits and
SaaS API coverage must be established for the installed deployment.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Classified dummy object reaches a forbidden owned tenant with matching digest despite enforced policy | CONFIRMED egress control failure; FAIL |
| Fixture was never classified and a correctly classified control is blocked | REFUTED classifier-bypass claim; PASS for tested classifier |
| Sender reports success but receiver and policy logs are unavailable | CANDIDATE transfer; WARN |

## Provenance and treatment

Upstream research source: `Skills/post-exploitation/offensive-data-exfiltration/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Replaces covert channels and data staging recipes with bounded synthetic-data transfer and control
measurement.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

