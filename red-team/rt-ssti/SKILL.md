---
name: rt-ssti
description: "Red-team assessment of server-side template injection boundaries across Jinja2, Twig, Freemarker, Velocity, Pebble, Thymeleaf, Smarty, Mako, ERB, Handlebars, EJS, Pug and Nunjucks. Covers arithmetic/polyglot detection, engine fingerprinting by decision tree and error signature, sandbox-escape and RCE chains as bounded impact classes, filter/WAF bypass and blind/OOB inference, re-expressed as owned-fixture experiments with inert markers and negative controls."
---

# Server-Side Template Injection Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's SSTI craft — engine fingerprinting and per-engine escape chains — as scoped experiments: detection uses inert arithmetic/marker probes, and RCE chains are named as impact classes to demonstrate on an owned instance, not weaponized against a target.

## Scope and prerequisites

Find where input is concatenated into a server-side template rather than passed as template data. Use an owned instance; prove execution with an inert marker (unique arithmetic result, benign file-read of a planted fixture, or an owned OOB callback), never a reverse shell or production file read.

Declare target, engine (if known), version, attempt budget and stop condition. Source-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

Template injection differs from XSS: the expression evaluates server-side. Vectors: any field rendered through a template (emails, PDFs, names, error pages, CMS blocks, notification templates). Classes: direct (output reflected), blind (no output; OOB/timing), and sandboxed (engine runs with a restricted context that must be escaped).

## Mechanism and observation

Trace input into the template compile/render path.

**Firstness:** Record the engine's response to an arithmetic probe and any error string. **Secondness:** State whether that field is meant to be literal data vs an evaluated expression. **Thirdness:** Infer the defect class only after an inert marker evaluates server-side under control.

## Abduction and refutation

**Mechanism hypothesis:** Input is compiled as template syntax, giving expression evaluation and, via engine internals, a path out of the sandbox to the host.

**Competing benign explanation:** The `{{7*7}}` rendered literally (not an engine); the `49` came from the app echoing input; the engine autoescapes and runs sandboxed with globals removed; the error is a generic parser error unrelated to evaluation.

## Deduction and controls

A literal string control must render unchanged; an injection evaluates the expression. `{{7*7}}` returning `49` (and `{{7*'7'}}` disambiguating Jinja2 `7777777` vs Twig `49`) is the discriminator. Predeclare the exact evaluated marker. A field that renders `{{7*7}}` verbatim is REFUTED for that field. A sandbox that blocks the escape is a PASS control.

## Induction: bounded laboratory procedure

Owned instance; inert markers only.

1. **Detection.** Inject a universal polyglot and arithmetic probes (`{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, `#{7*7}`, `@(7+7)`); observe which evaluates.
2. **Fingerprint.** Disambiguate by behavior and error signature: `{{7*'7'}}` (Jinja2 vs Twig), `{{config}}`/`{{_self.env}}` markers, Freemarker `<#assign>`, error strings (`jinja2.exceptions`, `Twig\Error`, `freemarker.core`, `org.apache.velocity`, `mako.exceptions`, Thymeleaf/Pebble classes).
3. **Context/sandbox mapping.** Enumerate reachable objects with inert expressions (e.g. Jinja2 `{{ ''.__class__.__mro__ }}` read-only) to see whether globals/builtins are exposed.
4. **Inert execution proof (owned).** Demonstrate reachability with a benign marker — read a planted fixture file, or trigger an owned OOB DNS callback — not `id`/reverse shell against a real target.
5. **Blind inference.** If no output: time-based (engine-correct sleep) or OOB callback; boolean/error inference character-by-character against a fixture.
6. **Control.** Confirm the literal control renders inert and, if present, the sandbox blocks the escape.

Record results including refutations. Keep finding and control status separate.

## Per-engine escape craft (impact classes to bound)

These are the real escape chains; carry them as domain knowledge and demonstrate reachability on an owned lab, not as weaponized commands:

- **Jinja2/Python** — MRO traversal to `__subclasses__`, or globals via `cycler`/`lipsum`/`namespace`/`request.application`/`config` to reach `os`/`subprocess`. Subclass indices vary by version — never hardcode; enumerate at runtime.
- **Twig/PHP** — `_self.env` (Twig 1.x), filter/map/sort/reduce callback abuse (`{{'id'|filter('system')}}`) in 2.x/3.x; `dump`, `file_excerpt` for info disclosure.
- **Freemarker** — `Execute` and `ObjectConstructor`/`ProcessBuilder` built-ins.
- **Velocity** — `Runtime.exec` via reflection. **Pebble** — reflection chain. **Thymeleaf** — SpEL via preprocessing (`__${...}__`).
- **Smarty/Mako/ERB/Handlebars/EJS/Pug/Nunjucks** — each has a documented eval/require path; fingerprint first, then map the specific one.

Chains to adjacent impact: SSTI → SSRF (metadata), SSTI → file read, SSTI → data exfil via chunked DNS. Treat each as a bounded reachability demonstration.

## Filter and WAF bypass craft

When characters are filtered, the escape mutates (test as filter-vs-engine differential): `|attr()` and bracket access when `.` is blocked; hex/`request.args` smuggling when `_` is blocked; string construction (`~` concat, `join`, `chr()`) when quotes are blocked; request-parameter smuggling to assemble `__class__` from pieces. Confirm the engine executed what the filter passed.

## Domain-specific failure modes

`{{7*7}}=49` can be coincidental app math — always disambiguate with the engine-specific probe. A sandboxed engine with removed globals may evaluate expressions but not reach the host; scope the claim. Subclass indices and global availability are version-specific; a chain that works on one version fails on another. Blind timing is confounded by load.

## Evidence and deliverable

Provide the injected field, the evaluated marker, the fingerprinted engine and version, the reachability proof (fixture read / OOB callback), and the sandbox state. Keep host data out of portable output. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered engines.

## Versions and tool limitations

Pin the template engine and version — behavior and escape paths are version-bound. `tplmap`/`SSTImap` default to active exploitation; run only in bounded mode against owned fixtures. No engine behavior was verified by this content; confirm the installed version first.

## Remediation and detection

Never compile untrusted input as a template; pass user data as bound variables to a precompiled template; use a logic-less engine or a hardened sandbox with globals/builtins removed; sanitize template-syntax metacharacters where templates must accept text. Add a regression asserting the marker renders literally. Detect template-syntax metacharacters and engine error signatures correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An inert marker evaluates server-side (fixture read or OOB callback) on an owned instance where the literal control does not: CONFIRMED; FAIL (scope to reachability shown). |
| Benign refutation | `{{7*7}}` renders verbatim or the sandbox blocks the escape: REFUTED for the tested field; PASS for the control. |
| Insufficient evidence | Arithmetic evaluates but no engine fingerprint or escape is shown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-ssti/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's engine-fingerprinting decision tree, per-engine escape chains and filter-bypass craft, re-expressed as owned-instance experiments with inert markers and version-aware reachability bounds, replacing reverse shells and production file reads with bounded execution proof.
