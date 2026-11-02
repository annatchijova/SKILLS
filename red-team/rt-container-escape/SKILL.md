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
- **cgroup/namespace escapes** — `release_agent` (CAP_SYS_ADMIN), shared PID/net/IPC namespaces, kernel-exploit-class.

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

1. **Detect & enumerate.** Confirm containerization and read the posture: `/proc/self/status` CapEff (decode with capsh), mounts, `/var/run/docker.sock` presence, namespace sharing. (deepce/amicontained/CDK are enumeration aids.)
2. **Pick one misconfig.** e.g. mounted Docker socket → start a container mounting host `/`; or CAP_SYS_ADMIN → `release_agent` cgroup escape; or host-mounted path → read/write the planted marker.
3. **Prove reach, stop.** Touch the planted host marker once; do not establish host persistence.
4. **Controls.** Re-run in a hardened container (dropped caps, non-privileged, no socket/mount, seccomp/AppArmor, user-ns) and confirm the escape fails.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

The most common real escapes are a mounted container runtime socket (instant host control) and `--privileged`/CAP_SYS_ADMIN enabling `release_agent` or direct device access. A host filesystem mount is a direct read/write primitive. Shared PID namespace exposes host processes. Kernel-exploit escapes are version-bound. `CapEff: 0000003fffffffff` means all caps (privileged).

## Domain-specific failure modes

A non-privileged container with dropped caps and no mounts/sockets simply cannot escape — a PASS. Touching the container's own overlay is not host reach. User namespaces remap root to unprivileged on the host. Seccomp/AppArmor can block the specific syscall even when a cap is present. Prove the planted host marker, not a shell.

## Evidence and deliverable

Provide the posture (caps/mounts/sockets/namespaces), the escape class used, the planted host marker touched, and the hardened-container control result. Keep host data out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, untested configs.

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
