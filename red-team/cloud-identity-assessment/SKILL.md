---
name: cloud-identity-assessment
description: "Red-team assessment of cloud identity and privilege boundaries across AWS, Azure and GCP: IMDS credential reach, IAM privilege-escalation paths (iam:PassRole, CreatePolicyVersion, UpdateAssumeRolePolicy and peers), cross-account/cross-tenant trust, data-store reach (S3/snapshots/secrets), and persistence primitives. Re-expressed as scoped experiments in an owned sub-account using least-privilege test principals and policy-simulation controls instead of live escalation in production."
---

# Cloud Identity and Privilege-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's cloud-attack craft as scoped experiments in an owned sub-account/tenant: it names the escalation paths, proving one against a planted test principal with policy-simulation controls rather than escalating in production or evading real detection.

## Scope and prerequisites

Cloud compromise is IAM authority analysis: from a given principal, which paths reach higher privilege, cross-account trust, or sensitive data. Use an owned sub-account/tenant/project with planted least-privilege test principals. Prove a path against a planted target; do not escalate real production identities or disable real detection.

Declare provider, account/scope, attempt budget, stop condition. Config/policy-only authorization yields a hypothesis marked NOT TESTED. Persistence and detection-evasion are impact classes to reason about and bound, not to execute in production.

## Attack surface and classes

- **IMDS/metadata** — instance/pod identity credential reach (IMDSv1 vs IMDSv2 token requirement).
- **IAM privilege escalation (AWS)** — `iam:PassRole`+`lambda:CreateFunction`/`ec2:RunInstances`, `iam:CreatePolicyVersion`+`SetDefaultPolicyVersion`, `iam:UpdateAssumeRolePolicy`, `CreateAccessKey`/`CreateLoginProfile` on others, ABAC session-tag tricks. Azure (role assignment, managed identity) and GCP (serviceAccountUser, actAs) peers.
- **Cross-account/tenant** — role trust to your account, org-wide reach.
- **Data reach** — S3, cross-region snapshot share, RDS snapshot share, Secrets Manager/Parameter Store, Azure/GCP equivalents.
- **Persistence** (impact class) — backdoor roles/keys, event-driven re-grant.

## Mechanism and observation

Pick one principal and one path; trace the permission to the privilege/data it reaches.

**Firstness:** Record the capability gained against a planted principal (assumed a higher role, read a planted secret, shared a planted snapshot). **Secondness:** State the intended boundary and the deviation. **Thirdness:** Infer the escalation class only after the path is exercised under control.

## Abduction and refutation

**Mechanism hypothesis:** A principal holds a permission (or combination) that lets it grant itself more authority, assume a trusted role, or reach data across a boundary.

**Competing benign explanation:** An SCP/permission boundary blocks the action despite the IAM grant; the role trust requires conditions the principal does not meet; IMDSv2 blocks metadata from the context; the data store denies via resource policy; policy simulation shows the action denied.

## Deduction and controls

A principal acting within its grants succeeds (positive control); the escalation path must fail if a boundary holds. A confirmed finding exercises the path against a planted principal where an SCP/boundary/condition would deny it. Predeclare the capability. SCP/permission-boundary/trust-condition/IMDSv2 denials are PASS controls. Use the provider's policy simulator as an independent check.

## Induction: bounded laboratory procedure

Owned sub-account; planted least-privilege principals.

1. **Map.** Enumerate the test principal's effective permissions and trust relationships (and run the policy simulator).
2. **Pick one path.** e.g. `iam:PassRole`+create-compute to run as a higher planted role; or `UpdateAssumeRolePolicy` to add the principal to a planted role's trust.
3. **Exercise once (planted target).** Gain the capability against the planted principal/role; stop.
4. **Data/metadata.** Test IMDS reach and one planted data-store read.
5. **Controls.** Apply an SCP/permission boundary/trust condition and confirm the path now denies; corroborate with the simulator.
6. **Persistence/evasion.** Describe the class and its detection; do not implement it in production.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

The canonical AWS escalations are PassRole-to-compute and self-editing policy/trust; Pacu enumerates many. IMDSv2's PUT-token requirement blocks many GET-only reaches (see `rt-ssrf`). Cross-region snapshot sharing exfiltrates data without touching S3. ABAC + `sts:TagSession` can escalate if a role trusts session tags. Azure managed identity and GCP `actAs`/`serviceAccountUser` are the equivalent passthrough-privilege edges.

## Domain-specific failure modes

An IAM grant that an SCP or permission boundary overrides is not reachable — the simulator and a live attempt must agree. IMDSv2 and hop limits defeat many metadata paths. Resource policies can deny even with a broad identity grant. Prove one path against a planted principal; do not sprawl across the account or touch production identities.

## Evidence and deliverable

Provide the principal, the path (permissions used), the capability gained against the planted target, the simulator result, and the control (SCP/boundary) outcome. Keep real credentials/data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested paths.

## Versions and tool limitations

Pin provider, IMDS version/mitigations and the IAM policy set — paths are configuration-bound. Pacu/ScoutSuite/cloud CLIs perform real actions; run in the owned sub-account. No cloud behavior was verified by this content; confirm the live policies and run the simulator first.

## Remediation and detection

Least privilege, SCPs/permission boundaries, remove PassRole-to-compute and self-editing policy/trust combinations, enforce IMDSv2 + hop limit, condition role trust tightly, restrict snapshot/secret sharing, and monitor CloudTrail/Activity Log for escalation API calls. Add a regression asserting the path denies under the boundary. Detect IAM policy/trust edits, cross-account assume-role, and snapshot sharing.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | One escalation path is exercised against a planted principal in the owned sub-account where an SCP/boundary would deny: CONFIRMED; FAIL (scope to the path shown). |
| Benign refutation | An SCP/permission boundary/trust condition/IMDSv2 denies the path (simulator agrees): REFUTED; PASS for the control. |
| Insufficient evidence | A broad IAM grant with unverified boundary effect: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/cloud/offensive-cloud/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's IMDS, IAM-escalation, cross-account and data-reach craft, re-expressed as owned-sub-account experiments with planted principals, policy-simulation and SCP/boundary controls, naming persistence/evasion as bounded impact classes rather than production escalation. Composes with `cloud-control-plane-reasoning`, `root-of-trust-reasoning`, `rt-ssrf`.
