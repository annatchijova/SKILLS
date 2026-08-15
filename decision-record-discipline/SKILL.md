---
name: decision-record-discipline
description: Capture a technical decision while the context still exists — the forces at the time, the alternatives and why each was rejected, the assumption it rests on, its reversibility, and the condition that should reopen it. Use whenever a choice is being made that someone will later have to live with or undo: picking a library, a data model, a protocol, a boundary, a deployment topology; accepting a tradeoff or a known limitation; choosing NOT to build something; adding a workaround, a retry, a magic constant, or a guard whose reason is not obvious from the code. Trigger on "let's go with", "we decided", "why did we do it this way", "ADR", "design doc", "document this decision", "for now we'll just", "TODO: revisit", "leave it, it works", or a code review question that gets answered verbally. Governs choices; claim-provenance-discipline governs findings. It does not make the decision for you.
---

# Decision Record Discipline

Every strange piece of code was once obvious. Someone knew why the retry count is
7, why this service does not call that one directly, why the check nobody
understands must run before the write. The knowledge existed for about six weeks
and then evaporated, and what remains is a line of code that looks removable.

The cost is paid by a stranger — often you, later — who must choose between two
bad options: delete it and find out why it was there, or keep it forever out of
superstition. `software-archaeology` is the discipline for surviving that
situation; **this skill is the discipline that prevents creating it**.

A decision record is not documentation of *what* the system does — the code says
that, and says it more accurately. It records **what was true when the choice was
made, and what would make the choice wrong**.

Composes with: `software-archaeology` and `codebase-health-assessment` (fossils
are undocumented decisions), `abductive-engineering` (a decision is a hypothesis
about the future), `irreversible-action-gate` (one-way vs two-way doors),
`claim-provenance-discipline` (that one preserves findings in transit; this one
preserves choices over time), `daubert-defensible-writing` (say what you knew,
not what you hoped).

---

## Part 1 — The six fields, and why five of them get dropped

Almost every real-world "decision doc" records only the first field. The other
five are the ones with future value.

| Field | What it captures | What breaks without it |
|---|---|---|
| **Decision** | What we are doing | — (this is the one everyone writes) |
| **Forces** | The constraints that were real *at the time*: scale, deadline, team size, what the platform supported, what we did not yet know | The future reader judges a 2024 decision by 2027 conditions and concludes the author was incompetent |
| **Alternatives rejected** | Each option considered, and the specific reason it lost | The same debate is re-run every eighteen months, from scratch, by people who assume it was never had |
| **Assumption** | The belief the decision depends on ("traffic stays single-region", "the vendor keeps this API") | The assumption fails silently and nobody connects the outage to the choice that assumed it |
| **Reversibility** | One-way door or two-way door, and the cost of undoing | Cheap decisions get expensive deliberation; expensive ones get made in a standup |
| **Revisit trigger** | The observable condition that should reopen this | The decision becomes doctrine — permanent because it is old, not because it is right |

**The rejected alternatives are the load-bearing part.** They do double duty:
they stop re-litigation, and — more valuable — they tell a future reader whether
their new idea was already considered and under what conditions it lost. "We
rejected event sourcing because the team had no operational experience with it
and the deadline was eight weeks" ages into a *reopenable* decision. "We chose a
relational schema" ages into nothing.

---

## Part 2 — Reversibility sets the ceremony

Not every choice deserves a document. Match the effort to how hard it is to undo
(the same axis as `irreversible-action-gate`, applied to design):

- **Two-way door** — changed in an afternoon, contained inside one module. Decide
  fast, record in a code comment or the PR description, move on. Writing a formal
  record here is waste that trains people to ignore records.
- **One-way-ish** — a data model, a public API shape, a persisted format, a
  dependency that will spread. Undoing means a migration or a coordinated change
  across consumers. **This is where records earn their cost.**
- **One-way door** — a protocol other parties implement against, an external
  commitment, a data-retention or privacy choice, anything already shipped to
  users or stored irreversibly. Record before deciding, and treat the record as
  part of the deliverable.

A useful test: *if this turns out wrong, who finds out and how?* If the answer is
"a stranger, in an incident, in two years", write the record.

---

## Part 3 — Record the non-decisions too

The hardest knowledge to reconstruct is why something *doesn't* exist. Nothing in
the codebase points at it, so it is invisible, and it gets proposed again every
year and sometimes built.

Worth recording as first-class decisions:

- **"We deliberately did not build X"** — and why. The absence of a caching layer
  can be a considered choice or an oversight, and no reader can tell which.
- **"We accepted this limitation"** — the known-slow path, the case not handled,
  the tradeoff taken on purpose. Otherwise it will be "fixed" by someone who
  thinks they found a bug, and the reason it existed will resurface as a
  regression.
- **"We tried this and it failed"** — the approach that seemed right and did not
  work, with the evidence. This is the single most expensive knowledge in an
  organization to regenerate, and the least likely to be written down, because
  failed attempts feel like something to move past rather than a result.

---

## Part 4 — Anchor the record to the code

A record nobody finds at the moment of danger has no effect. The moment of danger
is when someone is reading the line and deciding to delete it.

- Put a short **pointer in the code**, at the surprising line: `# retry=7 and the
  400ms backoff: vendor rate limiter, see ADR-0031. Do not lower without a load
  test.` The comment explains *why*, never *what* — a comment restating the code
  rots and misleads; a comment carrying a reason cannot be derived from anywhere
  else.
- Keep the record **in the repository**, versioned alongside the code it governs.
  A decision in a wiki, a ticket, or a chat thread is a decision on a different
  clock from the code — and chat is not a record, it is a transcript of a
  conversation whose conclusion may never have been stated.
- Give it a **stable ID**, and reference that ID from the code, the PR, and any
  later record that supersedes it.
- **Supersede, never delete.** A reversed decision keeps its record and gains a
  pointer to the one replacing it — including *what changed* to justify the
  reversal. That chain is how an organization learns instead of oscillating.

---

## Part 5 — Write it at the moment, and write it honestly

**Timing.** The cheapest moment is while deciding; the context is free and
complete. A week later you will remember the conclusion and reconstruct the
reasoning — and reconstruction is where the record turns into an argument for
what you already did. A record written afterwards drops the alternatives that
were close calls and inflates the confidence of the winner.

**Honesty.** Two failure modes, both common:

- *Rationalization* — recording the justification rather than the reason. If the
  real driver was a deadline, a team preference, or an existing contract, write
  that. "We chose the boring option because the team ships it confidently" is a
  legitimate, defensible reason, and it is far more useful to a future reader than
  an invented technical narrative that does not survive scrutiny.
- *False certainty* — a record that reads as if the outcome were known. Say what
  was uncertain and how you decided under it. The reader's most useful question is
  "what did they not know", and a confident record answers it with silence.

**Record the losing argument's best point.** One line: the strongest thing the
rejected option had going for it. When conditions change, that is the sentence
that tells you the decision is worth reopening — and it is proof the alternative
was actually considered rather than dismissed.

---

## Template

```markdown
# ADR-00NN — <decision, stated as an action>
Date: <when>   Status: proposed | accepted | superseded by ADR-00MM
Reversibility: two-way | one-way-ish (cost: <migration/coordination>) | one-way

## Forces at the time
<constraints that were real then: scale, deadline, team, platform, unknowns>

## Decision
<what we are doing, specifically enough to check compliance against it>

## Alternatives rejected
- **<option>** — rejected because <specific reason>. Best argument for it: <one line>.
- **<option>** — rejected because <specific reason>. Best argument for it: <one line>.

## Assumption this rests on
<the belief that must hold. If it fails, this decision is wrong, not just dated.>

## Consequences
Accepted now: <what gets worse on purpose>
Deferred: <what we are choosing to deal with later>

## Revisit trigger
<observable condition: "if p99 write latency exceeds X", "if we pass N tenants",
"if the vendor ships Y", "review by <date> if none of the above fired">

## Anchored at
<code paths carrying a pointer comment to this ADR>
```

---

## Deliverable checklist

- Is the decision stated specifically enough that a reader could tell whether the code still complies with it?
- Are the forces described as they were *then*, including what was unknown?
- Does every rejected alternative carry a specific reason and its best argument?
- Is the load-bearing assumption named, so its failure is attributable?
- Is reversibility classified, and does the ceremony match it?
- Is there a revisit trigger that is observable, not "revisit someday"?
- Are the non-decisions recorded — what we chose not to build, what we accepted, what failed?
- Does the surprising code carry a pointer comment to the record?
- Is the record honest about the real driver, including non-technical ones?

---

## How to respond when this skill is active

- When a decision is being made, ask for the forces, the alternatives, and the revisit trigger before drafting anything — those are the fields that will be missing later.
- Classify reversibility first and scale the ceremony to it; say explicitly when a choice is a two-way door that needs no document.
- Push to record the rejected options with their best arguments. A record listing only the winner is a press release.
- Record non-decisions and accepted limitations as first-class entries; they are invisible in code and get "fixed" by strangers.
- Add the pointer comment at the surprising line, explaining why and never what.
- Write it now, at the moment of deciding. Flag reconstruction risk when asked to write a record for a decision made weeks ago, and mark which parts are recalled rather than recorded.
- Supersede rather than delete, and state what changed to justify the reversal.
- When asked "why is this here?" and nobody knows, treat that as the trigger to create the record now — with the honest answer being "unknown; preserved pending evidence" (`software-archaeology`).
