---
name: client-side-trust-boundary
description: Treat any code or data that runs on a device the user controls as code and data the adversary controls — the mobile app, the single-page app, the desktop client, the game — because the user can root the phone, hook it with Frida, bypass the certificate pin, read the "encrypted" local database, and patch out any check you shipped, so a security decision made client-side is a suggestion, never a control. Use whenever the subject is a client that runs on hardware you do not own: "is it safe to store this in the app", "we validate on the client", "the API key is in the mobile app", "cert pinning / SSL pinning", "jailbreak / root detection", "obfuscate the code", "the price/feature-flag/isPremium is checked in the app", "reverse engineering our app", "IDOR/BOLA in the mobile API". Sibling of validate-at-the-boundary (this is its client-side corollary — the server must re-make every decision) and agent-trust-boundaries (an untrusted execution context); it maps what you wrongly trust on the far side. It does not write the mobile app or the server, and never accepts a client-side check, secret, or obfuscation as a security property.
---

# Client-Side Trust Boundary

The line where your code stops running on hardware you control and starts running on
the user's device is the most under-respected trust boundary in software. Past that
line, everything is negotiable: the attacker owns the CPU, the memory, the storage, the
network stack, and the debugger. They can root the phone, attach Frida and rewrite any
function at runtime, bypass the certificate pin, dump the "encrypted" SQLite with the
key sitting three files over, decompile the APK, and flip the `isPremium` boolean. **A
security decision that is made only on the client has not been made.** It has been
suggested to an adversary who is free to decline.

Two failure modes, and both come from mistaking "the code we shipped" for "the code
that runs":

- **Trusting a client-side check.** The disabled button, the client-validated price,
  the feature gate, the input validation, the "jailbreak detected → refuse" guard — the
  attacker simply removes it. Worse, root/jailbreak detection and anti-tamper are
  themselves client-side code, so they are defeated by the same instrumentation they
  were meant to catch. A control that runs in the attacker's process protects nothing.
- **Hiding a secret on the client.** The hardcoded API key, the "encrypted" local store
  whose key is derived from something also on the device, the obfuscated algorithm. A
  secret that ships to the client is a disclosed secret; obfuscation raises the cost of
  reading it from minutes to an afternoon, which is not a boundary.

Composes with the library:

- **validate-at-the-boundary** — the server-side corollary: every client input and every client decision is re-validated on trusted ground or it is unvalidated
- **agent-trust-boundaries** — the client is an untrusted execution context whose output cannot carry authority
- **authorization-surface-mapping** — the client can craft any request; the server's authorization is the only real gate (IDOR/BOLA is this failure)
- **secret-lifecycle-discipline** — a secret embedded in a client is already leaked; treat it as compromised from ship
- **credential-material-triage** — an extracted client key is captured material; triage what it actually unlocks
- **honest-degradation** — a control that can only live client-side (offline, DRM) is defeatable; design for the loss, do not pretend it holds

---

## Step 0 — Draw the boundary and declare the far side hostile

Locate, explicitly, where execution crosses onto the user's device. Everything past
that point — app logic, local storage, in-memory values, outbound requests, TLS
endpoints the app talks to — is attacker-influenced. This is Firstness done honestly:
not "the app does X," but "the app *asks* the device to do X, and the device answers to
the user." Write the boundary before you reason about any control, because every claim
downstream depends on which side of it the control lives.

---

## Step 1 — Enumerate the client-side decisions and treat each as void

List every security-relevant decision the client makes, and mark each one **not a
control until it is re-made server-side**:

- Authentication/authorization checks ("is this user allowed to see this screen")
- Input validation ("the app won't let you submit a negative quantity")
- Pricing/business logic ("total computed in the app")
- Feature/entitlement gates ("premium unlocked locally")
- Integrity/anti-tamper/root-jailbreak detection

For each, the question is: *if the attacker deletes or flips this, what stops the
abuse?* If the answer is "nothing, the server trusts the client's word," that is the
finding. The server must independently recompute the price, re-check the entitlement,
re-authorize the action — because the request it receives may have been crafted by hand
with no app involved at all.

---

## Step 2 — Treat every shipped secret as disclosed

Anything the client must *have* to function, the attacker can *extract*:

- Hardcoded API keys, tokens, signing keys → disclosed; triage their blast radius
  (`credential-material-triage`) and prefer a design where the client holds nothing of
  value (server-side proxying, per-user short-lived tokens minted after real auth).
- "Encrypted" local storage whose key is on the same device → the key travels with the
  ciphertext; this is encoding, not protection.
- Obfuscation → a cost multiplier, not a boundary. State honestly that it deters casual
  and scaled attackers and does nothing against a targeted one (base rate: a determined
  reverser with Frida/decompilers reads it routinely).

---

## Step 3 — Separate what the client CAN do from what the server LETS it do

The client can issue *any* request — any endpoint, any object id, any parameter,
regardless of what the UI exposes. Capability is unbounded; the only real gate is
server-side authority. Every "the app only ever requests its own data" assumption is
an IDOR/BOLA waiting to happen. Route authorization through
`authorization-surface-mapping`: the server must check, on every request, that *this*
principal may perform *this* action on *this* object — never inferring permission from
the fact that a well-behaved client would not have asked.

---

## Step 4 — Rate anti-tamper honestly: speed bumps, not walls

Certificate pinning, root/jailbreak detection, integrity attestation, obfuscation, and
anti-debugging are worth having — they raise attacker cost, cut down casual and
automated abuse, and are appropriate defense-in-depth. But they are speed bumps, and
naming them as boundaries is where teams get breached. State for each what it actually
buys (deters scaled/casual attacks, adds reverse-engineering cost) and what it does not
(stops a targeted attacker instrumenting the process). Never let a security property
*rest* on one. Play integrity / hardware attestation is the partial exception — it
anchors below the app — and belongs to `root-of-trust-reasoning`, not to app code.

---

## Step 5 — When a control can only live client-side, design for its defeat

Some requirements are inherently client-side: offline-first enforcement, DRM,
rate-limiting a fully local action. You cannot make these unbreakable. Honest
degradation means: assume the control is defeated, and bound the damage —
server-side reconciliation that detects the tampered state after the fact, limits on
what a compromised client can affect, and monitoring that treats client-reported state
as a claim, not a fact. Say in the design "this is enforced only on the client and is
therefore defeatable; here is what limits the blast radius," instead of shipping a
client check and calling the requirement met.

---

## The one-line test

If the only thing standing between an attacker and the abuse runs on the attacker's own
device, then nothing stands between them and the abuse. Move the check to the server, or
write down plainly that the requirement is unenforced and design for the loss.
