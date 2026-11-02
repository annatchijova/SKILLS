---
name: rt-container-escape
description: "Red-team assessment of container isolation boundaries: dangerous capabilities (CAP_SYS_ADMIN, CAP_SYS_PTRACE, CAP_DAC_OVERRIDE, CAP_SYS_RAWIO), privileged mode, host mounts and socket exposure (Docker/containerd/CRI-O), and namespace/cgroup escapes. Re-expressed as scoped experiments inside an owned deliberately-misconfigured container that enumerate the isolation posture and prove one escape to a planted host marker with hardened-control negatives."
---

# Container Isolation-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's container-escape craft as scoped experiments inside an owned, deliberately-misconfigured container: it enumerates the isolation posture and proves one escape to a planted host marker, with a hardened container as the negative control.

## Scope and prerequisites

Container escape depends on how the container was configured (capabilities, privileged flag, mounts, shared namespaces). Use an owned lab container and an owned host with a planted marker file. Prove escape by touching the planted marker from inside; do not break out of a production host.

Declare the runtime and the container config, attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Capabilities** — CAP_SYS_ADMIN (mount, cgroup, namespaces), CAP_SYS_PTRACE (cross-namespace), CAP_DAC_OVERRIDE (permission bypass), CAP_NET_ADMIN, CAP_SYS_RAWIO (`/dev/mem`).
- **Privileged / device access** — `--privileged`, host devices, `/dev` access.
- **Host mounts** — host filesystem, `/`, or sensitive paths mounted in.
- **Socket exposure** — Docker/containerd/CRI-O socket mounted (control the host runtime).
- **cgroup/namespace exposure** — shared PID/net/IPC namespaces or version/configuration-specific cgroup interfaces. The legacy `release_agent` route is specific to cgroup v1 and requires additional writable/mount and execution preconditions; cgroup v2 does not provide `release_agent`. Kernel-exploit-class escapes are separately version-bound.

## Mechanism and observation

Enumerate the posture first, then trace one misconfiguration to host reach.

**Firstness:** Record the posture (effective caps from `/proc/self/status`, mounts, sockets, namespaces) and, if escaped, the planted host marker touched. **Secondness:** State the intended isolation and the deviation. **Thirdness:** Infer the escape class only after the marker is reached under control.

## Abduction and refutation

**Mechanism hypothesis:** A specific granted capability, mount or socket lets in-container code act on the host.

**Competing benign explanation:** The container drops all dangerous caps and is non-privileged; no host mount/socket is present; user namespaces remap root; seccomp/AppArmor blocks the syscall; the "escape" only touched the container's own overlay.

## Deduction and controls

A hardened container cannot reach the host (positive control = isolation holds). A confirmed escape touches the planted host marker from inside the misconfigured container where the hardened one cannot. Predeclare the marker. Dropped caps / non-privileged / no host mount / user-ns / seccomp-AppArmor are PASS controls.

## Induction: bounded laboratory procedure

Owned misconfigured container; owned host; planted marker.

1. **Detect & enumerate.** Record image digest, runtime configuration, UID mappings, effective capabilities, mounts, namespace identifiers, seccomp mode and LSM profile from authorized inventories. Decode `CapEff` against this kernel's capability limit. Have the lab operator provide a host-side reference so container-only observations do not masquerade as host evidence.
2. **Pick one misconfiguration and verify its preconditions.** A mounted runtime socket or host path can expose host resources according to its permissions. Consider a `release_agent` path only after confirming cgroup v1, the relevant hierarchy and mount permissions, required capabilities, and a reachable trigger; do not apply it as a generic CAP_SYS_ADMIN escape.
3. **Prove reach, stop.** Read only the operator-owned canary through the declared path. For a write claim, alter only a test-owned marker and independently verify its change from the host. Do not establish host persistence.
4. **Controls.** Repeat with the suspect bind/socket/capability removed or constrained while keeping relevant settings fixed. A read-only or no-bind control must be interpreted for the particular operation being tested.
5. **Other surfaces.** Assess runtime-socket authority through its configured API policy and a benign endpoint; do not mount host root or create privileged sibling containers merely to demonstrate reach. For CVE leads, inspect vendor package/backport status and interface reachability; a version banner is not confirmation.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

An exposed container-runtime socket can grant substantial host control according to the socket and daemon policy; a host filesystem mount grants only the access its mount and permissions allow. Shared PID namespace exposes process visibility subject to other controls. Kernel-exploit escapes are version-bound. `CapEff` is a hexadecimal effective-capability bitmask: decode it against the running kernel's `CAP_LAST_CAP` and the capability definitions. The value `0000003fffffffff` is not a version-independent synonym for every capability being enabled.

## Domain-specific failure modes

A non-privileged container with dropped caps and no host mounts or sockets has fewer common configuration-based escape paths; this does not rule out runtime, kernel, device, or other vulnerabilities. Scope a PASS to the tested vectors and configuration. Touching the container's own overlay is not host reach. User namespaces can remap container identities; verify the actual mapping and applicable controls. Seccomp/AppArmor can block a specific syscall even when a capability is present. Prove the planted host marker, not a shell.

## Evidence and deliverable

Provide the posture (caps/mounts/sockets/namespaces), the exact object and effective identity, the host-side canary provenance and observed operation, and the corresponding constrained-configuration result. A successful canary read confirms that mount/read boundary only, not arbitrary host execution. Keep host data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested configs.

## Versions and tool limitations

Pin the runtime, kernel and LSM (seccomp/AppArmor/SELinux) versions — escape viability is version-bound. Enumeration tools may attempt active escape; keep to the owned lab. No runtime behavior was verified by this content; confirm the live config first.

## Remediation and detection

Run non-privileged, drop all caps and add back only what is needed, never mount the runtime socket or host paths, enable seccomp/AppArmor/SELinux and user namespaces, and use rootless runtimes. Add a regression asserting the hardened container cannot reach the marker. Detect capability/mount anomalies and in-container runtime-socket access.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | In-container code touches the planted host marker via a misconfiguration where the hardened container cannot: CONFIRMED; FAIL (scope to the escape shown). |
| Benign refutation | Dropped caps / non-privileged / no mount-socket / seccomp defeats the escape: REFUTED; PASS for the control. |
| Insufficient evidence | A dangerous posture enumerated but no host reach demonstrated: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/container/offensive-container-escape/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's capability/mount/socket/namespace escape craft, re-expressed as owned-lab experiments that enumerate posture and prove one escape to a planted marker against a hardened control, replacing production host breakout with bounded reach proof. Composes with `rt-k8s-attacks`, `container-trust-boundary`.
