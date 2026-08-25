---
name: acquisition-order-of-volatility
description: Collect digital evidence in order of volatility, or destroy the thing you came for — memory, network state, and running processes evaporate the moment you pull power or start "just looking," and the act of collecting alters the scene, so order and method are the evidence's admissibility, not a formality. Use whenever evidence is being captured from a live or suspect system: "acquire the disk", "grab a memory dump", "should we pull the plug or shut down gracefully", "image this machine", "collect logs from the compromised host", "preserve the evidence", "is this forensically sound", "we already rebooted it". Sibling of finding-custody (chain of custody of the artifact) and tamper-evident-audit-chain (proving it was not altered after); it governs the collection act itself. It does not analyze the acquired image (that is the investigation) and never presents evidence collected out of order or without footprint as if it were pristine.
---

# Acquisition Order of Volatility

The evidence you most need is the evidence that disappears fastest. The contents of
RAM, the live network connections, the running process list, the routing and ARP
tables — all of it is gone the instant someone pulls power or, almost as bad, starts
poking at the box to "see what's going on." Disk survives; volatile state does not. So
the first law of acquisition is not "make a copy" — it is **collect in order of
volatility**, most-perishable first, because the order is the difference between having
the evidence and having overwritten it.

The second law follows from the first: **the act of collecting alters the scene.**
Mounting a filesystem writes access times; running a tool allocates memory over the
very RAM you wanted; opening a file changes its metadata. You cannot observe the
system without touching it, so the discipline is to *minimize and record* your
footprint, not to pretend you left none.

The two failure modes that ruin evidence before analysis even begins:

- **The "quick look."** An analyst logs in, browses the disk, runs a few commands,
  reboots to "check something" — and overwrites the memory, the timestamps, and the
  free space that held the answer. The investigation is now archaeology of the
  investigator's own footprints.
- **Disk-first.** Imaging the drive (slow, non-volatile, patient) while the live
  connections to the C2, the injected process, and the decryption keys sitting in RAM
  quietly evaporate. You preserved the part that was in no hurry to leave.

Composes with the library:

- **finding-custody** — the chain of custody begins at the moment of collection, not later; this skill is where custody starts
- **tamper-evident-audit-chain** — hash at the source so a verifier can later prove the image was not altered
- **incident-timeline-reconstruction** — the timeline is built from what you collect; collect out of order and the timeline has holes you caused
- **honest-degradation** — evidence collected imperfectly is a WARN on that evidence, stated, not a silent gap presented as clean
- **containment-under-uncertainty** — the "pull the plug now" containment instinct collides with acquisition; sequence them deliberately

---

## Step 1 — Order the targets by volatility before you touch anything

Write the collection order most-perishable to least, and follow it:

1. **CPU state, memory (RAM)** — the most volatile and often the richest: injected code,
   decryption keys, cleartext credentials, unpacked malware, network buffers.
2. **Live network state** — active connections, listening ports, ARP/routing tables,
   DNS cache: the map of what the box is talking to *right now*.
3. **Running processes and open handles** — the process tree, loaded modules, open
   files, which the reboot will erase.
4. **Ephemeral disk state** — temp files, swap/pagefile, unallocated space that the next
   write may reuse.
5. **Persistent disk** — the full image; non-volatile, patient, collect it after the
   perishable state is safe.
6. **Archived/remote logs, backups** — least volatile; collect but do not let them jump
   the queue ahead of RAM.

The one non-negotiable ordering error: never reboot or power-cycle *before* memory is
captured, unless a containment decision forces it — and if it does, say so (Step 5).

---

## Step 2 — Decide live vs dead acquisition, knowing each destroys something

Two paths, and each has a cost you must name:

- **Live acquisition** (collect from the running system) — preserves volatile state, but
  every tool you run alters memory and the running OS could be lying to you (a rootkit
  hides the very processes you are listing). Use trusted, statically-linked tools from
  external media; assume the compromised OS's answers are suspect.
- **Dead acquisition** (power off, image the disk) — gives a clean, repeatable disk
  image, but *pulling power destroys all of Step 1's volatile state* and a graceful
  shutdown runs the attacker's shutdown scripts and changes the disk. Neither
  power-off option is free.

There is no universally correct choice; there is a choice appropriate to *this*
incident, made deliberately and recorded. The wrong move is to back into one by habit.

---

## Step 3 — Minimize and record the footprint you cannot avoid

You will alter the scene; the discipline is to do it as little as possible and to log
exactly what you did, so a later analyst can subtract your footprint from the
attacker's:

- Prefer read-only / write-blocked access to disk; use a hardware or software
  write-blocker for imaging.
- Run collection tools from external, trusted media, not from the suspect disk.
- Record every command you ran, when, as whom, and what it touched — your actions are
  part of the timeline and must be distinguishable from the adversary's.

Unrecorded analyst activity is indistinguishable, later, from attacker activity — and
that ambiguity can sink both the investigation and its admissibility.

---

## Step 4 — Hash at the source; custody starts here

The integrity claim you will need later — "this image is exactly what was on the disk,
unaltered since collection" — can only be made if you anchor it at the moment of
collection:

- Compute a cryptographic hash of the acquired image (and of memory) *at acquisition*,
  and record it (`tamper-evident-audit-chain`).
- Work from copies; preserve the original acquisition untouched (`finding-custody`).
- Note who collected it, when, from what, and how — the chain of custody is a line that
  starts at your hands, not one you can back-fill from memory later.

---

## Step 5 — When containment forces a bad order, say so honestly

Sometimes the incident does not let you follow the order: ransomware is encrypting and
you must pull power *now*, or the box was already rebooted before you arrived. That is a
legitimate operational reality, and the honest response is not to pretend the evidence
is pristine — it is to record the degradation:

- "Memory not captured; host was powered off for containment at 14:02 before
  acquisition" is a WARN attached to the evidence, and it tells every downstream
  conclusion which questions can no longer be answered.
- Evidence collected out of order, or after a reboot, is still evidence — but it is
  *scoped* evidence, and presenting it as clean is the forensic version of the overclaim
  this library forbids everywhere. `ABSTAIN` on the questions the lost volatile state
  would have answered.

---

## The one-line test

If your first action on a suspect machine was to log in and look around, you began by
overwriting the evidence you came for. Order the targets by how fast they vanish,
capture memory before anything reboots it, hash at the source, and log your own
footprint — because acquisition is the one phase where a mistake is not a wrong answer,
it is the permanent absence of the right one.
