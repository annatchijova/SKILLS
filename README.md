# SKILLS — Engineering Discipline Skill Set

**Language:** English · [Español](README.es.md)

A collection of 53 skills for Claude Code that encode disciplined software engineering, forensic reasoning, and security-first construction. Each skill activates automatically when the conversation matches its trigger conditions, injecting methodology without requiring the user to ask for it.

These skills form a coherent system built on Charles Sanders Peirce's triadic semiotics and the abductive inference loop (abduction → deduction → induction). They cover the full engineering lifecycle: investigation, construction, patching, testing, auditing, and hardening.

---

## Skills

| # | Skill | Category | Activates when |
|---:|---|---|---|
| 1 | `abductive-engineering` | Core reasoning | Debugging, root-cause analysis, incident response, or architectural decisions under uncertainty. |
| 2 | `red-team-auditing` | Core reasoning | Security audits, adversarial review, threat modeling, or invariant analysis. |
| 3 | `secure-by-construction` | Core reasoning | Writing, extending, refactoring, or reviewing code with security boundaries. |
| 4 | `software-archaeology` | Core reasoning | Modifying legacy, inherited, or unfamiliar code without breaking behavior. |
| 5 | `diagnosing-bugs` | Core reasoning | Investigating hard bugs and performance regressions through controlled probes and regression tests. |
| 6 | `codebase-health-assessment` | Core reasoning | Classifying dead, fossil, live, and out-of-scope modules before changing a codebase. |
| 7 | `reverse-engineering` | Core reasoning | Reconstructing undocumented systems, binaries, protocols, file formats, or opaque APIs without readable source. |
| 8 | `daubert-defensible-writing` | Core reasoning | Writing findings and reports that separate evidence, inference, uncertainty, and opinion. |
| 9 | `deterministic-core` | Determinism & integrity | Producing bit-for-bit reproducible and tamper-evident decisions with canonical serialization and SHA-256 sealing. |
| 10 | `llm-out-of-the-loop` | Determinism & integrity | Keeping consequential decisions outside the LLM path and sealing results before optional narration. |
| 11 | `tamper-evident-audit-chain` | Determinism & integrity | Building or verifying append-only logs that detect alteration, insertion, reordering, or deletion. |
| 12 | `atomic-state-mutation` | Determinism & integrity | Making multi-write persistent operations all-or-nothing and isolated from concurrent callers. |
| 13 | `versioned-schema-evolution` | Determinism & integrity | Evolving serialized artifacts with explicit schema versions without breaking existing data. |
| 14 | `surgical-patcher` | Patching & editing | Applying anchored, verified, reversible changes instead of rewriting entire source files. |
| 15 | `audit-before-patch` | Patching & editing | Validating an audit finding against the current file before changing any code. |
| 16 | `validate-at-the-boundary` | Input & data | Validating untrusted input at the system boundary with clear errors. |
| 17 | `honest-degradation` | Input & data | Handling degraded, legacy, reconstructed, or unverifiable input without returning plausible-looking wrong results. |
| 18 | `sql-aggregation-not-materialization` | Input & data | Pushing counts, sums, and grouping into the database instead of loading rows into memory. |
| 19 | `git-discipline` | Process | Keeping AI-assisted coding sessions recoverable, reviewable, and free from unsafe history rewriting. |
| 20 | `claim-provenance-discipline` | Evidence governance | Preserving each claim's origin, epistemic level, scope bound, and falsifier across summaries and handoffs. |
| 21 | `attack-surface-triage` | Adversarial validation | Enumerating an authorized target's surface into a reproducible, falsifiable candidate queue — before any payload. |
| 22 | `purple-team-exercise` | Adversarial validation | Turning each technique into a detection hypothesis, detonating it minimally and marked, and measuring what the blue side saw. |
| 23 | `detection-engineering` | Adversarial validation | Turning a detection requirement into a tested, budgeted, versioned rule — with a benign twin that must not fire. |
| 24 | `agent-trust-boundaries` | Agent architecture | Keeping retrieved content as data, tool authority in deterministic policy, and the untrusted/private/egress trifecta broken. |
| 25 | `falsifiable-testing` | Verification | Writing tests that can actually fail — red first, negative controls, oracle strength, and flakes treated as findings. |
| 26 | `incident-timeline-reconstruction` | Evidence governance | Ordering events across clock domains, separating recorded from actual time, and labeling every gap by kind. |
| 27 | `irreversible-action-gate` | Process | Classifying actions by reversibility and blast radius, then gating them with preview, count assertion, and a written undo plan. |
| 28 | `dependency-provenance` | Supply chain | Knowing what is actually shipped, establishing package identity before trust, and treating advisories as candidates until reachability is shown. |
| 29 | `secret-lifecycle-discipline` | Credentials | Treating credentials as a lifecycle — redaction at the boundary, rotation rehearsed before it is needed, rotate-first on exposure. |
| 30 | `decision-record-discipline` | Process | Capturing forces, rejected alternatives, load-bearing assumptions, and revisit triggers while the context still exists. |
| 31 | `concurrency-reasoning` | Core reasoning | Reasoning about shared mutable state, invariants, and happens-before ordering instead of adding a lock and hoping. |
| 32 | `forensic-logging-design` | Evidence governance | Deciding what to record today so tomorrow's reconstruction is possible — decisions, correlation, and legible silence. |
| 33 | `invariant-hunting` | Core reasoning | Hunting violations of a declared or implied security invariant across a transition — a property established at T0 that a later state change must preserve. |
| 34 | `beyond-the-sink` | Core reasoning | An investigation stalls — looking past the sink-grep keyword list, the exhausted question family, or a single implementation when the obvious layer is dry. |
| 35 | `discriminating-proof` | Verification | Turning a plausible hypothesis into an earned verdict with the cheapest experiment that can kill it — binary oracle, canary value, negative control. |
| 36 | `forensic-persistence` | Core reasoning | A hunt, audit, or debug session returns zero findings, hypotheses keep getting refuted, or a target looks too hardened to continue. |
| 37 | `oracle-driven-fuzzing` | Verification | Bugs must be found by generated input — property-based, structure-aware, differential and metamorphic oracles, corpus discipline, shrinking, and crash triage. |
| 38 | `parser-differential-hunting` | Adversarial validation | Two components read the same bytes and disagree — the checkpoint decides on one meaning while the sink acts on another. |
| 39 | `authorization-surface-mapping` | Adversarial validation | Building the actor × resource × action matrix and testing the cells nobody wrote a test for — because a missing check looks like nothing. |
| 40 | `assume-breach-modeling` | Adversarial validation | A position is already held — mapping what that identity reaches, and finding the choke point whose removal cuts the most paths. |
| 41 | `resource-exhaustion-review` | Input & data | A small input buys a large amount of work or memory — asymmetry ratios, unbounded allocation, super-linear algorithms, missing backpressure. |
| 42 | `remediation-driven-reporting` | Adversarial validation | Writing the report so the class gets fixed, not the instance — surviving triage, severity scored to demonstrated impact, and verifying the patch against the class. |
| 43 | `finding-custody` | Evidence governance | A confirmed finding after it is reported — instance vs class vs method, the patch-diffing window, custody of the PoC, and a disclosure decision with a revisit trigger. |
| 44 | `data-leakage-hunting` | Machine learning | The one bug class whose symptom is a better score — evaluation data reaching the model through preprocessing, time, groups, duplicates, or a spent test set. |
| 45 | `training-run-provenance` | Machine learning | Determinism where it is achievable — the artifact, not the process: a sealed manifest, named nondeterminism, and a reproducibility claim at the rung the evidence supports. |
| 46 | `model-evaluation-discipline` | Machine learning | An evaluation that can actually fail — mandatory baseline, interval instead of point estimate, worst slice instead of mean, and negative controls. |
| 47 | `training-serving-parity` | Machine learning | The features a model was trained on are not the features it is served — two implementations of one computation, and the silent default that answers confidently on a vector never seen. |
| 48 | `beyond-the-fix` | Core reasoning | Auditing the fixes themselves — a patch proves someone knew something was wrong there, never that it is now right; eight ways a fix falls short, and the pre-fix control that tells them apart. |
| 49 | `dual-use-behavior-adjudication` | Security operations | Deciding malicious vs benign when the tool itself is legitimate — the living-off-the-land problem, where the verdict lives in provenance, baseline, and sequence, never in the artifact. |
| 50 | `threat-attribution-restraint` | Security operations | Resisting the pull to name an actor — every overlap that points at APT-X is contact between datasets, not identity of hands, and most of it is cheap to plant. |
| 51 | `credential-material-triage` | Credentials | Turning "we found a credential" into a finding — what it authenticates as, authorizes, for how long, and how to revoke it, without inflating a hash into a compromise. |
| 52 | `cloud-control-plane-reasoning` | Security operations | Reasoning about cloud compromise on the identity and control-plane graph, not the network diagram — where a stolen key is one AssumeRole from the whole account. |
| 53 | `untrusted-sample-handling` | Security operations | Examining a hostile artifact safely — never let it execute where it can reach anything real, never confuse what it can do with what it was aimed at. |

### Adversarial validation loop

`attack-surface-triage` opens the loop and `red-team-auditing` is the
confirmation step; the hunting skills feed candidates in, and the impact and
containment skills carry a confirmed finding back out to the blue side:

```
                 attack-surface-triage → ranked candidates
                              │
   ┌──────────────────────────┼──────────────────────────┐
   │  where candidates come from (the hunt)              │
   │  invariant-hunting · parser-differential-hunting    │
   │  authorization-surface-mapping · beyond-the-sink    │
   │  oracle-driven-fuzzing · resource-exhaustion-review │
   │  beyond-the-fix (the fix history is the map)        │
   └──────────────────────────┼──────────────────────────┘
                              ▼
      discriminating-proof → red-team-auditing → confirmed / refuted
                              │                        │
                              │            forensic-persistence (refuted → next axis)
                              ▼
      assume-breach-modeling → impact, choke points, containment
                              ▼
      purple-team-exercise → detection gaps
                              ▼
      detection-engineering → proven rule → (retest closes the loop)

   when the target is someone else's:
      remediation-driven-reporting → the class gets fixed, not the instance
      finding-custody → what you did NOT say, and what reopens the decision
```

Everything on the offensive side of this library exists to produce a defensive
artifact: a bound, a bulkhead, a generated negative test, or a rule that has
fired for the right reason.

### The machine-learning seam

ML breaks three assumptions the rest of the library rests on: the test is a
metric rather than a pass/fail, the data is the real program, and the
highest-severity bug class *raises* the score. Skills 44–47 restore them, and
they meet `deterministic-core` at a specific boundary:

```
training run        →   frozen artifact   →   inference   →   decision
nondeterministic        hashed, immutable     deterministic     exact
training-run-           the seam              same artifact     deterministic-core
provenance                                    + input           applies unmodified
       ↑                        ↑                   ↑
data-leakage-hunting   training-serving-parity   model-evaluation-discipline
(is the number real?)  (is the served input      (is the number a
                        the trained input?)       measurement?)
```

Determinism does not stop being reachable in ML — it stops being reachable
*upstream of the artifact*. Everything downstream is held to the same standard
as any other consequential output path here.

---

## Repository Structure

Each skill lives in its own directory and is a single self-contained file:

```
<skill-name>/
  SKILL.md      # YAML frontmatter (name + description) followed by the full methodology
```

The `description` field is the trigger surface — it must name the situations,
phrasings, and artifacts that should activate the skill, and it must stay under
1024 characters. The body is loaded only once the skill triggers.

No skill currently ships `scripts/` or `references/` subdirectories; add them
alongside `SKILL.md` if a future skill needs executable helpers or long reference
material that does not belong in the always-loaded body.

---

## Design Principles

- **No LLM in the decision path.** Consequential outputs are sealed deterministically before any model is called.
- **Abduction before deduction.** Every diagnosis generates a falsifiable hypothesis, derives a testable prediction, and confirms or refutes it against the real system.
- **Eco's razor.** Before acting on any hypothesis, attempt to refute it. A refuted hypothesis is a result, not a failure.
- **Honest degradation over false confidence.** Three states, not two: PASS / WARN / FAIL. ABSTAIN is a valid verdict.
- **Surgical patching over rewriting.** Regenerating a file from memory is the largest source of silent regressions.
- **Never trust a green you have not seen red.** A test — or a detection rule — that has never failed for the right reason measures nothing.
- **Authority comes from the channel, not the content.** Retrieved documents, tool output, and other agents' summaries are data; none of them can grant themselves permission.
- **Proportional gates before irreversible actions.** Preview the exact targets, assert the expected count before seeing it, and write the undo plan before acting — not after.
- **Red exists to produce blue.** A confirmed finding is not the deliverable; the bound, the bulkhead, the generated negative test, and the detection requirement are.
- **You cannot grep for an absence.** Missing checks, unenumerated cells, and unstated limits are invisible in a diff — they are found by enumerating what the system claims to enforce and testing the gaps.
- **A finding is not finished when it is patched.** The instance dies with the fix; the class does not. Reporting, custody, and the decision not to publish all have their own discipline.
- **A result that looks too good is a bug report.** In every other domain a defect makes something fail; leakage makes everything look better, so the alarm has to be inverted.
- **A fix proves the past, not the present.** That someone fixed it means they fixed that, and nothing else — the patched file is the least-reviewed code in the repository and the likeliest place for the next bug.

---

## Related

- [vigia-intent-analysis](https://github.com/annatchijova/vigia-intent-analysis) — VIGÍA forensic intent analysis engine (SANS FIND EVIL Hackathon 2026). These skills encode its engineering invariants.

---


                    ┌─────────────────────────┐
                    │     INQUIRY / REASONING │
                    │                         │
                    │ abductive-engineering   │
                    │ diagnosing-bugs         │
                    │ software-archaeology    │
                    │ reverse-engineering     │
                    │ invariant-hunting       │
                    │ concurrency-reasoning   │
                    │ beyond-the-sink         │
                    │ beyond-the-fix          │
                    │ forensic-persistence    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   ADVERSARIAL VALIDATION│
                    │                         │
                    │ attack-surface-triage   │
                    │ red-team-auditing       │
                    │ discriminating-proof    │
                    │ authorization-surface   │
                    │ parser-differential     │
                    │ oracle-driven-fuzzing   │
                    │ assume-breach-modeling  │
                    │ purple-team-exercise    │
                    │ detection-engineering   │
                    │ falsifiable-testing     │
                    │ remediation-reporting   │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             ▼                   ▼                   ▼
       INTEGRITY            TRUST / DATA          EVIDENCE
       deterministic       validate-boundary      provenance
       audit-chain         honest-degradation     timeline
       atomic mutation     secret lifecycle       logging
       schema evolution    dependency provenance  decision records
                           resource exhaustion
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ▼
                       CONSTRUCTION / CHANGE
                                 │
                  secure-by-construction
                  surgical-patcher
                  audit-before-patch
                  git-discipline
                  irreversible-action-gate

                    MACHINE LEARNING
                    (the same discipline, where the
                     test is a metric and the data
                     is the program)

                  data-leakage-hunting
                  training-run-provenance
                  model-evaluation-discipline
                  training-serving-parity
