---
name: rt-idor
description: "Red-team assessment of insecure-direct-object-reference and broken-object-level-authorization boundaries: numeric/UUID/encoded object IDs, mass-assignment, reference leakage, GraphQL node IDs, gRPC/protobuf, cloud-object URLs and OpenTelemetry leaks. Re-expressed as scoped cross-account experiments using owned test accounts and a bounded ID set with negative controls instead of mass enumeration of real users."
---

# Insecure Direct Object Reference Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's IDOR/BOLA craft as scoped cross-account experiments: it names the reference types and bypasses to test, using two owned accounts and a small bounded ID set rather than mass-enumerating real users' objects.

## Scope and prerequisites

Enumerate endpoints that take an object reference (path, query, body, header, GraphQL node ID, gRPC field). Create two owned accounts (A, B) at the same and different privilege levels. Test access to B's objects from A using a small, bounded set of owned IDs — do not harvest real users' data.

Declare target, attempt budget and a stop condition on first confirmation. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Direct ID swap** — numeric/UUID/slug changed to another object.
- **Encoded/obfuscated ID** — Base64/hashed/sequential-inside-encoding references.
- **Mass assignment** — extra fields (`role`, `owner_id`, `tenant`) accepted on write.
- **Reference leakage** — IDs exposed in one response reused on another endpoint.
- **Representation variants** — same object via GraphQL node ID, gRPC, cloud-object URL, or an observability export.

## Mechanism and observation

Trace a request's object reference to the authorization check (is ownership enforced, or only authentication?).

**Firstness:** Record whether A received B's (owned) object. **Secondness:** State the intended policy (A may access only A's objects) and the deviation. **Thirdness:** Infer broken object-level authorization only after a controlled cross-account read/write succeeds.

## Abduction and refutation

**Mechanism hypothesis:** The endpoint authenticates the caller but authorizes by the supplied object reference rather than by ownership, so changing the reference reaches another tenant's object.

**Competing benign explanation:** The object belongs to A too; a 200 returns an empty/filtered body, not B's data; the ID is an unguessable UUID and the "access" used a leaked legitimate share; a separate authorization layer (OPA/Cedar) actually denies and the response is a generic 404-as-403.

## Deduction and controls

A requesting A's own object succeeds (positive control); A requesting B's object must be refused if BOLA holds. A confirmed IDOR returns B's owned content (a field only B should see) where the control refuses — distinguish a real body from an empty 200. Predeclare the confirming field. A 403/filtered-empty response is a PASS control.

## Induction: bounded laboratory procedure

Two owned accounts; bounded ID set.

1. **Baseline.** As A, access A's object; capture the reference format and a field unique to the owner.
2. **Cross-account read.** As A, request B's (owned) object by its reference; compare the body to B's known content, not just the status code.
3. **Encoding/obfuscation.** Decode the reference; if it wraps a sequential ID, test adjacent owned IDs within the bounded set.
4. **Mass assignment.** On a write, add `role`/`owner_id`/`tenant` fields; check if the server honors them.
5. **Representation variants.** Reach the same object via GraphQL node ID / gRPC / cloud-object URL and re-test authorization per path.
6. **Control.** Confirm A→A succeeds and a known-denied object returns 403/empty.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

GraphQL global IDs often Base64-encode `Type:id`. Function-level endpoints (`/admin/...`) and verb changes (GET vs PUT) can expose BOLA that the UI hides. Authorization-as-code (OPA/Cedar) can have policy gaps distinct from code checks. Observability exports (OpenTelemetry) sometimes leak object IDs and payloads.

## Domain-specific failure modes

A 200 is not access — confirm the body is B's data. UUIDs raise discovery cost but do not fix missing authorization (reference leakage still applies). A single endpoint fixed does not mean sibling representations are; test each path. Empty-but-200 and 404-as-403 are refutations, not confirmations.

## Evidence and deliverable

Provide the endpoint, the two account contexts, the reference swapped, the owner-unique field that proved cross-account access, and the control refusal. Keep real user data out of portable reports; use only owned accounts. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered representations.

## Versions and tool limitations

Automated IDOR tools mass-enumerate — bound the ID set and use owned accounts only. No endpoint behavior was verified by this content; confirm the live authorization model first.

## Remediation and detection

Authorize by ownership at every object access and every representation, use unguessable references but never rely on them as the control, allowlist writable fields (no mass assignment), and centralize object-level checks. Add a regression asserting A cannot read B's object. Detect cross-account access patterns and ID-sweeping correlated to the account.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Account A retrieves/writes account B's owned object (owner-unique field present) where the control refuses: CONFIRMED; FAIL. |
| Benign refutation | The cross-account request returns 403 or an empty body: REFUTED for the tested endpoint; PASS for the control. |
| Insufficient evidence | A 200 with an ambiguous body, owner not confirmed: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-idor/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's reference-type taxonomy, mass-assignment and representation-variant craft, re-expressed as owned two-account experiments with a bounded ID set and ownership-confirming evidence, replacing mass enumeration of real users with scoped cross-account proof.
