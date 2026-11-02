---
name: fuzz-campaign-design
description: "Design and run a fuzzing campaign with discipline: harness construction, seed-corpus curation, coverage and sanitizer instrumentation, oracle/invariant selection, mutation vs grammar/structure-aware strategy, and a stop/triage criterion. Re-expressed as a scoped engineering experiment on an owned target that states the oracle and coverage goal up front and routes findings to triage, not a point-and-shoot crash hunt."
---

# Fuzzing Campaign Design

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the campaign design below.
This revision restores the upstream's fuzzing craft as a designed experiment: harness, corpus, coverage, oracle and stop criterion stated before running, with crashes routed to disciplined triage rather than treated as finished findings. Compose with `oracle-driven-fuzzing`.

## Scope and prerequisites

A fuzzing campaign is an experiment: what are you feeding, what are you measuring, and what counts as a bug? Fuzz an owned target or an in-scope component you may instrument. State the oracle up front — a crash is one oracle, but differential/metamorphic/assertion oracles find logic bugs a crash never will.

Declare the target, the harnessed entry point, the budget (CPU-hours), and the stop/triage criterion. Instrument-free black-box fuzzing yields weaker evidence — mark coverage NOT MEASURED.

## Design dimensions

- **Harness** — the smallest, fastest entry point that reaches the target logic deterministically; strip nondeterminism (time, RNG, network) or seed it.
- **Seed corpus** — minimal, diverse, valid inputs covering distinct code paths; minimize/`cmin` to remove redundancy.
- **Coverage** — compile with coverage instrumentation (SanitizerCoverage/`-fsanitize-coverage`); measure edges, not just lines.
- **Sanitizers** — ASan/UBSan/MSan/TSan as crash oracles that surface silent corruption.
- **Oracle** — crash (sanitizer), differential (two implementations disagree), metamorphic (a transform should not change output), assertion/invariant (an internal property must hold).
- **Strategy** — coverage-guided mutation (libFuzzer/AFL++) vs grammar/structure-aware (for structured inputs) vs generation-based.

## Mechanism and observation

Design so that a failing input is attributable to a stated oracle violation.

**Firstness:** Record coverage growth, the oracle that fired, and the input that caused it. **Secondness:** State the expected behavior (no sanitizer fault, implementations agree, invariant holds) and the deviation. **Thirdness:** Infer a bug class only after triage confirms the oracle violation is a real defect (route to `rt-bug-identification`/`rt-crash-analysis`).

## Abduction and refutation

**Hypothesis:** The target has reachable states violating the stated oracle that the current corpus/strategy has not yet reached.

**Competing benign explanation:** Coverage is plateaued because the harness cannot reach deeper code (harness defect, not target robustness); the "crash" is a harness/oracle bug; the differential is an intended behavioral difference; the input is invalid in a way the real caller prevents.

## Deduction and controls

A valid corpus runs clean under the oracle (positive control). A productive campaign grows coverage and surfaces oracle violations that triage confirms. Predeclare the coverage target and the oracle. A plateau with a harness that demonstrably cannot reach the target is a harness-effectiveness WARN, not target assurance.

## Induction: bounded campaign procedure

Owned/instrumented target.

1. **Harness.** Build the minimal deterministic entry point; verify it executes a known input and reaches the target code.
2. **Corpus.** Gather and minimize diverse valid seeds; confirm baseline coverage.
3. **Instrument.** Enable coverage + sanitizers; pick the oracle(s).
4. **Run to the budget.** Track coverage over time; save every oracle-violating input; deduplicate by coverage/stack.
5. **Triage.** Route unique findings to `rt-bug-identification` and `rt-crash-analysis` — a crash is a CANDIDATE until triaged.
6. **Assess coverage honestly.** Report what the campaign did and did not reach; a clean run over low coverage is WARN, not PASS.

Record results including refutations. Keep finding status separate from coverage/harness-effectiveness status.

## Craft notes (leads)

libFuzzer/AFL++ for coverage-guided mutation; grammar/structure-aware fuzzers for structured formats; differential fuzzing for parsers/implementations; property-based testing for logic invariants. The oracle choice determines what you can find — a crash-only campaign is blind to logic bugs. Corpus minimization and dictionary tokens accelerate reach. Determinism in the harness is essential for reproducibility.

## Domain-specific failure modes

"No crashes" over low coverage proves nothing — report coverage. A plateau is often a harness limitation, not target robustness. Sanitizer findings can be harness/oracle bugs; triage before claiming. Differential "bugs" can be intended differences. A crash is not a vulnerability until triaged (see `rt-crash-analysis`).

## Evidence and deliverable

Provide the harness, corpus, coverage achieved (edges), the oracle(s), the unique oracle-violating inputs, and their triage disposition. Attach minimal reproducers, expected/observed, rival explanation (harness/oracle bug), falsifier, code not reached.

## Versions and tool limitations

Pin the fuzzer, sanitizer and compiler versions. Coverage and sanitizer semantics are toolchain-specific. No target behavior was verified by this content beyond the instrumented run; reproduce findings independently.

## Remediation and detection

Fix root-cause defects, add the reproducing inputs as regression/corpus seeds, and run the campaign continuously in CI with a coverage floor. Treat coverage regressions as build failures. Report the guarantee level honestly (coverage reached), never a blanket "fuzzed, therefore safe".

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An oracle-violating input, triaged to a real defect, over meaningful coverage: CONFIRMED (bug class per triage). |
| Benign refutation | The crash is a harness/oracle bug or an intended differential: REFUTED. |
| Insufficient evidence | Clean run but low/uncertain coverage: NOT TESTED for the unreached code; WARN on coverage. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/fuzzing/offensive-fuzzing/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's harness/corpus/coverage/oracle/strategy craft, re-expressed as a designed experiment with a stated oracle, coverage honesty and triage routing, replacing point-and-shoot crash hunting with a measured campaign. Composes with `oracle-driven-fuzzing`, `rt-bug-identification`, `rt-crash-analysis`, `rt-vuln-classes`.
