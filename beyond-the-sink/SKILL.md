---
name: beyond-the-sink
description: Look past the obvious layer of an investigation — past sink-grep keyword lists, past the exhausted question family, past the single implementation where a bug class was first found. Use whenever a hunt is anchored on dangerous-function greps (eval, subprocess, open), when the scanner's output is being treated as the map, when a confirmed bug could exist in sibling implementations or languages, when second opinions or other models hand over leads, or when the user says "no obvious vulns", "only hardening findings", "where else should we look", "replicate this", "check the other SDKs", "fresh eyes", "what are we missing". Trigger even when the user only pastes scanner output and asks what to do next. Sibling of attack-surface-triage — that skill ranks the surface; this one keeps the search from being scanner-shaped, single-family, and single-implementation.
---

# Beyond the Sink

Scanner-shaped searches find scanner-shaped bugs. If the search is a grep for
dangerous functions, every auditor before you ran the same grep — the bugs
that survive are not there. Looking further is not a vague exhortation; it is
three concrete moves: change what you search *for*, change the *question
family*, and change the *implementation*.

Composes with the library:

- **attack-surface-triage** — the inventory this skill searches beyond
- **invariant-hunting** — the question family to pivot into
- **forensic-persistence** — the discipline that decides when to pivot
- **audit-before-patch** — the verification every borrowed lead passes through

---

## Part 1 — Search for resolution, not for sinks

A dangerous function is a *place*. What matters is the *path* that reaches it
carrying attacker-influenced authority. Instead of grepping for sinks:

```
subprocess   requests   open   eval
```

grep for the machinery that decides *what gets resolved, dispatched, and
trusted*:

```
resolve  lookup  dispatch  invoke  registry
identity  principal  owner  tenant  scope  namespace
permission  authorize  allowed  capability
approve  claim  grant  token  session
```

Then build the chain and ask the only question that matters at each arrow:

```
untrusted input → identity → resource identifier → resolution
                → authorization check → dispatch → privileged sink
```

> **What authority does the system believe it has at each transition — and who
> actually granted it?**

The anomaly worth weeks of attention is the arrow where the check is *absent*
or where the identifier changed hands between check and dispatch — not an
`eval()` with a nosec comment.

## Part 2 — Change the question family before changing the target

Every hunt runs inside an implicit question family. When the family stops
producing, name it and switch:

- "Can something execute without the authority that supposedly protects it?"
  → authority family.
- "Does what was established at T0 remain true at Tn?" → invariant family
  (`invariant-hunting`).
- "Is the state the system acts on the state it thinks it has?" →
  integrity/ordering family.
- "Does this component keep the promises its own docs make?" → contract
  family — the strongest, because the spec becomes the oracle.

The contract family deserves emphasis: a detailed behavioral specification,
an ADR, even an honest docstring is a free set of executable invariants.
"Spec says A → B → C; run A → X → B → C and check whether property P survives
X" converts documentation into a falsification harness. Changelogs and fix
history are maps of where the authors already bled — dig adjacent to old
fixes, not on top of them.

## Part 3 — Replicate laterally: a root class is a template

A confirmed bug is not a finding; it is the discovery of a **class**. The
highest-ROI move in existence is asking where else the class lives — sibling
SDKs, other languages, adjacent products — because the class is understood,
the surface is production, and coordinated fixes almost never cover every
implementation.

Method, cheapest gate first:

1. **Existence gate**: does the sibling have the same structural precondition
   (e.g. a caller-named credential header, an unpickler, an approval state
   store)? Source reading only.
2. **Behavior gate**: does its default plumbing have the same property (e.g.
   follows redirects and forwards custom headers)? Verify against official
   documentation, not memory.
3. Only if both gates pass, build the PoC (`discriminating-proof`).

Falsified siblings are not wasted work — they are evidence. If every peer
implementation defaults to safe and one does not, the peers prove the safe
default is *feasible and adopted within the same product family*, which
sharpens the confirmed finding. Record falsifications with the reason ("Rust
disables redirect-following entirely; JS blocks cross-origin by default") —
that table is part of the report's strength.

## Part 4 — Borrowed eyes, verified hands

Second opinions — other models, writeups, audit notes, your own past reports —
are lead generators, not evidence.

- Treat every cited construct, line number, and behavior as a **claim**. Grep
  the live code for it before building anything on it. A lead that cites real
  constructs graduates; one that cites phantom functions dies on the spot.
- Cross-check external behavior claims against official docs (the stdlib's
  own page, the RFC, the vendor reference), never against what you remember
  the behavior to be.
- The question a borrowed lead must answer is not "is this plausible?" but
  "**does the system break a boundary it claims to enforce?**" — that framing
  survives triage; "this looks dangerous" does not.
- Your own confirmed findings are your best lead source: the pattern that
  produced one MSRC-accepted report is a proven template. Re-read old findings
  not for nostalgia but as a search grammar.

---

## Anti-patterns

- Calling a keyword grep an audit.
- Down-weighting a scanner finding without reading the sink it points at —
  the same output that yields nine false positives hides the one path that
  matters; read before you rank.
- Concluding a bug class is closed because one implementation fixed it, while
  the siblings were never checked.
- Building a PoC on a second opinion's architecture description before
  confirming the constructs exist.
- Accepting "the transport just works that way" from memory when the official
  docs are one fetch away — the docs may literally hand you the concession
  that makes the finding.
- Looking further only when stuck. Looking further is the default posture, not
  the rescue maneuver.
