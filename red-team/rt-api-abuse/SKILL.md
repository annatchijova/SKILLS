---
name: rt-api-abuse
description: "Assess API operation accounting, cursor isolation and webhook delivery controls with small synthetic datasets and bounded workloads."
---

# API Consumption and Delivery Controls

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Separate consumption and delivery guarantees from endpoint authorization. Use the API boundary skill for method permissions, the workflow skill for business state, and the GraphQL skill for resolver execution.

Obtain a declared quota window, operation unit, pagination contract and webhook ownership policy. Provision two synthetic tenants, a handful of records and two owned callback collectors. Disable actual billing and external notifications.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace gateway counters through batch dispatch, worker queues and provider calls. For pagination, trace cursor decoding to tenant predicates; for webhooks, trace registration, verification, dispatch and retries.

**Firstness:** Record accepted operation counts, returned fixture IDs and delivery destination IDs. Compare these with quota units, tenant policy and registration state before inferring abuse.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A gateway counts envelopes while a worker performs several billable operations, or a cursor or queued delivery loses its tenant binding.

**Competing benign explanation:** A worker may reserve quota atomically, reapply the tenant predicate, or pin the verified destination despite a changed configuration. Public cursor metadata may intentionally reveal an approximate count.

## Deduction and controls

A small batch exceeding a deliberately tiny lab quota must be denied or partially admitted under the documented contract. A cursor from tenant A must not reveal tenant A records to B. A revoked destination must behave according to the documented in-flight delivery policy.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Set a tiny fixture quota and record its initial counter; submit a single allowed operation as a harness control.

2. Compare an equal number of operations delivered singly and in one supported batch. Read worker counters and durable effects, not only HTTP responses.

3. Transfer one fixture cursor between the two tenants; compare with a valid local cursor and an expired cursor.

4. Queue one synthetic webhook event, change or revoke its owned destination, and inspect the actual retry destination and signature verification.

5. Stop at the first policy violation or the predeclared operation budget. Drain only fixture jobs and verify counters reconcile.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A 429 after expensive work has already executed protects response volume but not cost. Cached pages can masquerade as cursor leakage; retries can masquerade as duplicate events. Distinguish intentional snapshot cursors from live pagination.

## Evidence and deliverable

Include quota unit/window, admitted versus executed counts, query tenant predicate, fixture cursor digests, event ID, destination version and retry ledger. Do not retain real API keys; inventory exposure locations using synthetic credentials.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record gateway, batch adapter and queue versions. Client retries and automatic pagination can silently multiply operations. Disable these or record each request. Schema discovery is not evidence of undocumented access.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Reserve cost before execution, bind cursors to authorized context, cap page size and scope webhook configuration updates. Pin or revalidate queued destinations according to a documented policy and deduplicate effects.

Correlate operation count with envelope count, cursor ownership denials and callback destination changes. Alert on executed work after quota denial, with fixture IDs for validation.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A two-operation batch executes twice under a one-operation lab quota despite a specified hard cap: CONFIRMED; FAIL. |
| Benign refutation | A foreign cursor is accepted syntactically but the query returns only caller-owned fixture rows: REFUTED for cross-tenant disclosure; PASS for that case. |
| Insufficient evidence | Only rate-limit headers were captured and worker effects are unavailable: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/api/offensive-api-abuse/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains the upstream's pagination, batching, webhook and cost mechanisms as a distinct consumption/delivery assessment; routes JWT and workflow overlap to their dedicated skills.

