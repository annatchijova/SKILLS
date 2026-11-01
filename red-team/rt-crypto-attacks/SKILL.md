---
name: rt-crypto-attacks
description: Assess cryptographic misuse through nonce lifecycle, authenticated processing and controlled error measurements using synthetic keys and messages.
---

# Cryptographic Implementation Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before defining a cryptographic claim.
Identify the required property: confidentiality, authenticity, freshness or key separation.
Do not certify a construction from an algorithm name or ciphertext length heuristic.

## Mechanisms and preconditions

- GCM nonce uniqueness is scoped to a key; duplicate nonce bytes under different keys
  are not the same defect. Track key-generation identity without exporting keys.
- Unauthenticated decryption becomes dangerous when plaintext or validity influences output.
- Secret-prefix hashes and HMAC are different constructions; inspect the exact composition.
- RSA public exponent alone does not establish weakness; padding and message constraints matter.
- Cryptographic randomness must survive restart, fork, snapshot restore and concurrent allocation.
- Password KDF suitability depends on parameters, salt, hardware budget and service constraints.
- Timing evidence requires controlling input length, execution path and environmental drift.

## Observation and baseline

Record library/build, construction, key identifier, nonce allocator and authentication order.
Use synthetic messages and ephemeral lab keys with no connection to production secrets.
Define an invariant such as "no repeated key-ID/nonce pair across independent encryptions"
or "no application side effect before ciphertext authentication succeeds."
Separate a code-level misuse from a demonstrated plaintext or forgery impact.

## Abduction and deduction

Hypothesis: nonce allocation restarts at a prior value while the same key remains active.
Benign rival: duplicate records are logging retries, or the restart changed the key.
Prediction: independently requested encryptions of distinct fixture messages after restart
reuse the pair; a persistent allocator or genuinely new key does not reuse that pair.
Record operation IDs so a duplicated log event cannot satisfy the oracle.

## Bounded laboratory procedure

1. Reproduce the relevant application path with synthetic keys and bounded input sizes.
2. Capture operation ID, key-generation ID and nonce for a small specified run budget.
3. Restart or fork the fixture in the suspected way; repeat independent operations.
4. Compare pair uniqueness and the allocator-corrected control without decrypting real data.
5. For authentication ordering, use library-generated invalid-tag fixtures and observe whether
   a mock application sink is reached; valid-tag fixtures prove the sink remains functional.
6. For error-oracle candidates, compare documented invalid classes of equal length in a local
   instrumented harness. Randomize order and record status, output length and integer timings.
7. Compare with a uniform-error implementation and an unrelated equal-length input control.
   Stop at evidence of distinguishability; do not recover secrets or construct forgeries.
8. Inspect MAC composition, KDF parameters and RNG sources from code/configuration;
   record unexecuted hypotheses separately from the measured nonce/authentication result.
9. Preserve sanitized measurements and configuration, then retire the lab keys and fixture.

## Failure modes and interpretation

Repeated ciphertext may reflect caching or deliberate deterministic encryption, not ECB.
Distinct error codes before cryptographic processing may be schema validation, not an oracle.
Network timing differences alone do not establish secret-dependent branching.
An invalid tag must prevent release/use of plaintext; internal decryption by a library is
not itself a failure if no unauthenticated plaintext escapes the API boundary.
XChaCha20-Poly1305's large nonce space is not nonce-misuse resistance; do not conflate them.
A length-extension concern does not apply unchanged to HMAC or unrelated hash constructions.

## Evidence, detection and remediation

Deliver the violated invariant, key-ID/nonce observations, operation IDs and controls.
For timing, retain sampling design and raw integer observations; avoid invented confidence.
Detect nonce allocation resets and authentication failures without logging plaintext or keys.
Use maintained authenticated-encryption interfaces, appropriate nonce management and KDFs.
Bind context through authenticated data and separate keys by purpose where required.
Retest restart, concurrency and invalid-input paths while preserving valid-message behavior.

## Versions and limits

Record crypto library, provider, runtime, platform and relevant configuration versions.
Verify current vendor guidance before using KDF thresholds or affected-version claims.
Custom schemes require specialist review; this workflow does not prove primitive security.
No decryption oracle exploit, key recovery or credential cracking ran during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Distinct operations reuse the same key-ID/nonce after restart; persistent allocator does not | CONFIRMED nonce-lifecycle defect; FAIL |
| Duplicate records share one operation ID and independent encryptions use unique pairs | REFUTED reuse claim for the observed duplicates; PASS |
| Ciphertext is block-aligned but construction and key lifecycle are unknown | CANDIDATE classification only; WARN |

## Provenance

Rewritten from `Skills/crypto/offensive-crypto-attacks/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain misuse and oracle preconditions; replace decryption, forgery, PRNG
cloning and cracking recipes with invariant checks and bounded synthetic measurements.
