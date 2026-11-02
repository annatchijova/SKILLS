---
name: rt-linux-privesc
description: "Red-team assessment of Linux local privilege-escalation boundaries: SUID/SGID and capabilities misuse, sudo misconfiguration and GTFOBins, writable paths in root-run scripts/cron, PATH and library hijacks, world-writable sensitive files, and kernel-exploit exposure. Re-expressed as scoped experiments on an owned host that prove one escalation vector against a planted root-run fixture with hardened-config controls instead of rooting a production system."
---

# Linux Privilege-Escalation Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's Linux-privesc craft as scoped experiments on an owned host: it names the escalation vectors, proving one against a planted root-run fixture rather than rooting a production system.

## Scope and prerequisites

Local privesc moves from a low-privilege user to root via a misconfiguration. Work on an owned host; where possible prove the vector against a planted root-run fixture (a lab SUID binary, a lab sudo rule, a lab root cron) so the effect is contained. Prove the escalation once with a benign marker (a root-owned marker file / `id`), then stop.

Declare the host, distro/kernel, attempt budget, stop condition. Enumeration-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **SUID/SGID & capabilities** — misused SUID binaries, dangerous file capabilities (cap_setuid, cap_dac_override).
- **sudo** — NOPASSWD rules, GTFOBins-abusable allowed commands, `sudo` CVEs.
- **Writable root-run paths** — world-writable scripts/binaries executed by root cron/systemd, writable service units.
- **PATH / library hijack** — relative PATH in root-run scripts, `LD_PRELOAD`/`LD_LIBRARY_PATH`, writable library dirs.
- **Sensitive file exposure** — world-readable shadow/keys, writable `/etc/passwd`/sudoers.
- **Kernel** — exploitable kernel version (version-bound; prove on a lab VM).

## Mechanism and observation

Pick one vector; trace the misconfiguration to root execution.

**Firstness:** Record the escalation achieved against the planted fixture (root marker written, root shell on the lab binary). **Secondness:** State the intended boundary (least privilege, no writable root-run paths, GTFOBins-safe sudo) and the deviation. **Thirdness:** Infer the vector only after the escalation is exercised under control.

## Abduction and refutation

**Hypothesis:** A specific misconfiguration lets a low-priv user run code as root.

**Competing benign explanation:** The SUID binary is not GTFOBins-abusable; the sudo rule is tightly scoped; the root-run path is not actually writable by the user; `secure_path`/absolute paths defeat PATH hijack; the sensitive file is correctly permissioned; the kernel is patched.

## Deduction and controls

A low-priv user cannot reach root on a hardened host (positive control). A confirmed finding escalates via the vector against the planted fixture where a hardened config refuses. Predeclare the root marker. Least-privilege SUID/caps / scoped sudo / non-writable root paths / `secure_path` / patched kernel are PASS controls.

## Induction: bounded procedure

Owned host; planted root-run fixture where possible.

1. **Enumerate.** SUID/SGID, capabilities, sudo rights (`sudo -l`), cron/systemd root jobs, writable paths, sensitive-file perms, kernel version (LinPEAS/linux-exploit-suggester as aids).
2. **Pick one vector.** Choose the clearest misconfiguration against a planted fixture.
3. **Exercise once.** e.g. abuse a GTFOBins sudo rule / writable root cron / SUID to write a root-owned marker; confirm root; stop.
4. **Controls.** Harden the fixture (scope the sudo rule, fix perms, `secure_path`) and confirm the vector fails.
5. **Kernel (lab only).** If testing a kernel exploit, do it on a lab VM snapshot.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

GTFOBins maps allowed/SUID binaries to escalation one-liners — the sudo/SUID finding is really "this binary should not be root-runnable by this user". Writable root-run cron/systemd paths and relative PATH in root scripts are recurring. Capabilities (cap_setuid on a binary) are a subtler SUID equivalent. Kernel exploits are version-bound and crash-prone — lab VM only.

## Domain-specific failure modes

A SUID binary not in GTFOBins (and not otherwise abusable) is not a vector. A sudo rule that cannot be escaped is safe. A root-run path the user cannot actually write is a refutation. `secure_path` defeats PATH hijack. Kernel exploits can crash the host — never on production. Prove against a planted fixture to stay contained.

## Evidence and deliverable

Provide the vector, the misconfiguration, the root marker achieved against the planted fixture, and the hardened-config control result. Keep to the owned host. Attach minimal replay, expected/observed, rival explanation, falsifier, vectors not assessed.

## Versions and tool limitations

Pin distro, kernel and sudo versions — vectors are version-bound. Enumeration tools are aids, not verdicts. No host behavior was verified by this content; confirm on the owned host first.

## Remediation and detection

Minimize SUID/SGID and file capabilities, scope sudo rules (avoid GTFOBins-abusable binaries, set `secure_path`), remove writable root-run paths, correct sensitive-file permissions, and patch the kernel. Add a regression asserting the vector fails. Detect SUID execution anomalies, sudo misuse, and writes to root-run paths.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A vector escalates to root against a planted fixture where a hardened config refuses: CONFIRMED; FAIL. |
| Benign refutation | Non-abusable SUID / scoped sudo / non-writable path / patched kernel defeats it: REFUTED; PASS for the control. |
| Insufficient evidence | A suspicious config without a confirmed escalation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/privesc/offensive-linux-privesc/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's SUID/sudo/cron/PATH/kernel craft, re-expressed as owned-host experiments against planted root-run fixtures with hardened controls, replacing production rooting with bounded, contained escalation proof. Composes with `rt-toctou`, `rt-advanced-redteam`.
