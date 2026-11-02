---
name: pipeline-boundary-assessment
description: "Red-team assessment of CI/CD pipeline execution boundaries: GitHub Actions expression injection and workflow_run artifact poisoning, mutable-tag vs pinned-SHA action references, Jenkins script-console/Groovy-sandbox/remoting-deserialization and shared-library injection, and GitLab CI YAML/MR injection. Re-expressed as scoped experiments on an owned pipeline with an inert marker and token-permission inspection instead of live controller RCE."
---

# CI/CD Pipeline Execution-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's pipeline-exploitation craft as scoped experiments on an owned pipeline: it names the injection and supply-chain vectors, proving code reaches the runner with an inert marker and inspecting token scope, rather than taking over a real controller.

## Scope and prerequisites

Pipelines execute untrusted inputs (PR titles, branch names, artifacts) with privileged tokens. Use an owned repo/pipeline; prove execution with an inert marker (an owned-collector callback or a benign echo), never a controller shell or org-wide push.

Declare the platform, attempt budget, stop condition. Config/workflow-file-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **GitHub Actions** — expression injection (untrusted `${{ }}` into `run`), `workflow_run` artifact poisoning (default-branch handler processes fork artifacts unsafely), mutable-tag action references (force-pushable vs pinned SHA), over-scoped `GITHUB_TOKEN`, self-hosted runner exposure, composite-action supply chain.
- **Jenkins** — script-console RCE (RunScripts), Groovy sandbox escape, remoting deserialization (port 50000), shared-library injection.
- **GitLab CI** — YAML/`.gitlab-ci.yml` injection via MRs, over-privileged job tokens.

## Mechanism and observation

Trace an untrusted input to the step that executes it and the token it runs with.

**Firstness:** Record the inert marker executing in the runner (callback/echo) and the token's permissions. **Secondness:** State the intended boundary (untrusted input is data; least-privilege token; immutable references) and the deviation. **Thirdness:** Infer the class only after the marker runs under control.

## Abduction and refutation

**Mechanism hypothesis:** An untrusted input flows into a shell/eval context, or a mutable/poisonable reference lets attacker-controlled code run in a privileged pipeline step.

**Competing benign explanation:** The input is passed via an environment variable (not interpolated into the shell); artifacts are validated/sandboxed; actions are pinned to SHAs; the token is read-only; the Groovy sandbox holds; the remoting port is firewalled.

## Deduction and controls

A normal pipeline run executes no injected code and uses a minimal token (positive control). A confirmed finding runs the inert marker in the runner via the vector where a hardened pipeline would not. Predeclare the marker effect. Env-var passing / pinned SHAs / least-scope token / sandbox / firewall are PASS controls.

## Induction: bounded laboratory procedure

Owned pipeline; inert marker.

1. **Baseline.** Run the normal pipeline; capture how inputs flow and the token scope.
2. **Expression injection.** On an owned repo, submit an input (PR title/branch) crafted to reach a `run` step; the marker calls an owned collector once.
3. **Artifact poisoning.** From a fork, upload an artifact the default-branch `workflow_run` handler processes; observe whether the marker runs.
4. **References/token.** Check for mutable-tag action refs; dump `GITHUB_TOKEN`/job-token permissions and whether it can push.
5. **Jenkins/GitLab.** Test script-console/sandbox/remoting reachability and MR YAML injection on owned instances with the marker.
6. **Control.** Confirm a hardened pipeline refuses each.

Record results including refutations. Keep finding and control status separate. Stop at the marker; do not push to real branches or dump real credentials.

## Craft notes (leads)

The classic GitHub vectors are untrusted `${{ github.event.* }}` interpolated into `run`, and `pull_request_target`/`workflow_run` running with write token + untrusted code. Pinning actions to a full commit SHA (not a tag) closes the mutable-reference class. Jenkins remoting deserialization uses ysoserial over JNLP (see `rt-deserialization`). Self-hosted runners on the default branch are high-value.

## Domain-specific failure modes

Input passed through an env var is inert even if it looks injected — a refutation. A read-only token bounds impact. Pinned SHAs defeat mutable-reference poisoning. A held Groovy sandbox or firewalled remoting port is a PASS. Prove the marker, not a real takeover.

## Evidence and deliverable

Provide the vector, the input, the marker execution in the runner, the token scope, and the control result. Use owned repos and inert markers. Attach minimal replay, expected/observed, rival explanation, falsifier, untested vectors.

## Versions and tool limitations

Pin the platform and (for self-hosted) controller versions — behaviors and defaults change. No pipeline behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

Treat all event inputs as untrusted (pass via env, never interpolate into shell), pin actions to SHAs, least-scope tokens, isolate/ephemeral runners, restrict `pull_request_target`/`workflow_run`, harden Jenkins (disable script console, firewall remoting, patch), and review MR CI changes. Add a regression asserting injected input is inert. Detect token over-use, unexpected pushes, and script-console/remoting activity.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An inert marker runs in the runner via the vector on an owned pipeline where a hardened pipeline refuses: CONFIRMED; FAIL (scope to the step reached). |
| Benign refutation | Env-var passing / pinned SHA / read-only token / sandbox defeats it: REFUTED; PASS for the control. |
| Insufficient evidence | A reachable sink without confirmed marker execution: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/cicd/offensive-cicd-pipeline/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's expression-injection, artifact-poisoning, reference-pinning and Jenkins/GitLab craft, re-expressed as owned-pipeline experiments with an inert marker and token inspection, replacing live controller RCE with bounded execution proof. Composes with `rt-cicd-secrets`, `rt-deserialization`, `rt-supply-chain`.
