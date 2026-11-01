---
name: rt-open-redirect
description: "Measure redirect destination policy and parser agreement in browser, server and authentication flows using two owned origins."
---

# Redirect Destination Validation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Determine where navigation actually ends and whether it violates a destination contract. Keep phishing, token collection and unrelated internal service probing outside the experiment.

Prepare two owned origins with empty landing pages, a test browser and a documented redirect policy. Disable real authentication artifacts; use opaque synthetic markers.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace destination input through decoding, URL resolution, policy comparison, response construction and browser navigation. Distinguish server Location headers, client-side navigation and server-side HTTP fetching.

**Firstness:** Record the raw supplied destination, normalized comparison value, emitted destination and final browser origin. A reflected URL is not automatically a redirect.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** Validation and navigation parse the same destination differently, permitting an origin outside the intended allowlist.

**Competing benign explanation:** The feature may intentionally be an unrestricted URL shortener, or an interstitial may require explicit user confirmation under the product contract. A relative redirect may remain within the approved origin.

## Deduction and controls

A fixture outside the declared allowlist is rejected or stops at the promised interstitial, while an approved destination completes navigation. Compare actual final origins, not string prefixes.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Establish one allowed navigation and one plainly disallowed owned-origin destination using the real browser and server path.

2. Replay an owner-approved parser conformance corpus offline against both validation and navigation parsers; retain differing normalized origins.

3. Exercise only the minimal differing inert case in the isolated application, with no codes, cookies or sensitive query values.

4. Follow the bounded redirect chain and record each hop; compare a direct approved destination with a chain that changes to the second owned origin.

5. For an authentication callback, check registration enforcement separately and hand transaction-binding questions to the OAuth skill.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

HTTP clients can normalize inputs differently from browsers. A server fetch is an SSRF boundary rather than navigation. A chain can change policy at a later hop; a final external page alone does not prove secret leakage.

## Evidence and deliverable

Provide raw and normalized destination representations, parser/library versions, hop sequence, browser trace and destination policy. Record whether navigation was automatic or user-confirmed.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin browser and URL parser versions; do not rely on historical backslash, userinfo or encoding behavior. Scanner labels based solely on Location strings require browser confirmation.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Prefer server-side destination identifiers or same-origin relative routes. Use a consistent parser and compare normalized scheme, host and port; document allowed external redirects and interstitial semantics.

Log rejected normalized destination origins and unexpected redirect chains without full sensitive query strings. Verify the same test navigation produces the expected audit event.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An automatic navigation reaches the second owned origin despite a documented same-origin-only rule: CONFIRMED; FAIL. |
| Benign refutation | An intentionally external URL shortener follows its published policy and transfers no protected artifact: REFUTED for the claimed policy bypass. |
| Insufficient evidence | Only a reflected destination string appears in HTML, with no navigation evidence: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-open-redirect/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains parser and authentication redirect analysis without domain spoofing catalogs, phishing construction or token interception chains.

