---
name: remediation-driven-reporting
description: Write the report that actually gets the class fixed — survivable in a triage queue of forty, severity scored to the demonstrated impact instead of inflated, framed so that closing your instance does not close the underlying pattern, and followed through until the patch is verified against the class and not merely against your payload. Use whenever a confirmed finding goes to whoever can fix it: a vendor security team, a bug bounty program, an internal owning team, a maintainer, or several vendors at once when one class spans products. Trigger on "write the report", "submit this", "CVSS", "what severity is this", "they marked it duplicate", "triage rejected it", "informative", "they only fixed the one endpoint", "the patch is incomplete", "who do I even send this to", or a confirmed finding sitting unreported because the writeup feels harder than the hunt. Sibling of daubert-defensible-writing, which governs how a claim is worded; this one governs what the report must contain for the fix to land.
---

# Remediation-Driven Reporting

The report is not a record of the finding. It is the instrument that causes the
fix, and it either causes the right one or it does not. That reframing decides
every choice in it: what goes first, how much detail, which severity, and what
you do after they reply.

Two failure modes dominate, and they pull in opposite directions:

> **The report dies in triage.** Too long, too impressive, impact buried,
> reproducer unminimized, severity inflated — closed as informative by someone
> with six minutes and thirty-nine reports behind yours.

> **The report succeeds and fixes nothing that matters.** They patch the exact
> input you demonstrated. The class you actually found stays live, in that
> product and in every sibling, and the file is closed on both sides.

The second is the more expensive, because it looks like a win. A finding is not
remediated when your PoC stops working; it is remediated when the invariant
holds.

Composes with the library:

- **daubert-defensible-writing** — how each claim is worded: fact vs inference,
  no overclaiming. This skill governs what the report must *contain*
- **discriminating-proof** — the reproducer and its negative control
- **assume-breach-modeling** — supplies the impact half of severity, with
  evidence instead of adjectives
- **invariant-hunting** / **parser-differential-hunting** /
  **authorization-surface-mapping** — supply the class statement and the ranked
  structural fix that the report should ask for
- **beyond-the-sink** — why the class matters more than the instance
- **finding-custody** — the sibling: everything you deliberately did *not* say,
  and what happens to the finding after the patch
- **claim-provenance-discipline** — the epistemic level of each claim must
  survive into the vendor's internal retelling

---

## Part 1 — Write for the first reader, who has six minutes

The first human to see this is triaging a queue, not admiring your work. They
are deciding one thing: *is this real, and how fast does it need to move?*
Everything that delays that answer costs you.

Order the report accordingly:

1. **One sentence of impact.** Who can do what to whom, without your consent
   model's vocabulary. "Any authenticated user of any tenant can read any other
   tenant's invoices."
2. **The reproducer.** Minimal, copy-pasteable, with the exact expected output
   and the negative control alongside it (`discriminating-proof`) so they can
   see which single change causes the break. Under five minutes to run, or it
   gets scheduled instead of executed — and scheduled means next quarter.
3. **Why it crosses a security boundary.** Name the invariant that is violated.
   This is the sentence that turns "unexpected behavior" into "vulnerability".
4. **The class** (Part 3).
5. Then, and only then, the details: environment, variations, discarded
   vectors, the analysis you are proud of.

Things that reliably get a real finding closed: a wall of text before the
repro; a PoC that was never minimized; screenshots where text would do;
"could potentially, in theory, allow"; an inflated score; and any framing that
reads as marketing for the researcher rather than a defect report.

## Part 2 — Severity is a credibility budget, and it is not refundable

Inflate once and every later report from you starts one rung lower in the
reader's mind. That penalty is invisible, permanent, and lands hardest on the
one report where you were right and urgent.

Score two numbers, separately labelled, never merged:

| | What it is | What backs it |
|---|---|---|
| **Demonstrated** | What you actually executed and observed | The reproducer in the report |
| **Plausible if chained** | Where it goes under `assume-breach-modeling` | Named edges, each labelled `CODE FACT` / `PLAUSIBLE` |

Report the demonstrated number as *the* severity. Put the escalation path
beside it as an explicitly labelled hypothesis, with the edges named. A reader
can act on "medium demonstrated, critical if the token this exposes is accepted
by the deploy API — I did not test that, here is why I believe it". Nobody can
act on "CRITICAL 9.8" attached to a proof of a 403 bypass on a static asset.

Underclaiming is also a failure, not modesty. A cross-tenant read filed as
"medium" gets a six-month SLA. If the demonstrated impact is severe, say so
plainly and let the evidence carry it — and if a scoring system's mechanics
produce a number that contradicts the plain-language impact, say that too,
rather than quietly accepting the number.

Two habits that hold the budget: state what you did **not** test, and include
the vectors you tried that failed. A report that lists its own refuted
hypotheses reads as measured, and it saves the vendor from re-testing them.

## Part 3 — Report the class, or watch them fix the instance

Triage teams close what is in front of them. That is rational behavior on their
side, and it means the class-level fix only happens if the report makes it the
obvious action.

Put these four things in every report where the finding is an instance of
something bigger:

1. **The invariant, stated as one checkable property.** Not "path traversal in
   the export endpoint" but "the path used for the read is not the path that
   was authorized". That sentence is what a fix has to satisfy.
2. **The pattern that produces it** — the code shape, so their own engineers
   can recognize it elsewhere. This is the difference between a bug report and
   a class report.
3. **Where else you have reason to believe it lives**, with the epistemic level
   attached and *no unauthorized testing behind it*. "The same helper is called
   from these four routes (`CODE FACT`, read from the public source); I did not
   test them" is enormously valuable and entirely in-scope. Grepping their
   source is not the same act as probing their production.
4. **The ranked fix**, structural first. Every hunting skill in this library
   ends with a fix ladder for exactly this moment: parse once and forward the
   parsed form; enforce in the data layer; deny by default at the router; bound
   the input at the boundary. Offer the point fix as the stopgap it is, and say
   which one closes the class.

Then ask, explicitly and in one line: *"the patch I would consider complete is
the one where <invariant> holds on all paths, not the one where my input is
rejected."* Vendors respond to a stated completion criterion far more often
than to an implied one.

**When the class spans several vendors**, the reporting order is itself a
security decision: the first patch to ship starts everyone else's clock
(`finding-custody` Part 2). Prefer reporting the siblings before the first fix
lands, ask each vendor about their release timing, and tell each one that the
class is not unique to them — that single fact usually raises the priority and
is not information any of them can misuse.

## Part 4 — "Duplicate" means three different things

Distinguish them before responding, because the right reply differs:

- **Genuinely duplicate** — someone reported the same instance first. Nothing
  to do. Check whether *their* report carried the class; if it did not, the
  class report is still worth filing separately.
- **Known internally, unfixed** — the most common, and not a resolution. "We
  are aware" with no fix date leaves the class live. One reply is warranted:
  ask for the tracking reference and the expected fix, and record the answer
  in the custody file.
- **Misread by triage** — they matched it to something structurally different.
  Reply once, with the single discriminator that distinguishes yours from what
  they matched it to. One clarifying message with the missing fact; not an
  argument, not a re-send of the whole report.

Before submitting anything, dedup against **your own** prior reports. Repeat
instances of a class you already reported belong appended to that thread, not
filed as new findings — filing them separately reads as inflating a count and
spends the credibility budget from Part 2.

## Part 5 — The fix is the deliverable, so verify it

The report is not finished when they say "fixed".

- **Re-run the original reproducer** — plus the negative control, so a green
  result means the fix, not an unrelated change or an environment difference.
- **Test the class, not your payload.** They will very often have blocked your
  exact encoding, id, or ordering. Try the next member of the class:
  a different encoding layer, another route through the same helper, the same
  invariant on the streaming path. This step finds incomplete fixes at a
  remarkable rate, because a point fix looks identical to a class fix from the
  outside.
- **An incomplete patch is a new report**, written the same way — not a
  complaint on the old thread. It also raises the priority of the class fix
  more effectively than any argument would.
- **Record the outcome** in the custody file (`finding-custody` Part 4): what
  was fixed, what was not, which siblings remain unreported, and what reopens
  the file.

---

## Deliverable

```
## <title: the invariant violated, not the technique used>
Impact (one sentence): <who can do what to whom>
Severity: demonstrated <x> | plausible-if-chained <y> (edges labelled)

### Reproduce
<minimal steps, expected output, negative control>

### Why this is a boundary crossing
<the invariant, as one checkable property>

### The class
Pattern: <the code shape that produces it>
Believed to also exist at: <locations + epistemic level + "not tested">
Complete fix = <invariant> holds on all paths

### Proposed remediation (ranked)
1. structural  2. scoped  3. point fix / stopgap

### Not tested / refuted during this work
<the honest boundary of the finding>
```

## Anti-patterns

- Opening with the analysis and burying the impact on page two.
- Submitting an unminimized PoC and losing triage to its size.
- Inflating severity once, then spending the next two years one rung lower.
- Merging demonstrated and speculative impact into a single number.
- Describing the technique in the title instead of the violated invariant.
- Reporting the instance only, then being surprised that the instance is what
  got fixed.
- Listing suspected sibling locations you confirmed by probing production
  without authorization — the suspicion was in scope; the probe was not.
- Filing each instance of one class as a separate finding.
- Accepting "known issue" with no tracking reference and no date.
- Arguing with triage instead of sending the one discriminating fact.
- Closing the file when the vendor says fixed, without re-running anything.
- Verifying the fix with your original payload only, and certifying a point
  patch as a class fix.
