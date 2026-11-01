---
name: rt-graphql
description: "Assess GraphQL resolver authorization, batching cost, pagination and subscription revalidation using a supplied schema and small synthetic graphs."
---

# GraphQL Resolver and Work Accounting

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Focus on GraphQL execution semantics. Introspection visibility is an inventory fact unless a specific confidentiality policy prohibits it.

Obtain the schema or an approved schema subset, two test identities, a small object graph and documented operation/depth/cost limits. Establish a tiny lab budget and subscription timeout.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace root and nested resolvers, global node lookup, data-loader cache keys, tenant filters and subscription event filtering. Distinguish HTTP envelopes, operations, aliases and actual resolver work.

**Firstness:** Record returned fixture IDs, per-resolver invocation counts and subscription events, including partial data and field errors. Compare with field policy and declared cost.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** Authorization runs only at a root field, while a nested node or shared loader returns another tenant's object; alternatively accounting charges one envelope for several costly resolutions.

**Competing benign explanation:** Public nodes may be intentionally readable. Partial responses may redact the protected field correctly. Data-loader deduplication can make aliases cheaper than their count suggests.

## Deduction and controls

A foreign fixture stays inaccessible through root, nested and node routes; equivalent bounded operations have the documented accounted cost, and revoked subscription access follows the declared revalidation policy.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Execute one permitted query per test identity and capture actual resolver traces as positive harness controls.

2. Reach the same owned and foreign fixture through root, nested and global-node paths; change one principal or path at a time.

3. Compare two small aliases with two individual queries under a deliberately low lab cost limit; measure actual resolver and database work.

4. Open one synthetic subscription, revoke its access, and publish one fixture event after the documented invalidation interval.

5. Check one local and one foreign cursor plus a small multipart upload if supported; stop on the operation budget or unexpected worker growth.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

HTTP 200 can contain unauthorized partial data or legitimate field errors. Shared data-loader caches can cross identities even when resolver checks are correct. Request-depth alone misses broad expensive fields; circular fragment rejection should be checked before execution.

## Evidence and deliverable

Provide schema digest, operation names, resolver trace, principal/object matrix, returned fixture fields, cost estimate versus measured work and subscription timeline. Keep secrets out of variable captures.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record server, data-loader, transport and incremental-delivery versions. Batch support, multipart parsing, introspection settings and subscription protocols are configuration-dependent; do not assume all endpoints implement them.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Enforce authorization where objects are resolved, scope caches by tenant/principal, bound resolver cost and pagination, and revalidate subscription delivery. Make mutation idempotency explicit rather than relying on query validation.

Log operation hashes, resolver costs, denied object references and post-revocation delivery attempts. Validate detection using the two-alias fixture rather than an exhaustion workload.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A nested resolver returns tenant B's private fixture to A while the root route denies it: CONFIRMED; FAIL. |
| Benign refutation | Introspection is intentionally public and all private fixture fields remain redacted: REFUTED for the claimed authorization break; PASS for tested cells. |
| Insufficient evidence | A complexity scanner flags a query but no query or resolver trace was captured: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-graphql/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves resolver, Relay, batch and subscription mechanisms; removes blind schema harvesting, credential amplification and depth-bomb procedures.

