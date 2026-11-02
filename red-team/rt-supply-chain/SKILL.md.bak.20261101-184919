---
name: rt-supply-chain
description: Validate artifact identity, build provenance and release admission with inert substituted artifacts and controlled signing identities.
---

# Artifact Trust and Promotion Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before inspecting release evidence.
Follow the artifact from approved source to deployed bytes. Use rt-dependency-confusion
for resolver origin and pipeline-boundary-assessment for execution-context questions.

## Mechanisms and preconditions

- A mutable tag/path can name different bytes at build and deployment time.
- A signature proves a relationship to a key; policy must authorize that signer and purpose.
- Provenance must bind the artifact digest to the expected builder, source and build context.
- A checksum fetched from the same writable location as the artifact is not independent trust.
- Install hooks and build plugins can execute before the final application exists.
- A compromised signing-capable builder may produce validly signed undesirable artifacts.
- SBOM presence establishes neither completeness nor runtime reachability of every component.

## Observation and baseline

Record requested dependency, locked dependency, installed tree and shipped artifact separately.
For each promotion hop, identify writer identity, object digest, verifier and policy revision.
Define the approved source revision and signing identity; use no production signing key.
Trace image index and platform manifest digests where multi-platform images are involved.
State whether reproducibility is required and what legitimate build variation is permitted.

## Abduction and deduction

Hypothesis: deployment admission accepts bytes not bound to the approved build identity.
Benign rival: the displayed tag changed, but deployment remains pinned to an approved digest.
Prediction: changing only the staged artifact digest makes the consumer accept an unauthorized
fixture if binding is absent; an otherwise identical verifier enforcing the binding rejects it.
Do not equate a missing checksum sidecar or unsigned commit with a compromised release.

## Bounded laboratory procedure

1. Copy the promotion/verifier policy to an isolated fixture registry and deployment sink.
2. Prepare inert artifacts A and B with distinguishable data markers and record their digests.
3. Sign or attest A using a lab-approved identity; establish that the consumer accepts A.
4. Substitute B only at the test-owned staging hop, leaving the expected digest/policy fixed.
5. Verify rejection and capture the exact policy reason; do not launch executable contents.
6. Separately test an intact artifact signed by a lab identity outside the allowed set.
7. Separately test provenance with the wrong source revision or builder identity.
8. Compare a pinned digest consumer with a mutable-tag consumer to isolate name resolution.
9. For build hooks, inspect source and run only inert fixture hooks in a no-secret sandbox;
   measure the build phase and authority without constructing a malicious package.
10. Stop at acceptance/rejection or the fixture budget; restore registry pointers and sink state.

## Domain failure modes

Verifier success may mean cryptographic validity only; inspect the policy evaluation result.
Re-signing B as the approved builder tests builder trust, not artifact transport tampering.
An attestation for A does not cover B merely because filenames or version labels match.
Reproducible builds can reproduce malicious approved source; identity is not source quality.
Timestamped signatures and key revocation have verifier-specific validity semantics.
An SBOM generated from a manifest may omit bundled or vendored shipped components.
Installer inspection can itself run hooks; treat tooling execution separately from archive reading.

## Evidence, detection and remediation

Retain digest lineage, signing identity, attestation subjects, trust roots, policy decisions
and the allowed control. Keep test key material outside portable reports.
Detect changed digest at promotion, unexpected signer/builder and policy bypass events.
Use immutable artifact identity, explicit signer/source policy and isolated signing authority.
Separate build, approval and promotion grants; verify at the consuming boundary.
After remediation, rerun altered artifact, wrong signer and legitimate release cases.

## Versions and limits

Record registry, build engine, package backend, signing client and verifier versions.
Inspect supported attestation predicate and policy semantics before selecting tooling.
Historical package hooks and verifier flags are research leads, not portable commands.
No package publication, signing service access or release operation ran during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| B reaches test sink despite expected A digest; binding-enabled twin rejects B | CONFIRMED promotion integrity failure; FAIL |
| Tag moves but sink still consumes approved A digest and rejects B | REFUTED tag-to-deployment claim; PASS |
| Artifact is signed but signer policy and consumer verification are unavailable | NOT TESTED trust enforcement; WARN |

## Provenance

Rewritten from `Skills/supply-chain/offensive-supply-chain/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain build-hook, signing and artifact handoff mechanisms; replace trojaning,
maintainer compromise and public publication with inert promotion-policy tests.
