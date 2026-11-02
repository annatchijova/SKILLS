---
name: pipeline-boundary-assessment
description: Review CI workflows for untrusted-input execution and artifact trust violations. Use for pull-request pipelines, workflow chaining, build caches and release identity reviews.
---

# Pipeline Boundary Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this workflow.

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Trace the execution context
For each workflow record trigger, actor, checkout ref, code origin, token permissions, secrets availability, runner persistence and downstream consumers.
Follow untrusted PR titles, branch names and artifacts into shell, expression engines and privileged jobs. Direct interpolation is a candidate; prove what bytes reach the interpreter.

## Controlled tests
Use a detached fixture with fake secrets and a harmless marker. Show that the marker can cross the intended boundary, then repeat with the proposed quoting or data-channel control.
For pull_request_target and workflow_run inspect the executed ref and downloaded artifact provenance; the event name alone does not establish exploitability.
For caches inspect writer permissions, key collisions, restore fallback and executable consumers.
For OIDC inspect issuer, subject, audience and environment constraints against the deploy role.
For dependencies distinguish requested versions, locked versions and shipped bytes; a mutable tag is a provenance weakness, not proof of compromise.

## Refutation
Check event actor restrictions, environment gates, pinned refs, fork permissions and escaping before promoting a finding. A job's declared write permission does not prove an outsider can cause it to run attacker-controlled code.
Do not trigger production releases or publish packages as a review side effect.

## Deliver
Produce source-to-sink traces, fixture outputs, missing preconditions and a regression check. Recommend separation of untrusted build and privileged release, immutable artifact identity, minimal credentials and appropriate runner cleanup. Keep unknown third-party action behavior explicit.

## Discriminating pipeline experiment

Hypothesis: contributor-controlled metadata becomes shell program text in a privileged
job. Benign rival: the workflow passes the value as data, the relevant event is gated,
or the runner executes a trusted ref that cannot consume the proposed input.
Deduction: the exact event fixture produces an unintended inert local marker only
when interpolation crosses the interpreter boundary; the data-channel control does not.

1. Copy the relevant workflow and action code into a local isolated fixture with no
   publishing credentials, deployments or external write integrations.
2. Record event payload, checkout ref, actor checks, token scopes and runner configuration.
3. Use a harmless quoted/whitespace-bearing fixture value to trace bytes reaching the
   interpreter. Instrument the local harness with an inert marker-only side effect.
4. Keep the same event and step under a data-channel control; capture expanded command
   representation and actual effects separately. Shell syntax errors alone are not execution.
5. Check the real event's eligibility and permission model before claiming deployment reachability.
6. For artifact handoffs, compare identical filenames with different controlled digests;
   show which provenance decision the privileged consumer actually makes.
7. Restore the fixture workspace and verify that no release or remote action was dispatched.

Treat GitHub event fields, Jenkins job parameters, GitLab merge-request variables and
Azure service connections according to their installed platform semantics. A YAML
alias or job name is not automatically an injection primitive. Third-party actions
can impose actor checks absent from the calling YAML; inspect that code before a verdict.
Separate source interpretation, command execution and credential reach into distinct claims.

## Detection, versions and acceptance

Correlate workflow run, triggering actor, source/artifact digest and runner identity.
Alert on privileged consumers accepting artifacts from unexpected refs or identities.
Record CI server/runner, shell, action digest and policy versions. Commands and workflow
syntax must be checked against the installed platform. No CI run executed during authorship.

| Evidence | Expected verdict |
|---|---|
| Eligible event reaches unintended fixture marker; data-channel twin prevents it | CONFIRMED interpretation boundary failure in the tested context; FAIL |
| Contributor value stays data and event gate rejects the proposed privileged path | REFUTED proposed path; PASS for tested boundary |
| Workflow declares a write token but triggering actor and executed ref are unknown | CANDIDATE; WARN |

## Provenance

Source path: `Skills/cicd/offensive-cicd-pipeline/SKILL.md`.

Methodology adapted from Claude-Red `offensive-cicd-pipeline` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

