---
name: rt-rce
description: "Assess whether application-controlled data reaches command, interpreter or dynamic-code boundaries using inert arguments and instrumented lab sinks."
---

# Execution Boundary Instrumentation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Establish the exact execution boundary and its reachable input. Route template and deserialization details to their dedicated skills. Do not construct shell commands, reverse shells or persistence.

Use a disposable worker with no secrets, denied egress and an owner-approved inert execution recorder. Record the deployed runtime, process API, privilege context and permitted input grammar.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace the input through validation, concatenation, argument construction, shell selection and child-process launch. Include file converters or dynamic evaluation only where the live call graph proves reachability.

**Firstness:** Record the actual API invoked, executable identity, argument vector and which fields are user-controlled. Compare with the intended fixed executable and structured argument contract.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A data field controls executable selection, option interpretation or interpreter source instead of remaining a literal argument.

**Competing benign explanation:** A structured process API may preserve metacharacters as inert data, or a fixed allowlist may select a safe operation before execution. A delayed response may be a slow converter rather than code evaluation.

## Deduction and controls

A harmless sentinel remains one literal argument under a safe path; a violated boundary changes the selected operation or recorded parse structure in the real execution adapter.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Capture a normal conversion or command-backed action in the lab using a fixed harmless worker and known fixture input.

2. Trace the released adapter with an inert owner-provided argument-boundary fixture; inspect invocation structure without executing generated commands.

3. Compare with the same fixture passed through the structured-argument control path.

4. If dynamic evaluation is present, use the runtime's debugger or audit hooks to observe source/data separation with a constant-only fixture.

5. Stop after identifying the boundary failure; document any recorder substitution and verify the worker leaves no test processes or files.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

A recorder proves adapter behavior, not arbitrary code execution on the deployed target. Argument injection can matter without a shell. Scanner CVE matches, generic callbacks and timing changes do not establish command execution.

## Evidence and deliverable

Provide input-to-sink trace, runtime/version, adapter settings, controlled fields, recorded invocation and privilege boundary. Distinguish source fact, instrumented lab observation and actual execution evidence.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Shell semantics, escaping functions, platform process APIs and converter capabilities differ by OS and version. Verify the actual adapter rather than relying on historical CVE payloads or a tool's exploit module.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Remove dynamic evaluation of untrusted data, use fixed executables and structured arguments, reject unsupported options and isolate converters. Limit worker privileges and network access independently of input validation.

Capture unexpected executable or child-process changes from application workers, blocked option selection and dynamic-evaluation events. Validate detection with the fixed harmless worker.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A fixture changes the selected executable in the actual adapter trace despite a fixed-command contract: CONFIRMED for execution-boundary control; FAIL; arbitrary RCE not claimed. |
| Benign refutation | The suspect string remains one literal argument and cannot select a new operation: REFUTED for shell interpretation on that path; PASS. |
| Insufficient evidence | Only a CVE banner match or response delay exists: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-rce/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves command, evaluator and processor boundary analysis while removing command payloads, shell chains, secret access and persistence.

