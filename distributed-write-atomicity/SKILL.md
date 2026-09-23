---
name: distributed-write-atomicity
description: Design the intermediate state, redelivery, and deduplication explicitly whenever two effects cannot share one transaction — a DB write plus an event/webhook/second-service call, a payment plus a notification, a state change plus a cache invalidation. Use whenever an operation must affect two systems that don't share a transactional authority. Trigger on "dual write", "outbox pattern", "idempotency key", "exactly-once", "duplicate event", "webhook delivery", "the payment charged twice", "publish an event after saving", "call another service after committing". Sibling of atomic-state-mutation — that skill covers multi-write atomicity inside one transactional authority; this one covers the case where no shared COMMIT exists at all.
---

# Distributed Write Atomicity

`atomic-state-mutation` answers: given one transactional authority, how do
several writes commit or roll back together? This skill answers the
question one level up, where that mechanism stops applying:

```
atomic-state-mutation
    └── one transactional authority
        DB write A + DB write B
        → COMMIT / ROLLBACK

distributed-write-atomicity
    └── distinct transactional authorities
        DB write + message/event/webhook/service B
        → no shared COMMIT exists
```

The central rule, and the reason this is a distinct discipline rather than a
harder version of the first one:

> **If two effects cannot participate in the same transaction, do not
> assert distributed atomicity. Design the intermediate state, the
> redelivery, and the deduplication explicitly — atomicity across
> independent authorities is not a stronger transaction, it's a different
> problem with a different shape of solution.**

Composes with the library:

- **atomic-state-mutation** — the outbox pattern below reduces this
  problem back into that skill's territory for the write that *can* be
  transactional; the two are sequential steps of the same design, not
  competitors
- **concurrency-reasoning** — an idempotency check that reads-then-writes
  without a unique constraint has the identical TOCTOU shape as any other
  race condition this skill's sibling covers
- **honest-degradation** — a stalled or failed relay/consumer must be
  visible (a lag metric, an alert), never silently absorbed as "eventually
  fine"
- **resource-exhaustion-review** — retry storms and thundering herd from a
  redelivery mechanism are that skill's territory; this skill designs
  *correctness* under redelivery, that one bounds its *cost*
- **forensic-logging-design** — at-least-once delivery means your own logs
  will show a delivery count greater than the business-effect count by
  design; log enough to distinguish "working as intended" from "actually
  duplicated the effect" after the fact

---

## The dual-write problem, precisely

Two independent commits are never atomic without a shared resource. A crash
between them — after the DB commit, before the event publish; or the
reverse — leaves exactly one side done and the other not, every time, given
enough attempts. There is no ordering of "write DB then publish" vs.
"publish then write DB" that removes this: it only changes which side is
missing when the crash lands.

- **Write-then-publish** (classic dual write): the DB commits, the process
  crashes or the publish call fails, the event never goes out — a silent,
  invisible loss with no error anywhere, because the DB write itself
  succeeded.
- **Publish-then-write**: a downstream consumer sees an event describing
  state the DB never actually reached — worse, because now an external
  system has acted on a fact that isn't true.

## The fix: transactional outbox, not a bigger transaction

Source: [AWS Prescriptive Guidance — Transactional outbox
pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

**MUST** write the "an event happened" fact as a row in the *same*
transaction as the business write, in the *same* database — this is now a
single-authority transaction, `atomic-state-mutation`'s territory, not a
cross-system one. **MUST** use a separate relay (a poller over the outbox
table, or log/CDC-tailing) to read committed outbox rows and deliver them
to the actual event system asynchronously — the relay only ever sees rows
from transactions that already committed, so it cannot publish a fact that
turned out to be false.

This does not make delivery atomic — the relay can still crash mid-delivery
and redeliver. It moves the atomicity problem to the one place it's
actually solvable (single-DB transaction) and turns the remaining
cross-system gap into an explicitly at-least-once delivery problem, which
is the next section.

## Guarantees are layered — name which one you're claiming

**MUST NOT** treat "exactly-once delivery" and "exactly-once business
effect" as the same claim, and **MUST NOT** state a universal law about
what transport can or cannot guarantee — state, per system, which of these
three distinct layers holds, and under what scope:

| Layer | What it means | Default absent a specific, demonstrated mechanism |
|---|---|---|
| Transport/delivery | Does the message arrive at least once, at most once, or exactly once at the consumer's doorstep? | At-least-once — retries on ambiguous failure (timeout, no ack) are the only safe default, because "at-most-once" silently drops on that same ambiguous failure |
| Processing | Does the consumer's handler run once per logical delivery, or once per physical delivery attempt? | Once per physical attempt, unless the consumer explicitly deduplicates |
| Business effect | Does the side effect (charge a card, decrement inventory, send an email) happen once per logical event, regardless of delivery/processing retries? | Only if the handler is made idempotent — see below; this is what actually matters to the business, and neither of the other two layers implies it |

**Some systems genuinely provide a stronger transport/processing guarantee
than bare at-least-once, under a stated scope** — this skill does not
assert that no such mechanism exists. Kafka's transactional producer +
`read_committed` consumer combination provides an effectively-exactly-once
processing guarantee for the specific case of a read-process-write pipeline
**entirely within one Kafka cluster** (verified against Confluent's own
delivery-semantics documentation: transactions are scoped to a single
cluster; a side effect that becomes externally observable outside that
cluster falls back outside the guarantee). The pattern to take from this
example, not the specific technology: a stronger-than-at-least-once claim
is only valid inside the exact scope the mechanism demonstrably covers, and
evaporates the moment an effect crosses that boundary — which, for most
"dual write" situations (an external webhook, a third-party API, a
different database), it always does.

**MUST**, before writing or trusting a claim like "this delivers
exactly-once," state: which of the three layers the claim is about, the
specific mechanism providing it, and the exact boundary where the guarantee
stops applying. A claim that doesn't survive that decomposition gets
treated as at-least-once at the business-effect layer — the safe default,
per `claim-provenance-discipline`'s treatment of an unfalsifiable-sounding
assertion: too-clean is a reason to look harder, not to relax.

## Idempotency: same key does not mean same operation

Source: [Stripe API docs — Idempotent
requests](https://docs.stripe.com/api/idempotent_requests), read directly,
not summarized from a secondary post.

**MUST** generate the idempotency key client-side and cache the *complete*
result (including a 500 or timeout) under that key for a stated,
policy-declared window (Stripe's own default is 24 hours — a value to
state explicitly for your own system, not copy blindly).

**MUST** treat "same key" and "same operation" as two separate claims. A
request arriving with a previously-used key but a **different** body
(amount, target, parameters) is not a legitimate retry — it's either a
client bug or a key-collision, and **MUST** be rejected with an explicit
error, never silently served the cached response from the original
request. Accepting a reused key with a different payload converts an
idempotency mechanism into a data-corruption vector: the caller thinks
their new request happened; what actually happened was the old one's
cached result, again. **MUST** fingerprint the request body (a hash of the
normalized payload) alongside the key and compare on every reuse.

**MUST** handle the concurrent case: two requests with the same key arriving
before the first has finished. Detect and reject/lock the second rather
than let both execute — an application-level `if (!seen(key))` check has
the identical race shape as any other check-then-act pattern:

```
if (!seen(key)) { ... }        ← observation/check — raceable, two
                                  concurrent requests can both pass it
                                  before either writes

UNIQUE(idempotency_key, ...)   ← enforcement — the database, not the
                                  application, decides who wins
```

**MUST** enforce idempotency with a unique constraint at the data layer, not
an application-level lookup — this is `invariant-hunting`'s "control
existence ≠ invariant enforcement" applied to exactly this mechanism: a
check that observes state is not the same thing as a constraint the
database refuses to violate.

## Reading your own logs under at-least-once delivery

Under a correctly-implemented outbox + idempotent-consumer design, this
sequence is the expected, correct signature — not an anomaly to chase:

```
event produced once
delivery attempted 4 times      (retries on timeout/no-ack — normal)
consumer observed 4 times       (the handler ran 4 times)
business effect committed once  (idempotency key deduplicated the other 3)
```

**MUST**, per `forensic-logging-design`, record enough to distinguish this
correct pattern from an actual duplication (a design gap that let one of
those 4 observations mutate state independently) — log the idempotency key,
the delivery attempt count, and which attempt (if any) actually produced
the committed effect. Without that, "delivery count > business-effect
count" is indistinguishable from a bug even when it's the system working
exactly as designed, and a future incident review will waste time
re-deriving what should have been a one-line log lookup.

## Failure modes / anti-patterns

- **Write-then-publish outside a transaction**: the classic dual write —
  DB commits, publish fails or the process dies, the event silently never
  goes out.
- **Publish-then-write**: a downstream system observes state the source of
  truth never actually reached.
- **Idempotency key without a fingerprint check**: a reused key with a
  different payload is served the old cached response — silent data
  corruption disguised as a successful retry.
- **Application-level idempotency check with no unique constraint**: a
  `SELECT ... WHERE key = ?` followed by an `INSERT` is a TOCTOU race under
  concurrent duplicate requests; only a DB-level unique constraint actually
  enforces it.
- **Claiming "exactly-once" without naming the layer**: asserting the
  property of the whole pipeline from a transport-level guarantee (or a
  vendor's marketing copy) without checking whether the business-effect
  layer is actually idempotent.
- **Treating a stronger in-scope guarantee as universal**: assuming that
  because one hop (e.g. Kafka-to-Kafka) is exactly-once, the whole chain is
  — when the effect crosses outside that mechanism's stated boundary (an
  external API call, a different data store), the guarantee does not
  travel with it.
- **Silent relay/consumer lag**: an outbox relay or consumer falling behind
  with no visible metric or alert — degradation that should be honest
  (`honest-degradation`) becomes an invisible and growing backlog instead.

## Verifiable checks

- [ ] Every cross-system side effect (event, webhook, second-service call)
      tied to a business write goes through an outbox row committed in the
      *same* transaction as that write — no direct publish call inside the
      business-write code path.
- [ ] A relay/consumer lag metric exists and is monitored; a stalled relay
      is visible, not silent.
- [ ] Every "exactly-once" claim in code, docs, or a PR description states
      which layer (transport/processing/business-effect) it's about and
      the specific mechanism + boundary that provides it — or is corrected
      to the honest at-least-once-plus-idempotency default.
- [ ] Idempotency keys are checked against a fingerprint of the request
      body; a reused key with a different payload is rejected, not served
      a cached response.
- [ ] Idempotency is enforced by a unique constraint at the data layer, not
      solely by an application-level existence check.
- [ ] A concurrent duplicate request (same key, arriving before the first
      completes) is handled by detection/locking, not a race between two
      handlers.
- [ ] Logs capture delivery attempt count and which attempt produced the
      committed effect, sufficient to distinguish expected at-least-once
      redelivery from an actual duplicated business effect.
