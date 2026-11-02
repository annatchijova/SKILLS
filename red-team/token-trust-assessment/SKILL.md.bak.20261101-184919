---
name: token-trust-assessment
description: Test token validation and identity binding in application authentication. Use for JWT, JWKS, OAuth callback and stale-session reviews.
---

# Token Trust Assessment

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Establish the contract
Locate the actual token consumer and pinned library version. Record issuer, audience, intended token kind, allowed algorithms, key source, expiry policy and revocation semantics. Decode fixtures locally; never upload live tokens to online decoders.
Do not assume every JWT is a three-part signed JWS: distinguish JWE and the application's supported formats.

## Controlled validation
Create synthetic keys and tokens. Begin with an accepted baseline. Mutate one dimension per case: signature, issuer, audience, expiration, not-before, algorithm, token kind or key identifier.
Trace who selects the key and algorithm. Check that token-controlled headers cannot replace the configured trust source. A key lookup error is not proof of SSRF; use an isolated callback fixture to establish network access.
Test rotation and cache isolation across issuers with the same key identifier. Replay after role revocation only against the documented invalidation contract.
For OAuth flows, bind callback to the initiating session, client, redirect URI and authorization transaction; inspect state and PKCE enforcement where the flow requires them. Validate with synthetic accounts.

## Refutation and evidence
An unsigned token that merely decodes is not accepted authentication. Prove access to a protected synthetic resource using the modified token, and denial with a bad-signature control.
Do not call visible signed claims a confidentiality defect unless the application promised secrecy.
Deliver a validation matrix, key provenance, sanitized token fixtures, consumer trace and regression assertions. Report missing runtime verification as a hypothesis, not confirmed bypass.

## Required methodology and laboratory boundary

Read [the assessment methodology](../METHODOLOGY.md) before execution.
Use only synthetic signing keys, fixture accounts and a protected canary resource in an isolated consumer.
Set a finite token-case budget and stop once the specific validation failure is demonstrated.
Do not crack signing secrets, extract mobile credentials or upload tokens to third-party decoders.
Firstness records consumer acceptance and resource access; Secondness records the consumer's configured trust policy.
Thirdness distinguishes claim validation, key selection and lifecycle defects rather than calling every token anomaly an authentication bypass.

## Discriminator: issuer-scoped key selection

**Abduction:** a shared JWKS cache indexes solely by key identifier and imports trust across issuers.
**Benign rival:** the cache is scoped by issuer, and the resource consumer validates issuer/audience before honoring the principal.
**Deduction:** two owned synthetic issuers using the same key identifier must remain separate trust domains.
**Induction:** accept a normal fixture from the configured issuer, then inspect how a fixture from the second issuer resolves its key.
Keep the consumer configuration fixed; record issuer, key-source identifier and protected canary response.
Use a known invalid-signature fixture as a rejection control and a valid configured-issuer fixture as an acceptance control.
If either control behaves unexpectedly, resolve the harness or configuration issue before assigning a verdict.
Do not generate algorithm-confusion or key-injection attack chains; use the library's supplied conformance fixtures and inspect validation decisions.

## Additional boundaries to measure independently

- Distinguish accepted token kind from merely parsed JWS or JWE structure; reject the wrong intended use under the application contract.
- Check issuer, audience, expiration and not-before separately with synthetic fixtures and a recorded controlled clock.
- Record configured clock tolerance rather than imposing an arbitrary universal number of seconds.
- During rotation, identify cache expiry, refresh and stale-key behavior; a grace interval is not automatically a defect.
- Treat role revocation according to the documented session contract; some designs retain short-lived access until expiry.
- For sender-constrained tokens, inspect the declared proof or certificate binding with owned test keys and compare a mismatched fixture.
- Key-header parsing errors do not establish network access or path traversal; those effects require independent sink evidence.
- Signed claims are not inherently confidential; assess sensitive content against the application's privacy contract.

## Evidence, tools and failure modes

Retain validation decisions, consumer trace, key provenance, fixture digests and canary access results.
Never store private signing keys or reusable tokens in the portable report.
Pin JWT library, JWKS fetcher, cache and application versions, including validation options.
A decoder or token editor cannot prove authorization; browser/client token refresh may replace the intended fixture silently.
No runtime tool behavior was verified during this content rewrite.
Route callback initiation and account linking to rt-oauth; a JWT validation result does not establish OAuth flow safety.

## Remediation and detection

Bind trusted algorithms, issuer, key source and token kind in server configuration.
Scope key caches by the full trust context and make rotation failure behavior explicit.
Record categorized validation failures without token bodies; validate alerts for wrong issuer and bad signatures.
Add regression cases for key-identifier collision across issuers and accepted-versus-decoded tokens.
Remove fixture credentials and restore clock/cache configuration while preserving sanitized evidence.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| A token from an untrusted synthetic issuer grants the protected canary because its key identifier collides in the shared cache; controls behave correctly. | CONFIRMED; FAIL for trust isolation. |
| A malformed token decodes locally but the protected consumer rejects it and still accepts the valid control. | REFUTED for accepted authentication; PASS for that case. |
| A decoded token contains an unusual algorithm or key header, but no consumer validation was observed. | CANDIDATE; WARN. |

Acceptance cases specify expected behavior; they are not executed target tests.

## Provenance

Exact upstream path: `Skills/auth/offensive-jwt/SKILL.md`.
Treatment: Strengthens JWT consumer and key provenance controls without secret cracking or mobile token extraction; OAuth transaction mechanics remain distinct in rt-oauth.

Methodology adapted from Claude-Red `offensive-jwt` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

