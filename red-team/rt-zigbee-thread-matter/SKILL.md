---
name: rt-zigbee-thread-matter
description: "Red-team assessment of IEEE 802.15.4 mesh security (Zigbee, Thread, Matter): network/link-key provisioning and the classic Zigbee open-join / default-Trust-Center-link-key exposure, commissioning weaknesses, key transport, and replay. Re-expressed as a scoped experiment in an isolated RF lab against an owned network with synthetic keys and a hardened-commissioning control instead of attacks on others' devices."
---

# 802.15.4 Mesh (Zigbee/Thread/Matter) Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the 802.15.4-mesh craft as a scoped experiment in an isolated RF lab against an owned network: it tests key provisioning, commissioning, and replay with synthetic keys, with hardened commissioning as the control, rather than attacking others' devices.

## Scope and prerequisites

Zigbee/Thread/Matter secure a mesh with network and link keys; the classic weaknesses are insecure joining and the well-known default Trust-Center link key. Work on an owned network/coordinator with synthetic keys in an isolated RF lab; respect spectrum law. Recover/inject only synthetic material.

Declare the owned network, stack (Zigbee/Thread/Matter), the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Insecure join / key transport** — a device joining receives the network key encrypted with a link key; the well-known default Zigbee Trust-Center link key exposes the network key if used.
- **Open commissioning** — permit-join left open; weak install codes.
- **Thread/Matter commissioning** — commissioning credential strength, PASE/CASE handshake posture, out-of-band secret.
- **Replay / injection** — replaying captured commands where anti-replay/frame-counter is weak.

## Mechanism and observation

Observe a join/commissioning on the owned network and test key exposure and replay.

**Firstness:** Record whether the (synthetic) network key is recoverable from a captured join using the default link key, whether permit-join is open, and whether a captured command replays. **Secondness:** State the secure baseline (unique install codes, non-default link keys, closed permit-join, frame-counter anti-replay, Matter certified commissioning) and the deviation. **Thirdness:** Infer a weakness only after a controlled test confirms it on the owned network.

## Abduction and refutation

**Hypothesis:** The network uses the default/weak link key or open commissioning, exposing the network key, or accepts replayed commands.

**Competing benign explanation:** Unique per-device install codes and non-default link keys are used (join is secure); permit-join is closed; Thread/Matter use strong commissioning with OOB secrets; frame counters enforce anti-replay; another owned network was observed.

## Deduction and controls

A hardened mesh protects the network key and rejects replay (positive control). A confirmed finding recovers the synthetic network key from a join (default link key / open join) or replays a command on the owned network where hardened commissioning does not. Predeclare the signal. Unique install codes / non-default keys / closed join / frame counters are PASS controls.

## Induction: bounded procedure

Isolated RF lab; owned network; synthetic keys.

1. **Capture a join/commissioning** on the owned network (802.15.4 sniffer).
2. **Key transport.** Attempt to decrypt the network-key transport using the default Trust-Center link key; succeeds only if the default/weak key is used.
3. **Commissioning posture.** Check permit-join state and install-code/credential strength (Zigbee); PASE/CASE and OOB secret posture (Thread/Matter).
4. **Replay.** Replay a captured owned command; check frame-counter anti-replay.
5. **Control.** Confirm unique install codes / non-default keys / closed join / anti-replay refuse the above.

Record results including refutations. Keep finding and control status separate. Synthetic keys only.

## Craft notes (leads)

The signature Zigbee finding is use of the well-known default Trust-Center link key, which lets a sniffed join reveal the network key — install codes/unique link keys are the fix. Open permit-join is a commissioning finding. Thread and Matter use stronger commissioning (ECDH-based PASE/CASE, OOB passcodes); findings there are weak passcodes or misconfiguration, not a default key. Frame counters provide anti-replay.

## Domain-specific failure modes

Unique install codes / non-default link keys defeat the key-transport attack — the primary refutation. Closed permit-join prevents rogue joins. Matter/Thread's modern commissioning resists the classic Zigbee weaknesses. Weak frame-counter handling enables replay. Interacting with others' meshes is out of scope; synthetic keys only.

## Evidence and deliverable

Provide the captured join/commissioning, the synthetic network-key recovery (or failure), the permit-join/credential posture, the replay result, and the hardened-commissioning control. Keep to the owned network. Attach expected/observed, rival explanation, falsifier, cases not tested.

## Versions and tool limitations

Pin the stack (Zigbee version/profile, Thread, Matter) and the 802.15.4 sniffer. Exposure is configuration- and stack-specific. No network behavior was verified by this content; test the owned network to confirm.

## Remediation and detection

Use unique per-device install codes and non-default link keys, close permit-join except during commissioning, prefer Thread/Matter with strong OOB passcodes, enforce frame-counter anti-replay, and segment IoT. Add a regression that the default-link-key decryption and replay are refused.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The synthetic network key is recovered via the default link key / open join, or a command replays, on the owned network where hardened commissioning does not: CONFIRMED; FAIL. |
| Benign refutation | Unique install codes / non-default keys / closed join / anti-replay refuses it: REFUTED; PASS for the control. |
| Insufficient evidence | A captured join that could not be decrypted, or unclear commissioning posture: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-zigbee-thread-matter/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's key-transport/commissioning/replay craft as a scoped experiment against an owned mesh with synthetic keys and hardened-commissioning controls, replacing attacks on others' devices with bounded key-exposure and replay proof. Composes with `rt-z-wave`, `rt-iot`, `rt-crypto-attacks`.
