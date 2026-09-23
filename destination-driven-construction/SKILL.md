---
name: destination-driven-construction
description: Build toward a chosen, ambitious final product in coherent levels — each one architecturally compatible with the destination, useful standalone, and carrying the invariants (security, persistence, authority boundaries) it will need later, never bolted on afterward. Use whenever planning or building a project meant to be kept, used, or maintained — including a hackathon project. Trigger on "let's scope this as an MVP", "build a quick prototype first", "we'll add security/tests/proper persistence later", "hackathon deadline", "what should v1 include", or any plan that phases work by technical concern (auth now, security later) instead of by a coherent state of the target product. Never suggest MVP-shaped scoping unless explicitly asked, even under a deadline. Composes with secure-by-construction (invariant inheritance), red-team-auditing (per-level and integrated adversarial review), and falsifiable-testing (explicit boundary on validation cadence — see below, this skill does not invent a TDD requirement).
---

# Destination-Driven Construction

This is a stated methodology, not a universal claim about how software should
be built — a different workflow than MVP-first iteration, adopted because the
systems built this way are meant to be kept, used, and maintained, not
discarded after a demo. Do not generalize it to other people's projects or
present it as the objectively correct approach; apply it because it's the
standing instruction for this author's work.

The organizing idea: the target is the *ambitious final product*, known and
named before construction starts — treated like a game with a final level.
Reaching it is winning. What varies with time and constraint is not the
target, but how many coherent levels toward it get built. The distinctive
trait is not the leveling mechanism by itself — staged delivery and similar
patterns also build in stages. It's that **every level is built with
knowledge of, and architectural compatibility with, the destination**, and
inherits the destination's load-bearing invariants from level 1, not as an
add-on once the "real" version starts.

> **When time runs out, stop at the highest coherent level reached. Do not
> replace unreached levels with disposable approximations.**

Composes with the library:

- **secure-by-construction** — that skill already names "we'll add auth
  later" as an anti-pattern for a single feature/diff; this skill applies
  the same refusal at the scale of an entire project's phasing — a
  security-first project's level 1 already has correct authority
  boundaries, not a security level bolted on afterward
- **red-team-auditing** / **invariant-hunting** — the mechanism for the
  validation cadence below: each new level gets adversarially reviewed, and
  the review specifically checks that the previous levels' invariants
  survived the transition
- **falsifiable-testing** — a distinct axis, not a competing one; see "The
  boundary with falsifiable-testing" below — read that section before
  assuming this skill changes per-change testing obligations
- **decision-record-discipline** — an irreversible architectural choice
  made at a given level (the one that fixes what later levels can build on)
  gets recorded with its Forces/Assumption/Revisit-trigger, the same as any
  other decision
- **irreversible-action-gate** — "abandonable without destroying already-
  demonstrated value" (below) is this skill's version of that skill's
  reversibility classification, applied to architectural choices rather
  than individual actions

---

## What a level is, and is not

A level is **a coherent state of the target product** — not a feature, not a
phase defined by technical concern, and not a prototype. **MUST NOT** shape
levels as "P0: auth, P1: security, P2: observability, P3: tests" — security is
not a later level if the project is security-first; it's a property every
level has from its first one, the same way `secure-by-construction` treats it
for a single change.

Each level **MUST** be:

- **Architecturally compatible with the destination** — nothing about it
  requires the destination's later levels to bypass or rebuild it.
- **Useful by itself** — a level is real, deliverable progress, not
  scaffolding waiting to be replaced.
- **Complete enough to constitute genuine progress**, not a thin slice that
  merely demonstrates a technical possibility.
- **Built with the invariants it will need later already in place** — the
  persistence strategy, the authority model, the determinism/integrity
  properties the destination requires, established at the level that first
  needs them, not deferred to a "hardening" pass.
- **Extensible without becoming scaffolding** — the next level builds on it,
  it doesn't replace it out of necessity.
- **Abandonable without destroying demonstrated value** — if direction
  changes, the levels already built still stand as real, usable progress;
  they are not sunk cost wrapped around a decision that turned out wrong.

## Reduce depth, not integrity

Under a real time constraint (a hackathon deadline, a sprint boundary), the
correct response is to **reach fewer levels, built correctly** — never to
build thin, precarious versions of every planned level to maximize apparent
feature coverage. Five levels built with their invariants intact are a
shippable, coherent state of the product. Eight levels built as
approximations are not eight levels — they're one fragile thing wearing
eight labels.

**MUST NOT** suggest scoping down to an MVP, a "quick version for the demo,"
or a prototype that the author does not intend to keep — not even under a
hackathon deadline — unless the author explicitly asks for that trade-off.
The default assumption for this author's projects is that the system is
meant to be kept, used, or maintained afterward; treat a deadline as a
reason to reduce the number of levels attempted, not as a reason to lower
what "done" means for the levels that are attempted.

## Validation cadence

**MUST NOT** automatically run a full regression/integration suite between
each level as a matter of course. **MUST**, instead, subject each new level
to an adversarial review (per `red-team-auditing`) as it's built, checking
two things: that the new level itself holds up, and that it preserves the
invariants established by the levels before it (per `invariant-hunting`'s
T0→Tn framing, applied across levels instead of within one transition).
Once the time-available horizon is reached (L1 through Ln), **MUST** run an
integrated adversarial review across the accumulated levels together, and
only then run integrated testing/verification. The expectation this cadence
is built for: the final suite *confirms* a reasoned construction — it is not
the first moment anyone learns whether the pieces are actually compatible.

**MAY** run tests between levels when explicitly requested — this cadence is
the default, not an prohibition on ever testing before the end.

### The boundary with falsifiable-testing — read this before inferring a new rule

**This skill does not waive, weaken, or replace any evidence or verification
requirement that another skill in this corpus already imposes.** If
`falsifiable-testing` (or `secure-by-construction`, or any other skill)
requires a red-first test, a specific oracle, or local verification for a
particular claim or change, that requirement still applies, at the point it
applies, regardless of what level is being built. This skill governs one
thing only: the cadence of the *integrated* regression/verification suite
across levels — not per-claim local evidence, and not a general testing
methodology.

**MUST NOT** be read as mandating fine-grained TDD "within a level" — the
author did not establish that requirement, and this skill does not invent
one on her behalf. It equally **MUST NOT** be read as forbidding TDD or any
other local verification habit already in use on the project. The only
claim this skill makes about testing cadence is the one stated above:
integrated suite runs are deferred to the time-available horizon (or an
explicit request), local evidence obligations from the rest of the corpus
are not deferred at all.

## Failure modes / anti-patterns

- **MVP-shaped scoping suggestion**: proposing a quick, minimal, or
  demo-only version without being asked, especially under a deadline —
  the exact suggestion this skill exists to prevent.
- **Phase-by-technical-concern leveling**: "auth now, security later,"
  "get it working then add proper persistence" — security or another
  load-bearing property treated as an add-on level instead of inherited
  from the first level that needs it.
- **Disposable level 1**: a first level built as a throwaway prototype that
  later levels can't extend and must instead replace wholesale.
- **Approximated-breadth under time pressure**: building thin, precarious
  versions of every planned level instead of fully building the levels time
  actually allows.
- **Skipping the per-level adversarial review**: adding a level without
  checking that it preserves the invariants of the levels before it,
  discovering the break only at final integration (or worse, after
  shipping).
- **Inferring a new TDD mandate from this skill's testing-cadence rule** —
  the specific inversion this skill's own boundary section exists to
  prevent.
- **Treating "reduce depth, not integrity" as license to cut corners** on
  the levels actually attempted, instead of cutting the number of levels
  attempted.

## Verifiable checks

- [ ] No level is defined by a technical concern (auth/security/tests) that
      should instead be a property inherited across all levels from the
      first one that needs it.
- [ ] Each completed level is independently useful and does not require a
      later level to rebuild or bypass it.
- [ ] No MVP, quick-prototype, or demo-only scope was suggested without an
      explicit request from the author.
- [ ] Under a time constraint, the response taken was fewer fully-built
      levels, not thinner versions of all planned levels.
- [ ] Each new level was adversarially reviewed for its own correctness and
      for preservation of prior levels' invariants before being considered
      done.
- [ ] No full regression/integration suite ran automatically between levels
      without an explicit request — while any per-claim local
      verification required by another skill still ran at its normal
      point, unaffected by this skill.
- [ ] The final integrated suite is described, honestly, as confirming a
      reasoned construction — not as the first check of whether the levels
      actually work together.
