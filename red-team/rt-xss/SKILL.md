---
name: rt-xss
description: "Red-team assessment of cross-site scripting boundaries: stored, reflected, DOM, blind and LLM-generated-content XSS across HTML, attribute, JavaScript and URL contexts. Covers context-aware probing, framework sink inventory (React, Vue, Svelte, Angular, Next, Solid, Astro), CSP/sanitizer bypass, mXSS and polyglots, re-expressed as scoped experiments against owned fixtures with marker payloads and negative controls instead of victim-facing exploitation."
---

# Cross-Site Scripting Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's XSS craft as scoped, marker-based laboratory experiments: it names the contexts, sinks and bypass families to test, without shipping victim-targeting payloads.

## Scope and prerequisites

Identify where untrusted input is reflected into a rendered response or evaluated by the DOM, and in which output context it lands. Use owned test accounts and a disposable instance; inject a unique, inert marker (a benign DOM mutation or a callback to an owned collector), never a credential-stealing or victim-facing payload.

Declare target, framework and version, permitted actions, attempt budget and stop condition. If only source is authorized, produce a context-based hypothesis and mark runtime verification NOT TESTED.

## Attack surface and injection classes

- **Reflected** — input echoed in the immediate response (search, error, URL params). Needs a delivery assumption to matter; state it.
- **Stored** — input persisted and rendered later to other sessions (comments, profiles, reviews). Highest impact, test with owned second account.
- **DOM-based** — a client-side sink (`innerHTML`, `document.write`, `eval`, `location`) consumes a source (`location.hash`, `postMessage`) with no server round-trip.
- **Blind** — execution happens in a context you cannot see (admin panel, log viewer); confirmed only by an owned out-of-band callback.
- **LLM-generated-content XSS** — model output rendered as HTML; the injection enters via poisoned context/RAG data and lands in an unsanitized sink.

Classify by output context before choosing a probe: HTML body, HTML attribute (quoted/unquoted), JavaScript string, URL/`href`, CSS, or a framework template binding. The escape required differs per context; a payload that fires in one is inert in another.

## Mechanism and observation

Trace source to sink: which input, through what encoding/sanitizer, into which context.

**Firstness:** Record the exact reflected bytes and the surrounding context (is the marker inside a quoted attribute, a script string, an HTML text node?). **Secondness:** State the expected encoding for that context and how the observation deviates. **Thirdness:** Infer the defect class only after a marker actually executes in a controlled view.

## Abduction and refutation

**Mechanism hypothesis:** Input reaches a context-inappropriate sink without the encoding that context requires, or a sanitizer is bypassed by a mutation/polyglot.

**Competing benign explanation:** The reflection is correctly entity-encoded and inert; the "execution" was the testing console, not the page; a CSP actually blocks the inline script despite the reflection; a framework auto-escapes and the raw value never reaches HTML.

## Deduction and controls

A context-appropriate encoded marker must stay inert; a true sink executes the marker where the encoded control does not. Predeclare the exact DOM event or callback that confirms execution. A marker that renders as visible text is a REFUTED injection for that context, not a finding. CSP, Trusted Types or a framework escape blocking execution is a PASS control, recorded separately.

## Induction: bounded laboratory procedure

Owned instance and owned viewer only; inert markers.

1. **Baseline.** Submit a benign unique string; locate every reflection and its context.
2. **Context probe.** Inject context-breaking characters inert to a correct encoder: `<>"'` in HTML, `"/>` in attributes, `';//` in JS strings, `javascript:` in URL sinks. Observe whether the context closes.
3. **Execution marker.** Only where the context breaks, fire an inert proof: a benign DOM mutation or a callback to your collector — not `document.cookie` exfiltration.
4. **Context-specific escalation (owned).** HTML: `<svg onload=...>`; attribute: `" autofocus onfocus=...`; JS string: break and chain; URL: `javascript:`/`data:` where the sink navigates.
5. **Encoded control.** Submit the same payload where the app claims it encodes; confirm it is inert there.
6. **Stored/blind.** For stored, view with a second owned account; for blind, wait on the owned OOB callback.

Record each result including refutations. Keep finding status (CANDIDATE/CONFIRMED/REFUTED/NOT TESTED) separate from control status (PASS/WARN/FAIL).

## Framework sinks and modern bypass craft

Most XSS now lives in framework escape hatches, not raw string concatenation. Know the dangerous APIs per stack (leads; confirm the live version):

- React: `dangerouslySetInnerHTML`, `href={userInput}` with `javascript:`.
- Vue: `v-html`. Angular: `bypassSecurityTrust*`, `[innerHTML]`. Svelte: `{@html}`. Solid: `innerHTML` in reactive statements. Astro: `set:html`. Next/Remix: unsanitized loader/Server-Action data, SSR hydration mismatches.

Bypass families to test as discriminators between filter and renderer:
- **CSP bypass** — JSONP endpoints, `base-uri`/`object-src` gaps, `unsafe-inline`, trusted-CDN script gadgets, nonce reuse.
- **mXSS** — markup that mutates on DOM re-serialization (innerHTML round-trips) into an executable form the sanitizer did not see.
- **Polyglot** — one payload valid across multiple contexts, to test context-detection failures.
- **Sanitizer bypass** — DOMPurify config gaps, `<template>`/`<noscript>`/SVG/MathML foreign-content tricks; confirm the installed sanitizer version.

## Domain-specific failure modes

A reflection is not execution; a payload firing in the console is not firing in the page. Framework auto-escaping can make a "reflected" value inert. CSP/Trusted Types can neutralize an otherwise-valid injection — report the residual impact honestly. Self-XSS (fires only in the attacker's own session) is not a finding without a delivery mechanism.

## Evidence and deliverable

Provide source, reflected context, the exact marker, the controlled execution event (or callback record), the encoded-control result, and any CSP/sanitizer that limited impact. Keep real session data out of portable output. Attach minimal replay, expected/observed, rival explanation, falsifier, and uncovered contexts.

## Versions and tool limitations

Pin framework, sanitizer and CSP versions. Scanner payloads may be stored and reach other users — only use owned accounts and inert markers. No tool or browser behavior was verified by this content; confirm installed versions and current browser behavior before claiming.

## Remediation and detection

Context-aware output encoding, Trusted Types + the native Sanitizer API, a strict nonce/hash CSP, framework-safe bindings, and no `innerHTML` of untrusted data. Add a regression asserting the marker renders inert. Detect via CSP violation reports and markers in logs correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An inert marker executes in a controlled owned view where the encoded control stays text: CONFIRMED; FAIL. |
| Benign refutation | The reflection renders as entity-encoded text / CSP blocks it: REFUTED for the tested context; PASS for the control. |
| Insufficient evidence | A reflection exists but no context break or execution is shown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-xss/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's context taxonomy, framework sink inventory and CSP/mXSS/polyglot bypass craft, re-expressed as owned-fixture experiments with inert markers and encoded controls, replacing victim-facing cookie/session exfiltration with bounded execution proof.
