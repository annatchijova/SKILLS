---
name: deception-signal-quality
description: Design deception so that a triggered decoy is a true positive by construction — a honeytoken, honeypot, or canary earns its keep only if nothing legitimate ever touches it, which turns "someone touched it" into signal with a near-zero false-positive rate, the inverse of every noisy detection you own. Use whenever deception is being built or evaluated: "let's plant a honeytoken", "set up a honeypot", "canary tokens", "decoy credentials / files / AWS keys", "tripwire", "we deployed a deception grid", "why is our honeypot noisy", "fake admin account to catch attackers". Sibling of detection-engineering (deception is a detection whose benign-twin rate is engineered to zero) and dual-use-behavior-adjudication (its mirror image: a decoy is built to have no legitimate use, so no adjudication is needed); it judges decoy placement and signal quality. It does not run offensive deception against third parties, and never trusts a decoy whose legitimate-access paths were not eliminated first.
---

# Deception Signal Quality

Most detection is a fight against base rates: the behavior you alert on is also
something legitimate users do, so every rule drags a false-positive tail and every
analyst learns to dismiss. Deception inverts the problem. A honeytoken, decoy account,
or canary file is built to have **no legitimate purpose whatsoever** — so the day
anything touches it, the base rate of benign access is (by design) zero, and the
signal is a true positive without adjudication. That inversion is the entire value, and
it is also the entire fragility: the moment a legitimate process, a backup job, a
vulnerability scanner, or a curious admin can reach the decoy, you have rebuilt a noisy
detection and lost the one property that made deception worth deploying.

Two symmetric failure modes:

- **The polluted decoy.** A honeypot the internal scanner probes nightly, a
  "fake" credential that a config-management tool reads, a canary file in a path the
  backup crawls. It fires constantly on benign access, trains dismissal, and when a real
  intruder finally trips it, the alert is in the same ignored bucket as the noise. A
  noisy honeypot is worse than none — it consumed attention *and* taught the team to
  ignore the exact channel that mattered.
- **The decoy that no attacker will ever reach (or believe).** A honeytoken buried where
  no lateral-movement path leads, or so obviously fake (`fake_password_DO_NOT_USE`) that
  any competent adversary steps around it. Zero false positives *and* zero true
  positives is not a detection; it is decoration.

The through-line: deception's power is a *manufactured absence of benign access*.
Protect that absence, place the decoy where an attacker will actually go, and make it
credible enough to be taken.

Composes with the library:

- **detection-engineering** — a decoy is a detection whose benign-twin rate you engineer to zero instead of budgeting for; the deploy/volume/tuning discipline still applies
- **dual-use-behavior-adjudication** — its exact inverse: that skill adjudicates signals with real benign explanations; a good decoy is defined by having none, so a hit needs no adjudication — which is why polluting it is so costly
- **forensic-logging-design** — a canary is only as good as the log that captures the touch; instrument the trigger and prove it records
- **honest-degradation** — a decoy of unproven placement/credibility is a WARN ("deployed, not validated"), not a working control
- **assume-breach-modeling** — placement follows the attacker's reachable paths; put the token where a breached foothold actually leads

---

## Step 1 — Eliminate every legitimate access path before deploying

The design work is subtractive: prove that nothing benign will ever touch this decoy,
because that proof is what converts a touch into signal.

- **Enumerate who and what could reach it** — users, service accounts, scanners, backup
  agents, config management, monitoring, indexing, EDR file-walkers. Each is a potential
  benign trigger.
- **Remove or exclude them** — the decoy sits outside the scanner's scope, the backup's
  crawl, the config tool's path. A honeytoken in a credential store must be one no
  automation reads; a decoy file in a location no legitimate job traverses.
- **If you cannot eliminate benign access, do not deploy it as a zero-FP tripwire.** A
  decoy with residual legitimate access is a normal detection with a false-positive
  budget — treat it as such (`detection-engineering`) and stop calling it high-fidelity.

This step is the whole skill. A honeytoken's fidelity is exactly the completeness of
this elimination.

---

## Step 2 — Place it where a real intruder will actually go

Zero false positives is necessary, not sufficient; the decoy must sit on an attacker's
path:

- **Follow the intrusion, not your intuition** — decoy credentials in memory/credential
  stores an attacker will dump; canary AWS keys in a `.env`/config an attacker will
  read; a decoy admin account in the directory an attacker will enumerate; honey files
  named like the crown jewels an attacker will exfiltrate. Let `assume-breach-modeling`
  tell you where a foothold leads.
- **Cover the technique, not just the asset** — a honeytoken that fires on credential
  reuse tests a specific adversary behavior; place it so that the *action you want to
  catch* (lateral movement, dumping, enumeration) necessarily touches it.

A decoy nothing benign touches and no attacker reaches is a perfectly clean signal that
never fires — measure both, not just the false-positive side.

---

## Step 3 — Make it credible; discard the obvious fake

An adversary who recognizes the decoy routes around it, converting a tripwire into a
map of where your defenses are:

- **Blend with the real** — naming, age, contents, and access history should match
  genuine assets. A honey account with a login history and a plausible name beats
  `honeypot01`. A canary document should look like the thing it imitates.
- **Beware the tell** — decoys that are too perfect, too isolated, or carry telltale
  monitoring artifacts can be fingerprinted. Credibility is itself an arms race; assume
  a competent adversary checks.
- **Do not over-index on the sophisticated attacker** — many intrusions are automated or
  hurried and will grab an imperfect decoy; credibility raises the catch rate, it is not
  all-or-nothing.

---

## Step 4 — Instrument the trigger and prove it captures

The decoy is only as good as the alert it raises:

- **Log the touch with the context you need** — source, identity, time, and enough to
  pivot into a response (`forensic-logging-design`). A canary that fires into a log no
  one reads is a tree falling in a forest.
- **Route the hit as high-fidelity** — because it is a true positive by construction, a
  decoy trigger deserves a different, louder path than the general alert queue
  (`alert-triage-economics`); do not let it queue behind the noise it was meant to escape.
- **Validate the trigger before you trust it** — actually touch the decoy in a test and
  confirm the alert fires and carries the context. An untested tripwire is a WARN, not a
  control (`honest-degradation`).

---

## Step 5 — Grade the deception honestly

State what the decoy does and does not cover:

- **"Deployed" is not "validated."** Until you have proven benign access is eliminated
  (Step 1), placement is on an attacker path (Step 2), and the trigger fires and logs
  (Step 4), the honest status is WARN, not PASS.
- **Report the coverage, not just the presence** — which techniques this deception grid
  would catch and which it would not. A honeytoken catches credential theft, not a
  quiet data read elsewhere; do not let a decoy imply blanket coverage.

---

## The one-line test

If any legitimate user, job, scanner, or backup could touch your decoy, it is not a
high-fidelity tripwire — it is a noisy detection you mislabeled, and its first real hit
will die in the same queue as its false ones. Prove the benign-access rate is zero, or
budget for it like any other rule.
