---
name: hypothesis-driven-hunting
description: Run a threat hunt as a falsifiable hypothesis about adversary behavior, not a keyword sweep — state before you query what you expect to see if it is true, what would refute it, and what "found nothing" actually proves, which is almost always far less than the hunter wants to claim. Use whenever someone is threat hunting or proposing to: "let's hunt for lateral movement", "go look for signs of compromise", "hunt for persistence", "we should proactively search for X", "did we find anything", "the hunt came back clean", "run an IOC sweep". Sibling of falsifiable-testing (a hunt that cannot fail found nothing) and detection-engineering (a confirmed behavior becomes a rule); it is the abductive loop pointed at an adversary. It does not write the detection rule or adjudicate a single hit in isolation (dual-use-behavior-adjudication), and never reads "no evidence found" as "no adversary present".
---

# Hypothesis-Driven Hunting

A threat hunt is a claim about the world — "an actor performed *this behavior* in *this
environment*, and if so, *these artifacts* exist in *these logs*" — subjected to a test
that could refute it. It is not running a block of IOC searches and seeing what lights
up. The difference is the whole discipline: a hunt with no stated refutation condition
cannot fail, and a search that cannot fail has not learned anything when it returns
empty. It has produced the *feeling* of coverage, which is worse than no hunt, because
someone will now report the environment as clean.

Two failure modes, and the second is the quiet, dangerous one:

- **Grep-for-evil.** A pile of IOC queries with no hypothesis behind them. A hit is a
  "maybe" you cannot interpret (the IOC is stale, shared, or benign), and a miss means
  nothing at all — you did not define what a miss would rule out.
- **Absence-as-proof.** Treating "the hunt found no evidence" as "there is no adversary."
  A null result is bounded entirely by the data you queried, its retention, and its
  coverage. "Not present in these logs, for this window, at this fidelity" is the honest
  claim; "not present" is a lie the hunt is not entitled to tell.

Composes with the library:

- **abductive-engineering** — the hunt hypothesis is an abduction; the query is its deduced consequence; the result is the induction
- **falsifiable-testing** — a hunt with no defined refutation is a test that cannot fail; state the failing case first
- **detection-engineering** — a behavior a hunt confirms becomes a detection *requirement*, closing the loop
- **dual-use-behavior-adjudication** — a hit is a lead to adjudicate against baseline and context, never a verdict
- **claim-provenance-discipline** — the hunt's coverage and null result must travel, so "clean" carries its own caveats
- **honest-degradation** — the meaning of a null is capped by data coverage; say what the hunt could not see

---

## Step 1 — Abduce a behavior, not a keyword

Start from a hypothesis about what an adversary *did*, framed so it has observable
consequences. "Hunt for evil" is not a hypothesis; "an actor that gained a foothold on
a workstation moved laterally to a server using WMI" is. The behavior is the object;
the artifacts are the evidence you will go looking for.

Ground it in something: a threat-intel report about an actor's TTPs, a gap a
`purple-team-exercise` exposed, an anomaly from another hunt, or a "what would I do
from here" walk of `assume-breach-modeling`. A hypothesis with a reason behind it is
worth testing; a random IOC list is not.

---

## Step 2 — Deduce the observable consequence and where it must live

If the hypothesis is true, *what must exist, and in which data source*? This is the
deductive step, and it is where most hunts are quietly unfalsifiable — the hunter never
names what a true instance would actually look like, so any result can be rationalized.

- WMI lateral movement → process-creation events for `wmiprvse.exe` spawning children
  on the target, network flows on 135/DCOM, auth events for the source account. Name the
  fields, the log source, the time window.
- State the **base rate** up front: WMI is also how a hundred legitimate management
  tools operate (link `dual-use-behavior-adjudication`). If the expected artifact is
  common, the hunt is a lead-generator, not a detector, and you should know that before
  you run it.

---

## Step 3 — State the refutation condition before you query

Write down, in advance: *what result would refute the hypothesis, and what a null result
would and would not prove.* This single act converts a sweep into a test.

- "If WMI lateral movement occurred in this window, I expect ≥1 `wmiprvse` child-process
  event on the server tier. Absence in *process-creation logs that we confirm were
  ingesting for this window* refutes the specific behavior *for hosts with that logging*
  — and says nothing about hosts where the log was off."
- The precommitment matters because after you see the data, every result looks
  explicable. Deciding the failing case first is what stops you from moving the goalposts
  (the Eco's-razor discipline: a result that fits too neatly is a prompt to check
  coverage, not to declare victory).

---

## Step 4 — Run, then interpret a hit as a lead and a null as bounded

- **A hit is a lead, not a finding.** Hand it to `dual-use-behavior-adjudication`: is this
  WMI use the adversary or the patch-management server doing its job? A hunt that stops at
  "found WMI activity, escalating as compromise" reproduces the false-MALICE error.
- **A null is bounded by coverage.** Before writing "clean," establish: were those logs
  actually ingesting for the whole window? What is the retention — did the window predate
  it? What fidelity — sampled netflow, disabled command-line logging? The honest output is
  "no evidence of *this behavior* in *these sources* over *this window*," with the blind
  spots named (`honest-degradation`). A null over logs that were off is not a null; it is
  an unrun hunt.

---

## Step 5 — Bank the result regardless of outcome, and close the loop

A hunt that finds nothing still produced knowledge, but only if it is recorded so the
next person can trust or re-run it:

- **Log the hypothesis, the queries, the data coverage, and the result** — so "we hunted
  for WMI lateral movement and found none, over these sources for this window" is an
  auditable, repeatable claim, not a vibe (`claim-provenance-discipline`). Six months
  later this is the difference between "we checked" and "someone remembers checking."
- **Confirmed behavior → detection.** If the hunt found real adversary activity, the
  behavior is now a `detection-engineering` requirement: build the rule with its benign
  twin so the next occurrence is caught automatically instead of re-hunted.
- **A refined or refuted hypothesis is a result.** "The behavior was not present, but the
  hunt revealed we have zero command-line logging on the server tier" is often more
  valuable than the hunt itself — it is the next work.

---

## The one-line test

If you cannot state, before running a single query, what result would prove your
hypothesis *wrong* and what a clean result would leave *unknown*, you are not hunting —
you are sweeping, and a sweep that comes back empty has told you only that you swept.
