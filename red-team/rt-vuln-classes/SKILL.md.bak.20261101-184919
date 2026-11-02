---
name: rt-vuln-classes
description: Diagnose competing native vulnerability classes using object bounds, lifetime, arithmetic, parser semantics and concurrency evidence rather than crash labels.
---

# Differential vulnerability classification

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Use this skill when several defect classes could explain the same observation.
Classify the first violated invariant separately from downstream effects and impact.
A class name, CWE suggestion or historical CVE resemblance is not confirmation.

## Inputs and baseline

Collect the raw observation, matching build, controlled input and interface contract.
Obtain object extent, allocation lifetime, integer types and operation order where relevant.
For binary-only evidence, mark uncertain types and reconstructed layouts explicitly.
For kernel/driver observations, require interface and privilege context; use supplied artifacts.
Do not execute unknown reproducers or build privileged test payloads to fill evidence gaps.
Define which evidence would discriminate the two leading explanations.

## Differential table

| Candidate pair | Discriminating evidence | Common misclassification |
|---|---|---|
| Bounds error / use after free | Object alive at access, offset and width | Calling every bad address a heap overflow |
| Double free / stale access | Second release versus dereference event | Grouping every allocator abort as one cause |
| Integer truncation / bounds omission | First conversion and resulting capacity | Blaming the final copy only |
| Type confusion / lifetime error | Valid live object with wrong layout versus dead object | Trusting decompiler type names |
| Uninitialized read / out-of-bounds read | Initializedness and access extent | Equating all leaked-looking bytes |
| TOCTOU / ordinary stale snapshot | Required policy version and checked/used identity | Assuming all change between reads is forbidden |
| Parser differential / allowed ambiguity | Shared specification and mode | Treating any disagreement as a defect |
| Resource exhaustion / infinite loop | Input-size growth and progress under budget | Calling every timeout a deadlock |
| Checked panic / memory corruption | Runtime guard and invalid access evidence | Treating Rust/Go panic as arbitrary memory access |

A format-string defect requires data to control interpretation, not merely contain percent signs.
A null dereference establishes a faulting access; availability impact depends on containment.
A read beyond bounds is not confirmed disclosure until unintended bytes cross an output boundary.
Use inert sentinel data for any disclosure test, never unrelated process secrets.

## Mechanism and preconditions

Memory safety concerns spatial bounds, lifetime, initialization and type-compatible access.
Integer arithmetic becomes a defect when it violates a size, count or range contract.
Unsigned wrap is defined arithmetic but can invalidate allocation assumptions.
Signed overflow in C/C++ is undefined; do not infer a portable wrapped result.
Concurrent memory races differ from application-level ordering defects.
An authorization flaw requires a prohibited actor/resource/action outcome.
A valid boot or driver signature alone does not establish the correctness of runtime behavior.

## Abduction and strongest benign explanation

Hypothesis: an invalid heap read is use after free rather than an out-of-bounds read.
Strongest benign rival: the object remains live and the reported address is a valid field;
stale symbols or a mismatched layout made it appear invalid.
A competing defect hypothesis is a live-object bounds error.
Deduction: allocation generation and release ordering distinguish lifetime from spatial faults.
Predict whether the accessed byte belongs to a live object before replay.

## Discriminating experiment

1. Use a synthetic object with recorded allocation ID, generation and capacity.
2. Record every release and access, including offset and width.
3. Run a live, in-bounds read as the negative control.
4. Run a known released-object read as the lifetime sensitivity fixture.
5. Run a separate live-object boundary violation as the spatial sensitivity fixture.
6. Compare the unknown fixture's first invalid event against both patterns.
7. Replay a repaired ownership or bounds implementation with the same logical input.
8. Report compound defects in order if both lifetime and size invariants fail.

For arithmetic-to-bounds chains, identify the first invalid size computation as root cause.
For a parser disagreement, constrain modes before declaring one implementation wrong.
For resource defects, measure several bounded input sizes with warm-up separated.
A finite sample of growth rates does not prove asymptotic complexity.

## Reproducibility and tool limits

Preserve raw sanitizer output, input hashes, build flags and allocation histories.
Check tool version and supported instrumentation before relying on a class label.
ASan and MSan observe different properties; one clean run does not substitute for the other.
Custom allocators and uninstrumented modules can hide relevant events.
Race instrumentation changes scheduling and does not prove absence of all interleavings.
Do not use a severity score to resolve uncertain root cause.

## Detection and remediation

Choose detection by invariant: lifetime tracking, checked arithmetic or policy-state assertions.
Repair the earliest violated contract and verify downstream behavior afterward.
Bounds fixes should cover unit conversions and termination, not only one input length.
Lifetime fixes must address all owners and aliases; parser fixes must preserve valid semantics.
Retain classification controls so future tool changes cannot silently relabel failures.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: a read follows release of the same allocation generation;
  live control passes and ownership repair passes. CONFIRMED lifetime defect.
- Benign refutation: matching layout proves a live in-bounds initialized read;
  stale-symbol interpretation caused the allegation. REFUTED memory-defect claim.
- Insufficient evidence: only a terminal allocator abort is available, without history;
  CANDIDATE with class unresolved and control WARN, not confirmed exploitability.

## Output and provenance

Deliver root-cause class, competing classes, decisive evidence and independently bounded impact.
Source: `Skills/fuzzing/offensive-vuln-classes/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten taxonomy; historical CVE narratives and severity estimates are not adopted as facts.
