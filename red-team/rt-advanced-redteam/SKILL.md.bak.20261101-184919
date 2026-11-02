---
name: rt-advanced-redteam
description: "Design bounded adversary-emulation exercises with evidence-linked objectives, deconfliction, stage gates and verified restoration."
---

# Adversary Exercise Coordination

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Coordinate a multi-stage exercise whose result is measured control behavior. Domain-specific
execution belongs to separate skills; this skill establishes whether the combined exercise can
support its conclusions.

- objective-to-control dependency graph.
- deconfliction and abort handling.
- stage-specific evidence custody.

## Preconditions and baseline

Name the protected business operation and the smallest synthetic outcome that represents failure,
such as a dummy invoice crossing a test approval boundary.

Build a dependency graph of identity, ingress, endpoint, egress and response stages. Mark each edge
as observed, assumed or untested.

Separate exercise administrators from simulated actors. Emergency access is available for recovery
but cannot count as evidence of an attacker capability.

## Discriminating laboratory procedure

Abduction: a response handoff fails because the receiving team cannot correlate an endpoint event to
the business operation. Rival: delivery delay or an incorrect exercise identifier explains the
missing response.

Deduction: the same marked event, with and without the required correlation field, should differ in
case linkage while remaining visible in the source collector.

Induction: replay one benign stage event into the lab incident workflow; capture source receipt,
alert creation, case assignment and acknowledgment timestamps.

Run a positive harness control with a previously validated event. Stop at the first failed
dependency; do not label downstream stages tested.

Exercise the stop channel once before execution. The owner must demonstrate cancellation of queued
test work without deleting the evidence ledger.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- A successful final marker does not validate intermediate detection stages; administrative fixture
  setup can accidentally grant the simulated actor additional rights.
- Preannounced tests and unannounced tests measure different response conditions. Keep them in
  separate cohorts.
- A containment action that disrupts an unrelated service exceeds the experiment; stop and preserve
  the partial record.

## Evidence and verdict

Deliver the dependency graph, action ledger, stage markers, actual response timestamps,
authorization boundary, restoration inventory and unresolved edges. Report coverage by stage,
without a blended success score.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require marker-to-case correlation across the relevant collectors and a response owner for each
stage. Fix missing routing or context propagation before increasing exercise complexity.

## Recovery

Revoke only exercise identities, cancel only test jobs and compare the fixture inventory with its
baseline. Preserve the ledger outside the disposable environment.

## Versions and tool limits

Record orchestrator, SIEM connector and endpoint-agent builds; event schemas and automation behavior
vary by integration version.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| A known-good event arrives, but the same event without a required join key never reaches its assigned queue | CONFIRMED routing gap; FAIL |
| Both variants are correlated after the documented ingestion interval | REFUTED routing-gap hypothesis; PASS for tested routing |
| Only the final dummy invoice exists; intermediate actions have no ledger | CANDIDATE chain explanation; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-advanced-redteam/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Retains engagement engineering as a distinct scope; replaces covert infrastructure and chained
compromise with observable, reversible exercises.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

