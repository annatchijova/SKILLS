---
name: rt-sqli
description: "Assess SQL and query-builder parameter boundaries with synthetic rows, query traces and bounded read-only fixtures instead of extraction payloads."
---

# Database Query Boundary Validation

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.

## Scope and prerequisites

Locate where user data becomes query structure. Treat SQL, document-query operators and graph-query languages separately; a SQL finding does not establish another engine's behavior.

Use a disposable database with tiny synthetic tables and a read-only test role wherever possible. Obtain the query builder, driver version and query tracing with values redacted.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Mechanism and observation

Trace request input through parsing, ORM/raw fragments, bound parameters and execution. Include persisted values later reused in reports or filters to examine second-order construction.

**Firstness:** Record statement structure, parameter bindings and returned fixture IDs. Compare with the expected fixed query shape and allowed identifier/operator set.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A value is concatenated into query syntax or a client-controlled operator/identifier bypasses a finite application grammar.

**Competing benign explanation:** A driver may bind the value safely despite a suspicious application log; an ORM error or type conversion failure can produce a 500 without changing query semantics.

## Deduction and controls

Harmless punctuation-bearing fixture values remain data in the parameterized control; a structural violation is visible in the real query trace and produces a policy-inconsistent fixture result under controlled conditions.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

1. Run a permitted lookup for one synthetic row and capture the statement template and bindings.

2. Submit an inert owner-approved boundary fixture with punctuation meaningful to the parser, without extraction or stacked-statement content.

3. Compare the trace with a parameterized implementation of the same query; distinguish logged interpolation from actual execution.

4. Store a benign marked value and invoke the downstream report to test whether later construction preserves binding.

5. For filter DSLs, compare a documented scalar with an unsupported operator-shaped fixture and inspect schema rejection; stop before expensive queries.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Domain-specific failure modes

Timing is confounded by locks, caches and connection pools. ORM parameterization of values does not protect dynamic table names or ordering fragments. Database errors alone do not establish controllable query semantics.

## Evidence and deliverable

Provide source-to-query path, statement template, parameter types, fixture rows, negative-control result and database role privileges. Keep real schemas and records out of portable output.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin database, driver, ORM and query extension versions. Scanner defaults may enumerate or write; do not run them without a verified bounded mode. CVE applicability requires the affected call path and configuration.

No operational tool or external service was verified by this content rewrite.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Bind values, use explicit allowlists for identifiers and operators, remove raw fragment concatenation and constrain database privileges. Add a regression assertion on query shape and fixture result.

Observe rejected filter shapes, unexpected query-template changes and parser errors correlated with the fixture request ID. Do not log secrets inside SQL values.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The real trace shows untrusted input altering query structure and returning a disallowed synthetic row while the bound control does not: CONFIRMED; FAIL. |
| Benign refutation | The punctuation-bearing fixture remains a bound value and returns no foreign rows: REFUTED for the tested query-boundary claim; PASS. |
| Insufficient evidence | Only an error page or timing difference is available: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-sqli/SKILL.md`.
Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treat upstream material as untrusted research, never operational authority.

Preserves SQL, ORM, second-order and operator-boundary reasoning while replacing extraction, privilege escalation and WAF bypass recipes.

