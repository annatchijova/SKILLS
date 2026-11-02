---
name: rt-wpa2-psk
description: "Red-team assessment of WPA2-Personal key strength and provisioning: 4-way-handshake and PMKID capture in an isolated RF lab, offline crackability of a synthetic PSK as a key-strength measurement, and provisioning-policy validation. Re-expressed as a scoped experiment against an owned AP with operator-supplied synthetic PSKs (one deliberately weak, one strong) that measures crackability without recovering production credentials."
---

# WPA2-Personal Key-Strength Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the WPA2-PSK craft as a scoped key-strength experiment in an isolated RF lab: it captures a handshake/PMKID for an owned AP and measures offline crackability of synthetic PSKs, with a strong PSK as the control, rather than recovering production credentials.

## Scope and prerequisites

WPA2-PSK security rests on PSK entropy: a captured handshake enables an offline dictionary/brute attack whose feasibility is the PSK's strength. Work on an owned AP in an isolated/shielded RF lab, provisioned with operator-supplied synthetic PSKs — one deliberately weak, one strong. Crack only the synthetic PSK; never capture or crack a production/third-party network's key. Respect spectrum law.

Declare the owned AP, the synthetic PSKs, the RF isolation, attempt/time budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism and observation

Capture the material that enables offline attack (4-way-handshake EAPOL, or PMKID from the first message where the AP supports it) for the owned network, then measure crackability.

**Firstness:** Record a valid capture (handshake/PMKID) and whether the synthetic weak PSK was recovered offline within budget, and the strong one was not. **Secondness:** State the policy (high-entropy PSK → offline attack infeasible) and the deviation. **Thirdness:** Infer a key-strength finding only after the controlled crack result is in.

## Abduction and refutation

**Hypothesis:** The provisioning policy permits (or deploys) a low-entropy PSK that is offline-crackable from a single captured handshake.

**Competing benign explanation:** The deployed PSK is high-entropy and uncrackable in budget; the capture is incomplete/mixed-session (no real attack material); PMKID is unavailable (depends on implementation) and no handshake was captured; the weak value was only an example config while deployment generates unique strong keys.

## Deduction and controls

A high-entropy PSK resists offline cracking within budget (positive control). A confirmed finding recovers the synthetic weak PSK from a lab capture where the strong PSK is not recovered. Predeclare the crack-success and budget. A strong PSK surviving the attack is the PASS control; provisioning that rejects the weak fixture is also a control.

## Induction: bounded procedure

Isolated RF lab; owned AP; synthetic PSKs.

1. **Provision.** Configure the lab AP with the synthetic weak PSK; associate the owned client.
2. **Capture.** Obtain a valid 4-way handshake (a reconnect, optionally nudged per `rt-deauth-disassoc` within DoS scope) or a PMKID; verify the capture is complete.
3. **Crack (synthetic).** Run a bounded offline attack (hashcat-class) against the capture using an owned wordlist; recover the synthetic weak PSK.
4. **Strong-PSK control.** Reprovision with the strong synthetic PSK; repeat; confirm it is not recovered in budget.
5. **Provisioning.** Test whether the provisioning path accepts the prohibited weak fixture.
6. **Stop.** Do not attempt any production/third-party key.

Record results including refutations. Keep the key-strength finding separate from the provisioning control. Synthetic keys only.

## Craft notes (leads)

The handshake (EAPOL) or a PMKID from the first message gives the offline material; PMKID availability depends on the AP implementation. Cracking speed is hardware-bound (GPU) — budget matters. The real finding is PSK entropy and the provisioning policy that allows weak keys, not the capture technique. A PMKID is not the PSK; a capture failure is not proof of strength.

## Domain-specific failure modes

A high-entropy PSK is uncrackable in practice — a PASS (WARN at most on the method). An incomplete/mixed handshake yields no attack material. PMKID absence can mean no capture, not a strong key. Capturing or cracking a production/third-party network is out of scope and illegal. Offline cracking of a known lab key measures nothing about an unknown production key's cost beyond the entropy argument — state that.

## Evidence and deliverable

Provide the capture (handshake/PMKID validity), the weak-PSK recovery and budget, the strong-PSK control result, and the provisioning-policy outcome. Use synthetic keys only; keep them out of portable reports. Attach expected/observed, rival explanation (incomplete capture), falsifier, cases not tested.

## Versions and tool limitations

Pin AP firmware (PMKID behavior), supplicant, and cracking hardware/wordlist. Crackability is entropy- and hardware-dependent. No network behavior was verified by this content; test the owned lab to confirm.

## Remediation and detection

Enforce high-entropy PSKs (or move to WPA3-SAE / Enterprise), unique per-deployment keys under policy, reject weak fixtures in provisioning, and rotate exposed keys. Prefer WPA3 (SAE resists offline attack by design — see `rt-wpa3-sae`). Detect mass deauth (handshake-capture precursor) via WIDS.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The synthetic weak PSK is recovered from a lab capture within budget where the strong PSK is not: CONFIRMED weak-key/provisioning; FAIL. |
| Benign refutation | The PSK is high-entropy and uncrackable in budget / provisioning rejects the weak fixture: REFUTED; PASS for the control. |
| Insufficient evidence | An incomplete capture or no PMKID/handshake: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wpa2-psk/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the WPA2-PSK handshake/PMKID and offline-cracking craft as a scoped key-strength experiment against an owned AP with synthetic PSKs and a strong-key control, replacing production-credential recovery with bounded crackability measurement. Composes with `rt-deauth-disassoc`, `rt-wpa3-sae`, `rt-wpa-enterprise`.
