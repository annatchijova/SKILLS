---
name: rt-wifi-recon
description: Build an evidence-bounded Wi-Fi inventory from authorized captures and controller records, measuring channel coverage and sensor blind spots.
---

# Wi-Fi observation coverage

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use supplied captures or a receive-only sensor on approved channels, plus an owned reference AP and controller inventory. Record dwell schedule, time synchronization and retention limits.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- Beacon RSN capabilities describe advertised options; association records establish negotiated authentication and PMF.

- Channel hopping trades breadth for dwell time and loses short exchanges; absence must be qualified by coverage.

- Hidden SSIDs, multi-BSSID profiles and multiple links can make one physical AP appear as incomplete or multiple assets.

- OUI, RSSI and probe patterns are weak identifiers; randomized addresses and shared chipsets defeat simple attribution.

## Observation and competing explanations

**Firstness / Secondness:** Record which frame and information element support each inventory field. Compare observed APs against the configured reference radio and coverage window.

**Abduction:** An in-scope AP advertises a weaker security policy than its controller inventory declares.

**Competing benign explanation:** The sensor decoded a different BSSID profile, cached an old beacon or never observed the intended band.

**Deduction:** A pinned-channel capture repeatedly shows the mismatch on the owned AP identity while controller timestamps and a known reference profile establish freshness and correct decoding.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Import inventory and mark ownership before collecting; omit unrelated device identifiers from exported results.

2. Verify reception of a known reference beacon on every band included in the claim; record unsupported channels as gaps.

3. Perform a bounded passive observation with fixed duration and packet budget; do not turn adapter validation into an injection test.

4. For a discrepancy, compare fresh pinned-channel frames with controller BSSID/profile mapping and a second supported decoder.

5. Produce an inventory with evidence pointers per field and explicit unobserved intervals; restore any test sensor configuration.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A monitor interface can coexist with software that transmits probes; verify receive-only behavior through configuration and bench observation.

- RSSI cannot establish distance or actor identity without a propagation model.

- A missing handshake does not prove no clients were connected; missed bands and channel dwell are alternate causes.

## Evidence and output

Provide per-BSSID profile, channel, advertised and negotiated fields separately, capture packet numbers, sensor version, drop counts and coverage map.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Compare authorized inventory with observed security-profile drift; evaluate monitoring coverage using the known reference AP rather than claims of passive-sensor invisibility.

Correct inventory drift, unsupported sensors or controller profiles. Preserve unknown values rather than filling them from vendor guesses.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Check installed capture tool help and driver support before naming band flags. Do not reuse upstream adapter compatibility tables or regulatory channel lists as current facts.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh frames tied to the managed BSSID repeatedly advertise the disallowed AKM and the reference profile decodes correctly. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The frames belong to a documented neighboring profile; the scoped BSSID matches its approved configuration. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | The sensor cannot receive the target band and the inventory entry was never observed. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wifi-recon/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Separates observation reliability from active testing; removes tracking, coercive discovery and assumed adapter support.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
