---
name: rt-race-condition
description: "Red-team assessment of race-condition / TOCTOU boundaries: limit-overrun on balances, coupons, gift cards, votes, invites and 2FA attempts; single-packet-attack concurrency; database isolation-level gaps; and cloud/serverless concurrency (Lambda/Cloud Functions). Re-expressed as owned-fixture concurrency experiments with a bounded parallel request set, a sequential control and state inspection instead of live financial abuse."
---

# Race Condition Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's race-condition craft as scoped concurrency experiments: it names the vulnerable flows and primitives, confirming limit-overrun on owned fixtures with a bounded parallel set and a sequential control rather than draining real value.

## Scope and prerequisites

Target operations with a check-then-act over shared state: balance debit, coupon/gift-card redemption, one-per-user actions, 2FA attempt counters, inventory reservation, invite/seat grants. Use owned accounts and synthetic balances/coupons. Keep the parallel request count bounded and the value synthetic.

Declare target, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Mechanism and observation

Trace the window between the check (balance ok? coupon unused? attempts < N?) and the act (debit / mark used / increment), and whether it is atomic.

**Firstness:** Record the final state after N parallel requests vs after N sequential (e.g. a $10 gift card redeemed yields $X credited). **Secondness:** State the invariant (exactly-once, balance never negative, attempts capped) and the deviation. **Thirdness:** Infer a race only after the parallel run violates the invariant where the sequential run does not.

## Abduction and refutation

**Mechanism hypothesis:** The check and the act are not atomic, so concurrent requests each pass the check against the same pre-act state and all commit.

**Competing benign explanation:** A DB unique constraint / row lock / conditional update serializes them; idempotency keys dedupe; the requests did not actually overlap (no single-packet alignment); the apparent overrun is normal retry behavior.

## Deduction and controls

N sequential requests yield the correct single-use result (positive control); N parallel requests must yield the same if the operation is atomic. A confirmed race shows the invariant violated only under concurrency (e.g. a $10 card credits $N*10). Predeclare the invariant and the violating state. A unique constraint/lock/idempotency key holding under parallelism is a PASS control.

## Induction: bounded laboratory procedure

Owned accounts; synthetic value; bounded parallelism.

1. **Baseline (sequential control).** Perform the action N times sequentially; confirm the limit holds (one redemption, balance correct).
2. **Alignment.** Prepare N identical requests; use the single-packet attack (HTTP/2, last frames in one TCP segment) or synchronized release so they arrive together.
3. **Parallel run.** Release the bounded set simultaneously against the owned fixture; inspect the resulting state.
4. **Confirm the violation.** Compare parallel-run state to the sequential control (double-spend, over-redeem, attempt-cap bypass, oversell).
5. **Isolation probe.** Where relevant, test DB isolation-level behavior and conditional-write presence.
6. **Control.** Re-run sequentially to confirm the invariant holds absent concurrency.

Record results including refutations. Keep finding and control status separate. Keep the parallel count small and the value synthetic.

## Craft notes (leads)

Classic flows: parallel coupon/gift-card redeem, parallel withdrawals each seeing full balance, 2FA code submitted N times before the lockout counter increments, parallel invite-accepts granting extra seats, last-item oversell. The single-packet attack neutralizes network jitter so the window is reproducible. Cloud/serverless adds its own concurrency (Lambda reused connections, concurrent invocations, conditional-write absence). WebSocket handshake races and rate-limiter/CAPTCHA races are variants.

## Domain-specific failure modes

Without arrival alignment, a "race" is just sequential and will not reproduce — the single-packet/synchronized release is essential. A unique constraint or conditional update makes the flow safe regardless of app logic. Apparent duplicates can be client retries; confirm by state, not request count. Non-reproducible one-offs are CANDIDATE, not CONFIRMED.

## Evidence and deliverable

Provide the flow, the invariant, the sequential-control result, the parallel-run state violating it, the parallelism used, and any serialization control observed. Use synthetic value only. Attach minimal replay, expected/observed, rival explanation (locking/retry), falsifier, uncovered flows.

## Versions and tool limitations

Pin the app, DB and isolation level, and the HTTP client's single-packet support. Tools (Burp single-packet, Turbo Intruder) send real concurrent requests; keep counts bounded and value synthetic. No behavior was verified by this content; confirm the live flow first.

## Remediation and detection

Make check-and-act atomic: DB unique constraints, `SELECT ... FOR UPDATE`/row locks, conditional/compare-and-set updates, idempotency keys, and serialized critical sections. Add a regression running the parallel set and asserting the invariant. Detect bursts of identical operations on one resource within a tiny window.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The bounded parallel run violates the invariant (double-spend/over-redeem) where the sequential control holds: CONFIRMED; FAIL. |
| Benign refutation | A unique constraint / lock / idempotency key serializes the parallel run: REFUTED; PASS for the control. |
| Insufficient evidence | A one-off anomaly that does not reproduce under aligned parallelism: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-race-condition/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's vulnerable-flow catalog, single-packet-attack primitive and cloud/serverless concurrency craft, re-expressed as owned-fixture bounded-parallel experiments with a sequential control and state inspection, replacing live financial abuse with bounded invariant-violation proof.
