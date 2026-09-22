---
name: frontend-testing-strategy
description: Allocate frontend test effort by the Testing Trophy (static > unit > integration > E2E) and write tests that assert on what the user perceives, using stable selectors, instead of internal implementation. Use whenever writing or reviewing UI tests, deciding what layer to test something at, or diagnosing flaky tests. Trigger on "how should I test this component", "flaky test", "testing implementation details", "what should be an E2E test", "selector broke when I refactored", "test pyramid". Not about test framework setup or CI configuration.
---

# Frontend Testing Strategy

A test suite that breaks every time you refactor a component's internals
without changing its behavior is testing the wrong thing. This skill is about
two decisions: **which layer** a given piece of behavior should be tested at,
and **what a test is allowed to know about** the component it's testing.

Composes with the library:

- **falsifiable-testing** — the general discipline (red-first, negative
  controls, oracle strength) applies here; this skill adds the
  frontend-specific layer allocation and selector discipline on top
- **resilient-ui-states** — the four mandatory states (loading/success/empty/
  error) are exactly what integration tests in this skill should cover per
  component
- **frontend-accessibility-by-construction** — role/label-based selectors
  (below) double as an accessibility check: if a test can't find an element
  by its accessible role or name, neither can a screen reader

---

## Layer allocation: the Testing Trophy (industry heuristic, not a normative standard)

Source: Testing Trophy model (Kent C. Dodds), Testing Library philosophy
("the more your tests resemble the way your software is used, the more
confidence they can give you").

| Layer | What it catches | Proportion of effort | Applies when |
|---|---|---|---|
| Static (TypeScript, ESLint) | Type errors, unreachable code, banned patterns | Broadest, cheapest — run on every keystroke/save | Always; this is the floor, not optional |
| Unit | Pure logic: a formatter, a reducer, a validation function | Small, focused on logic with no rendering | Any non-trivial pure function extracted from a component |
| Integration | A component (or a few composed together) rendered with real DOM, user interaction simulated | The largest deliberate investment — most bugs live at this layer | Any component with state, async data, or user interaction |
| E2E | A critical path through the real app, real routing, real (or realistic) backend | Smallest, most expensive, reserved for paths where a failure is severe | Checkout, auth, and other flows where an integration-test false-positive would be costly to miss |

**SHOULD** weight integration tests as the largest deliberate investment, not
unit tests — a component's value is almost always in how its pieces behave
together (state + rendering + interaction), which unit tests of isolated
functions don't exercise. **SHOULD NOT** write E2E tests for behavior already
covered by a faster integration test — E2E is for the paths where the
integration between real systems (routing, backend, auth) is itself the
thing under test.

## What a test is allowed to know

**MUST** assert on what a user would perceive: visible text, accessible
role/name, resulting DOM state a screen reader or sighted user would notice.
**MUST NOT** assert on internal state, private methods, or implementation
details (a component's internal `useState` value, a class instance's private
field) — that couples the test to the implementation, so a refactor with
identical behavior breaks the test for no user-visible reason.

**SHOULD** query the DOM the way a user or assistive technology would:
by accessible role and name (`getByRole('button', { name: 'Submit' })`), by
visible label, or by text content — **SHOULD NOT** query by CSS class name,
DOM structure/nesting, or element order, all of which are implementation
details that change on a purely visual refactor.

## Failure modes / anti-patterns

- **Implementation-detail testing**: asserting a component's internal state
  variable equals `true`, or calling an internal method directly — the test
  passes and fails independent of what the user actually sees.
- **Brittle selectors**: `.container > div:nth-child(2) > span` — breaks on
  any markup reshuffle even when behavior is unchanged; the inverse failure,
  a test that *doesn't* break when behavior actually changes, is just as
  common with overly loose selectors (e.g. matching by partial class name).
- **Snapshot-everything**: a full-DOM snapshot test that nobody reads on
  failure — it "catches" every change including intentional ones, training
  reviewers to `--update-snapshot` without reading the diff, which is
  equivalent to not testing.
- **E2E as the primary safety net**: pushing most coverage to E2E because
  it "feels most real" — slow, flaky under CI resource contention, and a
  failure gives almost no localization (which of 40 steps broke?).
- **Non-deterministic test data**: relying on real dates, random IDs, or
  live network calls inside a test — produces flakiness that gets
  "fixed" with retries instead of a fixed clock/seeded fixture, hiding a real
  bug behind noise.
- **Testing the framework, not the code**: asserting that `useEffect` ran, or
  that React re-rendered a specific number of times — tests React's own
  contract, not anything the team wrote.

## Verifiable checks

- [ ] No test asserts on internal component state, private methods, or
      instance internals not observable by a user.
- [ ] Selectors use accessible role/name or visible text — grep the test
      suite for CSS-class or DOM-structure selectors (`.className`,
      `nth-child`, `querySelector` with structural paths) as a smell, not an
      automatic fail (a handful of legitimate exceptions, e.g. testing a
      CSS-driven visual state, are fine).
- [ ] Every component with async data has an integration test covering at
      least loading, success, and error (see `resilient-ui-states` for the
      required states).
- [ ] E2E tests exist only for flows where the integration between real
      systems is the point (auth, payment, cross-page navigation) — not as a
      substitute for integration coverage of a single component.
- [ ] Test data (dates, IDs, random values) is fixed/seeded, not sourced from
      `Date.now()`, `Math.random()`, or a live network call.
- [ ] A failing test's output names what a human would recognize as wrong
      (e.g. "expected button 'Submit' to be enabled") rather than an opaque
      diff of internal state.
