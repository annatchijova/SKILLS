---
name: beyond-the-fix
description: Audit the bug fixes themselves — a patch proves that someone knew something was wrong there, never that it is now right. Hunt the eight ways a fix falls short: it covers the demonstrated input instead of the property, one path instead of every path, the wrong layer, the symptom instead of the cause, nothing enforcing it against the next caller, a new bug introduced by the rushed diff, siblings left unpatched, or a fix that has since decayed. Use whenever a fix, patch, advisory, CVE, changelog entry, or "closed as fixed" issue is in view, and whenever an area looks safe because it was already fixed once. Trigger on "audit the fixes", "is this patch complete", "variant analysis", "patch diffing", "they fixed it", "incomplete fix", "regression", "this was already patched", "check the CVE", "look near old fixes", or a security commit in the log. Sibling of beyond-the-sink — that skill looks past the scanner's map, this one looks past the fixer's.
---

# Beyond the Fix

A patch is the highest-signal artifact in any repository. Someone already did
the expensive part: they found the class, located the file, and wrote down what
they believed was wrong. What they did not do — because nobody does — is keep
looking after the tests went green.

The thesis, in one line:

> **That someone fixed it means they fixed that, and nothing else.**

A fix is evidence about the *past*: something was wrong here, and a human
confirmed it. It is not evidence about the present. Those are different claims,
and the entire discipline of this skill lives in the gap between them.

Three biases produce that gap, and all three are structural rather than
personal:

1. **Attention collapses at green.** The search terminates the moment the
   reporter's PoC stops reproducing. That oracle — *my one input no longer
   works* — is the weakest oracle in existence: it tests an input, not the
   property (`falsifiable-testing`).
2. **The frame came from the reporter.** The fixer inherited the demonstrated
   path and fixed the demonstrated path. Whatever the reporter did not think of,
   the fix does not cover.
3. **A fixed area repels review.** The file now carries a mark that says
   *already looked at*, usually by the person who understood it best. It becomes
   the safest-looking code in the repo, and it is the code most likely to hold
   the next bug. Security fixes ship under time pressure and get *less* review
   than ordinary features, not more.

This is not a hypothesis about how people work. Project Zero's tracking of
exploited-in-the-wild 0-days has repeatedly found that a large share of them
each year are variants of previously patched bugs. The exact fraction moves;
the pattern does not.

Composes with the library:

- **beyond-the-sink** — the sibling; its Part 3 (a root class is a template)
  is this skill's engine, applied systematically to fix history
- **invariant-hunting** — name the property the fix was *attempting* to
  establish, then ask whether it holds
- **discriminating-proof** — the pre-fix / post-fix control in Part 4
- **software-archaeology** — reconstructing intent from a diff whose author is
  unavailable
- **audit-before-patch** — the fix you are auditing must be confirmed present
  in the live code before anything is built on it
- **remediation-driven-reporting** — the report that gets the class fixed this
  time, referencing their own prior fix
- **falsifiable-testing** — the regression test that stops the fix from decaying

Scope: your own repositories, authorized targets, and public patches of open
source. Reading a public diff is research; probing someone's production because
the diff suggested something is not, and needs the same authorization as any
other test.

---

## Part 1 — Reconstruct the bug from the diff, not from the advisory

The advisory is the vendor's framing, written to be reassuring and to reveal as
little as is polite. The diff is the fact. Start there, always, and derive what
must have been possible *before* the change.

Then extract the thing that makes this skill work:

> **The fix encodes the author's mental model of the bug. The gap between that
> model and the real system is where the next bug is.**

Read the fix for its model, and the model predicts what else was missed:

| The fix looks like | Their model was | So they probably did not consider |
|---|---|---|
| blocking `../` and `%2e%2e` | "the attack is a string pattern" | resolution, symlinks, Unicode, the second decode |
| a check added in one handler | "the bug is in this handler" | every other caller of the same primitive |
| a length check before a copy | "the bug is this buffer" | the other three copies from the same source |
| `try/except` around the crash | "the bug is the exception" | the state the failed operation left behind |
| escaping at output | "the bug is display" | the stored value, and every other consumer of it |
| a new role check in the UI route | "the bug is who can click" | the API, the batch job, the CLI, the internal caller |

This is the abductive step (`abductive-engineering`): the patch is a *sign*, its
object is the author's belief, and the interpretant you want is the region their
belief did not cover.

## Part 2 — The eight ways a fix falls short

Name the family before searching. Each has a distinct search.

1. **It covers the input, not the property.** They rejected the reporter's exact
   payload, encoding, or id. Search: the next member of the class — another
   encoding layer, a different normalization, an equivalent value.
2. **It covers one path, not every path.** Sync patched, async not. The v2
   handler patched, v1 still routed. The interactive path patched; the batch,
   import, retry, streaming, replay, admin, and CLI paths untouched. Search:
   every path that reaches the same sink.
3. **It is at the wrong layer.** Patched where the bug was *observed* rather
   than where the property should be *enforced* — so every other caller of the
   same primitive still has it. This is the highest-yield family, because the
   fix is genuinely correct and genuinely local.
4. **It suppresses the symptom.** A `catch`, a retry, a clamp, a default. The
   operation no longer crashes; it now fails silently, and the corrupt state it
   leaves behind is a new problem (`honest-degradation`). Search: what does the
   system do *after* the suppressed failure?
5. **It is correct but unenforced.** The right check exists, and nothing stops
   the next contributor from adding a caller that skips it. No test, no type, no
   chokepoint. Search: how many callers exist, and what makes a new one safe?
6. **It introduced a new bug.** The diff was written fast, under pressure, by
   someone tired, and reviewed deferentially because they were the expert.
   Off-by-one in the new bound, a null path that did not exist before, a
   TOCTOU between the new check and the old use, a lock now held across I/O.
   **Read the fix diff adversarially as new code, because that is what it is.**
7. **Siblings were left unpatched.** Other implementations, other languages,
   other services, forks, vendored copies, the same function copy-pasted twice.
   Coordinated fixes almost never reach every implementation
   (`beyond-the-sink` Part 3's existence and behavior gates).
8. **It decayed.** The fix landed and no longer exists: a refactor moved the
   check to the wrong side of a branch, a performance patch added a fast path
   that skips it, a merge dropped it, a rewrite reimplemented the function
   without it. Search: does the check still exist at HEAD, and is it still on
   every path it used to cover?

Family 8 deserves a habit of its own: **for every historical fix you care
about, verify it is still present today.** Fixes with no regression test are the
ones that decay, and a decayed fix is a live bug with a closed ticket in front
of it.

## Part 3 — Where fixes announce themselves

The fix history is a map of where the authors already bled. Mine it:

- Commit messages: `fix`, `security`, `CVE`, `bypass`, `sanitize`, `escape`,
  `validate`, `harden`, `overflow`, `injection`, `regression`, `hotfix`.
- Advisories, CVE records and their patch commits; changelog and release notes;
  issues closed as fixed; your own past reports.
- **Suspiciously terse messages on sensitive files** — "minor cleanup" on a
  parser, "refactor" on an auth path. A silent security fix looks exactly like
  this, and it is the highest-value commit in the log.
- **Clusters.** Three fixes in one file over two years is not three incidents,
  it is one structural problem that has been patched three times. Fix density
  is the single best predictor of the next bug's location.
- **Velocity tells.** A fix landed within hours of a report, in a file its
  author does not usually own, is a rushed fix by definition.

And the rule inherited from `beyond-the-sink`: **dig adjacent to old fixes, not
on top of them.** The exact bug is the one place that is genuinely well tested
now. The neighbors are not.

## Part 4 — The pre-fix control makes the verdict unambiguous

When you have a candidate, run it against **three** versions, not one. This is
the discriminating experiment for this whole skill:

| Candidate behaves as | Pre-fix build | Post-fix build | Verdict |
|---|---|---|---|
| the original bug | works | works | **the fix never covered this path** — family 1, 2, 3 or 7 |
| the original bug | works | blocked | the fix holds here; record it as terrain |
| a new failure | clean | works | **the fix introduced it** — family 6 |
| nothing | clean | clean | refuted; log it (`forensic-persistence`) |

That table is why the pre-fix build is worth the trouble of checking out: it
separates *never fixed* from *newly introduced*, which are different findings,
with different severities, reported to different people, with different fixes.
Without it you have an observation and a guess about its origin.

Then apply the epistemic ladder as usual — a surviving path found by reading is
`PLAUSIBLE` until it is run (`discriminating-proof`).

## Part 5 — The report writes itself, and the blue fix is a chokepoint

An incomplete-fix finding is often *stronger* than a novel bug report, and it
is certainly easier to land:

- **The vendor already agreed it is a security issue.** They fixed it once.
  The entire "is this really a vulnerability" argument is pre-settled — cite
  their own commit or advisory.
- **Name the family** from Part 2 and show the specific surviving path. "The
  fix is incomplete" without a demonstrated survivor is an opinion.
- **Propose the chokepoint**, not another point fix — otherwise you are filing
  the same report again in six months, which is precisely the loop this skill
  exists to break (`remediation-driven-reporting` Part 3).

The defensive deliverable, for your own repos:

1. **A regression test per fix**, asserting the *property*, not the reporter's
   input. A fix with no test is a fix with an expiry date.
2. **A decay check**: a test that fails if the check is removed or bypassed —
   the only thing that catches family 8 before an attacker does.
3. **A post-fix review pass as policy.** The security fix diff gets *more*
   scrutiny than a feature diff, not less. Right now the opposite is true
   everywhere.
4. **A fix-cluster review.** When one file collects its third fix, stop patching
   it and redesign the boundary.

---

## Deliverable

```
## Fix audit — <component> — fixes reviewed: <n>
| fix / commit / CVE | invariant it attempted | families checked | outcome |

### Findings
<id> — family (1–8) — the surviving path — pre-fix/post-fix control result
     — epistemic level — the prior fix it references

### Fixes verified complete
<recorded as terrain: what was traced, which paths, what enforces it>

### Decayed fixes
<fix, when it landed, what removed or bypassed it, whether it is live now>

### Structural proposal
<chokepoint + regression tests + decay checks>

### Not reviewed
```

## Anti-patterns

- Reading the advisory instead of the diff, and inheriting the vendor's framing
  of what the bug was.
- Re-running the original PoC against the patched build and concluding the fix
  is complete — that is the fixer's own weak oracle, borrowed.
- Assuming the fix's location is the correct location for the property.
- Never checking whether a historical fix still exists at HEAD.
- Treating the fix diff as reviewed code. It is the least-reviewed code in the
  repository.
- Skipping the pre-fix control, and so being unable to distinguish "never
  covered" from "introduced by the fix".
- Digging on top of the exact bug that was fixed — the one spot now covered by
  a test — instead of adjacent to it.
- Reporting "the fix is incomplete" without a demonstrated surviving path.
- Accepting a second point fix for the same file, and scheduling your own next
  report.
- Recording a verified-complete fix nowhere, so the next auditor re-does the
  work you already did.
