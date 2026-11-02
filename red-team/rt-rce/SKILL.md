---
name: rt-rce
description: "Red-team assessment of remote-code-execution boundaries: OS command injection, code injection/eval, file inclusion (LFI/RFI), SSTI, unsafe deserialization, unsafe YAML/config parsers, Expression Language injection, and upload-to-processing chains. Re-expressed as scoped reachability experiments proving the boundary with inert markers (unique OOB callbacks, benign fixtures) and negative controls instead of shells or production command execution."
---

# Remote Code Execution Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's RCE craft as scoped reachability experiments: it names the injection families and their detection, proving execution with an inert marker on an owned instance, never a reverse shell or a command against a target you do not own.

## Scope and prerequisites

Find every place where input reaches a code/command/template/deserialization/parser sink. Use an owned instance; prove execution with an inert, non-destructive marker — a unique OOB DNS/HTTP callback, a benign timed delay, or a planted-fixture read — never `id`/`whoami` exfiltration, file writes, or a shell on a real target.

Declare target, language/runtime and version, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED. OS command execution, shell and reverse-shell are impact classes to demonstrate by reachability on an owned lab, not to run live.

## Attack surface and classes

- **OS command injection** — input concatenated into a shell call.
- **Code injection / eval** — input passed to `eval`/`exec`/dynamic require.
- **File inclusion** — LFI (local file into execution path, log poisoning, PHP filter chains) and RFI (remote include).
- **SSTI** — template engine evaluation (see `rt-ssti` for engine depth).
- **Unsafe deserialization** — gadget-chain execution (see `rt-deserialization`).
- **Unsafe YAML/config parsers** — `yaml.load`, type-tag constructors.
- **EL injection** — Spring SpEL, OGNL, JSP EL.
- **Upload-to-processing** — uploaded file reaches an interpreter/converter (see `rt-file-upload`).

## Mechanism and observation

Trace input to the specific dangerous sink and the context (shell metacharacters? eval string? include path?).

**Firstness:** Record the inert marker's effect (callback received, measured delay, fixture content). **Secondness:** State that a safe design executes none of this and how the observation deviates. **Thirdness:** Infer the defect class only after the marker demonstrably runs under control.

## Abduction and refutation

**Mechanism hypothesis:** Untrusted input reaches an interpreter (shell, language eval, template, deserializer, parser) without the separation that would keep it data.

**Competing benign explanation:** The input is passed as an argv element (not through a shell) and metacharacters are inert; the delay was load, not `sleep`; the include path is allowlisted; the deserializer is type-restricted; the YAML loader is `safe_load`.

## Deduction and controls

A benign input runs normally (positive control); an injection changes execution. A confirmed RCE triggers the owned callback / measured delay / fixture read where the control input does not. Predeclare the exact marker. Argv-separated execution that renders metacharacters inert is a PASS control.

## Induction: bounded laboratory procedure

Owned instance; inert markers only.

1. **Baseline.** Submit benign input; capture normal behavior and (from source if available) the sink.
2. **Command injection.** Test separators inert to a safe caller: `;`, `|`, `&&`, `$(...)`, backticks, newline. Prove with an OOB callback or a bounded `sleep`, engine/OS-correct, repeated to exclude jitter — not data exfiltration.
3. **Code/eval.** Submit a language-appropriate inert expression (arithmetic marker, benign callback) and observe server-side evaluation.
4. **File inclusion.** LFI: read a planted fixture, test traversal and PHP filter-chain base64 of a benign file, log-poisoning only on an owned log. RFI: include from your owned server.
5. **SSTI / deser / YAML / EL.** Route to the specific sub-skill; prove with inert markers (fixture read, callback), not host commands.
6. **Control.** Confirm the benign input and, where present, the safe API leave the marker inert.

Record results including refutations. Keep finding and control status separate.

## Injection craft (leads; impact classes to bound)

- **Shell context** — separators, space bypasses (`${IFS}`), wildcard and variable-expansion tricks, Windows `|`/`&`/newline and PowerShell. Obfuscation is for WAF-differential testing, not for hiding intent.
- **File inclusion** — `php://filter/convert.base64-encode`, `data://`, log/session poisoning, `/proc/self/environ`, path traversal normalization.
- **EL/OGNL/SpEL** — `T(java.lang.Runtime)` reachability, OGNL context pollution (Struts-class CVEs).
- **YAML** — `!!python/object/apply`, Ruby/Java type tags; `yaml.load` vs `safe_load`.
These are the reachable-impact classes; demonstrate reachability on an owned lab and report the bound.

## Domain-specific failure modes

A delay can be load; repeat and use OOB to confirm. Argv execution (no shell) makes metacharacters inert even when the input looks injected. A sandbox or container may contain the execution — scope the blast-radius claim. WAF obfuscation bypass proves a filter gap, not necessarily execution; show both.

## Evidence and deliverable

Provide the sink, the class, the inert marker and its controlled effect (callback/delay/fixture), the control result, and the runtime/version. Keep host output out of portable reports. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered sinks.

## Versions and tool limitations

Pin the runtime, shell and parser versions — behavior is version-bound. Automated RCE tools default to shells; run only in bounded mode against owned fixtures. No sink behavior was verified by this content; confirm installed versions first.

## Remediation and detection

Avoid shells (use argv APIs), never `eval` untrusted input, allowlist include paths, use type-safe/`safe_load` parsers, restrict EL contexts, and drop privileges. Add a regression asserting the marker stays inert. Detect via process-spawn and outbound-callback telemetry correlated to the request ID.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An inert marker runs server-side (OOB callback / repeated delay / fixture read) on an owned instance where the control does not: CONFIRMED; FAIL (scope to reachability shown). |
| Benign refutation | Metacharacters inert under argv execution / `safe_load` / allowlist: REFUTED for the tested sink; PASS for the control. |
| Insufficient evidence | A single slow response, no OOB or repeat: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-rce/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's injection-family taxonomy and per-class detection/escalation craft, re-expressed as owned-instance reachability experiments with inert markers and negative controls, replacing shells and production command execution with bounded execution proof. For engine- and gadget-level depth, compose with `rt-ssti` and `rt-deserialization`.
