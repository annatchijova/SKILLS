---
name: assume-breach-modeling
description: Start from "this step already succeeded" and map what the attacker reaches next — the identity held at that position, everything that identity unlocks, and the choke point whose removal cuts the most paths at once. Use whenever a finding is confirmed and the question turns to impact, whenever a design assumes a component will not be compromised, and whenever containment is being planned or claimed. Trigger on "what's the actual impact", "assume this is compromised", "blast radius", "lateral movement", "if this container/CI job/service account is popped", "worst case", "can they pivot", "defense in depth", "least privilege", "zero trust", "network segmentation", "what does this key unlock", "how would we contain it", or a risk rating that rests on one control holding. Turns red findings into blue architecture. It models reachability from an authorized position and produces containment; it never plans intrusion into systems outside the engagement.
---

# Assume-Breach Modeling

Every security argument has a load-bearing sentence of the form *"but an
attacker cannot get there"*. Assume-breach deletes that sentence and asks what
remains. It is the discipline that turns a single confirmed finding into an
architectural verdict, and it is where red work pays for itself defensively:
a point fix closes one door, a containment fix makes the next twenty doors
open into a small room.

The governing question:

> **Assume this position is held. What identity does the attacker now have,
> what does that identity reach, and what does each thing reached grant next?**

The severity of a finding is not a property of the finding. It is a property of
what sits behind it. "Low severity — it's only an internal service" and
"critical — that service holds a token that can deploy" describe the same bug;
only one of them was traced.

Composes with the library:

- **red-team-auditing** — supplies the confirmed position this model starts
  from; this skill supplies the impact half of its severity
- **invariant-hunting** — each edge here is an invariant claim ("this token
  cannot act on that resource") to be hunted
- **authorization-surface-mapping** — the intra-application edges
- **secret-lifecycle-discipline** — what each reachable credential unlocks and
  whether rotating it is rehearsed
- **agent-trust-boundaries** — when the compromised position is a model with
  tools, the trifecta is the pivot graph
- **purple-team-exercise** / **detection-engineering** — every edge is also a
  detection opportunity
- **irreversible-action-gate** — the containment actions themselves are
  destructive and need their own gate

Scope: model reachability inside the authorized engagement and in systems you
own. Modeling is analysis on paper and safe; *walking* an edge is a live test
and requires the same authorization as any other probe. Never traverse into a
third party because the model says an edge exists.

---

## Part 1 — Define the position precisely

"Compromised" is not a state. Write the starting position as four facts, or the
whole model is fiction:

| Field | Example |
|---|---|
| **Execution** | code runs as `app` inside the API container |
| **Identity** | the container's service account + whatever is in its env |
| **Network vantage** | the pod's egress: which hosts/ports are actually reachable |
| **Data in reach** | the DB rows this identity's credentials can read *today* |

Then state the *cause* only as a label, not a dependency: "arbitrary read as
`app`" is a position whether it came from a path traversal or a supply-chain
compromise. Positions, not exploits, are what the model composes.

Standard positions worth modeling in most systems, regardless of any finding:

- one application container / one worker
- a CI job on a pull request from a fork
- a developer laptop with the credentials it actually holds
- one third-party dependency executing at install or at import
- one SaaS integration's OAuth token
- one leaked long-lived key from a log or a repo
- an agent with tool access that read attacker-controlled content

## Part 2 — Enumerate the edges out of that position

An edge is *anything that converts the current identity into a broader one*.
Walk these categories in order; the first three account for most real
escalation:

1. **Credential reach.** Every secret readable from here: env vars, mounted
   files, the cloud instance metadata endpoint, the CI secret store, the
   config service, a `.git-credentials`, a browser profile, a kube service
   account token. For each: what does it authorize, and is that scope narrower
   than its holder needs?
2. **Trust relationships.** Who accepts this identity without further proof?
   IAM role assumption chains, mutual TLS with a permissive SAN policy,
   allowlisted internal IPs, a shared HMAC secret, a queue every service can
   publish to, an internal API that trusts a header, a service mesh that
   authenticates the mesh rather than the caller.
3. **Data-to-authority conversion.** Read access that becomes write authority:
   session tokens in a cache, password reset rows, a webhook secret, an
   artifact signing key, a config table read at boot, a feature flag store that
   changes behavior in production.
4. **Build and deploy paths.** Can this position influence what runs later? A
   writable artifact bucket, a mutable container tag, a CI cache, a
   post-install script, an admin-editable template. These edges convert one
   host into all hosts.
5. **Network vantage.** From here, what answers? Flat internal networks make
   every service one hop away. Record what is *actually* reachable, not what
   the diagram says — the diagram is a hypothesis.
6. **Human edges.** Access to a mailbox, an on-call channel, or a ticket queue
   converts into approvals granted by people.

Record each edge with an epistemic level (`red-team-auditing`'s ladder):
`CODE FACT` (the env var is in the manifest), `PLAUSIBLE` (this role probably
assumes that one), `CONFIRMED` (walked, in scope, with evidence). An
unlabeled pivot graph is a threat-modeling drawing, not a finding.

## Part 3 — Find the choke point

The output is a graph from the position to the crown-jewel assets. Do not
report the graph; report the **edge whose removal deletes the most paths**.

Method: for each edge, ask what breaks if it disappears. Rank by
`paths_cut / cost_to_remove`. This is what makes the exercise defensive rather
than theatrical — a fifty-node pivot graph is intimidating and unactionable,
while "this one service account can assume the deploy role, and nothing needs
it to" is a ticket someone closes this week.

The recurring high-value choke points:

- a long-lived credential where a short-lived, audience-bound one works
- a wildcard IAM policy on a role assumed by a request-facing service
- one shared secret trusted by many services (breaks *n* boundaries at once)
- a flat network segment holding both the front end and the data store
- CI holding production credentials on pull-request-triggered runs
- a mutable tag or unsigned artifact between build and deploy
- an admin plane reachable from the same identity as the data plane

For each, the remediation is a bulkhead: scope, segment, shorten, or separate.
Prefer changes that make the edge *structurally* impossible (the credential is
minted per request with an audience) over changes that make it *watched*.

## Part 4 — Containment must be rehearsed, not asserted

An incident plan that has never been executed is a hypothesis. For the modeled
position, answer with evidence:

- **Can we revoke it?** Find the actual command that invalidates this identity.
  If the credential is a static key in twelve places, revocation is an outage
  and nobody will pull the trigger during the incident.
- **How fast does revocation take effect?** Cached tokens, JWTs valid until
  expiry, and long-lived connections all keep working after the revoke button
  is pressed. Measure it.
- **Would we know?** Hand each edge to `purple-team-exercise` as a detection
  hypothesis. The edges that are both high-value and unmonitored are the
  priority list for `detection-engineering`.
- **Could we reconstruct it afterwards?** If this identity acted, do the logs
  identify *which* principal and *what* it touched (`forensic-logging-design`)?
  An edge that leaves no trace is worse than one that is merely open.

Rehearse the revocation in a non-production environment and record how long it
took. That number, not the plan document, is the containment claim.

---

## Deliverable

```
## Assume-breach model — <position> — <system> <date>
Position: execution / identity / network vantage / data in reach
Cause: <label only — the model does not depend on it>

### Reachability (each edge labelled CODE FACT / PLAUSIBLE / CONFIRMED)
from → to | mechanism | what it grants | evidence

### Crown-jewel paths
<shortest path to each high-value asset, with its weakest labelled link>

### Choke points (ranked by paths cut / cost)
<edge> — removing it cuts <n> paths — proposed bulkhead

### Containment
revocation command | measured time to effect | detection status | log coverage

### Not modeled
<positions and edges out of scope, so no one reads this as a full map>
```

## Anti-patterns

- Rating severity by the entry bug's cleverness rather than by what it reaches.
- Drawing the pivot graph from the architecture diagram instead of from what is
  actually reachable and actually mounted.
- Presenting fifty edges with no choke point, so nothing gets fixed.
- Mixing walked edges and assumed edges in one unlabeled picture.
- Concluding "contained" from the existence of a segment, without testing that
  the segment blocks the specific path.
- Claiming revocation works without ever having run it, or without measuring
  how long already-issued authority survives.
- Modeling only the outside attacker, never the compromised dependency, CI job,
  or agent — which are the positions most systems actually lose.
- Treating the model as a finding. It is a structured hypothesis set; each edge
  earns its verdict the same way anything else does.
