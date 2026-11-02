---
name: rt-race-condition
description: "Test application atomicity and idempotency with controlled two-worker schedules, serial controls and durable state assertions."
---

# Concurrent State Transition Validation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Concentrate on schedules and shared-state protection. Workflow-abuse-assessment defines broader business invariants; this skill establishes whether concurrency breaks a specific invariant.

Use synthetic balances, quotas or unique records in a disposable datastore. Record isolation level, unique constraints, retry policy and external deduplication; set worker and attempt budgets before running.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Locate read/check, conditional write, commit, external acknowledgement and retry boundaries. Identify whether a process lock protects all writers or only one instance.

**Firstness:** Record operation intervals, observed versions and final durable state. Compare with a serial execution of the same operations and an exact invariant such as one allocation per fixture.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** Two operations observe the same eligible state and both commit a forbidden effect because the invariant is not enforced atomically.

**Competing benign explanation:** A unique constraint, conditional update, serialization retry or provider deduplication may prevent duplicate effects even when responses both report success. A duplicate response is not necessarily a duplicate transaction.

## Deduction and controls

The selected interleaving violates the invariant under the weak boundary while serial execution and an enforced atomic guard preserve it.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Run the operation serially twice and record results, database rows and any synthetic provider ledger.

2. Use a lab barrier at the suspected check/write boundary with two workers; record the actual schedule rather than assuming parallel dispatch overlaps.

3. Release both workers within a fixed timeout and inspect durable state after all documented retries or compensations settle.

4. Repeat with the atomic guard enabled or a serial schedule, keeping data and operation inputs identical.

5. Test one lost-acknowledgement/redelivery case separately; reset fixture state and verify reconciliation without deleting audit evidence.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

Connection pools can serialize requests and hide the window. Wall-clock timestamps do not prove happens-before. Instrumentation can widen a window; disclose this and distinguish reachable logic from demonstrated production timing.

## Evidence and deliverable

Deliver the invariant, operation IDs, schedule, read/write versions, transaction outcome, retry count and final effect ledger. Record unsuccessful schedules and total attempts rather than only a winning run.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin database and driver versions, isolation configuration and worker deployment topology. Parallel-request features do not guarantee server concurrency; single-packet tooling is unnecessary for a controlled schedule.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Enforce invariants with conditional writes, constraints or suitable transactions; scope idempotency to actor and operation. Use an outbox or reconciliation policy at external boundaries and verify retry correctness.

Correlate duplicate effect keys, constraint conflicts, serialization retries and lease expirations. Alert on invariant violations rather than every concurrent request.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Two controlled workers commit two allocations for a fixture limited to one, while serial execution preserves one: CONFIRMED; FAIL. |
| Benign refutation | Both calls return success but share one transaction ID and one durable effect under documented idempotency: REFUTED; PASS. |
| Insufficient evidence | Concurrent requests were sent but no overlap or durable effect evidence exists: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-race-condition/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Replaces amplification and pool-exhaustion recipes with schedule-controlled atomicity, write-skew and redelivery analysis.

