---
name: rt-wifi
description: "Red-team assessment of 802.11 WLAN security posture in an authorized, controlled RF lab: an umbrella over recon, deauth/PMF, evil-twin, WPA2-PSK handshake/provisioning, WPA3-SAE, WPA-Enterprise/EAP and WPS, routing each to its specific skill. Re-expressed as a scoped WLAN posture assessment on owned networks with synthetic credentials and negative controls instead of attacks on third-party networks."
---

# 802.11 WLAN Posture Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the assessment below.
This revision restores the upstream's Wi-Fi material as an umbrella posture assessment over the specific wireless skills, bounded by authorization and spectrum law, testing an owned WLAN rather than third-party networks.

## Scope and prerequisites

A WLAN posture assessment covers discovery, availability (deauth/PMF), rogue-AP susceptibility, and the authentication/cipher layer. Test only owned/in-scope networks in a controlled RF setting with synthetic credentials; respect spectrum/monitoring law. Prove each weakness against the owned WLAN with a negative control.

Declare the scoped SSIDs, the RF environment, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Assessment areas (route to the specific skill)

- **Recon** — AP/client/cipher map → `rt-wifi-recon`.
- **Availability / management frames** — deauth/disassoc, PMF/802.11w → `rt-deauth-disassoc`.
- **Rogue AP / credential capture** → `rt-evil-twin`, `rt-wpa-enterprise`.
- **WPA2-PSK** — handshake/PMKID, provisioning policy → `rt-wpa2-psk`.
- **WPA3-SAE** — Dragonblood-class, transition-mode downgrade → `rt-wpa3-sae`.
- **WPA-Enterprise/EAP** — RADIUS/evil-twin, weak EAP → `rt-wpa-enterprise`.
- **WPS** — PIN/Pixie-Dust → `rt-wps`.
- **Protocol flaws** — KRACK/FragAttacks → `rt-krack-fragattacks`.

## Mechanism and observation

Assess each area against the owned WLAN's intended posture.

**Firstness:** Record the per-area observation (cipher, PMF state, WPS state, handshake/SAE behavior) from the specific skill. **Secondness:** State the target posture (WPA3 or WPA2 with PMF, no WPS, strong PSK/EAP) and the deviation. **Thirdness:** Infer a posture finding only after the specific skill confirms it under control.

## Abduction and refutation

**Hypothesis:** The WLAN has a posture weakness (weak cipher, no PMF, WPS on, weak PSK/EAP, downgrade-able transition mode).

**Competing benign explanation:** WPA3 with PMF is enforced; WPS is disabled; the PSK is high-entropy; EAP uses strong methods with proper server-cert validation; the guest/IoT SSID's weaker posture is intentional and segmented.

## Deduction and controls

The target WLAN meets its intended posture (positive control). A finding is a per-area deviation confirmed by the specific skill where the hardened posture would not allow it. The hardened posture (WPA3/PMF/no-WPS/strong-PSK-EAP) is the PASS control.

## Induction: bounded procedure

Owned WLAN; synthetic credentials.

1. **Map** with `rt-wifi-recon`.
2. **Route** each weakness area to its skill and run its bounded experiment (owned network, synthetic creds, negative control).
3. **Aggregate** the per-area results into a posture scorecard (PASS/WARN/FAIL per area).
4. **Control.** Confirm the hardened posture resists each tested area.

Record results including refutations. Keep per-area findings and control scores separate.

## Domain-specific failure modes

Testing a third-party network is out of scope and often illegal. An intentionally weaker segmented guest/IoT SSID is not a finding. A single area's weakness does not condemn the whole WLAN — score per area. Each area's depth and caveats live in its specific skill; this umbrella does not restate them.

## Evidence and deliverable

Provide the posture scorecard: per-area result, the specific-skill evidence, and the hardened-posture control. Keep to owned networks and synthetic credentials. Attach scope, expected/observed, rival explanation, falsifier, areas not assessed.

## Versions and tool limitations

Pin AP/supplicant firmware and adapter capabilities. Posture and attacks are version/hardware-specific. No WLAN behavior was verified by this content; test the owned WLAN to confirm.

## Remediation and detection

WPA3 (or WPA2 with mandatory PMF), disable WPS, high-entropy PSK or strong EAP with server-cert validation, avoid downgrade-able transition mode where feasible, segment guest/IoT, and deploy a WIDS. Add regressions per area. Detect deauth floods, rogue APs, and EAP downgrade.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A per-area weakness is confirmed by its skill on the owned WLAN where the hardened posture would not allow it: CONFIRMED; FAIL for that area. |
| Benign refutation | The hardened posture holds, or weaker guest/IoT posture is intentional/segmented: REFUTED; PASS. |
| Insufficient evidence | A suspected weakness not confirmed by the specific skill: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wifi/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's Wi-Fi material as a scoped posture umbrella routing to the specific wireless skills, replacing third-party attacks with a bounded, owned-WLAN scorecard. Composes with `rt-wifi-recon`, `rt-deauth-disassoc`, `rt-evil-twin`, `rt-wpa2-psk`, `rt-wpa3-sae`, `rt-wpa-enterprise`, `rt-wps`, `rt-krack-fragattacks`.
