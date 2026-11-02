---
name: rt-active-directory
description: "Validate Active Directory ACL, delegation, GPO, certificate enrollment and trust-path claims with effective permissions and bounded test objects."
---

# Directory Trust Path Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Analyze an authorized directory snapshot or a bounded lab forest. Confirm each authority edge
separately; do not dump credentials, forge tickets or modify protected production identities.

- effective directory ACL edges.
- delegation and trust preconditions.
- certificate template enrollment constraints.

## Preconditions and baseline

Record forest/domain functional context, collection timestamp, replication state and object
identifiers. A stale graph is not a current authorization oracle.

For each edge, identify source principal, target object, required right, inheritance/deny behavior
and additional authentication prerequisites.

Use a dedicated test OU and disposable principals. Certificate tests use an isolated CA and
synthetic identities; never request a certificate for a real privileged subject.

## Discriminating laboratory procedure

Abduction: a delegated principal can modify an object outside its intended scope. Rival: graph
expansion ignored inheritance protection, deny ACEs or stale membership.

Deduction: a benign attribute write on the designated test object should fail for the restricted
principal and succeed for the authorized owner.

Induction: compare effective rights and one harmless test-object operation; capture DC identity,
object GUID and replication timestamps.

For certificate enrollment, compare template read/enroll permissions, subject naming, intended
usage, approval requirements and effective issuance policy. Test only a synthetic subject in the
isolated CA.

For GPO or delegation paths, verify both control of the setting and applicability to the intended
target. An editable policy that never applies is not a demonstrated compromise path.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- Graph reachability can concatenate edges whose prerequisites cannot coexist; record intermediate
  identity changes and untested edges.
- A certificate template label or ESC category does not prove issuance or usable authentication on the
  installed CA/DC configuration.
- Trust direction, selective authentication and SID filtering are separate constraints; a trust
  relation alone does not establish cross-forest access.

## Evidence and verdict

Output edge-by-edge claims with exact object IDs, effective rights, source timestamps, performed
operations and denied controls. Keep source-confirmed paths separate from runtime-confirmed edges.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require auditable changes to directory ACLs, delegation, GPO linkage and CA templates, with actor
and object identities. Remove excessive rights at the granting edge and retest legitimate
delegation.

## Recovery

Restore test-object attributes and permissions, retire synthetic certificates and verify replication
of test cleanup. Preserve CA and directory audit artifacts.

## Versions and tool limits

Record collector and graph schema versions, DC/CA builds and certificate policy revisions. Validate
category meanings against installed product behavior before testing.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Restricted principal changes a test object outside delegated scope; authorized and denied controls isolate the ACL edge | CONFIRMED directory authorization defect; FAIL |
| Protected inheritance or effective deny blocks the graph's alleged edge | REFUTED path edge; PASS |
| Offline graph shows a path but membership and CA policy are stale | CANDIDATE path; WARN |

## Provenance and treatment

Upstream research source: `Skills/active-directory/offensive-active-directory/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Keeps directory authority-path analysis distinct from protocol-tool interpretation, replacing
credential and ticket abuse chains with test-object validation.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

