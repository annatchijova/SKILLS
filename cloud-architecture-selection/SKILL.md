---
name: cloud-architecture-selection
description: Derive cloud infrastructure from a workload's actual constraints and required capabilities — never from "X is popular" or from whichever provider is already open in a tab. Use whenever choosing or re-evaluating a cloud provider, a managed service, or a deployment architecture; whenever comparing AWS/GCP/Alibaba/Azure/other for a workload; or whenever a choice is being justified by brand familiarity, a tutorial's default, or sunk cost instead of a stated requirement. Trigger on "which cloud should we use", "AWS vs GCP vs Alibaba", "what should we run this on", "pick a database service", "lock-in", "multi-cloud", "should we migrate", "we already have credits/infra on X". Selects capabilities before products, distinguishes hard constraints from trade-offs from incumbency cost, and never treats a price, SKU, region, or service limit as a fact with an unstated as-of date. Composes with decision-record-discipline for the artifact this skill produces.
---

# Cloud Architecture Selection

Most cloud choices are not decisions — they are defaults inherited from
whichever tutorial, employer, or credit grant came first, retroactively
justified. This skill does not encode which cloud is better; it encodes
**how to earn an infrastructure decision**, the same way `red-team-auditing`
does not encode which bug is real — it encodes how to earn the verdict.

Composes with the library:

- **decision-record-discipline** — this skill's output *is* a decision
  record: it supplies the Forces (the constraint table below) and Alternatives
  rejected (the trade-off matrix); write the final artifact using that
  skill's six fields, don't reinvent a second template here
- **dependency-provenance** — a managed service is a dependency: know
  exactly what you're running, on whose infrastructure, under what SLA, the
  same way you'd track a package
- **cloud-control-plane-reasoning** — once a provider/architecture is chosen,
  that skill reasons about the blast radius of its identity and control-plane
  model; this skill decides *which* control plane you're accepting
- **secret-lifecycle-discipline** — provider choice determines your secret
  storage/rotation primitives (KMS vs Secret Manager vs KMS on Alibaba);
  don't choose the provider and discover the credential model afterward
- **honest-degradation** — evidence freshness (below) is this skill's
  instance of that skill's core rule: a stale price or limit presented as
  current is a plausible-looking wrong answer
- **irreversible-action-gate** — a provider migration or a managed-service
  cutover is frequently a one-way door; gate it accordingly once decided

---

## The core rule: select capabilities before products

**MUST NOT** start from a product name ("let's use RDS", "put it on Cloud
Run"). **MUST** start from a capability statement derived from the workload:
"managed PostgreSQL with point-in-time recovery, S3-compatible object
storage in region X, containers that scale to zero, max monthly cost $Y."
Only after the capability list is fixed does it get translated to
SKUs — and at that point, plural candidates per capability, across
providers, not one.

Architecture-by-catalog (opening a provider's console and picking whatever
best matches a vague need) inverts this and produces a design that fits the
vendor's product taxonomy instead of the workload's actual requirements —
and it is invisible as a failure mode, because the resulting system usually
still works, just at a cost (lock-in, price, ops burden) nobody chose on
purpose.

## The pipeline

```
workload
   ↓
hard constraints
   ├── region / data residency
   ├── latency
   ├── regulatory requirements
   ├── budget / credits
   ├── expected traffic
   ├── GPU / accelerator needs
   ├── managed-service requirements
   ├── portability requirements
   └── team operational capacity
   ↓
required capabilities
   ↓
candidate architectures
   ↓
provider mapping
   ├── AWS
   ├── GCP
   ├── Alibaba
   └── others if relevant
   ↓
trade-off matrix
   ↓
decision + falsifier + revisit trigger
```

Each stage is a filter or a translation, never a shortcut. Skipping straight
from "workload" to "provider mapping" is the architecture-by-catalog failure
mode restated as a diagram.

### Stage 1 — Hard constraints (MUST, elimination filter)

A hard constraint is binary: a candidate that fails it is eliminated, no
matter how well it scores on everything else. Do not let a trade-off masquerade
as a hard constraint (see Stage 5) or vice versa — treating a preference as
hard prematurely eliminates viable candidates; treating a real hard
constraint as a trade-off lets an eliminated candidate back into the matrix.

| Constraint | What makes it hard, concretely |
|---|---|
| Region / data residency | A named legal or contractual requirement that data stays in a jurisdiction, not a latency preference |
| Latency | A stated SLO (e.g. p99 < 50ms to a named user population), not "should feel fast" |
| Regulatory requirements | A named framework (PCI-DSS, HIPAA, a local data-protection law) with a specific control it imposes |
| Budget / credits | A committed ceiling, and separately, unexpired credits tied to a specific provider (a real constraint, not a preference — see Incumbency below) |
| Expected traffic | An order-of-magnitude estimate with its source (existing metrics, a stated projection) — not a guess presented as a number |
| GPU / accelerator needs | A named workload requiring a specific accelerator class, not "might need ML later" |
| Managed-service requirements | A stated unwillingness/inability to operate a category of infrastructure (e.g. "no in-house DBA," so self-managed Postgres is out) |
| Portability requirements | A stated need to run identically across providers or on-prem (multi-cloud by requirement, not aspiration) |
| Team operational capacity | Actual current skill/tooling in the team, not what the team could learn |

**MUST** state each constraint's source (who set it, what document/SLA/
regulation it comes from) — an unsourced "hard constraint" is a preference
wearing a badge, and the audit below should catch it the same way
`claim-provenance-discipline` catches an unsourced numeric claim in prose.

### Stage 2 — Required capabilities

Translate constraints into capability statements, provider-agnostic:
"object storage, S3-compatible API, versioning, region ∈ {list}",
"managed relational DB, ≥99.9% SLA, automated backups, max $N/month",
"container runtime, scale-to-zero, cold start < Xs." A capability statement
that can only be satisfied by one specific product name has probably
smuggled in a product decision — rewrite it as the underlying need.

### Stage 3 — Candidate architectures

Assemble 2-3 architecturally distinct candidates from the capability list
(e.g. "fully managed serverless," "managed containers + managed DB,"
"self-managed Kubernetes") before naming any provider. This is where
architectural shape gets decided — serverless vs. containers vs. VMs vs.
hybrid — independent of vendor.

### Stage 4 — Provider mapping

Map each surviving candidate architecture to a **sufficient set of
materially plausible providers** — not a fixed brand quorum.

- **MUST** consider more than one provider, unless a Stage-1 hard constraint
  or a documented capability requirement leaves only one viable candidate
  (state which constraint, explicitly — "only one viable candidate" is
  itself a claim that needs a traceable source, same as any Stage-1 entry).
- **MUST NOT** hardcode the candidate set by brand. A provider belongs in
  the mapping because it plausibly satisfies the capability set,
  jurisdiction, incumbency context, or workload shape from Stages 1-3 — not
  because a skill or a habit names it. AWS, GCP, Azure, and Alibaba are
  common enough to serve as default *examples* in this file, not as a
  quorum a decision must clear. A small regional SaaS with an EU-only
  residency constraint has no obligation to evaluate Alibaba; a workload
  needing bare-metal price/performance has no obligation to evaluate a
  hyperscaler at all — Hetzner, OVH, a national/regional provider, Fly.io,
  Cloudflare, Oracle Cloud, or on-prem/colo are all materially plausible
  candidates depending on the capability list, and excluding all of them by
  default is the same catalog bias this skill exists to remove, just
  pointed at a shorter, more "obvious" catalog.
- **MUST** verify current
  service names, regions, SKUs, and limits against the provider's live
  documentation at decision time — see Evidence Freshness below; do not fill
this stage from memory or from a cached mental model of "what AWS offers."

### Stage 5 — Trade-off matrix

Score surviving candidates (those that passed Stage 1) on dimensions that are
*not* eliminating — cost, ergonomics, lock-in, observability tooling
maturity, egress cost, cold-start behavior, provider support quality,
ecosystem maturity for the specific workload. **MUST NOT** let a trade-off
dimension silently function as a hard filter (e.g. discarding a candidate for
"too expensive" without having stated a budget ceiling in Stage 1 — if cost
is actually a hard limit, it belongs there, not disguised as a soft
preference used to eliminate one option and keep another).

### Stage 6 — Decision, falsifier, revisit trigger

Write the decision using `decision-record-discipline`'s six fields:
**Decision** (the architecture + provider chosen), **Forces** (Stage 1's
table, dated), **Alternatives rejected** (each surviving Stage-4 candidate
and the specific Stage-5 dimension that lost it), **Assumption** (what this
decision depends on holding true — e.g. "traffic stays under 10k req/s",
"the region requirement doesn't expand to a second jurisdiction"),
**Reversibility** (see Exit Cost below — this is the substance of that
field, not a separate exercise), **Revisit trigger** (the observable
condition — a traffic threshold, a new regulatory requirement, a pricing
change, a credit expiry date — that should reopen this decision).

---

## Three costs that a naive trade-off matrix omits

These are not part of the standard trade-off dimensions (Stage 5) because
they are asymmetric — they don't apply evenly to every candidate the way
"cost" or "latency" do. Model them explicitly, per candidate.

### Incumbency cost

Existing infrastructure, unexpired credits, IAM/identity setup already built,
CI/CD already wired to a provider, and team knowledge already invested are
real costs to abandon — migrating away from an incumbent is never free, even
when the incumbent scores worse on every Stage-5 dimension. **MUST** state
incumbency explicitly as a line item with an estimated cost (time, risk,
retraining), not fold it silently into "let's just keep using X" — an
unstated incumbency bias is exactly the "AWS is popular" failure this skill
exists to prevent, just with the popularity coming from inside the team
instead of the industry.

**MUST NOT**, symmetrically, let incumbency cost alone justify staying on a
provider that fails a Stage-1 hard constraint — a hard constraint failure
eliminates a candidate regardless of switching cost; incumbency only competes
against soft trade-offs.

### Exit cost / portability

For the leading candidate, name which parts are portable (containerized
workloads, open formats, standard protocols) and which convert a future
migration into a rewrite (a provider-proprietary managed service with no
open-source or standard equivalent — e.g. a proprietary workflow orchestrator
with no portable definition format, a proprietary NoSQL API with no
compatible alternative elsewhere). This is the substantive content of the
decision record's **Reversibility** field, applied per-component rather than
to the architecture as a whole — a system can be a one-way door in one
component and a two-way door in the rest.

### Evidence freshness

**MUST NOT** treat prices, regions, SKUs, service limits, or feature
availability as permanent facts baked into this skill or into institutional
memory — cloud providers change all of these on a timescale of months, and a
stale number presented with confidence is the `honest-degradation` failure
mode transplanted into infrastructure decisions: a plausible-looking wrong
answer. **MUST** consult the provider's current documentation/pricing page at
decision time whenever the decision depends on a specific number, and
**MUST** date-stamp any such figure in the decision record — format:
`<figure> — source: <doc URL/page>, checked <date>, verify before acting on
this later`. Never state a price, limit, or region availability in a decision
record without that stamp, and never carry a figure from this skill's own
text as if it were current — this file must not accumulate hardcoded
provider numbers as it's reused across sessions. A decision record that ages
past its revisit trigger should be treated as carrying stale pricing/limits
until re-verified, not assumed still accurate.

## Failure modes / anti-patterns

- **Catalog-driven architecture**: opening a provider console and picking a
  product that roughly fits, skipping the capability-derivation stage
  entirely — the workload ends up shaped by the vendor's taxonomy.
- **Popularity as justification**: "AWS is popular / has the most Stack
  Overflow answers" presented as a reason, with no named constraint it
  satisfies.
- **Silent incumbency**: staying on the current provider without stating that
  incumbency was the deciding factor — makes the decision look like an
  objective trade-off win when it was actually switching-cost avoidance.
- **Hard constraint smuggled as trade-off, or vice versa**: eliminating a
  candidate on "cost" without ever having stated a budget ceiling; or
  eliminating a candidate as a hard constraint failure when the actual
  requirement was a soft preference.
- **Stale evidence presented as current**: citing a specific price, region
  list, or service limit from memory or an old document without a
  freshness check, in a decision that will be acted on now.
- **Portability claimed without inspection**: asserting "we can always
  migrate later" without having named which specific components are
  actually portable and which are not.
- **One-provider trade-off matrix**: comparing configurations within a
  single provider (e.g. "RDS vs. Aurora") while calling it a cloud
  architecture decision — Stage 4 requires more than one provider unless a
  named Stage-1 constraint or capability requirement leaves only one viable
  candidate (state which, explicitly).
- **Default-catalog bias**: reflexively evaluating AWS/GCP/Azure/Alibaba
  because they're the obvious four, without asking whether a regional,
  specialist, or non-hyperscaler provider is materially more plausible for
  this specific capability set — the same failure this skill exists to
  prevent, relocated one level up from "which product" to "which shortlist
  of providers."

## Verifiable checks

- [ ] Every hard constraint in Stage 1 has a named source (SLA, regulation,
      stated team limitation) — none are unstated preferences.
- [ ] Capability statements (Stage 2) are provider-agnostic — none names a
      specific product as if it were the requirement.
- [ ] At least two architecturally distinct candidates were considered
      (Stage 3) before any provider was named.
- [ ] The provider mapping (Stage 4) considers more than one provider, and
      each candidate provider is there because it plausibly satisfies the
      capability set/jurisdiction/incumbency context, not by default brand
      habit — if only one provider was considered, a named Stage-1
      constraint or capability requirement justifies that.
- [ ] The candidate set was not silently capped to AWS/GCP/Azure/Alibaba
      when a regional, specialist, or non-hyperscaler provider was
      materially plausible for this capability set.
- [ ] Every price, SKU, region, or limit cited is date-stamped and was
      checked against current provider documentation, not recalled from
      memory.
- [ ] Incumbency cost is stated as an explicit, estimated line item wherever
      an existing provider is a candidate — not folded silently into the
      recommendation.
- [ ] Exit cost is stated per-component for the winning candidate — which
      parts are portable, which are a rewrite.
- [ ] The final decision is written as a `decision-record-discipline` entry
      with Forces, Alternatives rejected, Assumption, Reversibility, and a
      concrete Revisit trigger — not just a "Decision" line.
- [ ] No Stage-5 trade-off dimension was used to eliminate a candidate
      outright (that's a Stage-1 job) — check for a hard constraint hiding
      inside a soft dimension.
