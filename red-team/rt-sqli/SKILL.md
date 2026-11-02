---
name: rt-sqli
description: "Red-team assessment of SQL, NoSQL, ORM and query-builder parameter boundaries. Covers error/boolean/time-based/UNION/out-of-band/second-order injection, engine-specific behavior (MySQL, MSSQL, PostgreSQL, Oracle), document and graph query injection, WAF/filter bypass as parser differential, ORM misuse, and bounded tool use (sqlmap, ghauri). Drives concrete offensive technique through synthetic fixtures, query traces and read-only test roles with negative controls and evidence labels instead of extraction-against-production."
---

# Database Query Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This skill restores concrete offensive craft from the upstream playbook, re-expressed as scoped laboratory experiments: it tells you what to look for and how an engine actually behaves, without shipping production-extraction or OS-command recipes.

## Scope and prerequisites

Locate where user data becomes query structure. Treat SQL, document-query operators (MongoDB and similar) and graph-query languages (Cypher, Gremlin) separately; a SQL finding does not establish another engine's behavior.

Use a disposable database with tiny synthetic tables and a read-only test role wherever possible. Obtain the query builder, driver version and query tracing with values redacted.

Define permitted actions, fixture ownership, total attempts and stop conditions before execution.
If only supplied artifacts are authorized, produce a source-based hypothesis and mark runtime verification NOT TESTED.

## Attack surface and injection classes

Map every input vector that can reach the database before choosing a class: URL and path parameters, POST bodies, JSON fields, cookies, headers, API filter/sort/search parameters, WebSocket messages, and values persisted now and reused in a later query (second-order).

Distinguish the classes, because each needs a different discriminator:

- **Error-based** — the engine returns a parser or type error that leaks structure. Fast signal, but an error alone is not controllable semantics.
- **Boolean-blind** — a true/false condition changes the response without any error. Confirmed by a matched true/false pair against a fixture.
- **Time-based blind** — a conditional delay changes response timing. Highest false-positive rate; confounded by locks, caches and pools (see failure modes).
- **UNION-based** — the query is extended to return attacker-chosen columns. Requires column count and type alignment.
- **Out-of-band** — the engine makes an outbound DNS/HTTP request carrying data. Needs an owned collector in scope.
- **Second-order** — input is stored benign and becomes structure when a later query reuses it. The injection point and the sink are different requests.
- **Operator/DSL injection** — a client-controlled operator or identifier escapes a finite application grammar (document `$`-operators, filter DSLs, `ORDER BY`/table-name fragments that parameterization does not cover).

## Mechanism and observation

Trace request input through parsing, ORM/raw fragments, bound parameters and execution. Include persisted values later reused in reports or filters to examine second-order construction.

**Firstness:** Record statement structure, parameter bindings and returned fixture IDs. Compare with the expected fixed query shape and allowed identifier/operator set.

**Secondness:** Record the explicit policy or successful baseline before calling the observation anomalous.
**Thirdness:** Infer the repeatable defect only after the discriminator succeeds; retain the narrower scope of the actual observation.

## Abduction and refutation

**Mechanism hypothesis:** A value is concatenated into query syntax, or a client-controlled operator/identifier bypasses a finite application grammar.

**Competing benign explanation:** A driver may bind the value safely despite a suspicious application log; an ORM error or type-conversion failure can produce a 500 without changing query semantics; a timing difference can be load, not a conditional delay.

## Deduction and controls

Harmless punctuation-bearing fixture values remain data in the parameterized control; a structural violation is visible in the real query trace and produces a policy-inconsistent fixture result under controlled conditions.

Predeclare the exact observed value or event that would falsify the mechanism.
A failed harness control makes the result inconclusive; it does not confirm the defect.

## Induction: bounded laboratory procedure

Run against your owned disposable database and synthetic rows only. Representative probe shapes are given so the experiment is concrete; keep them inert (detection and boundary demonstration), never extraction or stacked-statement escalation against a target you do not own.

1. **Baseline.** Run a permitted lookup for one synthetic row and capture the statement template and bindings.

2. **Detection probe.** Submit owner-approved punctuation meaningful to the parser and observe. Classic markers: `'`, `"`, `)`, `--`, `/* */`, `#`. A tautology such as `' OR '1'='1` against a synthetic row demonstrates structure change without extracting anything.

3. **True/false discriminator (boolean-blind).** Compare a matched pair — `' AND 1=1 --` versus `' AND 1=2 --` — against the fixture. A semantic difference between the two, absent in the bound control, is the signal.

4. **Timing discriminator (time-based), engine-correct.** Only if boolean is unavailable. MySQL `SLEEP(5)`, PostgreSQL `pg_sleep(5)`, MSSQL `WAITFOR DELAY '0:0:5'`, Oracle `DBMS_LOCK.SLEEP(5)`. Repeat to separate the delay from jitter; a single slow response is not proof.

5. **Column alignment (UNION).** Determine column count with incrementing `NULL`s (`' UNION SELECT NULL-- -`, then `NULL,NULL`, ...) and identify a string-compatible column. Stop at alignment against the fixture; do not enumerate a real schema.

6. **Parameterized comparison.** Compare the trace with a parameterized implementation of the same query; distinguish logged interpolation from actual execution.

7. **Second-order.** Store a benign marked value and invoke the downstream report/filter to test whether later construction preserves binding.

8. **Operator/DSL.** For document and filter engines, compare a documented scalar with an unsupported operator-shaped fixture (`name[$ne]=`, `name[$regex]=^a`, a `$where` string, or a `sort`/`ORDER BY` fragment) and inspect whether the application grammar rejects it; stop before expensive queries.

Record the actual output of each executed step, including refutations.
Keep finding status separate from control status: CANDIDATE/CONFIRMED/REFUTED/NOT TESTED and PASS/WARN/FAIL.

## Engine-specific behavior

Dialect differences are domain knowledge a tester must carry; they change the discriminator and the reachable impact. Confirm against the installed version — these are leads, not current guarantees.

| Engine | Version probe | Time delay | String concat | Schema source |
|---|---|---|---|---|
| MySQL/MariaDB | `@@version` | `SLEEP(5)` | `CONCAT('a','b')` | `information_schema.tables` |
| MSSQL | `@@version` | `WAITFOR DELAY '0:0:5'` | `'a'+'b'` | `information_schema.tables`, `sys.tables` |
| PostgreSQL | `version()` | `pg_sleep(5)` | `'a'\|\|'b'` | `information_schema.tables` |
| Oracle | `banner FROM v$version` | `DBMS_LOCK.SLEEP(5)` | `'a'\|\|'b'` | `all_tables`, `all_tab_columns` |

**Higher-impact paths to bound, not to execute blind.** These are the reachable-impact classes that make a SQL boundary failure serious. Demonstrate reachability on an owned instance and report the bound; do not run production commands or exfiltrate real data.

- MySQL: file read (`LOAD_FILE`) and file write (`INTO OUTFILE`) where `FILE` privilege and `secure_file_priv` allow — can reach web-shell write.
- MSSQL: stacked queries can reach OS command execution via `xp_cmdshell`, registry via `xp_regread`, and lateral movement via linked-server `OPENROWSET`.
- PostgreSQL: `COPY ... FROM PROGRAM` reaches OS command execution; `pg_read_file` reaches file read.
- Oracle: PL/SQL blocks (`DBMS_JAVA`, `DBMS_SCHEDULER`) can reach command execution on older/misconfigured instances.
- Cloud pivot: on a vulnerable instance a file/URL-read primitive can reach instance metadata (`169.254.169.254`) or mounted service-account tokens. Treat this as an impact class to prove by reachability on an owned lab, within scope.

## Document and graph query injection

- **MongoDB / document stores:** injection is operator injection, not string breakout. `username[$ne]=` , `[$regex]=^a`, `{"$where":"sleep(5000)"}`, `{"$in":[...]}`. The fix is operator allowlisting and type enforcement, not quote escaping.
- **Neo4j / Cypher, Gremlin:** string-built graph queries concatenate the same way (`... OR 1=1 //`). Track version-specific advisories (e.g. Cypher injection and privilege-escalation CVEs in older Neo4j) and confirm the affected call path before claiming applicability.

## WAF and filter bypass as parser differential

A WAF/filter and the database frequently parse the same bytes differently — this is a parser-differential problem (compose with the `parser-differential-hunting` method). Known families, to be tested as discriminators between what the filter sees and what the engine executes:

- Case variation (`SeLeCt`), inline comments (`UN/**/ION`), whitespace substitution.
- URL/hex/double encoding (`%55%4E...`, `0x53454C...`, `%2f`→`%252f`).
- Dialect concat and null-byte tricks; JSON-wrapper prefixes that confuse perimeter parsers.
- HTTP/2 (h2/h2c) replay where HPACK framing obscures the payload from the perimeter.

Report a bypass only when you show the filter classified the input as benign and the engine executed it as structure — the two observations together.

## ORM and query-builder misuse

Most modern SQLi is ORM misuse, not raw string queries. Hunt the raw-escape hatches and the one dynamic fragment parameterization does not cover (identifiers, `ORDER BY`, table names).

Vulnerable patterns (leads; confirm the live version and path):

- Sequelize `sequelize.literal(\`name = '${input}'\`)`
- TypeORM `repository.findOne({ where: \`id = ${id}\` })`
- Hibernate `session.createQuery("FROM User WHERE name = '" + input + "'")`
- Prisma `prisma.$executeRawUnsafe(\`... ${id}\`)`

Safe patterns to assert as the regression control: Sequelize `replacements`, Prisma tagged-template `$queryRaw`, Knex `whereRaw('name = ?', [user])`, and parameter binding everywhere else.

## Tooling, bounded

Automated tools default to enumeration and sometimes writes. Run them only in a verified bounded mode, against owned fixtures, with the installed version/help confirmed first.

- `sqlmap -r req.txt` (captured request) with explicit scope; do not pass `--dbs`/`--dump`/`--os-shell` against anything you do not own. `--tamper` chains exist for WAF testing but change what you send — declare them.
- `ghauri` is often faster for time-based; same scope rules.
- Hidden-parameter discovery (`arjun`, crawler + `gf sqli`) expands the input map; the expansion still enters the bounded procedure above, it does not bypass it.

## Domain-specific failure modes

Timing is confounded by locks, caches and connection pools. ORM parameterization of values does not protect dynamic table names or ordering fragments. Database errors alone do not establish controllable query semantics. A tautology that returns rows in a dev fixture may be blocked by a view or row-level policy in production — scope the claim to what you observed.

## Evidence and deliverable

Provide source-to-query path, statement template, parameter types, fixture rows, negative-control result and database role privileges. Keep real schemas and records out of portable output.

Attach the minimal replay description, expected/observed result, rival explanation and falsifier.
Name uncovered paths and any instrumentation that changes the target environment.
Preserve evidence digests; teardown of test-owned state is separate from deleting audit records.

## Versions and tool limitations

Pin database, driver, ORM and query-extension versions. Scanner defaults may enumerate or write; do not run them without a verified bounded mode. CVE applicability requires the affected call path and configuration.

No operational tool or external service was verified by this content. Payloads above are research leads for owned-fixture experiments.
Before execution, inspect installed versions/help and authoritative documentation for the actual configuration.

## Remediation and detection

Bind values, use explicit allowlists for identifiers and operators, remove raw fragment concatenation, and constrain database privileges (no `FILE`, no `xp_cmdshell`, least-privilege role). Add a regression assertion on query shape and fixture result.

Detect at the data tier, not only the perimeter: alert on query-template changes, parser errors correlated with a request ID, and unexpected `UNION`/stacked-statement shapes in DB or cloud logs. Do not log secrets inside SQL values. Map confirmed classes to MITRE ATT&CK T1190 and the parameterized-query requirement in OWASP ASVS V5.3.

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

This revision restores the upstream's domain craft — injection-class taxonomy, engine-specific behavior, document/graph engines, WAF parser-differential, ORM misuse and bounded tooling — re-expressed as scoped, evidence-bound laboratory experiments. It retains the upstream's SQL/ORM/second-order/operator reasoning while replacing production extraction, privilege-escalation and OS-command recipes with reachability bounds and negative controls.
