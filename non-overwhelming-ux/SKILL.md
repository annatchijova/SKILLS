---
name: non-overwhelming-ux
description: Design and review user flows, forms, dashboards, and onboarding for cognitive, sensory, and choice load — grounded in WCAG 2.2 cognitive-accessibility criteria and W3C COGA guidance, and applicable to every user, not only neurodivergent ones, because reduced cognitive load helps anyone under stress, time pressure, or divided attention. Use whenever designing or reviewing a flow with multiple steps, simultaneous choices, interruptions, or time pressure. Trigger on "too many options", "overwhelming", "cognitive load", "sensory overload", "ADHD/autism-friendly", "decision fatigue", "the user got lost", "too many steps", stacked modals, autoplay, or countdown timers. Not a visual-design skill (color/typography aesthetics) — it governs interaction patterns, information architecture, and pacing.
---

# Non-Overwhelming UX

Accessibility framing treats cognitive load reduction as a feature for a
minority of users. The evidence doesn't support that framing: choice overload,
decision fatigue, and sensory overload degrade task completion for anyone
operating under stress, interruption, or divided attention — a neurotypical
user checking out on a phone while distracted is closer to a neurodivergent
user's baseline experience than either group's advocates usually credit.
Treat every rule below as a floor requirement for some users and a
quality improvement for everyone else, not as an optional add-on.

Composes with the library:

- **frontend-accessibility-by-construction** — perceivability/operability
  (WCAG Level A/AA structural requirements) is that skill's scope; this
  skill covers pacing, load, and interruption, which WCAG 2.2's cognitive
  criteria (COGA) also address but which are easy to satisfy technically
  while still producing an overwhelming experience
- **resilient-ui-states** — this skill's "never destroy user-entered work on
  error" principle is the same rule that skill states from the resilience
  angle; don't duplicate the implementation, cite it

---

## Standards (primary source: normative)

Source: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [W3C COGA — Making
Content Usable](https://w3c.github.io/coga/extension/index.html), [W3C WAI
COGA task force](https://www.w3.org/WAI/about/groups/task-forces/coga/).

| Rule | Level/source | Applies when | Does not apply when |
|---|---|---|---|
| **MUST** — no unrequested content change/interruption during input (autosubmit, auto-refresh) | WCAG 3.2.2 (A) | Forms, any input flow | User explicitly enabled the behavior |
| **MUST** — user can request more time or turn off a time limit, except real-time events | WCAG 2.2.1/2.2.6 (A/AAA) | Any session/task with a timer | The time limit is essential and real (e.g. a live auction) — must still warn and offer extension where technically possible |
| **MUST** — where a help mechanism (contact detail, self-help, chat, phone) appears on multiple pages of a set, it occurs in the same relative order/position on each, unless the user changed it | WCAG 3.2.6 Consistent Help (A) — verified against the exact SC text, 2026-09-22 | Any multi-page or multi-step flow with a repeated help mechanism | N/A |
| **SHOULD** — plain, direct language: one point per sentence; a sentence using more than two clauses is a candidate to split | COGA, *Making Content Usable*, quoted directly: "Have one point per sentence" / "If a sentence can use more than two clauses, it typically can be broken up" | User-facing copy: instructions, errors, confirmations | Legal/regulatory text with mandated wording — flag as an exception, don't silently rewrite |
| **SHOULD** — provide an undo/confirmation step before a destructive or hard-to-reverse action, instead of only a warning dialog | COGA / general usability heuristic | Delete, purchase, irreversible submit | The action is trivially reversible already (e.g. toggling a filter) |

**Provenance note, corrected 2026-09-22 (claim-provenance-discipline audit):**
WCAG 3.2.6 Consistent Help does **not** specify a numeric interaction count to
reach help — an earlier draft of this skill stated "≤2 interactions" and
attributed it to WCAG/COGA; that number does not appear in the normative SC
text and has been removed. Reaching help quickly and without re-explaining
context is still good practice — it is now stated as a MAY-level heuristic in
the checklist below, with no numeric authority and no standards citation,
because none exists.

## Empirical evidence: choice and cognitive load (not a W3C standard — behavioral research, and a section that needs its own provenance warning)

Source: [Laws of UX — Choice Overload](https://lawsofux.com/choice-overload/)
(verified: does **not** state a numeric threshold), [NN/g and others on
Miller's Law misapplication](https://stephaniewalter.design/blog/your-menu-doesnt-need-millers-7-plus-minus-2-rule/),
[UX Myths — "Choices should always be limited to 7±2"](https://uxmyths.com/post/931925744/myth-23-choices-should-always-be-limited-to-seven).

**Provenance note, corrected 2026-09-22:** an earlier draft of this section
claimed "capping simultaneous choices at roughly 5-9," implicitly Miller's
"7±2." That number is a documented UX myth in this exact form: Miller's Law
describes *working-memory recall capacity* (how many items a person can hold
in mind with nothing visible to check against), not how many *visible,
scannable* options an interface can show. A persistent on-screen menu relies
on recognition, not recall — NN/g and multiple UX sources explicitly warn
against capping nav items or visible choices at 7 for this reason. The
lawsofux.com source cited for the number does not, on inspection, state it.
The number is retracted; no numeric ceiling is asserted below.

Too many simultaneous options still measurably increase decision time,
anxiety, and abandonment (choice overload is real and well-documented) — but
the mechanism is **decision load**, not **memory capacity**, so the fix is
**grouping/filtering/chunking a large option set**, not hitting a specific
count. Apply this distinction:

- **Recognition context** (a visible nav menu, a visible list of filters the
  user scans rather than memorizes): there is no evidence-backed numeric cap.
  Group by category when the list is long enough that scanning it becomes the
  bottleneck — that is a UX judgment call per content, not a formula.
- **Recall/working-memory context** (a set of options the user must hold in
  mind to compare or decide between without re-reading — e.g. several
  interdependent form fields that must be filled from memory of an earlier
  step): this is where Miller's Law's actual claim (working-memory limits)
  applies, and chunking into smaller groups is the correct mitigation.

## Neurodivergent-specific guidance (secondary sources — practitioner literature, treat as heuristic, not standard)

Source: aggregated from ADHD/autism-focused UX design literature (practitioner
guides, not peer-reviewed standards — apply as heuristic, verify with real
users where the stakes are high).

- Predictable layout: navigation and key controls stay in the same position
  across the flow; nothing reorders based on state without the user
  triggering it.
- Optional low-stimulation mode: ability to disable non-essential animation,
  autoplay media, and decorative motion without losing functionality.
- Progressive disclosure: reveal detail only as needed, rather than
  presenting the full depth of a flow/page at once — reduces the "freeze"
  response to an unbounded amount of visible information.

## Failure modes / anti-patterns

- **Fabricated urgency**: countdown timers or "only 2 left" indicators that
  don't correspond to a real, verifiable fact — this manufactures anxiety
  without informing a decision, and is flatly incompatible with the "no time
  pressure without user control" principle above. If the scarcity is real,
  state it plainly; if it isn't, remove it.
- **Modal stacking**: a confirmation dialog opening on top of another dialog
  or a toast notification appearing while a modal is open — each interruption
  compounds the working-memory cost of the one before it.
- **Silent context reset**: a multi-step form or wizard that discards
  progress on a back-navigation, browser refresh, or a minor validation
  error — forces the user to reconstruct decisions they already made.
- **Ambiguous success/failure**: an action that changes state with no visible
  confirmation, leaving the user to guess whether it worked (did the "add to
  cart" register? did the form actually submit?).
- **Choice-without-grouping**: a filter panel or settings page listing 20+
  ungrouped options flat, instead of chunked into named categories with
  progressive disclosure.
- **Buried help**: a support/contact path that requires navigating away from
  the current task and re-explaining context already provided (e.g. re-typing
  an order number already visible on screen).

## Verifiable checks

- [ ] No countdown timer, low-stock indicator, or "X people viewing this"
      claim renders without being tied to a real, verifiable value.
- [ ] At any point in a flow, at most one modal/dialog/toast requiring
      attention is presented — no stacking.
- [ ] A user can pause, leave, and resume a multi-step flow (refresh,
      back-button, or explicit save) without losing entered data.
- [ ] Any timed session either has no hard limit, or offers an extension/
      warning before expiry (WCAG 2.2.1/2.2.6).
- [ ] A visible/scannable list (nav, filters) has no numeric cap asserted
      against it — check instead whether a *long* list (judgment call: long
      enough that scanning it is itself the bottleneck) is grouped into
      named categories rather than left flat. A *recall*-type set (options
      the user must hold in mind without re-reading, not just scan) is
      chunked into smaller groups — this is the case Miller's Law actually
      covers; see the provenance note above before citing "7" for anything
      else.
- [ ] Every state-changing action (submit, add, delete, save) produces a
      visible, unambiguous confirmation.
- [ ] A help/contact path exists without requiring the user to leave the
      task and re-supply context already given; if repeated across pages
      within a set, it appears in the same relative position each time
      (WCAG 3.2.6 — this is the actual normative requirement; no interaction
      count is specified anywhere in the SC and none should be asserted as
      if it were).
- [ ] User-facing copy (errors, instructions, confirmations) is checked for
      sentence length and subordinate-clause count — flag anything reading
      as legal/technical register outside of actual legal text.
