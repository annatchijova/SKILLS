---
name: dont-fall-in-love-with-the-bug
description: "Do not stop at a reproducible symptom — the gate that makes you earn the report before writing it. Name the broken invariant and its layer, sweep for variants, attack the fix you expect the maintainer to ship, map the real blast radius across shipped clients and versions, and calibrate severity against a named comparable advisory. Use whenever a finding is labeled CONFIRMED or EXPLOITABLE, a bounty report is being drafted or reviewed, or an obvious one-line fix is being assumed. Trigger on 'it reproduces', 'ready to submit', 'write it up', 'is this exploitable', or an assumed quick fix."
---

# Don't fall in love with the bug

The failure mode this prevents: you stop at the symptom, submit, and the maintainer does the variant/bypass pass you skipped — finding more than you reported. A confirmed repro is the *middle* of the work, not the end. This gate makes the agent earn the report.

## Trigger
A finding is reproducible and about to be written up or submitted; a result is labeled CONFIRMED/EXPLOITABLE; a bounty report is being drafted or reviewed; or an "obvious" one-line fix is being assumed.

## Steps (the gate — do not draft the report until each is answered)
1. **Root cause vs symptom.** Name the invariant that is actually broken, and at what layer. If you can only describe *what happens*, not *what guarantee fails*, you are still at the symptom — keep going.
2. **Variant sweep.** Same invariant, other call sites / headers / params / entry points. Run `variant-analysis`. List what you checked, *including* the ones that did not reproduce.
3. **Bypass the fix.** Write the patch you expect the maintainer to apply — then attack *that*. If a redirect, an encoding, or a second entry point walks around the obvious one-liner, that bypass belongs in your report now, not in their follow-up.
4. **Blast radius.** Who is actually affected? Which shipped clients / versions / configs reach this sink? A concrete downstream (a real client that sets the vulnerable policy in the default pipeline) turns "theoretical" into "reachable" and is the difference between triage bins.
5. **Severity, calibrated against a named gemelo.** Do not claim a number from a vibe. Anchor to a comparable public advisory (a GHSA/CVE with a CVSS) and state why yours sits above or below it. Use the comparable as calibration, not as the pitch.
6. **Only now, write it.** Hand the draft to `daubert-defensible-writing` so certainty is earned and limitations are stated plainly.

## Verification
- The report answers, before submission: root cause (invariant + layer), at least one recorded variant-sweep result, an explicit bypass-the-fix analysis, named affected clients/versions, and a severity with its named comparable.
- Anything you did *not* check is stated, not hidden.
- Nothing carries CONFIRMED/EXPLOITABLE without an independent repro (defers to `red-team-auditing`).

## Composes with
`variant-analysis` (step 2), `red-team-auditing` (earn the label), `attack-surface-triage` (reachability), `audit-before-patch` (validate the assumed fix against live code), `daubert-defensible-writing` (the writeup).
