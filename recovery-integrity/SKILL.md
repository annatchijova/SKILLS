---
name: recovery-integrity
description: Treat a backup you have not proven restorable and untampered as a hope, not a recovery plan — because the backup is inside the blast radius (same domain credentials, same network, same admin), and ransomware operators delete or encrypt backups before they detonate, so "we have backups" answers a question you did not ask. Use whenever recovery or backups are the subject: "we have backups so we're fine", "ransomware recovery", "can we restore", "backup strategy", "how fast can we recover", "are the backups safe", "disaster recovery plan", "immutable backups", "we never test restores". Sibling of honest-degradation (an unverified restore is a WARN, not a PASS) and tamper-evident-audit-chain (proving the backup was not altered); it audits the recoverability claim. It does not run the restore or build the backup system, and never accepts "the backup job succeeded" as evidence that recovery works.
---

# Recovery Integrity

"We have backups" is the answer to "did the backup job run." It is not the answer to
"can we recover," and the gap between those two questions is where organizations
discover, mid-ransomware, that their recovery plan was a hope with a cron schedule. A
backup is not a recovery until it has been *proven restorable* and *proven untampered* —
and both proofs are routinely skipped because the backup job's green checkmark feels
like one.

The reframe: **the backup is a target, and it is inside the blast radius.** A modern
ransomware operator's first move is not to encrypt — it is to find and destroy the
backups, because backups are the one thing that makes the ransom optional. If your
backups are reachable with the same domain admin credential that the attacker now
holds, on the same network, retained on a system they can log into, then they are not a
safety net; they are line one of the attacker's checklist.

The failure modes:

- **The untested restore.** Backups run green for two years; the first actual restore
  attempt, during the incident, fails — wrong scope, corrupted media, a dependency not
  captured, an encryption key that was itself only stored in the thing you are trying to
  restore.
- **The backup in the blast radius.** Online, credential-reachable backups get
  encrypted or deleted alongside production. "We had backups" becomes "we had backups
  until Tuesday."
- **The tampered restore.** You restore successfully — from a point *after* the
  attacker was already inside — and you have faithfully recovered the compromise. A
  restore is only clean if you can trust the point it came from.

Composes with the library:

- **honest-degradation** — an unverified restore is a WARN; "backups exist" reported as "we can recover" is the overclaim
- **tamper-evident-audit-chain** — proving a backup was not altered (and that its restore point predates the compromise) needs integrity you can verify
- **assume-breach-modeling** — assume the attacker holds domain admin; are the backups reachable from that position?
- **credential-material-triage** — the credential that can reach/delete the backups is the one whose blast radius includes your recovery
- **containment-under-uncertainty** — recovery timing depends on knowing when the compromise started; restoring to a bad point re-infects

---

## Step 1 — Is the backup reachable from the compromise?

Before anything about media or schedules, run `assume-breach-modeling`: assume the
attacker holds the highest privilege in the environment (domain admin, cloud admin) as
of now. From that position:

- Can they *reach* the backups (same network, same directory, mapped share)?
- Can they *authenticate* to the backup system (same credentials, same SSO, a service
  account they captured)?
- Can they *delete or encrypt* them (write access, admin on the backup server, API keys
  to the backup cloud)?

If the answer to all three is yes, the backups share the fate of production and are not
a recovery plan. The defense is separation: offline/air-gapped copies, immutability
(write-once, time-locked object lock), and credentials for the backup system that are
*not* the credentials that got compromised.

---

## Step 2 — Proven restorable, or it does not exist

A backup that has never been restored is Schrödinger's recovery — both present and
absent until observed, and the incident is the worst time to open the box. Require
actual evidence:

- **Test restores, on a schedule, to a clean environment** — not "the job succeeded,"
  but "we restored it and it came up." The metric is a completed restore, the way
  `detection-engineering` requires a rule to have fired on a true positive.
- **Scope completeness** — does the backup capture everything a restore needs: the data,
  the config, the schema, the dependencies, and the keys? A classic dead-end is backups
  encrypted with a key stored only inside the system you are restoring.
- **Restore-time honesty** — how long does a *full* restore actually take, measured, not
  estimated? "We can recover" with an unmeasured RTO is a WARN; the business decision
  (pay vs restore) depends on a real number.

---

## Step 3 — Restore to a point before the compromise, not just before the encryption

A successful restore of a compromised system is not recovery; it is re-infection with
downtime. The restore point must predate the *intrusion*, not merely the *detonation*:

- Dwell time is often weeks or months, so the "clean" backup from last night may
  already contain the attacker's persistence. Recovery timing depends on the timeline
  (`incident-timeline-reconstruction`): when did they actually get in?
- Retain enough history to have a restore point *before* the earliest confirmed
  compromise — and treat "we only keep 7 days and they were in for 30" as a finding.
- Verify the integrity of the chosen restore point (`tamper-evident-audit-chain`): can
  you show it was not altered, and that it is from before the breach?

---

## Step 4 — State the recovery claim honestly, with its gaps

Close with a claim someone can bet the business on, not a reassurance:

- **What is proven** — last successful test restore, its date, scope, and measured RTO.
- **What is assumed** — components never actually restore-tested, dependencies not
  verified, restore points whose integrity is unconfirmed.
- **What is exposed** — backups reachable from the compromise position, retention too
  short to predate dwell time.

"We can fully recover in 6 hours to a verified-clean point from immutable, offline
backups, last restore-tested Tuesday" is a recovery plan. "We have backups" is a hope,
and the honest report says which one you actually have — because the ransom negotiation
is not the place to find out.

---

## The one-line test

If your recovery plan has never been executed as an actual restore, you do not have a
recovery plan — you have backup jobs and optimism. Prove the backups are unreachable
from the compromise, prove a restore comes up clean from a point before the intruder
arrived, and measure how long it takes — until then, "we have backups" is answering a
question nobody asked.
