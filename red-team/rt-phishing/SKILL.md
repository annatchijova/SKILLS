---
name: rt-phishing
description: "Red-team assessment of phishing susceptibility and email-security controls via an authorized, consented simulation: pretext and lure design, delivery and mail-security evasion measurement, credential-capture and payload-execution landing pages, and click/report metrics. Re-expressed as a sanctioned simulation against consented recipients with benign tracked artifacts and detection/awareness measurement instead of a real credential-harvesting campaign."
---

# Phishing Simulation Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the simulation below.
This revision restores the upstream's phishing craft as a sanctioned, consented simulation: it designs lures and landing pages to measure susceptibility and mail-security coverage with benign tracked artifacts, not a real credential-harvesting campaign.

## Scope and prerequisites

A phishing assessment measures two things: whether mail security delivers the lure, and whether recipients click/submit/report. Run only as an authorized simulation with the client's sign-off and a defined recipient set (or an approved opt-out process). Use benign, clearly-tracked artifacts — a simulation landing page that records a click/submission without capturing real credentials or delivering real malware.

Declare the recipient scope, the mail-security stack, the simulation infrastructure, attempt budget, stop condition. Design-only review yields a hypothesis marked NOT TESTED.

## Attack surface and measurement targets

- **Delivery / mail security** — does SPF/DKIM/DMARC, the secure email gateway, and sandboxing block or deliver the lure?
- **Lure/pretext** — theme plausibility (compose with `social-engineering-plausibility`), sender spoofing/lookalike domain, urgency.
- **Landing page** — benign credential-capture simulation (records the submission event, not the password) or a benign "payload" that reports execution.
- **Human response** — click rate, submission rate, and crucially the report rate (did users report it?).

## Mechanism and observation

Send the simulated lure; measure delivery, click/submit, and report.

**Firstness:** Record delivery (reached the inbox?), the click/submission events (benign tracking), and reports to the security team. **Secondness:** State the expected controls (mail security blocks spoofed/lookalike lures; users report) and the deviation. **Thirdness:** Infer a susceptibility/control gap only after the measured rates are in.

## Abduction and refutation

**Hypothesis:** The organization is susceptible — mail security delivers the lure and/or users click/submit without reporting.

**Competing benign explanation:** DMARC/gateway blocks the spoofed sender; sandboxing detonates the link; users report at a high rate; the clicks came from security tooling scanning the link, not humans; the lure was unrealistic.

## Deduction and controls

A legitimate email is delivered and acted on normally (baseline). A confirmed gap shows the lure delivered and clicked/submitted with low reporting, where mail security or trained users would stop it. Predeclare delivery and the click/submit/report metrics; exclude automated link-scanner clicks. Mail-security blocking / high report rate are PASS controls.

## Induction: bounded simulation procedure

Consented recipients; benign tracked artifacts.

1. **Design.** Build a plausible, authorized lure and a benign landing page (records events, no real credential storage). Use a controlled sender/domain.
2. **Deliver.** Send to the scoped recipients; record which reached inboxes vs were blocked/quarantined.
3. **Measure.** Click rate, submission rate (benign), report rate; filter out security-scanner clicks (user-agent/timing).
4. **Mail-security coverage.** Note which controls (SPF/DKIM/DMARC, gateway, sandbox) blocked or passed the lure.
5. **Debrief.** Deliver awareness feedback; do not shame individuals.

Record results including refutations. Keep the susceptibility finding separate from the mail-security control score. No real credentials captured.

## Craft notes (leads)

The report rate is as important as the click rate — a workforce that clicks but reports fast is resilient. Mail-security evasion here is measured (does the gateway catch the lookalike/spoof?), not optimized to harm. Lookalike domains, display-name spoofing, and urgency are standard lure levers; realism must be plausible (see `social-engineering-plausibility`). Automated link scanners inflate click counts — filter them.

## Domain-specific failure modes

Scanner-generated clicks inflate the rate — filter by user-agent/timing. DMARC/gateway blocking the lure is a PASS, not a failed test. A high report rate is resilience even with some clicks. An unrealistic lure under-measures susceptibility. Capturing real credentials or delivering real malware is never appropriate — benign simulation only. Individual shaming is counterproductive and out of scope.

## Evidence and deliverable

Provide the lure, delivery results (per mail-security control), click/submit/report rates (scanner-filtered), and the awareness/remediation recommendations. No real credentials. Attach the recipient scope, consent basis, expected/observed, rival explanation (scanner clicks), falsifier, controls not exercised.

## Versions and tool limitations

Pin the mail-security stack and simulation platform. Delivery behavior is configuration-specific. No control behavior was verified by this content; run the sanctioned simulation to measure.

## Remediation and detection

Enforce SPF/DKIM/DMARC (reject), deploy a secure email gateway + sandboxing + lookalike-domain detection, provide ongoing awareness training with easy reporting (a report button), and measure report rate as a KPI. Add a recurring simulation cadence. Detect lookalike domains and spoofed senders.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The lure is delivered and clicked/submitted with low reporting where mail security or trained users would stop it: CONFIRMED susceptibility/control gap; FAIL (report rates). |
| Benign refutation | DMARC/gateway blocks it or report rate is high (and clicks were scanners): REFUTED; PASS for the control. |
| Insufficient evidence | Clicks unfiltered for scanners, or an unrealistic lure: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/social-engineering/offensive-phishing/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's lure/delivery/landing-page craft as a sanctioned, consented simulation measuring susceptibility and mail-security coverage with benign tracked artifacts and report-rate metrics, replacing real credential harvesting with bounded, ethical measurement. Composes with `social-engineering-plausibility`, `rt-social-engineering`, `rt-initial-access`.
