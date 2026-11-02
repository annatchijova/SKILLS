---
name: fuzz-campaign-design
description: Design bounded reproducible fuzz campaigns with meaningful oracles. Use when selecting harnesses, corpora, instrumentation or crash-triage procedures for owned parsers and services.
---

# Fuzz Campaign Design

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Choose the observable failure
Write the invariant before selecting a fuzzer. Use sanitizers for memory safety, round-trip properties for lossless codecs, metamorphic properties for normalization, and differential comparison only when implementations promise equivalent semantics.
Prove oracle sensitivity with a deliberately faulty local fixture; do not mutate production code.

## Harness and budget
Call the narrowest production entry point that preserves the relevant boundary. Record what authentication, parsing or network behavior the harness bypasses.
Reset persistent state between inputs. Fix or capture time, randomness, seed, build flags and dependency versions. Avoid uncontrolled network access.
Start from valid synthetic fixtures plus prior minimized failures; reserve malformed cases for error paths. Set wall-time, memory, input-size and execution budgets before running.
Use structure-aware generation when validation blocks deeper paths. For stateful APIs generate transitions and assert invariants after each step.

## Interpret results
A coverage plateau can mean unreachable code, weak seeds or an insufficient oracle; inspect which before extending the budget.
Minimize failures, replay in a fresh process, deduplicate by cause and separate harness defects from target defects. Differential disagreement is a lead until the contract determines which behavior is wrong.
Retain minimized input, seed, corpus identity and replay command. An unexplained crash is not demonstrated code execution.

## Output
Report harness boundaries, oracle sensitivity, budgets used, coverage limits, reproducible failures and unresolved cases. Turn confirmed failures into regressions. A clean campaign only bounds the inputs and properties actually exercised.

## Experimental contract and controls

Read [the assessment contract](../METHODOLOGY.md) before running the campaign.
Input: target/build identity, entry-point contract, owned corpus and permitted configurations.
Define one concrete invariant and its falsifier before choosing mutation strategy.
Record actor-controlled fields and any validation deliberately skipped by an internal harness.
An internal parser finding does not establish external reachability.
Use inert fixtures; do not construct exploit payloads or bypass mitigation mechanisms.

## Mechanism-specific instrumentation

- ASan: selected spatial and lifetime errors in instrumented native paths.
- UBSan: selected undefined behavior; ordinary unsigned wrap is not universally covered.
- MSan: uninitialized-value use, subject to compatible dependency instrumentation.
- TSan: observed data races, not filesystem or transactional check/use atomicity.
- Semantic assertions: truncation, inconsistent state, unauthorized output and wrong results.
- Differential oracles: disagreements only within explicitly equivalent modes and contracts.

Inspect installed compiler/engine versions and help before selecting instrumentation.
Run incompatible sanitizer configurations separately and retain each build identity.
A crash classifier can prioritize triage; it cannot establish exploitability.
Use an actual input reducer for minimization; symbolizers only interpret diagnostic names.

## Discriminating campaign experiment

Abduction: a length-prefixed fixture accepts a body shorter than its declared length.
Strongest benign explanation: the format intentionally permits partial streaming frames.
Another rival is a harness that strips bytes or supplies an incorrect buffer size.
Deduction: under a complete-frame contract, truncation must reject without reading past input;
under an incremental contract, it must return a documented need-more-data result.

1. Freeze complete-frame mode and record its exact rejection contract.
2. Use a valid two-byte body with declared length two as the negative control.
3. Use a one-byte body with declared length two as the discriminating input.
4. Confirm input bytes and lengths at the target entry point.
5. Run a deliberately faulty local fixture to verify oracle sensitivity.
6. Compare with the guarded fixture under identical resource limits.
7. Replay the minimized failure outside persistent mode in a fresh process.
8. Record observed output and first invalid access, not just the engine's crash count.

Refute the truncation claim if the contract permits streaming and returns need-more-data.
Do not refute a candidate when instrumentation failed or the target path was never reached.

## Corpus, state and plateau diagnosis

Keep valid structured seeds and malformed error-path seeds as identifiable partitions.
Preserve seed origin and hashes; minimize corpus coverage separately from individual failures.
For persistent execution, compare repeated input orderings with fresh-process results.
Reset globals, descriptors, callbacks and input ownership; record state that cannot be reset.
Snapshot fuzzing must restore external state as well as guest memory or disclose the gap.
Compare coverage only within compatible instrumentation maps and builds.
At a plateau, check parsing gates, feature configuration, stability and oracle sensitivity.
Stop or change one search axis when the budget expires; do not silently extend the campaign.

## Detection, remediation and behavioral cases

Retain first-cause signatures and minimized cases in bounded CI regression replay.
Repair the input boundary or ownership rule; suppressing a sanitizer report is not a repair.
Replay valid neighboring inputs to detect fixes that merely reject everything.

- Confirmed synthetic defect: complete-frame fixture reads beyond a truncated body;
  valid and repaired controls pass. CONFIRMED bounds defect in that fixture.
- Benign refutation: incremental mode returns its documented need-more-data status
  without invalid access. REFUTED complete-frame defect claim for that mode.
- Insufficient evidence: the harness never reaches the body parser or calibration fails;
  the claimed resistance is NOT TESTED, control WARN, even with zero recorded crashes.

Deliver corpus/build hashes, budgets, oracle calibration, replay artifacts and uncovered paths.
Report discovery nondeterminism separately from deterministic replay of a saved input.
Source path: `Skills/fuzzing/offensive-fuzzing/SKILL.md`.

## Provenance

Methodology adapted from Claude-Red `offensive-fuzzing` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

