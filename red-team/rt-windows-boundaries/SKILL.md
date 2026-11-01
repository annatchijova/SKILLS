---
name: rt-windows-boundaries
description: "Validate Windows token, integrity, AppContainer and broker boundaries with dummy resources and effective-access evidence."
---

# Windows Isolation Boundary Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Test a named resource boundary between a restricted actor and a privileged service or object. Keep
mitigation configuration analysis separate from proof of unauthorized access.

- token and mandatory integrity checks.
- AppContainer capabilities.
- broker authorization and effective DACLs.

## Preconditions and baseline

Capture actor SID, group attributes, integrity level, capabilities, session and impersonation state;
record the resource DACL and mandatory label.

For a brokered request, identify the client identity used by the broker and the specific
authorization check expected before access.

Use dummy files or an owned test broker. PPL and kernel isolation receive configuration review or
vendor diagnostics, not handle theft or driver exploitation.

## Discriminating laboratory procedure

Abduction: a broker grants access under its own authority without enforcing the client's
restriction. Rival: the client has an explicit capability or inherited ACE authorizing the
operation.

Deduction: a restricted client lacking the required capability should fail while the designated
permitted client succeeds against the same dummy resource.

Induction: record a direct access result and a brokered result for both actors, keeping object
identity and requested access mask constant.

Inspect effective permissions and the broker's recorded client identity. A different object path,
namespace or impersonation token invalidates the comparison.

Where mandatory integrity is relevant, vary the integrity label independently of the DACL and retain
the exact requested read/write operation.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- Integrity levels do not provide a universal read barrier; test the documented operation-specific
  policy.
- UAC consent behavior is not interchangeable with AppContainer isolation or a
  nonadministrator-to-SYSTEM boundary.
- An AppContainer capability, explicit allow ACE or approved broker capability can explain access
  without a defect.

## Evidence and verdict

Deliver actor/resource/action rows, access masks, direct versus brokered statuses, token summaries,
DACLs and labels. Redact identifiers that are not required to reproduce the boundary.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require broker logs to preserve the caller identity and authorization decision. Remediate checks at
the broker boundary, remove excessive capabilities and retest direct and brokered paths.

## Recovery

Remove only dummy objects and test broker registrations; verify original ACLs and policy hashes. Do
not alter protected process configuration as cleanup.

## Versions and tool limits

Record Windows build, broker binary digest, SDK diagnostic version and effective isolation policy.
Product security-boundary promises must be verified for that build before assigning impact.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Restricted actor is denied directly but broker grants the same forbidden operation without caller authorization | CONFIRMED broker boundary failure; FAIL |
| Effective ACL and capability explicitly permit the operation | REFUTED unauthorized-access claim; PASS |
| Token and resource identity were not captured | CANDIDATE isolation issue; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-windows-boundaries/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Separates security-boundary validation from exploit mitigation configuration; omits driver abuse and
security-sensor tampering.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

