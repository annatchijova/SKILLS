#!/usr/bin/env python3
"""
surgical_patch.py — Anchored, verified, reversible patching of existing files.

Enforces the five surgical-patcher invariants:
  1. Exact-count anchoring  — each anchor must appear exactly once, else abort.
  2. Dry-run by default      — writing requires explicit opt-in.
  3. Backup before write     — target copied to <file>.bak (or custom suffix).
  4. Verify after write      — syntax/structure check; restore on failure.
  5. (caller's job) re-read   — view the live file before building anchors.

Library use:
    from surgical_patch import apply_surgical_patches
    apply_surgical_patches("pipeline.py", PATCHES, dry_run=True)   # inspect
    apply_surgical_patches("pipeline.py", PATCHES, dry_run=False)  # commit

CLI use:
    python surgical_patch.py target.py patches.json           # dry run
    python surgical_patch.py target.py patches.json --apply    # write + verify

patches.json format:
    [
      {"anchor": "<verbatim substring>", "replacement": "<new text>"},
      ...
    ]
"""
from __future__ import annotations

import ast
import json
import shutil
import sys
from pathlib import Path
from typing import Callable, Iterable, Optional, Tuple

Patch = Tuple[str, str]  # (anchor, replacement)


class PatchError(RuntimeError):
    """Raised when a patch cannot be applied safely. Never swallowed silently."""


def _default_verifier(path: Path, applied_anchors: Iterable[str]) -> None:
    """Type-appropriate post-write verification. Raises PatchError on failure."""
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise PatchError(f"Post-patch file is empty: {path}")

    suffix = path.suffix.lower()
    if suffix == ".py":
        try:
            ast.parse(text)
        except SyntaxError as exc:
            raise PatchError(f"Post-patch Python syntax error in {path}: {exc}") from exc
    elif suffix == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            raise PatchError(f"Post-patch JSON is invalid in {path}: {exc}") from exc
    else:
        # Generic check: every anchor we replaced should no longer be present.
        for anchor in applied_anchors:
            if anchor in text:
                raise PatchError(
                    f"Anchor still present after replacement in {path}: {anchor[:80]!r}"
                )


def apply_surgical_patches(
    target: str | Path,
    patches: Iterable[Patch],
    *,
    dry_run: bool = True,
    backup_suffix: str = ".bak",
    verify: Optional[Callable[[Path, Iterable[str]], None]] = _default_verifier,
) -> str:
    """
    Apply (anchor, replacement) patches to `target`.

    Each anchor must appear exactly once in the live file. Aborts (PatchError)
    on a missing or ambiguous anchor before writing anything. With dry_run=True
    (the default) nothing is written; the would-be result is returned. With
    dry_run=False the file is backed up, written, and verified — and restored
    from backup if verification fails.

    Returns the patched text (whether or not it was written).
    """
    path = Path(target)
    if not path.exists():
        raise PatchError(f"Target does not exist: {path}")

    original = path.read_text(encoding="utf-8")
    src = original
    applied: list[str] = []

    for i, (anchor, replacement) in enumerate(patches, 1):
        count = src.count(anchor)
        if count == 0:
            raise PatchError(
                f"[patch {i}] anchor not found (stale or imagined) — aborting.\n"
                f"  anchor: {anchor[:120]!r}"
            )
        if count > 1:
            raise PatchError(
                f"[patch {i}] anchor is ambiguous: appears {count} times — "
                f"lengthen it until unique. Aborting.\n  anchor: {anchor[:120]!r}"
            )
        src = src.replace(anchor, replacement, 1)
        applied.append(anchor)
        print(f"[patch {i}] anchor matched exactly once — OK")

    if src == original:
        print("No effective change — patches already applied. Nothing to write.")
        return src

    if dry_run:
        print(f"\n[dry-run] {len(applied)} patch(es) would apply to {path}. "
              f"Re-run with apply enabled to write.")
        return src

    backup = path.with_name(path.name + backup_suffix)
    shutil.copy2(path, backup)
    print(f"[backup] {backup}")

    path.write_text(src, encoding="utf-8")
    print(f"[write]  {path}")

    if verify is not None:
        try:
            verify(path, applied)
        except PatchError:
            shutil.copy2(backup, path)
            print(f"[restore] verification failed — restored from {backup}")
            raise
        print("[verify] OK")

    return src


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    target = argv[0]
    patches_path = Path(argv[1])
    apply = "--apply" in argv[2:]

    if not patches_path.exists():
        print(f"ERROR: patch spec not found: {patches_path}")
        return 1

    spec = json.loads(patches_path.read_text(encoding="utf-8"))
    patches: list[Patch] = [(p["anchor"], p["replacement"]) for p in spec]

    try:
        apply_surgical_patches(target, patches, dry_run=not apply)
    except PatchError as exc:
        print(f"ABORT: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
