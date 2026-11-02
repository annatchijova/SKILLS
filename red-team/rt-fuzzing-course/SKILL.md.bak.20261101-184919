---
name: rt-fuzzing-course
description: Teach reproducible fuzzing through graded parser, semantic-oracle and stateful-harness labs with controls, minimization and evidence-based graduation.
---

# Fuzzing course with measurable learning gates

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Use synthetic parsers and local state machines with explicit contracts.
Course success means the learner can explain what the search tested and could detect.
Do not grade by crash count, tool count or claims of exploitability.

## Inputs and preparation

Collect learner language experience, available compiler, engine and sanitizer support.
Require fixture source, expected semantics, baseline seeds and a reproducible build.
Set maximum input length, memory, executions and wall time for every lab.
Keep target execution offline unless the authorized exercise requires local transport.
Use local pinned dependencies; source setup scripts are research examples, not instructions.
Record unavailable tools as skipped capabilities rather than silently changing the exercise.

## Lab 1: oracle calibration

Use a tiny length-prefixed parser with an explicit truncated-input rejection rule.
Write the invariant before choosing mutation settings.
Provide a deliberately faulty fixture and a corrected fixture.
Run a known violating input and a valid minimum-length input.
Graduation evidence: the oracle fires on the faulty fixture and accepts the valid control.
A live process or zero exit code alone cannot establish semantic correctness.

## Lab 2: coverage-guided byte search

Choose AFL++, libFuzzer or Honggfuzz based on the actual supported harness interface.
Seed valid headers, empty bodies, maximum permitted lengths and malformed truncations.
Compare rejection counts with coverage of the body parser.
Preserve corpus hashes and a record of the exact build used for coverage.
Graduation evidence: explain whether a plateau is a gate, a harness bug or exhausted search.
Do not compensate for an unreachable entry point by simply adding workers.

## Lab 3: structured and semantic generation

Generate a typed record with length and body, then serialize it consistently.
Reserve a separate malformed partition that deliberately breaks their relation.
For a lossless codec, assert decode(encode(record)) equals the original record.
For canonicalization, define the normalization equivalence before comparing outputs.
Differential implementations must promise the same semantics on the tested domain.
Graduation evidence: one meaningful semantic failure or one correctly explained disagreement.
A serializer and parser sharing the same bug can pass a round-trip test; add an independent check.

## Lab 4: stateful harness discipline

Model create, append, close and invalid-after-close operations as a sequence.
Assert resource count and allowed state after each transition.
Compare a fresh process with repeated persistent iterations using the same input sequence.
Reset globals, callbacks, file positions and allocator-owned objects between test cases.
Graduation evidence: demonstrate whether a failure belongs to the target or leaked harness state.
Do not discard stateful reproducers merely because a single isolated input does not fail.

## Lab 5: triage and shrinking

Preserve the original failing artifact before minimization.
Shrink while keeping the same violated invariant and first relevant operation.
Separate input minimization from corpus reduction for coverage.
Cluster by mechanism and lifetime history, not only terminal stack hash.
Replay a minimized artifact outside the search loop in a fresh process.
Graduation evidence: a compact reproducer, negative control and bounded impact statement.

## Lab 6: repair and bounded continuous testing

Turn the minimized case into a regression with an exact expected result.
Test the repaired fixture and neighboring valid cases.
Define a short CI replay suite separately from scheduled exploratory search.
Record timeouts and OOM events separately from sanitizer failures.
Kernel fuzzing is optional and requires a disposable VM plus separately defined scope.
A user-space course does not imply authorization to fuzz the host kernel.

## Abduction and strongest benign explanation

Hypothesis: duplicate fields cause the target to emit inconsistent parsed values.
Benign rival: the documented format permits last-field-wins behavior.
Deduction: only disagreement with the selected contract is a defect;
two conforming parsers using different supported modes do not prove a vulnerability.
Require the learner to freeze mode and duplicate-field semantics before replay.
Use single-field input and a deliberately faulty parser as negative and sensitivity controls.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: a fixture promising duplicate rejection instead accepts
  duplicates; single-field and repaired controls pass. CONFIRMED contract defect.
- Benign refutation: last-field-wins is documented and observed consistently;
  the duplicate-acceptance finding is REFUTED.
- Insufficient evidence: a million executions occurred without a sensitivity control
  or evidence of body-parser reachability. Detection claim NOT TESTED, control WARN.

## Reproducibility, detection and remediation

Pin engine/compiler/runtime versions and inspect their installed help before invocation.
Retain seed, corpus digest, harness revision, flags, oracle configuration and raw output.
Scheduling can alter search results; replay artifacts matters more than identical discovery order.
Sanitizers detect selected classes and do not establish universal memory safety.
Use invariant telemetry and regression replay to detect recurrence after repair.
Repair parser contracts or state reset at their owning boundary, not by suppressing errors.

## Output and provenance

Deliver lab sequence, graduation evidence, replay bundle and explicit skipped capabilities.
Source: `Skills/fuzzing/offensive-fuzzing-course/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten learning path; no upstream installation, platform or exploitability claim is inherited.
