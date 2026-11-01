---
name: rt-oauth
description: "Validate OAuth and OIDC authorization transaction binding, callback handling, refresh rotation and account linking using synthetic clients and identities."
---

# OAuth Transaction Binding

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Assess the authorization flow and identity binding. Token signature and key-selection mechanics belong to token-trust-assessment. Do not treat OAuth authorization alone as a user authentication assertion.

Provision an isolated authorization server or owned test tenant, two clients, two browser sessions and two synthetic identities. Record redirect registrations, grant types and the application's chosen CSRF and PKCE guarantees.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace authorization initiation, transaction storage, callback validation, code exchange, issuer validation and local account linkage. Record where nonce is checked for an OIDC ID token and where the resource server validates access tokens.

**Firstness:** Capture transaction and session identifiers as digests, selected issuer/client and resulting local account ID. Compare the result with the initiating session and registered redirect policy.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A callback is accepted under the wrong initiating session or client because correlation is checked superficially or after account binding.

**Competing benign explanation:** A missing visible state value may be compensated by another correctly implemented protocol binding. Different identity-provider emails may intentionally represent different local accounts. Refresh reuse may have a documented concurrency grace policy.

## Deduction and controls

A valid callback completes only its own transaction; a mismatched or already consumed transaction must not bind the wrong identity. A wrong PKCE verifier must fail at exchange when PKCE is required.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Complete one normal flow for each test client and record the initiating session, issuer, redirect and resulting synthetic account.

2. Using only test artifacts, replay a completed callback and try a callback associated with the other synthetic browser transaction.

3. Exercise the client's documented wrong-verifier and mismatched-issuer test fixtures; compare with successful exchange controls.

4. Test one refresh rotation and one reuse after the documented grace interval; observe family state rather than assuming immediate global revocation.

5. Test account linking with an unverified and a verified synthetic identity under the application's linking policy; stop before any real account mutation.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

Code consumption by the harness can cause false failures. SameSite cookie behavior and popup flows can remove correlation cookies. Email equality is not an issuer-subject binding; provider verification semantics must be established.

## Evidence and deliverable

Retain a redacted transaction sequence with callback decisions, exchange error category, issuer/subject pair, client identifier and local account outcome. Store no reusable codes or bearer tokens in portable reports.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record provider profile, SDK, browser and grant configuration. Verify supported PKCE, PAR, JAR, JARM or DPoP behavior against the deployed version; none is assumed simply because a feature name appears in documentation.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Bind callback processing to the initiating transaction before account mutation; use exact registered redirect handling, proper issuer/client validation and verified identity linking. Make rotation/grace and family revocation explicit.

Log correlation failures, issuer mismatches, repeated code use and refresh family reuse without secret values. Validate alerts with the same synthetic transactions.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A callback from synthetic session B links B's identity into session A without the required transaction binding: CONFIRMED; FAIL. |
| Benign refutation | The visible state is absent but enforced PKCE and documented transaction binding reject the mismatched callback: REFUTED for the claimed callback swap; PASS for that case. |
| Insufficient evidence | An authorization URL contains a broad redirect value but callback acceptance was not observed: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/auth/offensive-oauth/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Replaces token capture and account takeover chains with measured transaction, issuer, refresh and linking controls; avoids universal state, cookie and lifetime prescriptions.

