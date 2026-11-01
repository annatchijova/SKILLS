---
name: rt-crash-analysis
description: Diagnose native crashes and hangs from matching binaries, dumps and reproducers; separate first corruption, detection site, harness failure and demonstrated impact.
---

# Crash analysis with bounded conclusions

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Use supplied dumps or authorized isolated fixtures; preserve originals by digest.
A crash is a lead. Automated exploitability labels are tool output, not a verdict.
Do not turn register corruption into payload construction or a mitigation-bypass exercise.

## Intake and observation

Collect binary build ID, loaded module identities, symbols, dump and exact input.
Record OS, architecture, runtime libraries, compiler flags and relevant environment.
Preserve exit signal or exception code, fault address, access type and thread state.
Distinguish access violation, assertion abort, sanitizer abort, timeout and OOM kill.
A connection closing is not evidence that the server process crashed.
A core dump can contain secrets; keep it in the authorized evidence store.

## Baseline and preconditions

A replay must match the failing build, entry point, arguments and input framing.
Confirm the harness passes the actual buffer size and obeys the ownership contract.
Check symbol build IDs before interpreting function names or source locations.
For stripped binaries, retain module-relative offsets and confidence in disassembly.
For hangs, define a wall-time budget and expected progress counter before testing.
Separate cold initialization time from steady-state parser work.

## Mechanism-directed analysis

| Observation | Candidate | Evidence needed |
|---|---|---|
| Access beyond live allocation | Spatial bounds error | Allocation size, access width, offset |
| Access to released object | Lifetime error | Allocation/free/access stacks and generation |
| Abort in allocator | Earlier corruption or duplicate release | Earliest violating event |
| Very large allocation request | Arithmetic or legitimate workload | Original operands and conversion chain |
| Rust/Go bounds panic | Checked rejection or availability defect | Request boundary and exception handling |
| Timeout without progress | Deadlock or infinite traversal | All-thread stacks and stable wait relation |

Do not cluster solely by the final faulting instruction.
Keep provisional buckets by build, operation and first relevant target frame.
Merge only when the same violated invariant explains the minimized inputs.
Do not discard different allocation histories because their terminal stacks match.

## Abduction, refutation and discriminator

Hypothesis: a parser writes one byte past a heap object and crashes later during release.
Strongest benign rival: the dump uses stale symbols or the harness frees the object twice.
Deduction: matching instrumentation should stop at the parser write before release.
A harness-only duplicate release should instead reproduce with a stub parser.
Read the allocation/copy/free paths and verify symbol identity before assigning blame.

1. Replay the original input against the matching synthetic build.
2. Capture the earliest sanitizer error and its allocation history.
3. Run a valid neighboring-length input through the same harness.
4. Replace only the parser with a contract-preserving stub as a harness control.
5. Compare with a repaired bounds-check build, keeping all other settings fixed.
6. Minimize while preserving the same access site and violation, not merely any crash.
7. Replay in a fresh process; record successes and failures as integer counts.

A failure to reproduce does not refute an intermittent bug unless the test covers its trigger.
For hangs, compare progress and wait graphs under identical inputs and resource budgets.
Stop after the minimal demonstrated effect; no control-flow redirection is necessary.

## Tools and fidelity limits

Use installed GDB/LLDB/WinDbg capabilities after checking version and command help.
Read registers, mappings, disassembly and all-thread stacks without modifying execution.
CASR and similar classifiers can prioritize review but cannot confirm impact.
ASan red zones and Windows PageHeap can move the failure earlier and change layout.
Record those accommodations; do not compare their addresses as if layouts were identical.
MSan needs compatible instrumentation; missing coverage weakens a negative result.
Race detectors observe executions, not every possible schedule.
A symbolizer demangles names; it does not minimize input files.

## Detection and remediation

Retain root-cause buckets and sanitized crash signatures in regression monitoring.
Alert on recurrence by build and invariant, not on raw address equality.
Repair the first bad access, lifetime transfer or arithmetic precondition.
Keep the original reproducer and valid control to verify rejection remains correct.
Treat telemetry suppression or catching a signal as containment, not a memory-safety fix.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: matching ASan build identifies a one-byte parser overflow;
  valid input and repaired build pass, stub harness passes. CONFIRMED spatial defect.
- Benign refutation: a stale symbol file caused the alleged parser frame;
  matching replay shows deliberate invalid-input rejection without bad access. REFUTED claim.
- Insufficient evidence: an unsymbolized dump lacks binary and input identity;
  preserve a CANDIDATE with control WARN, rather than asserting code execution.

## Output and provenance

Deliver a crash card with artifact hashes, first cause versus detection site, replay and controls.
Include observed impact, recurrence count, alternative causes and missing instrumentation.
Source: `Skills/exploit-dev/offensive-crash-analysis/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten research methodology; upstream severity labels and exploit steps are not inherited.
