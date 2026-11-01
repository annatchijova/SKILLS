---
name: discriminating-proof
description: Turn a plausible hypothesis into an earned verdict with the cheapest experiment that can kill it — binary oracle with a canary value, a negative control inside the same run, prediction stated before execution, novelty gate before writing, and every link in the evidence chain labelled by epistemic level. Use whenever a security finding, bug hypothesis, or root-cause claim needs to be confirmed before reporting, when building a PoC, when the user says "prove it", "confirm the bug", "reproduce", "is this real", "ready to submit", "write the report", or when a claim rests on source reading alone and runtime confirmation is possible. Trigger even when a PoC already exists — to review whether its controls actually isolate the claimed factor. Sibling of falsifiable-testing — that skill builds tests that can fail; this one builds the single experiment whose failure kills the hypothesis and whose success a reviewer cannot dismiss.
---

# Discriminating Proof

A hypothesis confirmed by reading is a hypothesis confirmed by the layer of
the system you happened to read. The verdict that survives a hostile reviewer
is earned by a run — one designed so that its failure would falsify the claim
and its success cannot be explained by anything else.

The discipline in one line: **the run outranks memory, the control outranks
the result, and the ladder outranks enthusiasm.**

Composes with the library:

- **falsifiable-testing** — the test-design discipline behind the oracle
- **red-team-auditing** — the epistemic ladder this skill enforces
- **daubert-defensible-writing** — how the earned verdict gets written up
- **deterministic-core** — the PoC must be reproducible by the reviewer
- **claim-provenance-discipline** — each link keeps its level into the report

---

## Part 1 — The epistemic ladder: cap every claim at its rung

Every assertion carries exactly one level, and the level is set by the
strongest evidence actually obtained — never by the strength of the chain's
other links.

- **CODE FACT** — verified in the live source, with file and line. "Pipeline
  order is X", "the cleanup set is exactly these two names".
- **EXTERNAL FACT** — verified against official documentation, with the fetch
  performed this session. Not from memory.
- **SOURCE-CONFIRMED hypothesis** — every link is code or doc fact, but the
  end-to-end chain was never executed. Label it exactly that.
- **RUNTIME-CONFIRMED** — the chain executed and the oracle fired.
- **PLAUSIBLE HYPOTHESIS** — the cap when induction was not run, when a path's
  reachability was not traced, or when the construct was confirmed but the
  interaction was not.
- **REFUTED / FALSIFIED** — a first-class outcome, recorded with its evidence,
  never omitted from the report.

The frontier that is not a code fact is declared as such: "who controls the
Location header in a given deployment is deployment-dependent" — stated, with
the reason, never buried. The strongest framing available is often "the same
threat model the vendor already accepted when they fixed the sibling case".

## Part 2 — The oracle is binary, the value is a canary

Before building anything, state:

- **The prediction, in writing, before the run** — exact expected values, not
  a direction. "api-key == CANARY arrives; Authorization and Cookie do not."
- **The oracle**: one equality check on an unmissable sentinel
  (`CANARY-<target>-<date>`). If the canary appears at the destination →
  confirmed. If it does not → falsified. **Nothing else is inferred.** An
  oracle that requires interpretation is a horoscope.
- **The falsifier**: the observation that kills the hypothesis outright.

If the experiment cannot falsify the hypothesis, it is not the experiment yet
— redesign until a failure mode exists.

## Part 3 — The negative control runs in the same experiment

The result alone proves nothing; the reviewer's first counter-argument is
always "your harness just forwards everything". Preempt it structurally:

- **Intra-request controls**: set values the platform *does* strip
  (Authorization, Cookie) alongside the value under test. If the controls are
  stripped on the exact hop where the canary survives, "it forwards all
  headers" is dead — same pipeline, same transport, same redirect.
- **Negative-condition column**: run the identical chain with the one claimed
  factor removed (same-host redirect instead of cross-domain). The matrix —
  control forwarded in the negative column, stripped in the test column,
  canary surviving both — makes the strip demonstrably triggered by the
  factor you claim, and nothing else.
- **Run the skeptic's version first.** Build the naive PoC the reviewer would
  build, watch it fail to isolate the factor (a 127.0.0.1→127.0.0.1 redirect
  proves same-origin forwarding, not the bug), and document *why* the naive
  version does not exercise the gap. That note in the report is worth more
  than the PoC.
- **One factor per experiment.** When two variables change, fix one and re-run
  — a conflated run produces a verdict nobody can trust, including you.
- **Test each sink separately.** Two policies that share a failure class are
  two experiments; confirming one never confirms the other.

## Part 4 — Gates around the proof

- **Novelty gate, before writing**: changelog, commits, PRs, issues, CVE and
  GHSA databases, coordinated fix efforts in sibling implementations. A
  finding already fixed is a wasted report; a class with accepted precedent
  (the vendor fixed this exact pattern elsewhere) is armor — cite it.
- **Reality gate**: the PoC uses the real released component in its real
  configuration, pinned versions, and mocks only the attacker's share (the
  redirect, the network). A pipeline assembled by hand is a claim about your
  assembly, not about the product.
- **Environment honesty**: every harness accommodation (a TLS bypass flag for
  loopback, an offline transport) is documented in the report with the reason
  it does not change the result. Hidden accommodations are how good findings
  die in review.
- **The run outranks memory**: type names, option fields, default behaviors —
  verify by compiling and running, not by recalling. The cost of a wrong
  remembered detail is the whole credibility of the chain.
- **Version and scope gate**: affected versions, fixed versions if any, real
  shipped clients that reach the configuration — name one concrete consumer,
  not a theoretical one.

---

## Anti-patterns

- A PoC with no negative control, then arguing with the reviewer in prose.
- Reporting SOURCE-CONFIRMED chains as confirmed vulnerabilities.
- Inferring beyond the oracle ("the canary didn't arrive, but it probably
  still...").
- Checking novelty after writing the report instead of before.
- Hiding the harness bypass that made the offline run possible.
- Building the PoC on the documented API rather than the released one.
- Recording only the wins — an unreported falsification is a future
  duplicated effort and a missing piece of the target's assurance map.
