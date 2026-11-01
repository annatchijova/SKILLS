---
name: invariant-hunting
description: Hunt for violations of declared or implied security invariants across transitions — a property established at T0 (validation, authority, identity, integrity, namespace) must still hold when the effect happens at Tn. Use whenever auditing or debugging anything with state transitions, redirects, resume/checkpoint flows, approval gates, retries, batching, serialization, or multi-layer pipelines. Trigger on "the check exists but", "validated once", "re-materializes", "re-injects", "authorization decay", "does the check survive", "who approved this", "TOCTOU", "resume", "redirect", "checkpoint", "stale state", "the property is established here but used there", or whenever a security decision is made in one layer and consumed in another. Sibling of red-team-auditing — that skill earns verdicts on candidates; this one generates the highest-yield candidates by naming the invariant the system believes it keeps.
---

# Invariant Hunting

The highest-severity bugs are rarely a missing check. They are a **check whose
protection does not survive the journey** — established in one layer, silently
voided in another. "There is auth", "there is cleanup", "there is an
allowlist" are observations about a point in the code. The finding lives in
what happens *after* that point.

The core question of this skill is never "is there a control?" It is:

> **A property was established at T0. What proves it still holds when the
> effect occurs at Tn?**

Composes with the library:

- **red-team-auditing** — earns or refutes the verdict on each invariant
- **concurrency-reasoning** — when the transition between T0 and Tn is an
  interleaving
- **atomic-state-mutation** — when T0-to-Tn spans multiple writes
- **agent-trust-boundaries** — when the transported property is authority over
  content an agent reads
- **versioned-schema-evolution** — when the transition is a reload of
  persisted state

---

## Part 1 — Build the invariant table before reading for bugs

Do not start from sinks. Start from the properties the system *believes* it
maintains, and tabulate their lifecycle:

| Object | Established at | Transported by | Reconstituted at | Sink |
|---|---|---|---|---|
| approval authority | human decision | message / persisted state | resume | execute |
| credential scoping | auth policy | request headers | each redirect hop | origin server |
| object identity | registry / creation | identifier | lookup | privileged use |
| session/thread namespace | request routing | state store key | resume | cross-tenant data |
| integrity of state | writer | storage + format | restore | decisions on that state |
| event ordering | creation | log / checkpoint | replay | state machine |

Sources for rows: ADRs, design docs, docstrings, changelog entries, fix
history. A document that says "these IDs are candidate keys until ownership is
verified" is not documentation — it is an invitation with coordinates.

For each row, the hunt question is identical: **where in the transport or
reconstitution can the property change while the code assumes it did not?**

## Part 2 — The violation families

Name the family before testing; each has a known shape and known hunting
grounds.

1. **Validated once, never re-validated.** The check ran on the object as it
   was; the object changed before the sink. Redirects, JS navigation,
   retries, mutation between check and use.
2. **Decision downstream, re-materialization upstream.** The security decision
   (strip the credential, deny the action) is made in one layer; a later layer
   re-injects what was removed, because nothing binds the layers. Pipelines
   where policy order is load-bearing are the habitat.
3. **Authorization decay across transitions.** Principal → session →
   checkpoint → pending request → execution: each hop is individually
   authenticated, but some hop resolves *by ID alone*, so
   `owner(action_state) == authenticated_principal` silently breaks.
4. **Semantic boundary failure.** Two layers assign different meaning to the
   same bytes: one knows this header is a secret, the other treats it as
   generic metadata. Each layer is locally correct; the composition leaks.
5. **Namespace collapse.** Scoped keys in one code path, bare keys in another
   (`scope␟thread_id` vs `thread_id`) — two contexts share one slot.
6. **Deferred resurrection.** A decision is retained while the context it was
   made in is unavailable; when the context returns, the old decision executes
   without fresh authority.
7. **Batch laundering.** One visible item carries the check; hidden items ride
   its approval. Verify the keying binds content, not just proximity in a
   batch.
8. **Cross-context substitution.** State serialized under context A is
   restored under context B (different topology, version, owner) and
   interpreted as if A — no malicious modification required.

## Part 3 — Each invariant is a binary hypothesis

For each candidate violation, before writing any proof:

- **State the invariant as one checkable equation** —
  `namespace(execution_state) == namespace(approval_state)`,
  `ApprovedCapability(T1) == ExecutedCapability(T2)` — identity of the whole
  capability, not just the name.
- **State the falsifier**: what observation kills it.
- **Verify the constructs exist in the live code first.** Function names,
  flags, and line references from second opinions, docs, or your own memory
  are claims, not facts (`audit-before-patch`). Grep them before building on
  them.
- **Read the whole enforcing function, never infer from names.** A function
  named `deserialize_type` may be hardened; a resolver named `_resolve_*` may
  fail open. The name is a hypothesis; the body is the verdict.
- **Trace every path from T0 to Tn** — sync, streaming, parallel, resume,
  error paths. An invariant enforced on four of five paths is violated.
- **Respect the author's declared boundary.** A docstring that says "not a
  security boundary; here are all the bypasses" preempts the naive bug *and
  tells you where the real boundary lives* — hunt the layer it names instead.

## Part 4 — When the invariant holds

Record it in the discard registry (`forensic-persistence`) with the evidence:
which paths were traced, which functions were read in full, what the enforcing
mechanism is. A verified invariant is assurance data — and a map of where not
to dig again. The repo that withstands a serious invariant hunt is telling you
to change family or change layer, not to stop.

---

## Anti-patterns

- Grepping for `eval`, `subprocess`, `open` and calling the result an audit
  (that is `beyond-the-sink`'s core warning — sink-grep finds scanner-shaped
  bugs).
- Testing the check exists, then assuming the protection reaches the sink.
- Treating one safe path as proof the invariant holds on all paths.
- Building on a second opinion's line references before confirming the
  constructs exist in the live code.
- Reading the docstring's "not a boundary" as a bug report instead of a map.
- Collapsing "each endpoint has auth" into "the flow is authorized" — decay
  lives *between* the endpoints.
