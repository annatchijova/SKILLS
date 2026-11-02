---
name: rt-request-smuggling
description: "Red-team assessment of HTTP request-smuggling / desync boundaries: CL.TE, TE.CL and TE.TE between front-end and back-end, plus HTTP/2 downgrade desync, client-side desync, pause-based, CONNECT tunneling, WebSocket desync and header oversizing. A parser-differential problem between proxy and origin, re-expressed as owned two-tier lab experiments with timing/response discriminators and negative controls instead of live queue poisoning."
---

# HTTP Request Smuggling Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's desync craft as scoped experiments against an owned front-end/back-end lab: it names the desync variants and their discriminators while keeping confirmation to timing/self-observed effects rather than poisoning other users' responses.

## Scope and prerequisites

Smuggling is a parser differential (compose with `parser-differential-hunting`): the front-end and back-end disagree on where one request ends. Reproduce the real two-tier topology (proxy/CDN/load-balancer in front of an origin) in an owned lab. Confirm with timing and self-targeted effects; do not poison a shared queue or capture other users' requests on a live system.

Declare target topology, attempt budget and a stop on first confirmation. Source-only / single-tier setups yield a hypothesis marked NOT TESTED.

## Attack surface and classes

- **CL.TE** — front-end uses `Content-Length`, back-end uses `Transfer-Encoding`.
- **TE.CL** — the reverse.
- **TE.TE** — both support TE but one is tricked by an obfuscated header into ignoring it.
- **HTTP/2 desync** — H2 downgraded to H1 at the back-end with mismatched length semantics; H2.CL / H2.TE.
- **Client-side desync (CSD)**, **pause-based**, **CONNECT tunneling**, **WebSocket desync**, **header oversizing** — modern variants.

## Mechanism and observation

Trace how each tier computes message length (CL vs TE vs H2 frame).

**Firstness:** Record the timing/response anomaly (a delayed response indicating a back-end wait for bytes that never come, or a smuggled prefix affecting your own next request). **Secondness:** State the correct behavior (both tiers agree on message boundaries) and the deviation. **Thirdness:** Infer a desync only after a controlled, self-observed effect reproduces.

## Abduction and refutation

**Mechanism hypothesis:** Front-end and back-end parse length differently, so a crafted request leaves a prefix in the back-end's buffer that prepends to the next request on that connection.

**Competing benign explanation:** Both tiers normalize headers identically (no differential); the delay is network jitter; the connection is not reused between requests (no shared buffer); the front-end rejects ambiguous CL+TE outright.

## Deduction and controls

A well-formed request pair behaves normally (positive control). A true desync produces the time-based signature (the back-end stalls waiting for the declared body) and then a self-observed prefix effect on your own follow-up request. Predeclare the exact timing threshold and the self-targeted marker. A front-end that rejects ambiguous length framing is a PASS control.

## Induction: bounded laboratory procedure

Owned two-tier lab; self-targeted confirmation; single-packet where applicable.

1. **Baseline.** Send normal requests; confirm connection reuse and capture normal timing.
2. **Time-based probe.** Send a CL.TE / TE.CL probe whose framing makes the back-end wait for more bytes; a reproducible delay (vs the baseline, repeated) indicates a differential. This is the safe first discriminator.
3. **Confirm self-effect.** Smuggle a prefix that affects only your own next request (e.g. changes your own response), proving the buffer carried over — without targeting another user.
4. **TE.TE obfuscation.** Test header obfuscations (spacing, casing, duplicate TE, line folding) to see which tier is fooled.
5. **HTTP/2 downgrade.** If the front-end speaks H2 to an H1 back-end, test H2.CL/H2.TE and CRLF-in-H2-header injection.
6. **Control.** Confirm the well-formed pair stays in sync.

Record results including refutations. Keep finding and control status separate. Stop at the self-observed confirmation; do not escalate to live victim capture.

## Craft notes (leads)

Classic obfuscations: `Transfer-Encoding: chunked` with trailing space/tab, duplicate TE headers, `Transfer-Encoding:\nchunked`, `Content-Length` + `Transfer-Encoding` together. H2 desync exploits the length ambiguity introduced at downgrade; check `Alt-Svc`/H2/H3 support. Pause-based desync sends headers slowly then a smuggled request. Impact classes to bound: security-control bypass, cache/response-queue poisoning, request capture — demonstrate the mechanism, not the live population.

## Domain-specific failure modes

A single slow response is jitter until repeated. No connection reuse means no shared buffer, so no classic smuggling. A front-end that fully normalizes removes the differential even if the back-end is lenient. Timing signatures prove a differential but not yet a usable prefix — show the self-effect to confirm.

## Evidence and deliverable

Provide the topology, the framing probe, the reproducible timing delta, the self-observed prefix effect, and which tier was fooled. Keep any captured data to your own requests. Attach minimal replay, expected/observed, rival explanation (jitter/no-reuse), falsifier, uncovered variants.

## Versions and tool limitations

Pin front-end and back-end server/versions — desync is implementation- and version-specific (track real CVEs). Burp's HTTP Request Smuggler and the single-packet attack are the standard tools; keep probes self-targeted. No topology behavior was verified by this content; reproduce the live stack first.

## Remediation and detection

Make both tiers agree: reject ambiguous CL+TE, normalize/strip TE before the back-end, prefer HTTP/2 end-to-end without downgrade, disable connection reuse to untrusted back-ends, and cap header sizes. Add a regression asserting ambiguous framing is rejected. Detect anomalous response/queue behavior and malformed length headers at the front-end.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A reproducible timing signature plus a self-observed smuggled prefix on an owned two-tier lab: CONFIRMED; FAIL. |
| Benign refutation | Both tiers normalize identically / no connection reuse / front-end rejects ambiguity: REFUTED; PASS for the control. |
| Insufficient evidence | A single unrepeated delay, no self-effect: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-request-smuggling/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's CL.TE/TE.CL/TE.TE and modern H2/CSD/pause-based desync craft, re-expressed as owned two-tier lab experiments with timing and self-observed discriminators, replacing live queue/response poisoning with bounded mechanism proof.
