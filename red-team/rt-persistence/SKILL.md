---
name: rt-persistence
description: "Blue/purple-team assessment of persistence-mechanism detectability and an authorized engagement's reversible foothold: autostart/registry/service/scheduled-task, account and credential persistence, and OS-specific footholds, understood so defenders can detect them. Re-expressed as scoped experiments on an owned host that install a benign, reversible marker-persistence and measure whether endpoint controls detect and allow removal, not a stealth-persistence playbook."
---

# Persistence Detectability Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the detection exercise below.
This revision reframes the upstream's persistence material toward detection and reversibility: it names the mechanism categories so a defender can recognize them and installs only a benign, reversible marker on an owned host to measure detection, rather than teaching stealth persistence.

## Scope and prerequisites

Persistence re-establishes access across reboots/logins. The defensive question is whether each mechanism is detected and removable. In an authorized engagement, any persistence must be benign (a marker that calls an owned collector, not a backdoor), reversible, logged, and deconflicted, and removed at the end. Use an owned host.

Declare the host, the endpoint controls, the benign marker, attempt budget, stop condition. Config-only review yields a hypothesis marked NOT TESTED.

## Mechanism categories (as detection targets)

- **Autostart** — registry Run keys, startup folder, login items, launch agents/daemons, systemd units, cron.
- **Services/tasks** — Windows services, scheduled tasks; Linux timers.
- **Account/credential** — added accounts, SSH `authorized_keys`, API keys, modified sudoers.
- **Component hijack** — DLL search-order/COM hijack, `LD_PRELOAD`, plugin/extension.
- **Boot/firmware** — bootkit-class (understanding only; do not implement).

## Mechanism and observation

Install one benign marker-persistence, then measure detection and removability.

**Firstness:** Record the mechanism installed, whether it survived a reboot/login (marker callback), and which control alerted. **Secondness:** State the intended control (autostart/service/task creation is logged and alertable; changes are inventoried) and the deviation. **Thirdness:** Infer a detectability gap only after a benign mechanism survives undetected where a hardened host would catch it.

## Abduction and refutation

**Hypothesis:** A persistence mechanism can be installed without detection (a monitoring gap).

**Competing benign explanation:** EDR/auditing logs the autostart/service/task creation and alerts; file-integrity monitoring catches the change; the mechanism requires privileges the principal lacks; application allowlisting blocks the payload; the change is inventoried and flagged as drift.

## Deduction and controls

A clean host has a known-good autostart/service baseline (positive control). A confirmed gap has the benign mechanism survive a reboot/login undetected where a monitored host would alert. Predeclare the marker-survival signal and the expected alert. Autostart/service/task auditing / FIM / allowlisting detecting it are PASS controls.

## Induction: bounded procedure

Owned host; benign reversible marker; deconflicted.

1. **Baseline.** Record the autostart/service/task/account inventory.
2. **Install one benign mechanism** (e.g. a Run key / scheduled task / cron that calls an owned collector on boot — no backdoor).
3. **Verify survival.** Reboot/re-login; confirm the marker fired.
4. **Measure detection.** Did EDR/auditing/FIM alert on the creation? Would an inventory diff catch it?
5. **Score & remove.** PASS/WARN/FAIL; then remove the mechanism and confirm cleanup.
6. **Control.** Confirm a monitored host would have alerted.

Record results including refutations. Keep finding status separate from the control score. The mechanism is benign and removed at the end.

## Craft notes (leads)

Autostart (Run keys, startup, launch agents, systemd, cron) and scheduled tasks/services are the highest-volume categories and the most inventoriable — baseline-diffing catches them. Account/key persistence (new accounts, `authorized_keys`, sudoers) is detectable by account/FIM auditing. Component hijacks (DLL search order, `LD_PRELOAD`, COM) are subtler but have known telemetry. Boot/firmware persistence is understanding-only here.

## Domain-specific failure modes

An undetected benign mechanism is a real gap only if the control that should catch it exists and did not — confirm the expected alert. A mechanism needing privileges the principal lacks is not installable. Allowlisting can block the payload even if the autostart entry is created. Installing a real backdoor, or leaving persistence behind, is never appropriate — benign and removed.

## Evidence and deliverable

Provide the mechanism, the survival proof (marker callback post-reboot), the detection result, the removability confirmation, and the control score. Keep to the owned host with a benign marker. Attach minimal replay, expected/observed, rival explanation, falsifier, mechanisms not assessed, and cleanup confirmation.

## Versions and tool limitations

Pin the OS build and endpoint-control versions — mechanisms and telemetry are platform-specific. No host behavior was verified by this content; reproduce on the owned host first.

## Remediation and detection

Audit and alert on autostart/service/task/account changes, deploy file-integrity monitoring and configuration-drift detection, application allowlisting, and least privilege (persistence needs rights). Baseline and diff the autostart inventory. Add a regression that the benign mechanism's creation alerts. Detect component-hijack telemetry (DLL/`LD_PRELOAD`/COM).

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A benign mechanism survives a reboot undetected where a monitored host would alert: CONFIRMED detectability gap; control FAIL. |
| Benign refutation | EDR/auditing/FIM/allowlisting detects or blocks it: REFUTED; control PASS. |
| Insufficient evidence | Installed but survival or expected-alert not confirmed: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/post-exploitation/offensive-persistence/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision reframes the upstream's persistence-mechanism catalog as a detectability-and-reversibility exercise on an owned host with a benign, removed marker and PASS/WARN/FAIL scoring, replacing a stealth-persistence playbook with detection measurement. Composes with `forensic-persistence`, `detection-engineering`, `rt-advanced-redteam`.
