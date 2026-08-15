---
name: concurrency-reasoning
description: Reason about concurrent execution in terms of shared mutable state, invariants, and happens-before ordering — not in terms of "adding a lock" or "it works on my machine". Use whenever code can run more than once at a time: threads, async tasks, goroutines, workers, multiple processes or replicas, retries, webhooks, cron jobs, signal handlers, or a user who double-clicks. Trigger on "race condition", "thread-safe", "add a mutex", "deadlock", "it only fails under load", "it worked locally", "the job ran twice", "duplicate charge", "lost update", "exactly-once", "idempotent", "retry storm", "this test is flaky under parallelism", "async", or a singleton/cache/counter being initialized or mutated from more than one place. Covers ordering and visibility, critical-section scope, undeclared concurrency, idempotency, deadlock and liveness, and why a passing test proves only one interleaving. Sibling of atomic-state-mutation, which covers the database-transaction case specifically.
---

# Concurrency Reasoning

Concurrency bugs are not hard because concurrency is exotic. They are hard
because the reasoning most people apply is about **simultaneity** — "two things
happening at the same time" — and the actual subject is **ordering and
visibility**. Simultaneity is not observable, not reproducible, and not what
breaks. Ordering is.

The second reason they are hard: the failing interleaving is rare, so the test
passes, the review passes, and the defect ships with full confidence behind it.
A concurrency bug is a defect whose evidence is *statistical*, in a discipline
that treats a green test as proof.

Composes with: `atomic-state-mutation` (the same problem confined to a database
transaction), `falsifiable-testing` (a flake is often a race reporting itself),
`incident-timeline-reconstruction` (no global clock, same lesson),
`irreversible-action-gate` (check-then-act is TOCTOU),
`deterministic-core` (nondeterminism you did not choose).

---

## Part 1 — Name the shared mutable state, or stop

A data race needs exactly three ingredients:

1. **State reachable from more than one execution context**
2. **Concurrent access to it**
3. **At least one write**

Remove any one and the race is gone — and they are not equally expensive to
remove. In order of preference:

- **Eliminate the sharing.** Per-worker state, a value copied instead of
  referenced, immutability, single ownership, a message passed instead of memory
  shared. This is the only fix that cannot be got wrong later by someone who does
  not know the rule.
- **Eliminate the write.** Compute once before the concurrency starts; publish an
  immutable snapshot; recompute rather than mutate.
- **Make the operation atomic.** A compare-and-swap, an atomic counter, a single
  `UPDATE ... WHERE`, a unique constraint doing the arbitration for you.
- **Serialize with a lock.** Correct, and the most fragile, because its
  correctness lives in the discipline of every future caller rather than in the
  structure of the data.

Before any of that: **write down what is shared.** If you cannot name the shared
mutable state in a sentence, you are not yet reasoning about the bug — and a lock
added at that stage protects an unknown region against an unknown invariant.

---

## Part 2 — "I added a lock" is not an argument

Locks do not protect *variables*. They protect **invariants** — a relationship
that must hold across several reads and writes. So the questions are:

1. **What is the invariant?** ("balance never goes negative"; "the cache entry and
   its expiry timestamp are always consistent"; "at most one worker owns this
   job".)
2. **Over which region must it hold?** That region is the critical section, and
   it must span the **entire read-modify-write, including the decision** — not
   just the write.
3. **Does every path that touches the state take the same lock?** One unguarded
   accessor invalidates all the others. Locks are a whole-program property
   masquerading as a local one.

**Check-then-act is the canonical bug.** `if not exists: create`, `if
balance >= amount: debit`, `if not locked: take_lock`, `if file_missing: write`.
The condition was true when checked and false when acted on, because someone else
ran in between. Fix it by collapsing the check and the act into one atomic
operation — a conditional write, a unique constraint, a CAS, `INSERT ... ON
CONFLICT` — or by holding the invariant's lock across both. This is the same
time-of-check/time-of-use shape as in `irreversible-action-gate`: the preview and
the action must refer to the same state.

**Scope the lock to the invariant, not to the function.** Too narrow and the
invariant breaks between two guarded regions; too wide and you have serialized
your system and turned a correctness tool into a throughput bug. Both failures
look like "we have a lock".

---

## Part 3 — Happens-before, not "at the same time"

Two facts that reshape the reasoning:

**Ordering.** Without an explicit synchronization relationship, there is no
"before". Two operations are ordered only if something establishes it: a lock
acquired and released, a channel send and receive, a thread start or join, an
atomic with the right memory ordering, a database transaction boundary, a causal
dependency in a message. Absent that link, every interleaving is legal —
including the ones you did not imagine and the ones your hardware and compiler
are free to invent by reordering.

**Visibility.** A write performed without synchronization may **never become
visible** to another context. This is not a slow update; it is a permanently
stale read, and it defeats the entire genre of "I'll just check the flag".
`while not self.done: pass` can loop forever against a `done` that was set
minutes ago.

In distributed systems the same lesson arrives wearing different clothes: there
is no global clock, so timestamps from two machines cannot order two events
(exactly the clock-domain problem in `incident-timeline-reconstruction`). Order
by causality — sequence numbers, versions, fencing tokens, request IDs — never by
comparing wall clocks.

---

## Part 4 — The concurrency you never declared

Most concurrency bugs are found in code whose author never wrote a thread.
You are concurrent the moment any of these is true:

- The service runs as **more than one process, pod, or replica**. "Single-threaded
  code" stops being single-anything at the second instance.
- Anything **retries** — a client, a proxy, a queue with at-least-once delivery, a
  user reloading the page.
- A **scheduled job can overlap with itself** because the previous run has not
  finished. This is the classic silent doubler.
- **Webhooks and callbacks** arrive more than once, or out of order, by design.
- The UI lets someone **click twice**, or two people act on the same entity.
- Async/await, callbacks, signal handlers, or a garbage-collector finalizer
  interleave inside a single thread — no parallelism required, same reordering.

For each: ask what happens if this runs **twice, concurrently, with the second
starting before the first commits**. That single question finds more real defects
than any static analysis.

---

## Part 5 — Idempotency beats "exactly once"

Exactly-once *delivery* does not exist; exactly-once *effect* does, and you build
it rather than configure it:

- **Idempotency key** supplied by the caller, stored with the result. A repeat
  returns the stored result instead of doing the work again.
- **Let the database arbitrate.** A unique constraint is a race resolver that
  cannot be forgotten by the next caller — far more durable than a check.
- **Guard state transitions on the current state**: `UPDATE ... WHERE status =
  'pending'` and check the affected row count. Zero rows means someone else won,
  which is information, not an error.
- **Fencing tokens** for anything holding a "lease": a lock that can expire must
  hand out a monotonically increasing token, and the resource must reject stale
  ones. Otherwise a paused worker wakes up and writes with a lock it no longer
  holds — the failure mode that makes distributed locks dangerous rather than
  merely unreliable.

And retries have a systemic cost: synchronized retries turn a blip into an
outage. Bound them, add jitter, add a budget or circuit breaker, and never retry
a non-idempotent operation whose outcome you do not know — check first, or make
it idempotent so you do not have to.

---

## Part 6 — Deadlock and liveness

- **Lock ordering.** Deadlock needs a cycle. Impose a global order on lock
  acquisition and document it; almost all deadlocks are two code paths taking the
  same two locks in opposite orders.
- **Never hold a lock across I/O.** A network call under a mutex converts remote
  latency into local unavailability, and a remote hang into a permanent one.
- **Everything blocking gets a timeout** — locks, queues, connections, waits. A
  system without timeouts does not fail; it stops, which is harder to diagnose and
  much harder to recover.
- **Distinguish hung from slow.** They have different causes and opposite fixes.
  Instrument wait time explicitly rather than inferring it from total latency.
- **Watch for starvation and convoying**, not just deadlock: a lock that is always
  available to someone and never to *this* caller is a liveness bug with no error
  message.

---

## Part 7 — Testing what only sometimes happens

A passing concurrency test proves that **one interleaving** worked, on one
machine, once. Treat that for what it is:

- **Use the detectors.** Race detectors, thread sanitizers, and lock-order
  checkers find real defects that no test will reproduce on schedule. Run them in
  CI, not on demand.
- **Stress with variation, not repetition.** Randomize timing, injected delays,
  and ordering; run with more workers than cores; run the same operation
  concurrently N times and assert the invariant afterwards (the sum is right,
  exactly one winner, no duplicates) rather than asserting on a single call's
  return.
- **Assert invariants, not outcomes.** Under concurrency the per-call result is
  legitimately nondeterministic; the invariant is not. This is the property-based
  rung of `falsifiable-testing` applied to schedules.
- **Force the interleaving you fear.** A hook, a barrier, or an injected pause
  that makes the rare ordering deterministic turns "we think it's fixed" into a
  regression test that fails on the unfixed code — the red-first rule, applied to
  a bug that will not cooperate on its own.
- **A flake under parallelism is a finding.** It is the race reporting itself, on
  its own schedule. Retrying it deletes the report and leaves the defect
  (`falsifiable-testing`).

---

## Deliverable checklist

```markdown
## Concurrency review

Shared mutable state: <named explicitly>
Concurrency sources: threads · async · replicas · retries · overlapping cron ·
  duplicate webhooks · double-click · signal/callback   (which apply)
Invariant: <what must hold>   Critical section: <the region it must hold across>
Check-then-act: any? → collapsed into an atomic op / guarded across both steps
Ordering: what establishes happens-before between the accesses
Visibility: is every cross-context read synchronized (no unsynchronized flag polling)
Runs twice concurrently: what happens? → idempotency key / unique constraint /
  state-guarded update + affected-row check / fencing token
Locks: ordering documented · no I/O held under lock · timeouts on every wait
Tests: detector in CI · stress with randomized timing · invariant assertions ·
  the feared interleaving forced deterministically
```

---

## How to respond when this skill is active

- Ask what the shared mutable state is before discussing any fix; refuse to evaluate a lock whose invariant has not been stated.
- Prefer eliminating sharing over guarding it, and say why: a structural fix cannot be forgotten by the next caller.
- Name check-then-act on sight and offer the atomic form (conditional update, unique constraint, CAS) rather than a wider lock.
- Reframe "at the same time" as ordering and visibility; point out unsynchronized reads that may never observe a write.
- Ask "what if this runs twice, concurrently, with the second starting before the first commits" for every handler, job, and webhook.
- Treat a flaky-under-parallelism test as a defect report, and force the interleaving into a deterministic regression test before declaring the fix.
- For database-scoped versions of these problems, hand off to `atomic-state-mutation` rather than reimplementing transaction reasoning here.
