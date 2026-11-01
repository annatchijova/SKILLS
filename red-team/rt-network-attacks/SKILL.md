---
name: rt-network-attacks
description: Validate address assignment, neighbor trust, VLAN and NAC boundaries on isolated network fixtures without credential interception or relay.
---

# Layer 2 and Layer 3 control validation

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use a disconnected virtual switch or spare isolated switch, owned clients, a legitimate address server and inert canary endpoints. Export bindings, VLANs, host modes and intended trust-port roles.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- DHCP snooping trust, binding tables and Dynamic ARP Inspection work together; missing or static bindings affect interpretation.

- IPv6 router advertisements and DHCPv6 are different control planes; RA Guard does not by itself validate DHCPv6 responses.

- 802.1X port authorization, per-host mode and MAC-based exceptions determine access; a port is not universally single-principal or multi-principal.

- VLAN tagging, native VLAN handling and routed ACLs establish different boundaries; one-way receipt is not bidirectional access.

- Name-resolution fallback and application authentication are separate; a canary resolution change does not establish credential relay or TLS compromise.

## Observation and competing explanations

**Firstness / Secondness:** Record ingress port, protocol, switch decision and client route/address/neighbor state. Compare with the explicitly configured trust boundary.

**Abduction:** An untrusted access port can supply an address-service response that changes a client resolver contrary to the configured DHCP trust policy.

**Competing benign explanation:** The observed response entered a deliberately trusted uplink or the client retained a legitimate prior lease.

**Deduction:** The reviewed fixture from the untrusted port changes the fresh client's resolver; the trusted server succeeds and the same fixture is blocked when the specified control is enabled.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Snapshot switch and client state and verify a normal lease, resolver query and harmless canary connection.

2. Clear only test-owned lease state through supported client controls and confirm the actual ingress-port trust configuration.

3. Run one finite vendor conformance case for the selected protocol inside the disconnected lab, then inspect switch counters and client state; do not run poisoning or starvation chains.

4. Repeat with only the relevant control changed. For RA, DHCPv6, ARP, VLAN or NAC cases, build separate matrices with their own receipt and identity oracles.

5. Restore bindings, routes, trust roles and leases; verify ordinary connectivity and denied-zone isolation with both address families.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- A mirrored packet proves observation, not forwarding or acceptance; inspect the client and destination.

- RA Guard success says nothing about DHCPv6, and DHCP snooping without the appropriate rate policy does not prove starvation resistance.

- Double-tagged one-way delivery is not a completed session; NAC behavior depends on actual host mode and exception policy.

## Evidence and output

Provide port/VLAN/topology map, protocol-specific control configuration, client before/after state, switch counters and destination receipts. Never retain real authentication exchanges for this test.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Validate alerts for untrusted address servers, neighbor-binding violations, unexpected router advertisements and unauthorized host admission using separate protocol cases.

Constrain trusted ports, maintain correct bindings, enforce IPv6-specific controls and explicit VLAN/NAC host policy. Validate legitimate renewal and roaming after hardening.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Record switch OS/ASIC, virtual-switch implementation, host networking stack and conformance-harness version. Packet offload or SPAN behavior can hide tags; document capture limitations.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Untrusted-port fixture changes a fresh client's resolver, while trusted-server and enabled-control comparisons isolate the missing enforcement. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The response entered a documented trusted uplink; the same fixture is dropped on the untrusted port and client state remains unchanged. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A SPAN capture shows a DHCP response but no ingress trust mapping or client acceptance evidence exists. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/network/offensive-network-attacks/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Replaces poisoning, relay and network disruption chains with protocol-specific trust-control experiments, preserving VLAN, NAC, ARP and dual-stack distinctions.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
