---
name: git-discipline
description: Protect repository history during AI-assisted and agentic coding by tagging a restore point before each session, forbidding history-rewriting operations, and verifying actual repo state before claiming anything about it. Use this whenever an AI agent (Claude Code or similar) is about to make changes to a git repository, whenever you are about to run or recommend git operations that could lose work, and whenever you are about to document or report the state of a repo. Triggers — "start a coding session", "let the agent edit", "rebase", "squash", "force push", "clean up history", "what's the state of the repo", "commit these changes". Push to use this whenever an autonomous tool has write access to a repository, even for a small change.
---

# Git Discipline

An AI agent with write access to a repository is fast, occasionally wrong, and does not feel the loss when work disappears. The cost of a destroyed branch or a force-pushed history is paid by the human. The discipline here is the cheap insurance that makes agentic editing safe: a restore point before every session, a hard prohibition on operations that rewrite shared history, and a refusal to claim repo state without checking it.

## Tag a restore point before every session

Before an agent touches the repo, create an annotated tag at the current HEAD. A tag is a named, permanent anchor you can return to no matter what the session does to the working tree or branch. It costs nothing and it is the difference between "undo the session" and "reconstruct it from memory".

```bash
git tag -a "pre-session-$(date +%Y%m%d-%H%M%S)" -m "restore point before AI session"
```

Recovery is then trivial: `git reset --hard <tag>` returns to exactly the pre-session state. `scripts/pre_session_tag.sh` wraps this and prints the tag name.

## Forbid history rewriting in agent prompts

`git rebase`, `git squash` (interactive rebase), and `git push --force` rewrite history. In an autonomous session they are not productivity tools, they are loss generators: a rebase gone wrong scrambles the commit graph, a force-push overwrites the remote's record of what everyone else has. State explicitly in any agent prompt that these are prohibited. Forward-only operations — `commit`, `merge`, `revert` — change history by *adding* to it, which is always recoverable. If history genuinely needs cleaning, a human does it deliberately, outside the agent loop, never as a side effect of a coding task.

A `pre-push` hook can enforce the force-push prohibition mechanically rather than relying on the prompt; `scripts/install_guard_hooks.sh` installs one that blocks `--force` / `--force-with-lease` pushes.

## Verify state before you claim it

Never assert the state of a repo from assumption or from a stale snapshot. Before documenting what was done, before reporting "everything is committed", before assuming which branch you are on or which files changed — run the commands and read the output:

```bash
git status --short        # what is actually staged / modified / untracked
git log --oneline -n 10   # what the history actually shows
git branch --show-current # which branch you are actually on
```

The failure this prevents is a confident, wrong report — "the changes are committed and pushed" when they are staged but uncommitted, or "we're on the feature branch" when the session left you on main. Empirical state beats remembered state every time; a snapshot in your context is not the live repo.

## Commit messages: leave a legible trail

Commits made by or with an agent should be tagged consistently so the human can find them later — a fixed prefix (a ticket id, a `chore(agent):` scope, or a project-specific tag) makes the agent's contributions filterable in `git log`. The point is provenance: when something breaks, you can see at a glance which commits came from an automated session and review them as a group.

**Project-specific note:** the prefix `POST HACKATHON` applies **only to the `vigia-repo` repository** and must not be used in any other repo. When in doubt about the convention for a given repo, check its `CLAUDE.md` before committing.

## What this looks like in practice

1. `git tag` a restore point (or run `pre_session_tag.sh`).
2. Run the agent; let it `commit`/`merge`/`revert` freely — never `rebase`/`squash`/`force-push`.
3. Before reporting, `git status` / `git log` / `git branch --show-current` and report what they actually say.
4. If the session went wrong, `git reset --hard <tag>` and start over — no reconstruction needed.

Do not assume a repo's paths, branch, or cleanliness from earlier in a conversation; the working tree may have changed since. When in doubt, ask for the output of `git status` rather than guessing.
