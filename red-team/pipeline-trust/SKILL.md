---
name: pipeline-trust
description: Treat the CI/CD pipeline as a privileged execution environment that runs attacker-influenceable code with production credentials — not as configuration — because a build step is arbitrary code execution holding the keys to deploy, and the pipeline sits inside your trust boundary while rarely being modeled as an attack surface. Use whenever the subject is a build/deploy system: "is our CI secure", "GitHub Actions / GitLab CI / Jenkins pipeline", "a PR can run our workflow", "secrets in the runner", "poisoned pipeline execution", "someone can modify the build", "self-hosted runner", "dependency confusion in the build", "supply-chain risk in CI", "can a fork exfiltrate our secrets". Sibling of dependency-provenance (the build pulls untrusted code) and secret-lifecycle-discipline (the runner holds the deploy keys); it models the build as execution, not config. It does not write the pipeline YAML for you, and never treats "it's just CI" as lower-stakes than production — the pipeline deploys to production.
---

# Pipeline Trust

A build step is not configuration. It is arbitrary code, executing on a machine that
holds credentials to sign artifacts and deploy to production, frequently triggered by
input that an outsider can influence — a pull request, a dependency version, a commit
message, a tag. The CI/CD pipeline is therefore one of the most privileged and least
modeled execution environments an organization runs: it is inside the trust boundary,
it has production's keys, and it runs whatever the build tells it to. Reasoning about
it as "some YAML" is the category error this skill exists to correct.

The reframe, stated sharply: **whoever can influence what the build executes can act
with the build's privileges.** And the build's privileges are, by design, enormous —
push images, sign releases, assume deploy roles, read every secret the pipeline was
given.

The failure modes:

- **Poisoned Pipeline Execution (PPE).** A pull request modifies the workflow, the test
  script, or a build tool the workflow invokes — and the CI runs that attacker-authored
  code with the repo's secrets. A `pull_request_target` trigger, or a fork PR that runs
  privileged workflows, is remote code execution against your credentials wearing the
  costume of "running the tests."
- **Build-time dependency execution.** `npm install` / `pip install` / a Gradle plugin
  runs install hooks *during the build*; a dependency-confusion or typosquat hit
  executes in the runner, not in production, and the runner is where the secrets live.
- **Runner and secret sprawl.** A self-hosted runner reused across jobs, secrets scoped
  to the whole org instead of the one job, a token with `write` where `read` would do —
  each turns a small foothold into a deploy-anything position.

Composes with the library:

- **dependency-provenance** — the build pulls and *executes* untrusted third-party code; install-time execution is the vein
- **secret-lifecycle-discipline** — the runner holds deploy keys; their scope and lifetime is the blast radius
- **cloud-control-plane-reasoning** — a CI OIDC token is a control-plane identity, often with production rights
- **container-trust-boundary** — the runner is usually a container; its escape and identity surface apply
- **agent-trust-boundaries** — untrusted input (a PR) reaching a privileged executor is the same trifecta, in build clothing
- **assume-breach-modeling** — assume the runner is compromised and follow the deploy keys outward

---

## Step 1 — Model the build as code execution, and find who can influence it

For each pipeline, ask the only question that matters first: *what inputs decide what
code runs, and who controls those inputs?*

- **Trigger** — who can start a privileged run? A fork PR, an external contributor, a
  comment, a tag push? `pull_request_target` and its equivalents run *with secrets* on
  *PR-authored code* — the classic PPE door.
- **What the run executes** — not just the workflow file, but everything it invokes: the
  test suite, the build script, a Makefile, a linter config, a `postinstall` hook. Any
  of these being writable by the triggerer is code execution.
- **Trust of the pieces** — pinned actions/plugins by commit SHA, or floating tags an
  upstream can repoint? A third-party action is code you run with your secrets.

The finding is the shortest path from "an outsider can influence input X" to "the
runner executes their code."

---

## Step 2 — Enumerate what the runner holds (the blast radius)

The severity of that code execution is set by what the runner can reach:

- **Secrets and tokens** — which are exposed to *this* job? Org-wide secrets on a job
  that only needs one are the over-scoping that turns a small PPE into a full compromise
  (`secret-lifecycle-discipline`).
- **Cloud identity** — the OIDC token / assumed deploy role is a control-plane credential
  (`cloud-control-plane-reasoning`); enumerate what it can do, not what this job uses.
- **Artifact-signing / publish rights** — can the runner sign a release or push an
  image? Then a compromised build ships backdoored software to everyone downstream — the
  supply-chain amplifier.

---

## Step 3 — Least privilege per job, and isolate the untrusted trigger

The structural defenses are about *not handing the keys to the code that outsiders
influence*:

- Split trusted and untrusted work: run fork-PR code in a job with **no secrets**, and
  gate anything privileged behind a maintainer approval or a separate trigger.
- Scope secrets and tokens to the narrowest job and the shortest lifetime; prefer
  short-lived OIDC over long-lived stored keys.
- Pin third-party actions/plugins by immutable digest; treat a version bump as a
  dependency change that gets reviewed, not a silent upstream update.
- Isolate runners: ephemeral, single-use runners over reused self-hosted ones that
  accumulate state and cross-job secret residue.

---

## Step 4 — Provenance of what the pipeline ships

The pipeline's output is trusted by everyone downstream *because* it came from the
pipeline — so the pipeline's integrity is the root of that trust:

- Can you prove *which* source and *which* build produced a given artifact (build
  provenance / attestation)? Without it, a compromised runner's malicious build is
  indistinguishable from a clean one.
- Is the artifact signed, and is the signing key reachable only by the step that should
  hold it? A signing key exposed to the whole pipeline is a signing key exposed to a
  PPE.

---

## Step 5 — Assume the runner is breached, and state the honest reach

Put it together with `assume-breach-modeling`: assume attacker code ran in the runner.
What does it exfiltrate (every secret in scope), what can it deploy (anything the token
allows), what can it ship (any artifact it can sign), and how would you even know
(runner logs are often ephemeral and under the attacker's control during the run)?
State the reach plainly. "It's just CI" is the sentence to delete: the pipeline is the
thing that writes to production, so a compromise of the pipeline is a compromise of
production with better deniability.

---

## The one-line test

If you would not run a stranger's code on your production deploy host with the deploy
keys loaded, then a fork PR that can influence your privileged workflow is exactly
that — you just called it "running the tests." Find who can influence what the build
executes, scope the secrets so that influence buys nothing, and treat the pipeline's
output as trusted only as far as the pipeline's integrity is proven.
