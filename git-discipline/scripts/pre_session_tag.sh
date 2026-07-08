#!/usr/bin/env bash
# pre_session_tag.sh — Create an annotated restore point before an AI session.
#
# A tag is a permanent, named anchor at the current HEAD. After the session,
# `git reset --hard <printed-tag>` returns to exactly this state. Costs nothing.
#
# Usage:
#   ./pre_session_tag.sh                 # auto-named pre-session-<timestamp>
#   ./pre_session_tag.sh my-label        # custom label
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: not inside a git work tree." >&2
    exit 1
fi

label="${1:-pre-session-$(date +%Y%m%d-%H%M%S)}"
head_short="$(git rev-parse --short HEAD)"

git tag -a "$label" -m "restore point before AI session (HEAD was $head_short)"

echo "Restore point created:"
echo "  tag : $label"
echo "  head: $head_short"
echo
echo "To undo the entire session later:"
echo "  git reset --hard $label"
