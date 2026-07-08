---
name: surgical-patcher
description: Apply changes to existing source files by anchored, verified, reversible patches instead of rewriting whole files. Use this whenever you are about to edit, refactor, or modify an existing file programmatically; when applying a patch, diff, or change set proposed by an auditor or another model; when doing find-and-replace across a repo; or any time you would otherwise overwrite a file from memory or from a snapshot. This is especially important in AI-assisted coding, where the single largest source of silent regressions is a model rewriting more than it intended. Push to use this even when the user just says "edit this file", "apply this fix", "refactor X", or "the audit found a problem in Y".
---

# Surgical Patcher

Editing an existing file by regenerating it from memory is the most common way to introduce a silent regression: the model reproduces 95% of the file correctly and quietly drops a function, flips a default, or reformats a block that other code depended on. The defense is to never rewrite a file you can patch, and to make every patch anchored, verified, and reversible.

The discipline is small and non-negotiable.

## The five invariants

1. **Anchor on an exact, unique string.** A patch targets a verbatim substring of the current file (the anchor) and replaces it. Before applying, count the occurrences of the anchor in the live file. The count must be exactly `1`. If it is `0`, the anchor is stale (the file changed, or you imagined it) — abort. If it is `>1`, the anchor is ambiguous and you will patch the wrong site — abort and lengthen the anchor until it is unique. Never "apply to the first match" as a default; ambiguity is a bug, not a tie to break.

2. **Dry-run first, always.** The patcher must default to *not* writing. You opt into mutation explicitly (`--apply`). A dry run prints exactly what would change so a human (or you) can read the diff before anything touches disk.

3. **Back up before you write.** Before overwriting the target, copy it to `<file>.bak` (or a timestamped suffix). A patch you cannot undo in one command is a patch you should not apply.

4. **Verify after you write.** A patch that produces a syntactically broken file is worse than no patch. After writing, run a verifier appropriate to the file type — for Python, parse it with `ast`; for JSON, load it; for others, at minimum confirm the file is non-empty and the anchor is gone. If verification fails, restore from the backup and report.

5. **Read the file immediately before patching.** Anchors go stale the moment anything else edits the file. If you patched it once, re-read before the next patch — earlier views are no longer authoritative.

## Why anchored over whole-file rewrites

A whole-file rewrite asks the model to reproduce everything it is *not* changing, perfectly, from memory. An anchored patch asks it to reproduce only the small region it *is* changing. The blast radius of a mistake shrinks from "the entire file" to "one anchor". You also get a reviewable diff for free, which you do not get from a rewrite.

This is why you also never overwrite a repo file from a project-knowledge snapshot or a cached copy: the snapshot is almost always behind the live file, and the overwrite silently reverts whatever changed in between. Patch the live file; do not replace it.

## Workflow

For a one-off change, write a thin task script that declares the patches and calls the shared engine. The pattern, mirroring a real production patcher:

```python
from surgical_patch import apply_surgical_patches

PATCHES = [
    # (anchor — must appear exactly once, replacement)
    (
        "ollama_model: Optional[str] = None,",
        "ollama_model: Optional[str] = None,\n    llm_backend: Optional[str] = None,",
    ),
]

apply_surgical_patches("pipeline.py", PATCHES, dry_run=True)   # inspect
apply_surgical_patches("pipeline.py", PATCHES, dry_run=False)  # commit
```

Or drive it from the CLI with a JSON patch set (see `scripts/surgical_patch.py --help`):

```bash
python scripts/surgical_patch.py target.py patches.json            # dry run
python scripts/surgical_patch.py target.py patches.json --apply     # write + verify
```

`scripts/surgical_patch.py` is the shared engine. It enforces all five invariants: exact-count anchoring (abort on `!= 1`), dry-run by default, `.bak` backup, and a post-write verifier (`ast.parse` for `.py`, `json.loads` for `.json`, anchor-gone check otherwise) with automatic restore on failure. Copy it next to your task scripts or import it.

## Anchoring well

A good anchor is the smallest verbatim slice of the file that is unique and stable. Include enough surrounding context to be unique, but avoid pinning to lines that churn (comments, version strings) when a structural anchor (a function signature, a unique call) is available. If you cannot find a unique anchor for the region you mean, that is information: the file may already contain the change, or your mental model of it is wrong. Re-read before forcing it.

## When NOT to use this

Creating a brand-new file is not a patch — write it directly. A wholesale rewrite the user explicitly asked for (e.g. "throw this away and start over") is not a patch either. Surgical patching is specifically for *modifying existing content you want to preserve around the edit*.
