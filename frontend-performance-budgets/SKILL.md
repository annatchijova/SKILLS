---
name: frontend-performance-budgets
description: Set and enforce explicit performance budgets before writing frontend code, not measure after the fact — outcome metrics (LCP/INP/CLS) and the causal resource budgets that actually produce them (JS shipped, image weight, font loading, third-party scripts, critical request count, hydration cost). Use whenever adding a dependency, image, route, or client component, or when a page "feels slow" and the cause isn't obvious. Trigger on "bundle size", "Core Web Vitals", "hydration", "third-party script", "lazy load", "code split", "why is this slow", "LCP/INP/CLS", "render-blocking". Not a general "make it fast" skill — it is specifically about setting the budget before the fact and tracing outcome metrics to their causal resource.
---

# Frontend Performance Budgets

An outcome metric (LCP, INP, CLS) tells you the page is slow. It does not tell
you what to change — that requires tracing the outcome to the causal resource
that produced it. This skill keeps the two separate on purpose: **outcome
metrics** are what the user experiences and what you measure in the field;
**causal budgets** are what you constrain at build/review time because they
are the actual levers.

Composes with the library:

- **resource-exhaustion-review** — covers cost blow-up from *untrusted input*
  size (server-side); this skill covers cost from *your own* shipped
  resources (client-side), a different axis of the same discipline
- **frontend-component-boundaries** — client/server component boundary
  decisions in RSC frameworks directly gate hydration cost, one of the causal
  budgets below
- **non-overwhelming-ux** — perceived speed and jank contribute to cognitive
  load; this skill supplies the mechanism, that skill the user-facing
  rationale

---

## Outcome metrics (empirical evidence: field data, from web.dev / CrUX)

Source: [web.dev, Core Web Vitals](https://web.dev/articles/vitals).

| Metric | Good threshold (75th percentile, field data) | What it measures |
|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.5s | Time to render the largest visible element |
| INP (Interaction to Next Paint) | ≤200ms | Responsiveness of the *slowest* interaction across the session |
| CLS (Cumulative Layout Shift) | ≤0.1 | Unexpected layout movement |

**MUST** measure these at the 75th percentile of real users (field data), not
lab/synthetic averages — a lab score can pass while real users on slower
devices/networks fail the threshold. **SHOULD** set a budget per metric before
starting work on a page, not after shipping and noticing a regression.

## Causal resource budgets (methodological decision: what actually moves the outcome metrics)

These are not standards — they are the mechanism. Set explicit numeric
ceilings per project/route; the numbers below are starting points from field
practice, not universal law.

| Resource | Typical starting budget | Feeds which outcome metric | Applies when |
|---|---|---|---|
| JS shipped to client (compressed) | ≤170KB on the critical route | INP, and LCP via main-thread blocking | Any route rendering interactive UI |
| Total image weight above the fold | Sized to viewport, served in next-gen format (avif/webp) | LCP | Any route with a hero/above-fold image |
| Web font loading | `font-display: swap` or preloaded, ≤2 font families | CLS (swap-induced shift), LCP (if font blocks text render) | Any custom web font |
| Third-party scripts | Justified individually; each one is a request, a parse cost, and an unmanaged layout risk | LCP, INP, CLS simultaneously | Analytics, chat widgets, ad tech, embeds |
| Critical-path requests (render-blocking) | Minimize; nothing render-blocking that isn't needed for the LCP element | LCP | Any synchronous `<script>`/`<link>` in `<head>` |
| Hydration cost (React/Next.js RSC, or equivalent) | Client components only where interactivity is actually needed | INP, TBT | Any SSR/RSC framework — see `frontend-component-boundaries` |

**MUST** set the JS and image budgets explicitly per route before
implementation, when the route is known to be LCP- or INP-sensitive (landing
pages, checkout, any high-traffic entry point). **MAY** skip formal budgeting
for low-traffic internal tooling where the cost of measurement exceeds the
cost of the regression.

## Tracing outcome → cause (the actual debugging method)

1. **LCP is bad** → find the LCP element (Chrome DevTools Performance panel
   names it). Is it render-blocked by JS/CSS? Not preloaded? Is it an image
   with no explicit `width`/`height`, or loaded from a slow third-party host?
2. **INP is bad** → find the long task on the slowest interaction. Usually:
   too much JS parsing/executing on the main thread, or a synchronous
   handler doing work that should be deferred/chunked/moved off-thread.
3. **CLS is bad** → find the element that shifted. Usually: an image/ad/embed
   with no reserved space, a web font swap without matching fallback metrics,
   or content injected above existing content after load.

Never optimize the outcome metric directly ("just make LCP faster") without
naming the causal resource — that produces cargo-cult fixes (adding
`loading="lazy"` to an above-the-fold image, which *worsens* LCP).

## Failure modes / anti-patterns

- **Lazy-loading the LCP element.** `loading="lazy"` on the hero image delays
  the metric it's supposed to help.
- **Budget measured only in the lab.** A dev-machine Lighthouse score of 95
  says nothing about a real user on a mid-tier phone on 4G — always check
  field data (CrUX, RUM) before declaring victory.
- **One giant third-party bundle for one small feature** (e.g. a full charting
  library for a single sparkline) — the causal-budget check ("what does this
  dependency cost") is skipped because the outcome metric hasn't been
  measured yet.
- **Client component by default** in an RSC framework — every component
  marked `'use client'` ships its JS and hydrates, whether or not it needs
  interactivity.
- **No `width`/`height` (or `aspect-ratio`) on images/embeds** — the browser
  can't reserve space, so content shifts when the resource loads.

## Verifiable checks

- [ ] Route has a stated LCP/INP/CLS budget, checked against field data (CrUX
      report or RUM), not only lab Lighthouse.
- [ ] The LCP element is identified and is not render-blocked, not
      lazy-loaded, and preloaded if it's a late-discovered resource.
- [ ] JS bundle size for the route is measured (build analyzer) against a
      stated ceiling.
- [ ] Every image/embed has explicit dimensions or `aspect-ratio` reserved.
- [ ] Every third-party script is individually justified and, where possible,
      loaded async/deferred or on interaction.
- [ ] Every component marked as client-rendered (`'use client'` or
      equivalent) is client-rendered because it needs interactivity, not by
      default — see `frontend-component-boundaries`.
