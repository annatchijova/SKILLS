---
name: detection-engineering
description: Turn a detection requirement into a deployed, tested, versioned rule — with a benign twin that must NOT fire, an explicit false-positive budget, a volume estimate before deploy, and a tuning history that records every silently narrowed scope. Use whenever the user writes or reviews an alert, a Sigma/KQL/SPL/EQL/YARA rule, a SIEM correlation search, a WAF or EDR policy, an anomaly threshold, or a monitor that pages someone; whenever they say "write a rule for this", "alert when X", "we're getting too many alerts", "tune this detection", "why didn't this fire", "detection as code", or "add a monitor"; and whenever a purple-team gap needs closing. Sibling of purple-team-exercise — that skill specifies WHAT must be caught, this one builds and proves the thing that catches it. It does not run exercises, does not triage incidents, and never claims coverage from a rule that has not fired on a real true positive.
---

# Detection Engineering

A rule that has been written is not a detection. A rule that has been deployed is
not a detection either. A detection is a rule that has **fired on a known true
positive, stayed silent on its benign twin, and produced a volume someone will
actually triage**. Everything before that is a hypothesis with YAML around it.

This skill exists because the failure mode is invisible by construction: a rule
that never fires looks exactly like a rule protecting you from something that
never happened. The discipline is to make the silent failure loud *before* it
matters.

Composes with the library:

- **purple-team-exercise** — supplies the detection *requirement*; retests the rule
- **attack-surface-triage** — supplies the techniques worth detecting
- **falsifiable-testing** — a rule with no failing case is a test that cannot fail
- **claim-provenance-discipline** — every tuning exclusion is a scope narrowing that must travel
- **versioned-schema-evolution** — log formats change under your rules; version accordingly
- **daubert-defensible-writing** — "we have coverage for T1078" is a claim that needs evidence

---

## Step 0 — The input is a requirement, not a vibe

Start from a written detection requirement: **data source + observable condition +
threshold/logic, in plain terms.** If one was handed to you (usually by
`purple-team-exercise`), use it verbatim. If not, write one first and get it
agreed *before* touching rule syntax — otherwise you will discover halfway
through that the field you need was never collected, and quietly rewrite the
requirement to match the data you happen to have. That is how coverage becomes
fiction.

> *Requirement: "Alert when a service account authenticates interactively from a
> host it has not authenticated from in the prior 30 days (source: identity
> provider sign-in logs, field `authenticationMethod`, `deviceId`)."*

**Verify the data before writing the logic.** Three checks, in this order:

1. **Presence** — is the field actually populated in your environment, on the
   platforms you care about? (Not "the vendor documents it". Query it.)
2. **Fidelity** — does it mean what the name suggests, with what precision, and
   is it attacker-controllable? A field the attacker sets is not evidence.
3. **Latency and retention** — how long until the event is queryable, and how far
   back can you hunt? A 45-minute ingest lag makes a "real-time" rule a report.

If the data is not there, stop: the answer is a **visibility gap** and the
deliverable is a logging change, not a rule. Writing a rule against a field that
is empty in production is the single most common way a coverage matrix fills up
with green that means nothing.

---

## Part 1 — Climb the brittleness ladder as far as the data allows

Detections differ enormously in how cheap they are for an attacker to evade.
Know which rung you are on, and say so in the rule metadata:

| Rung | Detects | Attacker cost to evade |
|---|---|---|
| **Value** | A hash, an IP, a domain, an exact string | Seconds — change one byte |
| **Artifact** | A tool's characteristic filename, header, mutex, argument | Minutes — recompile, rename |
| **Behavior** | The technique itself: the sequence, the relationship, the anomaly | Real — requires changing method |

Value-level rules are not worthless — they are cheap, precise, and fine for known
campaigns — but a coverage matrix built entirely from them describes yesterday.
Aim for the highest rung the available telemetry supports, and when you ship a
value-level rule, record what a behavior-level version would require. That note
is the backlog item that eventually earns real coverage.

**Prefer relationships over thresholds.** "More than 50 failed logins" is a
number an attacker can stay under. "A successful login from a principal whose
prior 30 days contain no successful login from that ASN" describes a shape.
Shapes survive; thresholds get walked around.

---

## Part 2 — The benign twin (non-negotiable)

Every rule ships with **two** test cases:

- **The true positive** — a sample event or a marked detonation that the rule
  MUST match. Ideally the exact marked detonation from the purple exercise, so
  the retest closes the same loop that opened it.
- **The benign twin** — the closest legitimate activity you can construct that
  the rule MUST NOT match. The backup job that also reads a thousand records.
  The admin who also runs `net user`. The scanner that also touches every port.

Without a benign twin you cannot distinguish "specific" from "lucky". A rule
tested only against the attack always looks perfect, because you never showed it
anything it should ignore. The twin is what makes the rule falsifiable, and it is
what turns tuning from guesswork into a regression test: when a false positive
arrives in production, it becomes a new twin, permanently.

Keep both cases in version control next to the rule. A rule whose test cases live
in someone's terminal history is untested from the moment they leave.

---

## Part 3 — The false-positive budget is a design constraint

Decide the volume the rule is allowed to produce **before** deploying it, and
derive it from the triage capacity that actually exists — analyst-hours per day,
not aspiration. Then estimate the real volume by running the logic in **hunt
mode** over historical data (30–90 days) and counting.

If the estimate exceeds the budget, you have four honest options — in order of
preference:

1. **Raise fidelity**: add a condition that excludes the benign population by
   *mechanism* (the backup service account has a distinguishing attribute), not
   by coincidence.
2. **Change the response**: not everything is a page. Route to a hunt queue, a
   daily digest, or an enrichment that raises the score of a different alert.
3. **Narrow the scope**: apply the rule only to the crown-jewel subset — and
   record loudly that the rest is now uncovered.
4. **Do not deploy**: an alert nobody triages is a disabled alert that shows up
   green on the coverage matrix. This is the worst outcome, so name it as one.

**The anti-pattern with a name: tuning to zero.** Exclusions accumulate until the
rule fires on nothing, and everyone reports full coverage. Every exclusion is a
narrowing of the claim "we detect X" and must be recorded as such
(`claim-provenance-discipline`): what was excluded, why, who approved it, when it
should be revisited, and what the attacker gains if they operate inside the
exclusion. That last field is the one that stops bad exclusions — "the attacker
gains: run this from any host in the `svc-*` naming convention" reads very
differently from "excluded noisy service accounts".

---

## Part 4 — Detection as code

Rules are production code that runs against adversarial input. Treat them that way:

- **Version control**, reviewed by someone other than the author.
- **Stable ID + version** on every rule; the ID is what the ticket, the exercise
  ledger, and the coverage matrix all point at.
- **CI**: the true positive and the benign twin run as tests on every change to
  the rule *and* on a schedule, because the log schema can change underneath a
  rule that nobody edited. A silent field rename is a silent coverage loss.
- **Metadata contract** on every rule — see below.
- **Deprecation, not deletion**: a rule that is retired records why. A rule that
  vanishes teaches nobody.

```yaml
id: DET-0142
version: 3
requirement: "service account interactive auth from unseen host (purple PT-2026-03 gap #4)"
hypothesis: "credential theft of a service account manifests as interactive auth from a new device"
data_source: identity provider sign-in logs
fields_required: [principal, authenticationMethod, deviceId, asn]
rung: behavior
attack: T1078.004
validation:
  true_positive: tests/det-0142/tp_marked_detonation.json   # purple marker UA=purple-7f3a
  benign_twin:  tests/det-0142/benign_backup_service.json
volume_estimate: "6/week over 90d historical hunt (budget: 10/week)"
response: hunt queue, not page
exclusions:
  - scope: "svc-backup-01"
    reason: "documented nightly interactive session, ticket OPS-882"
    attacker_gain: "an attacker operating as svc-backup-01 from that host is invisible to this rule"
    revisit: 2026-09-01
owner: detection-eng
```

---

## Part 5 — Proving the rule works, and saying so honestly

A rule moves through states, and only one of them is "coverage":

| State | Meaning |
|---|---|
| `DRAFT` | Logic written, data verified |
| `VALIDATED` | Fires on the true positive, silent on the benign twin, in test |
| `DEPLOYED` | Live in production, volume within budget |
| `PROVEN` | Has fired on a real or marked true positive **in production**, and someone saw the alert |
| `DEGRADED` | Data source changed, volume collapsed, or exclusions now cover the technique |

The claim "we have coverage for T1078" is only supportable at `PROVEN`. Anything
below that is "a rule exists", which is a different sentence with a different
meaning to the person deciding where to spend next quarter.

**Watch for the silent death.** A rule that fired weekly and now fires never has
either fixed the world or broken itself, and the second is far more likely. Alert
on the *absence* of expected volume for rules with a known baseline — a detection
that monitors its own heartbeat is the only kind that fails loudly.

---

## Output contract

```markdown
# Detection — <id> v<n> — <technique>
Requirement: <verbatim, and where it came from>
Data verified: presence / fidelity / latency  → <yes | gap: ...>
Rung: value | artifact | behavior   (behavior-level would require: <...>)

## Logic
<the rule, in the target syntax, with the field semantics stated>

## Validation
True positive: <case> → matched
Benign twin:  <case> → not matched
Historical volume: <n over m days>   Budget: <n>   Response: <page | queue | digest>

## Exclusions
<scope → reason → what the attacker gains → revisit date → approver>

## State
DRAFT | VALIDATED | DEPLOYED | PROVEN | DEGRADED  (+ what would move it up)

## Known evasions
<how someone who reads this rule walks around it — written by the author, on purpose>
```

That last section is the honest one. You know your own rule's blind spots better
than anyone; writing them down converts private knowledge into a backlog instead
of leaving it as a surprise for the incident.

---

## Discipline checklist (before shipping a rule)

- Did I verify the field is populated, faithful, timely, and not attacker-controlled — by querying, not by reading docs?
- Is the requirement written and unchanged, or did I quietly reshape it to fit available data?
- Which rung am I on, and did I record what the next rung up would need?
- Does the rule have a true positive AND a benign twin, both in version control, both in CI?
- Did I estimate volume against historical data before deploying, against a stated budget?
- Is every exclusion recorded with what the attacker gains and a revisit date?
- Is the state honest — am I about to call `DEPLOYED` "coverage"?
- Did I write down how I would evade my own rule?

---

## How to respond when this skill is active

- Ask for (or write) the requirement before writing syntax; refuse to reshape the requirement silently around missing data.
- Query the data source before trusting a field exists. "The schema documents it" is not presence.
- Always produce the benign twin. If the user only supplies attack samples, construct the twin and say why it matters.
- Give a volume estimate with every rule, and name the triage cost. An untriaged alert is a disabled alert.
- Record exclusions as narrowed claims, with the attacker's gain spelled out — never as "tuned out noise".
- Say `a rule exists` when a rule exists. Reserve `we detect this` for rules that have actually fired on a true positive in production.
- Hand the rule back to `purple-team-exercise` for the marked retest; the gap is not closed until that retest passes.
