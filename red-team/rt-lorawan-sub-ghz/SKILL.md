---
name: rt-lorawan-sub-ghz
description: "Red-team assessment of LoRaWAN and generic sub-GHz security: OTAA vs ABP provisioning and key management, join-procedure and nonce/replay handling, AppKey/session-key exposure, and unauthenticated/replayable generic sub-GHz (OOK/FSK) control links. Re-expressed as a scoped experiment in an isolated RF lab against owned devices with synthetic keys and a hardened-provisioning control instead of attacks on others' networks."
---

# LoRaWAN / Sub-GHz Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the LoRaWAN/sub-GHz craft as a scoped experiment in an isolated RF lab against owned devices: it tests provisioning, join/replay, and generic sub-GHz control-link security with synthetic keys, with hardened provisioning as the control, rather than attacking others' networks.

## Scope and prerequisites

LoRaWAN security rests on key management (OTAA root/session keys vs ABP static keys) and join/replay handling; generic sub-GHz devices (remotes, sensors on OOK/FSK) often have unauthenticated, replayable links. Work on owned devices/gateway with synthetic keys in an isolated/attenuated RF lab; respect spectrum/duty-cycle law. Recover/inject only synthetic material.

Declare the owned devices, the provisioning mode, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Provisioning** — ABP static session keys (no rotation) vs OTAA; AppKey storage/exposure; reused keys across devices.
- **Join procedure** — DevNonce/JoinNonce replay handling (LoRaWAN 1.0 vs 1.1), join-accept replay.
- **Session security** — frame-counter anti-replay; MIC validation.
- **Generic sub-GHz** — OOK/FSK remotes/sensors with no authentication (capture-and-replay) or static codes.

## Mechanism and observation

Observe join/uplink traffic or a generic sub-GHz control signal on the owned setup; test key exposure and replay.

**Firstness:** Record the provisioning mode, whether a synthetic key is exposed/reused, whether a join or uplink replays (counter handling), and whether a generic sub-GHz command replays. **Secondness:** State the secure baseline (OTAA with unique keys, nonce/counter anti-replay, authenticated sub-GHz with rolling codes) and the deviation. **Thirdness:** Infer a weakness only after a controlled test confirms it on the owned setup.

## Abduction and refutation

**Hypothesis:** The device uses static/reused keys (ABP), mishandles join/frame nonces (replayable), or a generic sub-GHz link is unauthenticated and replayable.

**Competing benign explanation:** OTAA with unique per-device keys and proper nonce handling (1.1) prevents replay; frame counters enforce anti-replay; the sub-GHz link uses rolling codes/authentication; keys are stored in a secure element; another owned device was observed.

## Deduction and controls

A hardened setup resists key exposure and replay (positive control). A confirmed finding exposes a synthetic key, replays a join/uplink, or replays a generic sub-GHz command on the owned setup where OTAA/anti-replay/rolling-codes do not. Predeclare the signal. OTAA + unique keys / nonce + frame-counter anti-replay / rolling codes are PASS controls.

## Induction: bounded procedure

Isolated RF lab; owned devices; synthetic keys.

1. **Capture.** Record a join and some uplinks (LoRaWAN) or a generic sub-GHz control transmission (SDR).
2. **Provisioning.** Determine OTAA vs ABP; check for reused/static synthetic keys and AppKey exposure.
3. **Replay.** Replay a captured join/uplink and observe nonce/frame-counter handling; for generic sub-GHz, replay the captured command to the owned receiver.
4. **Session integrity.** Confirm MIC/frame-counter behavior.
5. **Control.** Confirm OTAA + anti-replay (or rolling codes) refuse the above.

Record results including refutations. Keep finding and control status separate. Synthetic keys only; respect duty-cycle/spectrum limits.

## Craft notes (leads)

ABP's static session keys (no rotation) and reused AppKeys are the core LoRaWAN provisioning findings; OTAA with unique keys and 1.1 nonce handling is the control. Join/frame-counter replay depends on version and implementation. Generic sub-GHz (garage/remote/sensor) devices frequently use static codes with no authentication — a capture-and-replay class defeated by rolling codes. SDR (e.g. with a LoRa/sub-GHz front-end) is needed.

## Domain-specific failure modes

OTAA with unique keys and proper nonce handling defeats key-exposure/replay — the primary refutation. Rolling codes defeat generic sub-GHz replay. Frame counters enforce anti-replay. Reused keys across devices turn one exposure into many. Interacting with others' networks/devices is out of scope; respect duty-cycle law.

## Evidence and deliverable

Provide the provisioning mode, the synthetic-key exposure/reuse (if any), the join/uplink or sub-GHz replay result, and the hardened-provisioning control. Keep to owned devices. Attach expected/observed, rival explanation (OTAA/rolling-code), falsifier, cases not tested.

## Versions and tool limitations

Pin the LoRaWAN version (1.0.x vs 1.1) and the device/gateway firmware and SDR front-end — replay and nonce behavior are version-specific. No device behavior was verified by this content; test the owned setup to confirm.

## Remediation and detection

Use OTAA with unique per-device root keys (not ABP), store keys in a secure element, enforce nonce and frame-counter anti-replay (prefer 1.1), and use authenticated/rolling-code links for generic sub-GHz. Add a regression that join/command replay is refused. Monitor for counter resets and duplicate joins.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A synthetic key is exposed/reused, or a join/uplink/sub-GHz command replays, on the owned setup where OTAA/anti-replay/rolling-codes do not: CONFIRMED; FAIL. |
| Benign refutation | OTAA + unique keys / anti-replay / rolling codes refuses it: REFUTED; PASS for the control. |
| Insufficient evidence | A capture that could not be decoded, or unclear provisioning: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-lorawan-sub-ghz/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's OTAA/ABP, join-replay and generic-sub-GHz craft as a scoped experiment against owned devices with synthetic keys and a hardened-provisioning control, replacing attacks on others' networks with bounded key-exposure and replay proof. Composes with `rt-z-wave`, `rt-zigbee-thread-matter`, `rt-iot`.
