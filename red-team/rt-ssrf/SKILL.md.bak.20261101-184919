---
name: rt-ssrf
description: "Validate server-side URL fetch policy, redirects, resolution and egress using owned callback fixtures and isolated network destinations."
---

# Server Fetch Destination Controls

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Determine which component initiates a fetch and which destinations it may reach. A callback establishes a fetch, not metadata access, credential access or arbitrary internal reachability.

Prepare two owned collectors in an isolated network and a documented destination allowlist. Use synthetic response bodies, blocked external egress and bounded redirect/time limits.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace URL parsing, DNS resolution, address classification, redirects, proxy routing and socket connection. Record method and header policy and whether fetched response data is returned to the caller.

**Firstness:** Capture collector request IDs, resolved and connected addresses and final response handling. Compare these with the configured permitted destination set.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** The validator approves one destination but the connector or redirect handler reaches another without revalidation.

**Competing benign explanation:** An outbound fetch may be the feature's intended behavior and restricted correctly. A DNS lookup may come from an inspection service or security scanner rather than the application fetcher.

## Deduction and controls

The approved collector succeeds as a control; a redirect to a disallowed isolated collector is stopped before connection. Any validator/connector mismatch must be associated with the same fixture request.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Fetch a small synthetic document from the allowed collector and correlate application and collector logs.

2. Use a single controlled redirect to the second lab collector, whose policy status is explicitly disallowed.

3. In the isolated resolver harness, compare the validated address set with the actual socket destination; do not target real internal services.

4. Check method, header forwarding and response exposure using only synthetic headers and body markers.

5. Repeat with redirect following disabled as a control, then stop on the first demonstrated policy breach and remove fixture registrations.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

DNS-only evidence does not prove HTTP access. An egress proxy can change resolution semantics. Mixed IPv4/IPv6 answers, cached resolution and redirects need separate observations; arbitrary internal scanning is not a discriminator.

## Evidence and deliverable

Provide URL normalization, DNS answer set, socket address, redirect sequence, method, synthetic header handling and response marker. Bound impact to the destination and data class actually tested.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Record HTTP client, resolver, proxy and URL library versions. Verify supported schemes and redirect defaults locally; do not inherit metadata endpoint or cloud-token assumptions from upstream.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Use explicit destination policy, validate resolved addresses at the connection boundary and revalidate redirects. Restrict schemes, methods and forwarded headers, with network egress controls as an independent layer.

Correlate rejected destinations and unexpected application egress with fetch request IDs. Verify telemetry distinguishes DNS resolution from established connections and returned data.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An allowed fixture URL redirects to a disallowed lab collector and the application connects despite a documented block: CONFIRMED; FAIL. |
| Benign refutation | Only the approved collector is fetched and the disallowed redirect is stopped before connection: REFUTED; PASS. |
| Insufficient evidence | An uncorrelated DNS callback appears but the initiating component and HTTP activity are unknown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-ssrf/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Retains fetch, DNS, redirect and egress mechanisms without metadata credential access, internal enumeration or protocol abuse chains.

