---
name: rt-api-abuse
description: "Red-team assessment of API-abuse boundaries: business-logic bypass via API chaining, GraphQL batching, pagination/cursor exploitation and sort/filter injection, webhook hijacking/SSRF, API transaction races, JWT manipulation, API-key leakage patterns, undocumented-endpoint discovery and algorithmic-complexity exhaustion. Re-expressed as scoped experiments on owned accounts and keys with bounded request sets and negative controls instead of live exfiltration or mass abuse."
---

# API Abuse Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's API-abuse craft as scoped experiments: it names the chaining, batching, webhook, JWT and discovery families, confirming each on owned accounts/keys with bounded request sets rather than exfiltrating real data.

## Scope and prerequisites

APIs expose logic and data directly; abuse combines legitimate calls in illegitimate orders or volumes. Use owned accounts and owned API keys; cap batch/pagination/complexity probes so a test does not become mass exfiltration or DoS.

Declare target, API style (REST/GraphQL/gRPC), attempt budget, stop condition. Source/spec-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Logic chaining** — skip payment, manipulate price/state/quantity (see `workflow-abuse-assessment`).
- **GraphQL** — introspection, depth/alias amplification, batched brute force (see `rt-graphql`).
- **Pagination** — oversized page size, cursor forging to reach arbitrary records, sort/filter injection.
- **Webhooks** — register an owned-server URL (SSRF), list to discover internal URLs.
- **Transaction races** — parallel calls (see `rt-race-condition`).
- **JWT** — alg confusion / none / kid / jku (see `token-trust-assessment`).
- **Key leakage** — repo search, client-bundle extraction, error-message leakage.
- **Discovery** — hidden params (Arjun), archive mining (ParamSpider), JS-bundle routes, predictable naming.
- **Complexity** — algorithmic-exhaustion endpoints.

## Mechanism and observation

Trace a sequence of calls to the invariant or control it bypasses.

**Firstness:** Record the state/data reached by the crafted sequence (an order confirmed unpaid; records returned past the owner boundary via a forged cursor; a webhook reaching your collector). **Secondness:** State the intended control (payment gating, per-owner scoping, rate/complexity limits) and the deviation. **Thirdness:** Infer the defect class only after a controlled sequence confirms it on owned fixtures.

## Abduction and refutation

**Mechanism hypothesis:** An endpoint trusts client-supplied order/values/cursors/tokens without server-side re-validation, or lacks per-operation limits, so a crafted sequence reaches data/state/volume it should not.

**Competing benign explanation:** The server re-validates each step and recomputes values; cursors are signed/scoped; rate limits count operations (defeating batching); the JWT is verified with the right algorithm and key; the "leaked key" is a public/test key.

## Deduction and controls

The legitimate call sequence behaves correctly (positive control). A confirmed finding reaches a forbidden state/record/volume via the crafted sequence where the control refuses. Predeclare the confirming artifact. Server-side re-validation / signed cursors / operation-count limits / correct JWT verification are PASS controls.

## Induction: bounded laboratory procedure

Owned accounts and keys; bounded sets.

1. **Baseline.** Run the legitimate flow; capture controls (auth, rate limits, cursor format).
2. **Chaining.** Reorder/skip calls; submit client values the server should recompute.
3. **Pagination/cursor.** Forge/modify a cursor and large page size against owned data; observe scope and volume (bounded).
4. **Webhook.** Register an owned-collector URL; confirm server-side fetch and whether internal URLs are listable.
5. **JWT/discovery/key.** Route JWT to `token-trust-assessment`; test discovery on owned endpoints; confirm any key is owned/non-production before use.
6. **Complexity (bounded).** Measure cost growth on a suspected endpoint; stop before impact.
7. **Control.** Confirm the legitimate flow and limits hold.

Record results including refutations. Keep finding and control status separate.

## Domain-specific failure modes

A reordered call the server re-validates is a refutation. A forged cursor that returns only owned records is not a scope break. Rate limits on HTTP requests are bypassed by batching, not more requests. A "leaked" key may be a public client key with no privilege. Complexity probes can DoS — keep them bounded.

## Evidence and deliverable

Provide the call sequence, the forbidden state/data/volume reached, the account/key context, and the control refusal. Use owned accounts/keys; keep real data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered endpoints.

## Versions and tool limitations

Pin the API framework and gateway versions. Discovery/complexity tools can exfiltrate or DoS; keep bounded and owned. No endpoint behavior was verified by this content; confirm the live API first.

## Remediation and detection

Re-validate every step and recompute values server-side, sign and scope cursors, enforce per-operation and complexity limits, validate webhook URLs (see `rt-ssrf`), verify JWTs with pinned alg/key, and rotate leaked keys. Add regressions for each bypass. Detect out-of-order sequences, cursor tampering, batched operations, and webhook registrations to internal/collector hosts.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A crafted sequence reaches a forbidden state/record/volume on owned fixtures where the control refuses: CONFIRMED; FAIL. |
| Benign refutation | Server-side re-validation / signed cursors / operation limits reject the sequence: REFUTED; PASS for the control. |
| Insufficient evidence | A reordered call with no confirmed forbidden effect: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/api/offensive-api-abuse/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's chaining, pagination, webhook-SSRF, JWT, key-leakage and discovery craft, re-expressed as owned-account/owned-key experiments with bounded request sets and negative controls, replacing live exfiltration and mass abuse with bounded proof. Composes with `workflow-abuse-assessment`, `rt-graphql`, `rt-race-condition`, `token-trust-assessment`, `rt-ssrf`.
