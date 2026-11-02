---
name: rt-netexec
description: "Red-team reference for NetExec (nxc) as a bounded protocol-enumeration and validation tool within an authorized engagement: SMB/WinRM/LDAP/MSSQL/SSH/RDP/FTP/WMI auth, discovery, share and user enumeration, password-policy-aware spraying, and the Pwn3d! semantics per protocol. Re-expressed as a scoped tool contract with lockout-safe throttling, owned-fixture validation and detection awareness instead of mass credential attack."
---

# NetExec (nxc) Bounded-Tooling Reference

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's NetExec craft as a bounded tool contract: it documents the protocol surface and flags, and insists on scope, lockout-safe throttling and detection awareness, rather than presenting spraying as a free action.

## Scope and prerequisites

NetExec acts across SMB, WinRM, LDAP, MSSQL, SSH, RDP, FTP and WMI. Every action authenticates against real accounts and can trigger lockouts, alerts and service disruption. Carry the engagement authorization: which hosts, which accounts, the attempt budget, and the stop condition. Check the domain password policy before any spray. Validate technique behavior against an owned lab first.

Declare targets, credentials in scope, attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED.

## Tool contract and observation

Core flags: protocol + target (CIDR/host/file), `-u`/`-p`/`-H` (hash), `-k` (Kerberos, ccache or password-derived TGT), `-d` domain or `--local-auth`, `-t` threads, `--timeout`, `--jitter` (random delay, e.g. `3`, `2-5`), `--no-bruteforce` (pair user[i]:pass[i] instead of full product), `--continue-on-success`.

`Pwn3d!` semantics differ by protocol: SMB/WMI = admin, WinRM/RDP/VNC = code execution, LDAP = path to DA, SSH = root, FTP = no check. A `[+]` is valid creds; `Pwn3d!` is privileged access — do not conflate them.

**Firstness:** Record the exact nxc output line (host, protocol, result, signing, OS). **Secondness:** State the expected access for that account and the deviation. **Thirdness:** Infer an access/authority finding only after the tool's result is corroborated (not from a single ambiguous line).

## Lockout-safe usage (the critical discipline)

1. **Read policy first.** `nxc smb <dc> -u user -p pass --pass-pol`; compute a safe attempts-per-window below the lockout threshold with margin.
2. **Spray, do not brute force.** One password across users with `--no-bruteforce`, `--jitter`, and attempts under the threshold; never the full user×pass product against a live domain.
3. **Throttle and jitter** to reduce lockout and detection; prefer `--continue-on-success` off unless the engagement wants full coverage.
4. **Validate on lab.** Confirm a technique's behavior against an owned host before running it against scoped production.

## Protocol surface (leads)

- **SMB** — host discovery (OS/signing/SMBv1), share enumeration and access, null/guest checks, RID-brute user enum (no creds), logged-on users (admin), `--pass-pol`. Signing:False flags relay targets (see `rt-active-directory`).
- **LDAP** — domain object enumeration, Kerberoast/ASREProast helpers, delegation and trust reads.
- **WinRM/WMI/MSSQL/SSH/RDP** — authenticated execution/enumeration where creds allow; each is code-exec-capable — treat as consequential.

## Abduction and refutation

**Mechanism hypothesis:** A supplied credential grants access or privilege it should not, or an unauthenticated enumeration (null/guest/RID) leaks principals.

**Competing benign explanation:** The `[+]` is an expected low-priv account; the `Pwn3d!` is on an in-scope admin host that is supposed to allow it; the enumeration is anonymous-allowed by design; a single result is a transient/timeout artifact.

## Evidence and deliverable

Provide the exact command (with throttling flags), the nxc output lines, the account context, and whether lockout policy was respected. Keep real credentials/hashes out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, hosts not covered.

## Domain-specific failure modes

Spraying without reading the policy causes account lockouts — a production-impacting mistake, not a finding. `[+]` is not `Pwn3d!`. Threads default high (100) and are noisy; a single result can be a timeout. Local-auth vs domain-auth confusion produces misleading results.

## Versions and tool limitations

Pin the NetExec version — protocols, flags and module behavior change across releases; confirm with `nxc --help` / `nxc <proto> --help` on the installed build before relying on any flag. No host behavior was verified by this content.

## Remediation and detection

Enforce SMB/LDAP signing, lockout policies, strong/unique local admin passwords (LAPS), disable null/guest and SMBv1, and restrict RID enumeration. Detect: spray patterns (many users, few passwords, from one source), RID-brute, and nxc's execution footprints (service creation, WMI, WinRM). Add detections rather than relying on the tool being noisy.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A scoped, policy-respecting run shows an account with access/privilege it should not have, corroborated: CONFIRMED; FAIL (scope to the access shown). |
| Benign refutation | The access is expected for that account / enumeration is anonymous-by-design: REFUTED; PASS for the control. |
| Insufficient evidence | A single ambiguous line, or a run that ignored lockout policy: CANDIDATE; WARN (and flag the policy risk). |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/active-directory/offensive-netexec/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's NetExec protocol/flag reference and `Pwn3d!` semantics, re-expressed as a bounded tool contract with mandatory lockout-safe throttling, owned-lab validation and detection awareness, replacing free-action mass credential attack with scoped, policy-respecting use. Compose with `rt-active-directory`.
