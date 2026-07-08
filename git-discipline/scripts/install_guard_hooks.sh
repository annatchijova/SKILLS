#!/usr/bin/env bash
# install_guard_hooks.sh — Install a pre-push hook that blocks force pushes.
#
# The prompt-level prohibition on force-push relies on the agent obeying it.
# This enforces it mechanically: a pre-push hook that aborts when the push
# rewrites the remote branch (a non-fast-forward / forced update).
#
# Usage: run from inside the repo:  ./install_guard_hooks.sh
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: not inside a git work tree." >&2
    exit 1
fi

hook_dir="$(git rev-parse --git-path hooks)"
mkdir -p "$hook_dir"
hook="$hook_dir/pre-push"

cat > "$hook" <<'HOOK'
#!/usr/bin/env bash
# pre-push: refuse non-fast-forward (forced) updates to a remote branch.
# git feeds "<local_ref> <local_sha> <remote_ref> <remote_sha>" lines on stdin.
set -euo pipefail
ZERO="0000000000000000000000000000000000000000"
status=0
while read -r local_ref local_sha remote_ref remote_sha; do
    # New branch (remote_sha all zeros) or deletion (local_sha all zeros): allow.
    [ "$remote_sha" = "$ZERO" ] && continue
    [ "$local_sha"  = "$ZERO" ] && continue
    # If remote_sha is NOT an ancestor of local_sha, this push rewrites history.
    if ! git merge-base --is-ancestor "$remote_sha" "$local_sha"; then
        echo "BLOCKED: non-fast-forward push to $remote_ref would rewrite remote history." >&2
        echo "         Forced/rewriting pushes are prohibited in this repo." >&2
        echo "         If this is truly intended, a human should do it deliberately:" >&2
        echo "           git push --no-verify ...   (bypasses this hook on purpose)" >&2
        status=1
    fi
done
exit $status
HOOK

chmod +x "$hook"
echo "Installed pre-push guard hook at: $hook"
echo "It blocks forced/rewriting pushes. A human can bypass deliberately with --no-verify."
