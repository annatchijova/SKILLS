---
name: rt-wifi-recon
description: "Red-team reconnaissance of an authorized 802.11 environment: monitor-mode capture, AP and client enumeration, SSID/BSSID/channel/cipher mapping, hidden-SSID and probe-request analysis, and client-AP association mapping. Re-expressed as scoped passive observation of an owned/authorized WLAN in a controlled RF setting that builds a network map with negative controls, not interception of third-party traffic."
---

# 802.11 Reconnaissance Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the observation below.
This revision restores the upstream's Wi-Fi recon craft as scoped passive observation of an authorized WLAN: it maps APs, clients and ciphers from monitor-mode capture, bounded by authorization and spectrum law, rather than capturing third-party traffic.

## Scope and prerequisites

Wi-Fi recon maps the authorized wireless environment before any active test. Observe only the owned/in-scope WLAN; passive capture in a controlled RF setting; do not capture or decode third-party networks' traffic, and respect local spectrum/monitoring law.

Declare the scoped SSIDs/BSSIDs, the RF environment, the passive/active boundary. Active probing beyond scope is out of scope. Config-only review yields a hypothesis marked NOT TESTED.

## Observation surface

- **APs** — BSSID, SSID (including hidden via probe/association), channel, band, cipher/auth (WPA2/WPA3/Enterprise/open), signal.
- **Clients** — associated stations, probe requests (preferred-network leakage), MAC/OUI.
- **Associations** — which clients are on which AP; roaming behavior.
- **Posture** — management-frame protection (802.11w), PMF, WPS presence.

## Mechanism and observation

Put the adapter in monitor mode and capture/beacon-parse within scope.

**Firstness:** Record the observed APs/clients/ciphers and associations. **Secondness:** State the expected inventory (known in-scope APs, expected ciphers) and the deviation (rogue AP, weak cipher, hidden SSID revealed, PMF off). **Thirdness:** Infer a posture finding only after corroborated observation.

## Abduction and refutation

**Hypothesis:** The environment exposes a weakness (rogue/unknown AP, weak/open cipher, no PMF, WPS enabled, probe-leaked preferred networks).

**Competing benign explanation:** The "rogue" AP is a sanctioned device; the open SSID is an intentional guest network; the weak cipher is a legacy IoT VLAN by design; PMF is actually enabled; the probe requests are from out-of-scope clients.

## Deduction and controls

A known in-scope AP shows the expected posture (positive control). A finding is a corroborated deviation (unknown BSSID on the corporate SSID, PMF off where required, WPS on). Predeclare the expected inventory/posture. Matching the sanctioned inventory is a PASS.

## Induction: bounded procedure

Authorized WLAN; passive-first.

1. **Monitor mode.** Configure the adapter; confirm capture on the in-scope channels.
2. **Enumerate.** Collect APs (airodump-class), ciphers, clients, and associations within scope.
3. **Hidden SSID / probes.** Reveal hidden SSIDs via observed association; analyze probe requests for preferred-network leakage (own clients only).
4. **Posture.** Note PMF/802.11w, WPS, open/weak ciphers, and any unknown BSSID on a corporate SSID.
5. **Corroborate.** Confirm deviations against the sanctioned inventory before flagging.

Record results including refutations (sanctioned devices, intentional guest nets). Keep confirmed deviations separate from expected posture.

## Craft notes (leads)

airodump-ng/kismet for discovery; monitor mode + channel hopping to cover bands. Hidden SSIDs leak on client association. Probe requests reveal clients' preferred networks (a privacy/evil-twin precursor — feeds `rt-evil-twin`). An unknown BSSID advertising a corporate SSID is a rogue-AP signal. PMF/802.11w status gates deauth and some downgrade attacks.

## Domain-specific failure modes

A sanctioned AP/guest network is not a rogue finding — corroborate against inventory. Capturing or decoding third-party networks is out of scope and may be illegal. Probe requests from out-of-scope clients are not your data. Monitor-mode capture must stay within the authorized RF environment. Recon observes; it does not transmit (that is the active skills).

## Evidence and deliverable

Provide the AP/client/cipher map, the corroborated deviations (rogue AP, weak cipher, PMF off, WPS on), and the sanctioned-inventory comparison. Keep to in-scope networks. Attach the capture scope, expected/observed, rival explanation, falsifier, areas not covered.

## Versions and tool limitations

Pin the adapter/driver (monitor-mode and band support vary) and tooling. Spectrum coverage is hardware-limited. No network behavior was verified by this content; capture within the authorized environment to confirm.

## Remediation and detection

Maintain an AP inventory and detect rogue BSSIDs, enforce PMF/802.11w, disable WPS, retire open/weak ciphers (WPA2→WPA3), and segment guest/IoT. Minimize probe-request leakage (client-side MAC randomization, network cleanup). Deploy a WIDS to detect rogue APs and recon.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A corroborated deviation (rogue BSSID on the corporate SSID, PMF off where required, WPS enabled): CONFIRMED; FAIL for that control. |
| Benign refutation | The AP/cipher is sanctioned/intentional (guest net, legacy VLAN): REFUTED; PASS. |
| Insufficient evidence | A single-capture anomaly not corroborated against inventory: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wifi-recon/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's monitor-mode/enumeration/hidden-SSID/probe craft, re-expressed as scoped passive observation of an authorized WLAN with inventory controls, replacing third-party capture with a bounded network map. Composes with `rt-wifi`, `rt-evil-twin`, `rt-deauth-disassoc`.
