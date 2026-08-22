---
name: authorization-surface-mapping
description: Build the actor × resource × action matrix a system implicitly claims to enforce, then test the cells it never wrote a test for — because authorization bugs are absences, and you cannot grep for an absence. Use whenever a system has more than one kind of user, more than one tenant, or any object with an owner — multi-tenant SaaS, admin panels, org/team/workspace models, RBAC or ABAC policy, sharing and invitation flows, API keys with scopes, service accounts, feature flags that gate privilege. Trigger on "IDOR", "BOLA", "broken access control", "can user A see user B's data", "tenant isolation", "row-level security", "privilege escalation", "who can access this endpoint", "check permissions", "admin bypass", "scoped token", "impersonation", "we added a role", or a new endpoint that takes an object id. Sibling of invariant-hunting, which follows one property across a transition; this skill enumerates the whole grid so no cell is untested. It maps and tests authorization; it does not design the policy engine.
---

# Authorization Surface Mapping

Broken access control is the most-reported serious bug class in real systems,
and it stays that way because of an asymmetry: a *present* check is visible in
the diff, in the code, in the test suite. A *missing* check looks exactly like
nothing. Reviewers read what is there. Attackers enumerate what should be
there and is not.

You cannot grep for an absence. You can only enumerate the grid the system
implicitly promises to enforce and check the cells nobody thought about:

> **actor × resource × action → allowed / denied.**
> The bugs are in the cells the developers never imagined a request for.

The second discipline of this skill is that **authorization is proven by the
denial, not by the permission.** A test suite where every case passes as the
rightful owner proves the feature works. It says nothing about access control.
A green suite full of positive tests is the single most common reason an IDOR
survives to production.

Composes with the library:

- **invariant-hunting** — takes one row of this matrix and asks whether the
  decision survives to the sink; this skill decides which rows exist
- **attack-surface-triage** — ranks which cells to test first
- **falsifiable-testing** — the negative test is the test; positive-only suites
  are its "tests that cannot fail" taxonomy applied to authz
- **oracle-driven-fuzzing** — sequence fuzzing over the state machine finds
  the transition-created cells nobody enumerated
- **discriminating-proof** — a 200 response is a lead until you prove the data
  belonged to another principal
- **forensic-logging-design** — every denial and every grant must be legible
  afterwards

Authorization to test: systems you own or are explicitly authorized to probe,
with accounts you were given. Never test isolation using a real customer's
data — provision two of your own tenants.

---

## Part 1 — Enumerate the three axes honestly

**Actors** are not just roles. List every distinguishable principal:

- unauthenticated
- authenticated but unrelated (a valid user of another tenant — the most
  under-tested actor in every system)
- each role: member, admin, owner, billing, read-only, support
- invited-but-not-accepted, suspended, offboarded, deleted-but-token-alive
- service accounts, CI principals, internal callers, and *the system itself*
- an API key or OAuth token with a narrower scope than its owner
- a delegated/impersonating principal (support acting as a user)

**Resources** are every object with an id that appears in a request, plus the
ones that do not: nested children (`/orgs/1/projects/2/keys/3` — is `3` checked
against `2`, or only against the caller?), soft-deleted rows, exports, audit
logs, aggregate counts, autocomplete suggestions, error messages, and
attachments served from object storage.

**Actions** are CRUD plus everything teams forget: list, search, export,
share, transfer ownership, invite, change role, revoke, restore, and the
*metadata* actions — "does this id exist?" is an action, and a 404-vs-403
difference answers it.

The grid is large. That is the point: the developers who built it never wrote
it down, so its uninhabited regions were never considered.

## Part 2 — The cells where the bugs actually are

Rather than test the whole grid uniformly, go straight for the families that
recur across every codebase:

1. **Object reference not scoped to the caller.** The handler authenticates the
   user, then fetches `Order.get(id)` without `WHERE tenant_id = caller.tenant`.
   Classic IDOR/BOLA. Hunt: every query that looks up by primary key alone.
2. **Nested resource checked at the wrong level.** Parent authorized, child
   assumed. `/projects/{p}/documents/{d}` where `d` is fetched globally.
3. **Function-level gap.** The UI hides the button; the endpoint does not check
   the role. Hunt: every route the frontend calls only from an admin screen.
4. **Field-level gap.** The object is yours, but the request body sets
   `role: "owner"`, `tenant_id`, `is_verified`, or `price`. Mass assignment is
   an authorization bug wearing a serialization costume.
5. **Read path vs write path divergence.** Write is guarded, read is not (or
   the reverse). Search, export, and list endpoints are the usual escapees
   because they were added later, by someone else.
6. **The stale principal.** Role revoked, membership removed, user suspended —
   but the existing session, cached claim, or JWT keeps the old grant until
   expiry. Ask: what invalidates an already-issued authority?
7. **Scope not enforced below the token check.** The token is validated as
   authentic and its `scope` claim never re-read at the action.
8. **Cross-tenant collision in a shared namespace.** Cache keys, file paths,
   queue names, or search indices keyed without the tenant.
9. **Privilege gained by transition.** No single step escalates, the sequence
   does: invite yourself → accept → transfer ownership → remove the other
   owner. Enumerate *paths*, not just cells.
10. **Inference channels.** Timing, response length, existence oracles,
    autocomplete, notification emails, and rate-limit counters that leak the
    presence of other tenants' objects.

## Part 3 — Test the matrix, do not read it

Reading the code proves the check *exists*. Only a request proves it *fires*.
The technique that finds these bugs in minutes:

**Capture as high privilege, replay as low privilege.** Perform the action as
the rightful owner, record the exact request, then replay it with only the
credential swapped — everything else byte-identical. That last clause is the
negative control (`discriminating-proof`): if you change the id *and* the token
*and* a header, a 403 tells you nothing about which one caused it.

Run each cell three ways, because the three answers mean different things:

| Replay as | Expected | If it succeeds |
|---|---|---|
| No credential | 401 | Unauthenticated access |
| Valid credential, other tenant | 404/403 | Cross-tenant break — usually critical |
| Valid credential, same tenant, lower role | 403 | Privilege escalation within the tenant |

And record what a *denial* looks like: 403 with the object's name in the error
message is still a disclosure; a 404 that takes 300 ms for existing objects and
20 ms for absent ones is an existence oracle.

**A 200 is not yet a finding.** Confirm the response actually contains the other
principal's data — an empty list, a redacted object, or your own tenant's data
under a foreign id are all "the control worked". Diff the response against the
legitimate owner's response for the same object.

## Part 4 — The blue deliverable

The matrix is worth more to the defenders than any individual finding, because
it converts one bug into permanent structure. Ship all four:

1. **The matrix itself**, as a checked-in document — the first written record
   of what the system claims to enforce. Half the value of this skill is that
   this artifact did not exist before.
2. **Negative tests, generated from the matrix**, in CI. One parameterized test
   over (actor, resource, action) whose assertion is *denied*, and which fails
   loudly when a new endpoint is added without a row. This is the fix that
   survives the next twenty features.
3. **The structural remediation, not the point fix.** Rank it: enforce in the
   data layer (row-level security, a tenant-scoped repository or query builder
   that *cannot* express an unscoped read) > a policy middleware that denies by
   default and requires each route to declare its rule > a check inside each
   handler, which is where the next gap will be. Deny-by-default routing means
   a forgotten check fails closed instead of open.
4. **A detection requirement** for `detection-engineering`: cross-tenant object
   access, a principal whose 403 rate spikes, or an id enumeration pattern.
   These are among the few detections with a naturally near-zero false-positive
   rate, because legitimate clients do not request other tenants' ids.

---

## Deliverable

```
## Authorization surface — <system> <version>
Actors: <list, including the ones with no UI>
Resources: <ids that appear in requests, and the ones that do not>
Actions: <CRUD + list/search/export/share/transfer/invite/role-change>

### Matrix
| actor | resource | action | expected | observed | evidence |
Cells not tested, and why: <coverage statement — never imply a full sweep>

### Findings
<id> — cell — replay evidence (request diff) — epistemic level — impact

### Structural remediation
<data-layer enforcement / deny-by-default routing / generated negative tests>
```

## Anti-patterns

- Reading the middleware, concluding "auth is enforced", and never sending a
  request.
- Testing only as the object's rightful owner. That is a feature test.
- Changing the id and the credential in the same replay, so the result is
  uninterpretable.
- Reporting a 200 as a break without confirming the body holds foreign data.
- Treating a hidden UI control as an access control.
- Enumerating cells but never sequences — the escalation is often a path.
- Patching the one handler that leaked and leaving the other forty unscoped
  queries in place.
- Shipping the fix without the generated negative test, guaranteeing the next
  endpoint reopens the hole.
