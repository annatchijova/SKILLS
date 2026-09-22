---
name: frontend-component-boundaries
description: Decide where to cut a frontend component's boundary by cohesion, behavior, semantics, reuse, and shared reasons to change — not by a mechanical "one responsibility per component" rule that produces ceremonial fragmentation. Use whenever creating a new component, splitting or merging existing ones, or reviewing a PR that adds/removes component files. Trigger on "should this be its own component", "this component is doing too much", "prop drilling", "too many props", "extract a component", "where does this state live". Not a naming/style-guide skill — it's about the structural decision of where the boundary goes.
---

# Frontend Component Boundaries

"One responsibility per component" sounds precise and is actually
underspecified — a component that renders a labeled input with validation has
"one responsibility" by any reasonable reading, and so does a component that
renders an entire checkout form. The rule doesn't tell you which one is
right; it just supplies false confidence for whichever granularity you picked
first. This skill replaces the slogan with the actual criteria.

Composes with the library:

- **frontend-performance-budgets** — the client/server component split in
  RSC frameworks is a boundary decision governed by *this* skill, whose
  performance consequence is covered *there*
- **resilient-ui-states** — where a loading/error/empty state machine lives
  (owned by the fetching component vs. passed down) is a boundary decision
- **non-overwhelming-ux** — a boundary that fragments one user-perceived task
  across many components can still be correct code architecture while
  producing a confusing, disjointed UI; keep the two judgments separate

---

## Methodological decision: five criteria, not one rule

There is no single normative source for component granularity — this is a
heuristic/methodological section, not a cited standard. Evaluate a proposed
boundary against all five; a boundary that fails most of them is probably
wrong, but a boundary that satisfies four and stretches the fifth may still
be the right call. **This is a judgment call, not a formula** — the failure
mode of "one responsibility" was treating a heuristic as a formula; do not
replace it with a stricter one.

1. **Cohesion** — do the pieces inside this boundary change together because
   they represent one coherent piece of UI state or behavior? (A form field's
   label, input, and its own validation message are cohesive; splitting them
   into three components that must be wired together by the parent on every
   use is not a responsibility split, it's friction.)
2. **Behavior** — does this boundary encapsulate a distinct interaction or
   state machine (open/closed, valid/invalid, loading/error) that the rest of
   the tree doesn't need to know about? A boundary around behavior hides
   complexity; a boundary that just wraps markup with no behavior of its own
   adds an indirection with nothing to show for it.
3. **Semantics** — does the boundary correspond to something a person
   describing the UI out loud would name ("the price card", "the filter
   panel")? If the only way to describe a component's purpose requires
   describing its internal implementation, the boundary is probably drawn at
   the wrong level.
4. **Reuse** — is this rendered, or plausibly about to be rendered, in more
   than one place with the same behavior? Reuse is a *reason* to extract a
   boundary, not a *requirement* for one — a component used exactly once is
   not automatically wrong.
5. **Shared reason to change** — when a product requirement changes, does it
   touch this whole boundary as a unit, or does it touch pieces that are
   artificially fused together (a data-fetching concern bundled with a purely
   presentational concern that a designer would want to change independently
   of the API)?

## Composition over configuration (empirical/industry heuristic)

**SHOULD** prefer composing smaller components (children, slots, render
props) over a single component with many boolean/variant props controlling
its internals. **Applies when** the variations represent genuinely different
content or behavior. **Does not apply** when the "variants" are truly just
styling toggles on otherwise-identical markup — in that case a single
component with a `variant` prop is simpler than five near-duplicate
components.

A prop list is a warning sign at the point where a caller has to read the
component's internals to know which combination of props is valid — that's
config-space explosion, not flexibility.

## Props describe intent, not implementation (heuristic)

`onSelect`, `onConfirm`, `onDismiss` describe what the consumer is doing;
`handleClick`, `handleChange` describe what the component does internally and
leak that detail to every caller. **SHOULD** name props/events for the
caller's intent. This is a naming heuristic, not a structural boundary rule —
it doesn't change where the boundary is, only how legible it is once drawn.

## Local state by default (heuristic, not a rule about component size)

**SHOULD** keep state local to the component that owns the behavior it
drives, and lift it only when a sibling or ancestor genuinely needs to read
or drive the same state. **MUST NOT** lift state to global/context by default
"in case it's needed later" — that's speculative coupling, and it makes every
consumer of the global state a hidden dependency on every other one.

## Failure modes / anti-patterns

- **Ceremonial fragmentation**: splitting a cohesive unit (label + input +
  error) into three separate component files because "one responsibility"
  was read as "one DOM element," producing a parent that has to manually wire
  IDs, ARIA attributes, and state between them — the split *adds* a place to
  break `aria-describedby` wiring, it doesn't remove complexity.
- **God component**: the inverse failure — one component doing data fetching,
  business logic, and rendering of an entire page section, where no single
  criterion above justifies keeping it fused (fails cohesion *and* shared
  reason to change, because a copy-change and an API-change now touch the
  same file for unrelated reasons).
- **Boolean prop explosion**: a component with `isCompact`, `isDark`,
  `hideFooter`, `showIcon`, `variant`, each combination untested, most
  combinations never actually rendered — a config surface nobody can reason
  about, disguised as one component.
- **Premature global state**: state lifted to context/global store "for
  reusability" before a second consumer exists — every future reader of that
  state now has to understand a wider blast radius than the feature needed.
- **Reuse-driven fragmentation with divergent behavior**: two call sites that
  look similar today are forced to share one component, and future changes
  add branching (`if (variant === 'checkout')`) inside it instead of letting
  them diverge — reuse was a reason to extract, not a reason to weld
  permanently.

## Verifiable checks

- [ ] For each component boundary, at least one of the five criteria
      (cohesion, behavior, semantics, reuse, shared reason to change) is
      articulable in one sentence — if none apply, question the split.
- [ ] No component requires the parent to manually re-wire ARIA
      relationships (`aria-describedby`, `aria-controls`) across a split that
      exists for organizational reasons only.
- [ ] Boolean/variant props on a single component: if there are more than
      ~4-5, or combinations exist that are never actually used, the
      component is a candidate for splitting by variant instead of branching
      internally.
- [ ] State lives in the lowest common owner of the components that need it
      — not lifted further "for later" without a current second consumer.
- [ ] Prop and event names describe what the caller is doing
      (`onSelect`/`onConfirm`) rather than the component's internal handler
      name.
