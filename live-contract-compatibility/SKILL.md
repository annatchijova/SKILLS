---
name: live-contract-compatibility
description: Change a request/response shape, RPC contract, or message schema so that vN and vN+1 producers/consumers keep working while both are simultaneously alive — not just so a future reader can parse an old artifact. Use whenever changing a field, endpoint, protobuf message, or GraphQL type during or across a rolling deploy, or when clients (especially ones you cannot force to update, like a mobile app) may run an old contract indefinitely. Trigger on "breaking change", "rolling deploy", "mixed versions in prod", "add a required field", "rename a field", "remove an endpoint", "protobuf field number", "API version". Sibling of versioned-schema-evolution — that skill asks whether a new reader can interpret an old persisted artifact; this one asks whether two live versions of a contract can coexist while both are actually running.
---

# Live Contract Compatibility

```
versioned-schema-evolution
        ↓
Can a new reader interpret an
artifact persisted by old code?
(one lifecycle: write once, read later,
 async, one version reading at a time)

live-contract-compatibility
        ↓
Can producer/consumer vN and vN+1
coexist while BOTH are live right now?
(two clocks running simultaneously,
 for a window that sometimes never closes)
```

These are different temporal shapes of the same-sounding problem
("compatibility"), and treating them as one skill hides the part that
actually causes incidents: a deploy is not an atomic cutover, it's a
*window* — sometimes minutes, sometimes (an unforced mobile client)
effectively permanent.

Composes with the library:

- **versioned-schema-evolution** — explicit sibling; don't duplicate its
  content here. If the question is "can this code read old data," go
  there. If the question is "can these two live things talk to each other
  right now," stay here.
- **decision-record-discipline** — a deprecation window is a decision with
  a revisit trigger; write it as one, with the actual traffic-evidence
  condition (below) as the trigger, not a calendar date
- **honest-degradation** — an old client encountering a value it doesn't
  recognize (a new enum member, an unfamiliar field) must degrade visibly
  (ignore-and-flag, or a defined fallback), never crash or silently
  misinterpret

---

## The central fact: a deploy is a window, not a cut

**MUST** treat any contract change as live for the entire span during
which any producer or consumer might still run the old version — not the
span until the new version is deployed. For an internal service behind a
fast, forced rolling deploy, that window might be minutes. For a public
API, a mobile app the user hasn't updated, or a partner's integration, it
can be indefinite. The design has to hold for the actual window, not the
optimistic one.

## Expand → Migrate → Contract: the only sequence that's actually safe

**MUST** sequence every breaking-shaped change as three separate,
independently-completable phases — never collapse them into one deploy:

1. **Expand.** Add the new field/endpoint/message variant *alongside* the
   old one. Nothing is removed. Both old and new consumers keep working
   unchanged, because nothing they depend on moved.
2. **Migrate.** Move producers and consumers to the new shape, one at a
   time, verified by evidence (see below) — not by assuming a deploy order
   implies completion.
3. **Contract.** Remove the old field/endpoint/message variant — only after
   Migrate's evidence gate is satisfied. This is the phase most often
   skipped or rushed, and the one this skill spends the most words on,
   because skipping stright to it is where the incidents live.

## Time is not evidence of absence

**MUST NOT** gate the Contract phase on elapsed time ("it's been three
months, surely nobody's still on the old path"). **MUST** gate it on direct
traffic evidence: a metric, a log query, or an access counter showing zero
(or a knowingly-accepted residual) usage of the old contract path, over a
window long enough to cover the slowest realistic client (a mobile app's
update adoption curve, a partner's release cycle) — not an administrative
deadline. An old mobile client that a user never updated does not expire on
a schedule set by the backend team; it expires when it's actually gone,
and the only way to know that is to look.

## Where this goes wrong even with good intentions

- **A new required field is the most common accidental break.** Old
  clients, unaware of it, keep sending requests without it. **MUST** give
  any new field added mid-window a default or treat its absence as valid —
  "required" only becomes safe to declare in the Contract phase, once
  Migrate's evidence gate confirms no live caller omits it.
- **"Renaming a field" is remove+add wearing one name.** It reads as a
  single atomic edit in a diff, which is exactly why it's where an agent
  skips the Migrate phase without noticing — the change *looks* like one
  step because the tooling shows it as one line changed, not two
  operations with a live window between them.
- **Protobuf/RPC: the field number is the real identity, not the name.**
  A `.proto` consumer compiled against an old definition resolves fields by
  number, not name. Renaming a field and reusing its old number for
  something semantically different is a silent type confusion for every
  consumer still on the old compiled definition — the wire bytes are
  identical, the meaning is not. **MUST NOT** reuse a retired field number;
  retire it permanently (`reserved` in proto3) even after the Contract
  phase completes.
- **An unhandled new enum value crashes an old consumer.** A `switch`/
  `match` with no default/else over an enum that later gains a member
  breaks every consumer compiled before that addition, the moment the
  producer starts emitting it — even though the producer's own change
  looked purely additive. **MUST** require an explicit default/unknown arm
  in any contract-facing exhaustive match.
- **Removing an endpoint "because nobody should be calling it" without
  checking.** An assumption about who calls what is not the same as an
  access log confirming it.

## Contract-driven testing: the producer doesn't get to decide alone

**SHOULD**, for contracts with more than one real consumer, verify
compatibility against each actual consumer's expectations (a contract test
per consumer, in the Pact style), not solely against the producer's own
updated test suite. The producer's tests can only confirm "the new shape
is internally consistent with itself" — they cannot confirm "every real
consumer still parses this," which is the actual Contract-phase gate.

## Failure modes / anti-patterns

- **Calendar-gated removal**: dropping an old field/endpoint on a schedule
  instead of on traffic evidence.
- **New required field with no default**, breaking every caller that
  predates it the moment the new validation ships.
- **Field rename treated as one atomic operation** instead of
  expand-then-contract with a live window between.
- **Reused protobuf field number** after retiring the field it used to
  mean.
- **Exhaustive match with no default arm** over a contract-facing enum,
  breaking on the next legitimately additive change.
- **Producer-only contract tests**: "our test suite is green" standing in
  for "every real consumer still works," when no consumer's actual
  expectations were checked.
- **Assuming a rolling deploy's internal ordering guarantees compatibility**
  — even a fast internal rollout has a real window where both versions run,
  and "it's usually fine" is not the same claim as "it's verified fine."

## Verifiable checks

- [ ] Any field/endpoint/message-variant removal is preceded by a
      completed Expand phase (new shape live and accepted alongside old)
      and a Migrate phase with recorded evidence, not just elapsed time.
- [ ] The Contract-phase gate is a stated traffic-evidence condition (a
      metric/log query showing old-path usage at zero or a named accepted
      residual), not a calendar date.
- [ ] Any new field added to a live contract has a default or is treated as
      optional until the Contract phase confirms no live caller omits it.
- [ ] No protobuf/RPC field number is reused after being retired; retired
      numbers are marked `reserved` (or the equivalent for the protocol in
      use).
- [ ] Every contract-facing exhaustive match (enum switch, discriminated
      union) has an explicit default/unknown arm.
- [ ] A field rename is implemented and reviewed as two operations (add
      new, later remove old) with a live coexistence window between them —
      not as a single edit.
- [ ] For a contract with more than one real consumer, compatibility is
      checked against each consumer's actual expectations, not only the
      producer's own test suite.
- [ ] An old client encountering an unrecognized value degrades visibly
      (flagged/ignored per a defined policy) rather than crashing or
      silently misinterpreting it.
