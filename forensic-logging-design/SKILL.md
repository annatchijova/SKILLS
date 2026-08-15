---
name: forensic-logging-design
description: Decide what to record today so that tomorrow's reconstruction is possible — derive fields from the questions someone will have to answer under pressure, log the inputs to decisions rather than only their outcomes, correlate across services, keep the event schema a versioned interface, and make silence distinguishable from outage. Use whenever logging, telemetry, or an audit trail is designed, changed, trimmed, or found wanting: "add logging", "what should we log", "observability", "structured logs", "we couldn't tell what happened", "the logs don't say", "correlation id", "trace id", "log levels", "our logging bill", "sample the logs", "PII in logs", "audit trail", or a postmortem action item that says "add more logging". Also trigger when a field is renamed or removed from an event, and when someone proposes logging everything or nothing. Upstream complement of incident-timeline-reconstruction, which consumes what this skill decides to record.
---

# Forensic Logging Design

Logs are written for a reader who does not exist yet: a stranger, under time
pressure, answering a question nobody anticipated, with no access to the person
who wrote the line. Almost all logging advice optimizes for the author —
readability, levels, tidiness. This skill optimizes for that stranger.

The design move is to work **backwards from the questions**. Not "what events
happen here" but "what will someone need to prove, and does any record let them".
A log line that nobody's question maps onto is cost; a question with no line that
answers it is a visibility gap you will discover at the worst moment.

Composes with: `incident-timeline-reconstruction` (the downstream consumer),
`detection-engineering` (rules can only see what is recorded),
`secret-lifecycle-discipline` (logs are the top leak channel),
`versioned-schema-evolution` (an event schema is a persisted format),
`tamper-evident-audit-chain` (for the audit-grade subset),
`agent-trust-boundaries` (record what motivated a privileged action).

---

## Part 1 — Start from the reconstruction requirement

Before adding a field, write the questions. They are remarkably stable across
systems:

- **Who did this?** The authenticated principal, the on-behalf-of chain, the
  service account, the automation. Not just the user-visible actor.
- **What changed?** Before and after, or an identifier that makes the prior state
  recoverable.
- **Why did it fail?** The *specific* reason and the input that caused it — not
  "operation failed".
- **What did the system believe at the time?** Configuration, feature flags,
  version, the value of the thing the decision was based on.
- **Was this us or them?** Our automation, our deploy, our retry — or an outsider.
- **When, relative to what?** Ordering against events from other systems.
- **Did it happen at all?** Distinguishing "no" from "not recorded".

For each question, name the record that answers it. Where none exists, that is a
gap with a known cost — the same three-state distinction
`incident-timeline-reconstruction` and `purple-team-exercise` both insist on:
`NOT LOGGED` (no telemetry exists) is expensive to fix and must be decided now;
`NOT COLLECTED` (retention or scope) is a policy choice; `NO ACTIVITY` is a real
answer. Only the third is available to a future investigator, and only if the
source can be shown alive.

**Postmortem action items should be written as questions, not as "add logging".**
"We could not tell whether the retry came from the client or the proxy" is a
requirement. "Add more logging to the payment service" is a wish.

---

## Part 2 — Log decisions, not just events

The highest-value record in any system is not "request received" or "job
completed". It is the one that captures **a decision, its inputs, and the branch
taken**:

```
authz.decision  allowed=false  reason=missing_scope  required=invoice:read
                had=[invoice:list]  principal=svc-billing  on_behalf_of=u_8812
                policy_version=14  resource=inv_44190
```

That line answers "why" without anyone reading the code, and — crucially — it
lets a future reader **re-derive the outcome** and check whether the code was
right. An outcome without its inputs cannot be re-derived; it can only be
believed. Anywhere a system decides — authorize, score, route, price, throttle,
match, classify, retry, skip — record the inputs, the rule or version applied,
and the branch. This is the same instinct as `deterministic-core` and
`llm-out-of-the-loop`: the decision is the thing worth preserving exactly.

Log the **skips and the no-ops** too. "Nothing to do" is an event; its absence is
indistinguishable from a crashed worker, and half of all "the job silently
stopped running" investigations end there.

Log **the boundary**: what entered the system and what left it, with the shape
and identity of the payload if not its contents. Systems fail at their edges, and
the argument "our service was fine, it was their input" needs evidence on both
sides.

---

## Part 3 — Correlation is the highest-value field

A record that cannot be joined to the records around it is a fact without a
story. Every event should carry:

- **Trace / request ID**, propagated across every service, queue, retry, and
  background job the work touches. Propagation through **asynchronous hops** is
  where this usually breaks, and asynchronous hops are exactly where the hard
  investigations live.
- **Actor and delegation chain** — who, on behalf of whom, via what automation.
  For agent systems, include the **provenance of the content that motivated the
  action** (`agent-trust-boundaries`); without it you cannot answer "on whose
  instruction did this happen".
- **Tenant / account**, so an investigation can be scoped and a blast radius
  measured.
- **Build version, config version, environment, host/instance.** "Which code was
  running" is asked in every incident and answered by almost no log.
- **Idempotency key or attempt number**, so retries are distinguishable from
  duplicates (`concurrency-reasoning`).

If you can add exactly one field to an existing system, add the correlation ID.
It converts a pile of isolated records into a reconstructable narrative.

---

## Part 4 — Events are an interface; version them

Dashboards, alerts, detections, billing, and someone's saved query all depend on
your field names. A rename is a breaking API change that fails **silently**: the
query returns zero rows, the detection stops firing, and everything looks
healthy. That is precisely the `DEGRADED` state in `detection-engineering`, and it
is caused far more often by a well-meaning refactor than by an attacker.

- **Structured over free text.** A message string is a schema nobody can query,
  and every log processor that parses one is a regex waiting to break.
- **Stable names, additive change.** Add fields; deprecate loudly; never repurpose
  a name to mean something new — a field whose *meaning* changed while its name
  stayed is undetectable downstream and poisons historical analysis.
- **Version the event schema** and carry the version in the event
  (`versioned-schema-evolution`). Old records stay readable because their version
  says how to read them.
- **Know your consumers.** Before removing a field, find who queries it. If that
  is unanswerable, the field stays — and building that answer is the real fix.

---

## Part 5 — What not to log

Logging is not free, and "log everything" is a liability position dressed as
diligence:

- **Never secrets.** Logs are the number-one leak channel
  (`secret-lifecycle-discipline`). Redact at the logger, recursively, by key and
  by pattern — never at the call site — and test the claim with a canary.
- **Minimize personal data.** Log identifiers, not contents. An ID that resolves
  to a person in a system with access control beats a name in a log with none.
  Retention and deletion obligations apply to logs, which means personal data in
  logs is a compliance surface with a very long half-life.
- **Sample deliberately, and never uniformly.** Volume is a real constraint; the
  answer is a stated policy — sample high-volume success paths, keep **all**
  errors, all security-relevant decisions, all state changes. A sampler that
  drops a fraction of authorization denials has destroyed the exact evidence the
  system exists to produce.
- **Levels are routing decisions, not emotions.** Define them once: `ERROR` means
  a human must act; `WARN` means a human should look if it recurs; `INFO` is the
  reconstruction record; `DEBUG` is for the author. A codebase where `ERROR` fires
  on ordinary conditions has no `ERROR` level.

---

## Part 6 — Make silence legible, and time defensible

**Absence must be provable.** Emit a periodic heartbeat or a known-cadence event
per component, plus explicit start, stop, config-loaded (with a hash), and
rotation markers. Without them, "no events between 02:00 and 04:00" is
uninterpretable: quiet, dead, or unrecorded, and the investigation cannot tell
which. This is the record that lets a future timeline state `NO ACTIVITY` as a
finding rather than a shrug.

**Time**: record in UTC with an explicit offset and enough precision to order
events that matter; where ordering is the point, add a per-source sequence number
and use monotonic time for durations. When emission can lag the event, record
**both** the event time and the emit time — a single timestamp whose semantics
are ambiguous is the root of most timeline disputes.

**Integrity, for the subset that needs it.** Security-relevant and audit-grade
records should be shipped off-host promptly, be append-only, and — where they may
be challenged — hash-chained (`tamper-evident-audit-chain`). State plainly who can
write to and delete each log stream; a log that the subject of an investigation
can edit is evidence about what they chose to leave.

---

## Deliverable checklist

```markdown
## Logging design review

Questions to answer: who · what changed · why it failed · what the system believed ·
  us or them · ordering vs other systems · did it happen at all
For each → the record that answers it, or the gap kind (NOT LOGGED / NOT COLLECTED)
Decision records: inputs + rule/policy version + branch taken (not just outcome)
No-ops and skips logged? Boundary in/out logged?
Correlation: trace id propagated through async hops · actor + delegation chain ·
  tenant · build & config version · attempt/idempotency key
Schema: structured · stable names · additive change · versioned · consumers known
Not logged: secrets (boundary redaction + canary test) · personal data minimized ·
  retention set · sampling policy (errors and security decisions never sampled)
Levels: defined by required action, not severity feeling
Silence: heartbeat / start / stop / config-loaded(hash) / rotation markers
Time: UTC + precision · sequence numbers · event time AND emit time when they differ
Integrity: off-host, append-only, hash-chained for the audit-grade subset; who can delete
```

---

## How to respond when this skill is active

- Ask what question the log is meant to answer before proposing fields; convert "add more logging" into a list of questions.
- Push for decision records — inputs, policy version, branch — wherever the code chooses between paths.
- Add the correlation ID first when a system has none; it is the single highest-value field.
- Treat a field rename or removal as a breaking change with silent failure, and ask who queries it before agreeing.
- Refuse secrets in logs and propose boundary-level redaction with a canary test; minimize personal data to identifiers.
- When volume is the problem, propose an explicit sampling policy that never touches errors, security decisions, or state changes — rather than a uniform rate.
- Insist on heartbeats and lifecycle markers so a future investigator can tell quiet from dead.
- Record both event time and emit time wherever they can diverge, and hand the result to `incident-timeline-reconstruction`.
