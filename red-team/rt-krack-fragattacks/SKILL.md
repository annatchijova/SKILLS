---
name: rt-krack-fragattacks
description: "Red-team assessment of 802.11 protocol-flaw patch status: KRACK (key-reinstallation in the 4-way/group-key handshake) and FragAttacks (fragmentation/aggregation design and implementation flaws). Re-expressed as a scoped patch-verification experiment in an isolated RF lab against owned AP/client that confirms whether the stack is vulnerable or patched, with a patched-stack control, instead of attacks on live networks."
---

# KRACK / FragAttacks Patch-Status Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the experiment below.
This revision restores the KRACK/FragAttacks craft as a scoped patch-verification experiment in an isolated RF lab: it confirms whether the owned AP/client stack is vulnerable or patched to these protocol flaws, with a patched stack as the control, rather than attacking live networks.

## Scope and prerequisites

KRACK and FragAttacks are known protocol/implementation CVE classes; the practical question is patch status on the specific AP/client. Work on owned devices in an isolated RF lab. Respect spectrum law.

Declare the owned AP/client firmware, the RF isolation, attempt budget, stop condition. Firmware-version-only review yields a hypothesis marked NOT TESTED (confirm by test where possible).

## Attack surface and classes

- **KRACK** — key reinstallation by replaying handshake messages (4-way, group-key, FT handshake), resetting nonces/replay counters and enabling decryption/replay on vulnerable stacks.
- **FragAttacks** — design flaws (plaintext injection, mixed-key fragment reassembly, cached-fragment) plus common implementation flaws; several are stack-specific.

## Mechanism and observation

Use the published test tools against the owned devices to determine vulnerability.

**Firstness:** Record whether the test reproduces the flaw (nonce reuse accepted, fragment injected/reassembled) on the owned stack. **Secondness:** State the expected patched behavior and the deviation. **Thirdness:** Infer "vulnerable" only after the test reproduces it under control on the owned device.

## Abduction and refutation

**Hypothesis:** The owned AP/client stack is unpatched for a KRACK or FragAttacks variant.

**Competing benign explanation:** The firmware is patched (the test reports not-vulnerable); the device rejects the replayed/retransmitted frame; the variant does not apply to this stack; the observed behavior is a test-harness artifact, not the device.

## Deduction and controls

A patched stack passes the test (positive control = not vulnerable). A confirmed finding reproduces the flaw on the owned device where a patched firmware does not. Predeclare the reproduction signal from the test tool. A patched stack passing is the PASS control.

## Induction: bounded procedure

Isolated RF lab; owned AP/client.

1. **Baseline.** Record firmware versions and expected CVE applicability.
2. **Run the published test** (the KRACK scripts / FragAttacks test tool) against the owned AP and client.
3. **Confirm per variant.** Record which variants the stack is vulnerable to vs patched.
4. **Patched control.** Update firmware (or test a known-patched device) and re-run; confirm not-vulnerable.
5. **Stop.** The deliverable is the patch-status matrix, not exploitation.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Both have authoritative test tools from the original research; use them rather than hand-rolling. KRACK is largely patched in current stacks but lingers in unmaintained firmware/IoT; FragAttacks has design variants that affect nearly all devices plus implementation variants that vary by stack. The finding is almost always "unpatched firmware", and the fix is updating it.

## Domain-specific failure modes

Patched firmware reports not-vulnerable — the primary refutation. A variant may not apply to a given stack. A test-harness artifact can look like a device flaw — corroborate. Inferring vulnerability from a version string without a test is weaker evidence (NOT TESTED). Live-network testing is out of scope.

## Evidence and deliverable

Provide the firmware versions, the per-variant test results (vulnerable/patched), and the patched-stack control. Keep to owned devices. Attach the test-tool output, expected/observed, rival explanation (patched/artifact), falsifier, variants not tested.

## Versions and tool limitations

Pin AP/client firmware — vulnerability is entirely patch-status-dependent. The test tools themselves have version/driver requirements. No device behavior was verified by this content; run the tests on the owned devices to confirm.

## Remediation and detection

Update AP and client firmware/drivers to patched versions; for unpatchable IoT, segment and monitor. Enforce WPA3/PMF where possible. Add a regression that the test tool reports not-vulnerable. Detect handshake-replay anomalies via WIDS where supported.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The test reproduces a KRACK/FragAttacks variant on the owned stack where a patched firmware does not: CONFIRMED; FAIL (scope to the variant/stack). |
| Benign refutation | The patched stack reports not-vulnerable / the variant does not apply: REFUTED; PASS for the control. |
| Insufficient evidence | Version suggests exposure but no test was run: NOT TESTED; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/wireless/offensive-krack-fragattacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the KRACK/FragAttacks material as a scoped patch-verification experiment against owned devices with a patched-stack control, replacing live attacks with a bounded patch-status matrix. Composes with `rt-wifi`, `rt-deauth-disassoc`, `known-defect-disposition`.
