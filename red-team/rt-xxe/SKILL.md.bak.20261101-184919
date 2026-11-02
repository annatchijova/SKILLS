---
name: rt-xxe
description: "Assess XML external resolution, parser configuration and bounded expansion behavior using synthetic resolver fixtures in isolated document pipelines."
---

# XML Resolver and Expansion Controls

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Validate XML parser and resolver behavior, including XML embedded in document formats. Do not read real local files, access cloud metadata or generate expansion bombs.

Use the deployed parser in a disposable environment with an owned resolver serving a tiny marker document. Deny external egress and provide only synthetic filesystem fixtures if local resolution is explicitly in scope.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace format admission, decompression, XML parsing, DTD handling, entity resolution, XInclude, schema validation and transformations. Each processor can have independent resolver settings.

**Firstness:** Record resolver invocations and whether a marker is incorporated into the parsed result. Compare with the application's no-external-resolution policy and expansion limits.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A later validator or transformer enables external resolution despite the initial parser being restricted.

**Competing benign explanation:** A parser may recognize a declaration but reject resolution; a network observation may be schema retrieval explicitly allowed by contract rather than entity expansion.

## Deduction and controls

The ordinary XML control parses successfully. The owner-provided external-reference fixture either fails before resolution or reaches only approved synthetic resources, with no unexpected marker incorporation.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Parse a tiny normal fixture through the complete pipeline and capture each processor's configuration.

2. Replay an owner-provided harmless external-reference conformance fixture against the isolated resolver; log both attempted and completed resolutions.

3. Compare with external resolution disabled at the actual processor, keeping the input and pipeline otherwise identical.

4. Exercise DTD, XInclude and schema-location handling separately where supported; use small non-recursive fixtures.

5. Set a deliberately low lab node/size limit and verify bounded rejection without a resource-exhaustion document; restore configuration and preserve logs.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

No outbound callback may mean network denial rather than parser rejection. A gateway validating XML shape does not establish downstream resolver safety. SAML signatures and XML parsing order require separate analysis and cannot be inferred from one resolver test.

## Evidence and deliverable

Provide parser/validator/transformer versions and flags, fixture digests, resolver event order, parsed marker result, configured size limits and network control status.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Defaults vary across parser versions, wrappers and entrypoints; verify the actual factory settings. Do not generalize behavior from one XML library to an office renderer, SVG processor or SOAP stack.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Disable unneeded DTD/entity processing, restrict resolvers and schema sources, and independently constrain each transformation stage. Bound decompressed size and node expansion before expensive downstream work.

Log rejected external resolution and size-limit events with document IDs, avoiding document contents. Correlate resolver attempts with egress denials so parser failure is not confused with network containment.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A supposedly restricted transform resolves the synthetic external marker and incorporates it into output: CONFIRMED for resolution-policy failure; FAIL. |
| Benign refutation | The pipeline rejects resolution before contacting the collector while normal XML still parses: REFUTED; PASS. |
| Insufficient evidence | No callback is observed but an egress firewall may have blocked it and parser logs are missing: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-xxe/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves multi-parser, entity, include and schema resolution analysis without local-file extraction, metadata pivots or exponential-expansion recipes.

