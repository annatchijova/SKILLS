---
name: control-effectiveness-vs-existence
description: Distinguish a control that exists from a control that works — because compliance attests existence ("MFA is enabled") while security requires effectiveness ("MFA that cannot be phished or bypassed on this path"), and the checkbox is passed by the presence of the control, not by its resistance to the threat it names. Use whenever a control is being claimed, audited, or trusted: "we're compliant", "we have MFA / EDR / a WAF / DLP", "we passed SOC2", "the control is in place", "is this control effective", "does this actually stop the attack", "we have a policy for that", "check the box", "audit the controls". Sibling of daubert-defensible-writing (a control claim gets cross-examined) and falsifiable-testing (an effective control survives an actual attempt to defeat it); it separates presence from performance. It does not run the compliance program or write the policy, and never accepts "the control exists" or "we're compliant" as evidence that the threat is stopped.
---

# Control Effectiveness vs Existence

A control that exists is not a control that works, and the entire compliance apparatus is
built to attest the first while implying the second. "MFA is enabled" passes the audit;
whether that MFA can be phished, SIM-swapped, prompt-bombed, or simply bypassed on a
legacy authentication path is a different question that the checkbox never asked.
Compliance measures *presence*; security measures *performance against a threat*; and
the gap between them is where breached-but-compliant organizations live.

The reframe: **a control is a claim that a specific threat is stopped, and a claim is
tested by trying to defeat it, not by confirming it is switched on.** "We have a WAF" is
existence. "The WAF blocks the injection payloads that reach this endpoint, and here is
the test that shows it" is effectiveness. Only the second is a security statement.

The failure modes:

- **The checkbox that passes on presence.** "Do you have anti-malware? Y/N." Yes. The
  control is EDR in audit-only mode that has never blocked anything, and the box is
  green. Compliance is satisfied; the threat is not addressed.
- **Compliance mistaken for security.** Passing the framework becomes the goal, and
  "we're SOC2 / PCI / ISO certified" is offered as an answer to "are we secure" — two
  different questions, one of which the certification did not test.
- **The control that exists but does not cover the path.** MFA on the web login, none on
  the API or the legacy protocol; the policy on paper, unenforced in practice. The
  control is real and the attacker simply walks around it.

Composes with the library:

- **falsifiable-testing** — an effective control survives an actual attempt to defeat it; a control never tested is a claim never checked
- **daubert-defensible-writing** — "we have this control" is a claim that gets cross-examined; state what you tested, not what you enabled
- **detection-engineering** — a detection control's effectiveness is "it fired on a true positive," not "the rule is deployed" — the same existence/effectiveness split
- **red-team-auditing** — the way you prove effectiveness is by adversarially trying to bypass the control
- **honest-degradation** — a control that exists but is untested is a WARN, not a PASS; name which you have
- **decision-record-discipline** — an accepted control gap is a risk decision to record, not a failure to hide

---

## Step 1 — Restate the control as the threat it claims to stop

Take each control offered as reassurance and rewrite it from "we have X" into "X stops
threat T on path P." The rewrite immediately exposes what the checkbox hid:

- "We have MFA" → "MFA prevents credential-replay account takeover *on every
  authentication path*." Now you can ask: which paths? (Legacy auth, API tokens, service
  accounts, the password-reset flow?)
- "We have EDR" → "EDR blocks and alerts on malicious execution." Now: block mode or
  audit-only? Alerting to a queue anyone reads (`alert-triage-economics`)?
- "We have backups" → "we can recover from ransomware" (which is `recovery-integrity`'s
  whole point — existence of backups vs proven recovery).

If a control cannot be restated as a threat it stops, it is a checkbox with no security
claim behind it, and that is the finding.

---

## Step 2 — Presence, coverage, enforcement, effectiveness — four different questions

For each control, answer all four; compliance usually answers only the first:

1. **Presence** — does the control exist at all? (The checkbox.)
2. **Coverage** — does it cover *every* path the threat can take, or just the obvious
   one? (MFA on web, not on API, is the coverage gap that eats the control.)
3. **Enforcement** — is it actually enforced, or is it a policy document / an audit-only
   mode / a setting that can be self-disabled? A policy nobody enforces is a wish.
4. **Effectiveness** — does it stop the threat when the threat actually tries? This is
   the question only a test answers.

A control can be present, and fail 2, 3, or 4 — and be reported as satisfied at every
compliance checkpoint. Name which of the four you have actually established.

---

## Step 3 — Effectiveness is proven by trying to defeat it

You do not learn whether a control works by confirming it is on; you learn it by
attacking it (`red-team-auditing`, `falsifiable-testing`):

- Phish the MFA. Send the payload past the WAF. Run the technique past the EDR.
  Exfiltrate past the DLP. The control that survives a genuine attempt is effective; the
  one that was never attempted is unmeasured.
- A control with no test that could show it failing is in the same epistemic position as
  a detection rule that has never fired — it *looks* identical to a control that works
  and to a control that does nothing, and you cannot tell which you have until something
  real tests it.
- Prefer the benign-but-real test over the assumption: an authorized attempt that the
  control blocks is evidence; "it should block that" is not.

---

## Step 4 — Compliant is not secure; say which claim you are making

Keep the two claims separate and never let one stand in for the other:

- **Compliance** — "we meet the framework's stated requirements" (existence, mostly).
  Legitimate, contractually necessary, and *not* a statement that attacks fail.
- **Security** — "these threats are stopped, and here is how we know" (effectiveness,
  tested).

The honest report distinguishes them: "we are PCI compliant; separately, our tested
control effectiveness is X, with these known gaps." Offering the certification as the
security answer is the overclaim `daubert-defensible-writing` forbids — it launders
"we checked the box" into "we are safe."

---

## Step 5 — An accepted gap is a recorded decision, not a hidden one

Where a control is present but not effective (or not covering a path), the answer is not
to quietly pass it. It is to name the gap, assess the residual risk, and record the
decision (`decision-record-discipline`): "MFA is not enforced on the legacy protocol;
we accept this risk until Q3 because X; revisit when Y." A known, documented WARN is an
asset — the Daubert posture the whole library favors — and infinitely better than a
green checkbox that cannot tell "the threat is handled" from "the control is switched on
and has never been tested."

---

## The one-line test

If your evidence that a control works is that it is enabled, you have measured its
existence and asserted its effectiveness. Restate it as the threat it claims to stop, ask
whether it covers every path and is actually enforced, and then try to defeat it —
because "we're compliant" and "the attack fails" are different sentences, and only one of
them is tested.
