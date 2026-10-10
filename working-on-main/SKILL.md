---
name: working-on-main
description: Default to working directly on main on the user's own solo repositories — including with multiple agents active on main at once, kitchen-line style, each owning its piece and none assuming another's work is correct — instead of a feature-branch-per-agent/per-change workflow that is actually harder to track with ADHD (forgotten branches, forgotten merges, multi-agent branch pileups). Reserve a branch only for work that already fully works and is being extended in a genuinely experimental direction. Before any significant change, cut a backup/tag pushed to the remote as a named freeze point the user can return to without hunting through history. Use whenever the repo is solo-owned, whenever multiple agents or subagents are about to work on the same repo concurrently, or whenever the user says "work on main", "no branch for this", "tag it first", or pushes back on a proposed branch/PR workflow for their own project. Does NOT apply to shared/team-owned/OSS repos the user doesn't solely control, nor whenever a repo-local CLAUDE.md/AGENTS.md/CONTRIBUTING file already names a branching requirement — that requirement wins. Composes with git-discipline (restore-point tagging, forbidden history rewrites) rather than restating it.
---

# Working on Main

## Purpose

This is a personal operating preference, not a methodology claim — see the
note in this skill set's README. It exists because the alternative (a branch
per change, or a branch per agent) is the thing that actually produces lost
work for this user: with ADHD, a branch is something to forget — forgotten to
merge, forgotten to delete, and multiplied across several agents it becomes
several diverging branches nobody reconciles. A tagged freeze point on `main`
is something that survives being forgotten about; a branch is not.

The model for how this works is a professional kitchen line, which is the
user's own background: many different tickets in flight at once, each
station owning its piece, nobody stops to watch the rice boil, and the whole
thing stays coordinated and safe by design — not by assuming every cook is
careful, but by building the station so the dangerous mistake is hard to make
in the first place. The same structure runs multiple agents toward one
result (one dish; one feature) on `main`, not one agent per isolated branch.

## Core rule: multiple agents, one main

On a confirmed solo repository, agents (including multiple agents or
subagents working concurrently toward the same result) work directly on
`main`. Do not create a branch per agent or per change by default, and do not
propose a branch/PR workflow unprompted.

Each agent:

1. Owns its piece of the task and commits its own work directly.
2. **Never assumes another agent's prior step was done correctly.** Verify
   the state you depend on (read the file, run the check) before building on
   it — the same discipline as not trusting a line cook blindly, not because
   anyone is expected to be careless, but because the station is designed so
   that an error there cannot propagate silently.
3. Coordinates with other agents the cheap way by default: surface what you
   changed and what you assumed in your own output, so it can be copy-pasted
   to another agent or read by the user. For coordination that needs to
   survive longer than one exchange — a plan spanning several turns or
   agents, a running list of who owns what — write it to a shared `.md` file
   in the repo rather than relying on anyone's memory of the conversation.

## Commit discipline on main

Forward-only, per `git-discipline`: `commit`, `merge`, `revert`. Never
`rebase`, squash, or `push --force` — unchanged by working on `main` directly.

## Backup-and-tag before a significant change

Before any change the user would call significant (not every commit — a
meaningful step: a working feature about to be extended, a refactor, anything
she might want back exactly as it stood), cut a named tag and push it to the
remote:

```
tag="freeze-<short-description>-$(date +%Y%m%d-%H%M%S)"
git tag -a "$tag" -m "<why this point matters>"
git push origin "$tag"
```

Compute the tag name once, into a variable — never re-evaluate `date` across
the two commands. If they run in different seconds, the push can reference a
tag that was never created under that exact name, which is precisely the
kind of implicit, unverifiable state this skill exists to eliminate.

This is distinct from the per-session restore-point tag in `git-discipline`:
that one guards the session; this one guards a specific point in the work the
user might want to return to without digging through commit history to find
it. Name the tag for what it is, not just when it was made, so it's findable
later by what it means rather than by date alone. Pushing it to the remote
means the freeze point survives even if the local clone is lost or redone.

## When a branch is actually warranted

Reach for a branch only when both are true:

- The current `main` state already fully works — nothing is mid-change or
  broken.
- What's about to happen is genuinely experimental: an approach that might
  not pan out, where the point is to try it without main ever being in a
  broken state if it doesn't.

Even then, merge or delete the branch as soon as the experiment resolves
either way — don't let it linger as a second parallel history. If it's not
both true, the default is still `main`.

## When this does not apply

Check before defaulting to this mode, not after:

- Any other person has write access, is expected to review, or could push to
  the same `main` concurrently — this whole model assumes one human
  orchestrating several agents, not several humans.
- The repository is a disqualifying context with its own frozen/branch-only
  rule (e.g. a hackathon repo under submission freeze) — that rule wins
  outright.
- A CLAUDE.md, AGENTS.md, or CONTRIBUTING file in that repository states a
  branch or PR requirement — repo-local instructions override this
  preference.
- The user is contributing to someone else's OSS project — that always goes
  through that project's own branch/PR/fork convention, never this one.

## What this replaces, and what it doesn't

This skips branch-naming, PR-opening, and per-agent-branch ceremony. It does
**not** skip:

- Verifying repo state before claiming it (`git status`, `git log`) —
  `git-discipline` still governs this in full.
- Verifying another agent's prior step before building on it, per the core
  rule above.
- Reviewing what's staged before committing, especially for anything that
  might carry a secret.
- Writing a real commit message describing why, not just what.
- Running tests before committing, where the repo has them.

## Verifiable checks

- [ ] Before defaulting to shared work on `main`, the repo was confirmed
      solo-owned, not assumed.
- [ ] No branch-per-agent or branch-per-change workflow was proposed
      unprompted on a confirmed solo repo.
- [ ] Before building on another agent's prior step, that step's actual
      output was checked, not assumed correct.
- [ ] Longer-lived coordination between agents went into a shared `.md` file
      in the repo, not only into a chat exchange that won't persist.
- [ ] A named, remote-pushed freeze tag exists before any change the user
      would call significant — distinct from the per-session restore tag.
- [ ] A branch was opened only when both the "main already works" and
      "genuinely experimental" conditions held, and was merged or deleted
      once the experiment resolved.
- [ ] Any repo-local branching/PR requirement (CLAUDE.md, AGENTS.md,
      CONTRIBUTING, hackathon freeze) was checked and takes precedence when
      present.
