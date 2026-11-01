---
name: variant-analysis
description: "Turn one disclosed or found bug into a family: extract the violated invariant, hunt the same class across shared deps and sibling sinks, and check dedupe/fix-coverage before filing."
---
 
# Variant analysis: one bug into a family
 
A disclosed vulnerability is a lead, not a finding. The value is the *invariant it violates*, which recurs in code the original author never touched. This skill turns a single disclosure — or a single bug you just found — into a queue of independent, confirmable variants, and settles the duplicate question up front.
 
## Trigger
Use whenever the input is a known bug (MSRC/CVE/ZDI advisory, a fix commit, a public writeup) or one bug you found, and the goal is to find the same class elsewhere; when the user says "where else", "bug family", "pattern", "variant", "is this a dup"; or when checking whether a fix is complete.
 
## Steps
1. **Get the real pattern, not the advisory blurb.** MSRC/CVE text is thin (versions + credit, rarely root cause). The pattern lives in the *fix diff*, the finder's writeup, or the ZDI advisory. Locate the patch and ask: what guarantee did the fix restore?
2. **Abstract to an invariant, not a string.** Express the bug as `sink + precondition + violated invariant + shape of the bypass`, in one queryable sentence. Example: "a safety validator runs once before the sink and is not re-run after a state change (redirect, in-page fetch) that can invalidate its result." Not "grep for `page.goto`."
3. **Rank the transfer surface.** Highest yield first:
   - **Shared OSS dependency** both codebases consume → literally the same vulnerable code. Confirm with the lockfile/SBOM (see `dependency-provenance`). This is where cross-vendor duplication is *literal*.
   - **Same-class sink in a different codebase** → the anti-pattern, not the code. Cross-vendor hunts (e.g. a Microsoft disclosure → a Google repo) mostly live here.
   - **Sibling call sites in the same codebase** → other headers, params, entry points. This is the incomplete-fix / bypass angle.
4. **Query, don't eyeball.** Encode the invariant as CodeQL / Semgrep / a structural query. Enumerate *every* call site of the sink and test each against the precondition. A no-hit is a recorded result, not a skip.
5. **Confirm each candidate independently.** A pattern match is a lead. Hand each to your reproduction discipline (`red-team-auditing`) before it earns CONFIRMED. Never batch-assert a whole cluster as real.
6. **Settle dedupe BEFORE it becomes a report.** For each confirmed variant ask: (a) is this exact instance already reported to this program or already fixed? (b) does the existing fix already cover this path? Only "no" to both is a fresh report. A variant in a *different vendor/program* is never a duplicate — the disclosure is prior art. In the report, cite the lead explicitly ("variant of CVE-X; the fix at commit Y does not cover Z because…") — that framing turns resemblance into impact evidence and pre-empts the "incomplete fix" question.
## Verification
- Every candidate traces to a one-sentence invariant and to the specific call sites you queried (hits and no-hits both recorded).
- Each confirmed variant has an independent repro, not just a match.
- Dedupe + fix-coverage checked and written down per variant before any report is drafted.
- The report names its prior-art lead.
## Composes with
`dependency-provenance` (shared-dep transfer + reachability), `red-team-auditing` (earn CONFIRMED), `attack-surface-triage` (rank the candidate queue), `daubert-defensible-writing` (the writeup), and `dont-fall-in-love-with-the-bug` (this skill is that skill's variant-sweep step).
