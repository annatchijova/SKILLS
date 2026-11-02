---
name: rt-shellcode
description: "Analyze executable-memory transitions and validate memory policy with harmless diagnostic fixtures, without constructing shellcode or loaders."
---

# Executable Memory Policy Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Assess whether a process follows its declared executable-memory policy. Inspect supplied samples
statically or use an owner-reviewed diagnostic program that never executes supplied bytes.

- memory protection transitions.
- static versus dynamic code provenance.
- architecture and policy compatibility.

## Preconditions and baseline

Identify architecture, process policy, intended dynamic-code use and the distinction between
image-backed and private memory.

Define the expected outcome for a diagnostic allocation/protection request. Separate policy denial
from subsequent execution behavior.

Use a disposable process with no network access, no remote-process handles and no ability to read
other processes.

## Discriminating laboratory procedure

Abduction: the process accepts a forbidden executable-memory transition. Rival: dynamic code is
explicitly allowed for a JIT, or the reported mapping belongs to a normal image.

Deduction: a reviewed fixture requesting the same transition under an enforced restrictive policy
should receive the documented denial; a data-only allocation should succeed.

Induction: run the vendor-supported policy diagnostic in a disposable VM and capture the API result,
effective policy and memory-map type.

Compare a documented permissive fixture process to the restrictive process with all other build
settings held constant. Do not place shellcode in either allocation.

For supplied binaries, correlate disassembly, imports and memory-region observations; static
loader-like structure remains a candidate capability until observed.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- RW-to-RX transitions are legitimate in some runtimes. Their presence alone is not maliciousness or a
  security-boundary failure.
- A failed request can reflect architecture mismatch, size constraints or resource exhaustion; the
  data-only control helps distinguish these.
- Absence of RWX regions does not prove absence of dynamically generated code, and a memory snapshot
  may miss transient states.

## Evidence and verdict

Retain architecture, compiler/runtime versions, allocation request parameters, status values, policy
state and region provenance. Bound the claim to acceptance or rejection of the tested transition.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Specify telemetry for unexpected executable private mappings in processes that prohibit dynamic
code. Remediate policy assignment and unnecessary dynamic-code exceptions without breaking required
runtimes.

## Recovery

Exit the disposable process and confirm its handles and allocations are released. Preserve test logs
before reverting the VM snapshot.

## Versions and tool limits

Verify OS policy API support and runtime behavior for the tested build. Do not carry forward PEB
offsets, syscall numbers, loader conventions or historical cross-platform claims.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Forbidden transition succeeds under verified enforced policy; data-only control succeeds | CONFIRMED policy violation; FAIL |
| Transition is permitted by a documented JIT exception | REFUTED prohibited-transition claim; PASS for stated policy |
| Static imports suggest allocation and execution but no runtime policy evidence exists | CANDIDATE capability; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-shellcode/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Retains executable-memory mechanics and evidence interpretation while excluding payload
construction, injection and stealth.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

