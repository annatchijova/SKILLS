---
name: rt-container-escape
description: Measure container isolation boundaries using host-owned canaries, runtime configuration and controlled denial tests without executing escape payloads.
---

# Container Isolation Boundary Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before inspecting the fixture.
Assess the actual container runtime boundary, not an assumed equivalence between
container root and host root. Kubernetes authorization belongs in rt-k8s-attacks.

## Mechanisms and prerequisites

- Host bind mounts expose specific filesystem objects under mount and permission rules.
- Runtime socket access depends on socket permissions, API authorization and daemon identity.
- Capabilities are scoped by user namespaces; a capability name alone does not prove host power.
- PID visibility, ptrace permission, LSM policy and user identity are distinct conditions.
- Shared kernel vulnerabilities require the affected build and reachable kernel interface.
- Cgroup behavior depends on hierarchy, mount delegation and kernel configuration.

## Observation and baseline

Capture the image digest, runtime configuration, UID mappings, capabilities, mount list,
namespace identifiers, seccomp mode and LSM profile from authorized inventories.
Compare container namespaces with a host-side reference supplied by the lab operator.
Two identifiers measured only inside the container do not establish a host namespace match.
Define a host-owned canary directory that the workload must not read or alter.
Keep host credentials, process memory and real device contents outside the experiment.

## Abduction and deduction

Hypothesis: a writable host bind exposes a forbidden host object to this workload identity.
Benign rival: the apparent host path is an image copy or a user-namespace remapped fixture.
Prediction: the container can observe the operator's newly changed canary only with the
suspect bind; an otherwise identical container without that bind cannot observe it.
Host-side observation must independently establish the canary's origin and any change.

## Bounded laboratory procedure

1. Use a disposable VM with a known snapshot and no production runtime sockets attached.
2. Record the baseline canary digest outside the container and prepare an unrelated control.
3. Start the existing suspect configuration only if its privileges are within the lab scope.
4. Attempt one ordinary read of the named canary through the declared mounted path.
5. If write validation is required, change only a test-owned marker and verify from the host.
6. Repeat with the bind removed or read-only, preserving all other relevant settings.
7. Assess socket policy through configuration and a benign version/authorization endpoint;
   do not create privileged siblings or mount host root to demonstrate access.
8. Validate a seccomp or LSM denial with a preselected harmless lab operation and audit event.
9. For a CVE lead, record package build/backport evidence and interface reachability;
   use vendor regression fixtures only within an explicitly disposable test environment.
10. Stop on unexpected host change, unavailable isolation telemetry or the test budget.
11. Restore the VM and verify canary and configuration state against the baseline.

## Domain failure modes

An interface name or Docker marker file is not proof of host network sharing.
A read-only bind of a socket does not itself restrict the API methods sent through it.
A rootless daemon changes host authority but can still expose that user's files.
Cgroup v1 release-agent assumptions do not transfer to a v2 hierarchy.
Kernel version strings may conceal backported fixes; a CVE match is a candidate.
Successful canary read demonstrates that mount boundary only, not arbitrary host execution.

## Evidence, detection and remediation

Retain configuration and canary digests, namespace comparison, denied operation and audit ID.
Report the exact object, effective identity and operation that crossed the boundary.
Detect unexpected runtime API clients, host-path access and policy-denied syscalls.
Remove unnecessary host mounts and sockets; minimize capabilities and apply runtime profiles.
For hostile multi-tenant workloads, evaluate stronger isolation against the stated threat model.
Retest the denied operation while verifying the legitimate application still functions.

## Versions and limits

Record host kernel package, runtime and shim build, cgroup mode and policy versions.
Inspect installed runtime/help rather than copying historical escape-tool commands.
No escape exploit, kernel payload or host credential read is supplied or executed here.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Host observer confirms fixture mutation through suspect bind; no-bind control denies it | CONFIRMED host-write exposure; FAIL |
| Apparent host file is image content and cannot follow host canary changes | REFUTED bind-exposure hypothesis; PASS for tested read |
| Only CAP_SYS_ADMIN or an old kernel banner is known | CANDIDATE; WARN, escape not demonstrated |

## Provenance

Rewritten from `Skills/container/offensive-container-escape/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain mount, namespace, capability, socket and runtime-version distinctions;
replace host takeover and persistence recipes with bounded isolation measurements.
