---
name: resource-exhaustion-review
description: Find the places in your own code where a small input buys a large amount of work or memory, and bound them — input-controlled loops and allocations, super-linear algorithms, catastrophic regex backtracking, decompression and expansion ratios, unbounded fan-out and retries, and missing backpressure. Use whenever writing or reviewing code that sizes anything from an untrusted value, and whenever a system falls over under load rather than under attack. Trigger on "ReDoS", "zip bomb", "billion laughs", "OOM", "the worker ran out of memory", "it hangs on large input", "quadratic", "N+1", "timeout under load", "retry storm", "thundering herd", "rate limit", "backpressure", "pagination", "batch size", "how big can this get", "we never set a limit", or a request whose cost depends on a caller-supplied count, depth, or size. Availability is an invariant like any other. This skill hardens code you own — it bounds work and sheds load; it never plans or conducts availability attacks against any system.
---

# Resource Exhaustion Review

Correctness review asks whether the code produces the right answer. This asks
what it costs to make it try. Availability is an invariant — *bounded work per
request* — and it is the one invariant almost nobody writes down, so almost
nobody notices when a refactor deletes it.

The measure that matters is not "is this slow?" but the **asymmetry ratio**:

> **What does one request cost the caller, and what does it cost the system?**

A 40-byte request that allocates 4 GB has a ratio of 10⁸. That ratio is the
finding. It does not require a botnet to matter — a single retrying client, a
misconfigured integration, or a customer importing a genuinely large file will
find it first, which is why this is reliability work as much as security work.

Scope: this skill reviews and hardens systems you own or are authorized to
test. Load testing goes against your own environment with the owner's
agreement. It produces limits, budgets, and load-shedding — never traffic
aimed at anyone.

Composes with the library:

- **validate-at-the-boundary** — the limit belongs at the edge, with a clear
  error, before the value sizes anything
- **secure-by-construction** — bounds are part of the contract, written before
  the diff
- **oracle-driven-fuzzing** — a timeout or an allocation ceiling is an oracle;
  fuzz for the input that hits it
- **concurrency-reasoning** — retry storms, thundering herds, and pool
  starvation are concurrency failures wearing a capacity costume
- **sql-aggregation-not-materialization** — the database-specific case of
  loading unbounded rows into memory
- **honest-degradation** — when shedding load, fail visibly; never return a
  truncated answer as if it were complete

---

## Part 1 — Follow the untrusted number

Grep-equivalent for this class: find every place an attacker-influenced value
becomes a *size*, a *count*, a *depth*, or a *repetition*.

```
limit  count  size  length  depth  page  per_page  batch  n
range  repeat  timeout  retries  width  height  quality  scale
```

For each, ask three questions in order:

1. **Is there a maximum?** Not a default — a *ceiling*, enforced at the
   boundary, that a caller cannot exceed.
2. **Is the work linear in it?** Two nested loops over a caller-controlled list
   turn 10× input into 100× work.
3. **Is the resource released?** Bounded per request is not bounded in
   aggregate if a thousand requests each hold their bound simultaneously.

The classic sources of an untrusted number that reviewers miss: a length prefix
in a binary format (allocating the declared size before reading it), a
`Content-Length` used to preallocate, a JSON array's length, a page size, a
recursion depth in nested structures, a `count` in a batch endpoint, image
dimensions in a header, and a client-supplied timeout or retry count.

## Part 2 — The amplification families

| Family | Shape | Where it hides |
|---|---|---|
| **Allocate-before-verify** | trust a declared size and reserve it before the bytes arrive | binary parsers, upload handlers, RPC framing |
| **Expansion ratio** | small compressed input, huge expansion | gzip/zip/tar entries, XML entities, deeply nested JSON, image and video decoding, recursive templates |
| **Super-linear algorithm** | O(n²) or worse in caller-controlled n | nested loops, repeated string concatenation, `list.remove` in a loop, dedup by scan, join in application code |
| **Catastrophic backtracking** | nested quantifiers with overlapping alternatives, applied to caller input | validation regexes, log parsing, `User-Agent` matching, anything user-supplied compiled as a pattern |
| **Hash/collision degeneration** | worst-case buckets or cache keys chosen by input | hash maps keyed by raw input, dedup sets, cache namespaces |
| **Fan-out** | one request becomes many downstream calls | N+1 queries, per-item API calls, webhook broadcast, graph query depth |
| **Unbounded accumulation** | memory that grows and is never trimmed | in-memory caches without eviction, unbounded queues, per-connection buffers, log lines held for batching |
| **Retry amplification** | each layer retries the layer below | client × gateway × service × DB: 3 layers of 3 retries is 27× at the bottom |
| **Held resources** | scarce handles kept during slow work | a DB connection held across an HTTP call, a lock held during I/O, a thread per idle connection |

Two rules of thumb that catch most of it: **never allocate what you have not
yet received**, and **never let one request's work depend on a number the
request itself chose**.

## Part 3 — Bound it at four levels

A single limit is usually the wrong fix; work down this ladder and take every
rung that applies.

1. **Bound the input.** Maximum body size, maximum array length, maximum
   nesting depth, maximum decompressed bytes (stream and count, aborting when
   the ratio is exceeded — never decompress to memory to measure it), maximum
   page size with a hard server-side cap. Reject at the boundary with a clear
   error naming the limit.
2. **Bound the work.** A timeout and a memory ceiling per operation, enforced
   where the work happens. Replace the super-linear algorithm where one exists;
   for regex, prefer a real parser or a non-backtracking engine over patching
   the pattern.
3. **Bound the concurrency.** Bounded pools and bounded queues, so the system
   refuses rather than swallows. Apply backpressure: a full queue must reject,
   not grow. Retries need jitter, a budget, and a circuit breaker; retry at one
   layer only.
4. **Bound the blast radius.** Isolate expensive work in its own pool or worker
   so it cannot starve cheap requests. Quota per tenant, not only globally —
   one customer's import must not consume everyone's capacity. Shed load
   deliberately, and say so honestly in the response (`honest-degradation`),
   never by silently returning partial results.

Then **write the bound down** as a stated contract: "this endpoint accepts at
most 1 MB / 1 000 items / depth 32, and completes within 5 s". Undocumented
limits get removed by the next refactor; a limit in the contract gets a test.

## Part 4 — Prove the bound, then keep it

- **A limit without a test is a comment.** Write the test that sends
  limit + 1 and asserts the rejection, and the test that sends the limit and
  asserts success. `falsifiable-testing`: see it fail first.
- **Measure the ratio, do not estimate it.** Run the worst case you can
  construct in your own environment and record input bytes → peak memory, CPU
  time, and downstream calls. That measurement is the evidence in the report;
  "could be exponential" is a hypothesis.
- **Fuzz for it.** Point `oracle-driven-fuzzing` at the parser with a timeout
  and an RSS ceiling as the oracle. This class is unusually well suited to
  automated search, because the oracle is trivial and needs no ground truth.
- **Alert on the ratio, not just on the outcome.** Requests whose cost exceeds
  the budget are a detection (`detection-engineering`) and an early warning
  that a limit was removed. Paging on the OOM is paging on the aftermath.

---

## Deliverable

```
## Resource review — <component>
| path | untrusted number | ratio (in → cost) | current bound | proposed bound |

Measured worst case: <input> → <peak memory / CPU / downstream calls>
Bounds added: input / work / concurrency / blast radius
Tests: limit+1 rejected, limit accepted, measured under the ceiling
Stated contract: <the documented limits>
Not reviewed: <paths not covered>
```

## Anti-patterns

- Treating this as a performance nicety and deferring it — availability is a
  security property, and the ratio is the finding.
- Adding a rate limit and calling the class closed: rate limits divide the
  cost, they do not bound one request's work.
- Setting a default instead of a ceiling, so a caller can pass a larger value.
- Decompressing fully in order to check the decompressed size.
- Retrying at every layer, multiplying load exactly when the system is
  degraded.
- Enforcing a global quota only, so one tenant can consume the whole budget.
- Patching a catastrophic regex by adding another quantifier.
- Shedding load by returning a truncated result that looks complete.
- Removing a limit during a refactor because "no test covered it" — which is
  the argument for the test, not for the removal.
