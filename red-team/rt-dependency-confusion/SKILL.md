---
name: rt-dependency-confusion
description: Test package source selection and namespace isolation using two private fixture registries and inert packages across supported ecosystems.
---

# Dependency Source Selection Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before designing resolution tests.
This skill covers which source supplies a package. Artifact signing and promotion
belong in rt-supply-chain; no public package publication is part of this procedure.

## Mechanisms and preconditions

Confusion requires an intended private identity, an alternate eligible source and a
resolver decision that selects the alternate bytes. Name availability is not that proof.
Separate client selection from registry proxy fallback; either can change package origin.
Read effective configuration from project, user, environment and CI layers.
Record package name normalization, version constraints, platform markers and lock mode.

| Ecosystem | Specific decision to inspect |
|---|---|
| npm | Scope-to-registry mapping, resolved lock URLs and private proxy upstream policy |
| pip | Candidate union across indexes, normalized names, hashes and wheel compatibility |
| NuGet | Package source mapping, restore mode, cache and transitive source eligibility |
| Maven/Gradle | Mirrors, content filters, plugin repositories and metadata resolution |
| Go | Module path ownership, GOPROXY separators, GOPRIVATE and checksum policy |
| Ruby | Bundler source blocks, lock source and transitive resolution |
| OCI images | Fully qualified registry, tag resolution and digest pinning |

Do not assume a universal "highest public version wins" algorithm or automatic npm fallback.
Go proxy 404/410 responses do not establish that a module namespace is claimable.

## Abduction and deduction

Hypothesis: an internal package resolves from an unintended configured source.
Benign rival: the observed URL is an approved mirror or a stale cache entry for identical bytes.
Prediction: a cold restore with source-distinct inert packages selects the wrong digest;
exclusive source mapping prevents that selection while still resolving the legitimate package.
Record the expected origin before running; do not infer execution from download alone.

## Bounded laboratory procedure

1. Copy only the relevant manifest and sanitized resolver settings into a temporary workspace.
2. Create two private/local fixture repositories representing intended and alternate sources.
3. Use invented package names and inert prebuilt packages with distinct content markers.
   Do not include install hooks, callbacks, real internal namespaces or production credentials.
4. Fix resolver version and platform. Record all configuration layers and proxy settings.
5. Run a bounded clean-cache resolution with both sources available and capture origin/digest.
6. Repeat with the intended source exclusively mapped; retain the successful allowed control.
7. Repeat with the intended package absent to measure fail-closed versus fallback behavior.
8. Compare locked and unlocked modes separately; do not silently regenerate the lockfile.
9. If metadata generation can execute a build backend, use inert wheels/packages instead
   or a disposable no-egress sandbox. A "download" command is not necessarily nonexecuting.
10. Stop after the origin decision is established; remove test repositories and workspace
    after retaining the sanitized configuration, logs and package digests.

## Failure modes and interpretation

Warm caches can mask source mapping changes; lockfiles can suppress the candidate under test.
An unsupported platform package can lose resolution for reasons unrelated to source trust.
Same-name packages in two feeds may be legitimate mirrors; compare digests and policy intent.
Dependency resolution, build execution and runtime import are separate evidence stages.
Disabled scripts reduce one effect but do not prove the correct package was selected.
Inspect plugin/build dependency sources even when runtime dependencies are locked.

## Evidence and remediation

Produce package coordinate, intended source, chosen source, digest, resolver decision log,
cache state, control result and missing preconditions for every candidate.
Detect unexpected source changes in lockfiles and build inventories, including transitive tools.
Remediate through namespace/source binding, controlled mirrors and hash-verified locked restores.
For OCI consumers, pin the fully qualified image digest and verify its provenance separately.
Retest source outage behavior: an unavailable private package should not silently widen trust.

## Versions and tool limits

Record package-manager, registry/proxy and lockfile format versions before execution.
Inspect installed help and ecosystem documentation for the exact restore mode and flags.
Scanners that report an unclaimed name produce candidates, not resolution or execution proof.
No resolver experiment or registry interaction was executed during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Cold restore chooses alternate marker; exclusive mapping chooses intended marker | CONFIRMED source-selection failure; FAIL |
| Alternate URL is an approved mirror with expected digest and no unauthorized source | REFUTED confusion claim for tested package; PASS |
| Public-name absence is reported without effective config or resolver output | CANDIDATE; WARN, no execution claim |

## Provenance

Rewritten from `Skills/supply-chain/offensive-dependency-confusion/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain ecosystem-specific resolution questions; replace public namespace
registration and callback packages with isolated source-selection experiments.
