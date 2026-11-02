---
name: rt-open-redirect
description: "Red-team assessment of open-redirect boundaries: redirect parameters, OAuth/post-auth return URLs and URL shorteners. Covers domain-spoofing, encoding, protocol-confusion, path-based and special-character bypasses as a validator-vs-navigator differential, re-expressed as owned-fixture experiments confirming the final navigation target with negative controls rather than live phishing or token theft."
---

# Open Redirect Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's open-redirect craft as scoped experiments: it names the bypass families and the high-impact contexts (OAuth, post-auth), confirming the actual navigation target rather than staging a live phishing or token-theft chain.

## Scope and prerequisites

Find parameters that influence a redirect (`?next=`, `?url=`, `?return=`, `?dest=`), including OAuth `redirect_uri` and post-authentication returns. Point redirects only at an owned domain you control; confirm by the final location, not by harm to a victim.

Declare target, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED. Token/credential theft via redirect is an impact class to reason about, not to execute against real users.

## Mechanism and observation

Trace the parameter to the redirect sink and the validation between them.

**Firstness:** Record the final `Location`/navigation when the parameter points at an owned external domain. **Secondness:** State the intended policy (redirect only to same-origin or an allowlist) and the deviation. **Thirdness:** Infer open redirect only after a controlled external navigation to an owned domain succeeds.

## Abduction and refutation

**Mechanism hypothesis:** The validator checks a representation of the destination (prefix match, substring, pre-normalization) that differs from what the browser ultimately navigates to.

**Competing benign explanation:** Only a path (no host) is accepted and the external value is rejected or treated as a relative path; the allowlist genuinely holds; the redirect is a same-origin 302 that ignores the parameter; the browser treats the crafted value as same-origin.

## Deduction and controls

A same-origin/allowlisted value redirects normally (positive control); an owned-external value must be refused if validation holds. A confirmed finding navigates to your owned external domain where the control refuses. Predeclare the owned target host. A validator that forces same-origin is a PASS control.

## Induction: bounded laboratory procedure

Owned external domain only.

1. **Baseline.** Supply an allowed value; confirm normal redirect behavior and how the parameter is validated.
2. **Direct external.** Point at your owned external domain; observe the final navigation.
3. **Bypass families (validator-vs-navigator differential).** Test: scheme-relative `//owned.example`, `https:owned.example`, backslashes `\/\/`, `@`-userinfo (`https://trusted@owned.example`), encoded/double-encoded separators, whitespace/control chars, trailing-dot and case, path-based `/trusted.com/../owned.example`, data/javascript schemes where the sink allows.
4. **High-impact contexts.** Test OAuth `redirect_uri` loosening (path/subdomain/suffix match) and post-auth returns — point only at an owned domain and reason about the token-leak impact.
5. **Control.** Confirm the allowed value still forces same-origin.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

CDN/reverse-proxy quirks can re-interpret the host. Browsers differ on scheme-relative and backslash handling — pin the client. OAuth suffix/substring matching (`trusted.com.attacker.com`, `trusted.com@attacker.com`, open subdomain) is the high-value variant because a loose `redirect_uri` leaks the authorization code/token. URL shorteners that follow the parameter inherit the redirect.

## Domain-specific failure modes

A relative-path-only redirect is not open redirect. A reflected parameter that is not actually used in the `Location` is not a finding. Browser normalization can make a crafted value same-origin (refutation) or external (confirmation) — verify the real navigation. Impact depends on context: a bare open redirect is low; an OAuth `redirect_uri` bypass that leaks a token is high.

## Evidence and deliverable

Provide the parameter, the bypass string, the final navigation target (owned domain), the context (plain vs OAuth/post-auth), and the control result. Do not involve real users. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered parameters.

## Versions and tool limitations

Pin the browser/client and any URL-parsing library — behavior is implementation-specific. No navigation behavior was verified by this content; confirm the live redirect and client first.

## Remediation and detection

Redirect only to same-origin or a strict host allowlist (parse and compare the resolved host, not a prefix), map user input to an internal ID rather than a raw URL, and for OAuth enforce exact `redirect_uri` matching. Add a regression asserting an external value is refused. Detect external hosts in redirect parameters correlated to the request.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The app navigates to an owned external domain via a crafted value where the control forces same-origin: CONFIRMED; FAIL (impact scoped to context). |
| Benign refutation | The external value is rejected or treated as a relative path: REFUTED; PASS for the control. |
| Insufficient evidence | The parameter is reflected but not shown to drive navigation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-open-redirect/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's bypass families and OAuth/post-auth high-impact contexts, re-expressed as owned-domain navigation experiments with same-origin controls, replacing live phishing and token theft with bounded navigation proof.
