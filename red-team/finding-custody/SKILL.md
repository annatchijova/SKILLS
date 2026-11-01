---
name: finding-custody
description: Govern what happens to a confirmed finding once it is reported and you are not going to publish it — the difference between disclosing an instance, a mechanism, and a hunting method; the patch-diffing window that leaks the class whether or not you write a word; custody of the PoC and of any data you touched confirming it; and a written decision with a revisit trigger instead of an undocumented default. Use whenever a finding is confirmed and the question turns to who is told what, whenever a writeup, talk, blog post, CVE text, or conference submission is considered, whenever the same class exists in products nobody has reported yet, and whenever a working PoC needs somewhere to live. Trigger on "should we publish", "write it up", "embargo", "CVE text", "the vendor patched it", "can I blog about this", "who else has this bug", "where do I keep the PoC", or a finding going quiet with no record. It never argues for or against publishing; it makes the decision explicit, bounded, and revisitable.
---

# Finding Custody

A confirmed finding is not finished when the vendor patches it. It is an asset
you are still holding: a working technique, an understanding of a class, and
usually a PoC that runs. Most methodologies end at "reported". Everything after
that point — what you say, what you keep, what you delete, and what would make
you revisit — is governed by nothing, which is why it is governed by habit.

Two claims this skill is built on:

> **Silence has operational requirements.** Deciding not to publish is not the
> zero-cost option; it is a custody obligation with a start date and no
> automatic end.

> **The patch is a disclosure you did not write.** A fix describes the bug,
> authored by the people who understand it best, shipped publicly. Whatever the
> patch reveals is revealed on the vendor's schedule, not yours.

This skill takes no position on whether to publish. It exists so that the
decision is made once, deliberately, with a written reason and a condition that
reopens it — rather than defaulting to silence and then never looking again.

Composes with the library:

- **remediation-driven-reporting** — the sibling: how the report gets the class
  fixed; this skill governs everything you did *not* put in it
- **beyond-the-sink** — the reason class-level disclosure matters: a confirmed
  bug is a template, and lateral replication is the highest-ROI move in
  existence, for you and for everyone else
- **decision-record-discipline** — the format for a decision with a revisit
  trigger
- **claim-provenance-discipline** — the finding's epistemic level must survive
  into the private record too
- **secret-lifecycle-discipline** — a PoC is a credential-grade asset: same
  storage, retention, and rotation-of-access thinking
- **irreversible-action-gate** — publication is irreversible; so is deleting
  your only copy of the evidence

---

## Part 1 — Three things you can disclose, and they are not equivalent

Separate them before deciding anything, because "did you disclose it?" is a
question about which of these three you moved:

| Layer | What it is | Who needs it | What it costs to release |
|---|---|---|---|
| **Instance** | This endpoint, this version, this parameter | The vendor that owns it | Low after the patch; the instance is dead |
| **Mechanism** | The class — the invariant that gets violated and how | Every vendor whose product has the class | High: it is a template, and it survives the patch |
| **Method** | How you hunt for it — the question family, the search that surfaced it | Nobody, unless you choose to teach it | Highest: it generates instances nobody has found yet |

The common intuition inverts this. People carefully redact the instance and
freely describe "the interesting technique" — which hands over the two layers
with leverage and withholds the one that is already patched.

Practical consequences:

- **"It's already patched" is not the criterion.** It settles the instance
  layer only. The mechanism is exactly as live as it was.
- **The vendor needs the mechanism, not just the instance** — otherwise they
  fix your input and keep the class (see `remediation-driven-reporting`
  Part 3). Full mechanism to the party that can fix it is not the same act as
  full mechanism to everyone.
- **A class that spans multiple vendors is a coordination problem before it is
  a publication question.** The ordering matters — see Part 2.
- **Method-level teaching has a real defensive case** (it is how the next
  generation of auditors learns), but it is a separate decision from this
  finding, made deliberately and stripped of live instances.

## Part 2 — The window opens with the patch, not with your writeup

Patch diffing is a discipline of its own, and it exists because the fix is the
highest-quality description of the bug ever written. A silent patch is not a
secret patch; it is a public artifact with the answer in it.

So model the timeline honestly:

```
report → vendor fix → patch ships → [ window ] → class derivable by anyone
```

The window's length is a property of the class, not of your discretion. A
one-line input filter on a rare code path is quiet for a long time; a
restructuring of how two components exchange a parsed value is legible almost
immediately.

What follows from this:

- **Do not plan on the silence. Plan on the window.** If your protection
  strategy is "nobody will notice", it has already failed for anyone who
  watches that repo's commits.
- **When the class spans several products, the first patch starts everyone's
  clock.** Every unreported sibling is exposed from that moment, by a signal
  you triggered. That is the strongest argument for reporting the siblings
  *before* the first patch ships, and for asking the first vendor about their
  release timing.
- **Use the window deliberately.** It is the period in which siblings can be
  reported and fixed with the least ambient risk. Spending it is a choice; so
  is letting it pass.
- **The vendor's advisory text is also a disclosure decision** — one someone
  else makes about your finding. If the class matters, that is worth a sentence
  in your report: what level of detail you would prefer the advisory carry,
  and why. They may decline. Ask anyway.

## Part 3 — Custody: a PoC is a live asset

You are holding something that works. Treat it with the same discipline as a
credential (`secret-lifecycle-discipline`), because that is what it is.

Inventory, honestly — most people underestimate this list:

- the PoC itself, and every intermediate script that also works
- notes, screenshots, recordings, terminal scrollback
- **any data you touched while confirming** — even a single object read from a
  system to prove cross-tenant access
- the report draft, and every copy in mail, chat, ticketing, or a shared drive
- **every third-party service that saw it**: an AI assistant's transcript, a
  cloud session, a pastebin, a CI log, a screenshot in a support ticket,
  a translation tool. If a model helped you build the PoC, the PoC is in that
  history and its retention is not yours to set.

Then apply four rules:

1. **Separate storage.** Not in your day-to-day repo, not in the folder you
   screen-share from. Encrypted at rest, with the target's name not in the
   filename.
2. **Delete the data, keep the method.** Anything you obtained from a live
   system during confirmation is the *vendor's* data, not your evidence. Keep
   the fact that you read it and the hash if you need proof; destroy the
   content. Holding another party's data is the part of this work that is
   hardest to justify afterwards.
3. **Set a retention date at the moment you file the report**, not "later".
   Default it to fix-verified plus a fixed period.
4. **Name who else has it.** Every co-researcher, every tool, every backup.
   A PoC in three places has three compromise scenarios.

Then run the scenario in one sentence: *if my machine, repo, or cloud account
were compromised tomorrow, what would the attacker inherit?* If the answer is
working exploits for services still in production, the custody plan is the
finding's most under-tested control.

## Part 4 — Write the decision down, with a trigger that reopens it

An undocumented "I don't publish" is not a decision; it is a default that never
gets re-examined. Use `decision-record-discipline`'s shape:

```
## Finding <id> — disclosure decision
Class: <the invariant / mechanism, in one line>
Reported to: <party> on <date> | fix status: <verified / pending / declined>
Instances known: <reported> / <believed to exist, unconfirmed, where>

Decision: instance disclosed to <n> vendors; mechanism NOT published;
          method NOT published
Rationale: <why — the class is portable, siblings unreported, etc.>

Revisit if:
  - the class appears in the wild or in someone else's publication
  - the last affected vendor ships a fix (window opens; see Part 2)
  - a vendor declines to fix, or goes silent past <date>
  - an affected product is EOL'd with the class unfixed
  - <date>: unconditional re-read of this record

Custody: PoC at <location>, retention until <date>, copies held by <who>
Successor: <who inherits this if I am not here>
```

Two fields people skip and should not:

- **The unconditional re-read date.** Circumstances move. A decision that is
  correct in one context and never revisited becomes a default again.
- **The successor.** If the class dies with your laptop while it is still live
  in production, the silence stopped protecting anyone and started protecting
  nothing.

---

## Anti-patterns

- Treating "reported and patched" as the end of the finding's life.
- Assuming a silent patch keeps the mechanism private — the diff is public.
- Redacting the instance carefully while narrating the method, which is the
  layer with the most leverage.
- Withholding the mechanism from the *vendor* out of publication habit. They
  cannot fix a class they were not told about.
- Reporting one product and sitting on the siblings while the first patch ships
  and starts their clock.
- Keeping the PoC in the working repo, or in a folder that gets screen-shared.
- Retaining data obtained during confirmation because it "proves" the finding.
- Forgetting the third-party transcripts, logs, and assistant histories that
  hold a full copy of the PoC under someone else's retention policy.
- A "never publish" with no rationale, no revisit trigger, and no expiry.
- No successor, so a live class in production has exactly one person keeping it
  alive as knowledge.
