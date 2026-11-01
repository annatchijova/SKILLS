---
name: rt-linux-privesc
description: "Assess Linux sudo, capabilities, service dependencies and namespace boundaries with effective configuration and harmless lab fixtures."
---

# Linux Privilege Configuration Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Trace one low-privilege actor to one protected operation through an actual policy or service
dependency. Do not treat root inside a user namespace as host-root authority.

- sudo command and environment constraints.
- capability and namespace scope.
- privileged service dependency ownership.

## Preconditions and baseline

Record real/effective IDs, supplementary groups, user namespace mappings, mount options and relevant
LSM policy.

Inspect the effective sudo rule including command arguments, run-as identity and environment
handling; NOPASSWD alone is not an arbitrary-command grant.

For services and scheduled jobs, resolve executable/configuration dependencies and ownership. Use a
disposable non-production fixture with a fixed-marker action.

## Discriminating laboratory procedure

Abduction: a low-privilege user can alter a dependency consumed by a privileged job. Rival: the job
reads a different path, a read-only mount prevents writes or namespace mapping confines the effect.

Deduction: the actor should fail to change the protected fixture input while the maintenance
identity succeeds; the job's fixed marker should identify its actual namespace and effective UID.

Induction: verify effective write permission on the owned fixture, trigger its normal lifecycle and
record the resulting marker and authority context.

For a capabilities claim, establish executable applicability, bounding/ambient sets and namespace
scope. Use a vendor diagnostic instead of a capability-enabled shell.

For version-based candidates, check distributor package metadata and backported fixes. Kernel
exploit execution is outside this skill's proof method.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- SUID on a nosuid mount, interpreter handling and privilege-dropping behavior can refute a
  superficial scanner finding.
- Container-engine socket access requires distinguishing rootful host control from rootless or
  remotely scoped engines.
- NFS export settings require client identity mapping, mount reachability and server-side permissions;
  a configuration string alone does not prove a root path.

## Evidence and verdict

Provide effective policy excerpts, actor/namespace context, dependency paths, file and mount
permissions, LSM outcomes and the minimal fixed-marker result.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Monitor changes to privileged job dependencies, sudo policy and engine-socket access. Prefer
immutable owned dependencies, constrained delegation and least-privilege service identities.

## Recovery

Restore the fixture and revoke test-only delegation. Verify no test timer, service or mounted
resource remains and retain all privilege-transition evidence.

## Versions and tool limits

Record kernel and distribution package builds, sudo/systemd/runtime versions and security policy.
Historical CVE version ranges must account for vendor backports.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Restricted user alters an owned fixture input consumed by a host-privileged job; matched protected control denies writes | CONFIRMED privilege path; FAIL |
| Observed UID 0 is confined to a mapped namespace and the host operation is denied | REFUTED host-root claim; PASS |
| Scanner flags a SUID binary without mount or runtime context | CANDIDATE configuration exposure; WARN |

## Provenance and treatment

Upstream research source: `Skills/privesc/offensive-linux-privesc/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Retains Linux authority semantics while removing root-shell recipes, kernel exploits and credential
harvesting.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

