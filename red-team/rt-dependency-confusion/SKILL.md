---
name: rt-dependency-confusion
description: "Red-team assessment of dependency-confusion / namespace boundaries across npm, PyPI, NuGet, Maven, Gradle, Go and RubyGems: internal-package-name reconnaissance (lock files, source maps, errors, repo mining) and registry-priority misconfiguration. Re-expressed as scoped experiments that prove resolution-order risk with a DNS-canary-only package and registry-config controls instead of publishing functional malicious packages."
---

# Dependency Confusion Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's dependency-confusion craft as scoped experiments: it names the recon sources and per-ecosystem misconfigurations, proving resolution-order risk with a canary-only package (DNS callback, no payload) rather than publishing a working malicious package.

## Scope and prerequisites

Dependency confusion exploits a resolver preferring a public package over a same-named private one. The engagement must authorize claiming names on public registries; use a canary package that only makes an owned DNS/HTTP callback and carries no functional payload, and remove it at the end. Prefer verifying the resolver's order in an owned build first.

Declare the ecosystems in scope, attempt budget, stop condition. Config/lock-file-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Recon** — internal names from lock files (`package-lock.json`, `yarn.lock`, `requirements.txt`, `Pipfile.lock`, `*.csproj`), JS source maps/webpack chunks, error messages/stack traces, GitHub mining (`.npmrc`, `--extra-index-url`, `NuGet.config`), job postings.
- **Resolution misconfiguration** (per ecosystem): npm unscoped or no scope→registry mapping; pip `--extra-index-url` (additive) vs `--index-url`; NuGet multiple feeds without `<clear/>`/packageSourceMapping; Maven/Gradle central-before-private; Go GOPROXY/GOPRIVATE; Ruby default sources.

## Mechanism and observation

Trace how the build resolves an internal name when a public name of equal/higher version exists.

**Firstness:** Record which registry the build resolved the name from (owned-build trace) or a canary callback on install. **Secondness:** State the intended resolution (private registry only / scope-pinned) and the deviation. **Thirdness:** Infer the confusion class only after a controlled build resolves the public canary.

## Abduction and refutation

**Mechanism hypothesis:** The resolver considers the public registry for an internal name, so a higher-version public package wins.

**Competing benign explanation:** A scope→registry mapping / exclusive index / `<clear/>` + source mapping / private-first repo pins resolution to the private source; the name is already claimed publicly by the org (defensive registration); the build uses a lockfile with pinned integrity hashes.

## Deduction and controls

A correctly-configured build resolves the internal name only from the private registry (positive control). A confirmed finding has the build resolve the public canary (callback or trace) where the pinned config would not. Predeclare the canary callback. Scope mapping / exclusive index / source mapping / private-first are PASS controls.

## Induction: bounded procedure

Owned build first; canary-only public package if authorized.

1. **Recon.** Extract candidate internal names from the sources above; identify which are unclaimed publicly.
2. **Config review.** Inspect the resolver config for the misconfiguration class per ecosystem.
3. **Owned-build trace.** In an owned build, add a same-named public canary at a higher version and observe which source resolves — the safest confirmation.
4. **Canary registration (if authorized).** Publish a DNS-canary-only package; a callback on the target's install confirms resolution. No payload.
5. **Control.** Apply the pinned config (scope mapping / exclusive index / source mapping) and confirm the private source wins.
6. **Cleanup.** Remove the canary package.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

The `confused` scanner checks lock files for confusable names across npm/pip/NuGet. The per-ecosystem secure patterns are in the table of the upstream and above — the fix is always "pin resolution to the private source," not "register every name" (though defensive registration helps). Integrity-hash lockfiles blunt confusion for already-locked deps but not new/unlocked ones.

## Domain-specific failure modes

A scope→registry mapping or exclusive index makes the public name unreachable — a PASS. A name already defensively registered by the org is not confusable. An owned-build trace that resolves private is a refutation. The canary must be payload-free and removed; publishing a functional package is out of scope.

## Evidence and deliverable

Provide the internal name, the recon source, the resolver misconfiguration, the owned-build trace or canary callback, and the pinned-config control result. Attach minimal replay, expected/observed, rival explanation, falsifier, ecosystems not covered. Note canary cleanup.

## Versions and tool limitations

Pin the package manager and registry-client versions — resolution semantics change (e.g. npm scope handling, NuGet source mapping). No resolver behavior was verified by this content; confirm the live config and prefer an owned-build trace first.

## Remediation and detection

Pin resolution to the private registry (scope→registry mapping, exclusive `--index-url`, NuGet `<clear/>` + packageSourceMapping, private-first Maven/Gradle, `GOPRIVATE`), use integrity-hash lockfiles, and defensively register internal names publicly. Add a regression asserting the internal name resolves only from the private source. Detect installs resolving internal names from public registries.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A build resolves the public canary for an internal name (trace or callback) where the pinned config would not: CONFIRMED; FAIL. |
| Benign refutation | Scope mapping / exclusive index / source mapping pins to the private source: REFUTED; PASS for the control. |
| Insufficient evidence | An unclaimed internal name without a confirmed resolution trace: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/supply-chain/offensive-dependency-confusion/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's recon-source and per-ecosystem resolution-misconfiguration craft, re-expressed as owned-build/canary experiments with pinned-config controls, replacing functional malicious packages with payload-free resolution proof. Composes with `rt-supply-chain`, `dependency-provenance`.
