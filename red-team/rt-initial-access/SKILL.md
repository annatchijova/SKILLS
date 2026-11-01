---
name: rt-initial-access
description: "Validate mail, download and remote-access ingress controls with inert files and dedicated accounts, distinguishing delivery from execution and authorization."
---

# Ingress Control Validation

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Test one ingress boundary at a time: mail to endpoint, browser download to application, or dedicated
user to a remote-access service. Do not infer code execution from delivery.

- download-origin metadata propagation.
- attachment handling and application policy.
- remote-access authentication gates.

## Preconditions and baseline

Define the expected treatment of an inert attachment or download, including quarantine, origin
metadata and application restrictions.

Choose an owned mailbox, an owned download endpoint or an isolated remote-access tenant. All fixture
files contain public dummy text.

Capture the effective client and gateway policies. Administrative delivery exemptions must be
explicit because they change the tested boundary.

## Discriminating laboratory procedure

Abduction: origin classification is lost during an approved file workflow. Rival: the file came from
a trusted internal source or the receiving filesystem cannot represent that metadata.

Deduction: matched inert files arriving through external and internal lab routes should retain
distinguishable origin classification when policy requires it.

Induction: transfer the paired fixtures through the actual mail/download client, inspect their
recorded metadata, and capture the gateway disposition.

Exercise application policy only with a harmless vendor test artifact; record whether opening,
execution or child-process creation is the actual tested action.

For remote access, compare one permitted and one disallowed dedicated account with valid test
credentials. A failed transport handshake is not an authorization result.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- Mail scanners may open links automatically; a landing-page hit does not demonstrate a user action.
- Archive extraction, copying and filesystem changes can alter metadata independently of a security
  defect; isolate each transformation.
- A gateway exception, audit-only rule or unsupported client can explain delivery. Report the
  effective configuration before alleging a bypass.

## Evidence and verdict

Provide the ingress route, fixture digests, client policy, pre/post metadata, gateway decision and
endpoint event. Keep delivery, opening, execution and access outcomes separate.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require provenance and disposition visibility across gateway and endpoint. Remediate missing origin
propagation or policy coverage, then retest the same transformation and a sibling supported client.

## Recovery

Delete only test inbox items and fixture files, revoke dedicated sessions and verify any temporary
routing exception has been removed.

## Versions and tool limits

Record browser, mail client, archive handler, filesystem, remote-access service and gateway builds.
Do not inherit historical claims about file formats or default policies.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| External fixture loses required origin metadata only at the supported extraction step; internal control remains distinguishable | CONFIRMED provenance gap; FAIL |
| Policy explicitly trusts the internal route and external fixture remains restricted | REFUTED bypass hypothesis; PASS |
| Gateway delivered the fixture but no endpoint evidence was collected | CANDIDATE downstream exposure; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-initial-access/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Preserves ingress-chain reasoning while replacing infection chains, credential stuffing and
weaponized documents with inert probes.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

