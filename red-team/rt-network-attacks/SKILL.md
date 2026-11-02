---
name: rt-network-attacks
description: "Red-team assessment of Layer 2/3 network trust boundaries in an authorized lab: ARP spoofing, LLMNR/NBT-NS/mDNS poisoning, rogue DHCP/DNS and DNS rebinding, MITM/SSL-strip/HSTS-bypass, VLAN hopping (switch-spoofing, double-tagging) and 802.1X bypass. Re-expressed as scoped isolated-segment experiments with a defined victim fixture, control traffic and strong detection focus instead of live interception of third-party traffic."
---

# Layer 2/3 Network Trust-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's L2/L3 craft as scoped experiments on an isolated authorized segment: it names the attacks and their detection signatures, confirming interception/redirect against a designated fixture rather than capturing real users' traffic.

## Scope and prerequisites

These attacks abuse implicit trust in L2/L3 protocols (ARP, LLMNR, DHCP, DNS, 802.1Q, 802.1X). Run only on an isolated lab segment with a designated victim fixture you own; never intercept third-party traffic on a shared/production network. Capture only the fixture's traffic.

Declare the segment, the fixture, attempt budget, stop condition. Config/topology-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **ARP spoofing** — poison the fixture/gateway mapping to MITM.
- **Name poisoning** — LLMNR/NBT-NS/mDNS answer broadcast lookups → capture NetNTLMv2 (relay → see `rt-active-directory`).
- **DHCP/DNS** — rogue DHCP (option 3/6 gateway/DNS redirect), DHCP starvation, rogue DNS, DNS cache poisoning, DNS rebinding.
- **MITM** — HTTP proxy, SSL-strip, HSTS bypass (`sslstrip+`/`dns2proxy`).
- **VLAN hopping** — switch spoofing (DTP), double tagging (802.1Q).
- **802.1X bypass**, IPv6 SLAAC/DHCPv6 RA attacks.

## Mechanism and observation

Pick one attack; trace the trust it abuses to the redirect/interception it achieves against the fixture.

**Firstness:** Record the fixture's traffic reaching your controlled node (captured ARP redirect, poisoned response, VLAN frame delivered). **Secondness:** State the protocol's intended behavior and the deviation. **Thirdness:** Infer the trust-boundary class only after the fixture is controlled-redirected.

## Abduction and refutation

**Mechanism hypothesis:** A protocol accepts unauthenticated assertions (ARP replies, name responses, DHCP offers, DTP/802.1Q tags), letting a rogue node redirect or impersonate.

**Competing benign explanation:** Dynamic ARP Inspection / DHCP snooping / RA Guard / port security block it; LLMNR/NBT-NS are disabled; the switch denies DTP and tagged frames on access ports; HSTS preload defeats SSL-strip; the "capture" is the fixture's own loopback.

## Deduction and controls

On an unhardened segment the redirect succeeds (demonstration); on a hardened one it must fail. A confirmed finding delivers the fixture's traffic to your node where the hardened control blocks it. Predeclare the captured artifact. DAI/snooping/RA-Guard/port-security/HSTS defeating the attack are PASS controls.

## Induction: bounded laboratory procedure

Isolated segment; designated fixture; capture only the fixture.

1. **Baseline.** Record normal L2/L3 behavior and the fixture's path.
2. **Run one attack.** e.g. ARP-spoof the fixture↔gateway; or stand up name poisoning; or a rogue DHCP offer with option 6; or DTP/double-tag into a target VLAN.
3. **Confirm redirect/interception** of the fixture's traffic at your node (one artifact), then stop.
4. **Controls.** Enable the corresponding hardening (DAI, snooping, RA Guard, port security, HSTS) and confirm the attack now fails.
5. **Detection.** Record the signatures each attack produced.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Tooling: bettercap/arpspoof/Ettercap (ARP), Responder/Inveigh (name poisoning, hashes in `/opt/Responder/logs`), ntlmrelayx (relay), dnsmasq (rogue DHCP/DNS), Scapy (custom ARP/DNS/gratuitous), Yersinia (L2), singularity (rebinding). DNS cache poisoning must match in-flight txid and source port. Double-tagging: outer=native VLAN, inner=target. These are lab primitives, not a license to run them on shared infrastructure.

## Domain-specific failure modes

A hardened switch (DAI, DHCP snooping, port security, RA Guard) defeats most of these — that is a PASS, report it. HSTS preload defeats SSL-strip. Capturing your own fixture's loopback is not interception. Running any of these on a production/shared segment is out of scope and can disrupt or surveil third parties.

## Evidence and deliverable

Provide the attack, the isolated segment/fixture, the captured redirect artifact, the hardening control result, and the detection signatures. Keep captures limited to the fixture. Attach minimal replay, expected/observed, rival explanation, falsifier, untested attacks.

## Versions and tool limitations

Pin switch/OS and tool versions — mitigations and behaviors vary. Tools transmit real L2/L3 frames; keep to the isolated segment. No network behavior was verified by this content; reproduce the lab first.

## Remediation and detection

Enable DAI, DHCP snooping on trusted ports, port security, RA Guard/DHCPv6 guard, disable DTP (set access ports), disable LLMNR/NBT-NS, enforce HSTS preload and DNSSEC, and 802.1X with sticky MAC. Detect: duplicate gateway MAC, multicast name responses, multiple DHCP offers, DTP/double-tagged frames, MAC flapping (per the upstream detection table). Add a regression that the hardened control blocks the attack.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The fixture's traffic is redirected/intercepted at the test node on the unhardened segment where the hardened control blocks it: CONFIRMED; FAIL. |
| Benign refutation | DAI/snooping/RA-Guard/port-security/HSTS defeats the attack: REFUTED; PASS for the control. |
| Insufficient evidence | A protocol anomaly without confirmed fixture redirect: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/network/offensive-network-attacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's ARP/name-poisoning/DHCP-DNS/MITM/VLAN/802.1X craft and its detection table, re-expressed as isolated-segment experiments against a designated fixture with hardening controls, replacing live third-party interception with bounded redirect proof.
