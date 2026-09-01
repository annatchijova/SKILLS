---
name: ot-safety-first-threat-model
description: Threat-model operational technology by inverting the IT reflexes — in OT/ICS the priority is availability and physical safety, not confidentiality, so the moves that are correct on a corporate network (patch immediately, scan aggressively, force MFA, encrypt everything) can halt a process, trip a safety system, or get someone killed. Use whenever the system controls or monitors physical process: "secure our SCADA / PLC / ICS", "OT network", "should we patch this controller", "can we run a vuln scan on the plant floor", "IT/OT convergence", "the HMI / historian / DCS", "safety instrumented system", "why can't we just patch it", "air gap". Sibling of assume-breach-modeling (blast radius here is physical) and irreversible-action-gate (a wrong control action has kinetic, unrecoverable consequences); it reasons about safety-first tradeoffs. It does not design the industrial process or its safety engineering, and never imports an IT control into OT without checking what it does to availability and safety.
---

# OT Safety-First Threat Model

Operational technology inverts the assumption every IT security instinct is built on.
On a corporate network the ranking is confidentiality, integrity, availability, and the
reflexes follow: patch the moment a CVE drops, scan aggressively to find exposure, force
encryption and MFA everywhere, reboot to apply. In OT — the PLCs, RTUs, HMIs, and safety
systems that run a turbine, a pipeline, a water plant, a factory line — the ranking is
**safety and availability first**, and those same reflexes become the threat. A vuln
scan can crash a fragile controller that has an uptime measured in years. A forced patch
can require a process shutdown that costs a week and a restart that is itself dangerous.
An "encrypt everything" mandate can add latency that violates a real-time control loop.
The wrong security action does not leak data; it stops a physical process or defeats a
safety function, and the consequence is measured in downtime, environmental release, or
lives.

Two symmetric failure modes:

- **IT reflexes imported blind.** Treating the plant floor like an enterprise LAN —
  scanning it, patching on the IT cadence, deploying agents onto devices that were never
  built to run them — and inducing the outage you were trying to prevent. The security
  team becomes the incident.
- **"It's air-gapped, it's fine."** The mirror error: assuming physical isolation that
  no longer exists (a historian bridged to the corporate network, a vendor's remote-
  maintenance modem, a USB workflow, IT/OT convergence) and therefore doing nothing,
  leaving a flat, unauthenticated, unpatchable network wide open once the gap is crossed.

The through-line: **model consequence in the physical world, and let availability and
safety, not confidentiality, set the priority.** Every control is judged first by what
it does to the process.

Composes with the library:

- **assume-breach-modeling** — the blast radius of an OT compromise is kinetic; "what does this foothold reach" ends at a physical actuator, not a database
- **irreversible-action-gate** — a control command (open a valve, change a setpoint, stop a safety system) is a one-way, physical action; the gate is not a UX nicety here, it is safety engineering
- **honest-degradation** — an unpatchable, end-of-life controller that cannot be fixed is a documented WARN with compensating controls, not a pretended PASS
- **dual-use-behavior-adjudication** — on an OT network, an engineering workstation issuing control commands is normal; malice is context (unexpected setpoint, off-hours, from the wrong host), not the command itself
- **detection-engineering** — OT detection is passive and protocol-aware (span ports, not agents; Modbus/DNP3/S7 semantics), because active probing is itself a hazard

---

## Step 1 — Rank the impact in the physical world, safety at the top

Before any control decision, state the consequence hierarchy for *this* system, because
it determines what "secure" even means:

- **Safety** — can a compromise or a security action cause physical harm (release,
  explosion, equipment destruction, injury)? A safety-instrumented system (SIS) that a
  control defeats or delays is the top of the risk stack, above any data concern.
- **Availability** — can it stop the process? Downtime in continuous processes is not an
  inconvenience; a restart may be slow, costly, or hazardous in itself.
- **Integrity** — a manipulated setpoint or spoofed sensor reading that drives the
  process to an unsafe state (the Stuxnet / Triton class), where the operator sees
  "normal" while reality diverges.
- **Confidentiality** — last, not first. Process data matters, but not at the cost of
  the three above.

An assessment that opens with "we should encrypt the historian" before it has
characterized the safety and availability impact has imported the wrong ranking.

---

## Step 2 — Test every proposed control against availability and safety first

For each IT-style control on the table, ask what it does to the process *before* asking
what it protects:

- **Patching** — does applying it require a shutdown? Is the vendor's patch validated for
  this device and firmware? Is the controller so fragile or end-of-life that the patch
  risk exceeds the vuln risk? Patch cadence in OT is driven by maintenance windows and
  vendor validation, not by CVE date.
- **Scanning / active discovery** — can this device tolerate a scan, or will an
  unexpected packet crash a decades-old TCP stack? Prefer passive discovery; active
  probing is a hazard until proven safe on that exact model.
- **Agents / encryption / MFA** — will the endpoint even run an agent? Does encryption
  break a real-time loop's timing budget? Does MFA on an HMI block an operator during an
  emergency when seconds matter? A control that impedes emergency operation is a safety
  regression.

A control that reduces a confidentiality risk while raising a safety or availability
risk is usually the wrong trade in OT. Name that trade explicitly.

---

## Step 3 — Verify the isolation you are assuming actually holds

The "air gap" is the most over-claimed control in OT. Do not assume it; map it:

- **Enumerate every crossing** — IT/OT firewalls and their real rules, historians and
  data diodes, jump hosts, vendor remote-access (cellular modems, TeamViewer, dial-up
  still exists), USB and laptop workflows, the engineering workstation that touches both
  worlds. IT/OT convergence has quietly bridged most "gaps."
- **Treat the crossing as the trust boundary** — the corporate network is untrusted from
  the OT side; the engineering workstation and the historian are the classic pivot
  points (assume-breach-modeling). Once inside, OT networks are typically flat,
  unauthenticated, and unencrypted by design — so a single crossing is often
  domain-wide on the process network.
- **If the gap is real, defend the few crossings hard rather than the many endpoints
  you cannot patch.** If it is not real, say so — a believed-but-false air gap is the
  worst of both worlds.

---

## Step 4 — Build compensating controls around what you cannot fix

Much of OT cannot be patched, upgraded, or hardened without unacceptable process risk.
Honest degradation is the posture, not a failure:

- **Segment and monitor instead of patch** — network zones/conduits (the Purdue model /
  IEC 62443 idea), tight allow-lists at the boundary, and *passive* protocol-aware
  monitoring that raises no traffic on the wire.
- **Protect the safety layer independently** — the SIS should be separated from the basic
  process control so that a compromise of the controllable layer cannot also defeat the
  system that would stop a runaway (the Triton lesson).
- **Document the residual risk as a WARN with a reason** — "controller X is end-of-life,
  unpatchable; compensating controls are segmentation + passive monitoring; residual
  risk accepted by process owner" is honest and auditable. A pretended-clean status on an
  unpatchable device is the dangerous lie.

---

## Step 5 — Detect and respond without becoming the incident

Detection and IR in OT carry the same inversion:

- **Passive, protocol-aware detection** — baseline the process traffic (Modbus, DNP3,
  S7, EtherNet/IP) and alert on the semantics: an unexpected setpoint change, a
  firmware download to a PLC, an engineering command from a host that never issues one
  (dual-use-behavior-adjudication, physical edition). No active agents on the process
  devices.
- **Containment cannot default to "isolate and reboot"** — pulling a controller offline
  or cutting the HMI may be more dangerous than the intrusion. Containment decisions run
  through the process/safety engineers, weighing the physical consequence
  (containment-under-uncertainty with a kinetic blast radius). The plant may need to run
  degraded, not stop.

---

## The one-line test

If your OT recommendation would be uncritically correct on a corporate laptop — patch it
now, scan the subnet, force encryption, isolate and reboot — you have not threat-modeled
OT; you have pointed IT reflexes at a physical process. Re-rank with safety and
availability on top, and test each control by what it does to the process before what it
protects.
