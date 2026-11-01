---
name: dependency-provenance
description: Know what you actually run, where it came from, and what changed — manifest vs lockfile vs installed vs shipped, identity before trust, pinning by digest, and vulnerability reports treated as candidates until reachability is shown. Use whenever a dependency enters, moves, or is questioned: "add this package", "npm/pip/cargo install", "upgrade this library", "bump the version", "dependabot opened 40 PRs", "we have a critical CVE", "is this package safe", "vendor this", "update the base image", "generate an SBOM", or a lockfile appears in a diff. Also trigger when a build or CI pipeline gains a new plugin or action, when an internal package name might resolve to a public registry, and when someone asks "do we ship version X of Y" during an incident. Covers install-time execution authority, name-confusion attacks, upgrade diffs nobody reads, and reachability-based triage. It does not audit dependency source code line by line.
---

# Dependency Provenance

Most of what runs in production was written by people you will never meet, pulled
by a resolver you did not watch, at a moment you did not choose. That is a
reasonable trade — and it is only reasonable if you can answer three questions at
any time:

1. **What do we actually run?** Not what the manifest requests. What is in the
   artifact.
2. **Where did it come from?** Which registry, which publisher, which commit, and
   what proves the link.
3. **What changed, and did anyone look?**

A dependency policy that cannot answer these is a preference, not a control.

Composes with: `deterministic-core` (a build that isn't reproducible can't be
attested), `attack-surface-triage` (the build system is an entry point with
production credentials), `claim-provenance-discipline` (a scanner's severity is
its claim, not your finding), `versioned-schema-evolution` (upgrades change
serialized shapes), `irreversible-action-gate` (publishing is R3).

---

## Part 1 — Four different answers to "what version do we use"

These diverge constantly, and people quote whichever one is at hand:

| Layer | What it says | How it lies |
|---|---|---|
| **Manifest** (`package.json`, `pyproject.toml`) | What you *requested* — usually a range | Says `^2.1.0`; you run 2.9.4 |
| **Lockfile** | What the resolver *chose*, at resolution time | Stale, or absent for transitive tooling; may not cover the build platform |
| **Installed tree** | What is on disk in this environment | Differs between dev, CI, and prod; may include hoisted or vendored copies |
| **Shipped artifact** | What is in the container/binary/bundle that actually runs | The only one that matters, and the one nobody inspects |

Ground your answers in the shipped artifact. When someone asks "are we affected
by CVE-X in library Y", the defensible answer comes from an inventory of the
image or bundle — not from `grep` in a manifest. Treat the manifest as a request,
the lockfile as a record of a past decision, and the artifact as fact.

**Transitive is the majority.** You chose maybe 30 packages; you run 900. The
ones you chose got the most scrutiny and carry the least risk. Any policy that
reviews direct dependencies only is inspecting a rounding error.

---

## Part 2 — Adding a dependency grants execution authority

The question is not "is this library good code". It is **"what does adding this
authorize, and where does that code run"**:

- **Install-time scripts** (`postinstall`, `setup.py`, build hooks) execute
  arbitrary code, as your user, on developer laptops and in CI — and CI is where
  the deploy keys are. Install-time execution is the highest-privilege moment in
  a dependency's life and the least observed.
- **Build plugins, bundler plugins, CI actions, test fixtures**: same authority,
  same credentials, and usually exempt from whatever review the runtime deps get.
  A test-only dependency that runs in CI is not "low risk"; it is a
  production-credential-adjacent dependency with less scrutiny.
- **Runtime**: what the library can reach — network, filesystem, secrets in the
  process environment. Most language runtimes give a dependency exactly the same
  authority as your own code. There is no inner boundary unless you built one.

Practical stance: disable install scripts by default where the ecosystem allows
it and allowlist the few that genuinely need them; pin CI actions and build
plugins by commit digest, not by tag; and treat "dev dependency" as a description
of *when* it runs, never of *how much it can do*.

---

## Part 3 — Identity before trust

Before evaluating whether a package is trustworthy, establish that it is the
package you think it is. The attacks here are boring, cheap, and effective:

- **Typosquat / homoglyph** — one character off, or a Unicode lookalike.
- **Scope and namespace confusion** — `@org/thing` vs `org-thing`; a name that is
  official in one ecosystem and unclaimed in another.
- **Dependency confusion** — an internal package name that also exists on the
  public registry, where the resolver prefers the higher version. The fix is
  configuration (scoped registries, explicit index priority, reserved
  namespaces), not vigilance.
- **Repo-link laundering** — a package's metadata can claim *any* repository URL.
  A GitHub link in a registry page is a claim by the publisher, not a
  verification. Only a signed provenance attestation, or a build you performed
  yourself from that source, links artifact to source.
- **Maintainer transfer / account takeover** — the package that was trustworthy
  for eight years and changed hands last month. This is why "it's popular" is a
  weak signal: popularity is what makes a takeover worth doing.

Signals worth checking at intake, in rough order of value: does a published
provenance attestation exist and verify; how many maintainers and how recently
did that set change; does the version being installed exist in the source repo as
a tag; how large is its own transitive closure; does it run install scripts; is
the release cadence consistent with the changelog.

---

## Part 4 — Pin, lock, and prefer digests

A version range is a standing promise that every future release from that
publisher will be safe. Nobody can make that promise.

- **Commit the lockfile.** For every ecosystem, including the ones for tools
  ("we only use it in CI" — see above).
- **Install in locked mode in CI** (`npm ci`, `--frozen-lockfile`,
  `pip-sync`/hashes, `--locked`), so a build fails rather than silently resolving
  something new. A CI job that can quietly acquire a different dependency than the
  lockfile specifies has no lockfile.
- **Pin by digest** where the ecosystem supports it — container base images by
  `sha256`, CI actions by commit SHA, package hashes in the lockfile. Tags move;
  digests do not. `FROM node:20` is a moving target, and the day it moves is
  chosen by someone else.
- **Separate the two upgrade decisions**: *when* to take a new version (a
  scheduled, deliberate act) from *what* the range would have allowed (nothing,
  until you decide). Automation should open a proposal, never resolve at deploy
  time.
- **Vendoring is a fork.** It removes upstream surprise and takes on upstream's
  security work. Record the source commit and the reason, or your vendored copy
  becomes a fossil nobody dares to touch (`software-archaeology`).

---

## Part 5 — The upgrade diff nobody reads

A patch bump can contain anything; semantic versioning describes intent, not
content. Scale the review to what the dependency can reach:

- **Read the actual diff, not the changelog**, for anything with install-time
  execution, credential access, network egress, or crypto responsibility. The
  changelog is written by the same party whose compromise you are worried about.
- **Look for the shape of a compromise**, not for clever code: a new install
  script, a new network call, added obfuscation or minified blobs in a source
  package, a sudden dependency on something that touches env vars, a release with
  no corresponding source-repo commit.
- **Batch the boring, isolate the interesting.** Forty automated bumps merged as
  one is a review of nothing. Merge low-reach updates in a batch; give
  high-reach ones their own PR and their own diff read.
- **Know why you are upgrading.** "Fixes a CVE we are exposed to" and "a bot
  opened a PR" deserve different urgency and different testing. Upgrading for its
  own sake, at speed, is itself a supply-chain risk: it shortens the window
  between a malicious publish and your adoption of it. A brief cooldown before
  adopting brand-new versions costs almost nothing and removes the most common
  attack window.

---

## Part 6 — Vulnerability reports are candidates, not findings

A scanner result says: a package in your tree matches a version range in an
advisory. That is a match, not an exposure. Applying `claim-provenance-discipline`
to the whole class:

- **Ingest at level CANDIDATE**, with origin (`scanner`, version, advisory ID).
  Do not inherit CVSS into your own report as if you derived it — the base score
  describes a generic deployment, not yours.
- **Ask for reachability**: is the vulnerable function called, on a path reachable
  by untrusted input, in a configuration that enables the flaw? A vulnerable
  parser you never invoke and a vulnerable parser on your public endpoint are
  the same row in a scanner and completely different problems.
- **Say which it is.** `REACHABLE — exploitable path exists` /
  `PRESENT, NOT REACHED — no call path found (evidence: …)` /
  `UNKNOWN — reachability not analyzed`. `UNKNOWN` is honest and common; it is
  not the same as safe, and it is not the same as critical.
- **Not-reached is not "won't fix" forever.** It is a claim with a falsifier: a
  future change that introduces the call path. Record the falsifier so the
  decision reopens by itself.
- **The unfixable case**: no patched version exists. The options are remove,
  replace, vendor-and-patch, or compensate (block the input at the boundary).
  Choose one and record it (`decision-record-discipline`) — an open ticket is not
  a mitigation.

---

## Part 7 — Inventory you can query during an incident

The test of all of this is a single question, asked at 2am about a package name
you have never heard of: **do we ship it, in what versions, in which services?**

If answering takes a day of grepping repos, you do not have an inventory. Produce
one per artifact, at build time, from the artifact itself — an SBOM is fine, but
its value is being *queryable and current*, not being a document that satisfies a
form. Include the transitive closure, versions, digests, and the build that
produced it, and keep it addressable by the artifact's own digest.

Two things worth alerting on: a dependency appearing that no manifest requested
(a resolver surprise or a hijack), and a package whose maintainer set changed
between the version you run and the version you are about to take.

---

## Deliverable checklist

```markdown
## Dependency provenance review

Inventory source: manifest | lockfile | installed tree | SHIPPED ARTIFACT ← use this
Direct: <n>   Transitive: <n>   Ecosystems: <...>
Intake checks (new dep): identity (typosquat/scope/confusion) · maintainers & recent changes ·
  install scripts · transitive closure size · provenance attestation verified?
Execution authority: install-time / build & CI (credentialed) / runtime — stated per dep
Pinning: lockfile committed · CI installs locked · base images & CI actions by digest
Upgrade: reason (CVE / scheduled / bot) · diff read? · cooldown applied? · batch vs isolated
Advisories: <id> → REACHABLE | PRESENT-NOT-REACHED (evidence) | UNKNOWN → action + falsifier
Unfixable: remove | replace | vendor-and-patch | compensate — decision recorded where
Incident readiness: "do we ship X@Y?" answerable in <time> from <source>
```

---

## How to respond when this skill is active

- Answer "which version do we run" from the shipped artifact, and say which layer you looked at.
- Before evaluating a new dependency's quality, check its identity — name confusion is cheaper for an attacker than writing malicious code.
- Name the execution authority being granted, especially install-time and CI, and treat "dev dependency" as a statement about timing, not privilege.
- Push for digests over tags and locked installs in CI; flag any pipeline that can resolve something the lockfile does not name.
- Read the diff, not the changelog, for anything with reach; batch the rest rather than pretending forty bumps were reviewed.
- Downgrade scanner output to CANDIDATE and ask for reachability before anyone writes "critical" in a report.
- When no patch exists, force a choice among remove / replace / vendor-and-patch / compensate, and record it. An open ticket is not a mitigation.
