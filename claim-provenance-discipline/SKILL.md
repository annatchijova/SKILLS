---
name: claim-provenance-discipline
description: Tracking and preserving the origin of every assertion as it travels through drafts, handoffs, summaries, and documents — ensuring confidence levels, scope bounds, and evidence pointers are never stripped in transit. Use whenever findings move between people or phases: postmortems, incident briefs, audit handoffs, executive summaries, escalation chains, or review cycles. Trigger when a finding is paraphrased without citing its source, when a confidence level disappears in a rewrite, when "it was confirmed" lacks a traceable pointer, or when a summary silently inherits a parent document's assumptions. Pair with daubert-defensible-writing — which governs how individual claims are worded — this skill governs what happens to those claims when they travel.
---

# Claim Provenance Discipline

A methodology for preserving the epistemic status of a claim across its entire lifecycle — from first observation to final document. The problem it solves is not how to write a good claim (that is `daubert-defensible-writing`), but what happens to a correctly-written claim the moment it is summarized, paraphrased, handed off, or quoted.

Every claim is a sign in Peirce's sense: it has an **object** (the thing in the world it refers to), a **representamen** (the words used), and an **interpretant** (what the reader takes it to mean). Claim decay happens when the representamen is altered in transit — compressed, promoted, or stripped of its bounds — while the interpretant in the receiving document stays anchored to the original strength. The reader believes the claim is stronger than any evidence warrants; no one lied; the decay was structural.

This skill installs the structural fix: a claim carries its provenance, confidence level, scope, and falsifier as non-separable attributes, not as optional metadata that can be dropped at the summary stage.

---

## Part 1 — The Four Attributes That Must Travel

Every claim has four attributes that are part of the claim itself, not decorations around it. Stripping any one of them changes what the claim asserts:

| Attribute | What it captures | What is lost when stripped |
|---|---|---|
| **Origin** | Where the evidence came from: the log line, the test run, the cited document, the author. | The claim becomes orphaned — "it was found that" with no finder. |
| **Epistemic level** | CODE FACT / PLAUSIBLE HYPOTHESIS / CONFIRMED / FALSIFIED (per the family ladder). | A hypothesis inherits the weight of a confirmed finding. |
| **Scope bound** | The exact conditions under which the claim holds: the version, the threat model, the dataset, the environment. | The claim expands silently to cover conditions it was never tested against. |
| **Falsifier** | The evidence that would reopen or downgrade the claim. | The claim becomes unfalsifiable in transit — a protected assertion with no stated edge. |

**Transit decay pattern.** The typical sequence: a carefully bounded finding in the body becomes a summary bullet that drops the scope; the summary becomes a slide deck that drops the epistemic level; the slide becomes an action item that asserts the finding as fact. At each step, no one chose to misrepresent anything — each author compressed toward readability. The result is a claim whose current wording would never have survived the original evidence.

---

## Part 2 — The Chain of Custody Requirement

A finding label (`CONFIRMED`, `CRITICAL`, `EXPLOITABLE`) is a claim about the evidence, not about the conclusion alone. The chain of custody requirement is: **at every stage of document lifecycle, that label must be traceable to the run, log, or experiment that earned it.**

A finding with no traceable chain is a finding in name only. Treat it as PLAUSIBLE HYPOTHESIS regardless of the label it arrived with — this is not distrust of the original author, it is the correct epistemic posture when the evidence cannot be inspected.

### The three chain-of-custody checks at each handoff

When a document or finding moves from one person, phase, or format to another:

1. **Source check.** Does the receiving document cite the origin of each inherited claim? Not just "per the audit report" but specifically enough that the reader could find and read the original evidence. A pointer to a document is not a pointer to evidence; a pointer to the section, experiment, or log entry is.

2. **Level check.** Was the epistemic level of each claim preserved, not promoted? A claim that arrived as PLAUSIBLE HYPOTHESIS must leave as PLAUSIBLE HYPOTHESIS unless induction was performed in *this* document's scope. Summary ≠ confirmation.

3. **Scope check.** Was the scope bound preserved? A finding confirmed "under the threat model where the attacker controls the label field" must not become "the verdict is manipulable" without restating the precondition. The full claim is the scope-bound claim; the stripped version is a different and stronger claim with no earned evidence.

---

## Part 3 — The Promotion Antipattern and Its Variants

Promotion is the single most common form of claim decay: a claim moves from one epistemic level to a higher one without new evidence. It is usually invisible because no single step is dramatic — each author was just "summarizing for the audience."

### Variants to name and catch

**Summary promotion.** The body says "consistent with a race condition — not reproduced." The executive summary says "race condition identified." The word "identified" sounds like a CODE FACT; the evidence is a hypothesis. Correct: "race condition — PLAUSIBLE HYPOTHESIS, not yet reproduced."

**Inherited confirmation.** Document B cites Document A's CONFIRMED finding. Document A's run was against version 2.3; the current system is version 2.7. Document B now says CONFIRMED against a version it never tested. Correct: note the version gap and downgrade to PLAUSIBLE HYPOTHESIS pending verification against 2.7.

**Aggregation collapse.** A table of ten findings, mixed epistemic levels, is summarized as "ten confirmed vulnerabilities." The real count of CONFIRMED items was three; the rest were hypotheses. Correct: break down the count by epistemic level in every aggregation.

**Passive laundering.** "It was determined that the system is vulnerable." Determined by whom, from what, under what scope? Passive voice strips the agent and erases the chain of custody. Restore both: "The 2026-06-15 red-team run (commit `a3f2c`) confirmed, under the threat model where the attacker controls the input field, that the verdict degrades."

**Scope expansion by omission.** "The filter can be bypassed" — a true statement about one input class — becomes the implicit claim "the filter can be bypassed in general" when the scope is not restated. Append the scope every time the claim moves, not once at origin.

---

## Part 4 — Upstream Assumption Imports

A document that inherits conclusions from upstream sources inherits their assumptions. Those assumptions are invisible unless explicitly restated.

The structural risk: an upstream report makes Assumption X (e.g., "the acquisition pipeline is trusted"). Your document cites its conclusion without restating X. A reader who does not share X reads your conclusion as more general than it is. You are now liable for testimony you never examined.

**The import discipline:**

1. Before citing an upstream source, read its scope section and its limitations section — not just its conclusions.
2. When you cite its finding, state the assumption it depends on: "per the Phase 1 audit, *under the assumption that the acquisition pipeline is trusted*, the verdict cannot be retroactively altered."
3. If you cannot restate the upstream assumption confidently, treat the finding as PLAUSIBLE HYPOTHESIS in your document regardless of how it was labeled at the source.
4. When your own document's scope differs from the upstream document's scope, say so explicitly and explain whether the finding still applies.

The upstream author cannot be cross-examined by your reader. You are the one in the room; you carry the burden of the assumptions you import.

---

## Part 5 — Provenance Blocks

Any document producing findings that will be cited downstream should include a provenance block at the point of each major finding. This is not metadata for a database — it is a short, readable paragraph or structured header that makes the chain of custody legible to a human.

```markdown
### Finding: [ID] — [Title]
**Epistemic level:** CONFIRMED BY INDUCTION  
**Scope:** Version 2.3, commit `a3f2c91`, threat model: attacker controls input label field  
**Evidence:** script `poc/label_relabel.py`, run 2026-06-15, 12/12 reproductions  
**Falsifier:** the finding would be reopened if a schema validator enforces label provenance upstream of scoring  
**Inherited from:** none (original finding in this document)
```

When a finding is inherited:

```markdown
**Inherited from:** Phase 1 Audit §3.2, 2026-04-10  
**Upstream assumption:** acquisition pipeline is trusted  
**Verified for current scope:** NO — version 2.7 not re-tested; downgraded to PLAUSIBLE HYPOTHESIS pending rerun
```

These blocks survive compression because they are self-contained. A summarizer who reads one knows exactly what they are dropping when they drop it.

---

## Part 6 — The Summary Integrity Audit

The last step before any document ships that will be cited downstream:

1. **List every claim in the summary or executive section.**
2. For each claim, locate its origin in the body. If it has no body origin, it is an orphan — delete it or send it back for evidence.
3. Check that the epistemic level in the summary matches the level in the body. If the summary promoted it, restore the original level.
4. Check that the scope stated in the summary is no broader than the scope in the body. If it expanded, narrow it back.
5. Check that any claim marked CONFIRMED in the summary traces to an executed induction in the body — a run, an experiment, a log. "Consistent with" in the body means PLAUSIBLE HYPOTHESIS in the summary, regardless of how confident the language reads.

**The compression rule:** a summary may omit detail; it may not omit epistemic level or scope bound. Those two attributes are not detail — they are the load-bearing structure of the claim. A claim whose level or scope was omitted in summary is a different, stronger claim, and its author did not make it.

---

## Deliverable checklist

Apply at each document handoff or summary stage:

```markdown
## Claim provenance audit

### Source check
Each inherited finding → pointer to the section, experiment, or log that produced it.
Orphaned claims (no traceable origin) → flagged for deletion or re-evidence.

### Level check
Each claim in summary → level matches body. Promotions → reverted and noted.

### Scope check
Each claim in summary → scope bound preserved. Expansions → restated at original boundary.

### Falsifier check
Each CONFIRMED finding → falsifier stated at claim. Missing → added or level downgraded.

### Upstream assumption imports
Each claim inherited from another document → its upstream assumptions listed and evaluated for applicability to this document's scope.

### Honest status
Claims resting on un-run reasoning: flagged.
Findings not re-verified for current version: downgraded with scope note.
Aggregations (e.g. "N confirmed findings"): broken down by actual epistemic level.
```

---

## How to respond when this skill is active

- Treat a finding's epistemic level and scope bound as non-separable from the finding itself — summarizing without them produces a different, stronger claim that the evidence does not support.
- Before citing an upstream source, read its scope and limitations; restate the assumptions your citation depends on.
- Name the promotion antipattern explicitly when you see it: "this summary says CONFIRMED; the body says PLAUSIBLE HYPOTHESIS — restore the original level."
- Apply the summary integrity audit before any document that will be cited downstream.
- Treat "it was confirmed earlier" with no traceable pointer the same as an orphaned claim: either find the pointer or downgrade to hypothesis.
- When reviewing someone else's document, attack the chain of custody, not the author — "where does this CONFIRMED trace to?" is an evidence question, not a credibility accusation.
