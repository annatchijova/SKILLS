---
name: token-trust-assessment
description: "Red-team assessment of JWT and bearer-token trust boundaries: alg-none and RS256-to-HS256 confusion, weak-secret HMAC, kid injection (path traversal/SQLi), jku/x5u abuse, claim tampering, header injection, cross-token confusion, HMAC timing, and token-in-URL leakage. Re-expressed as owned-token experiments that prove a forged token is accepted against a negative control instead of attacking live sessions."
---

# Token Trust Boundary Assessment (JWT)

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's JWT craft as scoped experiments on owned tokens: it names the signature, algorithm and claim attacks, confirming that a forged token is accepted by the verifier where a correct control rejects it, rather than hijacking real sessions.

## Scope and prerequisites

Find where the app issues and verifies tokens. Use owned accounts and their own tokens; forge only tokens for owned identities. Confirm acceptance against an owned endpoint, not a victim's session.

Declare target, token type, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Algorithm** — `alg:none` (and case/encoding variants), RS256→HS256 confusion (public key used as HMAC secret).
- **Signature** — weak HMAC secret (brute force), missing verification, wrong key.
- **Header injection** — `kid` (path traversal to a predictable file, SQLi), `jku`/`x5u` pointing at an attacker JWKS.
- **Claims** — tamper `sub`/`role`/`exp`/`aud` and re-sign with a known/forged key.
- **Confusion** — JWT where an API key is expected (or vice versa).
- **Side channels** — HMAC verification timing; tokens leaked in URLs/logs; insecure mobile storage.

## Mechanism and observation

Decode the token; trace how the verifier selects the algorithm and key and what it checks.

**Firstness:** Record whether a modified/forged token for an owned identity is accepted (a protected response returns). **Secondness:** State the correct verification (fixed alg, pinned key, full claim checks) and the deviation. **Thirdness:** Infer the defect class only after a forged token is accepted under control.

## Abduction and refutation

**Mechanism hypothesis:** The verifier trusts token-supplied parameters (`alg`, `kid`, `jku`) or fails to verify the signature/claims, so a token the server did not issue is accepted.

**Competing benign explanation:** The library pins the algorithm and rejects `none`/confusion; `kid`/`jku` are ignored or allowlisted; the secret is strong; claims (`exp`,`aud`,`iss`) are fully validated; the endpoint rejects the forged token with 401.

## Deduction and controls

A legitimately-issued token is accepted (positive control); a forged/modified token must be rejected if verification holds. A confirmed finding has the forged owned-identity token accepted where the control rejects it. Predeclare the acceptance signal. Alg-pinning / strong secret / claim validation rejecting the forgery are PASS controls.

## Induction: bounded laboratory procedure

Owned identities only.

1. **Baseline.** Use a legitimate token; confirm a protected response and decode the header/claims.
2. **alg:none.** Strip the signature, set `alg:none` (+ case variants); submit; observe acceptance.
3. **RS256→HS256.** If RS256, sign with the public key as HMAC secret; submit.
4. **Weak secret.** For HMAC, attempt an offline dictionary crack of the owned token's signature; if found, forge claims.
5. **kid/jku.** Test `kid` path traversal/SQLi and `jku`/`x5u` pointing at your owned JWKS.
6. **Claim tamper.** Change an owned-identity claim (e.g. `role`) and re-sign with any key that the broken verifier would accept.
7. **Control.** Confirm the verifier rejects each forgery when correctly configured.

Record results including refutations. Keep finding and control status separate. Forge only owned identities; demonstrate acceptance, do not escalate to another user's data.

## Craft notes (leads)

jwt_tool automates inspection, the common attacks and HMAC cracking. `none` must be tried in multiple casings. RS256→HS256 requires the public key (often exposed at a JWKS endpoint). `kid` is a file/DB selector — traversal and SQLi both apply. `jku`/`x5u` acceptance of arbitrary URLs is a full forgery primitive. Tokens in URLs leak via logs/referrer; mobile storage (SharedPreferences/Keychain/backup) can leak them.

## Domain-specific failure modes

A decoded, tampered token that the server rejects is a refutation, not a finding. Alg-pinning libraries defeat none/confusion. A strong secret makes HMAC cracking infeasible (WARN, not FAIL). Acceptance must be shown by a protected response, not just a 200 error page.

## Evidence and deliverable

Provide the original token, the forgery, the attack class, the acceptance signal (protected response), and the control rejection. Forge only owned identities; keep real tokens out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested classes.

## Versions and tool limitations

Pin the JWT library and version — alg handling and `kid`/`jku` behavior are library-specific. jwt_tool performs real forgery attempts; use owned tokens. No verifier behavior was verified by this content; confirm the live library first.

## Remediation and detection

Pin the algorithm server-side, reject `none`, never derive HMAC keys from public keys, allowlist `kid` and disable `jku`/`x5u` (or allowlist), validate all claims (`exp`,`nbf`,`aud`,`iss`), use strong secrets/rotation, and keep tokens out of URLs. Add a regression asserting each forgery is rejected. Detect `alg:none`, external `jku`, and anomalous `kid` values.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A forged owned-identity token is accepted (protected response) where the control rejects it: CONFIRMED; FAIL. |
| Benign refutation | Alg-pinning / strong secret / claim validation rejects the forgery: REFUTED; PASS for the control. |
| Insufficient evidence | A tampered token with ambiguous (non-protected) response: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/auth/offensive-jwt/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's algorithm/signature/header/claim attack craft, re-expressed as owned-identity forgery experiments with verification controls, replacing live session hijacking with bounded acceptance proof. Composes with `rt-oauth`, `crypto-misuse-reasoning`.
