---
name: container-trust-boundary
description: Treat a container as isolation, not as a security boundary — because "it runs in a container" is not "it is contained": it shares the host kernel, and the real perimeter is the kernel attack surface it can reach, the provenance of the image it was built from, the orchestration identity it holds, and the escape surface it was granted. Use whenever the system is Docker/Kubernetes/containerd and the question is blast radius, isolation, or "is this safe to run": a compromised or untrusted container, a `privileged` flag, a `hostPath` mount, a mounted `docker.sock`, a pod service-account token, an image from an unverified registry, "can it escape", "is the container a security boundary", "we run untrusted code in containers". Sibling of cloud-control-plane-reasoning (a pod's identity reaches the control plane) and agent-trust-boundaries (running untrusted code); it maps the container's real edges. It does not configure Kubernetes or write admission policy, and never accepts the container edge as a boundary without checking the kernel, image, identity, and escape surface behind it.
---

# Container Trust Boundary

A container is a bundle of namespaces and cgroups sharing one host kernel. That is
isolation — process A cannot see process B's filesystem — and it is emphatically not
a security boundary in the sense a VM or a hypervisor is. "It runs in a container" is a
statement about tidiness, not containment, and every threat model that stops at the
container edge has drawn its perimeter one layer too shallow.

The boundary that actually matters is four things behind the edge, each of which a
"contained" workload can reach:

- **The shared kernel** — one exploitable kernel bug and namespaces are a suggestion,
  not a wall. The container's real attack surface includes every syscall it can make.
- **The image's provenance** — the code was decided at build time by whoever authored
  the layers and the base image. An unpinned `FROM ...:latest` from an unverified
  registry is untrusted code you scheduled with intent.
- **The identity it holds** — a Kubernetes pod carries a service-account token; that
  token is a control-plane credential (see `cloud-control-plane-reasoning`). The pod
  does not need to escape the node if its token already reaches the API server.
- **The escape surface it was granted** — `privileged`, `hostPath`, a mounted
  `docker.sock`, dangerous capabilities, host PID/network namespaces. These are not
  vulnerabilities; they are doors handed over in the manifest.

Composes with the library:

- **cloud-control-plane-reasoning** — the pod/container identity is a control-plane credential; the shortest path out is often the token, not a kernel bug
- **agent-trust-boundaries** — running untrusted or model-generated code in a container is only as contained as this skill's four edges make it
- **dependency-provenance** — the image is a dependency graph; what is in the layers, and who put it there, is the provenance question
- **secret-lifecycle-discipline** — mounted secrets and tokens are the container's most valuable reachable asset
- **assume-breach-modeling** — start from "this container is compromised" and follow the four edges outward
- **honest-degradation** — "we scanned the image, no CVEs" is not "the image is trustworthy"; say which claim you can make

---

## Step 1 — Isolation vs security boundary: name which one you have

State it plainly for the workload in question: namespaces + cgroups + seccomp +
capabilities give you *isolation with a shared kernel*. A boundary you would stake
untrusted multi-tenant code on is a *different, stronger* claim (gVisor, Kata,
a microVM, a separate node pool, ultimately a separate machine).

- If you are running code you do not trust (customer builds, model-generated code,
  a captured sample), the default container is **not** the boundary you need — say so,
  and name what would be (`untrusted-sample-handling` for the hostile-artifact case).
- If the threat is a bug in your own trusted service, isolation may be sufficient — but
  only after Steps 2-4 confirm the other three edges are not wide open.

The error this kills: quoting "it's containerized" as if it settled the trust question
it merely relabeled.

---

## Step 2 — Image provenance: what is actually in this, and who decided

The running container is the image, and the image was authored — by a chain of layers,
a base image, and a build that pulled dependencies. Trace it:

- **Base pinned by digest, or floating?** `FROM ubuntu:latest` means "whatever that tag
  resolves to today," which is a decision you delegated to a registry.
- **What is in the layers** — unexpected binaries, build tools left in production
  images, secrets baked into a layer (they persist in history even if a later layer
  deletes them — the same trap as a rotated key in git history).
- **Provenance of the source** — an image from an unverified public registry is
  unreviewed third-party code with root in your cluster's namespace. Registry typo /
  name-confusion is the container form of dependency confusion.
- A CVE scan is one input, not the verdict: "no known CVEs" says nothing about a
  deliberately malicious layer or an unpinned supply chain (`dependency-provenance`).

---

## Step 3 — The identity the container holds is often the real exit

Before hunting kernel escapes, ask what the container can already do *without*
escaping, because the answer is usually more than a kernel bug would buy:

- **Service-account / workload identity** — a mounted pod token, an IRSA/workload-
  identity role, a cloud instance profile inherited from the node. Enumerate what that
  identity reaches on the control plane (`cloud-control-plane-reasoning`); a
  broadly-scoped token is a full compromise that never touched the kernel.
- **Mounted secrets** — env vars, mounted volumes, config maps: the crown jewels are
  frequently one `cat` away inside the "contained" process.
- **Network reach** — a flat pod network means the container can talk to every other
  service and the metadata endpoint. "Isolated" on disk is not isolated on the wire.

---

## Step 4 — The escape surface is a list of granted doors, not a mystery

Container escape is usually not an exotic 0-day; it is a permission somebody set in the
manifest. Enumerate the doors as reachable edges:

- `privileged: true` — effectively root on the host; the boundary is gone by
  configuration.
- `hostPath` mounts — a writable host filesystem path is a path to the node.
- Mounted `docker.sock` / container runtime socket — the container can create sibling
  privileged containers; this is root on the host with extra steps.
- Dangerous capabilities (`CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`), host PID/IPC/network
  namespaces, disabled seccomp/AppArmor.

Each is a *granted* escape, present in a config you can read, not a vuln you must
discover. Rank the workload's danger by which of these it holds.

---

## Step 5 — Assume breach and follow the four edges out

Put the four edges together and reason from "this container is already compromised":
kernel surface + image trust + held identity + escape doors. The output is the blast
radius — usually node, then (via the token) namespace, then (via a too-broad role)
cluster, then (via the control plane) the cloud account. State the shortest path and
the honest uncertainty: "no known escape door, but the pod token is cluster-admin, so
containment is irrelevant" is a finding; "contained" without checking the token is a
hope.

---

## The one-line test

If your argument for safety is "it runs in a container," you have named the isolation
and skipped the boundary. Point at the kernel surface, the image's provenance, the
identity the workload holds, and the escape doors in its manifest — and if a compromise
of that container reaches the node or the control plane through any of the four, it was
never contained, only tidy.
