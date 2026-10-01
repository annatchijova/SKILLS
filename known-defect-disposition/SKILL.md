---
name: known-defect-disposition
description: Severity controls response urgency; it does not authorize neglect. A P0/P1 earns immediate review — but P2/P3/P4 remain known defects requiring disposition, not a silent backlog, and before anything is deferred its severity must be re-tested under interaction, composition, adversarial control, and deployment context, because initial severity usually scores the finding in isolation while the real exposure is reachable only in combination. Use whenever a finding, bug, or audit result is being triaged by priority tier, whenever the phrase "not blocking current work" is used to justify not fixing something, and whenever time runs out before every finding is addressed. Trigger on "P2/P3/P4", "low severity, deferring", "not blocking, ship it", "we'll get to it later", "known issue, out of scope for now", or any triage pass that assigns a tier without asking whether that tier survives composition. Composes with debt-closure-discipline (the three terminal states this skill's gate feeds into) and assume-breach-modeling (the chaining method the escalation questions reuse). It does not lower your bar for what counts as P0 — it raises your bar for what you're allowed to call P3 without having checked.
---

# Known Defect Disposition

> **Severity controls response urgency; it does not authorize neglect.**

P0/P1 triggers immediate review and remediation. That part of every triage
scheme works fine and needs no new skill. The failure mode this skill exists
for lives one tier down: P2, P3, and P4 getting treated as *lower priority*
in a way that quietly becomes *not anyone's problem*. They are not. They are
**known defects requiring disposition** — the same obligation debt-closure-
discipline states for any known issue, applied specifically to the moment a
severity tier gets assigned and a decision gets made about what happens next.

> **A known defect cannot disappear into prioritization. It must be
> repaired, explicitly accepted, or explicitly deferred with evidence — and
> deferral requires first testing whether interactions can amplify its
> severity.**

That second clause is the part most triage processes skip, and it is the
part this skill is actually about. Initial severity is almost always scored
against the finding *in isolation* — this input, this function, this code
path. The reachable consequence is frequently not the isolated finding; it is
what the finding becomes once it is placed next to who can trigger it, what
else it touches, and what is reachable from the state it leaves behind.
Scoring the isolated finding and stopping there is not triage — it is
describing the symptom and calling it the diagnosis.

Composes with the library:

- **debt-closure-discipline** — defines the three terminal states (resolved /
  explicitly rejected / documented-as-open) every known issue must reach.
  This skill supplies the mandatory gate that must run *before* a defect is
  allowed into the "documented as open" state, and the structured record
  that state must contain when the defect is a security- or correctness-
  relevant finding rather than generic debt. Don't restate that skill's
  three-state mechanism here — compose to it.
- **assume-breach-modeling** — the escalation questions below ("who
  controls it", "what's reachable from the stuck state") are that skill's
  chaining method, run once per deferred finding instead of once per system.
- **exploitability-triage** — tells you whether an escalation path is
  theoretically describable or actually reachable in this deployment; an
  escalation hypothesis with no reachability behind it is a `PLAUSIBLE`, not
  a `CODE FACT` — label it that way.
- **claim-provenance-discipline** — every field in the escalation analysis
  (Part 3) carries its own epistemic level; don't let a guess about reachable
  consequence read as a confirmed one.
- **decision-record-discipline** — a deferral is a decision. It gets that
  skill's revisit-trigger discipline, not a bare "won't fix."
- **beyond-the-fix** / **red-team-auditing** — supply the adversarial
  posture this skill's escalation gate asks you to apply to your own
  findings before someone else applies it for you.
- **destination-driven-construction** — "insufficient time" stops work at the
  last coherent level; it does not authorize pretending the next level's
  known gaps don't exist. Same principle, applied here to defects instead of
  build phases.

---

## Part 1 — What severity tiers actually mean

A tier says *when* something gets worked and in what order. It does not say
whether the lowest tier may sit forever as a semantically-closed item just
because someone wrote it down with a "P3" next to it. Restated plainly,
because this is the entire thesis:

- **P0/P1** → immediate review and remediation. Not in dispute.
- **P2/P3/P4** → scheduled later, worked in tier order. **Still known
  defects requiring disposition.** Not a quieter queue that disposal
  obligations don't apply to.

If "not blocking current work" is the only thing written next to a tier,
nothing has actually been decided — see Part 4.

---

## Part 2 — The escalation gate: mandatory before any deferral

Before a finding is allowed to leave triage as anything other than "fixed
now," it must pass through this gate. Skipping the gate is the single most
common way a real P1 ships labeled P3.

```
Finding
   │
   ▼
Initial severity P0–Pn   (scored against the finding in isolation)
   │
   ▼
Can interaction, composition, adversarial control,
deployment context, or another known defect raise severity?
   │
   ├── YES → investigate the escalation path before deferral.
   │          Re-score. If the escalated path reaches P0/P1
   │          territory, it IS P0/P1 — relabel, don't footnote.
   │
   └── NO  → retain current classification, but retain it
              WITH the evidence that was checked, not by default.
   │
   ▼
Fix now?
 ├─ YES → fix → regression evidence → close (debt-closure-discipline
 │        state 1, and beyond-the-fix scrutiny before it counts as closed)
 └─ NO  → explicit deferral decision (Part 4) → PENDING_BUGS.md
```

**The escalation analysis is not optional ceremony for findings that "feel"
serious.** It is mandatory for every P2–P4 before deferral, because the
entire reason this skill exists is that "feels minor in isolation" is
exactly the judgment the gate is built to distrust.

### The six questions

Run these against the finding, not against your intuition about the finding.
Answer each one with evidence (a trace, a code reference, a reproduction),
not with a plausibility argument alone — an unevidenced "probably not"
is how the gate gets rubber-stamped instead of run.

1. **Who controls the value or trigger condition?** An attacker-reachable
   input and a value only your own deploy pipeline ever sets are not the
   same finding, even if the code path is identical.
2. **Can it be induced deliberately, on demand, not just hit by accident?**
   A bug that requires a one-in-a-million race is a different risk than one
   a counterparty can trigger at will by sending one crafted message.
3. **What state is left behind once it fires — and is that state stuck?**
   "Reverts cleanly" and "leaves the system in a state nothing can exit"
   are different findings wearing the same stack trace.
4. **Is value — funds, credentials, trust, authority — reachable from that
   stuck state?** This is where "overflow → revert" becomes "overflow →
   activation permanently blocked → counterparty appropriates the position
   without posting collateral." The syntactic bug and the reachable
   consequence are not the same sentence.
5. **Does an alternate path exist that avoids the stuck state**, or is this
   the only way through? A recoverable dead end is lower severity than an
   irrecoverable one even when the trigger condition is identical.
6. **Does the party who can trigger this gain an asymmetric economic or
   security benefit from doing so?** A bug that only hurts its trigger is a
   different risk posture than one that pays the trigger to pull it.

Worked shape of the pattern (generalized from the kind of finding that
motivates this skill — a numeric overflow superficially read as "DoS,
moderate"): asking who controls the overflowing value, whether they can
force it deliberately, and what is reachable from the resulting revert can
turn "integer overflow causes a revert" into "a counterparty can force the
activation step to fail permanently, and the frozen state lets them acquire
the position at the stale price with no collateral posted." The first
sentence describes a crash. The second describes a theft. Both describe the
same line of code. Only the gate tells you which one you are actually
holding.

If any question's answer pushes the reachable consequence into P0/P1
territory, **that is the severity** — not a caveat attached to the lower
number. A footnoted P0 is a mislabeled P0.

---

## Part 3 — "Not blocking current work" is not a disposition

This phrase, by itself, describes scheduling. It says nothing about the
defect's disposition under Part 4's three terminal states. It is routinely
used as if it were a decision, and it is not one — it has no reason, no
accepted impact, no revisit trigger, and no record of whether the escalation
gate ever ran.

**MUST NOT** treat "not blocking" as equivalent to any of:
reject-with-reason, documented-as-open, or fixed. It is a true statement
about sequencing that carries zero disposition content on its own, and it
must never be the only thing recorded about a deferred finding.

---

## Part 4 — The structured deferral record

A defect that is not fixed now is still required to leave triage with a
record carrying: initial severity, the escalation analysis actually run (not
"assumed clean"), the disposition, and the conditions that would reopen it.
This is `decision-record-discipline`'s revisit-trigger discipline, applied
to a defect instead of a design choice. Store it in a tracked
`PENDING_BUGS.md` (or your project's equivalent known-issues ledger) — not a
comment, not a chat message, not a verbal agreement.

```yaml
id: BUG-NNNN
title: <one line, states the defect, not the symptom>

severity_initial: P3          # scored against the finding in isolation
severity_reviewed: P3         # after the escalation gate; may differ from initial

escalation_analysis:
  adversarial_control: <who can trigger this, and how>
  composition: <what else this interacts with>
  affected_invariants: <what property breaks if this fires>
  reachable_consequence: <the worst reachable state, traced, not guessed>
  p0_p1_path_found: false     # true forces severity_reviewed up — see Part 2
  evidence: <trace / repro / code reference the above rests on>

disposition: DEFERRED         # one of: FIXED | REJECTED | DEFERRED
reason: <why not fixed now — a real constraint, not "didn't get to it">
why_not_fixed_now: <time, dependency, scope — named specifically>
known_impact: <what is actually exposed while this stays open>
accepted_exposure: <what you are explicitly choosing to tolerate, and for whom>
revisit_trigger: <observable condition that reopens this — a date,
                   a traffic threshold, a dependency shipping, not "later">
owner: <who is accountable for the revisit, not just the fix>
```

A record with `escalation_analysis` filled in but `p0_p1_path_found` never
actually evaluated — left as a default `false` nobody checked — is a record
that looks complete and is not. The field exists to be answered, not to be
inherited as a template default.

---

## Part 5 — Insufficient time is a reason not to fix; it is never a reason to erase

Running out of time, a dependency not yet available, or a lower-ranked
priority queue are all legitimate reasons a defect stays open. None of them
are a reason for the defect to stop existing in the project's record.

This is the same discipline `destination-driven-construction` applies to
build phases — when time runs out, you stop at the last coherent level, you
do not pretend the next level's requirements were never real. Applied here:
when time runs out on triage, the unresolved findings go into
`PENDING_BUGS.md` with the record in Part 4. They do not go nowhere.
"Deferred" must remain visibly, trackably open — exactly
`debt-closure-discipline`'s state 3, never read as a quieter state 4 that
exits tracking.

---

## Failure modes / anti-patterns

- **Isolated scoring without the gate.** Severity assigned against the
  finding alone, with no attempt to ask whether interaction or adversarial
  control changes the picture — the single most common way a P1 ships
  wearing a P3 label.
- **"Not blocking" used as a disposition.** See Part 3 — it is a scheduling
  statement, not a decision, and recording only this is recording nothing.
- **Escalation field present but unanswered.** A `PENDING_BUGS.md` entry
  with `escalation_analysis` keys filled with placeholders or copied
  boilerplate instead of an actual trace of reachable consequence.
- **`p0_p1_path_found: true` footnoted instead of acted on.** If the gate
  finds an escalation path into P0/P1 territory, the severity *is* P0/P1 —
  treating the finding as still-deferrable at the old tier because the path
  is "theoretical" contradicts `p0_p1_path_found` being true in the first
  place; downgrade the field, not the severity.
- **Deferral with no revisit trigger**, or one that is not observable
  ("revisit later" instead of "revisit if monthly volume exceeds X" or "revisit
  when dependency Y ships").
- **The record living somewhere untracked** — a Slack thread, a verbal
  agreement, a comment in a PR that gets squashed away — instead of in a
  file that survives the session that created it.
- **Treating time pressure as grounds to drop the finding from the record**,
  rather than grounds to leave it open and say so.

---

## Verifiable checks

- [ ] Every P2–P4 finding has a documented escalation analysis (Part 2's six
      questions, answered with evidence) before it is deferred — not scored
      in isolation and left there.
- [ ] No finding is marked deferred on the strength of "not blocking current
      work" alone; a reason, known impact, accepted exposure, and revisit
      trigger are all present.
- [ ] Any escalation analysis that found a path to P0/P1 consequence has had
      its `severity_reviewed` raised accordingly — not footnoted at the
      original tier.
- [ ] Every deferred finding exists as a structured record (Part 4) in a
      tracked file, not only in conversation, a comment, or memory.
- [ ] Every deferral record has an observable revisit trigger, not "later"
      or "someday."
- [ ] A defect dropped due to insufficient time still appears, open, in the
      project's known-issues ledger — it was never silently removed from
      the record because it didn't get fixed.
- [ ] A "fixed" disposition has been checked against `beyond-the-fix`
      before being marked resolved, consistent with `debt-closure-
      discipline`'s state 1.

---

## How to respond when this skill is active

- When a finding is tiered P2–P4, run the six escalation questions before
  accepting the tier — out loud, with evidence, not as an assumed "probably
  fine."
- If any question surfaces an adversarially-reachable path to a worse
  consequence, say so plainly and re-score — do not present the escalated
  risk as a footnote under the original number.
- Refuse to accept "not blocking current work" as a complete disposition;
  ask for the reason, the known impact, the accepted exposure, and the
  revisit trigger, and write them down.
- Push every deferred finding into a structured `PENDING_BUGS.md`-style
  record (Part 4) rather than leaving it in chat history or a verbal
  agreement.
- When time runs out before every finding has a disposition, say explicitly
  which findings remain undecided and file them as open — never let "we ran
  out of time" read as "these are resolved" or let them quietly disappear
  from the list.
