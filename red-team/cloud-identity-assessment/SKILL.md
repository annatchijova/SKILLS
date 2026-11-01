---
name: cloud-identity-assessment
description: Assess effective cloud and workload identity paths from policy and controlled evidence. Use for IAM, federation, service-account and cloud-to-container trust reviews.
---

# Cloud Identity Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this workflow.

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Identity graph
Record principal, account/project, resource, action and session conditions. Use supplied policy exports or authorized read-only inventory. Keep identity discovery separate from resource mutation.
Build edges for role assumption, role passing, workload creation and policy modification. Each edge needs its exact resource and preconditions.

## Effective permission checks
For each candidate edge inspect identity policy, resource trust, explicit denies, organizational constraints, session restrictions and permission boundaries as applicable.
A role-passing grant alone does not prove escalation: the actor must also be able to create or alter a workload, the service must assume that role, and the resulting identity must reach the claimed asset.
For federated CI identities inspect subject, audience, issuer and branch/environment restrictions.
For Kubernetes inspect namespace, service account, role bindings, admission policy and reachable cloud identity. A visible token or capability alone is not a demonstrated host escape.

## Experiment and refutation
Prefer policy evaluation and a disposable fixture with synthetic data. A simulator result is evidence of modeled policy, not proof of live execution.
Test the strongest blocking explanation before marking a path reachable. If runtime proof is unavailable, keep the path hypothetical and identify the missing edge.
Use simulated metadata endpoints when testing application SSRF; retrieving real workload credentials is unnecessary to prove the application boundary.

## Output
Deliver the identity graph with evidence per edge, denied edges, conditions, version/time, unknowns and least-privilege remediation. Any live permission change or workload creation must fit the existing engagement authorization and have an explicit cleanup plan.

## Discriminating identity experiment

Hypothesis: an application principal can cause an owned test workload to act with
authority outside the application's intended resource boundary. Benign rival:
role trust, a session restriction or a resource policy blocks the proposed path.
Deduction: an innocuous marker action succeeds only through the disputed identity
edge, while direct access by the initial principal remains denied.

1. Record initial identity, target resource, intended policy and exact policy versions.
2. Establish allowed and denied direct requests to two synthetic marker resources.
3. Evaluate every proposed delegation edge independently, including resource trust
   and session conditions; retain explicit denials rather than dropping them from the graph.
4. In an authorized disposable fixture, exercise only the minimum delegation path
   needed to access the marker. If only policy exports are available, stop at a candidate.
5. Observe the actual service identity and correlated audit event at the marker sink.
6. Repeat with the disputed trust edge removed, keeping the legitimate allowed case.
7. Verify cleanup of test-owned identities, sessions and resources from the inventory.

Do not infer effective access from one policy statement. Cloud authorization layers
and simulator coverage differ by provider, service and request context. Azure role
assignment scope, GCP service-account impersonation and AWS role passing are distinct
mechanisms; identify the service-specific prerequisites before constructing a graph edge.
Resource existence errors and inventory permission failures do not establish denial
of the business action itself. Session expiry is separate from credential revocation.

## Evidence, detection and limits

Keep policy digests, principal/resource IDs, request IDs, condition values and the
allowed/denied control results. Detect unexpected delegation and sensitive policy
changes using the same correlation IDs. Prefer narrowing trust and resource scope
at the edge responsible for the demonstrated grant; retest legitimate workloads.
Record provider API, identity integration, SDK and policy-evaluator versions.
No cloud operation ran during authorship; policy simulation does not certify runtime access.

## Behavioral acceptance

| Evidence | Expected verdict |
|---|---|
| Delegated fixture identity reads forbidden marker; direct and restricted-edge controls deny it | CONFIRMED delegated boundary failure; FAIL |
| Resource trust rejects the modeled delegation and the legitimate allowed control works | REFUTED proposed path; PASS for that edge |
| A broad role-passing statement exists without workload creation or effective trust evidence | CANDIDATE; WARN |

## Provenance

Source path: `Skills/cloud/offensive-cloud/SKILL.md`.

Methodology adapted from Claude-Red `offensive-cloud` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

