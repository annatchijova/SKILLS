---
name: attack-surface-triage
description: Enumerate the attack surface of an AUTHORIZED target and rank it into a reproducible, falsifiable candidate queue — reachability × asset value × technique plausibility — before anyone touches a payload. Use whenever the user asks "where should we start", "what's our attack surface", "what should we test first", "map the exposure", "prioritize these findings", "which endpoints matter", or hands over a recon dump, an asset inventory, a subdomain list, an OpenAPI spec, or a pile of scanner output and asks what to do with it. Also trigger when a security engagement is being scoped, when a pentest backlog needs ordering, or when a threat model needs candidate entry points. This skill produces a ranked queue of CANDIDATES with stated falsifiers — it never produces exploits, never asserts a vulnerability exists, and never scores by model intuition. Feeds red-team-auditing (confirm one candidate) and purple-team-exercise (measure detection for one technique).
---

# Attack Surface Triage

Triage is the step everyone skips. Without it, testing follows whatever was
easiest to find, the report reflects the tester's tooling rather than the
target's risk, and the highest-value path is discovered by the attacker instead
of by you.

The product of this skill is a **queue of candidates**, ordered, each one
carrying the evidence that put it there and the observation that would remove
it. A candidate is a hypothesis about where an attacker would go — Firstness, a
possibility noticed. It is not a finding, and this skill never promotes it to
one.

Composes with the library:

- **attack-surface-triage** (this) — surface inventory → ranked candidate queue
- **red-team-auditing** — takes one candidate and earns or refutes a verdict
- **purple-team-exercise** — takes one technique and measures whether it is seen
- **deterministic-core** — the ranking function must be reproducible, not vibes
- **claim-provenance-discipline** — candidates keep their epistemic level in transit
- **tamper-evident-audit-chain** — the scope and inventory as of a point in time

---

## Step 0 — Scope gate

Triage is reconnaissance-adjacent, and reconnaissance against systems you do not
own is not a neutral act. Before enumerating anything:

- **Authorization**: written scope, the owner, and the window.
- **In-scope assets**: an explicit list or pattern. Anything discovered that
  falls outside it is recorded as `OUT OF SCOPE — not enumerated further` and
  reported to the owner, not tested.
- **Passive vs active**: which is permitted. Passive triage (specs, source,
  inventories, DNS records already public) is a different authorization from
  active probing (requests to live hosts).
- **Third-party boundaries**: SaaS, CDNs, and shared infrastructure usually
  belong to someone who did not sign your scope document.

Without authorization, this skill still works — on the artifacts you legitimately
have (your own source, your own spec, your own architecture diagram) — but every
active-probe entry is marked `BLOCKED — pending authorization` and stays that
way. Do not soften this by "just checking whether the host is up".

---

## Part 1 — Enumerate the surface, not the findings

The attack surface is every place where **untrusted input crosses a trust
boundary**. Enumerate boundaries, not endpoints; endpoints are what boundaries
look like from the outside.

Sweep for each of these classes, because tooling is biased and a scanner-shaped
inventory produces a scanner-shaped engagement:

| Class | What to enumerate | Common blind spot |
|---|---|---|
| **Network-reachable** | Hosts, ports, virtual hosts, subdomains, load-balancer rules | Non-HTTP services; forgotten staging hosts |
| **Application entry points** | Routes, parameters, headers, file uploads, websockets, GraphQL fields | Undocumented routes present in code but absent from the spec |
| **Identity and authorization** | Auth flows, token issuance, session handling, role checks, tenant separation | The second tenant; the password-reset path; the service account |
| **Data ingress** | Webhooks, message queues, imports, scheduled jobs consuming external files | Anything asynchronous — it has no user watching it |
| **Supply chain** | Dependencies, build scripts, container base images, CI secrets, deploy keys | The build system is an entry point with production credentials |
| **Human/process** | Support flows that mutate state, admin tooling, break-glass paths | "Support can reset MFA" is an authentication bypass with a ticket queue |
| **Trust in the model era** | Content an LLM or agent reads and acts on, tool authority | See `agent-trust-boundaries` — retrieved content is a data channel |

For each item record: **what it is, how you know it exists** (spec, source file
and line, DNS record, observed response), and **which trust boundary it crosses**.
"How you know" is not optional — an inventory without provenance cannot be
re-verified after the system changes.

**Reachability is a property, not an assumption.** An endpoint in the source is
not necessarily routable; a route behind an internal-only load balancer is a
different candidate from the same route on the edge. Record reachability as one
of: `EXTERNAL`, `AUTHENTICATED`, `INTERNAL-ONLY`, `UNKNOWN`. `UNKNOWN` is an
honest and common answer, and it is not the same as external.

---

## Part 2 — Rank deterministically, or do not rank

A ranked queue is a decision artifact. It will be cited, resourced, and used to
justify what was *not* tested. That makes it exactly the kind of output that must
not come from model intuition (`llm-out-of-the-loop`).

Rank each candidate on three explicit axes, each with a stated basis:

1. **Reachability** — how much does an attacker need before this is touchable?
   (unauthenticated external > authenticated as any user > authenticated as a
   privileged role > internal network > requires prior compromise)
2. **Asset value** — what sits behind it? (regulated data, credentials, money
   movement, code execution, tenant separation, availability, nothing much)
3. **Technique plausibility** — is there a *specific* mechanism you can name for
   why this class of thing fails here? Not "APIs sometimes have IDOR" but "this
   route takes a numeric ID and the authorization decision is not visible in the
   handler".

The combination is the priority. Write the rule down and apply it identically to
every candidate; if two people rank the same inventory, they must produce the
same order. If your ranking needs a tiebreaker, make the tiebreaker explicit
(e.g. lower reachability cost wins) rather than resolving it by feel.

**Plausibility is where the skill lives.** A candidate whose plausibility basis is
a generic vulnerability-class stereotype is noise. A candidate whose basis is a
concrete observation about *this* system — a parameter that reaches a file path,
an authorization check that happens in the caller rather than the handler, a
version string with a known behavior — is signal. State the basis in one sentence.
If you cannot, the candidate ranks low regardless of how attractive it looks.

---

## Part 3 — Every candidate carries a falsifier

The queue is a set of hypotheses, so each entry names the observation that would
drop it:

> *"Candidate: `/api/v2/invoices/{id}` — horizontal authz bypass. Basis: numeric
> ID, no tenant scoping visible in the handler at `invoices.py:112`. Falsifier:
> a middleware or decorator that scopes the query by tenant before the handler
> runs; a database-level row policy."*

Write the falsifier before testing, not after. A falsifier written afterwards is
a rationalization of the result you already got. And when the falsifier is
observed, **record the refutation** — refuted candidates are the most valuable
part of the inventory next quarter, because they document what was checked and
why it was dropped. A queue that only remembers its survivors will re-litigate
the same dead ends forever.

---

## Part 4 — Epistemic hygiene: candidate ≠ finding

Everything this skill emits is at level **CANDIDATE**. Nothing here is
`CONFIRMED`, `EXPLOITABLE`, or assigned a severity, because no attempt was made
to confirm any of it and severity without confirmation is a fabricated number.

The ladder, and who is allowed to move an item up it:

| Level | Meaning | Who promotes |
|---|---|---|
| `SURFACE` | An entry point exists, with provenance | this skill |
| `CANDIDATE` | A named mechanism could plausibly fail here | this skill |
| `CONFIRMED` / `REFUTED` | Tested against the real system | `red-team-auditing` |
| `DETECTED` / `GAP` | Defensive visibility measured | `purple-team-exercise` |

Scanner output arrives pre-labeled with severities and confidence. Those labels
are the scanner's claim about its own heuristics, not evidence about your system:
ingest them as `CANDIDATE` with `origin: <scanner> <version>`, and re-derive the
priority under your own ranking rule. Inheriting a vendor's "Critical" into your
report is `claim-provenance-discipline`'s inherited-confirmation antipattern with
a logo on it.

---

## Part 5 — Coverage, and what you decided not to look at

The dangerous half of a triage document is the half that is missing. Two things
must be explicit:

- **Enumerated but deprioritized** — in the queue, below the line, with the rank
  that put them there. These were considered.
- **Not enumerated** — asset classes you did not sweep (no source access, no
  credentials for the authenticated surface, mobile client out of scope, no
  visibility into the message bus). These were *not* considered, and a reader who
  assumes the inventory is complete will draw a false conclusion from its silence.

Never let "not tested" be inferred from "not listed". State it.

---

## Output contract

ALWAYS emit this. In Claude Code, write to `attack-surface.md` in the engagement
workspace (a results file — not `CLAUDE.md`).

```markdown
# Attack Surface Triage — <target> — <date>
Authorization: <ref>   Mode: <passive | active>   Inventory as of: <commit / scan id>

## Candidate queue (ranked)
| # | Candidate | Entry point | Reachability | Asset behind it | Plausibility basis | Provenance | Falsifier | Level |
|---|-----------|-------------|--------------|-----------------|--------------------|------------|-----------|-------|
| 1 | horizontal authz bypass | GET /api/v2/invoices/{id} | EXTERNAL+AUTH | tenant billing data | numeric id, no tenant scope in handler | invoices.py:112 | tenant-scoped query middleware | CANDIDATE |

## Below the line (enumerated, deprioritized)
<item → rank → the axis that sank it>

## Refuted during triage
<candidate → falsifier observed → evidence>

## Not enumerated (coverage gaps)
<asset class → why → what it would take to cover>

## Ranking rule used
<the exact rule, so the order is reproducible>
```

---

## Discipline checklist (before emitting)

- Is authorization recorded, and is every active probe either in scope or marked `BLOCKED`?
- Does every inventory item carry provenance (how do I know this exists)?
- Is reachability recorded as observed, with `UNKNOWN` where it is unknown?
- Is the ranking rule written down and applied identically to every candidate?
- Does every candidate have a *specific* plausibility basis, not a vulnerability-class stereotype?
- Does every candidate have a falsifier, written before testing?
- Is everything labeled `CANDIDATE` — no severities, no `CONFIRMED`, no scanner labels inherited?
- Are the coverage gaps stated explicitly, so silence is not read as absence of risk?

---

## How to respond when this skill is active

- Ask for scope and authorization before enumerating anything active; produce the passive inventory meanwhile rather than stalling.
- Enumerate trust boundaries first; endpoints are evidence of boundaries, not the unit of analysis.
- Refuse to attach severities. When asked for one, answer with the rank, the axes that produced it, and what confirmation would cost.
- When handed scanner output, strip its labels, keep its observations, and re-rank.
- Hand the top candidate to `red-team-auditing` for confirmation, or to `purple-team-exercise` if the question is "would we see it" rather than "is it real".
- Say plainly what was not enumerated. The reader's biggest risk is a gap they think you covered.
