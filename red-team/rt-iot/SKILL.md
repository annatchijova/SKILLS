---
name: rt-iot
description: "Red-team assessment of IoT/embedded device boundaries: firmware extraction and analysis, hardware debug interfaces (UART/JTAG/SWD/SPI flash), bootloader and secure-boot, protocol and update-integrity, and credential/key storage. Re-expressed as scoped experiments on an owned device with lab bench access that prove one boundary weakness against the device's own firmware with hardened-config controls instead of attacks on deployed third-party devices."
---

# IoT / Embedded Device Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's IoT craft as scoped bench experiments on an owned device: it names the firmware, hardware-interface and protocol boundaries, proving one weakness against the device's own artifacts rather than attacking deployed devices in the field.

## Scope and prerequisites

Embedded security spans firmware, hardware debug ports, boot chain, and protocols. Work on an owned device you may open and bench-test (or a consented sample), with its own firmware. Prove a weakness against the device/firmware itself; do not attack deployed third-party devices or radio spectrum outside scope (route RF to the wireless skills).

Declare the device, firmware version, bench access, attempt budget, stop condition. Datasheet-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Firmware** — extraction (flash dump, update-file unpack), analysis (binwalk, filesystem, hardcoded secrets/keys), modification + re-flash.
- **Hardware debug** — UART consoles (bootloader/root shell), JTAG/SWD (halt/dump/patch), SPI/I2C flash read.
- **Boot chain** — secure boot / verified boot, bootloader unlock, rollback protection.
- **Update integrity** — signed vs unsigned updates, downgrade.
- **Credential/key storage** — keys in firmware, lack of secure element.
- **Protocol** — device-to-cloud/app auth, local API (see `rt-network-attacks` / wireless skills for the transport).

## Mechanism and observation

Pick one boundary; trace the protection to the weakness.

**Firstness:** Record what was obtained (a flash dump, a UART root shell, a hardcoded key, an accepted unsigned update). **Secondness:** State the intended protection (encrypted/signed firmware, locked debug ports, secure boot, signed updates) and the deviation. **Thirdness:** Infer the class only after the weakness is exercised under control on the owned device.

## Abduction and refutation

**Hypothesis:** A boundary is unprotected — debug ports open, firmware unencrypted/unsigned, keys in the clear, updates unverified.

**Competing benign explanation:** Debug interfaces are fused/disabled; firmware is encrypted and secure boot verifies it; updates are signed and rollback-protected; keys live in a secure element; the "open" port is a decoy or requires authentication.

## Deduction and controls

A locked-down device resists the attempt (positive control = protections hold). A confirmed finding obtains the artifact/access via the boundary where a hardened device would not. Predeclare the obtained artifact. Fused debug ports / signed+encrypted firmware / secure boot / secure-element keys are PASS controls.

## Induction: bounded bench procedure

Owned device; bench access.

1. **Recon.** Identify chips, interfaces, and the update mechanism (datasheets, board inspection).
2. **Firmware.** Obtain firmware (update file or flash dump via SPI); unpack (binwalk), analyze for secrets/keys and the filesystem.
3. **Hardware debug.** Probe UART for a console/bootloader; attempt JTAG/SWD halt+dump; SPI flash read.
4. **Boot/update.** Test secure-boot enforcement and whether an unsigned/downgraded update is accepted on the owned device.
5. **Prove one weakness, stop.** e.g. extract a hardcoded key, or get a UART root shell; do not pivot to fielded devices.
6. **Controls.** Confirm whether fusing/secure-boot/signing would have blocked it.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

UART consoles (often a 3- or 4-pad header) frequently drop to a bootloader or root shell. SPI flash can be dumped in-circuit or with a clip. binwalk + filesystem extraction surfaces hardcoded credentials/keys and private keys embedded in firmware (a recurring real finding). Secure boot + signed, rollback-protected updates + a secure element for keys are the controls that defeat most of this. RF protocols route to the wireless skills.

## Domain-specific failure modes

Fused/disabled debug ports defeat UART/JTAG access. Encrypted firmware + secure boot defeats trivial extraction/modification. A hardcoded key found in firmware is a real finding only if it is actually used for a security function (not a test/public key). Attacking deployed devices or out-of-scope spectrum is out of scope. Bench access to an owned device is required.

## Evidence and deliverable

Provide the boundary, the artifact/access obtained, the firmware version, and the control (fusing/secure-boot/signing) result. Keep to the owned device; redact extracted secrets. Attach minimal replay, expected/observed, rival explanation, falsifier, boundaries not assessed.

## Versions and tool limitations

Pin the firmware/bootloader and silicon revisions — protections and fuse states are device- and version-specific. No device behavior was verified by this content; confirm on the owned device first.

## Remediation and detection

Fuse/disable debug interfaces in production, encrypt firmware and enforce secure boot with rollback protection, sign updates, store keys in a secure element (never in firmware), and authenticate device-to-cloud protocols. Add a regression that an unsigned update and a debug-port access are refused. Detect anomalous update/boot behavior server-side.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A boundary yields access/artifact (UART root, flash dump, used hardcoded key, accepted unsigned update) on the owned device where hardening would refuse: CONFIRMED; FAIL. |
| Benign refutation | Fused ports / secure boot / signing / secure element defeats the attempt: REFUTED; PASS for the control. |
| Insufficient evidence | A debug pad found but no access/artifact obtained: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/iot/offensive-iot/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's firmware/hardware-debug/boot/update/key-storage craft, re-expressed as owned-device bench experiments with hardening controls, replacing attacks on fielded devices with bounded, bench-scoped weakness proof. Composes with the wireless skills, `rt-crypto-attacks`, `root-of-trust-reasoning`.
