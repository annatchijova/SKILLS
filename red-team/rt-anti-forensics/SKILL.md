---
name: rt-anti-forensics
description: "Test forensic pipeline integrity, timeline reconciliation and recovery using altered copies of synthetic evidence while preserving originals."
---

# Forensic Evidence Resilience

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Evaluate whether investigators can detect missing or inconsistent evidence. Work on synthetic
exports and disposable copies; never clear real logs, erase artifacts or patch telemetry providers.

- event-gap and custody checks.
- cross-source timeline reconciliation.
- backup and retention recovery.

## Preconditions and baseline

Create an immutable baseline of synthetic events with sequence identifiers, timestamps and source
digests. Preserve acquisition metadata separately.

Select independent corroborating sources: host events, collector receipt times, file metadata or
network flow records.

Define expected retention, rotation, time synchronization and collection delays before labeling a
gap suspicious.

## Discriminating laboratory procedure

Abduction: a missing event or inconsistent timestamp is being silently accepted as complete
evidence. Rival: normal rotation, clock offset or parser normalization explains the discrepancy.

Deduction: the verifier should flag a copy with one deliberately omitted synthetic event while
accepting the intact baseline and a documented rotation fixture.

Induction: ingest the controlled copies into an isolated analysis pipeline; compare gap detection,
coverage warnings and evidence references.

Use a separate synthetic timestamp-disagreement fixture to test reconciliation across independent
sources. Do not change actual filesystem timestamps to conceal activity.

Restore the missing fixture event from the preserved backup and verify digest and sequence
continuity; restoration must not silently overwrite the original observation.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- A valid hash proves a file has not changed since hashing, not that acquisition was complete or
  truthful.
- Filesystem timestamps, journal records and collector timestamps have different semantics;
  disagreement alone does not prove tampering.
- A missing source must reduce the claimed reconstruction coverage. Do not fill gaps with inferred
  events presented as observed facts.

## Evidence and verdict

Output baseline and test-copy digests, transformation ledger, parser versions, sequence gaps, clock
uncertainty and recovery results. Preserve original and reconstructed timelines as separate
artifacts.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require explicit incomplete-evidence warnings, remote retention and independently protected custody
records. Improve collection redundancy and restore testing rather than relying only on local logs.

## Recovery

Discard disposable test copies only after preserving results. Verify original evidence hashes and
recovery-store access; no live audit record is removed.

## Versions and tool limits

Record filesystem/export format, event schema, parser and backup tool versions. NTFS journal, ADS
and Linux journal availability vary by acquisition method.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| A deliberately incomplete synthetic export passes the pipeline as complete while intact control parses | CONFIRMED evidence-integrity validation gap; FAIL |
| Documented rotation fully explains the gap and continuity is recovered from the archive | REFUTED tampering inference; PASS |
| Only one mutable log exists and acquisition completeness is unknown | CANDIDATE gap; WARN |

## Provenance and treatment

Upstream research source: `Skills/forensics/offensive-anti-forensics/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Reverses evidence-destruction guidance into tamper detection and recovery testing, keeping
filesystem and telemetry distinctions.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

