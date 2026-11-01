---
name: rt-osint
description: Build an evidence-bound organizational asset inventory from authorized public-source snapshots, distinguishing ownership, hosting and historical observations.
---

# Organizational Exposure Research

Read [METHODOLOGY.md](../METHODOLOGY.md) before selecting collection sources.
Use this skill for organization-owned infrastructure and public artifact exposure.
Use rt-osint-methodology for cross-source claim adjudication and timeline reconstruction.
Personal profiling, face identification and credential-use experiments are outside this workflow.

## Mechanisms and preconditions

- DNS relates a name to records at an observation time; it does not prove server ownership.
- Certificate transparency records issuance claims, not current service or domain control.
- ASN and shared-hosting associations identify providers, often shared by unrelated customers.
- Public code metadata can reveal package/service names without establishing their deployment.
- Search indexes and passive scanners may be stale, incomplete or copied from one another.
- A public document can expose internal identifiers; importance depends on actual sensitivity.

## Observation and baseline

Start from an authorized seed list of domains, organization IDs, repositories and time window.
Define a specific question, such as whether an inventory misses an organization-controlled service.
Record source query, collection time, source observation time, license/access constraint and artifact.
Keep raw spelling and a normalized comparison value; use correct DNS suffix boundaries.
Preserve original records and digests so a later reader can distinguish evidence from enrichment.

## Abduction and deduction

Hypothesis: a certificate SAN and passive DNS match identify an unmanaged organization asset.
Benign rival: the address belongs to a shared CDN, an expired deployment or an unrelated tenant.
Prediction: an independent owner-supplied inventory or deployment record links the exact hostname
and service identifier at the relevant time; unrelated same-IP hosts lack that relationship.
Shared IP, favicon similarity and a common certificate issuer do not satisfy the discriminator.

## Bounded collection procedure

1. Use supplied exports first and define a maximum query count and artifact-size budget.
2. Parse DNS, certificate and repository observations without visiting discovered endpoints.
3. Normalize hostnames with explicit wildcard and internationalized-name handling.
4. Join observations on exact identifiers and overlapping time intervals, retaining source IDs.
5. Compare candidate assets with an owner-provided inventory or authoritative ownership record.
6. Include known shared-hosting neighbors as negative controls for overbroad attribution.
7. Inspect supplied public document/source metadata for exposure using a synthetic marker
   or exact nonsecret identifier; never validate discovered credentials against services.
8. Where public querying is authorized, use official/read-only interfaces and record coverage
   limits. A third-party page crawler or public upload is an additional disclosure/action.
9. Stop at the question's resolution or budget; unexplained relationships stay candidates.
10. Retain the evidence graph and query ledger; do not expand scope automatically through pivots.

## Domain failure modes

Substring domain matching can merge unrelated suffixes; distinguish a hostname from its URL path.
Wildcard DNS can make guessed names appear valid without corresponding distinct applications.
Expired certificates and historical DNS can describe different owners at different times.
An API returning no results may mean pagination, quota or provider coverage, not absence.
Two commercial results can derive from the same certificate feed and are not independent.
An AI-generated entity label is a hypothesis requiring source confirmation.
Local analysis is not automatically private if extensions or telemetry transmit artifacts.

## Evidence, detection and remediation

Deliver nodes for exact assets and edges labeled resolves-to, issued-for, deployed-by or
observed-at; do not replace them all with "owned by."
For each candidate include time bounds, source diversity, contrary evidence and next check.
Report exposure of a synthetic/internal marker separately from credential validity or compromise.
Recommend inventory reconciliation, removal of unintended public artifacts and ownership review.
For monitoring, compare new certificate/DNS/repository observations against approved changes;
validate alerts using a known test asset and a benign shared-provider neighbor.

## Versions and tool limits

Record parser, normalizer, API schema, dataset snapshot and pagination/coverage limitations.
Inspect current installed tool capabilities before relying on passive-only collection modes.
Do not import upstream service availability, pricing or model context-size claims.
No external queries, person searches, public uploads or endpoint probes ran during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Exact hostname links to owner deployment record and is absent from approved inventory | CONFIRMED inventory gap, bounded to that record; FAIL |
| Shared IP candidate belongs to another tenant and lacks an owner deployment link | REFUTED ownership inference; no vulnerability verdict |
| Only an old certificate SAN is available with no current ownership evidence | CANDIDATE asset relation; WARN |

## Provenance

Rewritten from `Skills/recon/offensive-osint/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain infrastructure, code-artifact and archival collection value; replace
tool-directory breadth, people profiling and leak-service pivots with bounded asset evidence.
