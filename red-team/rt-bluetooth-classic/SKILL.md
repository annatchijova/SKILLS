---
name: rt-bluetooth-classic
description: "Red-team assessment of Bluetooth Classic (BR/EDR) security: device/service discovery (SDP), pairing/authentication mode and legacy-pairing weakness, profile exposure (RFCOMM/OBEX/HFP), and known protocol-flaw patch status (e.g. KNOB, BIAS-class). Re-expressed as a scoped experiment in a controlled RF setting against an owned device that proves one weakness with a negative control instead of attacks on others' devices."
---

# Bluetooth Classic (BR/EDR) Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the Bluetooth-Classic craft as a scoped experiment against an owned BR/EDR device: it enumerates services, tests pairing/authentication strength, and verifies patch status for known protocol flaws, with a hardened control, rather than attacking others' devices.

## Scope and prerequisites

BR/EDR security spans discovery, pairing/authentication, exposed profiles, and known CVE-class flaws (KNOB key-entropy downgrade, BIAS impersonation). Work on an owned device in a controlled RF setting; interact only with the owned device; respect spectrum law.

Declare the owned device, the RF environment, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Discovery** — SDP service enumeration, device class, discoverability.
- **Pairing/auth** — legacy pairing vs Secure Simple Pairing/Secure Connections; Just-Works; PIN strength.
- **Profile exposure** — RFCOMM/serial, OBEX push/ftp, HFP/HSP, and app-specific services reachable without auth.
- **Protocol flaws** — KNOB (negotiated key entropy downgrade), BIAS (authentication impersonation) — patch-status questions.

## Mechanism and observation

Enumerate services and test pairing/auth and patch status against the owned device.

**Firstness:** Record discoverable services, the pairing/auth negotiated (and the key entropy), unauthenticated profile access, and KNOB/BIAS test results. **Secondness:** State the expected protection (Secure Connections, adequate key entropy, authenticated profiles, patched stack) and the deviation. **Thirdness:** Infer a weakness only after a controlled test confirms it on the owned device.

## Abduction and refutation

**Hypothesis:** The device uses weak pairing/low key entropy, exposes a profile without authentication, or is unpatched for KNOB/BIAS.

**Competing benign explanation:** Secure Connections with adequate key entropy is enforced (KNOB mitigated); profiles require authentication; the stack is patched (BIAS mitigated); the device is non-discoverable/requires user confirmation; another owned device was observed.

## Deduction and controls

A hardened device enforces strong pairing/auth and patched behavior (positive control). A confirmed finding downgrades key entropy, accesses a profile without auth, or reproduces KNOB/BIAS on the owned device where a hardened/patched config does not. Predeclare the signal. Secure Connections / min-key-entropy / authenticated profiles / patched stack are PASS controls.

## Induction: bounded procedure

Controlled RF; owned device.

1. **Discover & enumerate.** SDP scan; map services/profiles and discoverability.
2. **Pairing/auth.** Observe the pairing method and negotiated key entropy; test legacy/Just-Works acceptance.
3. **Profile access.** Attempt unauthenticated access to exposed profiles (RFCOMM/OBEX) on the owned device.
4. **KNOB/BIAS.** Use the published tests to check key-entropy downgrade and impersonation on the owned device.
5. **Control.** Confirm Secure Connections / min-entropy / authenticated profiles / patched stack refuse the above.

Record results including refutations. Keep finding and control status separate. Owned device only.

## Craft notes (leads)

KNOB downgrades the negotiated encryption-key entropy (to as low as 1 byte on unpatched stacks); the fix is a minimum-entropy floor. BIAS impersonates a previously-paired device on stacks that mishandle authentication; the fix is a patched stack + Secure Connections. OBEX push and open RFCOMM serial are classic unauthenticated-profile findings. Legacy pairing and short PINs are weak.

## Domain-specific failure modes

A patched stack with Secure Connections and an entropy floor defeats KNOB/BIAS — the primary refutations. An authenticated profile is not an unauthenticated finding. A non-discoverable device that requires user confirmation raises the bar. Interacting with others' devices is out of scope.

## Evidence and deliverable

Provide the service map, the pairing/auth and key entropy, unauthenticated profile access (if any), the KNOB/BIAS results, and the hardened-config control. Keep to the owned device. Attach expected/observed, rival explanation (patched/authenticated), falsifier, cases not tested.

## Versions and tool limitations

Pin the Bluetooth stack/version and controller — KNOB/BIAS exposure is patch-status-dependent. No device behavior was verified by this content; test the owned device to confirm.

## Remediation and detection

Enforce Secure Connections with a minimum key-entropy floor, patch the stack (BIAS), require authentication for sensitive profiles, disable unused profiles/discoverability, and use strong pairing. Add a regression that KNOB/BIAS tests report not-vulnerable and profiles require auth.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Key-entropy downgrade / unauthenticated profile access / KNOB or BIAS reproduces on the owned device where hardening/patching does not: CONFIRMED; FAIL. |
| Benign refutation | Secure Connections / entropy floor / authenticated profiles / patched stack refuses it: REFUTED; PASS for the control. |
| Insufficient evidence | An exposed profile of unclear sensitivity or a version-only KNOB/BIAS inference: CANDIDATE/NOT TESTED; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-bluetooth-classic/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's SDP/pairing/profile/KNOB/BIAS craft as a scoped experiment against an owned device with hardened/patched controls, replacing attacks on others' devices with bounded boundary and patch-status proof. Composes with `rt-bluetooth-ble`, `rt-iot`.
