---
name: purple-team-exercise
description: Run an AUTHORIZED, collaborative purple-team exercise — turn each attack technique into a detection hypothesis, detonate it minimally and marked, and measure whether the blue side prevented it, detected it, or missed it entirely. Use this whenever the user wants to validate detection coverage, test whether a control or alert actually fires, close the loop between offensive testing and defensive telemetry, map findings to MITRE ATT&CK, or plan/run/write up a purple exercise. Trigger even when the user only says "did our SIEM catch this", "test our detections", "validate this control", "what's our coverage for technique X", "run a purple exercise", or hands over red-team findings and asks "would we have seen it". This skill measures and specifies detection; it does NOT author vendor rule syntax (that's the detection-engineering sibling) and does NOT generate turnkey exploits (detonations are minimal, marked, non-destructive).
---

# Purple Team Exercise

Purple is not "red plus blue in the report". It is one collaborative loop whose
product is **measured, improved detection coverage**. Red says where to attack;
this skill asks, for every technique: *what should the defenders see, did they see
it, and how do we make the next miss impossible?* The deliverable is the detection
**gap**, not the bug.

Composes with the library:

- **attack-surface-triage** — supplies candidate techniques to exercise
- **red-team-auditing** — validates a specific exploit hypothesis if one is contested
- **purple-team-exercise** (this) — technique → detection expectation → observed outcome → gap → detection requirement → retest
- **detection-engineering** (sibling, may not exist yet) — turns a detection *requirement* into vendor rule syntax (Sigma/KQL/SPL)
- **tamper-evident-audit-chain** — the exercise ledger (what was detonated, when, with which marker)
- **daubert-defensible-writing** + **claim-provenance-discipline** — the write-up

Run the loop; hand rule authoring and confirmation to those. Don't reimplement them.

## What this skill will and won't do

WILL: plan atomic detection tests, tag them to ATT&CK, detonate minimally with a
correlation marker, compare expected vs observed telemetry, classify the outcome,
write a precise detection *requirement* for each gap, and drive retest.

WON'T: generate working exploits or turnkey payloads; test destructively or
out-of-scope; author production rule syntax; or grade the blue team. A detonation
is the *smallest marked action that produces the telemetry under test* — not a
weaponized attack. If a real confirmation needs a destructive action, it goes to
`red-team-auditing` under explicit authorization, not here.

## Step 0 — Scope + coordination gate

Purple is collaborative and authorized by definition. Before anything:

- **Authorization**: the exercise is sanctioned and both sides know the window.
- **In-scope assets**: only these are exercised; out-of-scope drops from the plan.
- **Rules of engagement**: destructive prohibitions, rate limits, production vs
  staging, data-touching limits.
- **Coordination mode**: announced (blue knows each test as it fires) or
  unannounced/"detection-only" (blue sees only their telemetry, not the schedule).
  Record which — it changes how you read a miss.
- **Deconfliction**: a channel to confirm "that alert was us", so a real intrusion
  during the window isn't dismissed as the exercise.

If any of this is unset, produce the test plan but mark every detonation
`BLOCKED — pending coordination`.

## Step 1 — Build the test plan (atomic tests)

One test = one technique, ATT&CK-tagged, small enough to attribute a detection
outcome to it cleanly. Bundling techniques makes a miss un-diagnosable — you won't
know which step was invisible. Consume `attack-surface-triage` output as the
candidate source; prioritize by *defensive value*: techniques on the likely
attack path that you have no confirmed detection for rank highest.

For each test record: technique, ATT&CK ID, target asset, and the **expected
telemetry** — the data sources that *should* light up if this fires (e.g. an SSRF
should show outbound connections from the app tier to internal IPs; an authz-bypass
export should show anomalous bulk read volume). Expected telemetry is a
*hypothesis*, not a fact — label it so.

## Step 2 — Detonation discipline

Every detonation is **minimal, in-scope, and marked**:

- Minimal: the smallest action that generates the telemetry under test. You're
  testing whether the smoke alarm works, not burning the building.
- Marked: carry a known correlation canary — a unique user-agent, a benign
  timestamped filename, a distinctive source — so blue can find *exactly* this
  event in their logs and you can prove attribution.
- Logged: append each detonation to the exercise ledger (technique, marker,
  timestamp, operator) via `tamper-evident-audit-chain`. A purple exercise that
  can't prove what it fired and when can't defend its own findings.

## Step 3 — Measure detection (fact vs inference)

For each detonated test, classify the outcome — and keep the discipline tight,
because the three states have *different fixes*:

- **PREVENTED** — a preventive control blocked it (WAF, authz, egress filter). Note
  which. (Blocked ≠ detected: a silent block is still a detection gap.)
- **DETECTED** — an alert fired AND blue can show it, correlated to your marker.
  "Detected" is a fact only when you see the alert artifact. Blue *saying* it would
  alert is not detection.
- **LOGGED, NOT ALERTED** — the telemetry exists in the logs but no alert fired.
  This is the highest-value finding: the data is there, the detection logic isn't.
- **INVISIBLE** — no telemetry at all. This is a *visibility* gap (missing log
  source), a different and usually costlier fix than a detection-logic gap.

Never collapse "logged-not-alerted" and "invisible" into "missed" — you'd prescribe
the wrong remediation.

## Step 4 — Gap analysis + detection requirement

For each gap, write a **detection requirement**: a precise, testable spec of what
must be true to catch this next time — the data source, the observable condition,
and the threshold/logic in plain terms. NOT vendor rule syntax; that's the
`detection-engineering` sibling's job, fed by this requirement. Writing the
requirement here and the rule there keeps the "what we need to catch" separable and
auditable from the "how this vendor expresses it".

Example requirement: *"Alert when the application service account opens an outbound
TCP connection to an RFC1918 address it has never contacted in the prior 30 days
(source: egress netflow / EDR network events)."*

## Step 5 — Remediate and retest (close the loop)

An open gap isn't a finding, it's a to-do. Track each: gap → requirement → rule
built (sibling) → **retest with the same marked detonation** → outcome now
DETECTED. The loop isn't closed until the retest passes. Report both states.

## Output contract

ALWAYS emit this. If running in Claude Code, append to `purple-findings.md` in the
engagement workspace (results file — NOT `CLAUDE.md`).

```markdown
# Purple Team Exercise — <target> — <window>
Coordination: <announced | detection-only>   Scope: <in-scope | pending>

## Coverage matrix
| # | Technique | ATT&CK ID | Expected telemetry | Detonation marker | Outcome | Gap type | Detection requirement | Retest |
|---|-----------|-----------|--------------------|-------------------|---------|----------|-----------------------|--------|
| 1 | SSRF to internal metadata | T1090 | egress netflow, app logs | UA=purple-<id> | LOGGED-NOT-ALERTED | detection-logic | <spec> | pending |

## ATT&CK coverage rollup
<per-tactic: exercised / prevented / detected / gap — a coverage view, not a score>

## Open gaps (prioritized by defensive value)
<gap → requirement → owner → retest status>

## Exercise ledger
<reference to the tamper-evident chain of detonations>
```

## Collaboration discipline

Purple measures the *system*, not the blue team. Report coverage and
mean-time-to-detect as **observations**, never as a grade — the moment it becomes a
scorecard, blue stops surfacing their own blind spots and the exercise loses its
point. Frame every gap as a shared to-do with a concrete requirement, not a failure.

## Discipline checklist (before emitting)

- Is every out-of-scope asset out of the plan?
- Is "expected telemetry" labeled as hypothesis, and "detected" backed by a real alert artifact correlated to a marker?
- Did I keep "logged-not-alerted" and "invisible" distinct?
- Does every detonation have a correlation marker and a ledger entry?
- Is each gap paired with a testable detection *requirement* (not rule syntax, not a payload)?
- Are coverage/MTTD framed as observations, not a blue-team grade?

## Example

**Input:** red triage flagged `dev-api.target.com/api/v2/users/export` as a
candidate authz-bypass (bulk user export).

**Purple test (good):** Technique = unauth bulk data access, ATT&CK T1213.
Expected telemetry (hypothesis): anomalous read volume + access from an
unauthenticated session in app logs. Detonation: single authenticated-vs-
unauthenticated request pair, marked `UA=purple-7f3a`, minimal rows, logged to
ledger. Observed: request appears in access logs, no alert fired → **LOGGED,
NOT ALERTED**. Requirement: *"Alert on >N distinct user records returned to a
session lacking an admin claim within 60s (source: app access log + authz
decision log)."* Handed to detection-engineering; retest pending.

**Not this (bad):** "Confirmed IDOR, dumped all users, blue team failed to
detect, Critical." Claims an exfiltration action, a verdict, and a blame metric —
none of which is what a purple exercise is for.
