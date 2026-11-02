---
name: rt-waf-bypass
description: "Red-team measurement of WAF/filter control effectiveness: does the WAF actually stop a given injection class, or can a semantically-equivalent payload transformation reach the application? Covers encoding, case/comment, protocol-level (HTTP/2, HTTP/3, chunked), SNI/domain-fronting, GraphQL and ML-WAF differential families as a filter-vs-application parser differential, re-expressed as owned-stack experiments that score the control PASS/WARN/FAIL with the defender in the loop."
---

# WAF / Filter Control-Effectiveness Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision reframes the upstream's bypass catalog as control-effectiveness measurement (the purple-team posture): the question is whether the WAF stops a class, measured against an owned stack with the defender informed, not how to evade detection to harm a third party. Compose with `purple-team-exercise` and `parser-differential-hunting`.

## Scope and prerequisites

A WAF bypass is a parser differential: the WAF classifies the request as benign while the application parses it as the attack. Test against an owned application behind the owned WAF, with the WAF team aware, measuring whether a known-malicious class is blocked or reaches the app. Do not use this to evade a third party's controls.

Declare the WAF product/mode and the backend, the injection class under test, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Mechanism and observation

Send a payload that is unambiguously the attack class to the application, with and without transformation, and observe whether the WAF blocks it and whether the app executes it.

**Firstness:** Record the WAF verdict (block/allow) and the app's behavior (inert/executed) for each payload variant. **Secondness:** State what the WAF is expected to stop and the deviation. **Thirdness:** Infer a control gap only after a transformed payload is both allowed by the WAF and acted on by the app.

## Abduction and refutation

**Mechanism hypothesis:** The WAF normalizes/parses the request differently from the application, so a semantically-equivalent transformation of a blocked payload slips past while remaining effective at the app.

**Competing benign explanation:** The WAF blocks the transformed variant too; the "bypass" payload is also inert at the app (transformation broke it); the app's own validation stops it regardless of the WAF; the test hit a different rule/path.

## Deduction and controls

The raw attack payload is blocked (positive control = WAF working). A confirmed gap has a transformed payload allowed by the WAF and executed by the app, where the raw payload was blocked and a benign control is allowed. Predeclare both the app effect and the WAF verdict. The WAF blocking all effective variants is a PASS control.

## Induction: bounded laboratory procedure

Owned stack; defender informed.

1. **Baseline.** Confirm the WAF blocks the raw attack payload (control that the rule exists) and allows a benign request.
2. **Transformation families (differential probes).** Apply equivalence-preserving transforms and re-test both WAF verdict and app effect:
   - Encoding: URL/double-URL, hex, HTML-entity, Unicode normalization/overlong.
   - Lexical: case variation, inline comments, whitespace substitution, string concatenation/dialect tricks.
   - Protocol: chunked transfer, HTTP/2 and HTTP/3 framing, header/param placement (payload in a low-weight field).
   - Content-type/parser confusion, JSON wrappers, GraphQL-specific shapes.
3. **Confirm both ends.** A gap requires WAF=allow AND app=executed. If the app is inert, the transform broke the payload (not a bypass).
4. **ML-WAF note.** For ML/scoring WAFs, measure robustness to paraphrase/synonym/noise-token variants as a model-evaluation question, not a guaranteed evasion.
5. **Control.** Re-confirm the raw payload is still blocked.

Record results including refutations. Keep finding status (control gap) separate from the control score (PASS/WARN/FAIL).

## Craft notes (leads)

Fingerprint the WAF first (response signatures, headers). The high-value differentials are protocol-level (the WAF and origin disagree on request structure) and encoding/normalization (the WAF decodes once, the app twice). Payload-in-low-weight-field and content-type confusion exploit incomplete inspection. SNI manipulation and domain fronting are routing/perimeter concerns — note them, but the application-layer differential is the measurable control question here. Origin-direct access (reaching the backend IP, bypassing the WAF entirely) is an architecture finding, not a payload bypass.

## Domain-specific failure modes

A transform that the app does not execute is not a bypass — confirm the app end. Blocking the raw payload proves the rule exists, not that the control is complete. ML-WAF evasion is probabilistic; one evading sample is WARN on robustness, not a guaranteed bypass. Testing a third party's WAF to attack it is out of scope for this skill.

## Evidence and deliverable

Provide the class under test, the raw-blocked baseline, the transformed payload with WAF verdict and app effect, and the benign control. Report the control as PASS/WARN/FAIL. Attach minimal replay, expected/observed, rival explanation, falsifier, untested families. Share with the defender.

## Versions and tool limitations

Pin the WAF product, ruleset version and mode, and the backend — differentials are version-specific. WAF-testing tools exist; keep testing on the owned stack. No WAF behavior was verified by this content; confirm the live product and rules first.

## Remediation and detection

Normalize identically to the backend (decode fully, canonicalize) before inspection, prefer positive-security/allowlist models, block origin-direct access, cap and normalize protocol variants, and defend the app independently of the WAF (defense in depth). Add a regression asserting each known transform of the class is blocked. Detect transformed-payload patterns reaching the app.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A transformed payload is allowed by the WAF and executed by the app where the raw payload was blocked: CONFIRMED control gap; control FAIL. |
| Benign refutation | The WAF blocks all effective variants, or the transform leaves the payload inert at the app: REFUTED; control PASS. |
| Insufficient evidence | A variant passes the WAF but the app effect is unconfirmed: CANDIDATE; control WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-waf-bypass/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's evasion catalog as owned-stack control-effectiveness measurement scored PASS/WARN/FAIL with the defender in the loop, retaining the encoding/protocol/parser-differential craft while dropping third-party anti-bot/CAPTCHA/residential-IP evasion as outside the authorized-testing posture.
