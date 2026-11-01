---
name: rt-windows-privesc
description: "Assess Windows service, task and installer privilege paths with effective permissions and benign fixtures, without token theft or exploit payloads."
---

# Windows Privilege Configuration Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Establish whether a standard test user controls input consumed by a higher-privilege component.
Separate configuration exposure from demonstrated privileged effects.

- service DACL and dependency permissions.
- privileged action reachability.
- token privilege preconditions.

## Preconditions and baseline

Capture user token, enabled privileges, group attributes and integrity level. A privilege name alone
does not establish a usable impersonation path.

Inventory service/task principal, configuration permissions, executable path, directory ACLs and
restart/trigger permissions.

Use an isolated service fixture whose only privileged action records a fixed public marker. Do not
replace production binaries, inspect credential stores or load exploit drivers.

## Discriminating laboratory procedure

Abduction: a standard user can modify a dependency that a privileged service consumes. Rival: the
apparent writable path is not the resolved executable or the service cannot be triggered.

Deduction: the standard actor should be unable to modify the protected fixture dependency, while an
authorized maintenance actor can do so.

Induction: inspect effective ACLs for the actual resolved path and test a harmless configuration
field on the owned fixture. Record the exact denied or allowed operation.

Trigger the fixture through its approved lifecycle and record executing identity with its fixed
marker. A writable file without consumption remains a candidate path.

For unquoted paths or DLL search observations, establish actual resolution order and writable
location first. Do not plant executables or substitute libraries.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- A NAME NOT FOUND library probe does not prove a writable location will be loaded.
- An administrator using a filtered token differs from a standard user acquiring new authority; report
  the starting privilege accurately.
- Installer policy, token privileges and historical CVE names require their additional preconditions;
  scanner labels are not proof.

## Evidence and verdict

Deliver the actor-to-input-to-consumer graph, effective permission results, resolved dependency
identities, trigger evidence and observed executing principal.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require changes to privileged service/task configuration and dependencies to be attributable to an
actor. Fix ownership, narrow modification rights and remove unnecessary service-account privileges.

## Recovery

Restore only test fixture configuration and remove its marker. Verify service health and compare
pre/post ACLs; preserve audit events.

## Versions and tool limits

Record Windows build, service binary digest, tool version and policy revision. Check package
remediation rather than assuming vulnerability from OS marketing version.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Standard actor modifies an owned fixture dependency consumed under SYSTEM and controls demonstrate the path | CONFIRMED privilege configuration failure; FAIL |
| Reported writable directory is not in the actual service resolution path | REFUTED candidate path; PASS for that path |
| SeImpersonate is listed but no reachable privileged interaction is established | CANDIDATE escalation hypothesis; WARN |

## Provenance and treatment

Upstream research source: `Skills/privesc/offensive-windows-privesc/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Preserves local privilege-path analysis while replacing exploit families and secret extraction with
effective-access and controlled-service evidence.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

