---
name: zero-trust-as-a-claim
description: Treat "zero trust" as a per-request property to be verified, not a product you bought or a network you segmented — the honest question is always "trusted to do what, verified how, on every request", and the failure is the implicit trust that survives the architecture diagram: a flat network behind the VPN, a service mesh that authenticates identity but never authorizes the action, an internal API that trusts any caller who reached it. Use whenever "zero trust" is claimed, designed, or bought: "we implemented zero trust", "is this zero trust", "ZTNA", "we have a service mesh so we're zero trust", "microsegmentation", "trust but verify", "the request came from inside the network", "east-west traffic", "should this service trust that one". Sibling of authorization-surface-mapping (every request is an actor-resource-action to authorize) and agent-trust-boundaries (authority comes from the channel, not the position); it audits the trust claim. It does not sell or configure a ZTNA product, and never accepts network position, a valid mTLS identity, or "it's internal" as authorization.
---

# Zero Trust as a Claim

"Zero trust" is not a product, a network topology, or a box you checked when you bought
a ZTNA gateway. It is a *property of every request*: that the request is authenticated,
authorized for the specific action, and evaluated on its own merits rather than trusted
because of where it came from. Stated as a slogan it is marketing; stated as a claim it
is falsifiable — and the useful move is always to falsify it, because the interesting
answer is where implicit trust *survived* the architecture that was supposed to remove
it.

The honest question is never "are we zero trust?" (unanswerable, unfalsifiable). It is
**"this request — trusted to do what, verified how, and re-verified when?"** Ask it at
each hop and the residual trust becomes visible.

The failure modes are all the same shape — trust that moved rather than disappeared:

- **The perimeter that moved inward.** The VPN / ZTNA gateway authenticates you once at
  the edge, and behind it the network is flat: reach one service and you reach them
  all. The castle wall got a better front door and the same open courtyard.
- **Authentication mistaken for authorization.** A service mesh gives every workload an
  mTLS identity and proves *who is calling* — and then authorizes nothing, so any
  authenticated workload can call any endpoint. Knowing the caller's name is not
  deciding what the caller may do.
- **"It came from inside."** An internal API, a message on the internal bus, a request
  from a trusted subnet — trusted *because of its origin*, which is precisely the
  implicit trust zero trust is defined against.

Composes with the library:

- **authorization-surface-mapping** — every request is an actor-resource-action cell that must be authorized; zero trust is that matrix enforced per request
- **agent-trust-boundaries** — instruction/authority comes from the verified channel, not from having reached the position; the same principle
- **assume-breach-modeling** — zero trust's premise *is* assume-breach; test it by assuming the caller is already compromised
- **cloud-control-plane-reasoning** — identity is the perimeter; a workload identity that is authenticated but over-authorized is the mesh failure in cloud form
- **honest-degradation** — "we have zero trust" is a WARN-worthy overclaim unless you can point at the per-request authorization; name what is actually enforced

---

## Step 1 — Restate the claim as per-request verification, then hunt the exceptions

Take whatever "we do zero trust" means in this system and rewrite it as a testable
claim: *for each request between components, the receiver authenticates the caller,
authorizes the specific action, and does not rely on network position.* Now hunt every
place that is not true:

- Which internal calls are authorized only by "you reached me"?
- Which trust boundaries are actually network boundaries in disguise (a subnet, a VPC, a
  "trusted zone")?
- Where does a single successful authentication grant broad, unre-verified access for a
  long session?

Each exception is a finding. The architecture diagram that says "zero trust" across the
top is the claim; the exceptions are the truth.

---

## Step 2 — Separate authenticated from authorized at every hop

The single most common zero-trust failure is stopping at identity. For each component
that receives requests:

- **Authentication** — does it know *who* is calling (mTLS, signed token, verified
  identity)? Necessary, and where most "zero trust" implementations stop.
- **Authorization** — does it decide whether *this caller* may perform *this action on
  this resource*? This is the half that actually contains a breach, and the half a mesh
  or an API gateway frequently omits.

A system where every service authenticates and nothing authorizes is not zero trust; it
is a well-labeled flat network. Route the authorization question through
`authorization-surface-mapping` — the point is that it must be answered *per request*,
not once at login.

---

## Step 3 — Network position must grant nothing

Test the premise directly: assume the caller is inside — behind the VPN, on the trusted
subnet, holding a valid workload identity, already on an internal host — and ask what
that *position* grants that a verified authorization would not.

- If reaching the network buys access, trust is positional and the claim is false.
- "East-west" traffic (service-to-service) is where positional trust hides, because the
  perimeter mindset only ever guarded north-south. A breach's entire lateral movement
  lives in the east-west trust nobody removed.

The correct answer is that being inside grants *nothing* — every internal request is
authorized as if it came from the internet.

---

## Step 4 — Continuous, not once: re-verification and revocation

Zero trust is per-request and *ongoing*, not a one-time gate:

- Is trust re-evaluated as context changes (device posture, risk signals, session age),
  or granted once and held until an hour-long token expires?
- Can access be *revoked* mid-session, or does a compromised-but-still-valid credential
  ride until natural expiry (the gap `credential-material-triage` cares about)?
- A long-lived, broadly-scoped token issued at login and never re-checked is the
  "verify once, trust forever" pattern wearing zero-trust vocabulary.

---

## Step 5 — State honestly what is enforced, and what is still implicit

Close with the falsifiable inventory, not the slogan: for the system in question, list
where per-request authorization is genuinely enforced, and — the valuable part — where
implicit trust remains (the flat segment behind the gateway, the mesh that only
authenticates, the internal bus that trusts any publisher). "We are zero trust" is an
overclaim; "north-south is per-request authorized; east-west authenticates but does not
authorize; here is the residual implicit trust and its blast radius" is a defensible
statement someone can act on. `ABSTAIN` from the label; report the enforcement.

---

## The one-line test

If a request is trusted because of where it came from — the VPN, the subnet, the
internal network, a valid identity with no check on the action — then the trust did not
go to zero, it moved. Ask of every hop "trusted to do what, verified how, re-checked
when," and the residual trust the diagram hid is your finding.
