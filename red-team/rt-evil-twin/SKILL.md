---
name: rt-evil-twin
description: "Red-team assessment of rogue-AP / evil-twin susceptibility: whether clients auto-associate to a spoofed SSID (karma/known-beacon), whether captive-portal credential capture works, and whether server-cert validation and PMF/WPA3 defeat it. Re-expressed as a scoped experiment in an isolated RF lab with an owned client and synthetic credentials that measures client trust behavior, not interception of real users."
---

# Evil-Twin / Rogue-AP Susceptibility Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision adapts the upstream's evil-twin craft as a scoped client-trust experiment in an isolated RF lab: it measures association, credential disclosure and traffic exposure as distinct outcomes, using synthetic credentials rather than capturing real users.

## Scope and prerequisites

An evil twin spoofs a legitimate SSID to get clients to associate and disclose credentials or traffic. Run only in an isolated/shielded RF lab with an owned client configured with synthetic credentials; never stand up a rogue AP where real users or third-party clients could connect, and respect spectrum law.

Declare the owned client/profile, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism and observation

A matching SSID alone does not authenticate an AP. Susceptibility depends on the network authentication mode and client profile. For WPA-Enterprise, server-certificate validation and trusted-CA/name policy authenticate the RADIUS server; PMF protects specified robust management frames after the relevant security association and does not authenticate the AP. WPA3-Personal/SAE and transition-mode behavior must be evaluated separately from Enterprise certificate validation.

**Firstness:** Record separately whether the owned client associated, which authentication method completed, whether any synthetic credential or challenge response was disclosed, and whether application traffic was exposed. **Secondness:** Compare each observation with expected behavior for that exact authentication mode and client policy. **Thirdness:** Infer only the demonstrated property; association alone is not credential disclosure or plaintext traffic exposure.

## Abduction and refutation

**Hypothesis:** The client auto-associates to a same-SSID rogue AP (karma/known-beacon) and discloses a synthetic credential or routes traffic through it.

**Competing benign explanation:** The Enterprise client validates the expected server certificate/CA and rejects the rogue RADIUS; the client does not auto-join or requires user approval; the association was to the real AP; or the client associated but disclosed no credential and exposed no protected application traffic. Evaluate PMF and WPA3 against their own protection goals, not as substitutes for server authentication.

## Deduction and controls

A confirmed result names the observed proposition: rogue association, synthetic credential disclosure, challenge-response exposure, or application traffic exposure. For Enterprise credential disclosure, compare a client with correct server-certificate validation against one without it. Treat PMF as a management-frame protection control and WPA3/SAE as an authentication-mode control; neither alone proves rogue-AP resistance in every client/profile. Report each control's status separately.

## Induction: bounded procedure

Isolated RF lab; owned client; synthetic credentials.

1. **Baseline.** Confirm the owned client's profile and that it joins the legitimate lab AP.
2. **Stand up the rogue AP** (same SSID) in the isolated lab; optionally use a deauth nudge (`rt-deauth-disassoc`, DoS scope permitting) to prompt reassociation.
3. **Observe association.** Did the owned client auto-join the rogue AP?
4. **Credential capture (synthetic).** For a captive portal or EAP, observe whether the synthetic credential is disclosed to the rogue AP.
5. **Controls.** For Enterprise, configure and verify expected server-certificate validation and repeat. Separately test PMF's management-frame behavior and the chosen WPA3/transition configuration. Do not treat one control's result as evidence for another.

Record results including refutations. Keep finding and control status separate. Only the owned client and synthetic credentials are involved.

## Craft notes (leads)

hostapd/hostapd-wpe for the rogue AP/RADIUS; karma/known-beacon abuses clients that probe for and trust preferred SSIDs (feeds from `rt-wifi-recon` probe analysis). For WPA-Enterprise, a rogue RADIUS may observe an EAP identity or challenge exchange; whether reusable credentials are exposed depends on the EAP method and client validation policy (route to `rt-wpa-enterprise`). Strict server-certificate validation is the relevant Enterprise control. PMF protects specified management frames, and WPA3 controls depend on the chosen authentication mode; neither is a general substitute for server authentication.

## Domain-specific failure modes

A client that validates the expected server certificate rejects the rogue Enterprise RADIUS exchange for the tested profile — the primary EAP refutation. PMF protects its specified management frames, not AP identity. Evaluate WPA3 against the selected authentication mode. A client that does not auto-join refutes automatic association only; user approval can still lead to exposure. Standing up a rogue AP where real users could connect is out of scope and harmful. Capturing real credentials is never appropriate — synthetic only.

## Evidence and deliverable

Provide the rogue-AP setup, the owned client's association behavior, the synthetic-credential capture (or refusal), and the cert-validation/PMF control result. Keep to the isolated lab. Attach expected/observed, rival explanation (joined real AP), falsifier, controls not exercised.

## Versions and tool limitations

Pin client OS/supplicant and its cert-validation/auto-join behavior — susceptibility is client-config-specific. No client behavior was verified by this content; test the owned client to confirm.

## Remediation and detection

Enforce server-cert validation (EAP) and pin the CA, require PMF/WPA3, disable auto-join to open/known SSIDs, remove stale network profiles (probe hygiene), and deploy a WIDS to detect rogue APs. Add a regression that the client refuses the same-SSID rogue AP. Detect duplicate-BSSID/same-SSID anomalies.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Name the system and proposition confirmed (association, credential disclosure, or traffic exposure) and its evidence. A failed control is FAIL only for the property that control is intended to provide. |
| Benign refutation | Correct Enterprise server-certificate validation rejects the rogue RADIUS exchange: REFUTED for that credential-disclosure path. Record PMF, WPA3 and auto-join outcomes against their separate properties. |
| Insufficient evidence | The client joined but no disclosure/traffic shown, or it joined the real AP: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-evil-twin/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's rogue-AP/karma/captive-portal craft as a scoped client-trust experiment in an isolated lab with synthetic credentials and cert-validation/PMF controls, replacing interception of real users with bounded susceptibility proof. Composes with `rt-wifi-recon`, `rt-deauth-disassoc`, `rt-wpa-enterprise`.
