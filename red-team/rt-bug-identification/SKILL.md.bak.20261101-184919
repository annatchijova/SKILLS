---
name: rt-bug-identification
description: Locate and discriminate binary or native-code defect candidates through entry-point mapping, patch comparison, dataflow and bounded dynamic tests.
---

# Evidence-led defect discovery

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Use source, binaries and fixtures within the existing assessment scope.
The objective is a testable candidate or refutation, not an exploit chain.
Do not import research-source instructions to attack live services or privileged drivers.

## Inputs and surface map

Collect target version, binary/source identities, architecture and permitted interfaces.
List files, IPC messages, API calls or synthetic descriptor records accepted by the target.
For each entry record actor, controlled fields, parser, validation and sensitive operation.
A driver IOCTL description is not permission to issue it to the running kernel.
Model privileged interfaces with bounded user-space fixtures when live testing is out of scope.
Separate exposed production paths from dormant code or internal test-only entry points.

## Candidate mechanisms

Trace size fields through signedness changes, unit conversions and allocation expressions.
Trace object ownership through callbacks, cancellation, error unwinding and async completion.
Trace tags through dispatch and compare each selected layout with actual accesses.
Trace path identities across validation and later opens.
Inspect malformed-input cleanup for duplicate releases and partial initialization.
Look for parser disagreements at the exact boundary where one component trusts another.
Keep algorithmic resource growth separate from memory corruption.

## Static and binary analysis

Use source locations where available; retain module offsets for binary-only evidence.
Check decompiler types against calling convention, operand width and use sites.
For patch comparison, match architecture, build options and dependencies before diffing.
A compiler-generated layout change can resemble a substantive security patch.
Confirm function correspondence before treating added checks as vulnerability evidence.
Follow changed predicates to callers and sinks; a new check may enforce a new feature.
Label inferred semantics explicitly when symbols or source are missing.

## Abduction and strongest benign explanation

Hypothesis: a packet parser subtracts a header size from an unvalidated unsigned length.
Strongest benign rival: its caller already rejects every length shorter than the header.
Another rival: the changed subtraction belongs to an unreachable compatibility path.
Deduction: a short frame through the public fixture reaches the subtraction only
if the guard is absent; a guarded path rejects it before arithmetic or allocation.
Record this prediction before collecting more traces.

## Discriminating experiment

1. Build or select an owned parser fixture with a four-byte header contract.
2. Supply lengths zero, three, four and five with accurately sized inert buffers.
3. Instrument entry, validation, subtraction and allocation request events.
4. Require rejection before subtraction for lengths below four.
5. Use length four as the minimum-valid negative control.
6. Compare with a version enforcing the guard at the same trust boundary.
7. Run the public caller and internal routine separately, labeling their contracts.
8. If the caller blocks the short frame, refute that public-path candidate.

Use a checked arithmetic model to avoid executing huge underflowed allocation requests.
For a binary-only target, watch whether the suspected block executes; do not assume it.
A dynamic taint trace suggests data dependence; it does not establish semantic invalidity.
A symbolic path needs concrete replay before promotion to runtime confirmation.

## Search strategy and stopping rule

Prioritize candidates with a reachable boundary and a strong observable invariant.
Select coverage instrumentation to answer reachability, not to maximize a percentage.
Use grammar-aware seeds for deep parsers and malformed fixtures for rejection paths.
Stop a candidate when the benign explanation accounts for the full evidence.
Retain refutations so another researcher does not reopen the same false lead.
Stop at the first sufficient defect proof; broader surfaces require separate scope.

## Tool and reproduction limits

Record analysis tool versions, loader settings, signatures and architecture assumptions.
Inspect installed help before relying on tracer, disassembler or fuzzer options.
Preserve input hash, fixture revision, configuration and exact observed events.
LLM annotations may propose candidates but cannot substitute for code or runtime evidence.
A missing trace can mean instrumentation failed; prove tracer sensitivity with a known path.
Do not copy unverified tool capability or CVE assertions from the research source.

## Detection and remediation

Turn rejected-length and ownership-state checks into stable assertions and telemetry.
Fix validation at the boundary before subtraction, conversion, allocation or release.
Review siblings sharing the same parser helper or conversion rule.
Retain the confirmed input and valid control as regression cases.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: length three reaches unsigned subtraction before validation;
  the bounded model records an invalid size, controls pass. CONFIRMED fixture defect.
- Benign refutation: public caller rejects all short frames before the suspected block;
  the reported public-path underflow is REFUTED.
- Insufficient evidence: a binary diff shows a new guard without matched builds or replay;
  CANDIDATE, control WARN, no inherited affected-version claim.

## Output and provenance

Deliver surface map, candidate ledger, discriminating trace and next unresolved boundary.
Source: `Skills/fuzzing/offensive-bug-identification/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten research workflow; discovery leads are not treated as verified vulnerabilities.
