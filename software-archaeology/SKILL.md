---
name: software-archaeology
description: Disciplined modification of existing, legacy, inherited, or unfamiliar code — change without breakage, deletion without regret. Use this skill whenever the user asks to modify, refactor, clean up, simplify, modernize, migrate, or delete existing code; fix a bug in code they (or you) did not write; upgrade a dependency or framework; remove "dead" code, "unnecessary" checks, or "old" workarounds; understand why a strange piece of code exists; or work inside any codebase that predates the current session. Trigger even when the user only says "clean this up", "this looks wrong, remove it", "refactor this", "make it modern", "why is this here", "touch this carefully", or pastes unfamiliar code with a change request — especially for deletions, because deletion is the change with the most invisible consequences. Fourth member of the family — abductive-engineering (inquiry), secure-by-construction (building new), red-team-auditing (attacking finished) — this one is for changing what already exists.
---

# Software Archaeology

A methodology for *modifying* software that already exists — the most frequent activity in real engineering, and the one the rest of the family does not cover. `secure-by-construction` governs new code, `red-team-auditing` attacks finished systems, `abductive-engineering` supplies the engine (A–D–I loop, semiotic triad). This skill applies them to the ground everyone actually stands on: code written by someone else, or by yourself long enough ago to count as someone else.

It exists because a language model modifying code has three strong and dangerous default habits:

1. **It deletes what it does not understand.** A check with no obvious purpose reads as noise, and the gradient rewards "cleaner". But in a mature codebase, unexplained code is more often load-bearing than dead.
2. **It improves beyond the request.** Asked to fix one bug, it reformats, renames, restructures — destroying the discriminating experiment and multiplying the blast radius of a one-line change.
3. **It mistakes its interpretant for the object.** It reads the code, forms a fluent story about what the code does, and edits the story instead of the code. In legacy systems, the gap between those two is where regressions live.

The three prime directives that answer them:

> **The author is absent; the code is the only testimony.** Every strange construct is a sign whose intent must be *abduced*, never assumed away.
> **Understanding precedes modification; characterization precedes understanding.** Pin what the code *does* before touching what it *should do*.
> **The smallest diff that achieves the goal is the correct diff.** Every line changed beyond the request is unrequested risk.

---

## Part 1 — The Dead Author Problem

Peirce: a sign stands for an object to an interpretant. Legacy code is a sign whose author cannot be interrogated. You do not have access to the object (the intent, the constraint, the production incident that motivated line 217). You have only the sign — and your interpretant of it, which is a *hypothesis*, not a fact.

This inverts the epistemics of writing new code. When you write, you know the object and choose the sign. When you excavate, you hold the sign and must reconstruct the object. That reconstruction is abduction, and it obeys the rules from `abductive-engineering`:

**For any code whose purpose is unclear, generate rival hypotheses of intent (aim for 3), of the form "if the author faced constraint A, this code would be a matter of course":**

- It handles an input class you have not imagined (see the hostile-input table in `secure-by-construction`).
- It works around a bug in a dependency, platform, or era that may or may not still exist.
- It preserves a behavior some caller depends on (Hyrum's Law: with enough users, every observable behavior of your system will be depended on by somebody — including the bugs).
- It is a performance fix for a load pattern not visible in the code.
- It is genuinely dead — but "I don't see it called" is not "it is not called". Reflection, config-driven dispatch, serialization, cron, and other repos all call code invisibly.

**Then consult the indices before deciding.** Peirce's indexical signs — causally connected to their object — are the archaeologist's raw material, and they are cheap:

| Index | What it testifies |
|---|---|
| `git log -p` / `git blame` on the line | *When* it appeared, *with what else*, under what commit message |
| The commit message and linked issue/PR | The surprise that motivated the code — often the entire object, written down |
| Tests that touch the line | The invariant somebody once cared enough to defend |
| The date | What world the code was written for (old TLS, old API, old locale bug) |
| Grep for the symbol across *all* repos, configs, and templates | The callers you did not imagine |

A `git log` costs thirty seconds and routinely falsifies the "this is obviously dead" hypothesis. Run it before every deletion. **An unexplained line of code is a surprising fact; deleting it without abduction is explaining away the surprise.**

### Chesterton's fence, formalized

The classic rule — do not remove a fence until you know why it was put up — is exactly the A–D–I loop applied to deletion:

1. **Surprise:** this code appears to do nothing useful.
2. **Abduce:** rival hypotheses of intent (above), ranked by economy of research.
3. **Deduce:** for each, a discriminating prediction. *If* it guards an input class → a test with that input fails without it. *If* it works around dependency bug #X → the changelog shows the fix, and the minimal repro passes without the workaround. *If* it is dead → no index anywhere references it, and removing it under full test + trace shows zero behavior change.
4. **Induce:** run the cheapest discriminating experiment.
5. Only a **falsified** "it is load-bearing" hypothesis licenses deletion. "I could not think of a reason" is not falsification — it is a description of your imagination.

Confidence language must track the evidence: "this *appears* unused" (read the code) → "no index references it" (searched) → "removed under characterization tests with zero observed change" (ran it). The word **dead** is earned by induction, exactly as **CONFIRMED** is in `red-team-auditing`.

---

## Part 2 — Characterization Before Change

You cannot verify that a change preserves behavior you never measured. So before modifying code you do not fully own:

**Pin the current behavior with characterization tests.** These differ from normal tests in one honest, explicit way: they assert what the code *does*, not what it *should do* — including its bugs. This is deliberate and must be labeled, because `secure-by-construction` rightly bans "the golden output of a buggy run" *when it masquerades as a correctness test*. A characterization test does not masquerade: its name and comment say `characterizes_current_behavior_including_rounding_bug_issue_4711`. It exists so that when your refactor changes an output, you find out from a red test in seconds instead of from production in weeks — and then *decide consciously* whether the change was the point or a casualty.

Discipline:

- **Write them before the first edit.** A characterization test written after the change characterizes the change.
- **Feed them the hostile inputs**, not the demo input — reuse the probe table from `secure-by-construction` Part 1. Legacy behavior at the boundaries is precisely what nobody remembers.
- **When a characterization test goes red under your change, that is a decision point, not an obstacle.** Either the behavior change is the goal (update the test, say so out loud, note who might depend on the old behavior) or it is collateral (your change is wrong — fix the change, never the test). Silently updating a red characterization test is the archaeology version of tuning an assertion into green.
- **Where the code has no seams for testing**, introduce the *minimal* seam (extract the function, inject the dependency) as its own separate, behavior-preserving commit — verified by the characterization tests you already wrote at the coarser boundary.

### The blast radius is the threat model

`secure-by-construction` asks "who can call this?"; archaeology asks the past-tense version: **who already calls this, with what expectations, since when?** Before any signature, format, ordering, timing, or error-behavior change, enumerate: direct callers, reflective/config-driven callers, other repos, serialized data at rest written by the old code, external consumers of the output format, and humans with muscle memory. Observable behavior includes error messages, ordering of results, and timing — Hyrum's Law does not care that the docs never promised it.

---

## Part 3 — Pace: One Stratum at a Time

Archaeologists dig in layers and label everything; so do you.

- **Separate the fix from the refactor — always, physically, in different commits.** A commit that fixes a bug *and* cleans up the surroundings has destroyed the discriminating experiment: when something breaks, you cannot tell which half did it, and you cannot revert one without the other. The sequence is: characterize → minimal fix (red test goes green) → *then*, optionally, behavior-preserving refactor under the same tests. This is the anti-pattern `secure-by-construction` names "the refactor smuggled into the fix", given its full protocol.
- **No unrequested improvement.** Reformatting, renaming, "while I'm here" — each one widens the diff, obscures the review, and adds risk the user did not purchase. If you see something worth improving, *report it as a finding*; do not silently do it.
- **Every step reversible.** Prefer changes that can be reverted in one commit. For risky migrations, prefer parallel-run (old and new side by side, compare outputs on real traffic/data) over cutover, and expand–migrate–contract over in-place mutation.
- **Match the stratum's conventions.** New code inside old code follows the *local* dialect, even when you dislike it. A modern idiom in a legacy file is a false sign: it tells the reader "this part is different" when it is not. Consistency is Thirdness; breaking it locally is a regression even when the new idiom is objectively better. (Converting the whole stratum is a separate, explicit project — propose it, don't smuggle it.)
- **When the requirement is ambiguous about whether a behavior change is intended, stop and ask.** "Fix the rounding" might mean "make it correct" or "make it match the old system". Those are different diffs with different blast radii.

---

## Part 4 — Anti-Patterns to Name and Correct

- **Fence removal by aesthetics** — deleting code because it is ugly, old, or unexplained. Ugliness is Firstness; load-bearingness is Secondness. They are uncorrelated.
- **The confident narrative** — a fluent summary of what the code does, produced by reading it once, treated as ground truth. Your interpretant is a hypothesis until an index or an experiment corroborates it.
- **The refactor smuggled into the fix** — one commit, two purposes, zero discriminating power.
- **"Dead code" by grep-of-one-repo** — declared unreachable after searching one codebase, ignoring reflection, config dispatch, serialization, cron, and the other three repos.
- **Silent behavior change** — the output format "improved", the error message "clarified", the ordering "fixed" — each one an unannounced breaking change for some Hyrum-caller.
- **Characterization tests updated to green** — the test said the behavior changed; the commit made the test agree instead of deciding whether the change was intended.
- **Modernization as a virtue in itself** — rewriting working code into the current idiom with no failing test, no requirement, and no characterization. The riskiest possible change: maximal diff, zero purchased value.
- **The big-bang migration** — cutover with no parallel run, no rollback, and no comparison of outputs, justified by "the tests pass" (whose tests? characterizing what?).
- **Trusting the comment over the code** — the comment is a sign about a sign, synchronized with the object at some unknown past date. When comment and code disagree, the code is the testimony; the disagreement itself is a finding (a stale sign manufacturing false interpretants — fix it in its own commit).

---

## Deliverable format

```markdown
## Excavation report
What this code does (evidence: read / indexed / executed — per claim).
Intent hypotheses considered for anything strange, and which indices arbitrated them.

## Blast radius
Known callers and depended-on behaviors (incl. Hyrum candidates: format, ordering, timing, errors).
Assumptions I could not verify — confirm or correct these.

## Characterization
Tests pinning current behavior (hostile inputs included), written BEFORE the change.
Any pinned bugs, labeled as bugs.

## The change
Minimal diff for the stated goal. Fix and refactor in separate commits.
Behavior changes: intended ones listed explicitly; collateral ones = defects.

## Verification
Characterization suite before/after. Red tests: each one classified
(intended change — updated with justification | defect — fixed in code).

## Findings (not acted on)
Improvements observed but not requested. Dead-code candidates awaiting their experiment.
```

---

## How to respond when this skill is active

- Treat every unexplained construct as a surprising fact: abduce rival intent hypotheses, consult the indices (`git log`, issues, tests, cross-repo grep) before concluding, and let the cheapest discriminating experiment decide.
- Never delete code on the strength of "I see no reason for it". *Dead* is a label earned by induction; cap everything else at "no index references it".
- Characterize before changing: pin current behavior — bugs included, labeled — with tests written before the first edit, fed hostile inputs.
- Keep the diff minimal. Fix and refactor in separate commits. No unrequested improvements — report them as findings instead.
- State the blast radius before any observable-behavior change; assume Hyrum's Law until falsified.
- When ambiguity changes the blast radius (correct vs. compatible), ask instead of guessing.
- Confidence language tracks the evidence: "appears" (read) → "no index found" (searched) → "verified under characterization" (ran). When an experiment refutes your earlier narrative of the code, say so immediately — the corrected excavation is the deliverable, not the fluent first story.
