---
name: debt-closure-discipline
description: Priority determines resolution order, not permission to accumulate indefinitely — every known issue (bug, inconsistency, TODO, workaround, deferred P3) must terminate in resolved, explicitly rejected with a reason, or documented as an open unresolved constraint, never silently vanish by being written down. Use whenever triaging bugs/findings/technical debt, prioritizing a backlog, closing a task under time pressure, or reviewing whether a TODO/workaround/deferred item has actually been addressed. Trigger on "P0/P1/P2/P3", "backlog", "leave this for later", "known issue", "TODO", "technical debt", "we'll clean this up eventually", "out of scope for now". A module whose patch history has become hard to read triggers software-archaeology's replacement procedure, not a repeat of it here — see below.
---

# Debt Closure Discipline

> **Priority determines resolution order, not permission to accumulate
> indefinitely.**

P0/P1/P2/P3 (or any priority scheme) says *when* something gets worked, in
what order. It does not say that the lowest tier may sit forever as an
unaddressed, semantically-closed item just because someone wrote it down.
This skill governs the second half of that sentence, which most triage
processes leave unstated.

Composes with the library:

- **software-archaeology** — already contains the full mechanism for a
  module whose accumulated patches have made its intended semantics hard to
  read: prefer parallel-run over cutover, expand-migrate-contract over
  in-place mutation, characterization tests before changing behavior, and
  git log/blame to extract original intent. This skill does not restate
  that mechanism — it only names the trigger: when a patched module's
  history obscures its intended behavior for a reader, that's a
  software-archaeology job, not something this skill will improvise its own
  version of.
- **decision-record-discipline** — "explicitly rejected with a reason" (one
  of this skill's three terminal states) is that skill's Alternatives-
  rejected field, applied to a piece of debt instead of a design choice.
  Use that skill's structure to record the rejection; don't invent a
  second format.
- **beyond-the-fix** — that skill audits whether a *shipped* fix is actually
  complete (root cause, variant sweep, blast radius). This skill governs
  what happens to an item *before* it's fixed — the queue discipline, not
  the fix-quality audit. A fix that closes an item under this skill's
  discipline still owes `beyond-the-fix`'s scrutiny before the item is
  actually marked resolved.
- **git-discipline** — "history belongs in version control ... not in the
  active control flow" (below) leans on that skill's forward-only,
  recoverable history as the place old context actually lives.

---

## Every known issue ends in one of three states

**MUST** resolve every known issue — a bug, an inconsistency, a TODO, a
workaround, a deferred lower-priority item — to exactly one of three
terminal states, and **MUST NOT** let it exist indefinitely in none of them:

1. **Resolved.** The issue is fixed, verified, and (per `beyond-the-fix`)
   checked for whether the fix is actually complete, not just present.
2. **Explicitly rejected, with a reason.** A deliberate decision that this
   will not be addressed — recorded the way `decision-record-discipline`
   records any rejected alternative: what was considered, why it lost, and
   what would reopen the question.
3. **Documented as an open, unresolved constraint.** Time ran out, priority
   ranked it below what got done, or it depends on something not yet
   available — and it is recorded as **still open**, with enough context
   (what it is, why it matters, what would be needed to close it) that
   whoever picks it up next doesn't have to reconstruct that from scratch.

**Documented is not a fourth, easier state — it is state 3, and state 3 is
still open.** Writing an item down does not resolve it; it only makes the
open item legible instead of silent. A TODO comment, a backlog ticket, or a
"known limitation" note that nobody tracks as still-outstanding is
functionally identical to the issue having vanished — the code and the
record both look finished when neither is.

## What this is not

This is not a rule against triage, against deprioritizing genuinely
lower-value work, or against shipping with known limitations. Priority
tiers exist and are respected — P3 legitimately means "not now." What
**MUST NOT** happen is P3 (or "backlog," or "someday") functioning as a
synonym for *this stops being anyone's problem*. The distinction is whether
the item remains an open, trackable item in state 3, or silently exits
tracking altogether while still being unresolved.

## The patched-module trigger

**MUST** treat a module whose accumulated patches (compatibility shims,
workarounds, fixes-for-workarounds, special cases) have made its actually-
intended behavior hard for a reader to determine as the trigger for
`software-archaeology`'s replacement procedure — not a threshold to hit a
specific patch count against. **MUST NOT** assign an arbitrary numeric
threshold ("5 patches," "3 workarounds") for this judgment; it is a
qualitative call about whether the *current reader* can still tell what the
module is supposed to do, and that call is made by actually trying to state
the module's intended behavior in one paragraph — if that paragraph
requires reading the patch history to write, the trigger has been met.

## History belongs in version control and decision records, not in the active control flow

**MUST NOT** keep dead branches, obsolete compatibility hacks, or comments
that contradict the code's current behavior in the active codebase on the
theory that they were once necessary and might be needed for context.
`git-discipline`'s forward-only, recoverable history is where that
genealogy actually lives and can be recovered if truly needed — production
code should express the design that is *currently* in effect, not a layered
record of everything it used to be. When `software-archaeology`'s
replacement procedure completes for a patched module, the old
implementation's story belongs in the commit history and, if the decision
to replace it was non-trivial, in a `decision-record-discipline` entry —
not left inline as a comment block explaining what used to be true.

## Failure modes / anti-patterns

- **P3-as-graveyard**: a lower-priority item that stops being tracked
  entirely instead of remaining an open item in state 3.
- **"Documented" mistaken for "closed"**: a known-limitations note or a TODO
  comment treated as if writing it down discharged the obligation to
  eventually resolve or explicitly reject it.
- **Silent scope-narrowing**: an item quietly dropped from a plan with no
  rejection reason recorded, indistinguishable later from an item nobody
  ever noticed.
- **Threshold-hunting for the patched-module trigger**: waiting for an
  arbitrary patch count instead of checking whether the module's intended
  behavior can still be stated without consulting its patch history.
- **Reimplementing software-archaeology's replacement mechanism from
  scratch** inside a debt-triage process instead of composing to it.
- **Archaeological code**: dead branches, retired compatibility shims, or
  comments describing old behavior left in the active control flow instead
  of in git history or a decision record.
- **Marking an item resolved without `beyond-the-fix` scrutiny** — closing
  state 1 on the presence of a fix rather than its completeness.

## Verifiable checks

- [ ] Every known issue currently tracked resolves to exactly one of:
      resolved (with completeness checked), explicitly rejected (with a
      recorded reason), or documented as an open unresolved constraint —
      none exist outside these three states.
- [ ] No item marked "documented" or "known limitation" is treated as
      closed; each remains visibly trackable as open.
- [ ] Every explicit rejection has a recorded reason and, where relevant, a
      condition that would reopen it — not a bare "won't fix."
- [ ] A patched module's replacement decision was triggered by an actual
      attempt to state its intended behavior in one paragraph (and failing
      to, without the patch history), not by an arbitrary patch count.
- [ ] A patched-module replacement follows `software-archaeology`'s
      procedure (parallel-run/expand-migrate-contract, characterization
      tests, intent extraction from history) rather than an improvised
      variant.
- [ ] No dead branch, obsolete compatibility hack, or behavior-contradicting
      comment remains in the active codebase after a replacement completes
      — that history lives in git and, where the decision was non-trivial,
      in a decision record.
- [ ] An item marked resolved has been checked against `beyond-the-fix`,
      not just marked done because a fix exists.
