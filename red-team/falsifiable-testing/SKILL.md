---
name: falsifiable-testing
description: Write tests that can actually fail, and prove it — see the test red before you trust it green, break the code deliberately as a negative control, and strengthen the oracle from "it ran" to "it is right". Use whenever tests are being written, reviewed, fixed, or relied on: "add tests for this", "write unit tests", "the tests pass", "improve coverage", "this test is flaky", "why didn't the tests catch this", "mock this out", "update the snapshot", or a PR whose diff adds test files. Also trigger when a bug reached production through a tested code path, when a test suite is being used as evidence that a change is safe, or when coverage numbers are cited as quality. Covers oracle strength, negative controls, mock discipline, flake diagnosis, and the tests-that-cannot-fail taxonomy. It does not pick frameworks and does not chase coverage percentages.
---

# Falsifiable Testing

A test is an experiment, and an experiment that cannot come out the other way
measures nothing. Most useless tests are not wrong — they are unfalsifiable:
they would pass on correct code, on broken code, and on no code at all. They
accumulate quietly, and the suite's green becomes a ritual rather than evidence.

In the Peircean loop this skill governs **induction**: the step where a
prediction meets the world. A test is the apparatus. Its assertion is the
**oracle** — the thing that decides right from wrong. Weak oracle, weak
induction, no matter how many tests there are.

The one rule that generates most of the others: **never trust a test you have
not seen fail.**

Composes with the library: `diagnosing-bugs` (the red-capable loop comes first),
`abductive-engineering` (test = induction), `honest-degradation` (a test that
can't tell "passed" from "skipped" lies), `deterministic-core` (flakes are
nondeterminism you haven't found yet), `software-archaeology` (a
characterization test is how you pin behavior you don't understand yet).

---

## Part 1 — See it red first

Before a test counts as evidence, it must have failed at least once for the
reason it exists:

- **New behavior**: write the test, run it, watch it fail, then implement. The
  classic red-green loop is not a workflow preference — the red run is the only
  proof the test is wired to the thing it claims to check.
- **Bug fix**: reproduce first. The regression test must fail on the unfixed
  code. A regression test written after the fix, never seen red, frequently
  tests the wrong path and would not have caught the original bug.
- **Existing test you inherited**: break the code under it deliberately and
  confirm it goes red. Put the code back. This takes thirty seconds and is the
  fastest audit of a suite you did not write.

If the test cannot be made to fail, it is not testing what you think it is.
Investigate that before adding another one.

---

## Part 2 — The taxonomy of tests that cannot fail

Learn to recognize these on sight; they are the bulk of decorative suites.

| Antipattern | What it looks like | Why it can't fail |
|---|---|---|
| **No assertion** | Calls the function, ends | Only crashes fail it. Half the code paths return wrong values without crashing. |
| **Existence oracle** | `assert result is not None`, `assert len(x) > 0` | Passes on any non-empty garbage. |
| **Mock asserting the mock** | Stub returns `42`, test asserts the result is `42` | Verifies the test's own arrangement. The real code could be deleted. |
| **Tautology** | Recomputes the expected value with the same code the test exercises | Both sides move together; a wrong formula stays "correct". |
| **Blessed snapshot** | `--update-snapshots` run, output committed unread | Records current behavior, including the bug. |
| **Swallowing wrapper** | `try: ... except Exception: pass` inside the test | Converts every failure into a pass. |
| **Untriggered branch** | The test's input never reaches the condition it names | Renaming the test would change nothing. |
| **Time/order dependent pass** | Passes because of execution order or a leftover fixture | Fails alone; passes in suite. Or the reverse — worse. |
| **Skipped in CI** | `@skip`, an env guard, an excluded path | Reports as "not failed", read by humans as "passed". |

The last one deserves emphasis: in most reporting, **skipped is rendered as
not-red**, and not-red is read as verified. Any test skipped in the environment
that gates merges is coverage you do not have. Count skips explicitly, with a
reason and an owner, or delete them.

---

## Part 3 — The negative control (mutation on the cheap)

The rigorous version of "see it red" is **mutation testing**: change the code in
a small, semantically real way and check that some test notices. You do not need
a mutation framework to get most of the value — do it by hand, at the moment of
writing, on the code you just wrote:

1. Invert a comparison (`>` → `>=`).
2. Replace a return value with a plausible neighbor (a constant, an empty list).
3. Delete a validation branch.
4. Skip one step of a multi-step operation.

If nothing goes red, the oracle is too weak or the case is unreached. Fix the
test, then revert the mutation. Keep the mutation list in the PR description when
the code is consequential — it is the cheapest possible evidence that the suite
has teeth, and it is far more informative than a coverage delta.

**Coverage is a map of what was executed, not what was verified.** A line covered
by an assertion-free test is 100% covered and 0% tested. Cite coverage only as
what it is: a lower bound on unreached code, useful for finding blind spots,
worthless as a quality claim.

---

## Part 4 — Strengthen the oracle

Oracles form a ladder. Climb until the rung matches the consequence of being
wrong, then stop — over-specifying is its own failure mode (a brittle test that
fails on every irrelevant change trains people to ignore red).

1. **It ran** — no exception. Weakest useful rung; fine as a smoke test, never as
   the only test of a computation.
2. **Shape** — type, length, keys, schema. Catches structural breakage.
3. **Invariant** — a property that must hold for *all* valid inputs: the sum is
   conserved, the output is sorted, encode∘decode is identity, no duplicate IDs.
   Invariants are the highest value-per-line in most suites.
4. **Exact value** — the known-correct answer, computed independently of the code
   under test (by hand, from a spec, from a reference implementation). If you
   computed the expected value *with* the code, you are back at tautology.
5. **Property / metamorphic** — relations that hold across inputs even when no
   single expected value is known: `f(sorted(x)) == f(x)`, doubling the input
   doubles the count, a permutation does not change the verdict. This is the
   right tool when the correct answer is hard to state but its behavior isn't —
   scoring functions, parsers, optimizers, anything numeric.

**Test the boundary, the empty case, and the hostile case.** Most defects live at
zero, one, off-by-one, empty, null, duplicate, and "the thing the caller was
never supposed to pass". A suite of happy paths tests the demo, not the system.

**Assert the error, not just the exception type.** `pytest.raises(ValueError)`
passes when a *different* `ValueError`, from a different line, fires for a
different reason — often exactly the reason your fix was supposed to eliminate.
Match the message or the error identity, and assert the state afterwards
(nothing partially written, nothing left locked).

---

## Part 5 — Mocks: what they buy and what they cost

A mock replaces a dependency with an assumption. The assumption is now untested
and, worse, frozen: when the real dependency changes shape, the mock keeps
agreeing with the old world and the suite stays green through a real breakage.

- Mock the **boundary** (network, clock, filesystem, payment provider), not the
  interior. Mocking your own modules mostly tests your ability to write mocks.
- If you mock a contract, **test the contract somewhere** — one integration or
  contract test that runs against the real thing, even if it runs nightly rather
  than per-commit. Otherwise the mock is a permanent untested assumption.
- Assert on the **interaction that matters** (was the charge issued exactly once,
  with this amount) rather than on incidental call counts, which break on
  refactors and teach nothing.
- Prefer **fakes** (a small real implementation: in-memory store, fake clock) to
  mocks. A fake can be wrong once, centrally, and fixed once. Mocks are wrong
  independently in fifty files.
- A test whose arrange block is longer than the system's real call site is
  telling you about a design problem, not a testing problem.

---

## Part 6 — Flakes are findings

A flaky test is a **true report of nondeterminism** in the test, the code, or the
environment. Retry decorators do not fix it; they delete the report and leave the
nondeterminism in production, where it will surface as an incident that "the
tests never caught".

Diagnose along the usual suspects (this is `diagnosing-bugs` applied to the
suite): shared state between tests, execution order, real clocks and timezones,
real network, unseeded randomness, concurrency and timing assumptions, resource
exhaustion, or a genuine race in the code under test — the most valuable case,
and the one retries hide most effectively.

If you must quarantine, quarantine with a receipt: a hypothesis, an owner, an
expiry date, and a visible count. A quarantine list with no expiry is a list of
things that will be broken forever, and the second entry costs nothing to add
once the first has been tolerated.

---

## Deliverable checklist

```markdown
## Test integrity

Red-first: each new/changed test observed failing for its intended reason → yes/no
Negative control: mutations applied → which tests caught them
Oracle level: existence | shape | invariant | exact | property   (matched to consequence)
Boundaries covered: empty / zero / one / off-by-one / duplicate / hostile input
Mocks: what is mocked, what assumption that freezes, where the contract is tested for real
Skips & quarantines: count, reason, owner, expiry
Known blind spots: what this suite would NOT catch (stated, not implied)
```

That last line is the one that makes the suite honest. Every suite has a shape it
is blind to; writing it down is the difference between "tests pass" and "tests
pass, and here is what that does and does not mean".

---

## How to respond when this skill is active

- Before writing a test, ask what would make it fail; if there is no clean answer, the test is not ready to write.
- For a bug fix, reproduce first and show the test red on the unfixed code — always, even under time pressure. Especially then.
- Run at least one hand mutation against new logic and report which test caught it.
- Refuse to present coverage percentage as evidence of quality; report unreached code and unverified paths instead.
- Name the antipattern when you see it ("this asserts the mock's return value, not the code's behavior") and offer the stronger oracle rather than deleting the test.
- Treat a flake as a defect report with a hypothesis, never as a candidate for a retry decorator.
- When a suite is green and something broke anyway, ask which of the nine antipatterns let it through — that is the real bug, and it is in the suite.
