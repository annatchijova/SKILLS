---
name: rt-deserialization
description: "Review and safely instrument object reconstruction boundaries in serialized inputs, queues and caches without constructing gadget chains."
---

# Deserialization Boundary Validation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Determine whether untrusted input can choose executable reconstruction behavior. Format recognition alone is inventory; it does not establish code execution.

Use a disposable runtime with synthetic data, denied outbound network and no production secrets. Obtain the actual serializer settings, dependency graph, class allowlist and input provenance.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace decoding and decompression, signature verification, type resolution, object construction and post-load validation. Include queue consumers, uploaded archives and cache values only when an actual call path reaches a serializer.

**Firstness:** Record the exact loader and resolved type, plus whether integrity validation preceded object reconstruction. Compare with the intended data-only schema.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** An untrusted type discriminator selects a reconstruction hook before the trust or type check.

**Competing benign explanation:** A format signature may belong to an opaque signed blob rejected before loading, or a serializer may use only explicit data-transfer types. A listed dependency need not be reachable from the entrypoint.

## Deduction and controls

An approved inert sentinel type with only an in-memory event recorder is instantiated through the real loader only when the type boundary is permissive; the same input must be rejected by the restricted configuration.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Load a normal data-only fixture through the deployed loader configuration and capture type resolution events.

2. Use an owner-provided inert type-selection fixture that records construction without file, network or process effects; do not generate gadgets.

3. Compare allowed and disallowed type identifiers with the same serializer, verifying whether rejection happens before any hook.

4. Corrupt a synthetic integrity tag and confirm that the loader is not invoked; restore a valid tag as the harness control.

5. Repeat the minimal case at the actual queue or cache adapter when in scope, then discard the disposable runtime while retaining logs.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

Instrumenting a synthetic type can establish loader ordering but cannot establish availability of a dangerous production gadget. Autoloaders, finalizers and nested objects may resolve after the top-level type check. Do not use DNS callbacks as a synonym for safe deserialization.

## Evidence and deliverable

Provide loader/configuration locations, dependency versions, provenance of bytes, ordered integrity/type/hook events and the inert fixture definition. Label instrumentation-only results and untested production reachability explicitly.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

PHP archive metadata behavior, YAML loader defaults, Java object filters and .NET serializer availability vary by version. Check installed APIs and runtime behavior instead of inheriting upstream historical claims.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Replace executable object formats at trust boundaries with schema-validated data; validate integrity before reconstruction where appropriate. Use explicit type admission and bounded graph depth as defense in depth, not a promise that untrusted native serialization is safe.

Monitor unexpected type-resolution attempts and integrity failures before load. Validate telemetry with inert rejected fixtures; preserve dependency and consumer identity in the event.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The actual input path instantiates a disallowed inert type before validation: CONFIRMED for type-boundary failure; FAIL; arbitrary code execution remains unproven. |
| Benign refutation | A tampered opaque blob is rejected before the loader and a valid fixture still loads: REFUTED for that untrusted reconstruction path; PASS. |
| Insufficient evidence | Only serialization magic bytes and an old CVE match are available: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-deserialization/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves cross-runtime reconstruction and producer/consumer trust analysis while removing gadget generators, shell chains and version-independent PHAR assertions.

