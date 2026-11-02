---
name: api-boundary-assessment
description: "Red-team assessment of API security boundaries against the OWASP API Top 10: BOLA/IDOR, broken auth and token lifecycle, excessive data exposure, BFLA and mass assignment, REST verb/content-type tampering, SSRF via parameters, gRPC (reflection, metadata, BOLA) and WebSocket (origin, CSWSH) testing, plus versioning/misconfiguration. Re-expressed as scoped experiments on owned accounts with bounded sets and negative controls."
---

# API Security Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's API-security craft as scoped experiments mapped to the OWASP API Top 10, confirming each class on owned accounts with bounded request sets rather than enumerating real users.

## Scope and prerequisites

Collect the API surface (specs, Swagger, gRPC reflection, WebSocket endpoints). Use owned accounts across roles and a disposable instance. Bound enumeration and rate-limit probes.

Declare target, protocols, attempt budget, stop condition. Spec-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes (OWASP API Top 10 2023)

- **BOLA/IDOR** — object-level authorization (see `rt-idor`).
- **Broken auth** — missing login rate limits, token lifecycle (expired, post-password-change, malformed bearer accepted).
- **Excessive data exposure** — endpoints returning more than the UI shows.
- **BFLA** — function-level: admin methods reachable with a user token.
- **Mass assignment** — unexpected writable properties.
- **Verb/content-type tampering** — method override, content-type switch, parameter pollution (see `rt-parameter-pollution`).
- **SSRF via parameters** (see `rt-ssrf`).
- **gRPC** — reflection enumeration, metadata injection, BOLA/BFLA over gRPC.
- **WebSocket** — origin validation, CSWSH.
- **Misconfiguration** — version sprawl, exposed docs/debug, CORS, missing security headers.

## Mechanism and observation

Trace a request to the authorization/validation performed and the data returned.

**Firstness:** Record the access or data obtained outside the account's intended scope (another owned object; an admin method succeeding with a user token; fields beyond the UI). **Secondness:** State the intended policy and the deviation. **Thirdness:** Infer the class only after a controlled request confirms it on owned accounts.

## Abduction and refutation

**Mechanism hypothesis:** Authorization or validation is enforced inconsistently across objects, functions, verbs, protocols or versions, so one path grants access another denies.

**Competing benign explanation:** Every path enforces the same checks; the admin method returns 403; the extra fields are not actually returned/accepted; an old API version is deprecated and gated; CORS reflects only allowlisted origins.

## Deduction and controls

A properly-scoped request succeeds (positive control); the out-of-scope request must be refused if controls hold. A confirmed finding obtains the out-of-scope access/data on owned accounts where the control refuses. Predeclare the confirming artifact. Consistent enforcement across paths is a PASS control.

## Induction: bounded laboratory procedure

Owned accounts across roles; bounded sets.

1. **Baseline.** Authenticate per role; capture legitimate access and controls.
2. **BOLA/BFLA.** Access another owned object (user token); call an admin method with a user token.
3. **Token lifecycle.** Replay an expired/post-password-change token; send a malformed bearer.
4. **Mass assignment / verb / content-type.** Inject non-user fields; tamper methods and content types.
5. **gRPC/WebSocket.** Enumerate via reflection; test metadata injection and BOLA; test WS origin/CSWSH from an owned page.
6. **Misconfig.** Enumerate versions; check exposed docs/debug, CORS, headers.
7. **Control.** Confirm scoped requests behave and the out-of-scope path is refused.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Tooling: grpcurl (reflection), mitmproxy gRPC addon (`--mode reverse`), websocat (WS/origin), Burp/Arjun (discovery). CSWSH applies when the WS handshake trusts cookies without origin checks. Old API versions often lack newer authz fixes. Method-override headers can bypass method-based WAF rules.

## Domain-specific failure modes

A 200 is not access — confirm the body is out-of-scope data (see `rt-idor`). A deprecated version that is gated is a refutation. CORS reflecting only allowlisted origins is a PASS. Excessive-exposure requires the field to actually be returned, not merely present in a schema.

## Evidence and deliverable

Provide the endpoint/protocol, the account/role context, the out-of-scope access/data obtained, and the control refusal. Use owned accounts; keep real data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered endpoints.

## Versions and tool limitations

Pin the API framework, gateway and gRPC/WS stack versions. Tools enumerate aggressively; bound them. No endpoint behavior was verified by this content; confirm the live API first.

## Remediation and detection

Enforce object- and function-level authorization uniformly across REST/gRPC/WS and versions, validate token lifecycle, allowlist writable fields, restrict verbs/content-types, validate URL parameters (SSRF), enforce WS origin, and deprecate old versions. Add regressions per class. Detect cross-scope access, admin-method calls by user tokens, and verb/content-type anomalies.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An out-of-scope object/function/data is obtained on owned accounts where the control refuses: CONFIRMED; FAIL. |
| Benign refutation | Uniform enforcement refuses the out-of-scope path: REFUTED; PASS for the control. |
| Insufficient evidence | A 200 with ambiguous body / unconfirmed field exposure: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/api/offensive-api-security/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's OWASP-API-Top-10, gRPC and WebSocket testing craft, re-expressed as owned-account experiments with bounded sets and uniform-enforcement controls, replacing real-user enumeration with scoped boundary proof. Composes with `rt-idor`, `rt-parameter-pollution`, `rt-ssrf`, `token-trust-assessment`.
