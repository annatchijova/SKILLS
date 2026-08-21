---
name: forensic-persistence
description: Keep an investigation alive and productive when every hypothesis has been refuted, the target looks hardened, and the session feels empty — refutation is terrain mapping, pivot the question family instead of abandoning the target, and never convert "we found nothing" into "there is nothing". Use whenever a hunt, audit, or debugging session produces zero findings, when the user says "no encontramos nada", "everything was refuted", "this repo is too hardened", "let's just drop it", "we tried everything", "dead end", "I'm stuck", "diminishing returns", or is tempted to declare a component safe because the tools came back empty. Also trigger when a bug survives several fix attempts, when a bounty report was rejected, or when deciding whether to continue, pivot, or park an investigation. Sibling of red-team-auditing and abductive-engineering — those skills run the hypotheses; this one governs what happens when the hypotheses keep dying.
---

# Forensic Persistence

The bugs exist. They were not found — those are different claims, and the
second is the only one your evidence supports. A session that refutes twelve
hypotheses has not failed; it has mapped twelve places nobody ever has to look
again. The investigator who stops is the one who hands the finding to whoever
comes next.

A hardened target is an advantage, not a verdict. It repels the competition,
which means the bugs are still there — in deeper layers than the surface
everyone else swept. Persistence is not stubbornness about a hypothesis; it is
stubbornness about the *target*, combined with total willingness to kill any
hypothesis the evidence kills.

Composes with the library:

- **red-team-auditing** — runs each candidate to a verdict; this skill governs
  the campaign across candidates
- **abductive-engineering** — generates the next hypothesis when one dies
- **attack-surface-triage** — picks the next axis when the current one is spent
- **decision-record-discipline** — parks a target with a resumption queue, not
  a tombstone
- **claim-provenance-discipline** — keeps "not found" from mutating into "safe"

---

## Part 1 — Refutation is terrain, not failure

Every refuted hypothesis earns a permanent record: what was claimed, what
killed it, and the evidence pointer. This is the **discard registry**, and it
is a deliverable even when nothing else survives the session.

Rules of the registry:

- Record the refutation reason precisely enough that a future reader can
  re-verify it after the code changes ("deserialize_type resolves only via
  allowlist or already-loaded modules; no eval on the path" — not "checked,
  fine").
- Record the *almosts* too: hygiene issues, unreachable-but-ugly constructs,
  defense-in-depth gaps. Capped at their honest level, they are residuals —
  noted, never inflated, never deleted.
- The registry is cumulative across sessions and across tools. Its first use
  next session is to prevent re-treading; its second use is to show a reviewer
  the target was taken seriously.

Never let a registry entry decay into "X is safe". The honest statement is
always "X was checked, by this method, on this date, and held".

## Part 2 — Pivot the axis, not the target

When a question family stops producing, the failure is in the *family*, not in
the target. Change the question before you change the repo.

The pivot moves, in order of preference:

1. **Change the question family on the same surface.** Exhausted "can
   something execute without authority?" → try "does what was established at
   T0 remain true at Tn?" (`invariant-hunting`). Exhausted authority → try
   integrity. Exhausted integrity → try ordering, identity, namespace.
2. **Change the surface within the target.** The engine was clean → the web
   layer, the transport adapters, the storage provider. Each surface has a
   different authority model; a boundary that does not exist in one component
   lives in another.
3. **Change the implementation of the same root class.** A confirmed bug class
   is a template: replicate laterally to sibling SDKs, languages, and products
   (`beyond-the-sink`) before concluding the class is closed.
4. **Park, don't bury.** If energy or time genuinely runs out, park the target
   with a written resumption queue — the un-probed leads, in priority order,
   with the reason each was deferred. "Parked with a queue" is a state;
   "dropped" is a leak.

Only after all four is "this target is currently beyond our reach" an honest
sentence — and even then it is a scheduling decision, not a verdict.

## Part 3 — The honest ways a session ends

A session may end. What it may not do is end *dishonestly*.

- **"Held up" is a result.** "We looked seriously and it withstood" is a
  finding about the target's assurance level — record it with the same rigor
  as a vulnerability: scope, method, date, what was and was not covered.
- **Silence is "not checked", never "proven safe".** Every coverage statement
  names its gaps explicitly. A table row with no entry means the row was not
  examined.
- **Rejection is data, not refutation.** A bounced bounty report means the
  *case as presented* did not land; the defect's existence is a separate
  question. Extract what the rejection teaches (scope, impact framing,
  reachability proof) before deciding whether to rework or re-aim.
- **Energy is a resource to allocate, not a mood to obey.** The right moves
  when tired are: run the cheapest remaining discriminating test, write the
  registry while the context is fresh, or park with a queue. The wrong move is
  a sweeping conclusion the evidence does not carry.

---

## Anti-patterns

- Declaring a component safe because the scanner or the first sweep found
  nothing.
- Re-running the same sweep with the same keywords and calling it persistence.
- Abandoning the target when what died was the question family.
- Quietly dropping an investigation with no registry, so the next session
  pays full price to re-discover the refutations.
- Treating "the authors clearly had a security review" as a reason to stop.
  It is a reason the shallow bugs are gone — and that the remaining ones are
  better.
- Inflating a hygiene residual into a finding to make the session feel
  productive. The registry keeps you honest; keep it honest.
- Letting "no paro porque no tengo otra cosa" energy turn into sloppiness.
  Persistence without rigor is just more time at the same depth.
