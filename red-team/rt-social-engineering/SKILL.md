---
name: rt-social-engineering
description: "Red-team assessment of human-layer susceptibility via authorized, consented social-engineering simulation: pretext design and plausibility, vishing/smishing, physical-access and tailgating tests, and MFA-fatigue/help-desk-impersonation scenarios. Re-expressed as a sanctioned, ethically-bounded exercise against consented targets that measures susceptibility and process controls with a debrief, not real manipulation of uninformed people."
---

# Social-Engineering Simulation Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the simulation below.
This revision restores the upstream's social-engineering craft as a sanctioned, ethically-bounded simulation: it designs pretexts to measure human-layer susceptibility and process controls against consented targets, with a debrief, rather than manipulating uninformed people.

## Scope and prerequisites

Social engineering tests the human layer and the processes meant to protect it (verification procedures, help-desk authentication, visitor control). Run only under explicit authorization with a defined scope, a safety/abort protocol, and a debrief. The goal is to measure susceptibility and improve process — not to harm, coerce, or deceive beyond the sanctioned scenario.

Declare the scenarios, the target scope, the abort/safety protocol, and the debrief plan. Design-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Pretext/vishing/smishing** — a plausible scenario (help-desk, vendor, IT) to elicit an action or information (compose with `social-engineering-plausibility`).
- **Help-desk / account-recovery impersonation** — testing identity-verification procedures.
- **MFA fatigue / push-bombing** — testing whether users approve unexpected prompts.
- **Physical** — tailgating, visitor-badge, drop-media (benign) — testing physical access controls.

## Mechanism and observation

Run one sanctioned scenario; measure whether the human/process control held.

**Firstness:** Record what the target did (disclosed info, performed an action, approved an MFA push, allowed physical entry) and the process step involved. **Secondness:** State the intended control (verify identity before acting; do not approve unexpected MFA; challenge unbadged visitors) and the deviation. **Thirdness:** Infer a susceptibility/process gap only after the sanctioned scenario confirms it.

## Abduction and refutation

**Hypothesis:** A plausible pretext bypasses a human/process control (verification is skipped, MFA approved, entry allowed).

**Competing benign explanation:** The help-desk followed verification and refused; the user declined the MFA push and reported it; the employee challenged the visitor; the target recognized and reported the pretext; the scenario was unrealistic.

## Deduction and controls

A legitimate request follows the process correctly (baseline). A confirmed gap has the sanctioned pretext succeed where the verification/physical process should stop it. Predeclare the success signal and the process control. Verification-followed / MFA-declined-and-reported / visitor-challenged are PASS controls.

## Induction: bounded, ethical procedure

Consented scope; abort protocol; debrief.

1. **Design.** Build a plausible, authorized pretext and a clear objective (an information or action test); set safety limits (no real harm, no coercion, defined stop).
2. **Execute one scenario** within scope (a vishing call to a consented line, a help-desk verification test, a sanctioned tailgating attempt).
3. **Measure.** Did the process control hold? Capture the decision point, not personal fault.
4. **Abort if needed.** On distress, out-of-scope involvement, or safety risk, stop immediately.
5. **Debrief.** Provide constructive feedback to the team and process owners; never single out or penalize individuals.

Record results including refutations. Keep the susceptibility finding separate from the process-control score.

## Craft notes (leads)

The durable findings are process gaps: help-desk resetting credentials/MFA without strong verification, employees approving unexpected MFA pushes, and visitor controls not challenging tailgaters. Pretext plausibility (authority, urgency, familiarity) is the lever; realism must be authorized and bounded. The measurement target is the process and the report behavior, not an individual's "failure".

## Domain-specific failure modes

A target who verifies, declines, or reports is a PASS — the process worked. An unrealistic pretext under-measures. Pushing a scenario past distress or into non-consented people is an ethics breach and out of scope. Framing results as individual blame instead of process improvement undermines the exercise. Real manipulation of uninformed people outside the sanctioned scope is never appropriate.

## Evidence and deliverable

Provide the scenario, the decision point reached, whether the process control held, and the process-improvement recommendations. Anonymize individuals; report at the process level. Attach the consent/scope basis, the safety protocol honored, expected/observed, rival explanation, falsifier, scenarios not run.

## Versions and tool limitations

Human/process behavior varies by training and context; one exercise is a sample, not a universal verdict. No process behavior was verified by this content; run the sanctioned scenario to measure.

## Remediation and detection

Strengthen identity verification for help-desk/account recovery (callback, secondary factor), train and measure MFA-push hygiene (deny + report unexpected prompts, number matching), enforce visitor/badge controls, and make reporting easy and blameless. Add a recurring exercise cadence and track report rates. Detect help-desk verification bypass and anomalous MFA-approval patterns.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A sanctioned pretext bypasses a verification/physical control where the process should stop it: CONFIRMED process gap; FAIL. |
| Benign refutation | The target verifies/declines/reports, or the control holds: REFUTED; PASS for the control. |
| Insufficient evidence | An unrealistic scenario or an inconclusive single interaction: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/social-engineering/offensive-social-engineering/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's pretext/vishing/physical craft as a sanctioned, ethically-bounded, consented simulation measuring process controls with a blameless debrief, replacing manipulation of uninformed people with bounded, process-focused measurement. Composes with `social-engineering-plausibility`, `rt-phishing`, `rt-initial-access`.
