---
name: api-boundary-assessment
description: Assess authorization and input boundaries in owned APIs using controlled cross-principal replays. Use for REST, GraphQL, gRPC or WebSocket security reviews.
---

# Api Boundary Assessment

Use within the user's authorized scope. Carry existing authorization forward; a skill does not expand it. Record observation, expected behavior, hypothesis, falsifier and actual result. Distinguish CANDIDATE, CONFIRMED, REFUTED and NOT TESTED.

## Experiment
Map actor, tenant, resource, action and transport. Provision two synthetic tenants and a lower-privilege role. Capture a legitimate request and establish the expected denial policy before replaying it with only the principal changed.
Trace routing, middleware, resolver, repository and serialization: a missing handler check may be enforced upstream or by row-level policy.

## Discriminating probes
- Compare owner, unrelated tenant and restricted role responses by actual data and persisted effects, not status alone.
- Test nested object ownership, list/export paths and writable fields separately. A readable field need not be writable.
- GraphQL: verify resolver-level authorization and bounded alias/batch behavior with a small documented request budget.
- gRPC: test method policy and metadata propagation. Reflection exposure alone is not an authorization break.
- WebSocket: distinguish handshake authentication from per-message authorization; test a synthetic session after revocation.
- For URL-consuming fields use a controlled callback fixture. Record whether redirect handling and final destination validation agree; never infer metadata access from a generic callback.

## Refutation and outcome
A 200 with redacted or caller-owned data refutes the claimed cross-tenant disclosure. A 403 with foreign fields can still disclose data. For writes, inspect state after denial.
Deliver the actor/resource/action matrix, paired requests, sanitized responses, exact version, tested cells and omitted cells. Confirm only demonstrated unauthorized data or state transitions. Recommend a negative regression test and the enforcement layer that covers the class.

## Required methodology and scoped setup

Read [the assessment methodology](../METHODOLOGY.md) before execution.
Record the deployed route/schema revision, two synthetic tenant identities, allowed mutations and request budget.
Use disposable records and disable external notifications; stop at a demonstrated boundary failure.
Firstness records response fields and durable effects; Secondness records the policy matrix.
Thirdness names the missing enforcement boundary only after the discriminator succeeds.

## Mechanism-specific experiment

**Abduction:** an alternate method or content type reaches a handler without the role or field policy enforced on the ordinary route.
**Benign rival:** shared middleware, typed binding or database policy already rejects the forbidden action; the alternate route may only return a harmless generic response.
**Deduction:** a restricted role must fail the same logical action through each supported transport, while the authorized fixture succeeds.
**Induction:** compare one ordinary request and one supported alternate representation, preserving identity, object and intended action.
Capture the selected handler, effective method and bound fields; inspect durable state after either success or denial.
For mass assignment, use a synthetic server-owned property and verify whether it persisted, not whether it was echoed.
A response echo without a state or permission change does not confirm assignment.

## Transport controls

- gRPC: compare a permitted and denied method using the same test identity; capture interceptor identity, application status and trailers.
- Verify that client-supplied identity metadata cannot replace the authenticated principal; use inert test identity labels.
- A successful HTTP transport status does not establish gRPC success, and reflection visibility alone is inventory.
- WebSocket: establish a normal authorized message, then change only the referenced fixture or revoke its permission.
- Record whether long-lived connections revalidate messages within the declared invalidation interval.
- Validate cross-origin browser behavior with a dedicated test page and synthetic cookies; a command-line Origin header does not reproduce browser credential policy.
- CORS: observe whether the test browser can read protected fixture data, rather than concluding from preflight headers alone.
- Keep API version comparisons limited to routes identified in supplied specs or source, without speculative endpoint enumeration.

## Failure modes, evidence and versions

Include gateway policy, effective principal, handler ID, serializer projection and before/after fixture state.
Distinguish field readability from writability and public response metadata from private data.
Record client retries, redirects and automatic credential propagation that could invalidate paired requests.
Pin gateway, framework, protobuf/gRPC and WebSocket library versions; verify tool options before replay.
No operational tooling was executed during this rewrite; CLI success and scanner output are not target evidence.

## Remediation and detection

Apply policy at the common resource/action boundary and bind only explicitly writable fields.
Propagate authenticated identity through trusted server context, not caller-controlled metadata.
Log permission decisions and mutation outcomes under the same request ID without bearer values.
Validate a detection for denied message access and a regression assertion that forbidden fields remain unchanged.
Restore fixture permissions and close test connections while retaining the evidence bundle.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| A restricted synthetic role persists a server-owned property through an alternate serializer while the ordinary route denies it. | CONFIRMED; FAIL for the field boundary. |
| A route returns 200 but projects only caller-owned data and leaves forbidden state unchanged under verified middleware policy. | REFUTED for the alleged foreign access; PASS for the tested case. |
| A tool reports an administrative endpoint but no authenticated replay or state inspection occurred. | CANDIDATE; WARN. |

Acceptance cases specify expected behavior; they are not executed target tests.

## Provenance

Exact upstream path: `Skills/api/offensive-api-security/SKILL.md`.
Treatment: Strengthens the existing cross-transport boundary skill while routing object relationship detail, GraphQL execution and consumption accounting to distinct domain skills.

Methodology adapted from Claude-Red `offensive-api-security` at commit `a8de813edc9f66f60d44cfe42d47750e89d9930b`. See [collection provenance](../PROVENANCE.md). This is a rewritten assessment workflow, not a verbatim upstream skill.

