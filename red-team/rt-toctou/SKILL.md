---
name: rt-toctou
description: Test check/use identity and snapshot consistency with deterministic synthetic schedules across files, shared buffers and transactional services.
---

# Check/use consistency assessment

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Work on test-owned files, memory and service fixtures without privileges.
Use explicit synchronization hooks in fixtures instead of timing-amplification techniques.
Do not race privileged programs, mounts, procfs targets or live payment operations.

## Inputs and required invariant

Obtain the check site, use site, protected property and mutable object identity.
Record who may change each field and which lock, snapshot or transaction spans the interval.
For a file, distinguish path text, directory handle, open handle and inode identity.
For memory, distinguish pointer equality from allocation generation and field values.
For an API, distinguish authentication time from authorization policy at commit.
Define whether the contract requires current policy or permits a documented snapshot.
Do not label every stale read a security defect.

## Mechanisms

A TOCTOU defect requires a checked fact to become invalid before a dependent action.
A double-fetch uses mutable input twice while assuming the validated values stayed fixed.
A descriptor can pin file identity while contents or permissions remain mutable.
A lock helps only when all relevant mutators participate in the same exclusion rule.
An idempotency key prevents duplicates only if key, request identity and commit are bound.
A data-race-free transaction can still violate an application-level check/use invariant.

## Abduction and strongest benign explanation

Hypothesis: a path is validated as object A and later resolved again to object B.
Benign rival: the code opens once, validates the same handle and uses that handle.
Another rival: the policy intentionally authorizes a versioned snapshot.
Deduction: changing only the test path binding after check changes the used identity
in the faulty fixture, while the handle-bound control continues to use A.
Refute the path-reresolution claim if the used handle demonstrably remains A.

## Controlled filesystem experiment

1. Create a private test directory containing inert files A and B with distinct markers.
2. Define the fixture contract as reading only the identity accepted at check time.
3. Add a test-only barrier immediately after the check; record the checked identity.
4. Through the fixture's test controller, change the path binding from A to B.
5. Resume the fixture and record the identity actually opened and the returned marker.
6. Compare with a no-change schedule and a handle-bound repaired implementation.
7. Assert equality of checked and used identities; compare markers as corroboration.
8. Preserve event order and object metadata, then remove only test-owned state.

The barrier establishes possible ordering in the model, not frequency in production.
An instrumentation hook inserted in a real target must be disclosed as an accommodation.
Do not claim deployment reachability without tracing the actual mutation authority.

## Shared-buffer and service variants

For double-fetch, model a descriptor containing length and data in ordinary user memory.
Pause after validation, update the model field, then compare used versus validated length.
Use a local immutable copy as control; assert the same snapshot feeds validation and use.
Do not infer kernel behavior from a user-space model.
For quota checks, use two fixture transactions and a one-unit synthetic resource.
Record both reads, reservations, commits and final count under a defined schedule.
Compare with a serializable reservation or atomic conditional update.
For idempotency, reuse a test key with a different inert body and assert conflict.
Do not mistake two successful responses for two committed mutations.

## Reproducibility and tool limits

Save schedule, event sequence, fixture revision, filesystem and isolation settings.
Use explicit barriers and bounded waits; record deadlock or timeout separately.
TSan can expose unsynchronized memory access but cannot prove filesystem atomicity.
Tracing adds latency and may hide races; record whether the trigger depends on it.
Verify platform-specific handle and path-resolution semantics before choosing APIs.
A no-follow flag on the final component does not constrain every parent component.
A final-component symlink restriction alone is not a complete confinement proof.

## Detection and remediation

Log checked/used object IDs or policy versions with operation correlation IDs.
Detect reservation conflicts and body/key mismatches without logging sensitive contents.
Prefer validating an opened object and using that same handle within the required scope.
For mutable fields, validate a stable copy or hold the appropriate ownership/lock.
For business state, bind predicate and mutation in one atomic commit.
Replay the offending schedule and a permitted schedule after the repair.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: check records A, controlled rebinding yields B at use;
  unchanged and handle-bound controls yield A. CONFIRMED identity TOCTOU in the fixture.
- Benign refutation: renamed path still yields A through the validated open handle;
  the identity invariant holds. REFUTED path-substitution claim, control PASS.
- Insufficient evidence: intermittent failure lacks checked/used IDs and schedule;
  CANDIDATE with control WARN; no privilege-escalation conclusion.

## Output and provenance

Deliver an event table, identity invariant, minimal schedule, controls and remediation scope.
Source: `Skills/exploit-dev/offensive-toctou/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten from research data; race weaponization and platform claims are not adopted.
