---
name: rt-k8s-attacks
description: Validate Kubernetes RBAC, admission, network policy and operator authority using isolated namespaces and synthetic resources.
---

# Kubernetes Control Boundary Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before planning requests.
Keep API authorization, admission, node isolation and cloud identity as separate boundaries.
Use supplied exports when a disposable cluster is unavailable.

## Mechanisms and prerequisites

- RBAC grants are resource-, verb-, namespace- and sometimes name-specific.
- Creating role objects does not by itself bypass escalation or binding authorization checks.
- Pod creation can confer access to identities or volumes, subject to admission and scheduling.
- Admission webhooks apply according to selectors, operations and failure policy.
- NetworkPolicy effects depend on selected endpoints and the actual CNI implementation.
- A custom resource may cause a privileged operator to act as a confused deputy.
- Kubelet and etcd have distinct authentication surfaces; API-server RBAC alone does not
  establish their effective authorization.

## Observation and baseline

Record cluster and namespace, service account, authorizer configuration and admitted pod spec.
Read Role/ClusterRole rules and bindings from their actual schema, including aggregated roles.
Inventory webhook selectors, Pod Security configuration, CNI and operator identities.
Define two fixture namespaces and a synthetic ConfigMap accessible only to its owner.
Identify the API route and admission stage expected to reject each forbidden operation.

## Abduction and deduction

Hypothesis: a low-privilege principal can induce an operator to read a foreign fixture object.
Benign rival: an operator reconciliation log describes a rejected or cached request.
Prediction: only a permitted cross-namespace reference produces the unique foreign marker
in the controlled result; an equivalent reference under restrictive policy cannot do so.
Keep the operator's legitimate same-namespace operation as a positive liveness control.

## Bounded laboratory procedure

1. Use a disposable cluster or explicitly scoped test namespaces with synthetic data.
2. Snapshot RBAC, admission and network configuration; designate cleanup ownership.
3. Compare authorization review results for allowed and forbidden fixture actions.
4. Where permitted, execute the harmless real API action and retain its audit event;
   an authorization review alone does not test admission or runtime behavior.
5. Exercise one operator reference with same-namespace and cross-namespace twins.
6. For admission, submit harmless fixture manifests differing in one prohibited field;
   use server dry-run only when the installed webhook supports it and records the decision.
7. For network isolation, use a dedicated echo service and compare allowed and denied
   pod pairs, recording labels, namespace selectors, route and CNI observations.
8. Verify workload metadata isolation using a simulated endpoint, not live token extraction.
9. Review kubelet/etcd authentication configuration and supplied audit evidence separately;
   do not enumerate real secrets, execute in unrelated pods or deploy a DaemonSet.
10. Stop at the demonstrated boundary, restore fixture policy and remove owned resources.

## Domain failure modes

An empty egress list is interpreted with policyTypes and policy selection, not in isolation.
Service, pod-IP, host-network and node routes may have different implementation behavior.
An API 403 can come from authorization; an admission rejection requires separate evidence.
Webhook failurePolicy Ignore is a conditional exposure, not proof that a failure occurred.
Base64 encoding of a Secret says nothing about etcd encryption or effective read permission.
Service-account token audiences and expiry matter even when a token file is present.
Operator CRD edit rights and controller execution rights must both be traced.

## Evidence, detection and remediation

Deliver actor-resource-action rows with authorizer, admission and runtime outcomes.
Retain audit IDs, sanitized resource diffs, observed marker and policy revision.
Detect unexpected binding changes, operator cross-namespace access and direct node API use.
Restrict bind/escalate/impersonate grants, constrain CR references and minimize workload identity.
Enforce admission on intended routes and validate CNI isolation empirically.
Retest the same-namespace control alongside the originally forbidden path.

## Versions and limits

Record API server, kubectl, CNI, operator, webhook and cloud identity integration versions.
Inspect installed schemas/help; historical kubelet ports and token defaults are not universal.
No live cluster actions or offensive toolkit modules were executed during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Foreign synthetic marker appears through operator; restrictive twin denies it | CONFIRMED deputy boundary failure; FAIL |
| Role creation is allowed but binding/escalation checks deny the proposed grant | REFUTED escalation path; PASS for that check |
| Policy YAML exists but no CNI behavior or traffic control was measured | NOT TESTED enforcement; WARN |

## Provenance

Rewritten from `Skills/container/offensive-k8s-attacks/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain RBAC, admission, operator and network mechanisms; replace secret dumping,
node takeover and persistence with synthetic resource and control validation.
