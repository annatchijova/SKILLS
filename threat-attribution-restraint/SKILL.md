---
name: threat-attribution-restraint
description: Resist the pull to name an actor — attribution is the most overinterpreted act in security, and every signal that points at APT-X (shared hash, reused C2, a Cyrillic string, a compile timezone) is evidence of contact between datasets, not identity of hands, and most of it is cheap to plant. Use whenever an investigation starts reaching for a name: "this looks like APT29 / Lazarus / a Russian group", "same actor as last time", "the TTPs match", "shared infrastructure", "attribute this campaign", "who did this", "the malware overlaps with", "false flag", or a report that needs an actor in the executive summary. Also use when reviewing someone else's attribution claim before it drives an indictment, a sanction, a hack-back, or a headline. Sibling of daubert-defensible-writing (the claim gets cross-examined) and red-team-auditing (certainty is earned, not asserted); applies analysis of competing hypotheses to the actor question. It does not do the malware analysis itself (untrusted-sample-handling) and never upgrades "our datasets touched" into "we know who".
---

# Threat Attribution Restraint

Attribution is where good investigators lose their discipline, because naming an
actor is the one output that makes a report feel finished. "Unknown actor" reads as
failure; "assessed with high confidence to be APT-Whatever" reads as expertise. That
asymmetry is exactly the narrative pressure that produces confidently wrong
attribution — and attribution, unlike most findings, gets used to indict people,
sanction states, and authorize retaliation. It is the finding that most needs
restraint and most rarely gets it.

The core error is treating **overlap as identity**. A shared hash, a reused C2
domain, a common mutex, a PDB path, a code-reuse match, a TTP similarity, a
victimology pattern, a compile-time timezone, a language artifact — each is evidence
that two datasets *touched*. Whether they touched because the same hands made both,
or because one actor copied another, or bought the same commodity tool, or
*deliberately planted the overlap to be found*, is the entire question, and the
overlap alone cannot answer it.

The through-line of this skill: **a threat actor who reads your last report knows
exactly which artifacts you attribute on, and can plant every one of them.** False
flags are cheap (Olympic Destroyer wore four different actors' clothes). So the test
of an attribution is not "does the evidence point at X" — planted evidence points
beautifully — but "would this survive the actor actively trying to mislead me."

Composes with the library:

- **abductive-engineering** — attribution is analysis of competing hypotheses; the false-flag hypothesis is a mandatory competitor, not an afterthought
- **red-team-auditing** — "high confidence APT-X" is a CONFIRMED claim; earn it by induction or downgrade it
- **daubert-defensible-writing** — an attribution that drives sanctions gets cross-examined; write it to survive that
- **claim-provenance-discipline** — attribution confidence must travel; "linked to X" in a summary loses the "low confidence, single planted artifact" that birthed it
- **untrusted-sample-handling** — supplies the technical overlaps; shared code is a lead, never a verdict
- **incident-timeline-reconstruction** — the campaign's shape, not one sample, is the stronger (still forgeable) signal
- **honest-degradation** — an unattributed cluster is a valid, often-correct output

---

## Step 0 — Firstness: inventory exactly what overlaps, and nothing more

Before any name, list the concrete overlaps as pure observation, each with the
*artifact*, not the interpretation:

- SHA-256 `a3f…` present in this sample and in the 2023 campaign.
- C2 domain resolves to an IP in the same /24 as prior infrastructure.
- Malleable C2 profile is byte-identical to a public Cobalt Strike default.
- PDB path contains a username; string table contains non-English text.
- ATT&CK technique set overlaps at T1055, T1027, T1105.

Do not write "APT29 uses this technique" yet. Write "T1105 is present." The moment you
attach an actor name to an observation you have contaminated Firstness with your
conclusion.

---

## Step 1 — Rank each overlap by forgeability and base rate (Secondness)

An overlap is only evidence against a **baseline of how common and how plantable it
is**. Two independent axes, and most "strong" attribution collapses on one of them:

**Forgeability — how cheaply could an adversary plant this to frame someone?**

- *Trivially planted:* strings, language/keyboard artifacts, compile timezones,
  filenames, mutexes, user-agent strings, a hardcoded "we are APT-X" taunt. Near-zero
  attribution weight; their presence is as consistent with a frame as with the truth.
- *Moderately hard:* infrastructure reuse, TLS cert reuse, shared commodity tooling —
  forgeable by anyone who watched the prior campaign, which includes every vendor who
  published on it.
- *Harder (never impossible):* deep non-public code reuse, a private builder's
  idiosyncratic bug, operational-habit patterns across many intrusions, opsec slips.
  These carry weight *only* to the extent they are non-public and expensive to mimic.

**Base rate — how common is this artifact across unrelated actors?**

- A Cobalt Strike default, a public RAT, a commodity loader, a shared exploit, a
  widely-leaked builder: shared by dozens of unrelated groups. Overlap here is
  evidence of a shared *market*, not shared hands. Adjust every "match" by how many
  other groups also match.

A signal that is both trivially forgeable and high base-rate (a Russian-language
string in a commodity RAT) is not weak evidence — it is *no* evidence of identity, and
treating it as weak evidence is how the aggregate "picture" gets built out of noise.

---

## Step 2 — Build the false-flag hypothesis as a first-class competitor

Mandatory, always, before any attribution above "unattributed cluster." Assume an
adversary wanted you to reach the name you are about to reach, and build the strongest
version of that story:

- Which of the overlaps in Step 0 would a competent actor plant to impersonate the
  group you are about to name? (Usually: all the cheap ones — which are usually the
  ones the attribution rests on.)
- Is there a *residue* the frame cannot explain? A frame is built from public
  knowledge of the imitated group; a true match may include non-public artifacts the
  imitator could not have known to plant. That residue — and only that residue — is
  what distinguishes real attribution from a successful frame.
- Cui bono is a motive, not evidence, and motive is itself plantable (the obvious
  beneficiary is the easiest actor to frame). Do not let "who benefits" close the case.

If the false-flag story explains every overlap you have, your attribution is
*underdetermined*: it is one of at least two actors and you cannot yet say which. That
is a finding. Write it.

---

## Step 3 — Cluster first, name last

Do not jump from artifacts to a named, storied APT. Move up the ladder one rung at a
time, and stop at the highest rung the evidence actually supports:

1. **Activity cluster** — "these intrusions share enough non-trivial artifacts to be
   tracked together." Give it an internal, un-storied label (an `UNC####`-style
   handle). This commits to *co-occurrence*, not to identity, and it is correct far
   more often than a name.
2. **Assessed actor** — a named group, *with a confidence tier and the specific
   evidence that lifts it above the cluster*. This rung requires surviving Step 2.
3. **Sponsor / nationality** — the highest rung and the one with the lowest evidence
   and the highest consequence. Almost never supported by intrusion artifacts alone;
   usually requires intelligence you do not have in the malware.

Most technical investigations top out at rung 1, and rung 1 is a legitimate,
useful, honest deliverable. Reaching for rung 3 because the report "needs" it is the
failure this skill exists to prevent.

---

## Step 4 — Grade, and let ABSTAIN be the answer

State attribution on an explicit confidence scale, never as a bare name, and tie the
tier to what would change it:

- **Unattributed cluster** — tracked, not named. The default, and often the truth.
- **Low confidence** — overlaps exist but are forgeable / high-base-rate / survive the
  false-flag story as one of several actors. Name the group *and* the competitor.
- **Moderate** — non-public residue the frame cannot explain, corroborated across
  independent intrusions, not just one sample.
- **High** — the above plus evidence no imitator plausibly had access to; and even
  here, write the sentence that would downgrade it.

**ABSTAIN — "insufficient to attribute" — is a valid verdict and frequently the
correct one.** A documented "we cluster this with the March activity; we do not
attribute it to a named actor; the overlaps are consistent with a false flag" is worth
more than a confident name that a single planted string could have produced. A known
limitation is an asset; a false attribution is a liability that can end a career or
start a conflict.

---

## The one-line test

If a single artifact an adversary could plant in an afternoon — a string, a reused
domain, a timezone — would flip your named attribution, then you attributed the
plantable surface, not the actor. Downgrade to the cluster and name what non-forgeable
residue you would need before you say a name out loud.
