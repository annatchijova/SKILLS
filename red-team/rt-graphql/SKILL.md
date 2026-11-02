---
name: rt-graphql
description: "Red-team assessment of GraphQL boundaries: introspection and blind schema reconstruction, resolver authorization gaps (node-ID IDOR, nested and mutation auth), injection through resolver arguments (SQL/NoSQL/SSRF), batching/alias abuse, query-depth/complexity DoS, subscription and CSWSH, and verbose-error/field-suggestion oracles. Re-expressed as owned-schema experiments with bounded cost limits and negative controls instead of production brute force."
---

# GraphQL Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's GraphQL craft as scoped experiments against an owned schema and fixtures, naming the attack families while keeping batching/DoS probes bounded and authorization tests on owned accounts.

## Scope and prerequisites

Locate the GraphQL endpoint(s) and transport (POST, GET, WebSocket). Use owned accounts across privilege levels and a disposable instance. Cap batch sizes and query depth in your own probes so a DoS test does not become a DoS.

Declare target, server implementation (Apollo, Yoga, Hasura, graphql-java, ...) and version, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Schema disclosure** — introspection on, or blind reconstruction via field-suggestion/error oracles.
- **Authorization** — node-ID IDOR, nested-object auth gaps (checks only at top level), mutation auth, cursor/pagination leakage.
- **Injection via resolvers** — SQL/NoSQL in variable-backed resolvers, SSRF via URL arguments, directive injection.
- **Batching abuse** — alias/batch to brute-force credentials/OTP past per-request rate limits.
- **DoS** — depth bombs, alias amplification, circular fragments, incremental-delivery abuse.
- **Subscriptions** — unauthenticated subscribe, stale-token long-lived connections, cross-site WebSocket hijacking.

## Mechanism and observation

Trace a query to its resolvers and the authorization/validation performed per field.

**Firstness:** Record the response to a scoped probe (schema fields returned, a foreign object returned, a batch accepted). **Secondness:** State the intended policy (introspection off in prod, ownership enforced per resolver, batch limits) and the deviation. **Thirdness:** Infer the defect class only after a controlled probe confirms it with owned accounts.

## Abduction and refutation

**Mechanism hypothesis:** Authorization is enforced at the top-level resolver or HTTP layer but not at every nested resolver, and cost/batch controls are absent — so a crafted query reaches data or amplifies work it should not.

**Competing benign explanation:** Introspection is disabled and the schema came from docs; the "foreign" object is actually owned by the test account; a persisted-queries allowlist blocks arbitrary queries; depth/complexity limits reject the bomb; the resolver parameterizes the query.

## Deduction and controls

An owned-object query succeeds (positive control); a cross-account query must be refused if authz holds. A confirmed IDOR returns another owned account's object via its node ID where the control refuses. Predeclare the object/field that confirms it. Depth-limit/complexity/persisted-query controls rejecting a probe are PASS controls.

## Induction: bounded laboratory procedure

Owned accounts and schema; bounded probes.

1. **Baseline.** Authenticate as a normal owned account; run a legitimate query.
2. **Schema.** Try introspection (`__schema`, `__type`); if disabled, probe field-suggestion/verbose errors as a reconstruction oracle.
3. **Authorization.** With account A's token, request account B's (owned) object by node ID; test nested paths that top-level checks miss; test mutations.
4. **Resolver injection.** In variable-backed arguments, run the `rt-sqli`/SSRF discriminators against owned fixtures.
5. **Batching (bounded).** Submit a small aliased/batched set (e.g. a handful) to show per-request rate limits are bypassed; do not run a real brute force.
6. **DoS (bounded).** Demonstrate a modest depth/alias amplification and measure cost growth; stop before impact.
7. **Subscriptions.** Test `connection_init` auth, token expiry on a live connection, and Origin enforcement for CSWSH.
8. **Control.** Confirm owned-only queries behave and any cost/persisted-query control holds.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Node-global-IDs often Base64-encode `Type:id` — decode to enumerate. Field suggestions ("did you mean ...") leak schema even with introspection off. Hasura/Apollo have implementation-specific metadata and error leaks. Incremental delivery (`@defer`/`@stream`) and circular fragment spreads are amplification primitives. CSWSH applies when the WS handshake trusts cookies without Origin checks.

## Domain-specific failure modes

Introspection off is not authorization — data can still leak via suggestions. A "foreign" object may be the test account's own; verify ownership. Rate limits counted per HTTP request are bypassed by batching, not by more requests. A depth limit can block the bomb while nested-auth gaps remain — they are separate findings.

## Evidence and deliverable

Provide the endpoint, the query/mutation, the account context, the response proving the gap, the bounded cost measurement (for DoS), and any control that held. Keep real user data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered resolvers.

## Versions and tool limitations

Pin the GraphQL server and version; cost/limit middleware (GraphQL Armor, depth/complexity plugins) changes verdicts. Tools default to full introspection and aggressive batching; keep probes bounded. No server behavior was verified by this content; confirm the version first.

## Remediation and detection

Disable introspection and suggestions in prod, enforce ownership at every resolver (not just top level), parameterize resolver queries, limit depth/complexity/alias/batch, use persisted queries, re-validate subscription tokens and enforce Origin, and return generic errors. Add a regression asserting a cross-account query is refused. Detect `__schema`/`__type` in prod logs and abnormal alias/batch counts correlated to the token.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A query returns another owned account's data, or a bounded batch bypasses the per-request limit, where the control is refused: CONFIRMED; FAIL. |
| Benign refutation | Nested resolver enforces ownership / depth limit rejects the bomb: REFUTED for the tested path; PASS for the control. |
| Insufficient evidence | Introspection is on but no authz or injection gap is shown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-graphql/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's introspection, resolver-authorization, injection, batching, DoS and subscription attack families, re-expressed as owned-account/owned-schema experiments with bounded cost probes and negative controls, replacing production brute force and uncapped amplification with bounded proof.
