---
name: honest-degradation
description: Make code that runs on degraded, legacy, reconstructed, or unverifiable input fail visibly instead of returning a plausible-but-wrong answer. Use this whenever you write or review backward-compatible deserialization, loaders for data saved by an older schema, best-effort guarantees, optional components that may be absent, health/test states that are "not quite pass", or any path that fills in a missing value — anywhere "it ran without error" could be hiding "it ran on bad data". Push to use this whenever you see a fallback, a default-for-a-missing-field, a best-effort claim, or a try/except that lets execution continue, even if the user hasn't flagged it as a correctness concern.
---

# Honest Degradation

The most dangerous output is not an error — an error gets noticed and fixed. The most dangerous output is a confident, well-formed, *wrong* answer produced silently from degraded input: a model projected over a reconstructed-as-zero centre, a test suite that counted an unverified environment as PASS, a result computed from a legacy field that no longer means what its type says. The system "worked"; the answer is garbage; nobody knows. This skill is the discipline that makes degradation loud and safe instead of silent and wrong.

The principle behind all of it: **when you cannot guarantee correctness, never emit a result that looks correct. Mark it, report a distinct state, warn at the boundary, and force the safe path.** Documented limitations are an asset, not a weakness — a known WARN is worth more than a false PASS.

## The six patterns

**1. A reconstructed value is not the real value — flag it.** When you fill a missing field with a default (zeros for an absent mean vector, an empty dict for missing config), the object no longer represents what its type claims. Set an explicit flag on it (`requires_rebuild = True`) and have every downstream validity/staleness check honor that flag, so the system rebuilds from real data instead of silently computing over the wrong basis. The flag is not optional bookkeeping; it is the only thing standing between "loaded successfully" and "loaded successfully and now lying".

**2. Distinguish "can't confirm" from "confirmed good" from "confirmed bad".** A two-state PASS/FAIL has nowhere to put "this guarantee is best-effort and this environment did not confirm it" — so it gets recorded as PASS, and a real weakness disappears into a green check. Use three states: PASS / WARN / FAIL. Count and surface WARNs separately in the summary. Critically, a child process that *failed* must never be folded into PASS because the parent didn't check its exit code — that is a false PASS masquerading as health.

**3. Name the guarantee level — in the schema, the docstring, and the header.** If a property holds strongly in one regime and only best-effort in another (deterministic intra-process, best-effort cross-process), state that explicitly everywhere a reader might look, and serialize it as a field (`"determinism_level": "best_effort"`) so other code can read the honest claim. An optimistic blanket guarantee that quietly fails on someone else's machine is worse than a modest one that holds.

**4. Warn at the boundary where degradation enters.** Emit the warning the moment you take the degraded path — the legacy load, the dtype coercion, the persistence failure — not later, not never. The caller is the one who can decide whether degraded is acceptable for their use, and they can only decide if they were told. A silent coercion or a swallowed fallback removes their ability to choose.

**5. An absent optional component degrades the feature, never the core — but discloses.** Wrap the optional import; if it is missing, disable the dependent feature, log the fact once, and make sure its absence cannot break the core path (`except Exception: pass` *only* where the feature is genuinely optional and its failure is logged). The core keeps working; the disclosure exists; the feature is simply off.

**6. A failure in a non-critical step must not destroy valid work from a critical one.** A persistence error — locked database, full disk — must not discard a correctly computed in-memory result. Warn and return the valid result; let the caller retry the write. Conflating "I couldn't save it" with "I couldn't compute it" throws away good work over a recoverable I/O problem.

## Why this is the Daubert posture

A system that documents and surfaces its own limitations is more trustworthy, not less — its claims can be relied on precisely because it does not overclaim. An ABSTAIN, a WARN, a `requires_rebuild` flag are features: they are the system telling the truth about the boundary of what it can stand behind. The failure to avoid is the opposite — a uniform green that cannot distinguish "verified correct" from "ran without crashing".

## Tooling

`scripts/tristate_runner.py` is a minimal check runner that treats PASS / WARN / FAIL as distinct outcomes, counts WARNs separately, and never lets a non-PASS hide in the pass count — generalized from a determinism-aware test suite. `references/patterns.md` has the concrete code shapes for the reconstructed-value flag, the level-in-schema field, and the boundary warning, with the failure each one prevents.
