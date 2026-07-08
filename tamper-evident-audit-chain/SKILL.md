---
name: tamper-evident-audit-chain
description: Build and verify append-only logs that prove no entry was altered, inserted, reordered, or dropped after the fact — a hash chain where each entry seals the previous one. Use this whenever you build or review an audit trail, ledger, chain of custody, provenance record, or any append-only log that could later be challenged; whenever you need to detect tampering rather than just record events; and whenever someone says "audit log", "tamper-evident", "tamper-proof", "hash chain", "ledger", "provenance", or "prove this wasn't changed". Push to use this even when the user only says "log every X" or "keep a record of Y" and that record might one day need to be trusted.
---

# Tamper-Evident Audit Chain

A plain log answers "what did we record?". A tamper-evident log answers a harder question: "can anyone prove this record was not altered after we wrote it?". The difference is a hash chain — each entry carries the hash of the previous one and a hash of its own content, so any edit, insertion, reordering, or deletion breaks the chain at a detectable point. Getting this right is mostly about a few subtle failure modes that quietly defeat the whole purpose.

## The construction

Each entry stores `prev_hash` and its own `audit_hash`, where:

```
audit_hash = sha256( canonical(payload) + prev_hash )
```

Chaining — not just per-entry hashing — is what makes insertion and reordering detectable. A standalone per-entry hash proves an entry wasn't edited, but says nothing about whether an entry was removed or two were swapped. The `prev_hash` link is what closes that gap.

## The failure modes that defeat it

These are the ways a chain looks valid while protecting nothing. Each one is load-bearing.

**1. Hash the content, not just the identifiers.** If the payload contains only IDs or foreign keys (`memory_id`, `record_id`), the referenced rows can be edited afterward and every hash still recomputes correctly — the chain "validates" over data that changed. Carry a `content_hash` of each referenced object *inside* the hashed payload. Then editing the referenced content breaks recomputation.

**2. Capture every mutable input exactly once.** The timestamp (and anything else volatile) that goes into the hash must be the *same value* stored in the row. If you hash `now()` and separately store another `now()`, the two differ by microseconds and the chain can never be recomputed from persisted data — verification becomes structurally impossible. Rule: every field fed to the hash is a stored column, captured once.

**3. Verify two independent properties, separately.** A real verifier checks:
   - **linkage** — `entry[i].prev_hash == entry[i+1].audit_hash` for all adjacent entries. Catches reordering, insertion, and deletion.
   - **integrity** — each `audit_hash` recomputes from that entry's own stored columns. Catches in-place edits to any hashed field.
   Report them as distinct results. A chain can be linked but have a tampered field, or have intact fields but a broken link; collapsing them into one boolean hides which attack happened.

**4. Never restart the chain.** A second producer (a batch job, a consolidator, a migration) that begins a new segment with `prev_hash = genesis` silently orphans everything before it — the gap reads as a clean start, not as the break it is. A new producer must read the current last hash and continue from it. There is exactly one genesis, ever.

**5. Verify the tail before appending; warn loudly, do not launder.** If the existing chain is *already* broken and you append onto it, you bury the break: every entry after the break links correctly, so the tamper point disappears under a pile of "valid" entries. Before appending, check the linkage of the last N entries. Still append (the operation must be recorded), but surface the break loudly so it stays discoverable by a full verification — never silently chain over it.

**6. Make the hashed payload deterministic.** Canonical JSON: sorted keys, fixed separators, explicit encoding. If floats are unavoidable in the payload, round them deterministically (e.g. to 6 places) so the same logical entry always produces the same bytes. Better, keep raw floats out of the sealed payload entirely — see the companion `deterministic-core` skill for exact arithmetic and canonical serialization.

**7. The verifier should be independent of the producer.** Write verification with the standard library only and no dependency on the producing code, so confirming the chain does not require trusting the system that wrote it. A verifier that imports the producer's logic can inherit the producer's bug.

## Quick start

`scripts/audit_chain.py` is a stdlib-only, SQLite-backed implementation of all seven points: `append()` (reads the last hash, continues the chain, warns on a broken tail), `compute_hash()`, and `verify_chain()` returning `{linkage_ok, integrity_ok, issues}`. Run it directly to see a chain built, verified, tampered, and the tamper caught.

```python
from audit_chain import connect, append, verify_chain, fetch_all_desc

conn = connect("audit.db")
append(conn, op="recall", body={"q": "..."}, content_hashes=["<sha256 of each record>"])
report = verify_chain(fetch_all_desc(conn))   # {'linkage_ok': True, 'integrity_ok': True, 'issues': []}
```
