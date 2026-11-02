---
name: rt-wps
description: "Red-team assessment of Wi-Fi Protected Setup (WPS) exposure: online PIN brute-force and the Pixie-Dust offline attack against weak E-S1/E-S2 nonce generation, and whether WPS is enabled/locked. Re-expressed as a scoped experiment in an isolated RF lab against an owned AP that measures WPS exposure with a WPS-disabled control instead of attacks on live networks."
---

# WPS Exposure Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the WPS craft as a scoped exposure experiment in an isolated RF lab: it measures PIN brute-force and Pixie-Dust feasibility against an owned AP, with WPS-disabled as the control, rather than attacking live networks.

## Scope and prerequisites

WPS can expose the WPA2 PSK via an 8-digit PIN (structurally ~11,000 half-PIN guesses) or, where the AP generates weak E-S1/E-S2 nonces, via the offline Pixie-Dust attack. Work on an owned AP in an isolated RF lab; recover only the owned network's synthetic PSK; respect spectrum law.

Declare the owned AP, its WPS state, the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism and observation

Test whether WPS is enabled and whether the PIN is recoverable online (brute) or offline (Pixie-Dust).

**Firstness:** Record WPS state (enabled/locked), and whether the PIN/PSK was recovered via brute or Pixie-Dust on the owned AP. **Secondness:** State the secure baseline (WPS disabled, or locked with rate-limiting and strong nonces) and the deviation. **Thirdness:** Infer a WPS finding only after recovery is demonstrated under control.

## Abduction and refutation

**Hypothesis:** WPS is enabled and the PIN is recoverable (online brute without lockout, or Pixie-Dust due to weak nonce generation), yielding the PSK.

**Competing benign explanation:** WPS is disabled; the AP locks WPS after failed attempts (rate-limiting defeats brute); the AP uses strong random E-S1/E-S2 (Pixie-Dust fails); only push-button (PBC), not PIN, is enabled.

## Deduction and controls

A WPS-disabled AP exposes nothing (positive control). A confirmed finding recovers the PIN/PSK via brute or Pixie-Dust on the owned AP where a disabled/locked/strong-nonce config does not. Predeclare the recovery signal. WPS-disabled / lockout / strong nonces are PASS controls.

## Induction: bounded procedure

Isolated RF lab; owned AP.

1. **Check state.** Determine whether WPS (PIN method) is enabled and whether the AP locks after failures (reaver/wash-class, bounded).
2. **Pixie-Dust first.** Attempt the offline Pixie-Dust attack (fast, no sustained brute) against the owned AP; it succeeds only if nonces are weak.
3. **Online brute (bounded).** If Pixie-Dust fails and no lockout exists, a bounded PIN brute may recover it — keep it bounded and note lockout behavior.
4. **Recover (synthetic).** On success, recover the owned network's synthetic PSK; stop.
5. **Control.** Disable WPS (or confirm lockout/strong nonces) and confirm no recovery.

Record results including refutations. Keep finding and control status separate. Owned AP/synthetic PSK only.

## Craft notes (leads)

Pixie-Dust is the high-value case: it is offline and fast when the AP's E-S1/E-S2 nonces are weak/predictable (many older chipsets). The online PIN brute is slower and defeated by WPS lockout/rate-limiting. PBC-only (push button) is not PIN-brute-exposed. The fix is simply disabling WPS PIN. Recovery yields the PSK, bridging to `rt-wpa2-psk`.

## Domain-specific failure modes

WPS disabled defeats everything — the primary refutation. AP lockout/rate-limiting defeats online brute. Strong random nonces defeat Pixie-Dust. PBC-only is not exposed to PIN brute. A sustained brute against a live network is out of scope and disruptive; keep to the owned AP and bounded attempts.

## Evidence and deliverable

Provide the WPS state, the attack used (Pixie-Dust/brute), the PIN/synthetic-PSK recovery (or failure), and the WPS-disabled/lockout control result. Keep to the owned AP. Attach expected/observed, rival explanation (locked/strong-nonce), falsifier, cases not tested.

## Versions and tool limitations

Pin the AP firmware/chipset — Pixie-Dust exposure and lockout behavior are chipset/firmware-specific. No AP behavior was verified by this content; test the owned AP to confirm.

## Remediation and detection

Disable WPS PIN entirely (the only reliable fix); if WPS is required, use PBC only, enforce lockout/rate-limiting, and ensure strong nonce generation. Add a regression that WPS PIN is disabled. Detect WPS registrar brute-force attempts via the AP logs/WIDS.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Pixie-Dust or a bounded brute recovers the PIN/synthetic PSK on the owned AP where disabled/locked/strong-nonce does not: CONFIRMED; FAIL. |
| Benign refutation | WPS disabled / lockout / strong nonces / PBC-only defeats it: REFUTED; PASS for the control. |
| Insufficient evidence | WPS enabled but no recovery within bounded attempts: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wps/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's PIN-brute and Pixie-Dust craft as a scoped exposure experiment against an owned AP with a WPS-disabled control, replacing live-network attacks with bounded recovery proof. Composes with `rt-wpa2-psk`, `rt-wifi-recon`.
