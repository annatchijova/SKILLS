---
name: language-selection
description: >
  Select programming languages, DSLs, query languages, policy languages, proof
  systems, or runtimes from the concrete forces of the problem rather than from
  model familiarity or the human's prior exposure. Use whenever new code must be
  written and the language is not already fixed: scripts, tools, services,
  parsers, deterministic cores, security components, smart contracts, queries,
  data pipelines, scientific code, infrastructure, embedded software, kernels,
  CLIs, prototypes, or agent-generated implementations. Also use when comparing
  languages, reconsidering an existing component's language, or deciding whether
  a system should be polyglot. In an agentic workflow the model — not the human —
  is responsible for surfacing the right candidates, including ones the human has
  never used; the human's job is to own the trade-off, not to have memorized the
  option space.
---

# Language Selection

A programming language is a bundle of guarantees you buy and a bundle of failure
modes you inherit. It decides which bugs are impossible, which are caught at
compile time, which are caught by tests, and which reach production. It decides
what the artifact is, how concurrency fails, how numbers round, and who can
maintain the thing in three years.

A model has a strong prior: it reaches for whatever dominated its training corpus
for tasks that look similar — usually Python, sometimes TypeScript, occasionally
Rust when the request sounds serious. **A prior is not a reason.** This skill
replaces the prior with a derivation: the forces of the problem, mapped onto the
computational model of each candidate, with losers named and the winner
falsifiable.

## The central thesis

**The human is not expected to already know every relevant language, DSL, query
language, proof system, runtime, or paradigm.** If SPARQL, Datalog, Rego,
Ada/SPARK, Lean, Julia, Erlang, Rust, CUDA, or something the human has never
touched is the right fit, the model surfaces it anyway.

> The model is responsible for knowing and expanding the option space.
> The human is responsible for understanding enough of the proposed trade-off
> to own the decision.

This cuts both ways. Never withhold a candidate because "the human doesn't know
it" — that is knowledge retrieval, and knowledge retrieval is delegable. But never
select an unfamiliar language merely because the model can generate it, either —
architectural judgment is not delegable, and the human still has to be able to
audit the decision and own its consequences.

This is not a skill against any language, and not a skill for the technically
"strongest" one. Python is right for a large share of real work, and this skill
picks it whenever the forces point there. Static typing is not automatically
superior; native code is not automatically faster in the dimension that matters;
a declarative language is not "weaker" because it expresses less mechanism.
**There is no default language.** If the choice cannot be traced to a concrete
constraint, it hasn't been made yet.

In abductive-engineering terms: the chosen language is a **hypothesis** — the one
that best explains the constraints. The reopen condition is its falsifier, and
production is where induction tests it.

**Composes with:** decision-record-discipline (the output here is a decision
record), deterministic-core (numeric/serialization constraints that eliminate
candidates), validate-at-the-boundary (static types end at the runtime edge in
every language), concurrency-reasoning, dependency-provenance (the ecosystem is
also a supply chain), sql-aggregation-not-materialization, secure-by-construction.

---

## Why agentic development changes the cost model

AI substantially reduces the cost of: syntax recall, boilerplate, API lookup,
initial implementation, translation between languages, mechanical refactoring.

AI does **not** reduce the cost of: wrong architecture, wrong computational
model, misunderstood semantics, invalid invariants, unsafe trust boundaries,
dependency/supply-chain decisions, verification, debugging, operational failure,
long-term maintenance.

Two symmetric errors follow from confusing these:

- Ruling out a language because the human "can't write it fluently from memory."
  Syntax fluency is the part AI absorbs; it is not a proxy for whether the human
  can read, review, and own the result.
- Choosing an unfamiliar language *because* the model can generate it, without
  the human developing enough understanding of its guarantees and failure modes
  to audit what got built.

Maintainer fluency still matters for long-term ownership — but distinguish
**syntax fluency**, **reading comprehension**, **semantic understanding**,
**debugging capability**, and **operational maintainability**. Don't collapse
these into a single "knows the language: yes/no." A human who has never written
Rust can still own a Rust component if the model surfaces its ownership model,
its panic/`unsafe` boundaries, and its verification story clearly enough for the
human to interrogate the choice and read the diffs that matter.

## Who owns what

**Human owns:** problem definition, requirements, invariants, trust boundaries,
acceptable failure modes, operational constraints, the trade-off decision itself,
acceptance criteria, final sign-off.

**Model owns:** expanding the candidate space; identifying relevant paradigms,
languages, DSLs, runtimes — including ones the human didn't mention or doesn't
know; explaining why each candidate entered the search, what it buys, what it
costs, and where its guarantees end; challenging its own preferred or default
candidate; implementing once the decision is made.

**Shared:** the model proposes and explains; the human interrogates and decides;
the implementation is tested against the properties that motivated the choice —
mechanically (compiler, type checker, tests, fuzzer, sanitizer) and behaviorally
(does it actually satisfy the force that picked it).

---

## Procedure

### 1. Is the language actually open?

Extending an existing codebase, a browser target, a mobile platform, a database
query, an EVM/Soroban contract, a kernel subsystem, an external mandate, or a
library that exists in exactly one ecosystem — all of these impose the language.
Say so in one line and move on, unless the imposed choice creates a material
problem worth flagging separately. Otherwise, continue.

### 2. What kind of problem is this, actually?

Before naming any language, classify the computational shape — per component,
since one system can mix shapes. Ask explicitly:

Is this even a general-purpose programming-language problem — or is it
relational, logical/rule-based, policy-based, symbolic, numerical, statistical,
concurrent, distributed, actor-oriented, dataflow, systems-level, embedded/real-
time, GPU/accelerator, smart-contract, proof-oriented, hardware-description,
infrastructure/configuration, query-shaped, or otherwise domain-specific?

The shape alone eliminates most candidates before performance ever comes up:
relational → SQL; rules/authorization → Datalog, Prolog, or Rego; a statistical
report → R or Python's stack; numerical simulation → Julia, Python+native, or
C++; hostile binary input → a memory-safe language; many independent,
failure-prone conversations → BEAM or Go; gluing tools together → Python or
shell. The human does not need to have named any of these first — discover them.

### 3. Extract the forces, with numbers where numbers exist

State each applicable constraint concretely: not "fast" but "p99 under 5 ms at
2k req/s"; not "secure" but "parses PDFs from anonymous uploaders"; not
"reproducible" but "sealed with SHA-256, must recompute identically on a third
party's machine." Where no real measurement exists, say so instead of inventing
one — a guessed number is worse than an honest "unmeasured."

| Axis | Decides | Breaks when mismatched |
|---|---|---|
| Type discipline | static/dynamic, sound/unsound, erased/reified | prod errors assumed impossible; an annotation trusted as a runtime check |
| Memory model | GC, refcounting, ownership, manual, arenas | latency-budget pauses; use-after-free on hostile input; cycle leaks |
| Execution model | AOT native, JIT/VM, interpreter, WASM | startup cost, JIT warm-up, missing runtime on target |
| Concurrency model | threads+locks, GIL, CSP, async, actors, STM | races, deadlocks, colored-function sprawl, cores left unused |
| Error model | exceptions, Result/Option, error returns, let-it-crash | swallowed failures, prod panics, errors dropped because dropping was free |
| Numeric model | IEEE-754 doubles, bignums, fixed-width, decimals, rationals | money in floats; silent overflow; a sealed result that diverges by machine |
| Distribution artifact | static binary, bytecode+VM, source+interpreter+deps | "works on my machine"; an installer bigger than the program |
| Ecosystem/supply chain | which mature libraries exist; how deps resolve | rebuilding a solved problem, or importing a bigger attack surface than the app |
| Fault tolerance | independent crash/restart, supervision | one bad input takes the whole system down |
| Auditability | explainable, sealed, replayable decisions | a verdict nobody can reproduce or challenge |
| Maintainers | who can read, review, change this in three years | a correct system nobody can touch safely |

If maintainer fluency could decide it and is unknown, ask — don't assume.

### 4. Surface candidates the human may not have named

This is the model's core responsibility. For every force from Step 3, ask what
computational model answers it best, without filtering by what the human already
knows. A non-exhaustive prompt list, organized by problem shape — **never treat
this as a whitelist**; surface something not on it when the forces justify it:

- **Systems/native:** Rust, C, C++, Zig, Ada/SPARK
- **Managed/general-purpose:** Go, Java, Kotlin, C#, Swift
- **Dynamic/scripting:** Python, JavaScript/TypeScript, Ruby, Lua, Perl
- **Functional/ML-family:** Haskell, OCaml, F#, Scala, Clojure
- **Concurrent/fault-tolerant:** Erlang, Elixir (BEAM)
- **Relational/query/logic/policy:** SQL, Prolog, Datalog, Rego, SPARQL, Cypher, Gremlin
- **Scientific/numerical/statistical:** Julia, R, MATLAB, Fortran
- **GPU/accelerator:** CUDA, HIP, OpenCL, SYCL, WGSL, Metal, GLSL
- **Shell/automation:** Bash/POSIX, PowerShell
- **Infrastructure/configuration:** HCL, Nix, Dhall, Jsonnet, CUE, Starlark
- **Smart contracts:** Solidity, Vyper, Rust (where platform-imposed), Move
- **Hardware description:** Verilog, SystemVerilog, VHDL, Chisel
- **Proof/formal:** Lean, Coq, Agda, Isabelle/HOL

See `references/candidate-index.md` for a compact per-language cheat sheet
(buys / costs / typical failure mode to guard against) — a lookup aid for
picking candidates fast, not a tutorial. The model already knows how to program
in these; the index exists so the *decision* stays fast, not so the model learns
syntax.

For every candidate that the human may not know, use this contract instead of a
syntax lecture:

```
Candidate: <language / model>
Why it entered the search: <the specific force>
What it buys: <the relevant property>
What it costs: <the relevant cost>
Where the guarantee ends: <the important limitation>
Why not <the obvious/default alternative>: <the specific distinction>
How we'd verify the implementation: <compiler/type checker/test/fuzzer/analyzer>
```

### 5. Separate the language from its environment

Don't attribute to a *language* what belongs to its compiler, runtime, standard
library, framework, deployment target, or hardware. "Rust is deterministic" is
too broad — determinism still depends on iteration order, floats, external
services, serialization, clocks, and dependency versions. "JavaScript is
single-threaded" is too broad — the real execution model depends on the host,
workers, and native extensions. Name the actual layer responsible, and avoid
claims brittle enough to age out within a couple of major versions unless the
distinction is load-bearing for the decision.

### 6. Consider decomposition, and price every boundary

A system doesn't need one language. Ask whether components have genuinely
different forces (a Rust core under Python orchestration, SQL for the relational
slice, Rego for authorization behind a Go/Kotlin service, a Rust/WASM module
under a TypeScript frontend). Every boundary costs a second toolchain,
serialization, FFI review, duplicated domain models, extra reviewers. A split is
justified by a force, per component — never by taste, and never invented just to
pad the candidate list.

### 7. Name the rivals and attempt to falsify the preferred one

At least two viable candidates, plus the corpus-prior default if it didn't win.
For each rejected candidate: the force it lost on, and its strongest argument —
that's what tells a future reader when to reopen the decision. Then attack the
winner: is the bottleneck measured or assumed? Is this chosen for prestige, or
because the model generates it well? Is a boundary's complexity bigger than what
it buys? Which changed assumption would flip the choice? A decision block
listing only the winner is a press release, not a decision.

### 8. Break ties honestly

When the forces genuinely don't discriminate, prefer the option with the lowest
total maintenance cost in the actual development environment.

Do not reduce that to prior syntax fluency alone — that's the corpus-prior bias
from Step 3 sneaking back in through the tie-breaker. Consider separately:
reading comprehension, semantic understanding, debugging capability, tooling
support, available agent assistance, operational familiarity, fit with the
surrounding stack, and the actual cost of acquiring whatever knowledge is
missing. Prior maintainer experience is a legitimate tie-breaker, not an
automatic veto against an unfamiliar language — a team with no Rust history but
strong compiler/test/review support from an agent has a different real
acquisition cost than a team maintaining it unassisted.

Write the tie-breaker down as the tie-breaker it is, not dressed up as a
technical advantage.

### 9. Scale the depth to the stakes

A ten-line disposable script doesn't need an ADR. Scale reasoning depth with
consequence of failure, expected lifetime, architectural commitment, security
exposure, migration cost, and uncertainty. Trivial work gets 1-2 lines. Security-
critical or long-lived components get the full derivation.

### 10. Record the decision before writing substantial code

```markdown
## Language decision — <component>

Problem shape: <what kind of computational problem this actually is>
Language imposed?: no | yes — <why>

Decisive forces:
- <concrete force>

Candidates surfaced:
- <candidate> — entered because <force>
- <candidate> — entered because <force>

Chosen: <language/model> [+ <language> for <component>, if split]
Why: <how its actual model/runtime/ecosystem answers the forces>

Guarantees we're relying on:
- <guarantee> — provided by <language | compiler | runtime | framework>

Guarantees we're NOT getting:
- <important boundary>

Rejected:
- <candidate> — lost on <force>. Strongest argument for it: <one line>.

Accepted cost: <what gets worse on purpose>
Verification plan: <how the generated implementation gets checked>
Boundaries (if split): <what crosses, how, what it costs>
Reopen if: <observable condition that would flip the choice>
```

For trivial code, collapse this to 1-2 lines. Never zero.

---

## On Python, and on defaults in general

Python is frequently correct — glue, data, ML, research, automation, or an
exact-arithmetic core that isn't throughput-bound usually goes to Python on
ecosystem, iteration speed, and a standard library with `Fraction` and bignums
built in. Defaulting to it anyway is still a defect, exactly like defaulting to
TypeScript or reaching for Rust because the task sounds serious — the problem is
never the language, it's the missing derivation. The test is symmetric: can the
"why this one" line be written in terms of a Step 3 force? If yes, the choice
stands, whatever it is. If the only honest answer is "it came to mind first,"
the choice hasn't been made yet.

## Anti-patterns

- Choosing by corpus prior, prestige, or "sounds serious" instead of a stated
  force. "Rust > Python," "static > dynamic," and "the agent knows best" are not
  arguments.
- Withholding a candidate because the human hasn't used it — that's the model
  refusing its own job.
- Choosing an unfamiliar language purely because the model generates it well,
  without giving the human enough to audit the choice.
- Benchmark claims without representative measurement.
- Rewriting a whole system around a small hot path that could be isolated behind
  one boundary.
- Reimplementing joins/aggregation/grouping imperatively instead of using SQL.
- Treating static types as validation of hostile input, or memory safety as
  complete application security.
- Calling something "deterministic" without naming the actual layer responsible.
- Treating generated code as correct because it compiles.
- Adding a second language without pricing the boundary.
- Choosing first, justifying afterward.
- Turning this skill into "learn every language" or "humans no longer need
  programming knowledge" — knowledge retrieval is delegable, architectural
  judgment is not.

## Deliverable checklist

- [ ] Checked whether the language is imposed before comparing anything.
- [ ] Problem shape identified per component, used to eliminate candidates.
- [ ] Forces stated as concrete constraints, numbers where they exist.
- [ ] Candidate space actually expanded — including at least one candidate the
      human likely didn't name, when the forces justify it.
- [ ] Each unfamiliar candidate explained via the contract (why/buys/costs/
      guarantee-ends/verification) — no syntax lecture.
- [ ] At least two named rivals with the force each lost on and its strongest
      argument, or a stated reason only one is viable.
- [ ] Language claims attributed to the correct layer (language vs. runtime vs.
      framework vs. hardware).
- [ ] Any split justified per component by a force, and each boundary priced.
- [ ] Reasoning depth scaled to consequence, lifetime, and security exposure.
- [ ] An observable reopen condition is stated.
- [ ] A verification plan is stated for the chosen implementation.

## How to respond when this skill is active

Never open by writing code in a language that wasn't derived — produce the
decision block first, sized to the stakes. Check whether the language is imposed
before comparing. Expand the candidate space actively; don't wait for the human
to name options, and don't prune options because the human hasn't used them.
Explain unfamiliar candidates through the contract, not a tutorial — the model
already knows how to program in them; what the human needs is the trade-off, not
the syntax. Treat Python like every other candidate. Name the rivals and their
strongest arguments. Split only when a component's forces genuinely differ, and
price the boundary. State a verification plan and a reopen condition. Then
implement — and carry the chosen language's known failure modes into that
implementation from the first line.
