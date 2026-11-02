---
name: rt-ssrf
description: "Red-team assessment of server-side request forgery boundaries: URL-input, webhook, importer, PDF/screenshot and proxy vectors. Covers allowlist/denylist bypass (IP representation, DNS rebinding, redirects), cloud-metadata reachability (AWS IMDSv1/v2, GCP, Azure, ECS), and Kubernetes/service-mesh/container-socket exposure, re-expressed as scoped reachability experiments against owned collectors and fixtures with negative controls instead of live internal pivoting."
---

# Server-Side Request Forgery Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's SSRF craft as scoped reachability experiments: it names the vectors, bypass families and high-value internal endpoints to probe, using owned collectors and lab targets rather than live internal exploitation.

## Scope and prerequisites

Find every place where the server fetches a URL derived from input: URL fields, website previews, link unfurlers, webhooks, importers, media/document converters, PDF/screenshot exporters, API gateways and proxies. Use an owned callback collector (DNS and HTTP) in scope, and a lab instance whose internal topology you are authorized to reach.

Declare target, permitted internal ranges, attempt budget and stop condition. If only source is authorized, produce a vector hypothesis and mark runtime verification NOT TESTED. A metadata-credential pivot is an impact class to demonstrate on an owned lab, not to run against production infrastructure.

## Attack surface and classes

- **Full SSRF** — the server returns the fetched response to you (read internal services).
- **Blind SSRF** — no response body; confirmed only by an owned callback.
- **Semi-blind** — timing/status/length differences leak reachability.
- **Second-order** — a stored URL is fetched later by a backend job.

## Mechanism and observation

Trace the input URL through validation (scheme, host allow/deny, DNS resolution) to the actual fetch.

**Firstness:** Record what the server resolved and requested (owned-callback logs, response, timing). **Secondness:** State the intended egress policy (which hosts/schemes are allowed) and how the observation deviates. **Thirdness:** Infer the defect class only after a controlled callback or internal response confirms the request left as directed.

## Abduction and refutation

**Mechanism hypothesis:** The fetcher validates a representation of the destination (string, pre-resolution host) but acts on another (post-resolution IP, post-redirect URL), letting a request reach an unintended internal target.

**Competing benign explanation:** An egress firewall blocks the internal request regardless of app behavior; the callback was the app's legitimate preview fetch; the "metadata" response is a mocked fixture; DNS did not actually rebind in the time window.

## Deduction and controls

An allowed external URL fetches normally (positive control); a disallowed internal URL must be refused if the control holds. A confirmed SSRF shows the owned collector received the request, or an internal fixture response returned, where the control URL did not reach. Predeclare the callback or response that confirms it. Egress blocking it is a PASS control, recorded separately.

## Induction: bounded laboratory procedure

Owned collector and authorized lab targets only.

1. **Baseline.** Submit an allowed external URL pointing at your collector; confirm the fetch and capture request metadata (headers, source, follows-redirects?).
2. **Internal reachability.** Point at authorized lab internal addresses: `127.0.0.1`, `0.0.0.0`, `localhost`, link-local, internal service names; observe response/timing/callback.
3. **Bypass discriminators** (filter-vs-resolver differential): alternate IP encodings (decimal, octal, hex, IPv6, `[::ffff:a.b.c.d]`), DNS rebinding (owned rebinder), open-redirect chaining, `@`-userinfo tricks, scheme abuse (`file:`, `gopher:`, `dict:`), trailing-dot and case.
4. **Metadata reachability (owned lab)** — demonstrate the class, do not harvest production creds: AWS IMDS `169.254.169.254` (note IMDSv2 requires a PUT token — a GET-only SSRF often cannot reach it), GCP `metadata.google.internal` with `Metadata-Flavor: Google`, Azure IMDS with `Metadata: true`, ECS task-metadata URI.
5. **Protocol/port sweep** against the lab only, bounded.
6. **Control.** Re-run the allowed URL to confirm the positive control still passes.

Record each result including refutations. Keep finding status and control status separate.

## High-value internal targets (impact classes to bound)

On a vulnerable fetcher in an authorized lab, these are the reachable-impact classes that make SSRF serious; demonstrate reachability and report the bound, do not exfiltrate real secrets:

- **Cloud metadata** → instance IAM credentials (the classic escalation; IMDSv2 and hop-limit mitigations change reachability — test, do not assume).
- **Kubernetes** → kubelet API (often weakly authenticated), service-account token at the mounted path, then API-server `secrets`.
- **Service mesh** → Envoy/Linkerd admin on localhost, Pilot discovery.
- **Container sockets** → Docker/containerd/CRI-O sockets (via `unix:`/gopher where supported) → container control.
- **Internal dashboards** → Prometheus, Grafana, ArgoCD, Rancher, Consul.

## Framework and domain failure modes

A callback alone proves reachability, not data return — separate blind from full. Egress controls can make an app-layer SSRF unexploitable; report residual impact. DNS rebinding depends on TTL and resolver caching; a single failed window is not a refutation. Node (`request`/`axios` redirect handling), Python (`requests`/`urllib`), and Java (`URL`/`HttpClient`) differ in redirect and scheme behavior — pin the client.

## Evidence and deliverable

Provide the vector, the submitted URL, the resolved destination, owned-callback records or internal fixture response, the bypass used, and any egress control that bounded impact. Keep real credentials and internal data out of portable output. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered vectors.

## Versions and tool limitations

Pin the HTTP client and its redirect/scheme config; pin cloud metadata-service version and mitigations (IMDSv2, hop limit). No endpoint behavior was verified by this content. Confirm installed versions and current cloud metadata behavior before claiming.

## Remediation and detection

Validate post-resolution (resolve, then check the IP against a denylist of internal/link-local ranges, and re-check after redirects), allowlist schemes and hosts, disable unused URL schemes, enforce IMDSv2 with hop limit 1, and isolate egress. Add a regression asserting an internal URL is refused. Detect via egress logs showing requests to metadata/link-local ranges correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An owned collector or authorized internal fixture receives the server's request where the control URL does not: CONFIRMED; FAIL (scope the impact to what was reached). |
| Benign refutation | The internal URL is refused / egress blocks it: REFUTED for the tested vector; PASS for the control. |
| Insufficient evidence | Only a timing difference, no callback or response: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-ssrf/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's vector taxonomy, IP/DNS/redirect bypass families and cloud/Kubernetes/service-mesh target map, re-expressed as owned-collector reachability experiments with egress controls, replacing live metadata-credential harvesting and internal pivoting with bounded reachability proof.
