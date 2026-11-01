---
name: rt-waf-bypass
description: "Measure WAF inspection coverage and parser consistency in an owned lab using inert policy markers and known rule decisions, without evasion recipes."
---

# WAF Enforcement Coverage Measurement

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Treat the upstream topic as control-effectiveness measurement. Do not rotate identities, solve challenges, hide automation, bypass origin controls or construct attack encodings.

Obtain an owner-controlled WAF configuration, exact rule version, enforcement mode and a small benign conformance corpus. Use a dedicated origin and lab-only rule matching a harmless marker.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace listener, routing, inspection body limit, content decoding, rule evaluation and origin handling. Record exclusions, skip rules, fail-open policy and protocol termination.

**Firstness:** Capture per-request rule matches, action, inspection completion and origin receipt. Compare with the explicit lab rule's expected allow/deny decision.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** The WAF does not inspect a supported request location or its normalized view differs from the application's view.

**Competing benign explanation:** A rule may intentionally run in log-only mode, an approved exclusion may apply, or the request may never reach the origin. A missing block alone does not show a bypass.

## Deduction and controls

A known harmless denied marker is blocked in each declared supported location while a marker-free control reaches the origin. A missed location must be demonstrated in both WAF and origin traces.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Install or select the owner-provided lab marker rule and record its intended coverage and enforcement mode.

2. Replay one marker-free request and one marker-bearing request through the same authorized route.

3. Move the same inert marker among declared supported body/header fields without obfuscation; inspect which locations the engine actually evaluates.

4. Use a tiny lab-configured inspection-size threshold to test at and just beyond the limit without large traffic; compare documented reject, truncate or skip behavior.

5. Compare supported protocol paths using identical semantics, then restore the lab rule configuration and retain the result matrix.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A WAF block can originate from rate limiting rather than the intended rule. Origin logs may be absent because of caching. Detection of an inert marker measures coverage, not exploit prevention against arbitrary payloads.

## Evidence and deliverable

Provide policy/rule digest, enforcement mode, request corpus hashes, per-location decisions, inspection completeness and correlated origin receipt. Report uncovered paths without supplying operational evasion strings.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record WAF engine, managed-rule revision, connector and protocol versions. Vendor product names and historical bypass claims do not establish behavior. Verify replay tools preserve the intended benign request structure.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Align supported parsers and normalization, explicitly reject unsupported or uninspected content and test exclusions. Keep application validation independent; do not represent a marker-rule pass as complete application security.

Alert on inspection skips, oversize truncation and unexpected origin receipt after a deny decision. Validate alerts with known marker cases and inspect false positives on the clean control.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A supported field reaches the origin with the lab deny marker while logs show that field was skipped contrary to policy: CONFIRMED for coverage failure; FAIL. |
| Benign refutation | The rule is intentionally log-only and records the marker exactly as configured: REFUTED for an enforcement malfunction; PASS for logging only. |
| Insufficient evidence | A scanner fingerprints a WAF and receives 200 without rule or origin evidence: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-waf-bypass/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Reframes evasion into measurable inspection coverage, mode and parser validation; removes residential proxy, CAPTCHA, fingerprint and origin-bypass guidance.

