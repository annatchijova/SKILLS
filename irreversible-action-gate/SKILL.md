---
name: irreversible-action-gate
description: Classify an action by reversibility and blast radius before executing it, then require a gate proportional to what cannot be undone — preview the exact targets, assert the expected count, take a restore point, and write the undo plan before the action, not after. Use before any destructive, bulk, or outward-facing operation: rm/DROP/TRUNCATE/DELETE without a tested WHERE, mass find-and-replace, force-push or history rewrite, migrations, `terraform apply`, prod deploys, package publishes, sending email or messages, posting to an external service, revoking credentials, or deleting anything whose purpose is unclear. Trigger on "delete all", "clean up", "bulk update", "wipe", "reset", "migrate", "publish", "send it", "just remove", or a script whose blast radius is a wildcard. Also trigger when an autonomous agent is about to take an action with side effects. Pairs with git-discipline (restore points for repos) and software-archaeology (never delete what you cannot explain).
---

# Irreversible Action Gate

Most catastrophic operations were correct in intent and wrong in scope. The
command matched more than it was supposed to, ran against the wrong environment,
or was undoable in principle and undone by nobody in practice. The gap is almost
never knowledge — it is that **nothing stood between deciding and doing**.

This skill installs that something. It is deliberately proportional: trivially
reversible actions get no ceremony, because a process that treats every action as
dangerous trains people to skip the check exactly when it matters.

Two premises:

- **Reversible-in-theory is not reversible.** A restore that has never been
  tested, a backup nobody can locate, an undo that requires a vendor ticket — for
  the next fifteen minutes, these are all "irreversible".
- **Publishing is irreversible even when deletable.** Once content reaches an
  external service it may be cached, mirrored, indexed, forwarded, or read. The
  delete button removes the copy you control.

---

## Part 1 — Classify: reversibility × blast radius

**Reversibility class:**

| Class | Meaning | Examples |
|---|---|---|
| **R0** | Undone locally in seconds, no coordination | Local edit, uncommitted change, feature flag off |
| **R1** | Reversible with effort, no data loss | Revert a commit, roll back a deploy, restore from a repo |
| **R2** | Reversible only from a backup or snapshot | Dropped table, deleted bucket, overwritten file with no VCS |
| **R3** | Not reversible | Sent email, published package version, leaked secret, deleted the only copy, destroyed infrastructure with state, revoked the credential you were using, notified a customer |

**Blast radius:** one entity → a set you can name → a whole environment/tenant →
everyone. Ask specifically: how many rows, which environment, whose data, who
sees it.

The gate is set by the **worse** of the two axes. A single R3 (one email to one
customer) still needs a gate; an R1 across production for everyone does too. R0 at
small radius needs none — just do it.

Two questions that reclassify an action upward more often than any others:

- **Is this production?** Verify from the environment itself — the connection
  string, the account ID, the cluster context, the hostname in the prompt — not
  from which terminal tab you believe you are in.
- **Do I know what this thing is for?** If you cannot explain why it exists,
  deleting it is at least R2 regardless of how dead it looks
  (`software-archaeology`, `codebase-health-assessment`). Unexplained is not
  unused.

---

## Part 2 — The gate

For anything above R0-small, in this order:

**1. Preview the exact targets.** Convert the destructive form into a read: the
`SELECT` before the `DELETE`, `--dry-run`, `git diff`/`--stat`, `terraform plan`,
`find` before `find -delete`, the list of recipients before the send. Look at the
list — not the count alone, the actual items, or at least a sample plus the
extremes.

**2. Assert the expected count before you look at the real one.** Say the number
out loud first: *"this should match 3 rows."* Then compare. `expected 3, matched
1,204` is the single highest-yield safety check in this entire skill, and it only
works if you commit to the number before seeing the result. Any mismatch stops
everything until it is explained — a mismatch means your mental model and the
system's state disagree, and the destructive operation is the worst possible way
to resolve that disagreement.

**3. Take the restore point.** A tagged commit (`git-discipline`), a table copy, a
snapshot, an export — created *now*, for this operation, and **verified to exist
and be readable**. "There's a nightly backup" is not a restore point; it is a
hypothesis about a system you have not checked, with up to 24 hours of loss built
in.

**4. Write the undo plan before acting.** Concretely: the command or procedure
that reverses this, who can execute it, and how long it takes. If you cannot
write it, the action is R3 and needs the R3 gate below — *the inability to write
an undo plan is the definition, not an inconvenience*.

**5. Act on the previewed set, not on the predicate.** Time-of-check/time-of-use
matters: between your `SELECT` and your `DELETE`, the world changed. Where the
scale allows, capture the IDs from the preview and operate on that explicit list.
Where it does not, run inside a transaction and check the affected count before
committing (`atomic-state-mutation`), or bound the operation with a `LIMIT` and
iterate.

**6. Verify after.** Confirm the intended change happened *and* that nothing else
did — the neighboring rows, the other environment, the unrelated files. "The
command exited 0" reports the command's opinion of itself.

**For R3 specifically**, add: an explicit confirmation from the person who owns
the consequence (not the person who wants the action), stated in terms of the
consequence — *"this sends 12,000 emails and cannot be recalled"*, not *"proceed?
y/n"* — and, where the action is scheduled or automated, a delay window in which
it can still be cancelled.

---

## Part 3 — Patterns that turn a normal action into a dangerous one

- **The unbounded predicate.** `DELETE FROM t` where the `WHERE` was lost in
  editing; `rm -rf $DIR/` where `$DIR` is empty; `s/foo/bar/g` across a repo where
  `foo` also appears in a vendored dependency. Prefer forms that fail closed:
  require a `WHERE`, quote and check variables, scope the path explicitly.
- **The wildcard that widened.** A glob written when the directory had 3 files,
  run when it has 3,000. Preview every time, not once when the script was written.
- **The loop that partially completed.** Half the operations succeeded, then a
  failure — now the system is in a state neither the before nor the after plan
  describes. Make it atomic, or make it idempotent and resumable, and record
  progress as you go.
- **The environment mix-up.** Identical commands, different context. Make prod
  visually distinct, require an explicit env argument with no default, and read
  the environment back from the connection before acting.
- **The cascade you did not know about.** Foreign keys, triggers, webhooks,
  replication, search indexes, downstream consumers, and CI that reacts to the
  push. Ask what *else* observes this state before changing it.
- **The credential you are standing on.** Rotating, revoking, or restricting the
  access you are currently using — verify you have a second path in before you
  close the first.
- **The automation that will not stop.** A scheduled job or agent loop that
  repeats the destructive action; disable the schedule before repairing state, or
  you are racing it.

---

## Part 4 — For agents and scripts acting autonomously

An autonomous agent has no hesitation, so the gate must be structural
(`agent-trust-boundaries`, `llm-out-of-the-loop`):

- Destructive capability is granted by policy, per run, scoped to a path,
  namespace, or row set — not by the agent's judgment about its own request.
- Count assertions and dry-runs are enforced in the tool, not requested in the
  prompt. A tool that refuses to delete more than N without an explicit override
  is worth more than any instruction.
- Every R2+ action lands in an append-only record with its preview, count, and
  restore point (`tamper-evident-audit-chain`).
- Confirmation is reserved for the genuinely irreversible. An agent that asks
  about everything gets approved reflexively, which is worse than not asking.

---

## Deliverable checklist

```markdown
## Irreversibility gate

Action: <what>
Environment: <verified how — connection string / account id / context>
Class: R0 | R1 | R2 | R3    Blast radius: <n entities / env / tenant / everyone>
Preview: <command run, sample of the actual targets>
Expected count: <n, stated before>   Actual: <n>   → match / STOP
Restore point: <what, where, verified readable at HH:MM>
Undo plan: <exact procedure, owner, time to execute>
Cascades checked: <FKs, triggers, webhooks, replicas, indexes, CI, downstream consumers>
Automation paused: <yes/n-a>
Confirmation (R3): <who owns the consequence, what they were told>
Post-verification: <intended change confirmed + nothing else changed>
```

---

## How to respond when this skill is active

- State the reversibility class and blast radius before proposing the command; keep it to one line for R0/R1 so the ceremony stays proportional.
- Always show the preview form first, and commit to an expected count before running it.
- Stop on any count mismatch and explain the discrepancy before proceeding — never adjust the expectation to match the result.
- Create and verify a restore point for R2+, and refuse to rely on "there's a backup somewhere".
- Write the undo plan before the action. If it cannot be written, treat the action as R3.
- Ask what else observes this state — cascades and downstream automation are the usual source of surprise.
- For R3, put the consequence in the confirmation question, in units the owner cares about.
- After acting, verify both that the intended thing happened and that nothing adjacent did.
