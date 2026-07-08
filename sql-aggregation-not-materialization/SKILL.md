---
name: sql-aggregation-not-materialization
description: Push counting, summing, and grouping into the database instead of loading rows to tally them in application code; replace per-item queries inside loops with one batched query; and cap any result set that can grow without bound. Use this whenever code reads from a database to compute a statistic, whenever a loop issues one query per element (the N+1 pattern), whenever an endpoint returns "all" of something, and whenever a function that runs on a hot path (every request, every tick, every recall) deserializes rows it does not need. Triggers — "this query is slow", "it scales with the table", "N+1", "database is the bottleneck", "the export times out", "count by", "group by", "stats endpoint". Push to use this whenever row-reading work grows with corpus size on a frequently-called path.
---

# SQL Aggregation, Not Materialization

A query that loads rows into application memory to count or summarize them is doing the database's job badly. The database can count, sum, and group over millions of rows without handing any of them to you; pulling every row across the wire — deserializing blobs and JSON you will not even look at — to compute a single number is the difference between an O(1) counter and a full-table scan. This matters most exactly where it is easiest to miss: a "cheap" stats function that quietly became a scan because it runs on every request.

## Aggregate in the database

If the answer is a count, a sum, a grouping, or a distinct tally, compute it in SQL and read back the small result — not the rows.

```sql
-- not: load every memory, deserialize embeddings + fingerprints, tally in Python
SELECT state, COUNT(*) FROM memories GROUP BY state;
SELECT COALESCE(SUM(recall_count), 0) FROM memories;
SELECT COUNT(DISTINCT author_id) FROM memories;
```

The materializing version is doubly wasteful: it transfers every row *and* pays the deserialization cost (embedding bytes, fingerprint JSON) for data the tally never touches. Aggregation in SQL stays constant in application memory regardless of corpus size.

## Where it runs matters as much as what it does

A function's cost is its per-call cost times its call frequency. A stats call that materializes the table is tolerable once at startup and catastrophic on a hot path — every recall, every dashboard tick, every websocket broadcast. When you optimize, look first at the functions that run constantly: turning one full-table scan per second into one aggregate query per second is a far bigger win than shaving a rare call. Profile by *where it runs*, not just *what it does*.

## Batch, never N+1

A loop that issues one query per element is the N+1 pattern: 1 query to get a list, then N more, one per item. Collapse it into a single query with an `IN (...)` clause, or preload an index once before the loop.

```python
# N+1: one query per id inside the loop
for mid in ids:
    row = conn.execute("SELECT * FROM memories WHERE memory_id=?", (mid,))

# batched: one query for all ids
rows = conn.execute(f"SELECT * FROM memories WHERE memory_id IN ({ph})", ids)
```

The same applies to graph traversals: load all edges once into an index keyed by source node *before* the BFS, rather than querying each node's edges inside the hop loop. A traversal that did dozens of queries collapses to one.

## Respect the engine's limits when batching

A batched `IN (...)` can exceed a backend limit — SQLite caps bound parameters at 999. Chunk the id list into sub-999 batches and union the results, so the batched query degrades gracefully on large inputs instead of throwing. The fix for N+1 must not become a new failure at scale.

## Cap anything that grows without bound

An endpoint that returns "all nodes" or "the whole graph" returns a small payload in testing and tens of megabytes in production — large enough to time out the request or exhaust memory. Cap it: return the top-N by a meaningful ranking (most-recalled, most-recent) and include a `truncated` flag plus the true total, so the client knows it received a window, not the whole. The honesty of that flag is the hand-off to `honest-degradation`: a truncated result that doesn't say it's truncated is a silently wrong one.

## Tooling

`scripts/sql_aggregation.py` is a runnable SQLite demo contrasting a materializing tally with a SQL `GROUP BY`, a chunked batch loader that respects the 999-parameter limit, and a capped export that returns a `truncated` flag — showing the aggregate and the scan return identical numbers while only one of them reads the rows.
