---
name: deterministic-core
description: Keep any consequential output path reproducible bit-for-bit and tamper-evident — no floats in the decision path, canonical typed serialization, SHA-256 sealing, and a determinism check. Use this whenever you build or review code that produces a verdict, score, decision, risk number, classification, or any result that will be audited, sealed, hashed, or relied on as evidence; whenever a hash changes between runs and shouldn't; whenever floating-point arithmetic sits anywhere near a result that must be exactly reproducible; and whenever someone says "reproducible", "deterministic", "seal", "chain of custody", "bit-for-bit", or "Daubert". Push to use this even when the user only says "scoring", "the decision logic", or "why does the output differ between machines".
---

# Deterministic Core

Some outputs only need to be approximately right. Others are load-bearing: a verdict, a score that decides an action, a number that goes into evidence. For those, "approximately reproducible" is a defect. If the same input can produce two different sealed results — across runs, machines, or dict orderings — the result cannot be defended as evidence, and the seal proves nothing. This skill is the discipline that makes a decision path reproducible bit-for-bit and tamper-evident.

There are four rules. They compound: each one is load-bearing for the seal.

## Rule 1 — No float in the decision path

Floating point is not deterministic enough for a load-bearing result. The same sum can differ by ordering, by platform, and by compiler; `0.1 + 0.2 != 0.3`. Any float in the path that produces a sealed number is a reproducibility violation waiting to surface on a different machine.

Use exact arithmetic in the decision path:

- `fractions.Fraction` for ratios, weights, likelihoods, and accumulations — exact, ordering-independent, and serializable as `numerator/denominator`.
- integers where the quantity is genuinely integral (counts, indices).
- `decimal.Decimal` with a pinned context only when you specifically need fixed decimal places and accept its rules.

Floats are fine in the *narrative* layer (a display rounding, a chart) — never in the layer whose output gets sealed. The boundary between "exact, sealed" and "approximate, cosmetic" must be explicit in the code.

## Rule 2 — Canonical, typed, versioned serialization

Two objects that mean different things must never serialize to the same bytes, and the same object must always serialize to identical bytes. That requires a single canonical encoder, used everywhere, with three properties:

- **Typed.** Encode the type, so `1` (int), `"1"` (str), `1.0` (float), and `True` (bool — check it *before* int, since `bool` subclasses `int`) are distinguishable. Untyped JSON collapses these and silently changes the hash's meaning.
- **Ordered.** Sort dict keys recursively. Dict and set iteration order must never leak into the bytes.
- **Versioned.** Stamp a `CANONICALIZE_VERSION` into the sealed payload. When you change the schema, bump it and keep the old verifier working, so historical bundles still validate.

Make it one module that is the single source of truth. Divergent ad-hoc canonicalizers (`"true:bool"` in one place, `"true"` in another) are how the same input ends up with two different hashes in two modules — the exact failure the seal is supposed to prevent. `scripts/canonicalize.py` is a ready-to-use typed/ordered/versioned encoder plus a `seal()` helper.

## Rule 3 — Seal with SHA-256 over the canonical bytes

The seal is `sha256(utf8(json(canonicalize(payload), sort_keys=True)))`. Compute it over the canonical form, not the raw object. Store the digest, the `CANONICALIZE_VERSION`, and enough chain-of-custody metadata (inputs, tool versions, timestamp recorded *outside* the sealed payload) that a third party can recompute and confirm. A verifier should be stdlib-only and independent of the producing code, so verification does not depend on trusting the producer.

## Rule 4 — Prove it: the determinism check

Determinism you do not test is determinism you do not have. Produce the result at least twice and assert the seals are identical. Better, do it in a way that would catch the usual leaks: re-order inputs, run in a fresh process, run on a second machine if you can. `scripts/determinism_check.py` runs a producer callable N times and reports the first divergence with a structural diff, so a nondeterminism bug points you at the offending field instead of just failing.

Common leaks to hunt: a float that sneaked into the path; `set` iteration order; `dict` ordering before a sort; an unpinned timestamp or RNG seed inside the sealed payload; `hash()` randomization (`PYTHONHASHSEED`); locale-dependent formatting.

## Why this is a feature, not overhead

A reproducible, sealed result is what lets you say "anyone can recompute this and get the identical digest" — which is the whole basis for treating an automated output as evidence rather than opinion. The cost (exact arithmetic, one canonicalizer, a check) is small and pays for itself the first time a result is challenged.

## Quick start

```python
from canonicalize import canonicalize, seal, CANONICALIZE_VERSION
from determinism_check import assert_deterministic

payload = {"decision": "FLAG", "posterior": str(Fraction(3, 7)), "edges": 12}
digest = seal(payload)                       # SHA-256 over canonical bytes
assert_deterministic(lambda: build_result(x), n=5)   # raises on first divergence
```
