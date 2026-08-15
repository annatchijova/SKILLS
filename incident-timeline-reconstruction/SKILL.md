---
name: incident-timeline-reconstruction
description: Build a defensible timeline of what happened from heterogeneous, imperfectly-clocked sources — separating recorded time from actual time, ordering from causation, and "no event" from "no coverage". Use whenever events from more than one source must be placed in sequence: incident response, outage postmortems, forensic investigations, breach reconstruction, distributed-system debugging across services, audit trails, or a "what happened when" question. Trigger on "build a timeline", "reconstruct what happened", "correlate these logs", "which came first", "the logs disagree", "clock skew", "root cause of the outage", "when did the attacker get in", or a paste of logs from two systems that need to be merged. Governs ordering, uncertainty, and gap discipline; the write-up itself goes to daubert-defensible-writing and the epistemic labels to claim-provenance-discipline.
---

# Incident Timeline Reconstruction

A timeline looks like a list of facts. It is mostly inference. Every row asserts
that an event happened, that it happened at a time, and — by its position — that
it happened before the row beneath it. Those are three different claims with
three different kinds of evidence, and merging logs from two machines quietly
manufactures all three at once.

The discipline here is to keep them apart: **what a source recorded** is
evidence; **when the event actually occurred** is usually an estimate; **why one
event followed another** is always an inference, and it needs a stated mechanism.

Composes with: `abductive-engineering` (rival explanations for the same
sequence), `daubert-defensible-writing` (how the write-up separates fact from
inference), `claim-provenance-discipline` (the labels must survive into the exec
summary), `tamper-evident-audit-chain` (whether the log could have been altered),
`honest-degradation` (gaps stay visible instead of being smoothed over).

---

## Part 1 — Three times, never one

For every event, distinguish:

- **Recorded time** — the string in the log. A fact about the log.
- **Actual time** — when the thing happened in the world. An estimate, with an
  error bar.
- **Sequence position** — where it sits relative to other events. Sometimes known
  far more precisely than either time (a causal chain within one process), and
  sometimes not known at all despite precise-looking timestamps.

Timestamps lie in *known, enumerable* ways. Before merging anything, ask of each
source: what does its timestamp actually mark?

| Semantics | The timestamp marks | Typical error |
|---|---|---|
| Event time | When the thing occurred | Best case — still subject to clock offset |
| Write time | When the line was flushed | Buffering, batching: seconds to minutes late |
| Ingest time | When the collector received it | Queue delay, backpressure, retries |
| Collection time | When someone ran the tool | Anything from the whole retention window |
| Derived time | Reconstructed by a tool from another field | Inherits every error above, invisibly |

Then the usual distortions: timezone recorded or assumed; local time crossing a
DST boundary (an hour that repeats or never happens); second vs millisecond
truncation; monotonic vs wall-clock sources; NTP step corrections that move a
clock *backwards* mid-log; containers inheriting the host clock; and any device
whose clock is set by a human.

---

## Part 2 — Clock domains and anchoring

Treat every source as its own **clock domain**. Do not merge two domains into one
ordered list until you have estimated the offset between them, or you will
"discover" that the response preceded the request.

**Anchor events** measure the offset: a single real-world event that two sources
both recorded and can be matched by identity, not by time — a request ID
appearing in both the load balancer and the application log; a TLS session; a
deployment with a build hash; a packet with a sequence number. The difference in
recorded times for the same identified event is the offset (plus the real latency
between the two observation points, which you should bound rather than ignore).

- With an anchor: record the offset and its direction, apply it, and state that
  the corrected times are **derived**.
- With multiple anchors over the window: check whether the offset *drifts*. A
  drifting offset means no single correction is valid across the window.
- Without an anchor: **do not interleave**. Present the sources as parallel
  tracks and reason only within each track. A parallel-track timeline that admits
  it cannot order across tracks is worth far more than a merged one that guesses.

For events within a single process, prefer causal evidence to timestamps
entirely: a request ID, a span/trace parent, a sequence number, a lock acquisition
order, a monotonically increasing log index. Causal links survive clock problems;
timestamps do not.

---

## Part 3 — Ordering is not causation

Adjacency in a timeline is the most persuasive and least reliable thing a
document can do. B follows A on the page, and every reader concludes A caused B.

Before asserting causation, state the **mechanism** — the specific path by which A
produces B — and check the rivals (`abductive-engineering`):

- **Common cause**: A and B both follow from C, which is in a log you have not
  collected.
- **Reverse direction**: the recorded order is an artifact of buffering
  differences between the two sources.
- **Coincidence**: the deploy at 14:02 and the error spike at 14:03 are the
  hypothesis everyone reaches first; the error spike also happened at 14:03 last
  Tuesday, when nothing was deployed. Check the baseline before pinning it.
- **Detection lag masquerading as onset**: the alert at 03:14 is when the
  *threshold* was crossed, not when the condition began. First *observation* and
  first *occurrence* are different rows.

Mark each causal link in the timeline as `MECHANISM STATED` or `ADJACENCY ONLY`.
The second is not a failure — it is an honest row, and it tells the reader
exactly which parts of the story are load-bearing inference.

---

## Part 4 — Gaps: absence of evidence, made explicit

The most consequential rows in an incident timeline are often the ones that are
not there. Distinguish three very different silences — the same distinction
`purple-team-exercise` makes about detection, applied to history:

- **NOT COLLECTED** — the source exists but was never gathered (retention expired,
  a host was reimaged, the bucket was not in the collection scope).
- **NOT LOGGED** — the system was running but does not emit this event class at
  all. A visibility gap, and usually the most expensive finding in the postmortem.
- **NO ACTIVITY** — the source was present, healthy, and recording, and genuinely
  shows nothing in this window. Only this one supports "nothing happened", and
  only if you can show the source was alive across the interval (a heartbeat, a
  neighboring unrelated event, a rotation marker).

Never let a visual gap in a timeline imply quiet. Draw the gap and label which
kind it is. And when a log ends abruptly, treat "the logging stopped" as an event
in its own right, with its own explanation — it is frequently the most
informative row on the page.

**Bound the unknown with known-good markers.** Even when the moment of an event
is unknown, you can usually bracket it: last known good (the last observation
consistent with a healthy state) and first known bad (the first observation
inconsistent with it). "Between 02:10 and 04:35" is a real, defensible finding.
"03:22" invented to fill the row is not.

---

## Part 5 — Source integrity

A timeline is only as good as the logs' resistance to alteration. State, per
source: who could write to it, whether it is append-only, whether it is
centralized off-host, whether any integrity mechanism exists
(`tamper-evident-audit-chain`), and — in an intrusion investigation — whether the
account under investigation could edit or delete it. A host log that the attacker
had root on is evidence about what the attacker chose to leave behind.

Preserve the raw. Quote it verbatim in the timeline row, keep the original file
hashed and untouched, and do all normalization in a derived copy. A normalized
timestamp with no visible raw string cannot be re-checked when someone challenges
the offset you applied — and someone will.

---

## Output contract

```markdown
# Timeline — <incident> — reconstructed <date>

## Sources
| Source | Clock domain | Timestamp semantics | Offset (vs reference, method) | Coverage window | Integrity |
|---|---|---|---|---|---|

## Timeline
| Time (± unc.) | Domain | Event | Raw quote | Source ref | Level | Link to prior |
|---|---|---|---|---|---|---|
| 02:14:07 ±2s (corr. +4s) | app-1 | 500s begin | "upstream timeout" | app.log:88214 | RECORDED | ADJACENCY ONLY |
| ~02:14 (bracketed 02:10–02:20) | — | config propagation | — | inferred | INFERENCE | MECHANISM: cache TTL 300s |

Levels: RECORDED (in a log) · DERIVED (offset applied) · INFERENCE (reasoned) · UNKNOWN

## Gaps
| Window | Source | Kind (NOT COLLECTED / NOT LOGGED / NO ACTIVITY) | Effect on conclusions |

## Bracketed unknowns
<event → last known good → first known bad → what would tighten it>

## Rival sequences considered
<alternative ordering or causation → evidence against it → or: still open>
```

---

## Discipline checklist (before publishing a timeline)

- Does every row show its source and a raw quote, with normalization visible as derived?
- Is each source's timestamp semantics identified (event / write / ingest / collection)?
- Are clock domains separated, offsets anchored to an identified shared event, and drift checked?
- Did I merge domains I have no anchor for? (If yes: split into parallel tracks.)
- Is every causal link marked MECHANISM STATED or ADJACENCY ONLY?
- Are first-observation and first-occurrence distinct rows where they differ?
- Is every gap labeled by kind, and is "no activity" backed by proof the source was alive?
- Are unknown moments bracketed rather than invented?
- Did I state which sources the subject of the investigation could have altered?

---

## How to respond when this skill is active

- Ask what each timestamp means before merging any two sources; the answer changes the timeline more than any log line will.
- Look for an anchor event first. If there is none, present parallel tracks and say why they cannot be interleaved.
- Write uncertainty into the time column (`±`, `~`, bracketed ranges) rather than into a footnote nobody carries forward.
- Distinguish first observed from first occurred every time an alert appears in the timeline.
- Label gaps by kind, and treat "the logs stop here" as an event needing an explanation.
- State a mechanism, or state that you only have adjacency. Never let position on the page do the arguing.
- Hand the write-up to `daubert-defensible-writing`, and make sure the epistemic levels survive into the summary (`claim-provenance-discipline`) — timelines are compressed for executives more aggressively than any other artifact.
