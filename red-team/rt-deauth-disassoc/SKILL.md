---
name: rt-deauth-disassoc
description: "Red-team assessment of 802.11 management-frame protection: whether deauthentication/disassociation frames can disrupt or deauth clients, and whether 802.11w/PMF defeats them. Re-expressed as a scoped availability-and-PMF experiment in an isolated RF lab against an owned AP and client, measuring whether management frames are protected, with explicit DoS-scope handling instead of disrupting live networks."
---

# Management-Frame Protection (Deauth/Disassoc) Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the upstream's deauth craft as a scoped PMF-effectiveness experiment in an isolated RF lab: it measures whether management frames are protected (802.11w), against an owned AP/client, with DoS scope handled explicitly, rather than disrupting live networks.

## Scope and prerequisites

Deauth/disassoc is fundamentally a DoS/availability technique — if the engagement excludes DoS, the deliverable is the PMF posture, not an executed flood. Run only in an isolated/shielded RF lab against an owned AP and client; never transmit deauth against third-party networks (illegal and disruptive). Respect spectrum law.

Declare the owned AP/client, the RF isolation, the DoS scope, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism and observation

Unprotected 802.11 management frames can be spoofed to deauth a client; 802.11w (PMF) cryptographically protects them.

**Firstness:** Record whether a spoofed deauth disconnected the owned client (lab) or was ignored (PMF). **Secondness:** State the expected protection (PMF required → management frames authenticated) and the deviation. **Thirdness:** Infer "management frames unprotected" only after the owned client is controlled-disconnected where PMF would prevent it.

## Abduction and refutation

**Hypothesis:** The AP/client accept spoofed deauth/disassoc, allowing targeted disconnection (and a precursor to evil-twin/handshake capture).

**Competing benign explanation:** PMF/802.11w is enabled and the spoofed frame is ignored; the disconnect was unrelated RF interference; the client roamed; management-frame protection is mandatory on this AP.

## Deduction and controls

With PMF off, the spoofed deauth disconnects the owned client (demonstration); with PMF on it must be ignored. A confirmed finding disconnects the owned client via spoofed frames where a PMF-enabled config ignores them. Predeclare the disconnect signal. PMF/802.11w ignoring the frame is the PASS control.

## Induction: bounded procedure

Isolated RF lab; owned AP/client.

1. **Baseline.** Associate the owned client; confirm a stable connection and the AP's PMF setting.
2. **PMF-off case.** With PMF disabled on the lab AP, send a bounded spoofed deauth to the owned client; observe disconnection. If DoS is out of scope, confirm the PMF setting from configuration instead of flooding.
3. **PMF-on control.** Enable PMF/802.11w; repeat; confirm the client is not disconnected.
4. **Stop.** Demonstrate the single targeted disconnect (or the config posture); do not flood or sustain.

Record results including refutations. Keep the finding (frames unprotected) separate from the control (PMF). Respect DoS scope throughout.

## Craft notes (leads)

aireplay-ng/mdk4 send deauth; the finding is really "PMF not enforced". Deauth is a precursor: it forces a reconnect to capture a WPA2 handshake (`rt-wpa2-psk`) or to push a client to an evil twin (`rt-evil-twin`). WPA3 mandates PMF; WPA2 can enable it as required/optional. A targeted single deauth proves the posture without a sustained DoS.

## Domain-specific failure modes

PMF enabled defeats the attack — a PASS, and the primary refutation. A disconnect from interference/roaming is not a deauth finding. Flooding a live network is illegal and out of scope. If DoS is excluded, report the PMF posture from configuration rather than executing disruption.

## Evidence and deliverable

Provide the PMF posture, the targeted-disconnect result (PMF-off lab) vs the PMF-on control, and the DoS-scope handling. Keep to the isolated lab. Attach expected/observed, rival explanation (interference/roaming), falsifier, and whether a flood was deliberately not run.

## Versions and tool limitations

Pin AP/client firmware and PMF capability — 802.11w support varies. No network behavior was verified by this content; test the owned lab to confirm.

## Remediation and detection

Enforce PMF/802.11w (required), prefer WPA3, and deploy a WIDS to detect deauth floods and spoofed management frames. Add a regression that a spoofed deauth is ignored. Alert on management-frame anomalies and mass disconnects.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A spoofed deauth disconnects the owned client (PMF-off lab) where PMF-on ignores it: CONFIRMED management-frames-unprotected; FAIL (availability impact scoped). |
| Benign refutation | PMF/802.11w ignores the frame: REFUTED; PASS for the control. |
| Insufficient evidence | A disconnect attributable to interference/roaming, or DoS out of scope with only config posture: CANDIDATE/NOT TESTED; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-deauth-disassoc/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's deauth craft as a scoped PMF-effectiveness experiment in an isolated lab with explicit DoS-scope handling, replacing live-network disruption with bounded posture proof. Composes with `rt-wpa2-psk`, `rt-evil-twin`, `rt-wifi`.
