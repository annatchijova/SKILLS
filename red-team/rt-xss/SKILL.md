---
name: rt-xss
description: "Validate untrusted content rendering, sanitizer transitions and browser execution policy with inert markers and isolated browser fixtures."
---

# Browser Rendering Trust Boundaries

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess whether untrusted data enters executable browser context. Reflected text or raw HTML alone does not prove script execution, and no session theft or external callbacks are part of this workflow.

Use an isolated browser profile, a local test origin, synthetic content and no real cookies. Obtain rendering code, sanitizer configuration and the expected allowed markup policy.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace URL, stored and message inputs through decoding, sanitizer, template binding, DOM insertion and subsequent mutation. Include markdown or generated content only when it reaches a real rendering sink.

**Firstness:** Record raw response, parsed DOM and relevant sink calls. Compare with the content contract: literal text, permitted markup or explicitly trusted component.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A source reaches an executable DOM context without appropriate encoding, or post-sanitization mutation creates a prohibited node or attribute.

**Competing benign explanation:** The marker may be text-escaped, placed in an inert document, blocked by the enforced execution policy, or sanitized again before active insertion. A scanner can mistake reflection for execution.

## Deduction and controls

An owner-provided inert rendering fixture is preserved as text or permitted markup; the unsafe path creates a prohibited active context while the safe binding control does not.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Render a plain marker and establish its source-to-sink path using browser instrumentation.

2. Replay an approved inert sanitizer conformance fixture in the isolated page; inspect the live DOM after all framework mutations.

3. Compare the same content through a text-only binding and the suspected insertion path.

4. If execution confirmation is needed, use an existing local test fixture that only toggles an in-memory boolean; it must read no cookies, issue no requests and alter no persistent state.

5. For stored content, render through two synthetic roles and the actual preview/final views; remove only the fixture content and reset the profile.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A blocked execution attempt can still establish unsafe markup handling but not active execution under that policy. Browser extensions and devtools actions can contaminate evidence. Sanitization before later string concatenation may lose its guarantee.

## Evidence and deliverable

Provide source/sink locations, raw and post-mutation DOM snapshots, browser build, sanitizer settings, CSP/Trusted Types enforcement mode and the local execution oracle if used.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Verify browser support and enforcement rather than assuming CSP, native Sanitizer API or Trusted Types availability. Report-only policy does not block. Framework escaping guarantees apply only to supported binding paths.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Use context-appropriate binding, maintained sanitizers for intentionally allowed markup and avoid mutation after sanitization. Restrict dangerous DOM sinks; deploy execution policies as defense in depth with regression fixtures.

Correlate sanitizer rejection and browser policy reports with fixture IDs. A missing CSP report is not evidence of safety; verify report delivery with a known local control.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A supplied local fixture toggles only its in-memory oracle through the untrusted sink, while text binding stays inert: CONFIRMED for browser execution in tested context; FAIL. |
| Benign refutation | The reflected marker remains text and the suspect path never creates an active context: REFUTED for that execution claim; PASS. |
| Insufficient evidence | A scanner reports reflection without a DOM trace or execution observation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-xss/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains reflected/stored/DOM, mutation and browser-policy mechanisms without payload catalogs, CSP evasion or session extraction.

