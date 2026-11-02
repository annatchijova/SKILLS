---
name: rt-windows-mitigations
description: "Assess effective Windows exploit-mitigation configuration and harmless diagnostic outcomes across binaries, processes and hardware."
---

# Windows Mitigation Effectiveness

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Evaluate a specific mitigation promise for a named application and Windows build. Do not equate a PE
flag, policy setting or hardware feature with runtime enforcement.

- DEP and ASLR applicability.
- CFG and shadow-stack enforcement.
- VBS and HVCI effective state.

## Preconditions and baseline

Inventory PE architecture and mitigation metadata, process policy overrides, compiler/linker
settings and loaded module compatibility.

For VBS, HVCI or hardware shadow stacks, distinguish supported, configured and running states.
Record virtualization and firmware prerequisites.

Use signed or owner-reviewed harmless diagnostic fixtures in a disposable VM. Kernel exploitation
and intentional corruption of production processes are excluded.

## Discriminating laboratory procedure

Abduction: a mitigation exception leaves the target process unprotected. Rival: the static scanner
cannot recognize the binary's metadata or the application requires a documented exception.

Deduction: the same diagnostic should show enforcement in a matched protected fixture and absence in
the exempt process, while a valid operation succeeds in both.

Induction: inspect static flags and effective process state, then run a vendor-supported diagnostic
for one selected mitigation. Record the exact termination/status evidence.

For ASLR, compare mappings across fresh processes and relevant restarts; a few differing addresses
do not establish entropy or universal coverage.

For CFG or shadow stacks, verify instrumentation and hardware prerequisites before attributing a
diagnostic failure to the mitigation. Keep data-only behavior outside the claimed coverage.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- DEP, CFG, ASLR and shadow stacks address different primitives; one does not substitute for the
  others.
- A configured VBS feature may not be running after an unsupported boot or hardware configuration.
- Diagnostic crashes may reflect a harness defect; require a normal-operation control and the
  documented mitigation-specific signal.

## Evidence and verdict

Provide configured/effective/observed columns per mitigation, binary hashes, module coverage,
hardware prerequisites, diagnostic results and explicit exceptions.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Monitor policy exceptions and unexpected loss of running protection. Remove unnecessary per-image
overrides, rebuild unsupported modules and retest the original application workflow.

## Recovery

Restore test-only policy overrides and verify effective state after any required restart. Preserve
diagnostic logs before reverting the snapshot.

## Versions and tool limits

Record Windows build, CPU features, firmware, hypervisor, compiler and diagnostic version.
Historical Windows release defaults are research leads, not current evidence.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Effective process policy excludes required protection and the controlled diagnostic corroborates the gap | CONFIRMED configuration gap; FAIL |
| PE scanner misses metadata but runtime state and diagnostic demonstrate enforcement | REFUTED missing-mitigation claim; PASS |
| Hardware support is reported but running state was not collected | CANDIDATE protection claim; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-windows-mitigations/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Retains mitigation interaction analysis as distinct from authorization boundaries; replaces bypass
chains with configuration and diagnostic comparisons.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

