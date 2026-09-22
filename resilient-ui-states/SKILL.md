---
name: resilient-ui-states
description: Design every view that fetches or mutates data around its full state machine — loading, success, empty, and error are all mandatory, none optional — with error handling that fails at the right boundary and produces a specific, actionable message. Use whenever building or reviewing a component that does async data fetching, mutation, or submission. Trigger on "loading state", "error state", "empty state", "skeleton", "error boundary", "form validation", "what happens if this fails", "spinner forever", "blank screen", "something went wrong". Not about visual polish of these states — about which states are required to exist and where failure is caught.
---

# Resilient UI States

A view with data has (at minimum) four states, and treating any of them as
optional is where the incident starts: the loading state that never resolves
because there's no timeout, the empty state that doesn't exist so the user
sees a blank screen and assumes the app is broken, the error that's caught
three components up and takes the whole page down with it.

Composes with the library:

- **honest-degradation** — this skill's error/empty states are the frontend
  instance of that skill's PASS/WARN/FAIL discipline: never render a
  best-effort or partial result as if it were the complete one
- **validate-at-the-boundary** — the error state produced by a rejected input
  is this skill's territory (how it's surfaced); the rejection logic itself
  is that skill's
- **frontend-accessibility-by-construction** — an error/loading state that
  isn't announced to assistive tech doesn't exist for a screen-reader user;
  see that skill for `aria-live`/`role="alert"` mechanics

---

## The four mandatory states (methodological decision)

Every component that depends on async data has exactly these states, and
**MUST** render something intentional for each — never assume one "won't
happen":

| State | MUST render | Common failure when skipped |
|---|---|---|
| Loading | A distinct, bounded-time indicator (skeleton or spinner) | Blank screen read as broken; or spinner with no timeout, spins forever on a hung request |
| Success | The actual data | (rarely skipped — this is the state everyone builds for) |
| Empty | A state distinct from both loading and error, explaining *why* it's empty and what to do next | Renders as an empty loading skeleton or an empty error — user can't tell "no results" from "still loading" from "broken" |
| Error | A specific, actionable message tied to what actually failed | Generic "Something went wrong", or the loading spinner just... stops, with no explanation |

**MUST** distinguish empty from error from still-loading in the rendered
output — these are three different facts and collapsing any two of them is a
comprehension failure, not just a polish gap.

## Error boundaries: scope the blast radius

Source: [Next.js error handling docs](https://nextjs.org/docs/app/getting-started/error-handling) (framework-level convention); general React error boundary pattern.

**SHOULD** place error boundaries per independent feature/section, not one
global boundary at the app root. **Applies when** a page has multiple
independently-useful sections (e.g. a dashboard with several widgets) — one
widget's fetch failure should not blank the whole page. **Does not apply**
when the failing section's data is load-bearing for everything else on the
page (e.g. auth state) — in that case a page-level boundary is correct,
because partial rendering would be actively misleading.

## Form validation timing and structure

Source: [TetraLogical, form validation and error messages](https://tetralogical.com/blog/2024/10/21/foundations-form-validation-and-error-messages/).

- **SHOULD** validate on blur, not on every keystroke — validating on
  keystroke punishes the user mid-typing for an incomplete value that isn't
  wrong yet, it's just unfinished.
- **MUST** associate the error with its field via `aria-invalid="true"` and
  `aria-describedby` pointing at the error text — a red border with no
  programmatic link is invisible to a screen reader.
- **SHOULD** render a summary of all errors at the top of the form on submit,
  in addition to inline errors, for forms with more than a couple of fields —
  a submit that silently scrolls to the first error loses everyone who tabs
  or uses a screen reader.
- **MUST** use `role="alert"` or an `aria-live` region for the error summary
  so it's announced without requiring the user to find it visually.

## Failure modes / anti-patterns

- **Infinite spinner**: no timeout or retry-with-backoff on a hung request —
  the loading state has no maximum duration, so a stalled network call is
  indistinguishable from a working one.
- **Generic error message**: "Something went wrong" / "Error" with no
  specifics and no next action — technically correct, operationally useless.
- **Empty-as-loading**: an empty result set renders the same skeleton as the
  loading state, so the user waits for data that will never arrive.
- **One error boundary to rule them all**: a single unhandled rejection in
  one widget blanks the entire page instead of just that widget.
- **Optimistic UI with no rollback path**: a mutation is rendered as
  succeeded before the server confirms, with no visible correction if it
  actually fails — the user acts on a state that silently reverts.
- **Validation on keystroke**: the field turns red while the user is still
  typing a valid value, before they've finished.
- **Form reset on error**: a failed submission clears fields the user already
  filled in, forcing them to redo work — see `non-overwhelming-ux` for why
  this is a cognitive-load failure, not just an annoyance.

## Verifiable checks

- [ ] Every component with async data has distinguishable loading, success,
      empty, and error renders (test: force each state and screenshot/diff).
- [ ] The loading state has a maximum duration (timeout) with a defined
      fallback, or is provably bounded by the request itself.
- [ ] The empty state names *why* it's empty when the reason is knowable
      (no results for this filter vs. nothing created yet) and offers a next
      action.
- [ ] Every error message is specific to the failure (network vs. validation
      vs. permission vs. server error) — grep for generic strings like
      "Something went wrong" and confirm each one has a fallback only, not a
      primary use.
- [ ] Error boundaries are scoped to independent sections, not a single
      app-root boundary, unless the failing section is load-bearing for the
      rest of the page.
- [ ] Form errors are both inline (per field, with `aria-invalid` +
      `aria-describedby`) and summarized (`role="alert"` region) on submit
      for forms beyond 1-2 fields.
- [ ] A failed submission preserves user-entered data — nothing is cleared on
      error.
