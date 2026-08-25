---
name: dual-use-behavior-adjudication
description: Decide whether observed activity is malicious when the tool, command, or API call is itself legitimate — the living-off-the-land problem, where the artifact is identical for the admin and the intruder and the verdict lives entirely in context. Use whenever you must call a signal benign or malicious and the signal alone cannot settle it: PowerShell/WMI/PsExec/certutil/rundll32 execution, a valid credential used from a new location, an `AssumeRole` or `iam:PassRole` that is in-policy, RDP/SSH between hosts that do talk, a scheduled task or service install, bulk reads from a share, an admin doing admin things at 3am. Trigger on "is this malicious or is it just IT", "the tool is legitimate", "living off the land", "LOLBin", "false positive or real", "benign twin", "the account is authorized but", "should we escalate this alert", "adjudicate this detection hit", or a SOC queue where every hit is a maybe. Sibling of detection-engineering — that skill builds the rule that fires; this one adjudicates what a firing means. It does not write detection logic, does not reconstruct the full incident timeline (incident-timeline-reconstruction), and never converts "capable of harm" into "did harm".
---

# Dual-Use Behavior Adjudication

`certutil` downloads a file. That is its job. It is also how an intruder without
`curl` pulls down a payload. The bytes on the wire, the process name, the command
line, the exit code — identical in both cases. **The artifact does not contain the
verdict.** The verdict lives in who ran it, from where, in what sequence, against
what baseline, next to what else. Adjudicate the artifact and you will be wrong in
both directions: you will wave the intruder through because the tool is "legit,"
and you will flag the sysadmin because the tool is "suspicious."

This skill is the epistemic layer above the entire `detecting-*` / `hunting-*`
family. Those procedures tell you a signal *fired*. This one tells you what the
firing is *worth* — and refuses to let a legitimate tool name settle the question
in either direction.

Two failure modes, symmetric and both fatal:

- **False MALICE.** You escalate the administrator. You burn a day of a real
  person's time, you erode every future alert's credibility ("the SOC cries wolf"),
  and you train the org to click *dismiss* — which is how the real one gets missed.
- **False PASS.** You wave it through because "PsExec is a normal admin tool." The
  attack you were built to catch walks past you wearing the exact uniform you told
  yourself was safe. The silent version of this is worse: a rule tuned to exclude
  "known-good" behavior that the attacker now hides inside.

The discipline that kills both is the same one from `abductive-engineering §1.3`:
**you do not get to pattern-match to a verdict. You build the innocent explanation,
in its strongest form, and you try to confirm it against evidence — not refute it.**
Malice is what survives a genuine attempt to explain the activity as legitimate.

Composes with the library:

- **abductive-engineering** — Firstness/Secondness/Thirdness and the refutation step are the engine here
- **detection-engineering** — supplies the firing; this skill adjudicates it; a verdict feeds back as a tuning input
- **assume-breach-modeling** — if malicious, what position does this identity already hold and reach next
- **incident-timeline-reconstruction** — a MALICE verdict hands off here; adjudication is per-signal, timeline is the whole
- **claim-provenance-discipline** — the verdict travels with its evidence and confidence, never as a bare label
- **daubert-defensible-writing** — "confirmed malicious" is a claim that gets cross-examined; earn it
- **honest-degradation** — ABSTAIN is a verdict, not a failure to produce one

---

## Step 0 — Name the baseline before you call anything anomalous

An anomaly does not exist in the artifact. It exists only as a *deviation from a
norm* (Secondness). If you cannot state the norm, you are not adjudicating — you are
reacting to a tool name.

Before verdict, write the baseline in one sentence, and mark whether you actually
have it or are assuming it:

- **Actor norm.** Does *this* identity run *this* action? "svc-backup runs
  robocopy nightly" vs "svc-backup has never spawned a shell." A backup service
  account is expected to touch every share; a helpdesk account reading Finance is not.
- **Host norm.** Do these two hosts talk? Does this workstation normally run
  `wmic /node:`? Domain controllers initiate very little outbound; a DC beaconing is
  a different sentence than a jump box beaconing.
- **Temporal norm.** Is 03:00 abnormal *for this actor*? For an on-call SRE it is
  Tuesday. For a payroll clerk it is a flag.

If the baseline is **assumed, not measured**, that is a WARN cap on your whole
verdict — say so, and see Step 5. "No baseline available" is itself a finding: it
means the environment cannot currently distinguish this attacker from its own admins.

---

## Step 1 — Separate capability from intent (do not let the tool testify)

The single most common adjudication error is treating *what the tool can do* as
evidence of *what the actor meant*. `certutil` **can** exfiltrate; `mimikatz`-like
capability **can** dump credentials; `AssumeRole` **can** cross an account boundary.
None of that is intent. "The model/tool could generate X" is not "the attacker
executed X" — the same discipline you apply to threat models applies here.

Split every observation into two columns and keep them apart:

- **Capability** — what this action makes *possible*. Grep-able, always present for a
  dual-use tool, and therefore **near-zero evidentiary weight on its own.**
- **Intent markers** — choices the actor made that a legitimate user would not, or
  would not need to: obfuscated/encoded command lines (`-enc`, base64 blobs), output
  redirected to a staging path, timestamps stomped, logging disabled *first*,
  naming that mimics system components (`svch0st`), deletion of the tool after use.

A verdict built only on the capability column is a false MALICE waiting to happen.
Intent markers are what move a signal up the scale.

---

## Step 2 — Provenance beats sink (rank by who/where, not by what)

Rank the signal by its **provenance and authority**, not by how scary the sink
looks. The same `net user /add` is trivial from an interactive admin session on a
management host and alarming from a web server's service account whose parent process
is `w3wp.exe`. Trace, in order:

1. **Identity** — which principal, and is it acting inside its granted authority?
   (An authorized account doing something *outside its normal function* is the whole
   LOLBin problem; "authorized" is not "expected.")
2. **Provenance chain** — parent process / invoking service / calling role. A shell
   whose grandparent is a document reader or a web worker is a different sentence
   than one launched from a logon session.
3. **Path of entry** — interactive console, remote management, or a process that
   should never spawn children spawning one.

A high-authority action from an expected principal down an expected path is the
boring explanation surviving. A low-authority principal reaching a high-authority
action down an unexpected path is intent leaking through provenance.

---

## Step 3 — Read the neighborhood, not the single event

One dual-use action is almost never adjudicable alone — that is what makes it
dual-use. Adjudication happens at the level of the **sequence**: does this signal sit
in a neighborhood that only makes sense as an attack?

`certutil` downloads a file → the file lands in `C:\Users\Public` → a scheduled task
is created pointing at it → the task runs as SYSTEM → outbound to a fresh domain. No
single step is malicious. The *chain* has no benign author. Conversely, `certutil`
downloading a certificate revocation list, once, with no successor events, has a
benign author and you should say so out loud.

- **Corroboration.** Count *independent* signals, not restatements of one. Three
  fields of the same log line agreeing is one signal. EDR + network + identity
  logs agreeing is three. A verdict wants independent corroboration; a single
  high-severity line usually does not carry a MALICE by itself.
- **Kill-chain adjacency.** Is this signal flanked by recon before and staging
  after? Isolation (no neighbors) is evidence *for* the benign hypothesis, not a
  gap to be filled with imagination.
- **Guard against narrative pressure.** Evidence that fits your first guess too
  perfectly (Eco's razor) is a reason to look harder, not to relax. Do not assemble a
  kill chain by demoting every innocent step into a "stage."

---

## Step 4 — Try to confirm the benign explanation, then grade what survives

Build the strongest innocent story and test *it* against the full evidence:

- Is there a change ticket, deploy window, or automation schedule that predicts this
  exact action at this exact time? (Corroborating *evidence*, not a hunch.)
- Is this actor's baseline (Step 0) consistent with it?
- Does every anomaly have a benign author, or is there a residue the innocent story
  cannot explain?

If the benign story accounts for **every** anomaly without contradiction — stop. You
were about to escalate legitimate work; that is a real, valuable outcome ("looked,
and this is the nightly backup — svc-backup, expected path, matches 90-day baseline,
change window open"). If a residue survives — the encoded command line, the disabled
logging, the account acting outside its function — that residue is the finding.

Grade what survives on a scale that admits abstention. Do not collapse to a binary:

- **NOISE / benign** — benign author confirmed by evidence; expected actor, path,
  baseline. Close it *with the reason*, so the closure is auditable and re-openable.
- **SUSPICION** — deviation from baseline with no confirmed benign author, but no
  intent markers and no corroborating chain. Watch / enrich; do **not** escalate to a
  human as malicious.
- **INTENT / MALICE** — intent markers present (Step 1) and/or a chain with no benign
  author (Step 3), corroborated by independent signals (Step 4). This is the only
  verdict that costs an analyst their afternoon; make it earn that.
- **ABSTAIN** — the evidence does not decide, or the baseline is absent (Step 0). A
  documented "cannot adjudicate: no host baseline, single uncorroborated signal" is
  worth more than a coin-flip PASS or a coin-flip escalation. Abstention names the
  missing evidence, which is the next collection task.

Capability alone never reaches INTENT. Missing baseline caps you at SUSPICION or
ABSTAIN, never NOISE — you cannot certify benign against a norm you never measured.

---

## Step 5 — Emit the verdict so it survives cross-examination

The output is not a label. It is a label *plus the context that produced it*, because
the next reader (and the attacker's lawyer, and the auditor tuning the rule) will ask
"benign against what baseline? malicious on what corroboration?"

Every adjudication carries, at minimum:

- **Verdict + confidence**, on the graded scale, with the driver in one line
  ("MALICE — encoded PowerShell from w3wp.exe child, corroborated by EDR+proxy,
  no change window").
- **The baseline it was judged against**, and whether that baseline was measured or
  assumed (the WARN cap from Step 0).
- **Capability vs intent, kept separate** — so a later reviewer can see you did not
  convict the tool for existing.
- **The benign hypothesis you tested and what it failed to explain** — the residue is
  the evidence; if there was no residue, the verdict is NOISE and you say why.
- **What would flip it.** A MALICE that no evidence could downgrade is a prejudice; a
  NOISE that no evidence could upgrade is negligence. Name the observation that would
  change your mind — that line is what makes the verdict falsifiable.

A verdict feeds two places: to a human (via `daubert-defensible-writing` if it
escalates, or a closed ticket with its reason if it does not), and back to
`detection-engineering` as a tuning input. Note the trap on that return path: an
exclusion you add to silence *this* benign hit is a scope you just handed the
attacker to hide inside. Every tuning exclusion is a claim ("this shape is always
benign") that must travel with its justification (`claim-provenance-discipline`) — a
silently narrowed rule is how the next intruder lives off your own allowlist.

---

## The one-line test

If swapping the *tool name* for a synonym would change your verdict while every piece
of context stayed identical, you adjudicated the artifact, not the behavior — start
over at Step 0. The verdict must come from provenance, baseline, sequence, and intent
markers. The tool is never the witness.
