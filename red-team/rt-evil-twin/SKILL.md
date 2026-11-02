---
name: rt-evil-twin
description: "Red-team assessment of rogue-AP / evil-twin susceptibility: whether clients auto-associate to a spoofed SSID (karma/known-beacon), whether captive-portal credential capture works, and whether server-cert validation and PMF/WPA3 defeat it. Re-expressed as a scoped experiment in an isolated RF lab with an owned client and synthetic credentials that measures client trust behavior, not interception of real users."
---

# Evil-Twin / Rogue-AP Susceptibility Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the upstream's evil-twin craft as a scoped client-trust experiment in an isolated RF lab: it measures whether an owned client auto-associates to a spoofed SSID and whether server-cert validation / PMF / WPA3 defeat it, using synthetic credentials rather than capturing real users.

## Scope and prerequisites

An evil twin spoofs a legitimate SSID to get clients to associate and disclose credentials or traffic. Run only in an isolated/shielded RF lab with an owned client configured with synthetic credentials; never stand up a rogue AP where real users or third-party clients could connect, and respect spectrum law.

Declare the owned client/profile, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism and observation

A client that trusts an SSID by name (and lacks server-cert validation / PMF) can be lured to a rogue AP.

**Firstness:** Record whether the owned client auto-associated to the spoofed SSID and whether the captive portal / EAP exchange captured the synthetic credential. **Secondness:** State the expected protection (client validates server cert / requires PMF / does not blindly trust SSID) and the deviation. **Thirdness:** Infer susceptibility only after the owned client is controlled-lured.

## Abduction and refutation

**Hypothesis:** The client auto-associates to a same-SSID rogue AP (karma/known-beacon) and discloses a synthetic credential or routes traffic through it.

**Competing benign explanation:** The client requires server-cert validation (EAP) and rejects the rogue RADIUS; WPA3/PMF prevents the lure/downgrade; the client does not auto-join open/known SSIDs; the user must manually approve; the association was to the real AP.

## Deduction and controls

A properly-configured client only joins the legitimate AP (positive control). A confirmed finding has the owned client associate to the rogue AP and disclose the synthetic credential where cert-validation/PMF/WPA3 would prevent it. Predeclare the association + capture signal. Server-cert validation / PMF / WPA3 / no-auto-join are PASS controls.

## Induction: bounded procedure

Isolated RF lab; owned client; synthetic credentials.

1. **Baseline.** Confirm the owned client's profile and that it joins the legitimate lab AP.
2. **Stand up the rogue AP** (same SSID) in the isolated lab; optionally use a deauth nudge (`rt-deauth-disassoc`, DoS scope permitting) to prompt reassociation.
3. **Observe association.** Did the owned client auto-join the rogue AP?
4. **Credential capture (synthetic).** For a captive portal or EAP, observe whether the synthetic credential is disclosed to the rogue AP.
5. **Controls.** Enable server-cert validation / PMF / WPA3 and confirm the client refuses.

Record results including refutations. Keep finding and control status separate. Only the owned client and synthetic credentials are involved.

## Craft notes (leads)

hostapd/hostapd-wpe for the rogue AP/RADIUS; karma/known-beacon abuses clients that probe for and trust preferred SSIDs (feeds from `rt-wifi-recon` probe analysis). For WPA-Enterprise, the evil twin captures the EAP identity/MSCHAPv2 challenge unless the client validates the server certificate (route to `rt-wpa-enterprise`). WPA3/PMF and strict cert validation are the controls that defeat it.

## Domain-specific failure modes

A client that validates the server cert rejects the rogue RADIUS — the primary EAP refutation. WPA3/PMF prevents many lures. A client that does not auto-join (prompts the user) is a PASS. Standing up a rogue AP where real users could connect is out of scope and harmful. Capturing real credentials is never appropriate — synthetic only.

## Evidence and deliverable

Provide the rogue-AP setup, the owned client's association behavior, the synthetic-credential capture (or refusal), and the cert-validation/PMF control result. Keep to the isolated lab. Attach expected/observed, rival explanation (joined real AP), falsifier, controls not exercised.

## Versions and tool limitations

Pin client OS/supplicant and its cert-validation/auto-join behavior — susceptibility is client-config-specific. No client behavior was verified by this content; test the owned client to confirm.

## Remediation and detection

Enforce server-cert validation (EAP) and pin the CA, require PMF/WPA3, disable auto-join to open/known SSIDs, remove stale network profiles (probe hygiene), and deploy a WIDS to detect rogue APs. Add a regression that the client refuses the same-SSID rogue AP. Detect duplicate-BSSID/same-SSID anomalies.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The owned client auto-joins the rogue AP and discloses the synthetic credential where cert-validation/PMF would prevent it: CONFIRMED; FAIL. |
| Benign refutation | Server-cert validation / PMF / WPA3 / no-auto-join makes the client refuse: REFUTED; PASS for the control. |
| Insufficient evidence | The client joined but no disclosure/traffic shown, or it joined the real AP: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-evil-twin/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's rogue-AP/karma/captive-portal craft as a scoped client-trust experiment in an isolated lab with synthetic credentials and cert-validation/PMF controls, replacing interception of real users with bounded susceptibility proof. Composes with `rt-wifi-recon`, `rt-deauth-disassoc`, `rt-wpa-enterprise`.
