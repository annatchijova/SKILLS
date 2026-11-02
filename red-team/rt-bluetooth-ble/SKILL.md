---
name: rt-bluetooth-ble
description: "Red-team assessment of Bluetooth Low Energy security: GATT service/characteristic enumeration and unauthenticated read/write, pairing/bonding mode and Just-Works vs authenticated pairing, link-layer sniffing, and replay/relay exposure. Re-expressed as a scoped experiment in a controlled RF setting against an owned BLE device that proves one boundary weakness with a negative control instead of attacks on others' devices."
---

# Bluetooth Low Energy Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the BLE craft as a scoped experiment against an owned BLE device in a controlled RF setting: it enumerates GATT, tests pairing strength and unauthenticated access, and proves one weakness with a control, rather than attacking others' devices.

## Scope and prerequisites

BLE security spans GATT access control, pairing/bonding strength, and link-layer confidentiality. Work on an owned BLE device (and its owned companion app). Prove a weakness against the owned device; do not interact with others' BLE devices. Respect spectrum law.

Declare the owned device, the RF environment, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **GATT access control** — services/characteristics readable/writable without authentication; sensitive characteristics exposed.
- **Pairing/bonding** — Just-Works (no MITM protection) vs Passkey/Numeric-Comparison/OOB; LE Secure Connections vs legacy.
- **Link-layer** — sniffing (where unencrypted), connection-parameter abuse.
- **Replay/relay** — replaying captured commands; relay/distance attacks on proximity auth.

## Mechanism and observation

Enumerate GATT and test the access/pairing controls against the owned device.

**Firstness:** Record which characteristics are readable/writable without auth, the pairing method negotiated, and whether a captured command replays. **Secondness:** State the expected protection (authenticated pairing, access-controlled characteristics, LE Secure Connections) and the deviation. **Thirdness:** Infer a weakness only after a controlled read/write/replay confirms it on the owned device.

## Abduction and refutation

**Hypothesis:** The device exposes sensitive GATT without authentication, uses Just-Works pairing, or accepts replayed commands.

**Competing benign explanation:** Sensitive characteristics require authenticated/encrypted access; pairing uses Passkey/Numeric-Comparison with LE Secure Connections; commands carry anti-replay (nonce/counter); the device is not actually the target (another owned device).

## Deduction and controls

An unauthenticated client cannot read/write sensitive characteristics or replay commands on a hardened device (positive control). A confirmed finding reads/writes a sensitive characteristic without auth, or replays a command, on the owned device where authenticated access/anti-replay would prevent it. Predeclare the characteristic/command. Authenticated pairing / access control / anti-replay are PASS controls.

## Induction: bounded procedure

Controlled RF; owned device.

1. **Enumerate.** Scan and connect (bluetoothctl/gatttool/nRF tools); map services and characteristics and their permissions.
2. **Unauthenticated access.** Attempt to read/write sensitive characteristics without pairing.
3. **Pairing.** Observe the negotiated pairing method; test whether Just-Works is accepted.
4. **Replay.** Capture an owned command and replay it; check for anti-replay.
5. **Control.** Confirm that authenticated pairing / access control / anti-replay refuse the above.

Record results including refutations. Keep finding and control status separate. Owned device only.

## Craft notes (leads)

GATT characteristics often lack per-characteristic authentication, exposing control/sensitive data to any connected client — the most common BLE finding. Just-Works pairing provides no MITM protection. Legacy pairing (pre-4.2) is weak; LE Secure Connections (ECDH) is the control. Many IoT BLE commands lack anti-replay. Sniffing needs the device to transmit unencrypted (or a captured pairing).

## Domain-specific failure modes

A characteristic that requires authenticated/encrypted access is not an unauthenticated finding. Just-Works may be acceptable for non-sensitive devices — scope the impact. Anti-replay (counter/nonce) defeats replay. Interacting with others' BLE devices is out of scope. Sniffing encrypted LE SC traffic yields nothing.

## Evidence and deliverable

Provide the GATT map, the unauthenticated read/write (if any), the pairing method, the replay result, and the control outcome. Keep to the owned device. Attach expected/observed, rival explanation, falsifier, characteristics/commands not tested.

## Versions and tool limitations

Pin the BLE version (4.x/5.x), pairing mode, and the sniffer/adapter. Capabilities are version/hardware-specific. No device behavior was verified by this content; test the owned device to confirm.

## Remediation and detection

Require authenticated, encrypted access for sensitive characteristics, use LE Secure Connections with Passkey/Numeric-Comparison (avoid Just-Works for sensitive functions), add anti-replay (counter/nonce) to commands, and minimize exposed characteristics. Add a regression that unauthenticated access and replay are refused.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A sensitive characteristic is read/written without auth, or a command replays, on the owned device where hardening refuses: CONFIRMED; FAIL. |
| Benign refutation | Authenticated access / LE SC pairing / anti-replay refuses it: REFUTED; PASS for the control. |
| Insufficient evidence | A readable characteristic of unclear sensitivity, or Just-Works on a non-sensitive device: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-bluetooth-ble/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's GATT/pairing/sniffing/replay craft as a scoped experiment against an owned BLE device with authenticated-access and anti-replay controls, replacing attacks on others' devices with bounded boundary proof. Composes with `rt-bluetooth-classic`, `rt-iot`, `rt-crypto-attacks`.
