---
name: atomic-state-mutation
description: Make a logical operation that spans several writes to persistent state land all-or-nothing, isolated from concurrent writers, with dependents cleaned up in the same transaction. Use this whenever one conceptual operation involves multiple writes — insert-then-delete, merge, consolidate, migrate, move-across-tables, write-plus-cascade — and a crash or a concurrent writer between steps would leave the store inconsistent; and whenever you hit "database is locked", duplicated rows after a merge, or dangling references after a delete. Push to use this whenever you see more than one write that must all succeed together, even if the code currently commits them separately.
---

# Atomic State Mutation

A single logical operation that touches persistent state in several steps — insert the merged record, delete its sources, clean up their links — is only correct if it is *indivisible*. The moment those steps commit separately, two things can break it: a crash between commits (leaving the store half-mutated) and a concurrent writer slipping in between your read and your write (acting on state you were about to change). Both produce the same class of bug: duplicated data, double-counted aggregates, derived indexes built over a corrupted set — and all of it looks fine until something reads it.

## The six rules

**1. All-or-nothing in one transaction.** If "insert merged node" and "delete sources" are separate commits, a crash between them leaves *both* alive: the merged record and the originals it was supposed to replace. Now you have duplicated content, recall counts tallied twice, and any field rebuilt over the active set (an index, a PCA, an aggregate) computed over a space that contains both copies. Wrap the entire logical operation in one transaction, commit once at the end, and roll back on any exception. The unit of atomicity is the *logical* operation, not the individual statement.

**2. Take the write lock up front.** With deferred locking, the database acquires the write lock on your first write — which leaves a window between your initial read and that write where another writer can act. Begin the transaction in immediate/exclusive mode (`BEGIN IMMEDIATE` in SQLite) so the write lock is held from the first statement and the whole operation is isolated. Reading current state and then mutating it based on what you read is only safe if nobody can mutate it in between.

**3. Cascade dependent cleanup inside the same transaction.** Deleting a record while leaving its links, children, or back-references in place creates ghosts: a graph traversal follows an edge to an empty node, a join returns a half-row. Delete the dependents in the *same* transaction that deletes the parent, so there is never a committed state where the parent is gone but its dependents linger.

**4. Concurrency hygiene: busy timeout plus WAL.** A concurrent reader or writer should wait briefly and proceed, not immediately throw "database is locked". Set a `busy_timeout` on every connection so contenders block instead of failing. Use WAL journal mode so readers are not blocked by a writer at all. WAL is a persistent property of the database file — set it once at init, not per connection.

**5. References you cannot fix atomically must be tolerated by readers.** Some dependents can't all be cleaned in one transaction — for example, link maps embedded in *other* records that point at the deleted ID. Rather than forcing an unbounded cascade, let the read path guard against missing targets (skip them, let their weights decay) so a dangling reference degrades gracefully instead of crashing a query. Atomicity covers the core mutation; readers absorb the unavoidable residue.

**6. Refresh derived in-memory state after an external mutation.** If a separate process mutates the store — a batch consolidator, a migration script — any in-memory structure a long-running consumer holds (a KDTree, an index, a cache) is now stale and may reference rows that no longer exist. Either rebuild those structures or restart the consumer after the external mutation, and document the coupling so the operator knows the consumer must be cycled.

## Why "it worked in testing" is not evidence

These bugs are invisible under light, single-process, no-crash testing — exactly the conditions of most local runs. They surface under concurrency and failure: two writers, or a process killed mid-operation. The transaction boundary is cheap insurance against a failure mode you will not see until production, when it is a data-integrity incident rather than a code review comment.

## Tooling

`scripts/atomic_sqlite.py` provides `connect()` (sets `busy_timeout` and WAL) and an `atomic(conn)` context manager that runs `BEGIN IMMEDIATE`, commits on clean exit, and rolls back on any exception — generalized from a production merge-and-cascade operation. Run it directly to see a mid-operation exception roll back cleanly, leaving the store exactly as it was.
