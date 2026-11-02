---
name: workflow-abuse-assessment
description: "Red-team assessment of business-logic and workflow boundaries: state-machine step-skipping and replay, price/quantity/currency and coupon manipulation, refund/chargeback/payout abuse, tenant/role boundary and mass-assignment, and logic-level race conditions. Re-expressed as scoped experiments on owned accounts and synthetic value that reconstruct the intended state machine and prove a prohibited transition with negative controls, not live financial abuse."
---

# Workflow and Business-Logic Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's business-logic craft as scoped experiments: it reconstructs the intended state machine and tests prohibited transitions on owned accounts with synthetic value, rather than extracting real money.

## Scope and prerequisites

Business-logic flaws are not payload bugs — they are allowed operations in a disallowed order or combination. First build the intended state machine (the legitimate flow and its invariants), then test transitions it should forbid. Use owned accounts and synthetic balances/coupons/inventory.

Declare target, the flows in scope, attempt budget, stop condition. Source-only or spec-only authorization yields a hypothesis marked NOT TESTED. Monetary extraction is an impact class to demonstrate with synthetic value on an owned instance, bounded.

## Attack surface and classes

- **State-machine bypass** — skip a required step, replay a one-time action, downgrade state, invoke an endpoint directly out of order.
- **Value manipulation** — negative/zero/float quantities, hidden price fields, currency confusion, coupon stacking/reuse/negative discount, cart SKU tampering.
- **Refund/payout abuse** — refund more than paid, refund to a different method, payout-account race.
- **Identity/tenant/role** — tenant-ID substitution, role confusion via multipart/HPP, mass assignment, indirect privilege via object linking.
- **Logic races** — parallel coupon/withdraw/redeem/2FA (see `rt-race-condition`).

## Mechanism and observation

Map the state machine, then trace each transition's server-side enforcement.

**Firstness:** Record the state reached and the value computed after a crafted sequence (e.g. order confirmed without a payment step; total went negative). **Secondness:** State the invariant the flow should enforce (payment precedes fulfillment; total >= 0; one redemption per coupon) and the deviation. **Thirdness:** Infer the defect class only after a controlled prohibited transition succeeds.

## Abduction and refutation

**Mechanism hypothesis:** The server enforces the workflow only through UI sequencing or client-side values, so a direct or reordered request reaches a state/value the business rules forbid.

**Competing benign explanation:** The server re-validates every precondition (rejects the out-of-order call); prices/totals are recomputed server-side from trusted data (client values ignored); idempotency blocks replay; tenant/role is derived from the session, not the payload.

## Deduction and controls

The legitimate flow produces the correct state/value (positive control). A confirmed finding reaches a forbidden state/value via a crafted sequence where the control is rejected. Predeclare the violated invariant and the state that proves it. Server-side re-validation / recomputation / idempotency rejecting the crafted request is a PASS control.

## Induction: bounded laboratory procedure

Owned accounts; synthetic value.

1. **Reconstruct the state machine.** Enumerate steps and endpoints (including internal/undocumented ones from JS bundles, OpenAPI/Swagger). Record invariants.
2. **Step-skip / replay / downgrade.** Jump directly to a later step, replay a one-time action (refund/redeem) for idempotency, or move state backward; observe server enforcement.
3. **Value manipulation.** Submit negative/zero/float quantities, edit hidden price/discount fields, mismatch currency, stack/reuse coupons, tamper SKU — on synthetic items.
4. **Refund/payout.** Test refund > paid, refund to a different method, payout-account change timing — synthetic amounts only.
5. **Tenant/role.** Substitute tenant ID in a hidden field, add `role`/`owner` via mass assignment, link objects to bypass a role check.
6. **Logic race.** Route parallel-redeem/withdraw cases to `rt-race-condition` with a bounded set.
7. **Control.** Run the legitimate flow and confirm the invariant holds.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Compare authenticated vs unauthenticated JS bundles for buried admin routes; API specs list endpoints the UI never calls. Classic invariants to probe: payment-before-fulfillment, non-negative totals, one-time coupon/refund, per-tenant isolation, seat/quota caps. Negative-discount and coupon-stacking turn a discount into a surcharge-that-reduces-total. Single-packet parallel requests expose "one per user" checks. Free-trial/referral loops abuse non-unique identity (email aliasing, VOIP numbers, device-ID reset).

## Domain-specific failure modes

Server-side recomputation of price/total makes client tampering inert — report that as a control. An out-of-order call that the server re-validates is a refutation. Reaching a "weird" state is only a finding if it violates a real business invariant with impact; name the invariant and the loss. Synthetic value only — do not extract real money to "prove" it.

## Evidence and deliverable

Provide the reconstructed state machine, the crafted sequence, the forbidden state/value reached, the violated invariant, and the control rejection. Use synthetic value and owned accounts. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered flows.

## Versions and tool limitations

Business logic is app-specific; there is no generic tool verdict — reason from the state machine. No flow behavior was verified by this content; reconstruct the live workflow first.

## Remediation and detection

Enforce every precondition and value server-side (recompute totals from trusted data, re-check state transitions, idempotency keys for one-time actions, derive tenant/role from the session, allowlist writable fields). Add regressions asserting each prohibited transition is rejected. Detect out-of-order transitions, negative/float values, and repeated one-time actions.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A crafted sequence reaches a forbidden state/value (order without payment, negative total, double refund) on owned fixtures where the control is rejected: CONFIRMED; FAIL. |
| Benign refutation | The server re-validates/recomputes and rejects the crafted request: REFUTED; PASS for the control. |
| Insufficient evidence | An unusual state with no violated invariant or impact: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-business-logic/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's state-machine, value-manipulation, refund-abuse and tenant-boundary craft, re-expressed as owned-account experiments with synthetic value that prove a prohibited transition against a reconstructed invariant, replacing live financial abuse with bounded logic-violation proof.
