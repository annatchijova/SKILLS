---
name: codebase-health-assessment
description: Systematic assessment of a codebase's living, dead, and fossil modules — scan, categorize, prioritize, act. Use when the user says "audit the codebase", "find dead code", "what can we delete", "clean up the repo", "module archaeology", "codebase health", "what's unused", "technical debt inventory", or when a project has accumulated enough history that nobody is sure which modules are live and which are orphaned. Also trigger when the user asks "is this module still used?", "why do we have two copies of X?", or "what would break if I deleted Y?". Complements software-archaeology (which governs safe *modification* of individual modules) — this skill governs the *assessment* phase that decides which modules deserve that careful modification, which are candidates for bulk removal, and which need to be left alone with documentation. If software-archaeology is the surgeon, this skill is the triage nurse.
---

# Codebase Health Assessment

A methodology for scanning a codebase at the *module* level — not individual lines or functions, but whole files and namespaces — to answer: what is alive, what is dead, what is dangerous, and what should be done about each.

It exists because mature codebases accumulate modules faster than they retire them. Every feature added, every refactor attempted, every hackathon prototype committed leaves artifacts. Over months and years, the ratio of live code to fossil code degrades silently until nobody is confident about what is safe to touch, what is safe to delete, and what looks dead but is load-bearing.

The prime directive:

> **Classify before acting. Act by classification, not by intuition.** A module that "looks dead" may be load-bearing through paths invisible to grep. A module that "looks important" may have been superseded and never cleaned up. The classification phase produces evidence; the action phase consumes it.

---

## Part 1 — Scope and Index

### Establish the population

Count the files. Not lines, not functions — files. The unit of assessment is the module (one `.py`, `.rs`, `.java`, `.ts` file), because that is the unit of deletion, the unit of `git rm`, and the unit that appears in import graphs.

```bash
find . -name "*.py" -not -path "./.venv/*" -not -path "./node_modules/*" | wc -l
```

This number is the denominator of every percentage that follows. Write it down.

### Build the temporal index

The most valuable signal for health assessment is **recency of last meaningful commit**. Not last modification (a formatter touching every file is noise) — last commit that changed the module's *logic*.

```bash
git log --format="%H %ai" --diff-filter=M -- <file>
```

Modules untouched for 60+ days in an actively developed project are candidates for deeper inspection. 90+ days is a strong fossil signal. But recency alone is not sufficient — a module committed yesterday can be dead on arrival (a prototype that was never wired in).

### Unshallow the history

If the repository was cloned with `--depth`, the temporal index is unreliable — `git fetch --unshallow` before trusting any date-based classification. A module that appears "60 days old" in a shallow clone may actually be 6 months old in the full history.

---

## Part 2 — Classification

Every module gets exactly one classification. The categories below are ordered from most to least urgent to act on.

### FOSSIL_HIGH_RISK

**Definition:** The module was designed to participate in the decision path (scoring, verdict, gate, validation) but is not wired in — no live caller reaches it. Its *existence* is a risk because someone might wire it in without realizing it was never hardened, tested against the full corpus, or reviewed for correctness.

**Signals:**
- Contains logic that computes a score, verdict, classification, or gate decision
- Zero callers in `grep -rn` across the full repo (not just one directory)
- Has its own unit test that passes in isolation — giving false confidence
- May have known defects (floats in a Fraction-only path, stubs that return hardcoded values, inverted logic)

**Action:** Audit individually. Either wire in (with full test + corpus validation) or document as "designed but not integrated, pending [specific dependency]." Never leave a FOSSIL_HIGH in the repo without documentation explaining why it exists and what blocks its integration.

### DEAD_WEIGHT

**Definition:** The module is confirmed dead — zero callers, zero importers, no config-driven dispatch, no reflection, no cron. Its content has been superseded by another module or was a prototype that was never adopted.

**Signals:**
- Zero callers across all search methods (grep, AST analysis, config files, CLI entry points)
- A newer version of the same functionality exists elsewhere (v2 replaced v1, but v1 was never deleted)
- Byte-for-byte identical to another file (copy that was never diverged)
- Explicitly prohibited by project policy (e.g., shadow modes, deprecated patterns)

**Action:** Bulk delete with documentation. Group related dead modules into a single commit with a clear commit message listing every file and the reason for deletion. Run the full test suite after deletion — a test failure means the module was not actually dead (reclassify as CONNECTED_ALIVE).

### The Deletion Test

Before classifying anything as DEAD_WEIGHT, apply the deletion test:

> **Would deleting this module concentrate complexity somewhere useful, or would it just move it?**

If deletion would force the remaining code to handle something the deleted module was handling (even poorly), the module is not dead — it is *shallow* (interface nearly as complex as its implementation) and may deserve deepening, not deletion.

If deletion would simply remove code that nothing reaches, with no ripple effect on any other module, it is genuinely dead.

### FOSSIL_LOW_RISK

**Definition:** The module is old and disconnected, but its content is not dangerous — it does not participate in decisions, does not have security implications, and its existence does not mislead. Often documentation, utility helpers, or configuration templates.

**Action:** Low priority. Delete if doing a bulk cleanup; otherwise, leave with a note.

### CONNECTED_ALIVE

**Definition:** The module has live callers, is actively imported, and participates in the real execution path. It may still have problems (technical debt, poor design, missing tests), but it is not a health assessment finding — those problems are the domain of `/software-archaeology` or `/red-team-auditing`.

**Action:** None from this skill. Note any concerns as findings for other skills.

### DUPLICATE

**Definition:** Two or more modules implement the same functionality, often with slight divergence. One is canonical (actively maintained, properly hardened); the others are copies that were never cleaned up after a refactor or consolidation.

**Signals:**
- Similar or identical file names in different directories
- Same class/function names with different implementations
- One has hardening (input validation, error handling, security checks) and the other does not
- The less-hardened version may still have callers that should be migrated

**Action:** Identify the canonical version. Migrate callers of the non-canonical version. Delete the non-canonical version. Document as a name-collision or consolidation finding.

---

## Part 3 — The Assessment Report

Produce a structured report — not prose, not a flat list. The report serves two audiences: the developer who will act on it today, and the developer who will audit it six months from now.

### Required sections

1. **Population summary** — total modules scanned, breakdown by classification, percentage of codebase that is alive vs fossil/dead.
2. **High-risk findings** — every FOSSIL_HIGH_RISK module, with: file path, what it does, why it is high-risk, what blocks its integration, recommended action.
3. **Bulk deletion candidates** — every DEAD_WEIGHT module, grouped by reason (superseded, duplicate, prohibited, prototype), with the deletion test result for each.
4. **Duplicate map** — every DUPLICATE pair/group, identifying the canonical version and the migration path.
5. **Low-risk fossils** — listed but not prioritized.
6. **Connected-alive findings** — concerns observed during the scan that belong to other skills (security gaps, missing tests, architectural friction). Noted as findings, not acted on.

### Searchable, filterable format

For assessments of 50+ modules, produce an HTML report with filtering by classification. A flat markdown list of 112 files is not navigable. The report should allow the user to see "show me only FOSSIL_HIGH_RISK" or "show me everything older than 90 days."

---

## Part 4 — Acting on the Assessment

### Prioritization order

1. **FOSSIL_HIGH_RISK with known defects** — these are the most dangerous: code designed to influence decisions, not wired in, with bugs. If someone wires them in without noticing the bugs, the defect goes live silently. Act first.
2. **DEAD_WEIGHT bulk deletion** — the fastest win. Reduces cognitive load, shrinks the repo, and makes the next assessment easier. Group into one commit per logical cluster.
3. **DUPLICATES** — migrate callers, delete non-canonical versions.
4. **FOSSIL_HIGH_RISK without known defects** — document or wire in, depending on priority.
5. **FOSSIL_LOW_RISK** — last, if ever.

### Verification after each action

After every deletion or modification:
- Run the full test suite. A failure means the classification was wrong — reclassify and investigate before proceeding.
- Commit with a clear message that references the assessment finding (e.g., "B-121: delete 15 confirmed dead-weight files, deletion test passed for all").
- Push before starting the next cluster — do not accumulate multiple bulk deletions without pushing. The risk of losing work compounds with uncommitted changes.

### Documentation as the deliverable

The assessment report, the commit messages, and the bug tracker entries ARE the deliverable — not just the code changes. A bulk deletion without documentation is a knowledge loss. Six months from now, someone will ask "why was X deleted?" and the answer should be traceable from the commit message to the assessment report to the classification evidence.

---

## Part 5 — Recurring Assessment

A health assessment is not a one-time event. Schedule it:

- **After every major feature** — new features add modules; assess whether they also orphaned old ones.
- **After every hackathon or prototype sprint** — prototypes that do not graduate to production are the primary source of DEAD_WEIGHT.
- **Quarterly for mature projects** — even without major changes, dependency drift and team turnover create fossils.

Each assessment should compare against the previous one: how many modules were added, how many were retired, and whether the fossil ratio is improving or degrading.

---

## Anti-Patterns to Name and Correct

- **Grep-of-one-directory** — searching for callers only in the obvious places. Config files, CLI entry points, test fixtures, other repos, serialization, and reflection all call code invisibly. Search the entire repo, including non-code files.
- **Deletion by age alone** — "it's 90 days old, delete it." Age is a signal, not a verdict. A rarely-changed utility module that everything depends on is old AND alive.
- **The "clean repo" aesthetic** — deleting code to make the repo look tidy, without the classification step. This is fence removal by aesthetics (see `/software-archaeology`).
- **Preserving everything "just in case"** — the opposite failure. Dead code has a real cost: it misleads, it creates import collisions, it shows up in grep results, and it makes every future assessment harder. Documented deletion is safer than silent preservation.
- **Flat lists instead of structured reports** — an unstructured list of "these files might be dead" is not actionable for more than ~10 files. Structure and filterability are not optional for large assessments.

---

## How to respond when this skill is active

- Start by counting modules and establishing the temporal index. Unshallow the git history if needed.
- Classify every module in scope into exactly one category before proposing any action.
- Apply the deletion test to every DEAD_WEIGHT candidate: would deleting it concentrate complexity, or just remove unreachable code?
- Produce a structured, filterable report for assessments of 50+ modules.
- Act in priority order: high-risk fossils with defects first, bulk dead-weight second, duplicates third.
- Run the full test suite after every deletion. Push before starting the next cluster.
- Document every action with traceable references from commit message to assessment finding.
- When a deletion causes a test failure, treat it as a reclassification finding (the module was not dead), not as a reason to skip the rest of the assessment.
