---
name: credential-material-triage
description: Turn "we found a credential" into a finding by triaging what the material actually is, what it authenticates as, what it authorizes, for how long, and how to revoke it — because a Slack webhook and a long-lived cloud root key are both "a secret" and differ by orders of magnitude in blast radius. Use whenever secret material surfaces: a leaked key in a git commit or CI log, a password/hash dump, a captured Kerberos ticket, an OAuth access or refresh token, a session cookie, an SSH or signing key, a JWT, a private key, an `.env` in an S3 bucket. Trigger on "we found credentials", "is this exposed key a problem", "should we rotate", "pass-the-hash", "the token leaked", "how bad is this secret", "found in the repo history", or a pentest that captured hashes. Sibling of secret-lifecycle-discipline (which governs a secret's whole life) and assume-breach-modeling (which maps what the holder reaches); this skill sits between them, classifying captured material by what it grants. It does not design the vault or rotation system, and never inflates "we found hashes" into "accounts are compromised" without stating crackability.
---

# Credential Material Triage

"We found a credential" is not a finding. It is the noticing of a string that looks
secret. The finding is: *what kind of material is this, what identity does it
authenticate as, what does that identity authorize, over what scope, for how long,
can it be used offline, and how is it revoked.* Two artifacts that both read as "a
secret" — a 15-minute STS token and a non-expiring IAM access key with `iam:PassRole`
— are separated by orders of magnitude of consequence, and a triage that calls them
both "exposed credential, severity high" has told you nothing.

The two symmetric errors this skill kills:

- **Inflation.** "We dumped the NT hashes, the accounts are compromised." A hash is
  not a password; whether it is *usable* depends on the protocol (pass-the-hash vs
  relay-only vs must-crack) and, if it must be cracked, on the password's strength. A
  bcrypt of a 20-char passphrase is, for practical purposes, inert. Reporting it as
  "compromised" is the same overclaim `red-team-auditing` forbids everywhere else.
- **Deflation.** "It's just a read-only token, low severity" — for a refresh token
  that mints new access tokens indefinitely, or a "read-only" cloud role that can read
  every other secret in the account. Scope and refreshability, not the label, set the
  severity.

Composes with the library:

- **assume-breach-modeling** — the triage feeds it: assume this material is in hostile hands now, what position does it grant and reach next
- **secret-lifecycle-discipline** — governs the secret's creation/rotation/revocation; this skill decides how *urgent* that is
- **authorization-surface-mapping** — "what it authorizes" is an actor×resource×action question; resolve it there, don't guess
- **cloud-control-plane-reasoning** — a cloud key's real reach is its policy set plus everything it can assume transitively
- **honest-degradation** — unknown TTL / unknown scope caps the verdict; do not resolve the unknown to worst or best case
- **daubert-defensible-writing** — "compromised" is a claim; "NT hash, pass-the-hash-usable without cracking, valid domain-wide" is a defensible one

---

## Step 1 — Classify the material (the class sets the physics)

Name the exact type, because each type has different rules for use, lifetime, and
revocation. Do not stop at "a token" or "a key."

- **Password (cleartext)** — usable everywhere the account is, online; revoked by
  change; may be reused across systems (the real blast radius).
- **Password hash** — the critical fork: *how is it usable?*
  - NT hash → **pass-the-hash / relay usable without ever cracking**; NTLMv2 response →
    relay/crack-only, not pass-the-hash. State which.
  - Fast unsalted (MD5/SHA1/NTLM) → offline-crackable at scale; slow salted
    (bcrypt/scrypt/argon2) → crackability depends entirely on password strength.
  - Kerberos: an **AS-REP or Kerberoastable TGS** is an offline-crackable ticket, not a
    live credential.
- **Kerberos ticket** — TGT (authenticates as the user for anything) vs service TGS
  (one service); golden (forged TGT, krbtgt) vs silver (forged TGS, service key).
  Lifetime and renewal window matter.
- **OAuth / OIDC token** — **access token** (short-lived, bearer) vs **refresh token**
  (long-lived, *mints new access tokens* — the real prize); scopes; MFA-bound or not.
- **API key / cloud key** — static long-lived (IAM access key, no expiry) vs temporary
  (STS/Sed session, minutes-to-hours). Static is a standing door; temporary is a
  closing one.
- **Session cookie** — bearer, valid until expiry/logout; often bypasses MFA entirely.
- **SSH / signing / TLS private key** — long-lived, revoked only by rotation +
  distributing trust changes; a signing key compromises everything it ever signs
  forward *and* backward.
- **JWT** — inspect claims (`aud`, `scope`, `exp`); if signed with a key you also
  found, or `alg:none`-forgeable, it is a *minting* capability, not one token.

---

## Step 2 — Resolve the five properties that set blast radius

For the material in hand, answer each; where you cannot, mark it UNKNOWN (Step 4),
do not assume:

1. **Authenticates as** — which principal/identity. (A service account is often *more*
   dangerous than a user: no MFA, broad rights, no one watching.)
2. **Authorizes** — the actual permission set, resolved against the real policy, not
   the name. "read-only" is a label; `secretsmanager:GetSecretValue` on `*` is the
   fact. Route this through `authorization-surface-mapping` / `cloud-control-plane-reasoning`.
3. **Scope of validity** — one service, or SSO-federated across many, or domain-wide?
   Where else does this exact material work? Password reuse and SSO turn one leak into
   many.
4. **Lifetime & refreshability** — TTL, renewal window, and crucially whether it
   *regenerates* itself (refresh token, renewable TGT). A self-renewing credential is
   not a window that closes on its own.
5. **Revocability** — can it be killed *now* (session invalidation, key deletion, token
   revocation endpoint), or only by rotating an underlying key and redeploying? A
   non-revocable long-lived key is a different emergency than a revocable token.

---

## Step 3 — Blast radius and chaining (assume it is already stolen)

Do not evaluate the credential in isolation; evaluate the *position* it grants,
assuming it is in an attacker's hands as of now:

- **Direct reach** — everything Step 2's "authorizes × scope" grants.
- **Chaining** — what this credential *reaches into*: a refresh token → a stream of
  access tokens; a key with `iam:PassRole` → a more-privileged role → the control
  plane; a TGT → effectively the domain; a CI token → the deploy pipeline → production.
  The single most under-rated material is the one that mints or assumes other
  credentials. Hand the position to `assume-breach-modeling` for the full graph.
- **Reuse surface** — is this password/key used in other systems, other repos, other
  environments? The blast radius of a reused secret is the union of everywhere it works.

---

## Step 4 — Exposure history: the string outlives the rotation

A credential that was exposed is not made un-exposed by the fix. Establish:

- **Exposure window** — how long was it reachable, and *by whom* (public repo vs
  internal log vs memory dump)?
- **Was it used?** Check auth logs for use from unexpected sources during the window.
  "Exposed but no evidence of malicious use" is a WARN, not a PASS — absence of
  evidence is bounded by your logging (`forensic-logging-design`).
- **Where does the string persist after rotation?** Git history, CI/CD logs, container
  layers, backups, screenshots, the memory dump, a Slack message, a browser's saved
  form data. Rotating the live value does not scrub these; the old secret is still
  valid wherever an old artifact still trusts it. This is where "we rotated it" quietly
  fails to be "it's contained."

---

## Step 5 — Rank the response by revocability × blast radius, and state the unknowns

Response urgency is not a function of "it's a secret" — it is a function of how much it
grants and how hard it is to kill:

- **Revoke now** — high blast radius *and* revocable (kill the session, delete the key,
  hit the revocation endpoint). Fastest containment; do it first.
- **Rotate + hunt** — high blast radius but only rotatable (static key, private key,
  password): rotate everywhere it is valid (Step 2.3), *and* hunt for use during the
  exposure window (Step 4), because rotation closes the future, not the past.
- **Monitor / accept** — genuinely low reach *and* short-lived *and* self-expiring, with
  the reasoning written down.

Every UNKNOWN from Step 2 is a cap on the verdict, stated explicitly: unknown scope or
unknown TTL means you triage to the *more* urgent bucket and say why, rather than
silently assuming it is fine. "Unknown blast radius" is itself the finding that the
environment cannot tell what this credential unlocks.

---

## The one-line test

If you cannot state, in one sentence, *what this material authenticates as, what it
authorizes, for how long, and how to revoke it*, you have not triaged a credential —
you have noticed a string that looks secret. Everything before those four facts is
severity theater.
