---
name: rt-wifi
description: Assess Wi-Fi estate isolation, management reachability, roaming policy and cross-band consistency using owned clients and bounded lab traffic.
---

# Wi-Fi estate boundary assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use two owned clients, two managed APs and a canary service in each permitted zone. Export the intended role-to-zone matrix, controller configuration and allowed exceptions.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- SSID-to-VLAN mapping and controller tunnel placement determine the actual forwarding boundary; an SSID name is not an isolation control.

- Client isolation may differ for same-AP, cross-AP, wired-to-wireless and multicast paths; enumerate each separately.

- Roaming, cached authorization and dynamic VLAN assignment can retain stale access after a role change.

- Multi-band and multi-link configurations can expose different authentication or forwarding policies despite a shared profile name.

## Observation and competing explanations

**Firstness / Secondness:** Record the exact ingress SSID, negotiated security, AP/link, assigned role, address family and canary response. Contrast this with the policy for that actor and zone.

**Abduction:** A guest association inherits a forwarding role that permits access to a protected management canary.

**Competing benign explanation:** The apparent protected address is a guest-facing proxy, or the client retained an earlier administrator session.

**Deduction:** A fresh guest session reaches the protected listener, whose server log identifies that session; an explicitly denied comparison path stays denied and an allowed guest service remains usable.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Provision isolated guest and management fixtures with distinct response markers and no production credentials.

2. Establish allowed-path reachability and denied-path baselines on the same client; expire prior sessions using supported controls.

3. Exercise one harmless request per role/zone pair, changing only the association role; confirm receipt at the server.

4. Repeat the failing pair across the second AP and after a normal operator-initiated roam; record changed role and VLAN rather than assuming equivalence.

5. Restore profiles and verify the guest service and management isolation after the policy correction.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- DHCP leases and DNS caches can outlive a role change; inspect both before attributing traffic to a VLAN.

- A successful ping establishes only the tested path; it does not establish application authorization.

- A controller capture may omit direct AP forwarding or a second radio link.

## Evidence and output

Deliver the role/zone/IPv4/IPv6 matrix, association and controller event IDs, listener receipts, configuration revision and each untested roaming or multi-link case.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Correlate guest role assignment with management listener access and unexpected VLAN changes; test whether controller and destination logs agree.

Enforce role isolation at the forwarding boundary, isolate management services and reauthorize on relevant session changes. Retest same-AP and cross-AP paths.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record AP firmware, controller release, client OS/driver and capture adapter capabilities. A generation label such as Wi-Fi 7 proves neither capture completeness nor a security policy.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh guest session reaches the management canary while the matched deny control and permitted guest service behave as predicted. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | Only the documented guest proxy responds; direct management access is denied after cached administrator state is cleared. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | Only a shared SSID name and an address inventory are available. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/wireless/offensive-wifi/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Retains the broad Wi-Fi source as an estate forwarding and roaming assessment; delegates protocol-specific authentication claims to distinct skills.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
