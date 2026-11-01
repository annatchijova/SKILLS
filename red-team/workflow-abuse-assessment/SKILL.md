---
name: workflow-abuse-assessment
description: Test business workflow invariants across retries, concurrent requests and role changes. Use for payment, quota, approval, invitation and webhook state-machine reviews.
---

# Workflow Abuse Assessment

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Model before probing
Write states, permitted transitions, actors, preconditions and side effects. State conservation properties using integers or exact fractions: a refund cannot exceed the captured amount; replay cannot apply a debit twice.
Identify transaction, queue and external-provider boundaries. Use fixture balances and a sandbox provider.

## Experiments
Test skipped steps, reordered events, duplicate delivery, stale authorization and partial failure independently. Inspect durable state, not only the response.
For races, coordinate two workers at the suspected check/use boundary and record the schedule. Compare with serial execution. Bound concurrency, time and total attempts.
Inspect idempotency scope: same key and body should preserve the promised result; same key with a different body must follow the documented conflict policy; keys should not collide across principals.
Test failure between local commit and remote acknowledgement, then redelivery. Distinguish at-least-once delivery from duplicate business effect.

## Refute and deliver
Test the innocent explanation: a unique constraint, transaction isolation, provider deduplication or compensating action already prevents the alleged loss.
Report the shortest violating sequence, before/after state, interleaving, logs and exact invariant. Bound demonstrated impact to the fixture; do not extrapolate arbitrary financial totals.
Propose a regression sequence and an atomicity or reconciliation change at the responsible boundary. Cleanup only test-owned artifacts.

## Required methodology and fixture contract

Read [the assessment methodology](../METHODOLOGY.md) before execution.
Use synthetic orders, integer minor-unit amounts, explicit currency and a sandbox provider with no real settlement.
Declare the maximum events, attempts, worker count and reconciliation interval before running.
Firstness records the exact state delta; Secondness compares it with an explicit conservation or transition rule.
Thirdness identifies the absent atomicity, authorization or reconciliation rule only after the controlled experiment.
No CAPTCHA defeat, identity rotation, fraud-control evasion or real reward redemption belongs to this procedure.

## Discriminator: acknowledged effect versus durable effect

**Abduction:** a local retry reissues an external business effect after an acknowledgement is lost.
**Benign rival:** provider deduplication or reconciliation already guarantees a single settled effect even if multiple requests are logged.
**Deduction:** a repeated event with the same scoped operation identity must preserve the promised final ledger state.
**Induction:** execute one ordinary fixture transaction, then reproduce a lost acknowledgement with the sandbox's supported fault hook.
Redeliver the same fixture event once; compare application records, outbox entries and provider ledger after the declared settling interval.
Use a no-fault replay as the negative-condition control and a legitimate distinct operation as the acceptance control.
A double response or duplicate delivery is not a duplicate business effect.
If the settling interval or provider ledger is unavailable, retain a CANDIDATE result rather than declaring financial loss.

## Additional business mechanisms

- Price authority: compare a server-calculated fixture total with a client-submitted amount; the server must follow the documented authoritative source.
- Currency: carry amount and currency together; use fixed fixture conversion rules and exact arithmetic where conversion is part of the contract.
- Partial returns: assert cumulative refunds do not exceed the captured eligible amount for returned fixture items.
- Promotions: distinguish intentionally stackable discounts from violation of an explicit exclusivity rule.
- Entitlements: test one upgrade and downgrade sequence against the documented effective time and cache invalidation interval.
- One-time actions: compare a consumed invitation or coupon with an unused fixture, observing durable effects rather than only status.
- State rollback: test whether a finalized fixture can return to an editable state and whether prior side effects are reconciled.
- Authorization changes: inspect whether delayed workers use the required current or captured permission context; document that policy first.

## Evidence and tool limitations

Deliver a state-transition diagram or table, exact invariant, initial/final ledger and event IDs.
Include idempotency key scope, body identity, provider acknowledgement and compensation timeline.
Pin application, queue, database and sandbox-provider versions plus retry and isolation settings.
No runtime tools were executed for this rewrite; a payment emulator cannot prove a real provider's settlement semantics.
A sandbox may omit dispute or delayed-settlement behavior; mark those paths NOT TESTED.
Bound monetary impact to the synthetic violated invariant without multiplying it by imagined scale.

## Remediation and detection

Enforce state transitions and authoritative pricing server-side, with idempotency tied to actor and operation.
Use transactional event publication and explicit reconciliation across non-atomic provider boundaries.
Add assertions for conservation, duplicate-effect keys and forbidden entitlement transitions.
Correlate business event IDs with provider operation IDs; alert on actual invariant violations.
Verify the regression under replay and fault injection, not only the normal happy path.
Restore fixture balances and subscriptions and drain test events without deleting the audit trail.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| One captured synthetic order receives two settled refunds exceeding its eligible amount after a single controlled redelivery. | CONFIRMED; FAIL for the refund invariant. |
| Two successful responses resolve to one provider operation and one settled ledger effect under documented idempotency. | REFUTED for duplicate settlement; PASS. |
| Two requests were accepted but provider settlement and reconciliation state were not inspected. | CANDIDATE; WARN. |

Acceptance cases specify expected behavior; they are not executed target tests.

## Provenance

Exact upstream path: `Skills/web/offensive-business-logic/SKILL.md`.
Treatment: Strengthens economic and lifecycle invariants using exact synthetic ledgers while excluding fraud evasion and speculative scaling; schedule mechanics remain in rt-race-condition.

Methodology adapted from Claude-Red `offensive-business-logic` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

