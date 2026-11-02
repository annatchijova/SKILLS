---
name: rt-parameter-pollution
description: "Red-team assessment of HTTP parameter-pollution boundaries: duplicate parameters across URL/form/JSON/GraphQL/WebSocket, array-notation confusion (PHP/Express-qs/Rails), and parameter cloaking. A precedence-differential problem (gateway vs backend, validator vs processor) reaching auth bypass, WAF bypass, access-control bypass and IDOR, re-expressed as owned-fixture experiments observing which tier honors which value with negative controls."
---

# HTTP Parameter Pollution Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's HPP craft as scoped experiments: it names the pollution forms and the precedence differentials to test, confirming which component honors which duplicate value against owned fixtures.

## Scope and prerequisites

HPP is a precedence differential (compose with `parser-differential-hunting`): two components disagree on which occurrence of a repeated parameter wins. Identify where a value passes through more than one parser/tier (gateway→backend, WAF→app, framework array parsing). Use owned accounts and fixtures.

Declare target stack, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Duplicate parameters** — `?id=1&id=2` across URL, form body, JSON, GraphQL variables/aliases, WebSocket messages.
- **Array-notation confusion** — PHP brackets, Express/`qs` bracket-optional, Rails numeric indices, mixed notation.
- **Parameter cloaking** — encoding variants, double/triple encoding, Unicode normalization, legacy null-byte.

## Mechanism and observation

Trace a repeated/ambiguous parameter through each tier to see which value each one reads.

**Firstness:** Record which value each observable component acted on (the response, the authorization decision, the logged value). **Secondness:** State the intended single interpretation and the deviation between tiers. **Thirdness:** Infer the defect class only after a controlled pollution makes two tiers act on different values.

## Abduction and refutation

**Mechanism hypothesis:** One tier authenticates/authorizes/validates using the first occurrence while another processes the last (or vice versa, or an array-notation difference), so a security decision and the effect use different values.

**Competing benign explanation:** Both tiers pick the same occurrence (no differential); the framework rejects duplicates; the second value is ignored entirely; the observed difference is unrelated to the duplicate.

## Deduction and controls

A single, unambiguous parameter behaves consistently (positive control). A confirmed HPP shows the authorization/validation tier reading one value while the effecting tier reads another, against owned fixtures. Predeclare which value each tier should read. Consistent interpretation across tiers is a PASS control.

## Induction: bounded laboratory procedure

Owned accounts/fixtures.

1. **Baseline.** Send the single-parameter request; capture which value the app uses and logs.
2. **Duplicate.** Send two occurrences with distinct owned values; observe which the response/authorization reflects.
3. **Cross-tier.** If a gateway/WAF precedes the app, craft the duplicate so the front tier plausibly reads one value and the backend the other; confirm with owned IDs (e.g. front authorizes `id=own`, backend serves `id=own2`).
4. **Array notation.** Test bracket/index notations the framework parses differently.
5. **Cloaking.** Test encoding/Unicode variants that one parser decodes and another does not.
6. **Control.** Confirm the single-parameter request is consistent.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Occurrence precedence differs by stack: typically PHP/`$_GET` last, ASP first, Node/Express array, JSP first, Rails last — verify, do not assume. GraphQL alias/variable pollution can bypass per-operation rate limits. API-gateway-vs-backend precedence is the high-value variant (gateway picks first `id`, backend picks last → IDOR/access-control bypass). HPP can also smuggle XML/filter-evading content past a WAF checking a different occurrence.

## Domain-specific failure modes

If both tiers agree, there is no finding. A reflected second value is not an effect unless a security decision diverges from it. Framework rejection of duplicates is a refutation. The impact is entirely about the differential: name the two tiers and the two values.

## Evidence and deliverable

Provide the parameter, the two values, which tier honored which, the resulting security effect (auth/AC/WAF bypass, IDOR), and the single-parameter control. Use owned IDs only. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered parameters.

## Versions and tool limitations

Pin each tier's server/framework and version — precedence is implementation-specific. No parsing behavior was verified by this content; confirm each tier's live behavior first.

## Remediation and detection

Reject duplicate parameters (or canonicalize to one occurrence) consistently across all tiers, enforce a single array notation, and make the authorization tier and the effecting tier read the same canonical value. Add a regression asserting duplicates are handled identically end-to-end. Detect repeated parameters diverging between gateway and backend logs.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The authorization tier reads one value while the effecting tier reads another (owned IDs), producing a bypass/IDOR: CONFIRMED; FAIL. |
| Benign refutation | Both tiers read the same occurrence / duplicates rejected: REFUTED; PASS for the control. |
| Insufficient evidence | A second value is reflected but no cross-tier divergence is shown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-parameter-pollution/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's pollution forms, framework precedence knowledge and gateway-vs-backend high-impact variant, re-expressed as owned-fixture cross-tier experiments with consistency controls, replacing speculative impact with a demonstrated precedence differential.
