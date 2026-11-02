---
name: rt-wpa3-sae
description: "Red-team assessment of WPA3-SAE (Dragonfly) implementation security: transition-mode downgrade to WPA2, Dragonblood-class side-channel (timing/cache) and group-downgrade weaknesses, and PMF enforcement. Re-expressed as a scoped implementation experiment in an isolated RF lab against an owned AP that measures downgrade and side-channel exposure with a hardened-config control instead of attacks on live networks."
---

# WPA3-SAE Implementation Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the WPA3-SAE craft as a scoped implementation experiment in an isolated RF lab: it measures transition-mode downgrade and Dragonblood-class side-channel exposure against an owned AP, with a hardened WPA3-only config as the control, rather than attacking live networks.

## Scope and prerequisites

WPA3-SAE resists offline PSK attack by design, so findings are implementation- and configuration-level: downgrade to WPA2 in transition mode, and Dragonblood-class side channels in specific stacks. Work on an owned AP in an isolated RF lab. Respect spectrum law.

Declare the owned AP, the mode (WPA3-only vs transition), the RF isolation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Transition-mode downgrade** — WPA3/WPA2 mixed mode lets an attacker force a WPA2 handshake (then `rt-wpa2-psk` applies).
- **Dragonblood side channels** — timing and cache-based leakage in the SAE hash-to-group (password element derivation) in vulnerable implementations, enabling partial password partitioning.
- **Group downgrade** — forcing a weaker SAE group.
- **PMF** — WPA3 mandates PMF; confirm enforcement.

## Mechanism and observation

Test the owned AP's mode and SAE implementation.

**Firstness:** Record the negotiated authentication mode and whether a WPA2 handshake was obtained; separately record SAE side-channel measurements and PMF negotiation. **Secondness:** Compare downgrade behavior to the configured transition policy, side-channel behavior to the exact SAE implementation, and PMF state to its management-frame protection requirement. **Thirdness:** Infer only the property demonstrated by the corresponding test; PMF state does not establish downgrade or side-channel resistance.

## Abduction and refutation

**Hypothesis:** The deployment is downgrade-able (transition mode) or runs a Dragonblood-vulnerable SAE implementation.

**Competing benign explanation:** WPA3-only mode offers no WPA2 transition path for this profile; the tested SAE implementation has the relevant fixes; observed timing is noise rather than password-dependent; the group policy is expected. PMF can explain resistance to applicable management-frame attacks but does not refute a downgrade or SAE side-channel hypothesis.

## Deduction and controls

A WPA3-only configuration is a control for the transition-to-WPA2 path; a patched SAE implementation is a separate control for the tested side-channel class. PMF is measured as a management-frame control. Predeclare the downgrade handshake or statistical side-channel decision rule and report these control results separately.

## Induction: bounded procedure

Isolated RF lab; owned AP.

1. **Baseline.** Associate the owned client via WPA3-SAE; note the mode (transition vs WPA3-only) and PMF.
2. **Downgrade (transition mode).** Attempt to force a WPA2 handshake; if obtained, route to `rt-wpa2-psk` for the key-strength question.
3. **Side channel.** For a potentially vulnerable stack, measure SAE hash-to-group timing/cache behavior with statistical rigor across many samples; look for password-dependent variation.
4. **Group downgrade / PMF.** Test supported SAE group negotiation. Separately confirm PMF enforcement for its management-frame property.
5. **Controls.** Switch to WPA3-only to retest transition downgrade; deploy the applicable patched SAE build to retest the side channel. Record PMF only against its own test.

Record results including refutations. Keep finding and control status separate. Statistical rigor for any timing claim.

## Craft notes (leads)

The practical WPA3 finding may be transition-mode fallback to WPA2; that is not an SAE break. Dragonblood-class side channels affect specific implementations and require implementation-specific testing; a single timing sample is noise. WPA3-only mode addresses the transition path; applicable SAE fixes address the side channel; PMF addresses robust management-frame protection. SAE itself resists offline PSK attack — do not claim otherwise.

## Domain-specific failure modes

WPA3-only mode is a refutation for the tested WPA2 transition path; a relevant SAE fix is a separate refutation for the tested implementation-specific side channel. PMF does not refute either claim. A timing difference without statistical separation is noise. Claiming SAE is "cracked" offline like WPA2 is wrong — the finding is downgrade or implementation side channel, not the protocol. Live-network testing is out of scope.

## Evidence and deliverable

Provide the mode, the downgrade result (if transition), the side-channel statistics (if tested), the PMF state, and the WPA3-only control result. Keep to the owned lab. Attach expected/observed, rival explanation (noise/patched), falsifier, cases not tested.

## Versions and tool limitations

Pin AP/supplicant firmware and SAE implementation — Dragonblood exposure is implementation/version-specific. No network behavior was verified by this content; test the owned lab to confirm.

## Remediation and detection

Deploy WPA3-only (disable transition mode) where clients allow, patch SAE implementations (constant-time), enforce PMF, and fix strong SAE groups. Add a regression that downgrade is refused. Detect WPA2 handshakes on a WPA3 network and anomalous SAE negotiation.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A WPA2 downgrade is obtained in transition mode, or a password-dependent side channel is measured, where WPA3-only/patched does not: CONFIRMED; FAIL. |
| Benign refutation | WPA3-only refuses the tested WPA2 transition; patched SAE removes the measured side channel; or controlled measurements do not separate from noise: REFUTED for that claim. Score PMF separately. |
| Insufficient evidence | A timing hint without statistical separation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-wpa3-sae/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's transition-downgrade and Dragonblood craft as a scoped implementation experiment against an owned AP with a WPA3-only/patched control, replacing live-network attacks with bounded downgrade/side-channel measurement. Composes with `rt-wpa2-psk`, `rt-deauth-disassoc`, `rt-crypto-attacks`.
