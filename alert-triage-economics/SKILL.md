---
name: alert-triage-economics
description: Triage a security alert queue by expected loss, not by the severity label the tool stamped — because analyst attention is a scarce, exhaustible resource and a SOC's real failure is not a missed rule but a queue that trains its analysts to dismiss. Use whenever there is a backlog of alerts to prioritize, a "we get 10,000 alerts a day" problem, a decision about which detections to keep, or a claim that a queue is "under control": "which alerts do we work first", "we're drowning in alerts", "alert fatigue", "too many false positives", "should we even keep this rule", "the SOC missed it but the alert did fire", "tune the queue". Sibling of detection-engineering (which builds the rule that fires) and dual-use-behavior-adjudication (which decides what one firing means); this skill governs how a finite team spends attention across many firings. It does not write detection logic or adjudicate a single alert in isolation, and never treats a tool's severity field as a priority.
---

# Alert Triage Economics

A SOC does not fail because a rule was missing. It fails because the alert that
mattered arrived into a queue of ten thousand that didn't, worked by analysts the
queue had already trained to click *dismiss*. The scarce resource is not detection
coverage — it is **analyst attention**, and attention is finite, exhaustible, and
spent whether or not the alert was worth it. Triage is the economics of that spend.

The severity label the tool stamped is not the priority. "Critical" from a scanner
is a statement about the *vulnerability class in the abstract*, made with no knowledge
of whether the affected code is reachable, whether the account has any privilege, or
whether this is the third identical false positive today. Ranking a queue by that
label is ranking by the one number that was computed without looking at your
environment.

Two failure modes, and the second is the one that actually gets people breached:

- **Severity-label theater.** A hundred alerts marked "critical," none rankable
  against each other, so they get worked top-to-bottom or newest-first — which is to
  say, not by importance at all.
- **The queue that trains dismissal.** Every false positive an analyst waves through
  is a rep that teaches "alerts like this are noise." Do it for weeks and you have
  conditioned the exact reflex — fast dismissal — that the real intrusion needs to
  survive its first thirty seconds on screen. Alert fatigue is not a personality flaw
  or a staffing problem; it is a **control failure with a measurable cause**.

Composes with the library:

- **detection-engineering** — sets each rule's false-positive budget and volume estimate; this skill allocates attention across the rules that survive it
- **dual-use-behavior-adjudication** — the per-alert verdict; triage decides which alerts earn that scrutiny at all
- **honest-degradation** — an un-triaged backlog is a WARN on the whole queue, not a silent "we're monitoring"
- **claim-provenance-discipline** — a suppression is a claim ("this shape is benign") that must travel with its justification
- **irreversible-action-gate** — auto-response on a high-confidence alert is an irreversible action; gate it, don't let triage economics push you into auto-eviction on a guess

---

## Step 1 — Re-rank by expected loss, not by label

Priority is not severity; it is **expected loss** — roughly, probability the alert is a
true positive, times the impact if it is, times how reachable the affected asset
actually is. A "medium" on a domain controller reachable from the internet outranks a
"critical" on an isolated lab box that no untrusted input touches.

- **Probability** — this rule's historical true-positive rate, adjusted for anything
  specific to this firing (novel source, first-time-seen, corroboration).
- **Impact** — what the affected identity/asset actually grants (hand it to
  `credential-material-triage` / `assume-breach-modeling`; do not read it off the
  hostname).
- **Reachability** — is the asset exposed to the actor the alert implies, or is the
  scary finding two air-gaps away?

The output of Step 1 is a queue ordered by *what you would actually lose*, which is
almost never the order the tool handed you.

---

## Step 2 — Attention is a budget to spend, not a number to maximize

You will not work every alert, and pretending you will is how the important one waits.
Decide the budget explicitly:

- What is the team's real triage capacity per shift, in alerts-actually-investigated
  (not alerts-glanced-at)?
- Everything below the line that capacity draws is, in practice, *not being worked* —
  so say so. A queue of 10,000 with capacity for 200 is a queue where 9,800 alerts are
  a decorative log, and calling that "monitored" is the silent lie in Step 5.
- Spend the budget top-down on the expected-loss ranking, and treat the cutoff line as
  a real risk decision, recorded, not an accident of volume.

---

## Step 3 — Price the false-positive tax, because it compounds

A false positive does not cost one analyst-minute. It costs that minute *plus* a
fraction of the team's future willingness to look. That second cost compounds across
the whole queue and is the real price of a noisy rule:

- A rule at 5% precision is not "occasionally wrong" — it is teaching your analysts,
  nineteen times out of twenty, that its alerts are noise. The twentieth (true) one
  inherits that training.
- Rank rules for retirement/tuning by *total tax*, not by whether they ever catch
  anything. A rule that fires 500 times to catch one real event may be net-negative
  once you price the dismissal it trains elsewhere.

---

## Step 4 — Tune to cut noise without handing the attacker the gap

The instinct under a flood is to suppress. Suppression is correct and necessary — and
it is also the moment you can quietly hand an intruder a place to live. Every exclusion
is a claim that a shape is *always* benign, and the attacker who learns your
allowlist hides inside it (the tuning trap `detection-engineering` names).

- Suppress on the narrowest stable attribute that removes the noise, not the broadest
  convenient one ("exclude this service account on this host for this action," not
  "exclude all PowerShell").
- Record the exclusion with its justification and an expiry/review, so a silently
  narrowed scope is visible and re-openable (`claim-provenance-discipline`).
- Prefer raising the bar with *corroboration* (fire only when two independent signals
  agree) over deleting the signal — you keep the coverage and lose the noise.

---

## Step 5 — Measure the queue as a control, and be honest about the cutoff

The queue itself is a security control, and an unmeasured control is one you are
merely hoping works. Track, and report without smoothing:

- **Time-to-triage** for the top expected-loss band (the metric that actually maps to
  dwell time), not average across everything.
- **Dismiss rate and its trend** — a rising dismiss rate is the fatigue control
  failing in advance of the miss.
- **The cutoff line** — how much of the ranked queue is going un-worked. "We are at
  capacity and the bottom 90% is unreviewed" is a WARN that belongs in front of
  whoever owns the risk, not a fact buried in a dashboard nobody reads.

A green "0 open criticals" that was achieved by auto-closing the backlog is the report
this skill exists to refuse — it cannot distinguish "triaged and safe" from "gave up
and relabeled." Name which one it is.

---

## The one-line test

If your queue is ordered by the severity field, you have sorted by the one number
computed without looking at your environment. Re-sort by expected loss, draw the line
your real attention budget can reach, and say out loud what falls below it — because
the alert that breaches you will be a quiet one sitting just under a cutoff nobody
admitted was there.
