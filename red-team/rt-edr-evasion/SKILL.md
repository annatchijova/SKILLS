---
name: rt-edr-evasion
description: "Measure endpoint prevention, telemetry continuity and alerting using benign vendor-supported tests without implementing evasion or disabling sensors."
---

# Endpoint Telemetry Resilience

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Evaluate the observable coverage of a specified EDR deployment. Do not construct bypasses, patch
AMSI or ETW, load vulnerable drivers or alter security-agent protections.

- sensor-to-collector continuity.
- process and image telemetry correlation.
- prevention versus alert latency.

## Preconditions and baseline

Inventory the endpoint agent, kernel/user-mode sensor sources, collector route, policy assignment
and declared ingestion deadline.

Separate a prevention claim from a logging claim and an alerting claim. A blocked operation can
still be absent from the incident console.

Use an isolated test endpoint and vendor-supported harmless diagnostic events with unique
identifiers; record the exact expected event classes.

## Discriminating laboratory procedure

Abduction: a benign test action is not alerted because a collection path is broken. Rival: policy
intentionally records the action without alerting, or the action was prevented before the expected
event.

Deduction: if collection is broken, the endpoint-local event should exist while the corresponding
central record is absent after the declared deadline.

Induction: generate one benign process-start test and one known-good health event. Record local
timestamps and central ingestion identifiers.

Repeat only the missing event using the same policy. Compare a matched healthy endpoint, accounting
for clock offset and agent version.

Use an exported synthetic missing-heartbeat fixture to test health alerting. Do not suppress a
running production sensor to manufacture the gap.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- A signature test file validates a particular scanning path, not behavioral detection or resistance
  to injection.
- An event viewer showing no events can mean auditing was never enabled; it does not prove an attacker
  blinded the sensor.
- A laboratory replay tests downstream analytics only when it bypasses the actual endpoint collector;
  state that coverage boundary.

## Evidence and verdict

Output an event-class matrix with local generation, collection, indexing, alert and response
evidence. Attach policy hashes, event markers, delay measurements and negative results.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require separate alerts for sensor-health degradation and missing expected event classes. Correct
collection, retention or rule logic at the layer where the evidence diverges.

## Recovery

Remove only harmless fixture files and return test policy assignments to the recorded baseline.
Verify the health event still reaches the collector.

## Versions and tool limits

Pin EDR engine and signature versions, Windows build, policy revision and collector parser. Consult
installed help before choosing vendor diagnostics; historical bypass claims are unverified.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Local marked process event exists; health control arrives centrally; process event misses the ingestion deadline | CONFIRMED collection gap; FAIL |
| Event is indexed and policy explicitly specifies log-only behavior | REFUTED collection-gap hypothesis; PASS for collection only |
| No local artifact and no known-good control event | CANDIDATE visibility issue; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-edr-evasion/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Transforms evasion recipes into endpoint visibility and health validation, retaining telemetry-layer
distinctions.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

