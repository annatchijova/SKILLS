---
name: rt-file-upload
description: "Validate upload admission, asynchronous processing, storage isolation and download authorization with inert files and bounded archive fixtures."
---

# Upload Processing and Publication Boundaries

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess the full upload lifecycle, including presigned storage operations, chunk assembly, conversion and retrieval. A successful upload is not proof of executable content.

Prepare tiny inert files with known digests, a bounded archive fixture and two test tenants. Use a storage namespace isolated from application code and suppress external notifications.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace upload capability issuance, key selection, content validation, quarantine, processing, scanner result, publication and download authorization. Capture whether validation applies to original bytes, transformed bytes or both.

**Firstness:** Record stored object key/version, detected media type, processing state and retrieval headers. Compare them with the promised quarantine and tenant ownership policy.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** Publication happens before validation completes, or a storage capability permits replacing another tenant's object or trusted application content.

**Competing benign explanation:** An accepted upload may remain inaccessible in quarantine; a client-provided media type may be ignored by a safe decoder. A signed download URL may intentionally delegate time-limited access.

## Deduction and controls

A pending or rejected fixture must remain inaccessible on every publication path; a capability scoped to one fixture must not write a second tenant's fixture key.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Upload a normal small file and verify its final digest, tenant ownership and successful intended retrieval.

2. Pause the lab scanner or conversion worker at its documented test hook; request the pending object through both application and storage publication paths.

3. Use a harmless media-type mismatch fixture and inspect decoder output and publication decision without introducing executable content.

4. Check capability expiry and key binding using two owned objects; test incomplete multipart assembly and failed conversion recovery separately.

5. Use only an owner-supplied tiny archive containment fixture; assert extraction stays within the scratch root and stop on any out-of-root attempt.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

CDN caches can serve an earlier clean version while a new version is quarantined. Filename sanitization does not establish extraction containment. Presigned URLs may bind a key but not a digest; record what the application actually promises.

## Evidence and deliverable

Deliver object/version IDs, fixture hashes, admission and scan decisions, worker timeline, storage policy and retrieval headers. Record archive entry limits and processor CPU/memory/time budgets.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin storage SDK, decoder, image/PDF converter and scanner versions. Historical extension tricks and old null-byte behavior are not current findings. Browser rendering behavior depends on content type, disposition and origin.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Use immutable tenant-scoped keys, isolated quarantine, atomic publication after successful processing and separate untrusted download origins. Bound expanded size and processing time, and deny writes to executable/configuration locations.

Correlate upload IDs across scan failures, conversion errors and publication events; alert when publication precedes approval or a capability targets a mismatched namespace.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A rejected fixture is retrievable from the public object endpoint despite a quarantine guarantee: CONFIRMED; FAIL. |
| Benign refutation | A mismatched extension is accepted into quarantine, decoded safely and served only as an attachment after approval: REFUTED for the alleged executable upload; PASS for tested controls. |
| Insufficient evidence | Only the upload response is visible and storage/publication state is unknown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-file-upload/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains upload, object-storage, archive and converter boundaries while replacing web shells, polyglots and processing exploits with inert lifecycle tests.

