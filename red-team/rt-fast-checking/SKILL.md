---
name: rt-fast-checking
description: Design a time-bounded security triage pass that prioritizes discriminating checks and records untested coverage instead of treating checklist completion as assurance.
---

# Bounded Security Triage

Read [METHODOLOGY.md](../METHODOLOGY.md) before allocating the test window.
Use this skill for initial prioritization under a real time/request budget.
Route substantive follow-up to the relevant domain skill rather than compressing its proof.

## Mechanisms and prerequisites

Rapid triage fails when it treats technology fingerprints as vulnerabilities or distributes
too few observations across many unrelated boundaries to refute any hypothesis.
Start with supplied routes, architecture, roles and representative legitimate transactions.
Identify concrete actors, data objects, privileged actions and available control fixtures.
Separate anonymous, authenticated, administrative and asynchronous processing contexts.
Define permitted traffic, state changes, concurrency and resource budgets before testing.

## Observation and baseline

Capture one successful legitimate request for each selected boundary and its expected effect.
Record version hints as hints until corroborated by supplied inventory or actual build evidence.
Map API documentation against observed routes; an undocumented route is an inventory lead.
Keep CDN/WAF, application and backend outcomes distinct using correlation IDs where available.
A login page returning 200, schema introspection or a missing header is not itself a bypass.

## Abduction and deduction

Hypothesis: a selected object-read route authorizes identity but omits tenant ownership.
Benign rival: the response is public data, a cached error page or an intentionally shared object.
Prediction: account A receives B's private fixture marker through that route, while a missing
object returns a distinct result and B's own authorized read proves fixture availability.
Do not substitute response-code equality for the marker and ownership oracle.

## Select a small discriminating portfolio

| Surface | Cheapest useful check | Essential control |
|---|---|---|
| Object access | Two owned accounts and two private marker objects | Owner success and absent object |
| Session lifecycle | Fixture session after logout or expiry | Fresh authorized session |
| Privileged field | Submit one forbidden fixture property | Allowed-property update and persisted state |
| Upload pipeline | Inert file through documented processing route | Valid file and rejected unsupported format |
| Streaming API | Fixture subscription under correct/wrong tenant | Authorized subscriber receives marker |
| Configuration | Compare actual effective policy to intended rule | Evidence that the assessed route uses it |

## Bounded laboratory procedure

1. Rank candidates by demonstrated exposure, consequence, uncertainty and cost to discriminate.
2. Reserve enough budget for a matched control and evidence capture for each selected test.
3. Use an owned staging/lab fixture with synthetic accounts, objects and reversible state.
4. Run the legitimate baseline first; if it fails, resolve the harness before security inference.
5. Change one actor, object or policy factor, inspect the effect, then run the control.
6. Retain the minimum confirming or refuting evidence and move to the next ranked question.
7. Stop on the declared budget, unexpected service degradation or unowned data exposure.
8. Hand off unresolved mechanisms with exact next experiment and missing preconditions.
9. Restore fixture objects and sessions; preserve the evidence ledger and coverage gaps.

## Domain failure modes

Rate limits and gateway challenges can mask backend behavior; do not evade them to meet a quota.
Scanner defaults may crawl out of scope, mutate state or run expensive vulnerability modules.
Wordlists, malformed-request campaigns and concurrency tests require a separate bounded design.
An upstream cache can return another fixture's response without proving an authorization bug;
vary cache state separately and report the mechanism supported by correlation evidence.
Modern authentication fallbacks and API transports deserve separate cases, not blanket claims.
An omitted check means NOT TESTED, never PASS or "no vulnerabilities found."

## Evidence, detection and remediation

Deliver a coverage ledger: boundary, candidate, baseline, discriminator, result, cost and next step.
Count confirmed, refuted and untested cases separately; retain the smallest replay description.
For confirmed defects, name the enforcing layer and class-level remediation owner.
Record whether a correlated application/security event observed the fixture test.
Detect unexpected cross-tenant reads, denied privilege changes and stale-session acceptance
with identity-aware telemetry; a list of scanner requests is not detection coverage.

## Versions and limits

Record proxy/scanner versions, enabled modules, request caps and application revision.
Inspect installed help and exact module behavior before any automated traffic.
This skill chooses experiments; it does not replace specialist cryptographic or parser review.
No probes or scanner runs were executed during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| A reads private B marker; ownership and missing-object controls discriminate | CONFIRMED for that route; FAIL |
| 200 response is a login page and no private marker or state effect appears | REFUTED bypass claim; PASS for tested access check |
| Time expires after fingerprinting with no baseline/control pair | NOT TESTED security boundary; WARN |

## Provenance

Rewritten from `Skills/utility/offensive-fast-checking/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain high-value surface selection; replace exhaustive payload lists and WAF
evasion shortcuts with budgeted experiments and explicit coverage accounting.
