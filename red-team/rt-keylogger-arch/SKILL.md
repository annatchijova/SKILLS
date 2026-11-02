---
name: rt-keylogger-arch
description: "Blue-team assessment of keylogging / input-capture detection and defense: understanding the capture mechanisms (kernel/user hooks, raw input, accessibility APIs, hardware) so defenders can detect them, and measuring whether endpoint controls catch an authorized emulation. Re-expressed as a detection-and-prevention exercise on an owned lab host with a benign input-capture stub and PASS/WARN/FAIL scoring, not an implementation guide for covert surveillance."
---

# Input-Capture Detection and Defense Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the detection exercise below.
This revision reframes the upstream's keylogger-architecture material toward defense: it explains input-capture mechanisms so a defender can detect and prevent them, and measures endpoint controls against an authorized, benign emulation. It is not an implementation guide for covert surveillance. Compose with `detection-engineering`.

## Scope and prerequisites

Keylogging is surveillance; building a covert one against people is out of scope and can be unlawful. The legitimate purpose here is defensive: understand the capture mechanisms to detect and block them. Emulate only a benign, consented input-capture stub on an owned lab host (no real user's keystrokes), with the goal of measuring detection and prevention.

Declare the lab host, the endpoint controls (EDR/AV/OS protections), the benign emulation, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Capture mechanism classes (as detection targets)

- **User-mode hooks** — `SetWindowsHookEx`/event taps; detectable by hook enumeration and API telemetry.
- **Raw input / polling** — `GetAsyncKeyState`/raw-input registration; detectable by behavioral analytics.
- **Kernel/driver** — filter drivers; detectable by driver-load and code-integrity controls.
- **Accessibility APIs** — assistive interfaces abused for capture; detectable by API-grant monitoring.
- **Hardware** — inline devices; detectable by physical inspection and USB-device policy.
- **Exfiltration** — how captured data would leave (routes to `rt-data-exfiltration` for the channel).

## Mechanism and observation

Emulate one benign capture mechanism, then measure whether endpoint controls detect/prevent it.

**Firstness:** Record what the benign stub did (registered a hook, loaded a driver) and which control alerted/blocked. **Secondness:** State the expected detection/prevention and the deviation. **Thirdness:** Infer a gap only after an emulated mechanism evades a control that should catch it, under control.

## Abduction and refutation

**Hypothesis:** A given capture mechanism can run without detection or prevention (a defensive gap).

**Competing benign explanation:** EDR enumerates and flags the hook; driver signing/HVCI blocks the kernel path; the accessibility grant is monitored and alerts; AV detects the known pattern; the emulation did not actually register the mechanism.

## Deduction and controls

Normal input handling produces no alert (positive control = no false positive). A confirmed gap shows the benign emulated mechanism running undetected/unblocked where a hardened endpoint would catch it. Predeclare the detection/prevention signal. Hook enumeration / driver-signing-HVCI / accessibility monitoring / AV detection are PASS controls.

## Induction: bounded procedure

Owned lab host; benign consented stub.

1. **Baseline.** Run normal input handling; confirm no false alerts.
2. **Emulate one mechanism** with the benign stub (a hook that counts, not captures, keystrokes; a benign test driver load in a test-signing lab).
3. **Measure detection/prevention.** Did EDR flag the hook/driver? Did code integrity block it? Did accessibility-grant monitoring alert?
4. **Score.** PASS (detected/blocked), WARN (partial), FAIL (neither) per mechanism.
5. **Tune and re-test.** Add detections/controls for gaps; confirm closure.
6. **Control.** Confirm normal handling still does not alert.

Record results including refutations. Keep finding status separate from the control score. The emulation never captures real keystrokes.

## Craft notes (leads)

The defensive levers: hook enumeration (EDR can list installed hooks), driver signing + HVCI (blocks kernel capture), accessibility-API grant monitoring, USB-device policy (hardware), and exfiltration detection (the captured data must leave — see `rt-data-exfiltration`). Understanding the mechanism is what makes the detection specific rather than signature-based.

## Domain-specific failure modes

An undetected benign emulation may be an incomplete emulation, not a real gap. Hardware keyloggers evade software detection entirely — physical/USB policy is the control. Capturing a real person's keystrokes to "prove" it is never appropriate; the stub must be benign and consented. Exfiltration is a separate control layer.

## Evidence and deliverable

Provide the mechanism emulated, the detection/prevention controls that did/did not catch it, the score, and the tuning that closed gaps. Keep to the owned lab with a benign stub. Attach minimal replay, expected/observed, rival explanation, falsifier, mechanisms not assessed.

## Versions and tool limitations

Pin the OS build and endpoint-control versions — detection is product- and version-specific. No control behavior was verified by this content; reproduce on the lab first.

## Remediation and detection

Enumerate and alert on input hooks, enforce driver signing and HVCI, monitor accessibility-API grants, apply USB-device policy, and detect exfiltration channels. Add detections per gap and a regression that the emulated mechanism is now caught.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A benign emulated capture mechanism runs undetected/unblocked where a hardened endpoint would catch it: CONFIRMED defensive gap; control FAIL. |
| Benign refutation | EDR/code-integrity/monitoring detects or blocks it: REFUTED; control PASS. |
| Insufficient evidence | Partial detection or incomplete emulation: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/infrastructure/offensive-keylogger-arch/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's input-capture architecture as a defensive detection-and-prevention exercise with a benign consented emulation and PASS/WARN/FAIL scoring, replacing a surveillance-implementation guide with endpoint-control measurement. Composes with `detection-engineering`, `rt-data-exfiltration`.
