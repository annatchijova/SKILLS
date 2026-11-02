---
name: rt-cicd-secrets
description: Validate CI secret delivery, retention, federation and revocation with synthetic credentials in isolated runners.
---

# CI Secret Lifecycle Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before selecting an experiment.
Use this skill for credential distribution and residue; use pipeline-boundary-assessment
for the separate question of who controls executed code.

## Mechanisms and prerequisites

- Secret injection grants access to processes in a job; log masking does not revoke it.
- Vault authorization depends on authenticated role, path, namespace and lease;
  listing a secret name is different from reading its value.
- Federation binds issuer, audience and workload claims to a receiving identity.
  A decoded token establishes claimed content, not signature validity or acceptance.
- Persistent workspaces, caches and image layers can outlive the credentialed step.
- Registry helpers and service connections have their own identity and storage lifecycle.
- Runner registration authority and job authorization are separate grants.

## Observation and baseline

Record the job event, source ref, runner identity, environment gate and secret binding.
Inventory names, intended consumers, lifetime and storage classes without collecting values.
Define which fixture jobs may receive the synthetic secret and when it must disappear.
Record the policy revision and whether protected variables are available in this context.
Do not assume every CI platform exposes every stored secret through an API.

## Abduction and deduction

Hypothesis: a secret granted to the release job remains reachable by an untrusted later job.
Benign rival: the apparent value is a sample string, masked rendering or a new authorized lease.
Prediction: only reuse of the same runner storage exposes the unique fixture marker;
an equivalent job on a fresh runner and an unbound job do not observe it.
Use a private checker returning presence and artifact ID, never printing real credentials.

## Bounded laboratory procedure

1. Create an isolated pipeline fixture with no production integrations or external egress.
2. Bind a unique nonfunctional marker to one authorized job and verify that delivery works.
3. Let the ordinary build complete; inspect only the fixture log, artifact and cache paths.
4. Run the unbound consumer on reused storage, then repeat on fresh storage.
5. Vary one storage class at a time to distinguish environment inheritance from disk residue.
6. For Vault-like delivery, compare one allowed fixture path with one denied fixture path.
7. For federation, use an owned issuer/test verifier and change audience or subject alone.
8. For revocation, use an inert test service: check before expiry, after expiry and after
   revocation, distinguishing newly issued sessions from the original credential.
9. Stop at marker exposure or the agreed job/time budget; do not retrieve unrelated values.
10. Remove test-owned bindings and storage after retaining the authorized evidence.

## Domain failure modes

File-type variables may survive step cleanup; artifact upload can preserve their bytes.
Protected-branch and environment policies may differ between push and merge-request jobs.
Secret masking can hide a fixture from the UI while a downloaded log retains it.
Revoking a refresh credential may not immediately invalidate an already issued access token.
Cache restoration may be denied by writer scope even when cache keys match.
Separate these outcomes rather than reporting a single "secrets insecure" finding.

## Evidence and response

Keep binding metadata, runner reuse evidence, fixture marker ID, storage origin,
authorization outcomes and lease timestamps. Record CANDIDATE/CONFIRMED/REFUTED/NOT TESTED.
Detect secret access by unexpected workload identity and retention beyond job completion.
Prefer per-job short-lived identities, exact federation claims and isolated runner storage.
Verify revocation semantics with the issuer; log redaction is defense in depth.
Retest authorized delivery as well as denied delivery so the fix does not break releases.

## Versions and limits

Record CI server, runner, credential plugin, secret provider and helper versions.
Check installed help and provider documentation before executing platform commands.
Legacy JWT variable names and runner registration flows are not portable assumptions.
No tooling or credential validation against real services was executed to author this skill.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Unbound job reads the unique marker from reused cache; fresh runner cannot | CONFIRMED residue exposure; control FAIL |
| Suspected value is fixture documentation; actual secret remains restricted in both controls | REFUTED exposure claim for tested path; PASS |
| Only a masked screenshot is available, with no binding or raw fixture artifact | CANDIDATE; WARN, no credential-compromise claim |

## Provenance

Rewritten from `Skills/cicd/offensive-cicd-secrets/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: preserve delivery, federation and residue mechanisms; replace extraction,
mask evasion and credential pivots with synthetic lifecycle tests.
