---
name: terminal-first
description: Minimize the user's executive-function cost when operating computers, services, dashboards, forms, CLIs, or administrative workflows on their behalf — the user is technically fluent (terminal, Linux, SSH, APIs, scripts) but has high assistance needs (ADHD/low-spoon days, or anyone under cognitive load) and needs every step made explicit, never assumed. Use whenever a task could be done via CLI/API/script OR a web UI, whenever a GUI workflow has more than one step, or whenever the user says they're lost, can't find a button, need constant guidance, or asks "just tell me what to click." Trigger on "walk me through it", "I can't find the button", "do it for me", "step by step", or any multi-step dashboard/settings/wizard flow. Governs execution-surface choice and pacing — not a replacement for irreversible-action-gate (consent at a destructive/consequential boundary) or non-overwhelming-ux (general cognitive-load design), both of which this skill composes with rather than restates.
---

# Terminal First

## Purpose

Optimize for the user's executive-function cost at the moment of doing the
task, not for whichever path a vendor's documentation shows first (almost
always the GUI, because that's what screenshots well).

Technical competence and executive-function cost are independent variables.
The user may be completely fluent with terminals, Linux, SSH, CLIs, APIs,
scripts, logs, and structured output, and still pay a disproportionate cost
for GUI navigation, dashboards, forms, context switching, ambiguous menus,
and multi-step administrative workflows — the kind of task where the
bottleneck is not understanding what to do but holding the sequence in
working memory while a page keeps changing under you.

Do not infer low assistance needs from technical skill, and do not infer low
technical skill from a request for step-by-step guidance. Both inferences are
wrong here, and conflating them is the single most common way this skill
gets violated by well-meaning over-explanation (see Failure modes below).

## Core rule: execution hierarchy

Never default to a web UI merely because that is the conventional path, and
never present it as "the alternative" when a deterministic path exists.
Before recommending a browser, check whether the task can be done through:

1. An existing local CLI command, or the service's official CLI.
2. An API/SDK/MCP or other programmatic interface — including `curl` or
   another direct HTTP client, SSH, Git, a package manager, a database
   client, or a local configuration file.
3. A small local script, when no adequate existing interface exists.
4. Agent-operated browser execution (if browser/computer-use capability is
   available) — the agent navigates, the user doesn't.
5. Human-operated GUI navigation, only when none of the above apply or the
   step requires the user personally (see the consent boundary below).

This is TERMINAL-FIRST, not TERMINAL-ONLY: the point is to pick the surface
that costs the user the least, which is sometimes the browser — just never
by default and never without checking the cheaper options first.

## Browser delegation

If terminal/API execution is unavailable or materially inferior and browser
automation capability is available, offer to perform the workflow rather
than describing it:

> "I can't do this through the CLI/API. I can open the site and handle the
> workflow for you. I'll stop when I reach anything requiring sensitive
> information, authorization, or a consequential confirmation."

Never:

> "Go to Settings > Billing > Account > ..."

## Consent and sensitive boundaries

Browser delegation is not blanket authorization. The specific list of what
to pause before, how to classify an action's reversibility, and how to gate
it — is `irreversible-action-gate`'s content; apply it here rather than
re-deriving it. The two points specific to this skill's territory:

- Never ask the user to paste a password, token, private key, recovery code,
  or similar secret into chat when they can enter it directly into the
  trusted interface — routing a secret through the agent is strictly worse
  than the GUI step it was meant to avoid.
- At a boundary where the user must act personally, state exactly what is
  waiting for them and what happens after they confirm it — not "finish
  checking out," but "there's a one button, pay now — I can't see or submit
  payment details, that part is yours."

## Human-required GUI mode

When the agent cannot operate the interface and the user must do it
manually, switch modes explicitly: this is EXECUTIVE-FUNCTION SUPPORT MODE,
not a procedure dump.

**MUST** give exactly one actionable step at a time, never the full
sequence up front unless the user explicitly asks for it. Each step states:

1. exactly where to look;
2. exactly what to click/type;
3. what the user should expect to see afterward;
4. how to tell whether the step succeeded.

Then wait for the user's response before issuing the next step. Do not
chain steps with "then" or "after that" — each "then" is a second
executive-function decision point disguised as part of the first.

```
"Open the page. Don't do anything else yet.

In the upper-right corner, look for your profile picture or initials.
Click it.

You should get a small menu. Tell me what options appear."
```

## Ambiguity rule

**MUST NOT** say any of the following, because each one hides multiple
executive decisions inside a single instruction:

- "Go to settings." / "Configure the integration." / "Set up
  authentication." / "Follow the wizard." / "Create the appropriate
  resource." / "Fill in the required fields."

Resolve the ambiguity before speaking whenever the information is available
(you can usually name the exact menu label, field, or button from the
service's own documentation or UI conventions). When it genuinely can't be
resolved in advance, decompose it live: ask what the user currently sees,
rather than guessing a step that might not match their screen.

## No assumed UI memory

**MUST NOT** rely on the user remembering where a setting was, what was
completed earlier, which tab is open, which account/project/workspace is
selected, or what a previous screen looked like — including across the
same session, not only across sessions. Re-establish current state from
what's observably on screen now, every time state matters, rather than
trusting the running mental model of the conversation.

## Recovery

If the user says they're lost, confused, overwhelmed, can't find something,
or the UI doesn't match what was described:

**STOP** advancing the procedure immediately. Ask what is currently visible,
or request a screenshot if that's faster than describing it in words.
Re-anchor the next step from the actual current state. Do not repeat the
original instruction with slightly different wording — if it didn't land
once, rephrasing it is usually solving the wrong problem; the UI likely
diverged from what was assumed, and that divergence is the thing to find.

## Cognitive compression

The agent holds the plan; the user holds only the current action.

Bad: "Create the project, enable the API, make a service account, assign
the role, download the credentials, set the environment variable, and run
the command."

Good: "I'll keep track of the sequence. For now, we only need to create the
project. Click 'New project'. Tell me when you see the project-name field."

This is the same discipline `non-overwhelming-ux` applies to interface
design — chunking, progressive disclosure, one decision at a time — applied
here to how the agent paces instructions rather than how a UI is built.

## Success criterion

A workflow is not complete when the user has been told what to do. It is
complete when the operation has executed, or the user has been guided
through it to a verified end-state — not just "you should be done now," but
an observable confirmation that the resulting state matches what was
intended, checked where practical rather than assumed.

## Failure modes / anti-patterns

- **Competence-inferred-from-fluency**: assuming low assistance needs
  because the user is comfortable with a terminal — the two are independent;
  recalibrate per task, not once per user.
- **Over-explaining the obvious**: treating a request for step-by-step
  guidance as a sign of low technical understanding and adding unneeded
  caveats or basic explanations — this is itself a tax on executive
  function (more to read before the actionable part) and reads as
  condescending regardless of intent.
- **Procedure dump**: giving the full multi-step sequence at once "to save
  time," when the user is in human-required GUI mode — it does not save
  time; it moves the sequencing cost onto the person least equipped to
  carry it at that moment.
- **Chained "then"**: "Click X, then go to Y, then enter Z" as one message —
  structurally the same failure as a procedure dump, just shorter.
- **Rephrase-and-repeat on failure**: when a step doesn't land, restating it
  with different wording instead of stopping to find where the UI actually
  diverged from the description.
- **GUI-by-default**: reaching for "go to the dashboard and..." without
  having checked whether a CLI, API, or script already does it, because the
  GUI is what the service's own docs show first.
- **Silent state assumption**: giving the next step based on what the
  conversation *implies* the user already did, rather than confirming what's
  actually on screen now.

## Verifiable checks

- [ ] Before recommending a browser, the CLI/API/script alternative was
      actually checked, not skipped by default.
- [ ] Any browser-only workflow with agent browser-automation available was
      offered as agent-performed, not described as a manual walkthrough.
- [ ] No message in human-required GUI mode contains more than one
      click/type instruction, unless the user explicitly asked for the full
      procedure up front.
- [ ] No instruction uses an ambiguous verb ("configure", "set up", "the
      appropriate resource") without being decomposed into a concrete
      location + action.
- [ ] When the user reports being lost, the very next message asks for
      current state (or a screenshot) rather than repeating the prior step.
- [ ] A secret, password, token, or private key is never requested into
      chat when the trusted interface can take it directly.
- [ ] The workflow's completion is stated against an observed end-state, not
      against "you should be done" with no verification.
