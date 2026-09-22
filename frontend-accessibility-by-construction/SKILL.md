---
name: frontend-accessibility-by-construction
description: Build interactive frontend components — forms, modals, navigation, custom widgets — so they are operable and perceivable by construction, not patched afterward with ARIA. Use whenever writing or reviewing a component with keyboard interaction, focus behavior, or non-text content. Trigger on "accessible", "a11y", "keyboard nav", "screen reader", "focus trap", "aria-*", "custom dropdown/modal/tabs", "tap target", or a component built from a bare `<div>`/`<span>` instead of a native interactive element. Not a visual-design skill — color contrast and typography live here only where they gate comprehension, per WCAG, not as aesthetic preference.
---

# Frontend Accessibility By Construction

Accessibility retrofitted after a component ships is ARIA-as-plaster: attributes
bolted onto a `<div>` that was never operable to begin with. This skill is about
the order of operations — semantic structure and keyboard operability are
decided *before* a line of markup is written, not audited in afterward.

Composes with the library:

- **non-overwhelming-ux** — cognitive/sensory load (chunking, pacing,
  interruption control) is that skill's scope; this skill governs
  perceivability and operability of a single component
- **resilient-ui-states** — error/loading/empty states must also be
  accessible (announced, not just visible); see that skill for the state
  machine itself
- **validate-at-the-boundary** — this skill covers the *accessible surfacing*
  of a validation error (aria-invalid, aria-describedby); that skill covers
  the validation logic itself

---

## Standards (primary source: normative)

Source: [WCAG 2.2, W3C Recommendation](https://www.w3.org/TR/WCAG22/), [WAI Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/).

| Rule | Level | Applies when | Does not apply when |
|---|---|---|---|
| **MUST** — every interactive element reachable and operable via keyboard alone, no trap | A (2.1.1, 2.1.2) | Any custom widget (dropdown, tabs, modal, carousel) | Never waived — this is the floor |
| **MUST** — visible focus indicator on every focusable element | AA (2.4.7) | Always, unless a component-specific indicator (e.g. selected-state styling) is equally visible | Do not remove `outline` without a replacement that meets the same contrast |
| **MUST** — semantic structure conveys relationships (headings, lists, form labels) programmatically, not by layout alone | A (1.3.1) | Any content where visual grouping implies semantic grouping | N/A |
| **MUST** — target size ≥24×24 CSS px, or equivalent spacing, for pointer/touch targets | AA (2.5.8) | Buttons, links, form controls in normal reading flow | Inline text links, elements with an unstyled default browser rendering with no alternative |
| **MUST** — any drag interaction has a non-drag alternative (single pointer, no path) | AA (2.5.7) | Reordering lists, sliders, drag-to-dismiss | Drag is essential and no equivalent exists (rare — justify explicitly) |
| **SHOULD** — no more than one unexpected context change on input alone (focus, autosubmit) | AA (3.2.2) | Form fields, selects | User was warned beforehand |

MUST = the interface is broken without it. SHOULD = strong default; a documented
exception with a stated reason is acceptable. MAY = situational judgment call,
no standard mandates it.

## The precedence rule (methodological decision, not a standard)

1. **Native HTML element first.** `<button>`, `<a href>`, `<select>`, `<input>`,
   `<dialog>` already carry keyboard behavior, focus management, and semantics
   for free. Reaching for a `<div onClick>` is opting out of all of it.
2. **ARIA only where native HTML has no equivalent** (a combobox, a tree, a
   tablist). Follow the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) patterns exactly —
   a custom ARIA pattern invented ad hoc is worse than no ARIA, because it
   claims a contract with assistive tech it doesn't fulfill.
3. **Never use ARIA to fix a semantic problem native HTML would have
   prevented.** `role="button"` on a `<div>` still needs `tabindex`, `onKeyDown`
   for Enter/Space, and focus styling manually reimplemented — every one of
   which is a place to regress silently on the next edit.

## Failure modes / anti-patterns

- **Div-button**: `<div onClick>` with no `role`, `tabindex`, or keyboard
  handler — invisible to keyboard and screen reader users, works fine in a
  manual mouse-only test, which is why it ships.
- **Focus black hole**: opening a modal/menu that doesn't move focus into it,
  or closing one that doesn't return focus to the trigger — keyboard users
  land nowhere or lose their place.
- **Outline: none** with no visible replacement — passes a visual design
  review, fails every keyboard-only walkthrough.
- **ARIA overload**: adding `role`, `aria-label`, and `aria-*` to an element
  that already had correct native semantics — redundant announcements are as
  harmful as missing ones.
- **Icon-only control with no accessible name** — a trash-can icon button with
  no `aria-label`/visually-hidden text announces as "button" with no purpose.
- **Live region misuse**: wrapping static content in `aria-live` "just in
  case" — announces on every re-render, including irrelevant ones.

## Verifiable checks (for audit, human or agent)

- [ ] Every interactive element is reachable via Tab, in a logical order, with
      no keyboard trap (test: unplug the mouse, complete the flow).
- [ ] Every focused element has a visible indicator distinguishable from
      unfocused state.
- [ ] Every `<img>` conveying information has `alt`; every purely decorative
      image has `alt=""` or is a CSS background.
- [ ] Every form input has a programmatically associated `<label>` (not
      placeholder-only).
- [ ] Every icon-only interactive control has an accessible name
      (`aria-label`, `aria-labelledby`, or visually-hidden text).
- [ ] Opening a modal/dialog moves focus inside it; closing it returns focus
      to the trigger; Escape closes it.
- [ ] Tap targets measure ≥24×24px or have equivalent effective spacing.
- [ ] Any drag interaction has a keyboard/click alternative.
- [ ] Run an automated check (axe-core, Lighthouse a11y) as a floor, not a
      ceiling. Estimates of automated coverage vary by what's being counted
      and by vendor — [WebAIM Million 2026](https://webaim.org/projects/million/)-adjacent
      reporting puts machine-detectable *success criteria* around 20-30%,
      while Deque cites axe-core catching "on average 57%" of issues *by
      volume* (a few highly automatable failure types, like missing alt text
      and low contrast, dominate raw counts). No single number is
      authoritative across sources — treat automated tooling as necessary
      and clearly insufficient, and follow it with keyboard-only and
      screen-reader spot checks regardless of which estimate you use.

## What this skill does not cover

Color contrast as a pure aesthetic choice is out of scope except where it
crosses the WCAG 1.4.3 threshold (4.5:1 normal text, 3:1 large text/UI
components) — that threshold is a comprehension/perceivability requirement,
not a design preference, and is the one visual rule this skill enforces.
