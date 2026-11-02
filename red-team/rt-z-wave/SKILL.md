---
name: rt-z-wave
description: "Red-team assessment of Z-Wave security: S0 vs S2 security-class usage, the legacy S0 key-exchange weakness, insecure inclusion/pairing, and replay/injection on unencrypted or weakly-keyed command classes. Re-expressed as a scoped experiment in an isolated RF lab against an owned Z-Wave network with synthetic keys and an S2-hardened control instead of attacks on others' devices."
---

# Z-Wave Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the Z-Wave craft as a scoped experiment in an isolated RF lab against an owned network: it tests security-class usage, the legacy S0 inclusion weakness, and replay, with S2 as the hardened control, rather than attacking others' devices.

## Scope and prerequisites

Z-Wave security hinges on the security class: legacy S0 has a known key-exchange weakness during inclusion, while S2 uses ECDH with out-of-band authentication. Work on an owned Z-Wave network/controller with synthetic keys in an isolated RF lab (sub-GHz). Respect spectrum law. Recover/inject only synthetic material.

Declare the owned network, the security class in use, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **S0 inclusion weakness** — the S0 key is exchanged protected by a well-known temporary key during inclusion; sniffing the inclusion reveals the network key.
- **Insecure/weak inclusion** — devices included without security, or downgraded to S0.
- **Command-class exposure** — unencrypted/weakly-keyed command classes accepting commands.
- **Replay/injection** — replaying captured commands where anti-replay is weak.

## Mechanism and observation

Observe inclusion and command traffic on the owned network; test key exposure and replay.

**Firstness:** Record the security class negotiated, whether the synthetic S0 key is recoverable from a captured inclusion, and whether a captured command replays. **Secondness:** State the secure baseline (S2 with OOB authentication, no S0 downgrade, anti-replay) and the deviation. **Thirdness:** Infer a weakness only after a controlled test confirms it on the owned network.

## Abduction and refutation

**Hypothesis:** The network uses S0 (or allows downgrade), exposing the key at inclusion, or accepts replayed commands.

**Competing benign explanation:** S2 with OOB DSK authentication is enforced (no exposed inclusion key); the controller refuses S0 downgrade; command classes are encrypted under S2; anti-replay (nonce) holds; another owned network was observed.

## Deduction and controls

An S2-hardened network protects keys and rejects replay (positive control). A confirmed finding recovers the synthetic S0 key from a captured inclusion, or replays a command, on the owned network where S2 does not. Predeclare the signal. S2/OOB authentication / no-S0-downgrade / anti-replay are PASS controls.

## Induction: bounded procedure

Isolated sub-GHz RF lab; owned network; synthetic keys.

1. **Capture inclusion.** Sniff an owned device's inclusion (Z-Wave sniffer / SDR); note the security class.
2. **S0 key exposure.** If S0 is used, attempt to recover the synthetic network key from the inclusion using the well-known temporary key.
3. **Downgrade.** Test whether the controller can be pushed to include a device at S0 instead of S2.
4. **Replay.** Replay a captured owned command; check anti-replay.
5. **Control.** Confirm S2/OOB authentication and anti-replay refuse the above.

Record results including refutations. Keep finding and control status separate. Synthetic keys only.

## Craft notes (leads)

The signature Z-Wave finding is S0 inclusion key exposure (the temporary key is well-known), so a sniffed inclusion reveals the network key — S2's ECDH + OOB DSK authentication fixes this. S0-downgrade acceptance re-opens the weakness even on S2-capable networks. Unencrypted command classes and weak anti-replay enable injection/replay. Sub-GHz SDR or a Z-Wave sniffer is needed.

## Domain-specific failure modes

S2 with OOB authentication defeats the inclusion-key attack — the primary refutation. A controller that refuses S0 downgrade is hardened. Encrypted command classes under S2 resist injection. Interacting with others' networks is out of scope; synthetic keys only. Sub-GHz transmission must respect spectrum law.

## Evidence and deliverable

Provide the security class, the captured inclusion, the synthetic S0-key recovery (or failure), the downgrade and replay results, and the S2-hardened control. Keep to the owned network. Attach expected/observed, rival explanation (S2/OOB), falsifier, cases not tested.

## Versions and tool limitations

Pin the Z-Wave chip/SDK and security class support — exposure is S0-vs-S2 dependent. The sniffer/SDR has coverage limits. No network behavior was verified by this content; test the owned network to confirm.

## Remediation and detection

Use S2 with OOB DSK authentication everywhere, refuse S0 downgrade, encrypt command classes, enforce anti-replay, and retire S0-only devices. Add a regression that S0 inclusion-key recovery and replay are refused. Segment the controller.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The synthetic S0 key is recovered from a captured inclusion, or a command replays, on the owned network where S2 does not: CONFIRMED; FAIL. |
| Benign refutation | S2/OOB authentication / no-downgrade / anti-replay refuses it: REFUTED; PASS for the control. |
| Insufficient evidence | A captured inclusion that could not be decrypted, or unclear security class: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-z-wave/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's S0/S2, inclusion and replay craft as a scoped experiment against an owned network with synthetic keys and an S2-hardened control, replacing attacks on others' devices with bounded key-exposure and replay proof. Composes with `rt-zigbee-thread-matter`, `rt-lorawan-sub-ghz`, `rt-iot`.
