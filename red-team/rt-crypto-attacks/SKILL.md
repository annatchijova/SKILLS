---
name: rt-crypto-attacks
description: "Red-team assessment of cryptographic-implementation boundaries: CBC padding oracles, ECB block manipulation, hash length-extension, RSA weaknesses (small-e, shared factors, Coppersmith), weak/predictable PRNG, AES-GCM nonce reuse, and timing side channels. Re-expressed as owned-fixture experiments against a disposable oracle with synthetic keys and negative controls instead of decrypting production secrets."
---

# Cryptographic-Implementation Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's crypto-attack craft as scoped experiments against an owned oracle with synthetic keys: it names the attack classes and their discriminators, proving a weakness on a disposable fixture rather than decrypting production data. Compose with `crypto-misuse-reasoning`.

## Scope and prerequisites

These attacks exploit implementation choices (mode, padding, nonce, key generation, timing), not broken primitives. Use an owned endpoint/oracle with synthetic keys and planted ciphertexts. Recover only planted plaintext; never target production secrets.

Declare target, construction, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **CBC padding oracle** — distinguishable padding-error responses → decrypt/forge.
- **ECB** — identical plaintext blocks → identical ciphertext blocks (detect, then manipulate).
- **Hash length extension** — `H(secret||msg)` MACs with a Merkle-Damgard hash → append.
- **RSA** — small `e` (Hastad broadcast), shared prime across keys (common-factor GCD), partial-key-exposure (Coppersmith), textbook RSA.
- **Weak PRNG** — predictable tokens (e.g. Mersenne-Twister state recovery from 624 outputs).
- **AES-GCM nonce reuse** — repeated nonce → authentication-key recovery.
- **Timing side channels** — comparison/HMAC timing leaking position.

## Mechanism and observation

Trace a ciphertext/token through the construction and the observable the implementation leaks.

**Firstness:** Record the distinguishing signal (padding-error vs valid response; repeated ciphertext blocks; timing delta; recovered planted plaintext). **Secondness:** State the secure baseline (constant-time, authenticated encryption, unique nonce, CSPRNG) and the deviation. **Thirdness:** Infer the class only after the oracle yields a controlled result on a fixture.

## Abduction and refutation

**Mechanism hypothesis:** The implementation leaks a distinguishable response (padding, timing) or reuses state (nonce, PRNG, prime) that collapses the security of a sound primitive.

**Competing benign explanation:** Errors are uniform and constant-time (no oracle); the mode is authenticated (AEAD) so tampering is rejected; nonces are unique; the RNG is a CSPRNG; the timing difference is noise, not key-dependent.

## Deduction and controls

A valid ciphertext/token behaves normally (positive control). A confirmed finding recovers/forges planted material via the oracle where a constant-time/authenticated/unique-nonce implementation would not leak. Predeclare the recovered fixture value or the statistical threshold (for timing). Uniform errors / AEAD rejection / unique nonce / CSPRNG are PASS controls.

## Induction: bounded laboratory procedure

Owned oracle; synthetic keys; planted ciphertexts.

1. **Baseline.** Submit a valid ciphertext/token; capture the normal response and timing distribution.
2. **Oracle probe.** CBC: flip the last byte, check for a distinguishable padding error. ECB: send repeated identical blocks, check for repeated output blocks.
3. **Decrypt/forge a planted value** (padbuster-class) against the oracle; stop at the planted plaintext.
4. **Length extension.** Confirm the hash is Merkle-Damgard; try key lengths (e.g. 8-32) with hashpumpy to forge an extended planted MAC.
5. **RSA/PRNG/GCM.** Extract `n,e`; check size/shared factors (GCD across scoped keys)/Coppersmith (RsaCtfTool/SageMath); collect PRNG outputs to clone state; detect nonce reuse across captured messages.
6. **Timing.** Use percentile statistics across many samples to separate key-dependent deltas from noise.
7. **Control.** Confirm a hardened construction does not leak.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

padbuster (CBC oracle), hashpumpy (length extension), RsaCtfTool + SageMath (RSA, Coppersmith), MT19937 cloning (624 outputs). Nonce reuse in AES-GCM is catastrophic (recovers the auth key). Shared-prime GCD works across a corpus of keys from the same bad generator. Timing attacks need statistical rigor to be more than noise.

## Domain-specific failure modes

A single timing sample is noise — require statistics. Uniform, constant-time error handling removes the padding oracle. AEAD rejects tampering, defeating malleability. A CSPRNG defeats state cloning. Recover only planted values; recovering production secrets is out of scope. "The library could be misused" is not a finding without a demonstrated oracle.

## Evidence and deliverable

Provide the construction, the oracle/leak, the recovered/forged planted value (or timing statistics), and the control result. Keep real keys/plaintext out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested constructions.

## Versions and tool limitations

Pin the crypto library and mode/version. Tools perform real recovery; use synthetic keys and planted data. No construction behavior was verified by this content; confirm the live construction first.

## Remediation and detection

Use authenticated encryption (AES-GCM/ChaCha20-Poly1305) with unique nonces, constant-time comparisons and uniform errors, HMAC (not `H(secret||msg)`), CSPRNGs, and vetted RSA with OAEP/large `e`/unique primes. Add a regression asserting the oracle does not distinguish. Detect padding-error response patterns and nonce reuse.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Planted plaintext/MAC is recovered/forged via the oracle, or nonce reuse is shown, where a hardened construction does not leak: CONFIRMED; FAIL. |
| Benign refutation | Uniform errors / AEAD / unique nonce / CSPRNG prevents the attack: REFUTED; PASS for the control. |
| Insufficient evidence | A timing hint without statistical separation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/crypto/offensive-crypto-attacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's padding-oracle, ECB, length-extension, RSA, PRNG, GCM-nonce and timing craft, re-expressed as owned-oracle experiments with synthetic keys and hardened controls, replacing production decryption with bounded fixture recovery. Composes with `crypto-misuse-reasoning`, `rt-tls-attacks`.
