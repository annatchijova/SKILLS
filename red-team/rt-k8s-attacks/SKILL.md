---
name: rt-k8s-attacks
description: "Red-team assessment of Kubernetes cluster authority boundaries: service-account token discovery and RBAC abuse, kubelet/API-server reachability, privileged/hostPath/hostPID pod specs and escape, secrets access, and lateral movement across namespaces. Re-expressed as scoped experiments in an owned cluster using can-i permission mapping, a planted namespace/secret and RBAC-hardened negatives instead of live cluster takeover."
---

# Kubernetes Authority-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's Kubernetes craft as scoped experiments in an owned cluster: it names the token, RBAC and pod-spec escape paths, proving one against a planted namespace/secret with `kubectl auth can-i` as the control, rather than taking over a live cluster.

## Scope and prerequisites

Cluster compromise is RBAC and pod-security analysis: from a pod's service account, which API verbs and pod specs reach secrets, nodes or other namespaces. Use an owned cluster with a planted namespace and secret. Prove a path against the planted target; do not read real secrets or pivot across a production cluster.

Declare the cluster, your starting identity, attempt budget, stop condition. Manifest/RBAC-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Position** — inside a pod? service host/port and SA token injected; API server reachable via DNS.
- **Token/RBAC** — default/projected SA token; `kubectl auth can-i` to map effective verbs; over-broad roles (list/get secrets, create pods, impersonate).
- **Pod-spec escape** — create a privileged / hostPath `/` / hostPID / hostNetwork pod → node (see `rt-container-escape`).
- **Kubelet** — often weakly authenticated read/exec on `:10250`.
- **Secrets** — read secrets in-namespace or cluster-wide.
- **Lateral** — cross-namespace via RBAC gaps, node → other pods, cloud IAM via node identity.

## Mechanism and observation

Trace the SA's permissions to the authority they reach.

**Firstness:** Record the capability gained against the planted target (listed a planted secret, scheduled a privileged pod, reached the kubelet). **Secondness:** State the intended RBAC/pod-security boundary and the deviation. **Thirdness:** Infer the class only after the path is exercised under control.

## Abduction and refutation

**Mechanism hypothesis:** The service account holds verbs (or the cluster allows pod specs) that let it read secrets, create a node-reaching pod, or act in other namespaces.

**Competing benign explanation:** RBAC scopes the SA to its own namespace with minimal verbs; Pod Security Admission (restricted) blocks privileged/hostPath pods; the kubelet is authenticated; `can-i` returns no for the action; the token is auto-mount-disabled.

## Deduction and controls

A SA acting within its role succeeds (positive control); the escalation must fail if RBAC/PSA hold. A confirmed finding exercises the path against a planted namespace/secret where a hardened RBAC/PSA would deny (confirm with `kubectl auth can-i`). Predeclare the capability. `can-i: no` / restricted PSA / authenticated kubelet are PASS controls.

## Induction: bounded laboratory procedure

Owned cluster; planted namespace/secret.

1. **Locate & authenticate.** Confirm in-pod position; extract the SA token/CA; query the API with it.
2. **Map RBAC.** `kubectl auth can-i --list`; identify one path (read planted secret / create privileged pod / impersonate).
3. **Exercise one path (planted target).** e.g. list the planted secret; or schedule a hostPath pod and touch a planted node marker; or hit the kubelet.
4. **Prove capability, stop.** Do not read real secrets or pivot further.
5. **Controls.** Tighten RBAC / apply restricted PSA and confirm the path denies; corroborate with `can-i`.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Tools: kube-hunter, peirates (in-pod), kubeaudit, kdigger — enumeration aids. The projected SA token path is `/var/run/secrets/kubernetes.io/serviceaccount/`. Node-reaching pod specs (privileged, hostPath `/`, hostPID) turn pod-create into node compromise. A node's cloud identity bridges to `cloud-identity-assessment`. `can-i` is both recon and the control oracle.

## Domain-specific failure modes

A broad-looking role that `can-i` says cannot perform the action is a refutation. Restricted Pod Security Admission blocks the privileged-pod path regardless of RBAC. An authenticated kubelet closes `:10250`. Reading the planted secret is the proof; reading real secrets is out of scope.

## Evidence and deliverable

Provide the SA identity, the path (verbs/pod spec), the capability against the planted target, the `can-i` result, and the control outcome. Keep real secrets out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested paths.

## Versions and tool limitations

Pin the cluster version, PSA/PSP posture and kubelet config — paths are version-bound. Tools perform real API actions; run in the owned cluster. No cluster behavior was verified by this content; confirm live RBAC with `can-i` first.

## Remediation and detection

Least-privilege RBAC (no cluster-wide secret/get-list, no pod-create for app SAs, no impersonate), restricted Pod Security Admission, authenticated kubelet, disabled SA auto-mount where unused, network policies, and node-identity scoping. Add a regression asserting `can-i` denies the path. Detect privileged-pod creation, secret enumeration, and kubelet access.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A SA reads a planted secret / schedules a node-reaching pod where hardened RBAC/PSA would deny (`can-i` agrees): CONFIRMED; FAIL (scope to the path). |
| Benign refutation | RBAC/PSA/`can-i` denies the path: REFUTED; PASS for the control. |
| Insufficient evidence | A broad role without a verified reachable action: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/container/offensive-k8s-attacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's token/RBAC, kubelet, pod-spec-escape and lateral-movement craft, re-expressed as owned-cluster experiments with `can-i` mapping, a planted target and RBAC/PSA controls, replacing live cluster takeover with bounded authority-path proof. Composes with `rt-container-escape`, `cloud-identity-assessment`.
