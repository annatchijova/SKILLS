---
name: rt-ssti
description: "Validate whether user-controlled content becomes template source using constant-only lab fixtures and real rendering traces."
---

# Template Data and Source Separation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess template evaluation and trust boundaries. Constant evaluation is evidence of template interpretation, not proof of operating-system execution or sandbox escape.

Use the real renderer in a disposable environment with synthetic context, no secrets and denied network/process capabilities. Obtain the expected user content contract and engine configuration.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace template selection, string construction, compilation, rendering, escaping and any second render pass. Record which extensions, helpers and context objects are exposed.

**Firstness:** Capture the selected template, compilation inputs and raw rendered result before browser interpretation. Compare with the requirement that submitted text remain data.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A field intended as text is concatenated into template source or rendered a second time.

**Competing benign explanation:** The field may intentionally be an approved template editor, or the apparent evaluated output may come from client-side rendering or a hard-coded demonstration.

## Deduction and controls

An engine-appropriate constant-only fixture evaluates only on the suspected source path; the identical text passed as an ordinary context variable stays literal. A changed constant changes the output predictably.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Render ordinary marked text and establish the expected server response and browser-independent output.

2. Use an owner-approved constant arithmetic or literal-composition fixture for the installed engine; exclude attribute traversal, imports and file/process helpers.

3. Compare the same text through source construction and data binding, then repeat with a different constant to reject cached output.

4. Inspect whether a second render pass transforms previously escaped text; capture both render stages separately.

5. For an intentional template editor, inspect allowed capabilities and use inert registered helper probes only; stop before testing escape chains.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

Autoescaping protects output syntax but does not necessarily prevent source evaluation. A renderer error can fingerprint a parser without proving controllable evaluation. Engine identification by one arithmetic result is unreliable.

## Evidence and deliverable

Provide source/data flow, engine settings, paired raw outputs, compilation trace and the exact safe fixture class. Separate unintended evaluation from capability exposure and untested execution impact.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin engine and wrapper versions, sandbox settings and helper registrations. Historical object traversal chains are neither portable nor needed. Automatic template scanners may invoke unsafe probes; use only verified inert modes.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Use fixed templates with explicit data binding, remove second-pass rendering and restrict template selection. For intentionally programmable templates, minimize capabilities and isolate execution with documented resource limits.

Log unexpected compilation from user-originated fields and rejected helper access without recording private template context. Validate alerts using the constant-only fixture.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Text intended as literal content is compiled and evaluates two different constant fixtures while data binding preserves them: CONFIRMED for source/data boundary failure; FAIL. |
| Benign refutation | The documented template editor evaluates constants within its allowed capabilities: REFUTED for unintended evaluation; no sandbox conclusion. |
| Insufficient evidence | An error mentions a template engine but no controlled evaluation or compilation trace exists: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-ssti/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves engine, context, second-pass and sandbox analysis without traversal payloads, file reads or template-to-shell chains.

