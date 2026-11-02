---
name: rt-wpa-enterprise
description: "Red-team assessment of WPA-Enterprise (802.1X/EAP) trust: whether clients validate the RADIUS server certificate, evil-twin RADIUS credential (EAP identity/MSCHAPv2) capture, weak EAP method selection, and PMF. Re-expressed as a scoped experiment in an isolated RF lab with an owned client and synthetic domain credentials that measures server-cert validation with a hardened-supplicant control instead of harvesting real credentials."
---

# WPA-Enterprise (802.1X/EAP) Trust Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the WPA-Enterprise craft as a scoped server-cert-validation experiment in an isolated RF lab: it measures whether an owned client validates the RADIUS certificate before sending credentials, using synthetic credentials, rather than harvesting real ones.

## Scope and prerequisites

WPA-Enterprise security hinges on the client validating the RADIUS server certificate; a client that does not can be lured to a rogue RADIUS (evil twin) that captures the EAP identity and MSCHAPv2 challenge/response for offline attack. Work on an owned client provisioned with synthetic domain credentials in an isolated RF lab. Capture only synthetic credentials; respect spectrum law.

Declare the owned client/profile, the EAP method, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Missing/weak server-cert validation** — client sends credentials to any RADIUS claiming the SSID.
- **Evil-twin RADIUS** — rogue AP + hostapd-wpe captures EAP identity + MSCHAPv2 for offline cracking.
- **Weak EAP method** — EAP-MD5/LEAP/GTC exposure vs PEAP/EAP-TTLS vs certificate-based EAP-TLS.
- **PMF** — management-frame protection enforcement.

## Mechanism and observation

Stand up a rogue RADIUS in the lab; observe whether the owned client validates the cert before disclosing synthetic credentials.

**Firstness:** Record whether the owned client connected to the rogue RADIUS and disclosed the synthetic EAP identity/MSCHAPv2 (and whether that challenge is then offline-crackable for the synthetic password). **Secondness:** State the secure baseline (client validates the CA/server cert and refuses) and the deviation. **Thirdness:** Infer a validation finding only after the owned client is controlled-lured.

## Abduction and refutation

**Hypothesis:** The client does not validate the RADIUS certificate, so a rogue RADIUS captures the (synthetic) credential material.

**Competing benign explanation:** The client pins the CA/server cert and rejects the rogue RADIUS; EAP-TLS (mutual certs) has no crackable secret; the profile requires a specific server name; the capture is incomplete; PMF/other controls prevented the lure.

## Deduction and controls

A hardened supplicant refuses the rogue RADIUS (positive control). A confirmed finding has the owned client disclose the synthetic EAP/MSCHAPv2 to the rogue RADIUS where a cert-validating supplicant refuses. Predeclare the disclosure signal. CA/server-cert pinning / EAP-TLS / server-name match are PASS controls.

## Induction: bounded procedure

Isolated RF lab; owned client; synthetic credentials.

1. **Baseline.** Confirm the owned client's EAP profile and that it joins the legitimate lab RADIUS.
2. **Rogue RADIUS.** Stand up hostapd-wpe-class rogue AP/RADIUS for the SSID in the lab (optionally nudge reassociation per `rt-deauth-disassoc`).
3. **Observe validation.** Does the owned client check the cert and refuse, or disclose the synthetic EAP identity/MSCHAPv2?
4. **Offline (synthetic).** If MSCHAPv2 is captured, confirm crackability of the synthetic password as a strength measurement.
5. **Control.** Enable CA/server-cert validation (or EAP-TLS) and confirm the client refuses.

Record results including refutations. Keep finding and control status separate. Synthetic credentials only.

## Craft notes (leads)

hostapd-wpe captures EAP identities and MSCHAPv2 challenge/response; the MSCHAPv2 response is offline-crackable (asleap/hashcat) — hence the synthetic-password caveat. The root finding is almost always missing server-cert validation on the client, not a protocol break. EAP-TLS (mutual certificates) has no password secret to capture. Configure clients to validate the CA and the server name.

## Domain-specific failure modes

A client that validates the cert refuses the rogue RADIUS — the primary refutation and the fix. EAP-TLS has no crackable secret. An incomplete EAP exchange yields nothing. Capturing real domain credentials is never appropriate — synthetic only, in an isolated lab. Attacking a live enterprise WLAN is out of scope.

## Evidence and deliverable

Provide the EAP method, the client's validation behavior, the synthetic-credential disclosure (if any) and its crackability, and the cert-validation control result. Use synthetic credentials; keep them out of portable reports. Attach expected/observed, rival explanation (cert-validating/EAP-TLS), falsifier, cases not tested.

## Versions and tool limitations

Pin the supplicant and its cert-validation config and the EAP method — susceptibility is client-config-specific. No client behavior was verified by this content; test the owned client to confirm.

## Remediation and detection

Enforce server-cert validation (pin CA + server name) on all supplicants, prefer EAP-TLS (mutual certs), avoid weak EAP methods (MD5/LEAP), enforce PMF, and use a managed-profile to prevent user override. Add a regression that the client refuses a rogue RADIUS. Detect rogue RADIUS/evil-twin via WIDS.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The owned client discloses synthetic EAP/MSCHAPv2 to the rogue RADIUS where a cert-validating supplicant refuses: CONFIRMED missing-validation; FAIL. |
| Benign refutation | CA/server-cert validation or EAP-TLS makes the client refuse: REFUTED; PASS for the control. |
| Insufficient evidence | A partial EAP exchange with no disclosure: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wpa-enterprise/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's EAP/evil-twin-RADIUS craft as a scoped server-cert-validation experiment with synthetic credentials and a hardened-supplicant control, replacing real credential harvesting with bounded validation proof. Composes with `rt-evil-twin`, `rt-deauth-disassoc`, `token-trust-assessment`.
