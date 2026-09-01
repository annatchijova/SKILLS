---
name: social-engineering-plausibility
description: Reason about attacks that exploit human trust rather than a software flaw — where the target made a locally reasonable decision on deliberately crafted context, and no patch fixes it because the "vulnerability" is a person doing their job. Use whenever the vector is a human: "was this phishing", "how did they fall for it", "analyze this pretext", "why did the user click / wire the money / reset the password", "is this email a scam", "vishing / smishing / BEC", "social engineering assessment", "our people keep failing phishing tests", "just train the users". Sibling of agent-trust-boundaries (the human is an untrusted-content channel that must not carry instruction authority) and dual-use-behavior-adjudication (the requested action is often legitimate — the deception is in the context); reasons about pretext credibility and control placement. It does not run phishing campaigns against real people without authorization, and never lets "the user was stupid" stand in for a missing control.
---

# Social Engineering Plausibility

A phishing victim is not a bug to be patched and usually not a fool to be blamed. They
received a message that was **locally plausible** — the invoice looked like the vendor's
invoices, the CEO's urgency matched how the CEO actually writes, the IT call came right
after a real outage — and they made the decision that context made reasonable. The
exploit is not in their judgment; it is in the *context the attacker manufactured* and
in the fact that a legitimate action (reset a password, pay an invoice, run an
attachment) was requested through a channel that carried no real authority to request it.

Two symmetric failure modes this skill exists to prevent:

- **Blame the human, patch nothing.** "The user clicked; we sent them to training." This
  treats a systemic control gap as a personal failing, guarantees the next person
  clicks, and — because the action was often legitimate — punishes people for doing
  their jobs. It is the security equivalent of blaming the victim.
- **Assume a technical control solved it.** "We have a spam filter / DMARC / MFA, so
  we're covered." Each stops a subset of a fundamentally human exploit; a well-built
  pretext routes around all of them (a phone call, a look-alike domain the filter
  passed, an MFA-fatigue push the user approved).

The through-line with the library: **a human is an untrusted-content channel.** Content
that reaches a person can *persuade*, but the authority to take a consequential action
must come from the channel and the policy, never from the persuasiveness of the message.

Composes with the library:

- **agent-trust-boundaries** — the exact same principle as prompt injection: retrieved content (an email, a call) is data, not instruction authority; a person, like a model, must not act on instructions just because they arrived convincingly
- **dual-use-behavior-adjudication** — the requested action ("reset my password," "pay this") is usually legitimate; the maliciousness is in the manufactured context, so judge the context, not the act
- **red-team-auditing** — "our awareness training works" is a claim; a click-rate with no measured business-impact is not evidence it does
- **daubert-defensible-writing** — a post-incident writeup that says "user error" launders a control gap into a person's fault; write what actually failed
- **irreversible-action-gate** — the consequential actions social engineering targets (wire transfers, credential resets) are exactly the ones that need an out-of-band gate

---

## Step 1 — Reconstruct the pretext as the target experienced it

Firstness, from the victim's chair, not the analyst's hindsight. Describe the message
and the moment without "obviously fake" contaminating the description:

- **The claimed identity and channel** — who it appeared to be (a vendor, the CEO, IT,
  a bank) and how it arrived (email, SMS, call, a chat in a tool they trust).
- **The context that made it fit** — did it arrive at a plausible time (right after a
  real deploy, during quarter-end, following a genuine outage)? Did it reference real
  names, real projects, real prior threads (reply-chain hijack)?
- **The action requested** — and whether that action is, in isolation, a normal part of
  the target's job.

If, described this way, the pretext is coherent and well-timed, then "the user should
have known" is hindsight. The plausibility *is* the attack.

---

## Step 2 — Name the levers: why the decision felt right

Social engineering works by supplying context that makes the wrong action feel correct.
Identify which levers were pulled, because they map to different defenses:

- **Authority** — an instruction from someone the target does not refuse (executive,
  regulator, law enforcement, IT with admin rights).
- **Urgency / scarcity** — a deadline that prevents the pause in which the target would
  have verified ("the wire must go out in the next 20 minutes").
- **Context match / familiarity** — look-alike domains, hijacked threads, correct
  logos, knowledge of internal jargon — lowering the "this is external" signal.
- **Reciprocity / helpfulness** — exploiting the target's job of being helpful (support
  desks, finance, HR are targeted precisely because saying yes is their function).
- **Fear / consequence** — "your account will be closed," "you'll be reported."

These are not weaknesses of the individual; they are universal, and a good pretext
stacks several. The defense is not "be less human" — it is Step 4.

---

## Step 3 — Separate the human decision from the technical delivery

An incident usually has both a human lever and a technical enabler, and conflating them
hides half the fix:

- **Technical layer** — the look-alike domain the filter passed, the spoofable From
  header (no DMARC enforcement), the attachment that executed, the OAuth consent screen
  that granted a malicious app. These *are* patchable and often were the real gap.
- **Human layer** — the decision made on the manufactured context. This is not patchable
  by training alone, but it is *containable* by process (Step 4).

"The user clicked" often means "an unauthenticated sender reached the user's inbox with
an executable and a spoofed identity" — three technical failures wearing a human's face.
Find them before you write "user error."

---

## Step 4 — Move the defense from the person to the process

Because the exploit targets human judgment under manufactured context, the durable
control removes the *consequence* from the individual decision:

- **Out-of-band verification for consequential actions** — a wire transfer or a
  credential reset requires confirmation through a *different, pre-established* channel
  (call the vendor on the known number, not the one in the email). This is the human
  version of "authority comes from the channel, not the message"
  (`agent-trust-boundaries`, `irreversible-action-gate`).
- **Make the safe path the easy path** — a one-click "report phish" button, a finance
  workflow where dual-approval is default, a help desk script that never resets on
  inbound assertion of identity alone.
- **Reduce reliance on human vigilance** — DMARC enforcement, disabling macros,
  phishing-resistant MFA (FIDO2 over push), external-sender banners. Each shrinks how
  much the human must catch.
- **Measure the system, not the scapegoat** — report rate and time-to-report are better
  metrics than click rate; a fast report from someone who clicked is a working control.

---

## Step 5 — Report the failure without blaming the human

The writeup decides whether the org fixes the system or punishes a person:

- **State the control gaps** (Step 3's technical layer + the missing process gate),
  not "user fell for it." "User error" is an analytical dead end that prevents every
  future fix.
- **Credit the plausibility** — documenting *why* the pretext worked (Step 2) is what
  makes the case for the process control; "the user was careless" makes no case at all.
- **Awareness training is a WARN-level control, not a PASS** — it reduces rate, never to
  zero, and claiming coverage from a training completion is the checkbox fallacy
  (`control-effectiveness-vs-existence`). Say what training can and cannot carry.

---

## The one-line test

If your explanation of the incident ends at "the user should have known better," you
have described the bait and skipped the trap — find the manufactured context that made
the decision reasonable and the missing process gate that let one person's mistake reach
a consequence, because those, not the person, are the finding.
