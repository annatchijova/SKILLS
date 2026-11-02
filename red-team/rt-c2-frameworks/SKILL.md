---
name: rt-c2-frameworks
description: "Blue/purple-team assessment of command-and-control detection: understanding C2 beaconing, channel choices (HTTPS, DNS, named-pipe, cloud-fronted) and traffic-shaping so a defender can detect them, and measuring whether network/EDR controls catch emulated, authorized C2 in a lab. Re-expressed as a detection-coverage exercise with an authorized emulation profile and PASS/WARN/FAIL scoring instead of C2 deployment instructions."
---

# Command-and-Control Detection Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the detection exercise below.
This revision reframes the upstream's C2 material toward detection: it explains beacon and channel characteristics so a defender can recognize them, and measures whether controls detect an authorized emulation in a lab. It is a purple-team coverage exercise, not a C2 setup or evasion guide. Compose with `purple-team-exercise`, `traffic-as-evidence` and `detection-engineering`.

## Scope and prerequisites

The question is defensive: does the environment detect C2 activity? Emulate only with an authorized, sanctioned adversary-emulation profile (e.g. a sanctioned tool/benign agent) on an owned lab segment with the defender informed. Never stand up live C2 against systems you do not own; the deliverable is detection coverage, not a foothold.

Declare the lab segment, the emulation profile, the detection stack (NDR/EDR/proxy/DNS logging), attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Detection targets (C2 characteristics)

- **Beaconing** — periodic callbacks; detectable by interval regularity, jitter patterns, and low-and-slow volume over time.
- **Channel** — HTTPS (JA3/JA4, SNI, cert anomalies, URI patterns), DNS (high query volume, long/encoded labels, rare record types), named-pipe/SMB (lateral), cloud/domain-fronted (SNI vs Host mismatch, reputable-domain abuse).
- **Payload/staging** — initial loader, staging retrieval, in-memory execution (EDR telemetry).
- **Traffic shaping** — malleable profiles mimicking legitimate traffic; detectable by statistical and metadata analysis rather than signatures.

## Mechanism and observation

Emulate one C2 profile, then measure which controls detect it and at what layer.

**Firstness:** Record what the emulated beacon generated (network metadata, DNS queries, host telemetry) and which control alerted. **Secondness:** State the expected detection (beacon flagged by NDR; agent flagged by EDR; DNS tunneling flagged) and the deviation. **Thirdness:** Infer a detection gap only after an emulated profile evades a control that should catch it, under control.

## Abduction and refutation

**Hypothesis:** A given C2 channel/profile evades the current detection stack (a coverage gap).

**Competing benign explanation:** NDR already flags the beacon's periodicity/JA3; EDR flags the agent regardless of network evasion; DNS logging catches the tunneling; the proxy breaks TLS and inspects; the "evasion" simply did not run, or the emulation profile is unrealistic.

## Deduction and controls

A normal workload produces no C2 alert (positive control = no false positive). A confirmed gap shows an emulated C2 profile that generates no alert at any layer where a tuned stack would detect it. Predeclare the detection signal per layer. NDR beacon detection / EDR agent detection / DNS-tunnel detection / TLS inspection catching the profile are PASS controls.

## Induction: bounded purple-team procedure

Owned lab; authorized emulation profile; defender informed.

1. **Baseline.** Run normal traffic; confirm no false C2 alerts and capture what the stack logs.
2. **Emulate one profile.** Run the sanctioned emulation (a benign beaconing agent / a specified channel) on the lab host.
3. **Measure per layer.** Did NDR flag the beacon? EDR the agent/process? DNS logging the tunneling? The proxy the TLS metadata?
4. **Score coverage.** PASS (detected), WARN (partial/delayed), FAIL (undetected) per channel/profile.
5. **Tune and re-test.** Add detections for gaps (interval analysis, JA3/JA4, DNS entropy) and re-run to confirm closure.
6. **Control.** Confirm the normal workload still does not alert (false-positive control).

Record results including refutations. Keep finding status separate from the per-layer coverage score.

## Craft notes (leads)

Beacon periodicity and jitter are the strongest network signals; metadata (JA3/JA4, SNI/Host mismatch for fronting, DNS label entropy) beats payload signatures against encrypted/malleable C2. EDR provides host-side detection independent of network evasion — defense in depth. The purpose of understanding malleable profiles here is to build statistical/metadata detections, not to evade.

## Domain-specific failure modes

An undetected emulation can mean an unrealistic emulation profile, not a real gap — validate the profile. EDR can catch what NDR misses (and vice versa) — score per layer, not overall. A false-positive on normal traffic is its own finding. The goal is coverage measurement; standing up real C2 or tuning for evasion is out of scope.

## Evidence and deliverable

Provide the emulated channel/profile, the detection signals per layer (or their absence), the coverage score PASS/WARN/FAIL, and the tuning that closed any gap. Keep to the owned lab; share with the defender. Attach minimal replay, expected/observed, rival explanation (unrealistic profile), falsifier, channels not assessed.

## Versions and tool limitations

Pin the NDR/EDR/proxy/DNS-logging versions and the emulation profile — detection behavior is product- and profile-specific. No control behavior was verified by this content; reproduce on the lab first.

## Remediation and detection

Deploy beacon-interval and jitter analysis, JA3/JA4 and TLS-metadata detection, DNS-tunnel (entropy/volume/record-type) detection, SNI-vs-Host mismatch alerts for fronting, TLS inspection where feasible, and EDR for host-side agent detection. Add detections for each gap found and a regression that the emulated profile now alerts.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An authorized emulated C2 profile goes undetected at every layer where a tuned stack would catch it: CONFIRMED coverage gap; control FAIL. |
| Benign refutation | NDR/EDR/DNS/proxy detects the profile (or the profile was unrealistic): REFUTED; control PASS. |
| Insufficient evidence | Partial/delayed detection, or an unvalidated emulation profile: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/forensics/offensive-c2-frameworks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's C2 material as a detection-coverage purple-team exercise using an authorized emulation profile and PASS/WARN/FAIL scoring, replacing C2 deployment/evasion instructions with defender-facing detection measurement. Composes with `purple-team-exercise`, `traffic-as-evidence`, `detection-engineering`, `rt-edr-evasion`.
