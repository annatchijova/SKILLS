---
name: rt-persistence
description: "Assess autostart permissions, trigger visibility and complete removal using inert lab entries and restart evidence."
---

# Autostart Control and Recovery

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Validate one autostart mechanism in a disposable host: scheduled task, service, user startup entry
or systemd timer. Review sensitive authentication/domain mechanisms through supplied artifacts only.

- trigger-action-principal relationships.
- autostart change detection.
- post-removal trigger verification.

## Preconditions and baseline

Record who can create or change the entry, which principal executes it, its trigger and every
referenced file or registry object.

Choose a harmless action that writes a fixed marker to a dedicated test directory; use a clearly
named test entry rather than a disguised system name.

Snapshot the relevant configuration and enumerate existing entries. Define removal before creating
any fixture and preserve audit records independently.

## Discriminating laboratory procedure

Abduction: a low-privilege actor can modify an entry that later runs with greater authority. Rival:
the entry executes only as the same user or the actor cannot modify the referenced action.

Deduction: the actor should fail to change the protected fixture; an authorized owner control should
be able to change it and trigger its marker.

Induction: test the effective modification permission and, only in the isolated fixture, invoke the
documented trigger. Record executing identity with the fixed marker.

Compare trigger types explicitly: logon, restart and timer expiration are different conditions. A
one-time manual run does not establish restart persistence.

Remove the fixture through its normal management interface, then repeat the trigger and verify both
entry absence and absence of a new marker.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- A residual WMI binding, task reference or enabled timer can survive deletion of the action file;
  inventory all dependent objects.
- An autostart entry is not inherently malicious; installation records and ownership may explain it.
- Successful removal without a subsequent trigger test is incomplete recovery evidence.

## Evidence and verdict

Deliver the entry definition, ownership and effective permissions, referenced-object inventory,
trigger result, executing identity and before/after restoration comparison.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require telemetry for changes to autostart configuration and referenced actions, correlated with
execution identity. Remediate writable dependencies and excessive creation rights.

## Recovery

Remove only named test-owned entries and markers. Preserve configuration snapshots and audit logs,
then validate no fixture trigger remains active.

## Versions and tool limits

Record task scheduler/systemd/service manager version, OS build and policy. Per-user services,
lingering sessions and startup timing affect conclusions.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Restricted actor changes a protected fixture action and privileged trigger records the marker | CONFIRMED privilege-bearing autostart weakness; FAIL |
| Entry is approved and runs only with the same user's permissions | REFUTED privilege-escalation claim; PASS |
| Entry exists but its trigger and execution identity were not observed | CANDIDATE persistence capability; WARN |

## Provenance and treatment

Upstream research source: `Skills/post-exploitation/offensive-persistence/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Retains persistence lifecycle and recovery coverage without installing backdoors or modifying
authentication mechanisms.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

