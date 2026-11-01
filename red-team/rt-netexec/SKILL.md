---
name: rt-netexec
description: "Interpret and bound NetExec protocol assessments using installed help, dedicated identities and independently verified read-only results."
---

# NetExec Result Verification

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Review supplied NetExec output or run an explicitly scoped read-only protocol check. The tool name
or a success banner never expands permission to enumerate secrets or execute remotely.

- protocol-specific result semantics.
- authentication versus authorization.
- module side-effect review.

## Preconditions and baseline

Record the installed NetExec version, protocol plugin and module version. Read local help before
selecting options; do not transplant upstream command lines.

Inspect module behavior before use, including remote writes, authentication attempts and stored
output. Exclude secret collection, remote execution and broad target expansion.

Choose one owned endpoint, a known valid dedicated account and a harmless dummy resource. Set a
strict attempt budget and protect credentials from command history and logs.

## Discriminating laboratory procedure

Abduction: the tool reports administrative access even though the claimed operation is denied.
Rival: the label reflects a narrower protocol-specific capability rather than arbitrary
administration.

Deduction: a read-only operation on the dummy resource should independently establish the actual
capability; an explicitly denied identity should fail the same operation.

Induction: capture the minimal protocol check, its raw status and endpoint audit record. Use the
native service client for the same harmless request as the independent control.

Resolve local-versus-domain identity, target hostname and authentication method before interpreting
a result. Do not retry with harvested hashes or tickets.

If a module's effects cannot be determined from its installed source/help, omit it and mark that
capability NOT TESTED.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- Color, a success banner or a tool exit code may indicate transport or authentication success only.
- Name resolution, Kerberos service naming, clock skew and account lockout can cause failure unrelated
  to authorization.
- A version-dependent module may change behavior or default collection. Treat output databases as
  sensitive and export only necessary redacted facts.

## Evidence and verdict

Provide tool/plugin versions, reviewed operation, target identity, actor scope, raw status,
native-client comparison and server event correlation. State exactly which capability was verified.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require protocol authentication and resource-access logs to match the test account and endpoint. Fix
excessive service permissions; address tool interpretation errors separately from target defects.

## Recovery

Close test sessions and remove only documented test artifacts. Verify that no module wrote remote
services, files or jobs; retain redacted output and its digest.

## Versions and tool limits

No command or option is asserted current by this document. Local help and installed module source
are the authority for the selected release; historical CrackMapExec semantics may differ.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Tool and native client both read a forbidden dummy resource as the restricted test identity | CONFIRMED resource authorization failure; FAIL |
| Banner suggests administration but the documented narrow check succeeds while the protected action is denied | REFUTED broad-admin claim; PASS for protected action |
| Only a colored success screenshot is provided | CANDIDATE capability; WARN |

## Provenance and treatment

Upstream research source: `Skills/active-directory/offensive-netexec/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Preserves tool-specific interpretation as a separate skill; removes spraying, dumping and chained
execution while requiring version verification.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

