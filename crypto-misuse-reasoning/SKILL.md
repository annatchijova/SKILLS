---
name: crypto-misuse-reasoning
description: Judge a cryptographic system by how it is used, not by which primitive it names — because "we use AES-256" says nothing, and almost every real-world break is a misuse (reused nonce, ECB, unauthenticated ciphertext, a padding oracle, a homemade KDF, an accepted downgrade) sitting on top of a perfectly good algorithm. Use whenever crypto is being designed, reviewed, or trusted: "is this encryption secure", "we roll our own", "AES/RSA/we're fine", "how should I encrypt this", "sign then encrypt or encrypt then sign", "why is a nonce/IV a problem", "is ECB ok here", "verify this token/JWT", "compare passwords", "our TLS config". Sibling of secure-by-construction (build it hostile-first) and validate-at-the-boundary (a decrypted blob is still untrusted input); it reasons about misuse, not primitive selection. It does not implement primitives, does not hand out attack recipes, and never certifies a scheme secure from the algorithm name alone.
---

# Crypto Misuse Reasoning

The name of the primitive is the least interesting fact about a cryptographic system.
"We use AES-256-GCM" tells you nothing about whether the nonce repeats, whether the
ciphertext is authenticated before it is trusted, whether the key came from a password
through a real KDF or a single SHA-256, or whether an attacker can force a downgrade to
a weaker path. The algorithm is almost never the break. **The misuse is the break** —
and misuse lives in the composition, the parameters, and the surrounding code, not in
the cipher.

Two symmetric failure modes, and this skill exists to catch both:

- **Primitive-name assurance.** "It's AES, it's fine." A green checkmark on the cipher
  choice while the mode is ECB, the IV is a constant, or the MAC is missing entirely.
  The strongest cipher in the world, used wrong, is a plaintext leak with extra steps.
- **Roll-your-own, including the "small" glue.** Not just inventing a cipher — that is
  obviously reckless — but the quieter version: a hand-built token format, a custom
  "encrypt then base64" with no integrity, a password comparison with `==`. The danger
  is in the parts people do not think of as "crypto."

The through-line: crypto fails at the seams — where two correct primitives are
composed incorrectly, where a parameter that must be unique is not, where ciphertext is
trusted before it is verified. Reason about the seams.

Composes with the library:

- **secure-by-construction** — a hostile user picks the nonce, forces the downgrade, replays the token; design for that user
- **validate-at-the-boundary** — a decrypted or verified blob is still untrusted input until parsed safely; decryption is not validation
- **deterministic-core** — determinism is a virtue in a sealed decision path and a catastrophe in encryption (deterministic ciphertext leaks equality); keep the two worlds straight
- **red-team-auditing** — "this is secure" is a CONFIRMED claim; a break needs a demonstrated one, and absence of an obvious break is not proof of security
- **secret-lifecycle-discipline** — a key is a secret with a lifetime; the strongest scheme dies with a leaked or never-rotated key

---

## Step 1 — Name the guarantee the scheme is supposed to provide

Before judging anything, state what property this crypto must deliver, because misuse
is a gap against that property, not against a vibe:

- **Confidentiality** — the plaintext stays secret. (Encryption alone.)
- **Integrity / authenticity** — the ciphertext or message cannot be altered or forged.
  (A MAC or signature — *encryption does not provide this*, and assuming it does is the
  single most common misuse.)
- **Non-repudiation, freshness, forward secrecy** — distinct properties, each requiring
  distinct machinery (signatures, nonces/timestamps, ephemeral keys).

A scheme that provides confidentiality but not integrity, deployed where integrity was
the actual requirement, is broken even though every primitive in it is sound. Most
"encryption bugs" are really "we needed authenticated encryption and shipped raw
encryption."

---

## Step 2 — Hunt the uniqueness invariants: nonces, IVs, and randomness

A large fraction of real breaks are a value that had to be unique or unpredictable and
was not. This is the highest-yield place to look:

- **Nonce / IV reuse** — reusing a nonce under the same key in a stream cipher or GCM is
  catastrophic (it can leak plaintext XOR and, for GCM, the authentication key). A
  counter that resets, a hardcoded IV, an IV derived from static data — all reuse.
- **ECB mode** — no IV at all; identical plaintext blocks produce identical ciphertext
  blocks. Equal-looking data leaks structure (the classic visible-penguin image). Treat
  ECB in any confidentiality context as a finding.
- **Predictable "randomness"** — an IV, key, or token from a non-cryptographic RNG, a
  timestamp, or a weak seed is not random. Distinguish a CSPRNG from `rand()`.
- **Deterministic encryption used unknowingly** — if identical plaintext must produce
  identical ciphertext (for search/dedup), that is a deliberate confidentiality
  tradeoff (it leaks equality), not a default to stumble into.

---

## Step 3 — Check that ciphertext is authenticated before it is trusted

Order of operations at the boundary decides whether a padding-oracle-class attack
exists:

- **Encrypt-then-MAC / AEAD** — verify the tag *before* decrypting or acting. If the tag
  fails, the ciphertext never becomes plaintext you process. This is the safe shape.
- **MAC-then-encrypt / encrypt-and-MAC / no MAC** — decrypting first and revealing (even
  through timing or error differences) whether padding was valid hands the attacker a
  decryption oracle. The bug is the *order and the leak*, not the cipher.
- **Unauthenticated ciphertext** — if anyone can flip bits in transit and you cannot
  tell, you have confidentiality without integrity (see Step 1). A decrypted blob that
  was never authenticated is attacker-controlled input; hand it to
  `validate-at-the-boundary`, do not trust it because it "decrypted successfully."

---

## Step 4 — Follow the key: derivation, storage, comparison, lifetime

The scheme is only as strong as the key handling around it:

- **Password-derived keys** — a password must pass through a real, tunable KDF
  (argon2/scrypt/bcrypt/PBKDF2 with sane cost), *not* a single fast hash. A SHA-256 of a
  password is not a key-derivation function.
- **Comparison** — comparing MACs, tokens, or password hashes with a non-constant-time
  `==` leaks via timing. Use constant-time comparison for any secret-dependent equality.
- **Storage and lifetime** — where the key lives, who can read it, whether it is ever
  rotated (`secret-lifecycle-discipline`). A signing key compromise is retroactive: it
  forges everything, past and future.
- **Reuse across purposes** — one key for encryption and MAC, or across contexts,
  violates domain separation and can enable cross-protocol attacks. Separate keys per
  purpose.

---

## Step 5 — Assume the attacker chooses the weakest allowed path

Security is set by the worst path the system permits, not the best one it advertises:

- **Downgrade / negotiation** — if the protocol will accept a weaker cipher, an
  unauthenticated mode, `alg: none` in a JWT, or an old TLS version, the attacker
  negotiates exactly that. Enumerate what is *accepted*, not what is *preferred*.
- **Trusting attacker-supplied parameters** — a token that names its own algorithm, a
  message that carries its own IV/salt with no binding, lets the attacker pick
  favorable parameters. Bind or fix the security-critical ones server-side.
- **Error and side channels** — distinct error messages, timing differences, and
  compression (CRIME/BREACH-class) leak the secret without breaking the math.

---

## Step 6 — Grade honestly; ABSTAIN beats a false "secure"

Cryptographic judgments carry outsized weight, so calibrate like the rest of the
library:

- **State what you checked and what you did not.** "AEAD with unique nonces confirmed;
  key management not reviewed" is honest. A blanket "the crypto is fine" is the overclaim
  `red-team-auditing` forbids.
- **A demonstrated misuse is a finding; a suspected one is a hypothesis.** Do not assert
  a break you have not shown, and do not assert security you have not verified.
- **ABSTAIN when the scheme is non-standard.** Custom constructions warrant "cannot
  certify; recommend a vetted standard scheme (a named AEAD, a maintained TLS/JOSE
  library)" — a documented "I cannot vouch for this homemade protocol" is worth more
  than a confident guess. Do not produce attack recipes; produce the judgment and the
  safe alternative.

---

## The one-line test

If your assurance rests on the primitive's name — "it's AES, it's RSA, it's fine" — you
have not reviewed the cryptography; you have read the label. The security lives in the
nonce, the mode, the MAC-then-decrypt order, the KDF, and the weakest path the protocol
will accept — check those, or state that you did not.
