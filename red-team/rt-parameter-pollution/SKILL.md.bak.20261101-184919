---
name: rt-parameter-pollution
description: "Compare duplicate-key and parameter precedence semantics across gateways, validators and application parsers using inert fixture values."
---

# Parameter Interpretation Consistency

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess semantic disagreement about one logical field. Duplicate parameters are not inherently a vulnerability when every layer applies a consistent documented policy.

Use a lab gateway and real application parser with two synthetic resources and trace access to parsed values. Select a field whose authorization or business meaning is documented.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace query, form, JSON or multipart bytes through gateway normalization, validation, binding and repository use. Record whether each stage sees a scalar, list or rejected value.

**Firstness:** Capture the actual ordered input pairs and the value each layer uses. Compare them with the endpoint's single-value or multi-value schema.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** The authorization layer checks one fixture identifier while the consumer uses a different occurrence or source.

**Competing benign explanation:** The parser may reject duplicates before business logic, or all layers may use the same first/last/list rule. A multi-select field may legitimately accept repeated values.

## Deduction and controls

Conflicting benign fixture values must either be rejected or resolve identically at validation and consumption. Reversing order should reveal a deterministic policy, not a security decision on a different value.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Send each fixture value individually and establish the expected permitted and denied decisions.

2. Use one duplicate-key test fixture containing the two inert identifiers; record raw bytes because client dictionaries can erase duplicates.

3. Reverse their order while preserving transport and identity; compare gateway, validator and consumer traces.

4. Repeat only supported query/body or scalar/list combinations under the same endpoint contract; do not build encoding bypass chains.

5. Inspect durable effects and replay the canonical single-value control after each case; stop when the first mismatched decision is isolated.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

JSON parsers can discard evidence of duplicates before application logging. A proxy can reorder fields. Framework defaults are not universal, and array syntax may select a different endpoint schema rather than expose a mismatch.

## Evidence and deliverable

Retain a byte-level fixture digest, content type, ordered field sequence, per-layer parsed values, authorized identifier and consumed identifier. Record the status and actual object effect.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin gateway, framework, JSON library and binding options. Normalizing replay tools can invalidate the experiment; verify the transmitted capture rather than the request editor.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Define one canonical parameter source and duplicate policy at ingress; reject ambiguous single-value fields. Pass the validated typed object to the consumer instead of reparsing raw input.

Monitor duplicate single-value fields and disagreements between normalized request IDs and consumed resource IDs. Validate logs without storing private values.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Authorization checks allowed fixture A while the repository mutates forbidden fixture B from the same request: CONFIRMED; FAIL. |
| Benign refutation | All layers reject ambiguous duplicates and valid single-value requests still work: REFUTED; PASS. |
| Insufficient evidence | The replay client collapsed duplicates before transmission, so parser disagreement was never exercised: NOT TESTED; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-parameter-pollution/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains parameter precedence and type-coercion mechanisms while replacing bypass payload catalogs with observable parser contracts.

