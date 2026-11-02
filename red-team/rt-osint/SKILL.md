---
name: rt-osint
description: "Red-team reconnaissance of an authorized target's externally-observable footprint: domains/subdomains, DNS and certificate transparency, exposed services, public code/credential leaks, cloud assets, and organizational metadata. Re-expressed as scoped, passive-first, privacy-respecting collection that builds an attack-surface map from authorized sources with provenance, not intrusive scanning or personal-data harvesting of individuals."
---

# OSINT Reconnaissance Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the collection below.
This revision restores the upstream's OSINT craft as scoped, passive-first collection: it names the sources that build an organizational attack-surface map with provenance, bounded by authorization and privacy, rather than intrusive scanning or profiling individuals. Compose with `attack-surface-triage` and `intel-source-evaluation`.

## Scope and prerequisites

Reconnaissance maps the authorized target's external footprint before any active testing. Collect from public sources on the organization and its infrastructure within scope. Keep it passive-first (no active scanning unless authorized), and avoid collecting personal data about individuals beyond what the engagement requires. Record the provenance of each datum.

Declare the target org/domains in scope, which sources are authorized, and the passive/active boundary. Active scanning without authorization is out of scope.

## Collection surface

- **DNS & domains** — subdomain enumeration (passive: CT logs, passive DNS; active only if authorized), zone data, related domains.
- **Certificate transparency** — hostnames and infrastructure from issued certs.
- **Exposed services** — internet-wide scan data (Shodan/Censys-class) for the org's ranges — read, not scan, unless authorized.
- **Public code & leaks** — org repos, leaked credentials/keys in public commits, paste sites, exposed buckets.
- **Cloud assets** — enumerable buckets/endpoints tied to the org.
- **Organizational metadata** — tech stack, email format, public staff roles relevant to the engagement (minimized).

## Mechanism and observation

Build the surface map from corroborated sources.

**Firstness:** Record each asset/datum and its source (which CT log, which scan dataset, which repo). **Secondness:** State what is in-scope and expected vs what is unexpectedly exposed. **Thirdness:** Infer an exposure (e.g. a forgotten subdomain, a leaked key) only after corroboration, not from a single stale source.

## Source discipline (compose with intel-source-evaluation)

- Corroborate across independent sources; a single dataset can be stale or wrong.
- Record provenance and timestamp for every datum — recon data ages.
- Distinguish confirmed-live from historical (passive DNS/CT may list decommissioned hosts).
- Minimize personal data; collect only what the authorized engagement needs.

## Abduction and refutation

**Hypothesis:** The org has an externally-observable exposure (forgotten host, leaked secret, misconfigured bucket) worth testing.

**Competing benign explanation:** The host is decommissioned (stale CT/passive-DNS record); the "leaked key" is revoked or a public/test key; the bucket is intentionally public; the asset belongs to a different org sharing infrastructure.

## Deduction and controls

A known in-scope asset is confirmable live (positive control). A real exposure is one corroborated as live and unexpected. Predeclare what "live and in-scope" means. A stale or revoked datum is a refutation, not a finding.

## Induction: bounded collection procedure

Authorized sources; passive-first.

1. **Seed.** Start from the authorized domains/org.
2. **Expand passively.** CT logs, passive DNS, scan datasets, public code/leak search, bucket enumeration — recording provenance.
3. **Corroborate & age-check.** Confirm each asset is live and current (active confirmation only if authorized).
4. **Scope.** Drop out-of-scope or other-org assets; minimize personal data.
5. **Map.** Produce the attack-surface map with provenance, feeding `attack-surface-triage`.

Record results including refutations (stale/other-org assets). Keep confirmed-live separate from historical.

## Domain-specific failure modes

Stale CT/passive-DNS records list dead hosts — age-check. Shared infrastructure attributes another org's assets to the target — verify ownership. A "leaked" key may be revoked/public. Active scanning without authorization crosses from recon into unauthorized testing. Over-collecting personal data is both out of scope and an ethics/privacy problem.

## Evidence and deliverable

Provide the attack-surface map: each asset, its source/provenance, live-vs-historical status, and scope/ownership confirmation. Minimize personal data. Attach the source list, collection date, passive/active boundary honored, and assets excluded as out-of-scope.

## Versions and tool limitations

Datasets (CT, passive DNS, scan data) have coverage and freshness limits — state them. No asset was actively confirmed by this content unless authorized and done; mark confirmation status.

## Remediation and detection

Reduce external footprint: retire forgotten hosts/subdomains, rotate leaked secrets, lock down public buckets, minimize metadata leakage, and monitor CT logs and public code for org assets/secrets. Detect recon-driven scanning against confirmed assets.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A corroborated, live, in-scope exposure (forgotten host / active leaked secret / public bucket) with provenance: CONFIRMED exposure. |
| Benign refutation | The asset is stale/decommissioned, revoked, intentionally public, or another org's: REFUTED. |
| Insufficient evidence | A single stale-source datum not corroborated or age-checked: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/recon/offensive-osint/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's DNS/CT/scan/leak/cloud collection craft, re-expressed as scoped, passive-first, privacy-respecting collection with provenance and corroboration, replacing intrusive scanning and personal profiling with a bounded attack-surface map. Composes with `rt-osint-methodology`, `attack-surface-triage`, `intel-source-evaluation`.
