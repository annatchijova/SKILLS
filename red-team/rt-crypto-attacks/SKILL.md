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
- **ECB** — equal, block-aligned plaintext blocks under the same key encrypt to equal ciphertext blocks. This reveals structure; it does not by itself establish an exploitable cut-and-paste impact.
- **Hash length extension** — `H(secret||msg)` MACs with a Merkle-Damgard hash → append.
- **RSA** — small `e` (Hastad broadcast), shared prime across keys (common-factor GCD), partial-key-exposure (Coppersmith), textbook RSA.
- **Weak PRNG** — predictable tokens (e.g. Mersenne-Twister state recovery from 624 outputs).
- **AES-GCM nonce reuse** — repeated nonce under the same key violates GCM's IV-uniqueness requirement, compromises confidentiality, and can enable authentication-key recovery or forgery under applicable message/tag conditions. Repetition alone confirms nonce misuse, not successful key recovery or forgery.
- **Timing side channels** — comparison/HMAC timing leaking position.

## Mechanism and observation

Trace a ciphertext/token through the construction and the observable the implementation leaks. Record library/build, construction, a non-secret key-generation identifier, nonce allocator and authentication order. Distinguish independent cryptographic operations from duplicate log records with operation IDs; never export keys or connect this fixture to production secrets.

**Firstness:** Record the distinguishing signal (padding-error vs valid response; repeated ciphertext blocks; timing delta; recovered planted plaintext). **Secondness:** State the secure baseline (constant-time, authenticated encryption, unique nonce, CSPRNG) and the deviation. **Thirdness:** Infer the class only after the oracle yields a controlled result on a fixture.

## Abduction and refutation

**Mechanism hypothesis:** The implementation leaks a distinguishable response (padding, timing) or reuses state (nonce, PRNG, prime) that collapses the security of a sound primitive.

**Competing benign explanation:** Errors are uniform and constant-time (no oracle); the mode is authenticated (AEAD) so tampering is rejected; nonces are unique; the RNG is a CSPRNG; the timing difference is noise, not key-dependent.

## Deduction and controls

A valid ciphertext/token behaves normally (positive control). A confirmed fixture result must name the proposition established: e.g. the fixture exposes a distinguishable oracle, recovers a planted plaintext, permits a forgery, or reuses an IV under one key. These are separate outcomes; do not infer recovery or forgery from nonce repetition alone. Predeclare the artifact or statistical decision rule. Record finding status separately from control status.

## Induction: bounded laboratory procedure

Owned oracle; synthetic keys; planted ciphertexts.

1. **Baseline.** Submit a valid ciphertext/token; capture the normal response and timing distribution.
2. **Oracle probe.** CBC: flip the last byte, check for a distinguishable padding error. ECB: send repeated identical blocks, check for repeated output blocks.
3. **Decrypt/forge a planted value** (padbuster-class) against the oracle; stop at the planted plaintext.
4. **Length extension.** Confirm the hash is Merkle-Damgard; try key lengths (e.g. 8-32) with hashpumpy to forge an extended planted MAC.
5. **RSA/PRNG/GCM.** Extract `n,e`; evaluate each RSA attack only after checking its prerequisites (for example, Håstad broadcast requires compatible unpadded instances of the same message for enough recipients with pairwise-coprime moduli). Check shared factors only across scoped keys; use Coppersmith only with a stated partial-information model. For GCM, group records by key identity and test IV uniqueness; report nonce misuse separately from any demonstrated plaintext recovery or forgery. Treat a CSPRNG as a design claim to verify in implementation and use, not as proof by label.
6. **Timing.** Predeclare the secret-dependent contrast, randomized/interleaved sampling plan, sample size or stopping rule, noise controls, effect estimate and uncertainty. Percentiles may describe distributions but do not alone establish secret-dependent leakage.
7. **Control.** Confirm a hardened construction does not leak.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

The upstream attack catalog includes CBC padding-oracle, hash length-extension, RSA, weak-PRNG and GCM-nonce classes. Treat tools as leads and only use synthetic fixture data. GCM nonce reuse under one key is a serious confidentiality/authenticity failure; recovery of the GHASH subkey or a successful forgery depends on available messages, lengths and tag conditions and must be demonstrated separately. Shared-prime GCD requires an appropriately scoped corpus. Timing claims need a predeclared statistical design.

## Domain-specific failure modes

A single timing sample is noise — require statistics. Uniform error text alone does not rule out an oracle: compare externally observable behavior, including timing, status, response size, connection handling and downstream effects. A genuinely indistinguishable externally observable behavior can remove this oracle. AEAD verification before plaintext is trusted prevents unauthenticated modification, assuming correct use and key/nonce discipline. A correctly implemented and used CSPRNG is designed to resist relevant state-recovery attacks; the label alone is not evidence. Recover only planted values; recovering production secrets is out of scope. "The library could be misused" is not a finding without a demonstrated oracle.

## Evidence and deliverable

Provide the construction, the oracle/leak, the recovered/forged planted value (or timing statistics), and the control result. Keep real keys/plaintext out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested constructions.

## Versions and tool limitations

Pin the crypto library and mode/version. Tools perform real recovery; use synthetic keys and planted data. No construction behavior was verified by this content; confirm the live construction first.

## Remediation and detection

Use authenticated encryption with correct nonce management, authenticate before releasing or acting on plaintext, use HMAC rather than a secret-prefix hash construction, and use a correctly implemented CSPRNG. For RSA encryption, use a vetted scheme such as OAEP with appropriate key-generation parameters; a large public exponent alone is not a general remedy for RSA misuse. Add regressions for the specific oracle and lifecycle invariants. Detect externally distinguishable invalid-input behavior and same-key nonce reuse without logging secrets.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | State exactly what the experiment confirmed on which system: fixture-oracle behavior, planted plaintext recovery, forgery, or same-key IV reuse. Do not promote one result to another: CONFIRMED for that scoped proposition; report control status separately. |
| Benign refutation | Uniform errors / AEAD / unique nonce / CSPRNG prevents the attack: REFUTED; PASS for the control. |
| Insufficient evidence | A timing hint without statistical separation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/crypto/offensive-crypto-attacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's padding-oracle, ECB, length-extension, RSA, PRNG, GCM-nonce and timing craft, re-expressed as owned-oracle experiments with synthetic keys and hardened controls, replacing production decryption with bounded fixture recovery. Composes with `crypto-misuse-reasoning`, `rt-tls-attacks`.
