---
name: validate-at-the-boundary
description: Validate untrusted inputs at the edge of the system — with a clear error raised at the boundary — instead of letting bad shape, bad dtype, non-finite values, or hostile paths explode deep inside a library or propagate as silent corruption. Use this whenever code ingests data from outside its own control — deserialized tensors/arrays, file paths from a caller, parsed JSON, anything fed to numpy/pandas/a parser, anything that becomes a filesystem operation. Triggers — an opaque numpy broadcast error, a NaN that appeared from nowhere, a path traversal or symlink concern, "validate input", "sanitize", "this crashed deep in a library". Push to use this whenever an external value reaches a sensitive operation without having been checked first.
---

# Validate At The Boundary

When a bad input reaches a sensitive operation unchecked, you get one of two bad outcomes: an opaque crash deep inside a library (a numpy broadcast error six frames down, with no hint which of your inputs was malformed), or — worse — silent corruption that propagates as a plausible wrong answer. Both are fixed the same way: validate the input at the boundary, where you still have the context to produce a clear error, before it reaches the operation that can't.

The boundary is wherever a value crosses from outside your control to inside it: a deserialized array, a path from a caller, a parsed payload, an embedding handed to `vstack`.

## What to check, and why there

**Shape and structure first.** Confirm the array is the expected shape, non-empty, and the right rank before any operation that assumes it. A single wrong-length vector slipped into a list will detonate inside `vstack` with a broadcast error that names nothing useful; the same check at the boundary says "embedding 3 has shape (383,), expected (384,)". Validate *each element* before the bulk operation, not after it fails.

**Finiteness.** Reject (or, in a hot path, neutralize) `NaN` and `Inf` before they enter arithmetic. A non-finite value does not crash — it spreads. One `NaN` in a dot product makes the result `NaN`, which makes the score `NaN`, which sorts unpredictably and corrupts everything downstream without a single exception. Check `isfinite().all()` at the boundary.

**Dtype contract, explicitly.** If the operation needs `float32` and the source is JSON (which only produces `float64`), decide the policy at the boundary: raise for binary sources that should have preserved dtype, coerce-with-a-warning for text sources that structurally can't. Don't let a silent dtype surprise change precision or behavior downstream.

**Paths, before they touch the filesystem.** A path from a caller is hostile until proven otherwise. Resolve it first (so `..` and links are collapsed), then confirm: it is a regular file (not a symlink, device, pipe, or socket), it is within the allowed base directory (reject traversal outside it), and it is under the size limit. Resolve-then-compare is the order that matters — comparing before resolving lets `../../etc/passwd` slip through.

## Raise — don't assert, don't swallow

A boundary check that uses `assert` disappears under `python -O`; the validation you were relying on is gone in production. Use an explicit `raise ValueError(...)` / `raise RuntimeError(...)` with a message that names the offending value. And never wrap the check in a bare `except Exception: pass` — swallowing the error reintroduces exactly the silent corruption the boundary was supposed to stop. (The one legitimate `except: pass` is a genuinely optional feature whose failure is logged — see `honest-degradation`.)

## Reject at the boundary, degrade only in the hot path

There are two correct responses to a bad input, and which one is right depends on where you are:

- **At an ingest/build boundary, reject loudly.** You can afford to fail — raise a clear, named error and let the caller fix the input. Example: building a model from a corrupt embedding list should raise, not guess.
- **In a hot path where a crash is worse than a safe default, degrade.** A per-query projection that hits a non-finite input should return a neutral zero vector rather than propagate `NaN` and take down the whole recall. That is the boundary between this skill and `honest-degradation`: reject when you can fail safely; degrade (visibly) only where failing would be the bigger harm.

Noticing which situation you're in is the skill. The same module legitimately does both: it *raises* on a corrupt input at build time and *returns zeros* on a corrupt input at query time.

## Tooling

`scripts/boundary_validators.py` provides `validate_array()` (two-phase shape-then-dtype with finiteness and non-empty checks), `validate_finite()`, and `sanitize_path()` (resolve, reject non-regular/symlink, enforce base-dir confinement and a size cap) — all raising explicit, named errors. Generalized from production tensor- and path-validation code; run it to see each rejection.
