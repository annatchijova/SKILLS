# Candidate index

A fast lookup for the model when surfacing candidates in Step 4 — not a
tutorial. The model already knows how to program in every entry here; this
file exists so the *decision* moves fast, not so the model learns syntax.

Not exhaustive. Not a whitelist. Surface anything not listed here when the
forces justify it (a graph database language, a solver, a domain-specific
notation, a newer runtime).

For each: the property it's usually reached for, the cost it usually carries,
and the one failure mode most worth guarding against once it's chosen.

| Language | Reached for | Costs | Guard against |
|---|---|---|---|
| Rust | memory safety without GC, sealed/deterministic cores, hostile-input parsers | ownership learning curve, slow builds | `unsafe` without a written safety argument; `.unwrap()` on reachable paths |
| C | hardware control, stable ABI, tiny footprint | no memory safety | UB, unchecked buffers, unchecked returns |
| C++ | native perf with abstraction, existing C++ ecosystems | UB inherited from C, build complexity | dangling references, ABI drift across compilers |
| Zig | explicit low-level control, C interop, cross-compilation | pre-1.0 instability | `ReleaseFast` strips safety checks |
| Ada/SPARK | certified/high-assurance systems | small ecosystem | — |
| Go | operational simplicity, cheap I/O concurrency, single static binary | weak sum types, GC pauses | nil-in-interface trap, silently dropped `err`, goroutine leaks |
| Java/Kotlin | long-lived services, JVM data ecosystem, Android (Kotlin) | startup/footprint, framework weight | null at Java boundary, unsafe deserialization |
| C# | .NET/enterprise/Unity ecosystems | — | async-over-blocking deadlocks |
| Swift | Apple platforms | ARC cycles | actor-isolation migration bugs |
| Python | glue, data/ML, exact-arithmetic cores at moderate scale (`Fraction`, bignums) | 1-2 orders of magnitude slower CPU-bound, GIL limits threads, runtime type errors | mutable default args, `pickle`/`yaml.load` on untrusted input |
| JavaScript/TypeScript | browser (imposed), full-stack JS ecosystem | types erased/unsound, all numbers are doubles past 2^53, npm supply chain | `any` leaking through APIs, money/IDs as `number` |
| Ruby, Lua, Perl | web productivity (Ruby), embeddable scripting (Lua), text-processing legacy (Perl) | small-to-niche ecosystems for new work | — |
| Haskell | correctness-critical transformations, compilers/DSLs | lazy-eval reasoning difficulty, small hiring pool | space leaks, partial functions (`head`, `fromJust`) |
| OCaml/F# | ML-family predictability, compilers/symbolic tooling, .NET interop (F#) | narrower ecosystem | mutable state hiding inside "functional" code |
| Scala, Clojure | JVM + expressive types (Scala) or JVM + dynamic/immutable data (Clojure) | added conceptual weight | — |
| Erlang/Elixir (BEAM) | fault isolation, massive lightweight concurrency, let-it-crash | weak raw CPU throughput | mailbox growth from slow consumers, blocking NIFs |
| SQL | relational operations: joins, aggregation, constraints | dialect drift | string-built queries (always parameterize), `NULL` three-valued logic |
| Prolog/Datalog/Rego | rules/inference/authorization policy, transitive closure | poor fit for general app code | Prolog clause-order sensitivity, closed-world assumption |
| SPARQL/Cypher/Gremlin | graph- or RDF-shaped data | wrong fit outside graph problems | — |
| Julia | numerical/scientific code needing both speed and expressiveness | compile latency, smaller package ecosystem | type instability silently kills performance |
| R | statistics, reproducible reports, tidyverse | weak general-purpose engineering | silent vector recycling, `NA` propagation, unpinned packages |
| MATLAB, Fortran | domain toolboxes (MATLAB), legacy HPC codebases (Fortran) | licensing / age | — |
| CUDA/HIP/OpenCL/SYCL/WGSL/Metal/GLSL | GPU/accelerator kernels | target usually dictated by hardware, not preference | — |
| Bash/POSIX shell | process composition, CI glue, bootstrap scripts | no real data structures or error handling | unquoted variables, `set -e` surprises in pipelines |
| PowerShell | Windows/.NET automation | ecosystem-specific | — |
| HCL/Nix/Dhall/Jsonnet/CUE/Starlark | config generation, reproducible environments, infra state | learning curve per tool | — |
| Solidity/Vyper/Move/Rust(Soroban) | smart contracts, adversarial execution environments | platform-imposed, gas/resource semantics | treat as adversarial runtime, not a normal backend |
| Verilog/SystemVerilog/VHDL/Chisel | hardware description | different failure semantics than software | evaluate as hardware, not sequential code |
| Lean/Coq/Agda/Isabelle | machine-checked proofs | usually complements, not replaces, the production language | — |
