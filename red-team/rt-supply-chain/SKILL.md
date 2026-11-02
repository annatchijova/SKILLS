---
name: rt-supply-chain
description: "Red-team assessment of software-supply-chain boundaries: dependency confusion, typosquatting, and build-system install-hook injection (npm scripts, Python setup.py/pyproject hooks, Makefile targets) across npm, PyPI and NuGet. Re-expressed as scoped experiments using DNS-canary-only PoC packages and build-config controls, with a staged risk ladder and mandatory cleanup instead of live malicious distribution."
---

# Software Supply-Chain Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's supply-chain craft as scoped experiments with canary-only PoC packages and a staged risk ladder: it names the vectors and proves reach with a DNS callback, never distributing a functional payload, and mandates cleanup.

## Scope and prerequisites

Supply-chain attacks place attacker-controlled code into a target's build/install. The engagement must authorize public-registry actions; every PoC is a payload-free DNS-canary package, removed at the end. Prefer owned-build verification before any public registration.

Declare the ecosystems and whether public registration is authorized, attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Dependency confusion** (see `rt-dependency-confusion`) — npm/PyPI/NuGet name claiming.
- **Typosquatting** — near-miss names of popular packages.
- **Build-system install hooks** — npm lifecycle scripts (`preinstall`/`postinstall`), Python `setup.py`/`pyproject` build hooks, Makefile default-target injection — code that runs at install/build time.

## Mechanism and observation

Trace how a dependency's install/build step executes code on the consumer.

**Firstness:** Record the canary callback firing during the target's install/build (or an owned-build trace resolving the PoC). **Secondness:** State the intended behavior (dependencies install data/code without arbitrary execution; resolution pinned to private sources) and the deviation. **Thirdness:** Infer the class only after a controlled install/build triggers the canary.

## Abduction and refutation

**Mechanism hypothesis:** The build resolves or executes attacker-controllable package code (confusion, typosquat, or an install hook) during install/build.

**Competing benign explanation:** Resolution is pinned to private sources (confusion closed); lockfile integrity hashes reject substitution; install scripts are disabled (`--ignore-scripts`); the typosquat name is not actually referenced; the org defensively owns the name.

## Deduction and controls

A correctly-configured install resolves and builds only trusted code with no arbitrary execution (positive control). A confirmed finding fires the canary during install/build via the vector where the pinned/hardened config would not. Predeclare the callback. Pinned resolution / integrity hashes / disabled scripts / defensive ownership are PASS controls.

## Induction: bounded procedure with a staged risk ladder

Owned build first; canary-only PoC if public registration is authorized. Follow the ladder and stop at confirmation:

1. **Recon (low risk).** Extract internal/dependency names from lock files; find typosquat candidates; identify unclaimed names.
2. **Config review (low).** Check resolution pinning, lockfile integrity, and whether install scripts run.
3. **Owned-build trace (low).** Resolve/install a local canary with an install hook in an owned build; confirm the hook runs and where resolution points.
4. **Staged PoC registration (medium, if authorized).** Register a DNS-canary package (confusion or typosquat) with an install-time callback only; a callback confirms reach.
5. **Validate & document (low).** Confirm the callback, scope the impact.
6. **Cleanup (mandatory).** Remove PoC packages from public registries.
7. **Control.** Apply pinning/integrity/`--ignore-scripts` and confirm the vector closes.

Record results including refutations. Keep finding and control status separate. PoC packages are payload-free DNS canaries only.

## Craft notes (leads)

`confused` scans lock files for confusable names. Install hooks are the execution primitive: npm lifecycle scripts, Python `setup.py` `cmdclass`/entry hooks, Makefile targets that run before the default build. Typosquats rely on human/CI typos. The highest-impact variant is a transitive dependency's install hook, because it runs silently across many consumers.

## Domain-specific failure modes

Pinned resolution closes confusion. `--ignore-scripts`/no-install-scripts defeats hook execution. Integrity-hash lockfiles reject substitution of locked deps. A typosquat no one references is not reachable. Owned-build trace resolving trusted is a refutation. A functional payload is never appropriate — canary only, and clean up.

## Evidence and deliverable

Provide the vector, the recon source, the canary callback or owned-build trace, the control result, and confirmation of cleanup. Attach minimal replay, expected/observed, rival explanation, falsifier, ecosystems not covered.

## Versions and tool limitations

Pin package-manager versions — lifecycle-script and resolution behavior changes. Public registration has real side effects; keep PoCs payload-free and remove them. No build behavior was verified by this content; prefer an owned-build trace first.

## Remediation and detection

Pin resolution to private sources, enforce lockfile integrity, disable install scripts by default (`--ignore-scripts`, vet exceptions), defensively register internal names, use allowlists/SBOM and signed provenance (SLSA), and review new/transitive dependencies. Add a regression asserting the vector closes. Detect install-time network callbacks and new transitive deps with install hooks.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A canary fires during install/build via confusion/typosquat/hook where the pinned/hardened config would not: CONFIRMED; FAIL. |
| Benign refutation | Pinned resolution / integrity / `--ignore-scripts` / defensive ownership closes the vector: REFUTED; PASS for the control. |
| Insufficient evidence | An unclaimed/typosquat name without a confirmed install/build callback: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/supply-chain/offensive-supply-chain/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's confusion/typosquat/install-hook craft and staged risk ladder, re-expressed as owned-build/canary experiments with pinning and script controls and mandatory cleanup, replacing live malicious distribution with payload-free reach proof. Composes with `rt-dependency-confusion`, `dependency-provenance`, `pipeline-boundary-assessment`.
