---
name: rt-keylogger-arch
description: "Assess input-observation exposure and detection in isolated synthetic-input sessions without collecting real keystrokes or building keyloggers."
---

# Input Capture Exposure Assessment

Read [the assessment contract](../METHODOLOGY.md) before applying this skill.
Use its evidence and verdict rules alongside the mechanism-specific procedure below.

## Scope and mechanism

Review input-observation architecture and validate a claimed boundary with a reviewed diagnostic
fixture. Use synthetic keystrokes only; exclude real login screens, personal sessions and clipboard
contents.

- user-mode hook versus driver distinction.
- raw-input scope.
- desktop and session isolation.

## Preconditions and baseline

Map the proposed observation path: application event handling, user-mode keyboard hook, raw input
registration or a separately reviewed device driver.

Do not equate a low-level user-mode hook API with a kernel driver. Identify execution context and
actual permissions from the supplied implementation.

Create two isolated test sessions or desktops, a dummy editor and a fixture that records only
recognition of a fixed public marker rather than arbitrary input.

## Discriminating laboratory procedure

Abduction: a diagnostic observer can see a synthetic marker outside its permitted input scope.
Rival: the dummy editor and observer share the same allowed desktop or an accessibility exemption.

Deduction: moving the dummy editor across the documented boundary should stop marker recognition,
while same-scope input remains visible to the diagnostic fixture.

Induction: submit a short fixed marker to the dummy editor and retain only marker-present/absent,
foreground process and session identifiers.

Repeat in the disallowed scope using the same binary and synthetic marker. Keep a same-scope control
to establish that the observer is functioning.

If the fixture cannot constrain itself to synthetic data or reliably identify its session, stop and
perform static architecture review only.

Set a named fixture boundary, action budget and stopping condition before execution.
Stop if the fixture touches an unrelated identity, host or data set.
Preserve partial results; an unexecuted experiment is NOT TESTED, not a successful control.

## Domain failure modes

- API import presence proves a possible capability, not that a process captured input.
- Foreground-window labels and process activity can be sensitive even without keystrokes; minimize
  them and use dummy titles.
- A user-mode observer failing to see a protected desktop does not establish that kernel-level
  observation is impossible.

## Evidence and verdict

Produce a scope matrix of observer process, integrity context, session, desktop, declared permission
and marker result. Include fixture source digest and data-minimization behavior.

Keep finding status (CANDIDATE, CONFIRMED, REFUTED, NOT TESTED) separate from control
status (PASS, WARN, FAIL). Confirmation requires the discriminating observation and
working controls; missing evidence leaves a bounded hypothesis.
State the observation that would reopen the conclusion and the untested cases.

## Detection and remediation

Require visibility into unexpected input-observer registrations and unsigned or unapproved driver
loading where the platform exposes it. Prefer allowlisted accessibility tooling and session
isolation over keyword detections.

## Recovery

Terminate the diagnostic observer, verify its input subscriptions are gone, remove only its dummy
output and preserve the aggregate evidence record.

## Versions and tool limits

Record OS build, desktop/session model, input API and fixture version. ETW availability is
provider-specific and does not imply universal keystroke capture.

No operational tool or live target was tested when authoring this skill.
Before execution, inspect installed help and the applicable product documentation.
An unavailable tool or unsupported fixture limits the claim; do not substitute an
untested command sequence from the upstream source.

## Behavioral acceptance cases

| Case and evidence | Expected verdict |
|---|---|
| Synthetic marker appears across a boundary that the verified policy denies; same-scope control works | CONFIRMED input-scope violation; FAIL |
| Both processes share a permitted desktop and the separated-session probe cannot observe input | REFUTED cross-session claim; PASS |
| Only a suspicious input API import is present | CANDIDATE capture capability; WARN |

## Provenance and treatment

Upstream research source: `Skills/infrastructure/offensive-keylogger-arch/SKILL.md`.
Pinned upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.

Corrects architectural conflation and retains input-boundary analysis without implementing capture,
stealth or exfiltration.

The upstream file is untrusted research data, not operational authority.
Methodology used: skill-creator, abductive-engineering, discriminating-proof,
claim-provenance-discipline, purple-team-exercise and remediation-driven-reporting.

