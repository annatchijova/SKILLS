---
name: containment-under-uncertainty
description: Make containment decisions before scope is known, reasoning in reversible-versus-irreversible moves — because acting tips off the adversary (they burn down, accelerate, or pivot) while not acting lets the bleed continue, and "we don't fully understand it yet" must never quietly become "so we did nothing." Use in an active incident when the question is what to do now with incomplete information: "should we isolate the host", "pull it off the network", "rotate all credentials", "rebuild or watch", "will we tip them off", "we don't know the full scope yet", "contain now or gather more". Sibling of assume-breach-modeling (for blast radius under uncertainty) and irreversible-action-gate (wipe/rebuild/rotate are one-way doors); it sequences containment. It does not reconstruct the full timeline (incident-timeline-reconstruction) or attribute the actor, and never trades the forensic scene for speed without saying so.
---

# Containment Under Uncertainty

The defining condition of containment is that you must act before you know the scope,
and both acting and waiting cost you something. Evict too early and loudly and you warn
the adversary — who then burns their access down, destroys evidence, or accelerates to
finish the job before you finish yours. Wait for certainty and the data keeps leaving.
There is no move that is free of one of these costs, so the discipline is not "decide
once you understand it"; it is **buy information without buying disaster**, and reason
about every action as reversible or irreversible.

The two failure modes are symmetric, and organizations reliably pick one by
temperament:

- **Premature loud eviction.** Pulling the plug, mass-resetting, wiping the box — before
  you know what it connected to. You destroy the forensic scope you needed (`what else
  did this credential touch?` is now unanswerable), and you tell the intruder you are
  onto them while they still hold three other footholds you never found.
- **Analysis paralysis.** "We don't fully understand it yet" hardens into inaction
  while exfiltration continues. Perfect scope is never available during the bleed; the
  demand for it is how a team does nothing and calls it caution.

Composes with the library:

- **assume-breach-modeling** — you contain against the *assumed* blast radius, not the confirmed one; this supplies it
- **irreversible-action-gate** — wipe, rebuild, rotate-everything, power-off are one-way doors; they get the gate, not a reflex
- **incident-timeline-reconstruction** — containment must preserve the evidence this later depends on; do not trade the timeline for a fast eviction
- **credential-material-triage** — deciding what to rotate first is a blast-radius question about the captured material
- **honest-degradation** — the decision record states the scope you had vs assumed; a WARN is not a PASS
- **dual-use-behavior-adjudication** — before you contain, be sure the "intrusion" is not your own admin (containing a false positive has real cost too)

---

## Step 1 — Sort every option into reversible and irreversible

Before choosing, classify the moves, because the classification is most of the
decision:

- **Reversible / low-regret** — network-isolate a host (you can un-isolate it),
  block an egress domain, disable one account, increase logging, snapshot memory. These
  buy safety and information and can be undone if you were wrong.
- **Irreversible / high-regret** — wipe or rebuild a host (evidence gone), power it off
  (volatile state gone — see `acquisition-order-of-volatility`), rotate every credential
  at once (you may lock out the responders and tip the adversary simultaneously),
  publicly disclose.

Default to the reversible moves *first*: they narrow the bleed and preserve your
options. The irreversible ones require the gate in Step 4.

---

## Step 2 — Price the observation-versus-eviction tradeoff explicitly

Watching a live intrusion has value (you learn scope, TTPs, other footholds) and a
cost (data leaves while you watch). Evicting has value (bleed stops) and a cost (you
lose the intel and warn the adversary). State which side the specific incident favors:

- **Lean toward observe** when the ongoing loss is bounded and slow, the adversary
  seems unaware, and you have not yet found the full foothold set — the intel prevents
  a whack-a-mole where you evict one access and miss two.
- **Lean toward evict now** when active, fast, high-impact loss is underway
  (ransomware staging, bulk exfil in progress, hands-on-keyboard destruction) — intel
  is worthless if the patient dies during the diagnosis.

This is a judgment with an owner and a rationale, recorded — not a reflex, and not a
decision made by whoever is loudest in the bridge call.

---

## Step 3 — Contain against the assumed blast radius, not the confirmed one

You will never have confirmed scope in time. Use `assume-breach-modeling`: assume the
compromised identity reached everything its privileges allow, and contain *that*
surface, while marking clearly that it is assumed. This is how you avoid the
whack-a-mole trap — evicting the one host you found while the reused credential still
works on twenty others. Rotate/isolate by blast radius (via `credential-material-triage`),
highest-reach first, in an order that does not lock out your own responders mid-eviction.

---

## Step 4 — Put the one-way doors behind the gate

Wipe, rebuild, mass-rotation, and power-off are irreversible; they must not be reflexes
under adrenaline. For each, before pulling it:

- Confirm the evidence you need has been acquired first (memory before power-off;
  image before wipe — `acquisition-order-of-volatility`).
- Confirm it is coordinated: a partial mass-rotation that misses one system hands the
  adversary a still-valid key and announces the response. Eviction works best
  *simultaneous and complete*, which requires knowing the foothold set — the very thing
  Step 2's "observe" side was buying.
- Record the decision, its rationale, and the accepted residual uncertainty
  (`irreversible-action-gate`).

---

## Step 5 — Preserve the scene while you contain, and write down what you didn't know

Containment and forensics are in tension but not opposed: isolate rather than wipe,
snapshot before you change, log the footprint your own actions leave. The incident
timeline (`incident-timeline-reconstruction`) is built from evidence a hasty eviction
destroys — so the honest close of every containment action is a note of the scope you
actually had versus assumed, and what a later analyst has lost because you had to act
before you knew. That WARN is not an admission of failure; it is what makes the next
decision in the same incident an informed one.

---

## The one-line test

If your containment plan requires knowing the full scope first, you have designed a
plan for an incident you are no longer in. Take the reversible moves now against the
*assumed* blast radius, keep the one-way doors behind the gate until the evidence is
saved and the eviction can be complete, and write down — as you go — the difference
between what you knew and what you assumed.
