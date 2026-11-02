---
name: rt-toctou
description: "Red-team / research assessment of time-of-check-to-time-of-use boundaries: filesystem races (symlink/hardlink swaps between access() and open()), kernel double-fetch of user pointers, temp-file predictability, and check-then-act windows in privileged programs. Re-expressed as scoped experiments on an owned SUID/privileged binary that prove the window with a planted swap and a widened-window control instead of live privilege theft."
---

# TOCTOU Race Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's TOCTOU craft as scoped experiments: it names the filesystem and kernel race classes, proving the window on an owned privileged binary with a planted target rather than stealing real privilege. Compose with `invariant-hunting` (check-at-T0, use-at-Tn) and `concurrency-reasoning`.

## Scope and prerequisites

TOCTOU exploits the gap between a check (access/stat/validation) and the use (open/exec/write) of the same resource. Work on an owned SUID/privileged binary or kernel module in a lab; prove the race against a planted file/target you own. Do not race a production privileged program.

Declare the target, the check/use pair, attempt budget, stop condition. Source-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Filesystem races** — swap a path between `access()`/`stat()` and `open()`/`exec()` via symlink/hardlink/rename; the check sees a benign file, the use acts on a sensitive one.
- **Kernel double-fetch** — a syscall reads a user pointer twice (check then use); a concurrent thread changes it between fetches.
- **Temp-file predictability** — predictable names in a shared dir let an attacker pre-create/symlink.
- **Check-then-act** — any privileged validate-then-operate without holding a lock/handle.

## Mechanism and observation

Trace the resource from the check to the use and whether the identity is re-validated at use.

**Firstness:** Record that the use acted on the swapped (planted) target rather than the checked one. **Secondness:** State the invariant (the thing used is the thing checked) and the deviation. **Thirdness:** Infer the TOCTOU class only after a controlled swap makes check and use diverge.

## Abduction and refutation

**Mechanism hypothesis:** The program re-resolves the resource by name at use, so a concurrent swap makes it use a different object than it checked.

**Competing benign explanation:** The program opens once and operates on that file descriptor (handle), so a later name swap is inert; it safely constrains path resolution and verifies the opened object; the directory is not attacker-writable; the double-fetch copies once; or the window is too small to win without widening and never wins. `openat` alone does not prevent symlink traversal; `O_NOFOLLOW` ordinarily applies to the final path component, so assess intermediate components and directory trust too.

## Deduction and controls

Normal operation acts on the checked resource (positive control). A confirmed TOCTOU has the use act on the planted swapped target where a safely resolved, handle-based implementation would not. Predeclare the swapped-target effect. Verify fd-based operation, full path-resolution constraints, single-fetch and directory permissions as separate controls; `openat` alone or final-component `O_NOFOLLOW` is not a general path-traversal guarantee.

## Induction: bounded laboratory procedure

Owned privileged binary; planted target; lab dir.

1. **Baseline.** Run normally; confirm it acts on the checked resource and identify the check/use pair.
2. **Window widening.** To make the race observable, widen the window (filesystem pressure, large file, scheduler hints, `inotify`-timed swap) — this is a lab aid, not a requirement of the bug.
3. **Swap.** Between check and use, swap the path to a planted sensitive target (symlink) you own; loop until the use acts on it.
4. **Confirm.** Show the privileged use operated on the planted target (e.g. wrote to / read the planted file) — proof of the window; stop before escalating to real privilege.
5. **Kernel double-fetch.** If applicable, flip the user pointer's contents between fetches from a second thread and observe the divergence.
6. **Control.** Re-run against an fd-based / `O_NOFOLLOW` build and confirm the swap is inert.

Record results including refutations. Keep finding and control status separate. A race won even once (with the window widened) demonstrates the flaw, but note the natural-window reliability honestly.

## Craft notes (leads)

The canonical bug is `access()` then `open()` on a path in an attacker-writable dir. Constrain path resolution when opening, then operate on the opened fd and validate the selected object with `fstat`. `openat` is directory-relative, not by itself a symlink-traversal defense; `O_NOFOLLOW` protects the final component. Where available, stronger resolution constraints (such as Linux `openat2` flags) can reject symlinks or escapes in every component. Double-fetch is the kernel analogue: copy-from-user twice. Predictable temp names (`/tmp/foo.PID`) enable pre-creation. Widening the window makes an otherwise-tight race reproducible in the lab.

## Domain-specific failure modes

Operations on a previously opened fd make subsequent renaming of that pathname inert for that already-open object, but only if the open itself selected the intended object under safe resolution rules. A safe open-once pattern is the primary refutation. A non-attacker-writable directory removes the swap primitive. A tight window that never wins even widened is CANDIDATE, not CONFIRMED. Winning once in the lab proves the flaw but may be low-reliability in the wild — state it.

## Evidence and deliverable

Provide the check/use pair, the swap mechanism, the planted-target effect at use, whether the window was widened, and the fd-based control result. Keep to owned targets. Attach minimal replay, expected/observed, rival explanation (fd-based), falsifier, untested paths.

## Versions and tool limitations

Pin the OS/kernel and the program version — syscall sequences and fixes are version-specific. No program behavior was verified by this content; confirm on the owned binary first.

## Remediation and detection

Open once and operate on the file descriptor (`openat`, `O_NOFOLLOW`, `fstat` on the fd), avoid path re-resolution, use `mkstemp`/unpredictable temp names in non-shared dirs, copy user data once in kernel code, and hold locks across check-and-act. Add a regression swapping the path and asserting the use is inert. Detect symlink swaps on sensitive paths.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A privileged use acts on the planted swapped target (window widened as needed) where an fd-based build is inert: CONFIRMED; FAIL (note reliability). |
| Benign refutation | fd-based operation / `O_NOFOLLOW` / non-writable dir makes the swap inert: REFUTED; PASS for the control. |
| Insufficient evidence | A plausible window that never wins even widened: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/exploit-dev/offensive-toctou/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's filesystem-race, double-fetch and temp-file craft, re-expressed as owned-binary experiments with a planted swap, window-widening and fd-based controls, replacing live privilege theft with bounded window proof. Composes with `invariant-hunting`, `concurrency-reasoning`, `rt-linux-privesc`.
