---
name: writing-agents-md
description: Write an AGENTS.md (or CLAUDE.md) that actually changes agent behavior — falsifiable, enforced invariants grounded in this repo's real incidents, not a generic checklist any repo could have. Use whenever creating or reviewing a repo's agent-facing contract file, whenever an agent keeps making the same mistake a doc was supposed to prevent, or whenever a repo has none and one is being requested. Trigger on "write an AGENTS.md", "add agent instructions", "this repo needs a CLAUDE.md", "the agent keeps doing X, document it", or a PR that adds/edits AGENTS.md/CLAUDE.md with no invariant, no mechanism, and no reason attached. Not a style guide for prose — it governs what the file's content actually has to be to survive contact with an agent that hasn't read it in six weeks.
---

# Writing AGENTS.md

Most AGENTS.md files are lists of things any repo could say: "write tests,"
"don't commit secrets," "use meaningful commit messages." An agent reads
that once and it changes nothing, because it names no specific failure this
repo actually had and no mechanism that would catch a violation. This skill
is built from five AGENTS.md files that do change behavior — `velo`,
`zaynor`, `locoporcolt`, `annaconda`, `nexo` — read side by side to extract
what they have in common structurally, despite covering unrelated domains
(a ZK engine, a DFIR postmortem tool, a firearms marketplace, a live
forensic backend, a Rust decision-graph system).

Composes with the library:

- **decision-record-discipline** — an AGENTS.md invariant is a standing
  decision record; it needs the same Forces/Assumption/Revisit-trigger
  thinking, just written as a rule instead of a narrative
- **claim-provenance-discipline** — a rule with no traceable origin decays
  into doctrine the same way a finding does; ground every invariant in
  something checkable (a file, a test, an incident), not assertion
- **git-discipline** — the git-hygiene rules that appear in most of the
  five examples (forward-only history, restore-point tags, verify before
  claiming) are that skill's content; cite it instead of restating it
- **irreversible-action-gate** — a `git commit`/`git push` authorization is
  per-action, not per-session, the same way that skill treats any other
  hard-to-reverse action; see §11 below

---

## What AGENTS.md is, and what it is not

**MUST** state, at the top of the file if a generic discipline guide
(`CLAUDE.md`) also exists in the repo, which file wins when they conflict,
and what each one is actually for. `zaynor`'s framing: `CLAUDE.md` is the
portable development-discipline guide (git hygiene, editing discipline, the
reasoning loop) — generic, could apply to any repo. `AGENTS.md` is *this
product's* operating manual: its architecture, its authority boundaries, its
own invariants. `nexo` goes further and makes `AGENTS.md` itself explicitly
subordinate to `docs/`: "If anything below conflicts with those files, the
files in `docs/` win — this file is a summary and a checklist, not a new
source of truth." Either hierarchy is fine; **an unstated one is not** — an
agent facing a conflict between two files needs a decision procedure, not
two equally authoritative documents.

**MUST NOT** duplicate what a human-facing `README.md` or `CONTRIBUTING.md`
already says in full — `velo`'s AGENTS.md opens by naming
`CONTRIBUTING.md` as "the human-readable source of truth for the same
conventions" and positions itself as the agent-specific complement, not a
second copy.

## The anatomy: what makes an invariant actually load-bearing

A line that says "verify ownership before returning an object" is an
opinion. The same line becomes an invariant an agent will actually respect
when it carries these attributes — drawn directly from the strongest
examples in the five files:

### 1. A named enforcement mechanism, not just an instruction

**SHOULD** name, for each invariant that can be, the mechanism that would
catch a violation: a Semgrep rule (`locoporcolt`: "Enforced by a Semgrep
rule (`contact-disclosure-missing-clu-gate`)"), a database CHECK constraint
(`locoporcolt`: "the CHECK `clu_verif_photo_erased_on_resolve` makes a
resolved row that still holds it a state Postgres rejects"), a test that
must stay green (`annaconda`: "`tests/test_determinism.py` guards this; it
must stay green"), or a CI gate (`zaynor`'s `docs_check.py` / `DOCS_MAP`
mechanism that blocks a PR whose code diff has no matching doc update). An
invariant with no named mechanism is a request for the agent's good
behavior; an invariant with one is a fact about what will happen if the
agent ignores it. State honestly which kind each one is — don't imply
mechanical enforcement that doesn't exist.

### 2. The "why," specific enough to be falsifiable

**MUST** give a reason concrete enough that a reader could check whether it
still holds — not "for security" or "for maintainability." `locoporcolt`'s
Mercado Pago webhook invariant is the sharpest example: it doesn't just say
"verify the signature," it explains why the *obvious* pattern (verify over
the raw body, the Stripe convention) is actively wrong for this specific
provider, quotes the exact signed manifest format, and names the SDK
version it was checked against. A reason that specific can be re-verified
later; "for security" cannot.

### 3. Grounded in an actual incident, not a hypothetical

**SHOULD** cite the real event that taught the lesson, when one exists.
`velo`: "it is why PR #6 had to be closed rather than merged, and it nearly
happened again to PR #9 on a base that was three commits behind." A rule
grounded this way survives the question "is this really necessary?" — the
answer is "it already went wrong once, here's the PR." A rule presented as
pure hypothetical caution invites exactly that skepticism, and loses it.

### 4. Asymmetric failure modes named explicitly

**SHOULD**, when a rule mediates between two failure directions, say which
one is worse and why the rule is biased toward it. `locoporcolt`'s
`requires_clu` inheritance rule: "the two failure modes are not symmetric —
over-gating is visible and gets reported, under-gating publishes firearms
with no CLU and is silent — so the flag is forced up, never rejected." This
tells an agent which way to err under genuine uncertainty, which a bare
"the flag propagates down" does not.

### 5. Numeric values flagged as decisions, not defaults

**MUST** mark any magic number an agent might be tempted to "clean up" as a
deliberate decision with its current value stated, per `locoporcolt`'s
"Numeric thresholds are decisions, not defaults to normalize" section — a
list of every rate limit, TTL, and threshold in the system with a one-line
reason where non-obvious. Without this, a well-intentioned agent doing an
unrelated refactor "normalizes" a rate limit that was actually sized against
a specific abuse pattern.

### 6. One dominant invariant is allowed when that's the truth

**MAY** structure the whole file around a single invariant if the
architecture genuinely has one center of gravity — `annaconda`'s "The one
invariant (do not break this)": the LLM never touches the verdict,
everything else in the file is either a consequence of that rule or
unrelated setup/ops content. Padding a file with invented secondary
invariants to look thorough is worse than naming the one real one clearly.

### 7. A repo map with one-line purpose per module

**SHOULD** include a directory tree annotated with what each part is *for*,
not just its name — `annaconda`'s repo map states, per directory, the
specific invariant that module carries (e.g. "stdlib-only, no floats" next
to `core/`). This orients a fresh agent in seconds instead of requiring it
to infer architecture from file contents.

### 8. Operational gotchas that already cost real time

**SHOULD** document the invisible failure a deploy/setup step produces, not
the obvious one — `annaconda`: "`GOOGLE_CLOUD_PROJECT` is not injected by
Cloud Run... without it the store degrades to memory and the fleet's
continuity claim stops being true," with the exact confirmation check
(`/health` says `"case_store":"firestore"`). A gotcha worth documenting is
one that fails silently and plausibly, not one that throws an obvious error.

### 9. Definition of Done as a checklist mirroring the invariants

**MUST** close with a checklist a reviewer (human or agent) can literally
tick against a diff, and **MUST** have every checklist item trace back to a
stated invariant or mechanism earlier in the file — a checklist item that
introduces a *new* rule nobody explained is a sign the file's body is
incomplete, not that the checklist is thorough.

### 10. Verified commands, not remembered ones

**MUST** give the actual, current command to build/test/lint — copy-pasted
from a real run, not recalled — and **SHOULD** state what a green result
actually proves ("the tool-layer allowlist tests pass," per `zaynor`) rather
than let a passing suite imply more than it checked.

### 11. Who may commit where, and the owner/agent asymmetry

**MUST** state explicitly, per repo, two separate things — collapsing them
into one vague "use branches" line is how an agent ends up guessing:

- **Where direct commits to the trunk are allowed at all**, and for whom.
  Some repos forbid it for everyone, owner included — `zaynor`: "Nobody
  pushes straight to `main` — not the owner, not the team, not an agent,"
  enforced mechanically by branch protection, because with several people
  (human or agent) committing in parallel, an unreviewed direct push is
  exactly what the others don't find out about until it costs the most.
  Other repos give the maintainer direct-to-main latitude that a
  collaborator or an agent does not have — that asymmetry is legitimate,
  but **MUST** be written down as a rule, not left to be inferred from
  who happens to have push access. A collaborator or an agent working
  here **MUST** branch: `git checkout -b <type>/<short-description>
  origin/main`, never commit to the trunk directly, regardless of what the
  maintainer's own workflow looks like.
- **Whether an agent's write access to files also means standing
  permission to `git commit`/`git push`.** It does not, by default, and
  the file should say so. `zaynor`'s exact framing is the one to reuse:
  "An agent may stage changes and propose a commit message, but `git
  commit` and `git push` only run after the maintainer explicitly
  authorizes that specific action in the session. A general instruction to
  work on the repo is not commit permission." **MUST** treat this as
  per-action, not per-session — an authorization to commit once is not a
  standing authorization for the rest of the session, the same way a user
  approving one destructive action elsewhere doesn't imply approval for
  the next one (`irreversible-action-gate`'s territory, applied to git
  specifically).

A repo that skips this either gets an agent that asks permission for
everything (friction on work that was already authorized) or one that
commits and pushes on its own judgment (the actual incident this section
exists to prevent) — an unstated policy defaults to the second, more
dangerous reading, because "I have write access" is the easier inference
for an agent to make from silence.

## Distinguish authored content from tool-generated boilerplate

Next.js's `next dev` (and similar tooling) writes its own agent-guidance
block directly into `AGENTS.md` (`<!-- BEGIN:nextjs-agent-rules -->` ...
`<!-- END:nextjs-agent-rules -->`), regenerated automatically and meant to
be committed. Two observed instances (`zaynor/frontend`, `locoporcolt`) show
the correct handling: commit the block when the tool writes it (removing it
from a diff only recreates the uncommitted change), but **do not** count it
toward "this repo already has agent documentation" — it teaches an agent
about the framework, not about this codebase's own invariants, and a
9-line tool-generated file with no project-specific content is not a
substitute for the rest of this skill. **MUST** keep tool-generated blocks
clearly delimited (as the auto-inserted markers already do) and never hand-edit
inside them — the tool will silently overwrite hand edits on its next run.

## The throwaway-instance rule

Anna's specific addition, stated because it's *not* the obvious "don't
commit secrets" advice: **MUST**, when an agent session creates any test
instance, fixture, or example data for local verification (a sample `.env`,
a seeded local DB dump, a scratch config with placeholder credentials, a
demo recording), add it to `.gitignore` **immediately**, in the same action
that creates it — not as a cleanup step remembered before commit. The
failure this prevents isn't "a secret got committed" (that's
`secret-lifecycle-discipline`'s territory and already obvious); it's
*example/synthetic* artifacts silently accumulating in git history because
nobody flagged them as throwaway at creation time, which is invisible right
up until someone greps the repo for why it's full of stale fixture files
from six months ago.

## Failure modes / anti-patterns

- **Generic-checklist AGENTS.md**: "write tests," "use meaningful commits,"
  "don't hardcode secrets" — true of every repo, changes nothing about this
  one, and trains agents to skim past the whole file because none of it is
  specific enough to act on.
- **README duplication**: restating the product pitch or setup instructions
  a human-facing doc already covers, instead of linking to it and adding
  only the agent-specific delta.
- **Invariant with no mechanism and no reason**: "always check ownership" —
  true, but doesn't say what breaks if skipped or what would catch it.
- **Unstated hierarchy**: an AGENTS.md and a CLAUDE.md (or a `docs/` set)
  that both claim authority with no stated tie-breaker, leaving an agent to
  guess which one to follow on the first conflict.
- **Silent magic numbers**: a rate limit or TTL that reads as an arbitrary
  default an agent "cleans up" during an unrelated change, because nothing
  flagged it as sized against a real constraint.
- **Confusing tool-generated boilerplate for project documentation**: citing
  a framework's auto-inserted block as evidence the repo already has agent
  guidance, when it says nothing about this codebase's actual invariants.
- **Checklist items with no upstream explanation**: a Definition of Done
  entry that introduces a brand-new rule the body of the file never stated
  or justified.
- **Copy-pasted template with no incident grounding**: an AGENTS.md that
  reads like it was cloned from another repo and never adapted — no
  reference to an actual PR, bug, near-miss, or specific numeric value this
  codebase depends on.
- **Unstated commit/push authorization**: "agents may work in this repo"
  with no explicit statement of whether that includes committing and
  pushing, and no statement of who (if anyone) may work directly on the
  trunk — an agent then defaults to inferring the broadest reading of its
  own access.

## Verifiable checks

- [ ] If both AGENTS.md and a generic discipline file exist, the file
      states explicitly which one wins on conflict.
- [ ] The file does not restate content a human-facing README/CONTRIBUTING
      already fully covers — it links instead.
- [ ] Every stated invariant has either a named enforcement mechanism, an
      explicit note that none exists yet, or is honestly framed as
      convention rather than a guarantee.
- [ ] Every stated invariant's "why" is specific enough that a reader could
      check whether it still holds (not "for security"/"for
      maintainability" alone).
- [ ] At least one invariant, where the repo's history supports it, cites
      the actual incident (PR, bug, near-miss) that motivated it.
- [ ] Any rule mediating between two failure directions states which
      direction is worse and why the rule favors it.
- [ ] Magic numbers (rate limits, TTLs, thresholds) are listed with their
      current value and flagged as deliberate, not left implicit.
- [ ] Build/test/lint commands are the actual current commands, and a
      "tests pass" claim states what the suite covers.
- [ ] Tool-generated blocks (framework auto-inserted content) are kept
      distinct from authored invariants and not counted as "documentation
      already exists."
- [ ] Any throwaway test instance, fixture, or example-data artifact
      created during a session is added to `.gitignore` at creation time,
      not as an afterthought before commit.
- [ ] The Definition of Done checklist has no item that isn't traceable to
      an invariant stated earlier in the file.
- [ ] The file states who (if anyone) may commit directly to the trunk, and
      that a collaborator or an agent branches instead — not left to be
      inferred from access.
- [ ] The file states explicitly whether an agent's write access includes
      standing permission to `git commit`/`git push`, or whether each such
      action needs explicit per-action authorization.
