---
name: diagnosing-bugs
description: Disciplined diagnosis loop for hard bugs and performance regressions — build a tight feedback loop FIRST, then hypothesize, never the reverse. Use when the user says "diagnose"/"debug this"/"why does this fail"/"it's broken"/"it's slow", or reports something throwing/failing/flaky/wrong. Complements abductive-engineering (which supplies the reasoning framework — A-D-I loop, semiotic triad) with the operational mechanics that turn that framework into a repeatable debugging process. Where abductive-engineering says "abduce rival hypotheses", this skill says "here is how: build a red-capable loop first, rank 3-5 hypotheses before testing any, instrument one variable at a time, tag every probe, and ask what would have prevented this." Sixth member of the family (abductive-engineering, secure-by-construction, software-archaeology, red-team-auditing, daubert-defensible-writing) — this one governs the operational mechanics of finding and fixing defects.
---

# Diagnosing Bugs

An operational discipline for hard bugs. `abductive-engineering` supplies the engine (A-D-I loop, Peirce's inference triad); this skill supplies the gears — the concrete steps, checkpoints, and anti-patterns that turn abductive reasoning into a repeatable debugging process.

It exists because the single most common debugging failure mode is **jumping to a hypothesis before having a feedback loop that can falsify it.** A developer reads the code, forms a plausible story ("it's probably the race condition in the connection pool"), and starts editing — without ever running the bug. When the edit doesn't work, they form another story. This is narrative debugging, and it is the opposite of inquiry.

> **The prime directive: a tight, red-capable feedback loop comes before any hypothesis.** If you have one, you will find the bug. If you don't, no amount of code-reading will save you.

---

## Phase 1 — Build a Feedback Loop

**This is the skill.** Everything else is mechanical. Spend disproportionate effort here.

A feedback loop is a single command — a script, a test invocation, a curl — that:
- **Goes red** on this specific bug (not "runs without erroring" — it catches *this* symptom)
- **Is deterministic** (same verdict every run; for flaky bugs: a pinned, high reproduction rate)
- **Is fast** (seconds, not minutes)
- **Is agent-runnable** (no human in the loop unless absolutely unavoidable)

### Ways to construct one — try in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **CLI invocation** with a fixture input, diffing output against a known-good snapshot.
3. **Replay a captured trace.** Save a real input/payload/event to disk; replay it through the code path in isolation.
4. **Throwaway harness.** Spin up a minimal subset that exercises the bug path with a single function call.
5. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
6. **Bisection harness.** If the bug appeared between two known states, automate "boot at state X, check, repeat" so you can `git bisect run` it.
7. **Differential loop.** Same input through old-version vs new-version, diff outputs.

### Tighten the loop

Once you have *a* loop, **tighten** it:
- Can I make it faster? (Cache setup, skip unrelated init, narrow scope.)
- Can I make the signal sharper? (Assert the specific symptom, not "didn't crash.")
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop 100x, parallelize, add stress, narrow timing windows, inject sleeps. A 50%-flake is debuggable; 1% is not — keep raising the rate.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for:
(a) access to whatever environment reproduces it,
(b) a captured artifact (log dump, core dump, screen recording with timestamps), or
(c) permission to add temporary production instrumentation.

**Do not proceed to Phase 2 without a loop.** If you catch yourself reading code to form a theory before the loop exists, that is the exact failure this skill prevents.

### Completion criterion

Phase 1 is done when you can name **one command** you have **already run at least once** (paste the invocation and its output) that satisfies all four properties above.

---

## Phase 2 — Reproduce + Minimize

Run the loop. Watch it go red.

Confirm:
- The loop produces the failure the **user** described — not a nearby but different failure. Wrong bug = wrong fix.
- The failure is reproducible across multiple runs.
- You captured the exact symptom (error message, wrong output, timing) so later phases can verify the fix addresses it.

### Minimize

Shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running after each cut. Keep only what is load-bearing for the failure.

Why: a minimal repro shrinks the hypothesis space in Phase 3 and becomes the regression test in Phase 5.

Done when **every remaining element is load-bearing** — removing any one makes the loop go green.

---

## Phase 3 — Hypothesize (Ranked, Before Testing)

Generate **3-5 ranked hypotheses** before testing any of them.

This is the phase where `abductive-engineering` supplies the reasoning: each hypothesis is a Peircean abduction ("the surprising fact C is observed; if A were true, C would be a matter of course; hence there is reason to suspect A"). But the operational discipline this skill adds is:

1. **Generate multiple hypotheses first** — single-hypothesis generation anchors on the first plausible idea. Force yourself to at least 3.
2. **Each must be falsifiable** — state the prediction it makes:

> "If [X] is the cause, then [changing Y] will make the bug disappear / [changing Z] will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

3. **Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they have already ruled out. Cheap checkpoint, big time saver. Proceed with your ranking if the user is AFK.

4. **Test one hypothesis at a time.** Never "try a few things at once and see what sticks." Each probe must map to a specific prediction.

---

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

### Tool preference

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep."

### Tag every debug probe

**Every debug log, print, or instrumentation line gets a unique prefix:**

```python
logger.debug("[DBG-b127] prior_trust raw value: %r", raw)
```

At cleanup, one grep removes them all: `grep -rn "DBG-b127"`. Untagged logs survive; tagged logs die. This prevents the insidious accumulation of "temporary" debug output that nobody remembers to clean up.

### Performance bugs

For regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, profiler, query plan), then bisect. **Measure first, fix second.**

---

## Phase 5 — Fix + Regression Test

Write the regression test **before the fix** — but only if there is a correct seam for it.

A correct seam exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (unit test that cannot replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it — the codebase architecture is preventing the bug from being locked down.

If a correct seam exists:

1. Turn the minimized repro into a failing test.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original (un-minimized) scenario.

### Boundary tests

When the fix involves a threshold, limit, or comparison operator (< vs <=, > vs >=), **always add a test case at the exact boundary value** — not just below and above, but *on* the boundary itself. This is the class of bug that only appears at exact boundary values and is invisible to any test that uses values safely away from the edge.

---

## Phase 6 — Cleanup + Post-Mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DBG-xxxx]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway harnesses deleted
- [ ] The hypothesis that turned out correct is stated in the commit message

### The prevention question

**Then ask: what would have prevented this bug?**

- If the answer is a missing test: write it now (the prevention test catches *the class*, not just this instance).
- If the answer is an architectural gap (no good test seam, tangled callers, hidden coupling): hand off to `/software-archaeology` or `/codebase-health-assessment` with the specifics.
- If the answer is a process gap (no review caught it, no CI check covers it): document it.

---

## Anti-Patterns to Name and Correct

- **Narrative debugging** — reading code and forming a theory before having a feedback loop. Phase 1 exists to prevent it.
- **Single-hypothesis anchoring** — the first plausible idea becomes the only one investigated. Phase 3 requires 3-5 ranked alternatives.
- **Shotgun instrumentation** — "log everything and grep" instead of targeted probes mapped to specific predictions.
- **The fix-without-a-test** — applying the fix, watching it "seem to work", declaring victory.
- **Zombie debug output** — temporary prints left in the codebase because nobody remembers which lines were debug. The `[DBG-xxxx]` tagging convention prevents this.
- **Collateral fix** — while debugging X, noticing Y is also wrong and fixing both in one commit. Report Y as a finding; fix it separately.
- **Boundary blindness** — testing with values safely away from thresholds, missing bugs that appear only at exact boundary values.

---

## How to respond when this skill is active

- Never form a hypothesis before the feedback loop exists.
- Generate 3-5 ranked hypotheses before testing any. Show them to the user. Test one at a time.
- Tag every debug probe with a unique prefix. Remove them all before declaring done.
- Write the regression test before the fix. Add a boundary test when the fix involves a comparison operator.
- State the winning hypothesis in the commit message. Ask what would have prevented this.
- When this skill and `abductive-engineering` are both active, this skill governs the operational steps; `abductive-engineering` governs the reasoning framework. They do not conflict.
