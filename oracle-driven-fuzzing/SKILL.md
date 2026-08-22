---
name: oracle-driven-fuzzing
description: Search an input space too large to enumerate, with an oracle strong enough that the bug is visible when it is hit — property-based tests, structure-aware fuzzing, differential and metamorphic oracles, corpus and coverage discipline, shrinking, and crash triage that separates a reproducer from a finding. Use whenever bugs should be found by generated input rather than by reading — "fuzz this", "property-based", "hypothesis/quickcheck/proptest", "libFuzzer", "AFL", "differential testing", "generate test cases", "how do I test this parser/serializer/state machine", "it only breaks on weird input" — or when a crash corpus needs triage. Also trigger when a fuzzer "found nothing", and whenever a round-trip, an encoder/decoder pair, a cache, or a second implementation exists, because those are free oracles. Sibling of falsifiable-testing (hand-written tests) and discriminating-proof (confirming one hypothesis); this skill governs the automated search that generates them. It never calls a crash a vulnerability.
---

# Oracle-Driven Fuzzing

A fuzzer is two things: a generator and an oracle. Everyone builds the
generator. The bugs that matter are lost in the oracle — because the default
oracle is *"the process did not die"*, and almost nothing that matters kills a
process. Silent truncation, a wrong signature verdict, a permission that
widened, an amount off by one unit, a cache that returns another tenant's
entry: all of them exit zero.

So the discipline in one line: **build the strongest oracle you can afford
first, then point a generator at it.** A weak oracle with a billion executions
proves the target does not segfault. That is rarely the claim anyone needed.

Composes with the library:

- **falsifiable-testing** — oracle strength, negative controls, red-first;
  this skill applies them where inputs are generated instead of written
- **invariant-hunting** — the invariant table is the property list to fuzz
- **discriminating-proof** — a fuzzer finding is a *lead*; that skill earns the
  verdict
- **beyond-the-sink** — where to point the next campaign when this one is dry
- **deterministic-core** — a fuzz reproducer must replay bit-for-bit (seed,
  version, corpus commit)
- **honest-degradation** — the "returned something plausible" failures this
  skill is built to catch

Authorization: fuzz targets you own or are authorized to test. Fuzzing a
third-party production endpoint is a load test someone else did not consent to.

---

## Part 1 — Choose the oracle before the generator

Ranked by strength. Take the strongest one the target admits, and say in the
write-up which rung you used, because it bounds every claim the campaign can
make.

| Rung | Oracle | What it catches | Cost |
|---|---|---|---|
| 0 | Process lives | Memory-safety crashes, unhandled panics | free, near-useless in memory-safe languages |
| 1 | Sanitizers / runtime assertions | UAF, overflow, UB, leaked handles, integer wrap | recompile, ~2× slowdown |
| 2 | Declared invariants (`assert` in the target) | Internal contract violations | needs the invariant table |
| 3 | **Round-trip** `decode(encode(x)) == x` | Truncation, precision loss, canonicalization drift | free wherever a codec exists |
| 4 | **Metamorphic** relation between two runs | Wrong results with no reference implementation | requires stating a relation |
| 5 | **Differential** vs a second implementation | Semantic disagreement — the highest-yield class | needs a second implementation |

Rungs 3–5 are the ones people skip, and they are where the interesting bugs
live because they detect *wrong*, not merely *dead*.

**Free oracles already in most codebases.** Look for these before writing a
single generator: an encoder next to a decoder; a serializer next to a parser;
a cache next to the function it caches (`cached(x)` must equal `uncached(x)`);
an optimized path next to a naive one; a rewrite next to the legacy code it
replaces; two SDKs for the same wire protocol; the same validation implemented
in the client and in the server. Every one of those pairs is a differential
oracle nobody is running.

**Metamorphic relations when there is no reference.** State one property that
must survive a transformation:

- reordering independent inputs must not change the result
- a permission-narrowing edit must never widen the effective grant
- adding an ignored field must not change the parse
- `sum(chunks)` must equal `whole`
- normalizing twice must equal normalizing once (idempotence)
- re-signing must not alter the signed bytes

Each is a fuzzable assertion that needs no ground truth.

## Part 2 — The generator must be structure-aware, or it never gets past the front door

Random bytes against a target with a checksum, a magic header, a length
prefix, or a schema spend the entire budget being rejected in the first 20
lines of the parser. Coverage plateaus after minutes and the campaign is
measuring the validity check, not the program.

Fixes, cheapest first:

1. **Seed the corpus with real inputs.** Test fixtures, captured traffic,
   files from the repo's `testdata/`, previous bug reproducers. This alone
   changes most campaigns.
2. **Fuzz below the crust.** Call the internal function after the checksum,
   or recompute the checksum inside the harness so mutation reaches the body.
3. **Use a grammar or typed generator.** `hypothesis`/`proptest` strategies,
   protobuf/ASN.1 structure-aware mutators, an AST generator that emits only
   well-formed programs.
4. **Fuzz the state machine, not just the payload.** Generate *sequences* of
   API calls — `open → write → close → write`, `approve → revoke → resume` —
   and assert the invariant after each step. Most protocol and lifecycle bugs
   are unreachable with any single-input fuzzer.

**Deliberately reserve part of the budget for malformed input.** Structure-aware
generation makes everything valid; the parser's error paths then go untested.
Split the campaign: well-formed inputs to find logic bugs, corrupted ones to
find error-handling bugs.

## Part 3 — Coverage is a diagnostic, never a goal

Coverage answers one question: *is the search still moving?* A plateau is a
signal to change the harness, not a reason to run longer.

When coverage stalls, diagnose before extending:

- Are inputs dying at a validity gate? → Part 2.
- Is a hash, timestamp, RNG, or network call making the target
  non-deterministic? → stub it; a non-reproducible finding is not a finding.
- Is the interesting code behind a flag, a role, or a config the harness never
  sets? → parameterize the harness over configurations.
- Is the oracle at rung 0? → the search may be *finding* things and not
  *noticing* them. This is the most common silent failure of a campaign.

Never report coverage percentage as a security claim. "87% line coverage under
fuzz" says nothing about the 13%, and nothing about whether the oracle could
have seen a failure in the 87%.

## Part 4 — From crash to finding

A reproducer is not a finding. Between them sit four obligations:

1. **Minimize.** Shrink automatically (built into property-based frameworks;
   `afl-tmin`/`llvm-cxxfilt`-style tooling for byte fuzzers), then by hand
   until every remaining byte is load-bearing. A 4-byte reproducer explains
   itself; a 40 KB one gets closed as noise.
2. **Deduplicate by root cause, not by stack.** One bug produces dozens of
   distinct stacks. Group by the *first* frame in your own code and by the
   invariant violated. Report "one bug, 43 reproducers", never 43 findings.
3. **Classify severity honestly.** Ask what an attacker controls and what they
   gain: uncontrolled length in a memory-unsafe language is different from a
   `KeyError` in a Python handler that returns 500. Most fuzz crashes are
   availability-at-most, and saying so preserves credibility for the ones that
   are not.
4. **Pass it to `discriminating-proof`.** The crash is a *plausible
   hypothesis* about impact. The verdict is earned by an experiment with a
   binary oracle and a negative control — not by the fuzzer's exit code.

Record every reproducer as a permanent regression test with its seed, target
version, and corpus commit, so the fix is proven and the bug cannot silently
return.

## Part 5 — "The fuzzer found nothing"

That sentence has five possible meanings, and only the last one is the claim
people hear:

1. The oracle could not see failures (rung 0 on a memory-safe target).
2. The generator never reached the code (validity gate, missing config).
3. The campaign was too short for the search to leave the seed neighborhood.
4. The harness crashed early / the target was non-deterministic and results
   were discarded.
5. The target resisted N executions of this generator under this oracle.

Rule out 1–4 before writing anything. Then state 5 with its bounds —
executions, oracle rung, corpus origin, coverage reached, and what was
*not* in scope. "No bugs found" is never the right sentence; the honest one
names the search. When 5 holds and the budget is spent, hand off to
`forensic-persistence`: the exhausted axis is terrain, and the next campaign
should change the *oracle*, not merely add hours.

---

## Deliverable

```
## Fuzz campaign — <target> <version>
Harness: <entry point, what is stubbed, configurations swept>
Oracle: rung <n> — <the exact assertion>
Generator: <structure-aware? grammar? sequence-level?>
Corpus: <origin, commit, size>  Budget: <executions / wall time>
Coverage: <start → plateau, and what the plateau was diagnosed as>

### Findings (deduplicated by root cause)
<id> — invariant violated — minimized input — epistemic level — impact claim

### Not covered
<code paths the harness cannot reach, and why>
```

## Anti-patterns

- Building the generator first and bolting on an oracle that only checks for
  crashes.
- Reporting "no crashes in 10M executions" as evidence the target is safe.
- Filing one finding per unique stack trace.
- Fuzzing over a network with a non-deterministic backend and calling an
  unreproducible failure a bug.
- Treating a coverage number as a security metric.
- Shipping a reproducer that was never minimized, and losing the triage
  argument to its size.
- Deleting the seed and corpus commit, making the finding impossible to replay.
- Escalating a crash straight to "vulnerability" without an impact experiment.
