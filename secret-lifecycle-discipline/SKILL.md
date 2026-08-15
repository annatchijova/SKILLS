---
name: secret-lifecycle-discipline
description: Treat credentials as a lifecycle — issued, scoped, distributed, used, rotated, revoked — with redaction enforced at the boundary and rotation rehearsed before it is needed. Use whenever a secret is created, read, passed, logged, printed, committed, or exposed: API keys, tokens, passwords, private keys, connection strings, webhook signing secrets, service accounts. Trigger on "store this API key", "put it in the env", "we committed a secret", "rotate the credentials", ".env", "vault", "the token leaked", "redact the logs", "why is the key in the URL", "this test needs real credentials", or a diff containing a high-entropy string. Also trigger when an agent or LLM context could receive a credential, and when a debug/error path might serialize configuration. Includes the exposure axiom (written where it can be read = compromised = rotate), leak-channel inventory, and the post-exposure playbook.
---

# Secret Lifecycle Discipline

Secrets are usually treated as a storage problem — pick a vault, done. Storage is
the easy part. Nearly every real credential incident happens somewhere else: in
transit through a log line, in a URL, in a git object that was never rewritten,
in a container layer, in a crash report, in a support ticket, in a model's
context window.

A secret has a life: it is **issued, scoped, distributed, used, rotated,
revoked**. Weakness at any stage costs you the whole thing, and the stage most
organizations have never rehearsed is rotation — which means they discover it is
broken during an incident, which is the one moment it must work.

Composes with: `validate-at-the-boundary` (redact where data crosses out, not at
each call site), `irreversible-action-gate` (a leak is R3 — it cannot be
un-read), `falsifiable-testing` (redaction is a testable claim), `agent-trust-boundaries`
(exfiltration channels), `incident-timeline-reconstruction` (the exposure window),
`tamper-evident-audit-chain` (credential use records).

---

## Part 1 — The exposure axiom

> **A secret written anywhere it can be read is compromised. Rotate it.**

Not "assess whether it was likely read". Not "the repo is private". Not "only the
team has log access". The reasoning people reach for — *nobody would have looked*
— is unfalsifiable in the wrong direction: you cannot observe the absence of a
read, and the parties who would know are the ones you are worried about.

This is a design decision, not paranoia: the cost of rotating is bounded and
known; the cost of being wrong is unbounded. If rotating feels too expensive to
do on suspicion, that is the finding — **your rotation process is broken**, and
Part 4 is the fix.

Corollary: **"we removed it" is not remediation.** Deleting the line, force-pushing,
deleting the log, or deleting the message removes the copy you control. Rotation
is the only action that actually invalidates the credential.

---

## Part 2 — Where secrets actually leak

Audit for these specifically; the list is short and the same names keep appearing:

- **Logs** — not the log statements you wrote, but the ones you did not: exception
  handlers that dump request objects, framework debug modes, retry logic logging
  full headers, `print(config)` left in, structured loggers serializing an object
  whose `__dict__` contains a token.
- **URLs** — a credential in a query string ends up in server access logs, proxy
  logs, browser history, and `Referer` headers sent to third parties. Secrets go
  in headers or bodies. Presigned URLs *are* credentials, and are equally
  loggable.
- **Git history** — the object survives the follow-up commit. Forks, clones, CI
  caches, mirrors, and code-search indexes may already have it. History rewriting
  is a cleanup, not a remediation, and it cannot reach the copies.
- **Container image layers** — a secret added in one layer and deleted in the next
  is still in the image. Same for build caches and CI artifacts.
- **CI output** — an echoed variable, a `set -x` trace, a failing step printing
  its environment. Masking helps only for values the runner knows about, and only
  when they are not transformed (base64'd, concatenated, JSON-embedded).
- **Crash and telemetry pipelines** — the error reporter that ships local
  variables and environment to a third-party SaaS. This is exfiltration with a
  contract.
- **Human channels** — support tickets, chat, screenshots, pasted config, docs.
- **Model and agent contexts** — a credential in a prompt, in tool output, or in a
  file an agent reads is now in a context that may be logged, cached, sent to a
  provider, or coaxed out later (`agent-trust-boundaries`).
- **Test fixtures and notebooks** — real credentials used "just to check", then
  committed with the output cells.

---

## Part 3 — Redact at the boundary, and test it

Redaction applied at each call site fails the first time someone adds a new call
site. Put it where the data leaves:

- **Type the secret.** Wrap credentials in a type whose string and repr forms
  render `***`, whose value requires an explicit `.reveal()`, and which refuses to
  serialize by default. This turns "remember not to log it" — an instruction that
  degrades — into a property of the value that travels with it everywhere.
- **Filter in the logger/serializer**, by key name *and* by pattern, on the whole
  structure, recursively. Deny-list of key names is the floor, not the ceiling:
  values arrive under names you did not predict.
- **Never let the fallback be the raw value.** A redactor that logs the original
  when it fails to parse is worse than none.
- **Assert it.** A test that runs an operation with a canary credential and
  asserts the canary appears in no log, no error message, and no serialized
  output. This is `falsifiable-testing` applied to a claim everyone makes and
  nobody checks — and it is one of the highest-value tests in a codebase, because
  the failure it catches is silent and permanent.
- **Scan pre-commit and in CI**, but understand what scanning is: a net for
  accidents, not a control. It catches known shapes and misses your internal
  format entirely. Add your own credential formats to the patterns.

---

## Part 4 — Rotation is a capability, not a chore

The question that determines whether you can respond to an incident: **can you
rotate this credential right now, without downtime, without a deploy, without a
person who is on holiday?**

Rotation requires **two credentials valid at once**. If your design allows only
one, rotation means an outage, and a rotation that causes an outage will be
deferred — including during the incident where it matters. Build the overlap:
issue the new credential, distribute it, let consumers accept both, verify the new
one is in use, then revoke the old one *explicitly* (revocation is the step that
gets skipped, and an un-revoked old credential means you have not rotated, you
have merely added).

Then reduce what rotation has to cover:

- **Short-lived and workload-identity credentials** are the strongest control
  here: a token that expires in an hour bounds the value of a leak far more than
  any vault does for a token that never expires.
- **Scope narrowly**: per service, per environment, per purpose. A credential
  shared across three services cannot be rotated without coordinating three
  teams, so it never gets rotated, so it is the one that leaks and matters most.
- **Never share across environments.** A staging credential that works in
  production makes every staging exposure a production incident.
- **Inventory ownership and expiry.** A credential with no owner is a credential
  nobody will rotate. A credential with no expiry is one nobody will notice is
  stale.
- **Rehearse.** Rotate a real credential on a schedule while nothing is wrong.
  The first attempt always finds a consumer nobody knew about.

---

## Part 5 — When it has been exposed

Order matters, and the instinct to investigate first is wrong:

1. **Rotate and revoke.** Immediately, before determining scope. The window you
   are trying to close is open while you investigate.
2. **Establish the exposure window** — from when the secret first reached the
   exposed location to when the old credential was revoked. Not when you noticed.
   Use `incident-timeline-reconstruction`; the window's start is usually much
   earlier than the discovery.
3. **Look for use, not just exposure.** Query the provider's access logs for the
   old credential during the window: from where, by what, doing what. Absence of
   evidence is only meaningful if the logs actually cover the window — say which
   (`NOT COLLECTED` / `NOT LOGGED` / `NO ACTIVITY`).
4. **Assume propagation.** Public git object → assume cloned and indexed. Third
   party log → assume retained per their policy, and that deletion is a request,
   not an action you control.
5. **Check what the credential could reach**, and treat that blast radius as
   potentially touched: what data, what actions, what other secrets it could read
   (a credential that can read the vault is every credential).
6. **Fix the channel, not just the credential.** The same path will leak the
   replacement next month if the error handler still serializes config.
7. **Write it down** with the epistemic honesty of `daubert-defensible-writing`:
   "no evidence of use, within a log window covering X to Y" is a real finding.
   "It was not used" is a claim you cannot support.

**Canaries close the loop.** Plant credentials that are valid, useless, and
alerting — in a repo, in a config file, in an S3 bucket, in a document. They have
no false positives: nothing legitimate ever uses them. This is the cheapest
high-fidelity detection in existence, and it works exactly where secrets actually
leak. Pair with an alert on any use of a decommissioned credential
(`detection-engineering`).

---

## Deliverable checklist

```markdown
## Secret lifecycle review

Inventory: secret → owner → scope (svc/env/purpose) → TTL/expiry → where stored → who can read
Issuance: short-lived / workload identity available? shared across envs? (must be no)
Redaction: typed wrapper? boundary filter (recursive, key+pattern)? canary test asserting absence?
Leak channels checked: logs · URLs · git history · image layers · CI output · crash/telemetry ·
  human channels · model/agent context · notebooks & fixtures
Rotation: two-valid-at-once supported? downtime required? last rehearsed? revocation step explicit?
Exposure response: rotate-first playbook exists? provider access logs available & retained how long?
Canaries: planted where? alert on decommissioned-credential use?
```

---

## How to respond when this skill is active

- If a secret was exposed anywhere readable, say plainly: rotate. Do not help reason about whether it was probably seen.
- Correct "we removed it" to "removed ≠ remediated" — name rotation as the only invalidating action.
- When a secret is going into a URL, a log, a test fixture, or a model prompt, stop and offer the header/body/typed-wrapper/short-lived alternative.
- Propose a typed secret and a boundary-level redactor over per-call-site discipline, and write the canary test that proves it.
- Ask whether two credentials can be valid at once. If not, treat that as the finding — rotation is not a capability yet.
- In an exposure, order the work rotate → window → provider access logs → propagation → channel fix, and state coverage gaps in the logs rather than concluding non-use.
- Suggest canary tokens whenever detection comes up; they are the highest-fidelity, lowest-noise option available.
