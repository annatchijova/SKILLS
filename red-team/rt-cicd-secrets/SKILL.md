---
name: rt-cicd-secrets
description: "Red-team assessment of CI/CD secret-exposure boundaries: pipeline environment-variable and log-masking exposure, Vault/secrets-manager token reuse, cloud-runner metadata and managed-identity reach, and OIDC-federation trust. Re-expressed as scoped experiments on an owned pipeline using a planted canary secret and detection measurement, naming exfiltration as an impact class to bound rather than shipping exfil recipes."
---

# CI/CD Secret-Exposure Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's CI/CD secrets craft as scoped experiments on an owned pipeline with a planted canary secret: it names the exposure vectors and measures whether masking/isolation hold, treating exfiltration channels and masking bypass as impact classes to bound, not as free actions.

## Scope and prerequisites

A pipeline step runs with injected secrets, cloud-runner identity and often broad token scope. Use an owned pipeline with a planted non-production canary secret (a unique string wired to detection). Demonstrate exposure by observing the canary where it should not appear; do not exfiltrate real secrets off real infrastructure.

Declare the platform (GitHub/GitLab/Jenkins/cloud), attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Env/secret exposure** — secrets in the step environment; masking bypass (encoding, reversal, char-by-char) revealing the canary in logs/artifacts.
- **Vault/secrets-manager** — a present `VAULT_TOKEN`/AppRole or cloud secret handle reachable from the step.
- **Cloud-runner identity** — AWS IMDS creds, Azure managed identity, GCP metadata SA on the runner.
- **OIDC federation** — a workflow in a trusted org assuming a cloud role via OIDC.
- **Exfiltration channels** (impact class) — HTTP/DNS/ICMP/artifact egress from the runner.

## Mechanism and observation

Trace the canary from the secret store to the step and observe where it can leak.

**Firstness:** Record the canary appearing in a log, artifact, or an owned collector from the runner. **Secondness:** State the intended control (masking, least-scope token, runner isolation, egress limits) and the deviation. **Thirdness:** Infer the exposure class only after the canary leaks under control.

## Abduction and refutation

**Mechanism hypothesis:** The pipeline exposes secrets or identity more broadly than needed — masking is bypassable, the token is over-scoped, runner metadata is reachable, or OIDC trust is loose.

**Competing benign explanation:** Masking catches the canary in all encodings; the token is minimally scoped; IMDSv2/hop-limit blocks metadata from the step; OIDC `sub` claims are tightly conditioned; egress is restricted so no channel works.

## Deduction and controls

A normal step keeps the canary masked and contained (positive control). A confirmed finding surfaces the canary (decoded) in a log/artifact/collector where a hardened pipeline would not. Predeclare the leak location. Masking-all-encodings / least-scope token / blocked metadata / tight OIDC are PASS controls.

## Induction: bounded laboratory procedure

Owned pipeline; planted canary; detection on.

1. **Baseline.** Run a normal step; confirm the canary is masked and contained.
2. **Masking probe.** Attempt to surface the canary via encoding/reversal/char-by-char (bounded) and see whether masking catches it — a masking-effectiveness measurement.
3. **Token/identity reach.** Check whether `VAULT_TOKEN`/cloud identity is present and what it can read (scope the reads to the owned lab).
4. **Metadata.** Test whether the runner can reach cloud metadata (IMDSv2 token requirement often blocks GET-only reach).
5. **OIDC.** Inspect the federation trust conditions.
6. **Egress (bounded).** Confirm whether an owned collector is reachable from the runner — the exfil-channel class — without moving real data.
7. **Control.** Confirm a hardened configuration contains the canary.

Record results including refutations. Keep finding and control status separate.

## Domain-specific failure modes

Masking that catches every encoding is a PASS, not a bypass. A present token that can read nothing useful is low impact. IMDSv2 with hop-limit 1 blocks many metadata reaches. OIDC with tight `sub`/`aud` conditions defeats federation abuse. An owned canary must be used — never surface real secrets to "prove" the leak.

## Evidence and deliverable

Provide the vector, the canary leak location, the token/identity scope observed, and the control result. Use only the planted canary. Attach minimal replay, expected/observed, rival explanation, falsifier, untested vectors.

## Versions and tool limitations

Pin the CI platform, runner image and cloud metadata version/mitigations. No pipeline behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

Use least-scope tokens and short-lived OIDC with tight claim conditions, secret masking plus never echoing secrets, ephemeral isolated runners, and restricted egress. Treat IMDSv2 and hop limit as controls against specific metadata request paths, not proof that a CI step cannot reach metadata; verify runner/container network topology, role policy and reachable endpoints. Scan logs/artifacts for secret shapes. Add a regression asserting the canary stays contained through the tested paths. Detect secret-shaped strings and runner egress to unexpected hosts.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The planted canary surfaces (decoded) in a log/artifact/collector where a hardened pipeline contains it: CONFIRMED; FAIL (scope to the exposure shown). |
| Benign refutation | The tested encodings are masked, the token is minimally scoped, or the declared network/identity control blocks the tested metadata path: REFUTED for that path. Do not claim all encodings or all runner paths from a finite test. |
| Insufficient evidence | A reachable channel but no canary exposure: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/cicd/offensive-cicd-secrets/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's env/masking, Vault, cloud-runner-identity and OIDC exposure knowledge, re-expressed as owned-pipeline experiments with a planted canary and detection measurement, naming exfiltration/masking-bypass as impact classes to bound rather than shipping exfil recipes. Composes with `pipeline-boundary-assessment`, `cloud-identity-assessment`, `secret-lifecycle-discipline`.
