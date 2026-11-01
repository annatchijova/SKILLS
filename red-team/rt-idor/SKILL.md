---
name: rt-idor
description: "Validate object and relationship ownership across direct, nested, export and capability-based access using two synthetic principals."
---

# Object Reference Authorization

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess authorization of referenced objects and relationships. API boundary assessment covers transport-wide policy; this skill concentrates on the same object reached through multiple routes.

Provision two principals with private fixtures and a documented sharing rule. Record tenant membership, role, resource ownership and any delegated capability before testing.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace identifier parsing to repository predicates, policy-engine inputs, object relation lookup and response projection. Include background exports and signed URLs only if the application supplies those paths.

**Firstness:** Record actual fields returned and durable changes to the foreign fixture. Contrast with the policy matrix; guessable or sequential identifiers alone do not violate ownership.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A child object is authorized using its parent path without verifying the child's actual parent, or a secondary route omits the ownership predicate.

**Competing benign explanation:** The object may be public, shared intentionally or accessed via a valid bearer capability. Row-level database policy may enforce ownership even when a handler lacks a check.

## Deduction and controls

Changing only the referenced fixture or principal must preserve denial of private foreign data and effects. A legitimate share should succeed and a revoked share should fail after the documented cache interval.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Record successful owner access for each synthetic object and a denied unrelated principal as harness controls.

2. Replay one direct reference under the other identity, then one nested reference where parent and child belong to different test owners.

3. Compare read, edit and link operations independently; inspect persisted state even after a denied response.

4. Exercise one export job or attachment path and inspect both job authorization and result retrieval.

5. Test a synthetic capability before and after expiry or revocation where promised; remove only test shares and verify restoration.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A 200 with an empty or caller-owned projection is not disclosure. A 403 can still include private fields or occur after mutation. Cached authorization, policy-engine default permit, missing tenant context and relationship writes need separate evidence.

## Evidence and deliverable

Deliver actor/resource/action/relationship matrix, exact fixture IDs, policy source, paired sanitized requests and before/after state. Include the repository or policy-engine predicate and any cache delay.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record policy-engine and framework versions, storage signing semantics and test-client cookie behavior. UUID decoding or ID encoding tools cannot establish permissions. Automated ID sweeps are unnecessary for two-fixture proof.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Scope repository lookups and relation writes to authorized context; validate actual parent-child relationships. Apply the same decision to asynchronous jobs and downloads and invalidate policy caches under an explicit contract.

Log actor, tenant, resource class and denial reason using safe identifiers; correlate failed parent-child bindings and unusual export ownership. Validate that successful unauthorized access would also be visible.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A private child of B is returned to A through A's unrelated parent path: CONFIRMED; FAIL. |
| Benign refutation | The disputed object is intentionally shared and revocation blocks it as documented: REFUTED for unauthorized access; PASS. |
| Insufficient evidence | The identifier is predictable but no foreign-object response or effect was observed: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-idor/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Keeps object, relationship, export and policy-engine depth distinct from broad API coverage without enumeration or mass extraction.

