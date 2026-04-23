#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

DRILL_ID="${1:-parallel-01}"
WORKTREE_ROOT="$ROOT_DIR/.worktrees"

remove_one() {
  local path="$1"
  if [[ -d "$path" ]]; then
    git worktree remove "$path"
    echo "Removed worktree: $path"
  else
    echo "Skip missing worktree: $path"
  fi
}

remove_one "$WORKTREE_ROOT/${DRILL_ID}-api-data"
remove_one "$WORKTREE_ROOT/${DRILL_ID}-web-read"
remove_one "$WORKTREE_ROOT/${DRILL_ID}-review"

git worktree prune

cat <<EOF

Parallel drill worktrees were cleaned up for: $DRILL_ID
Branches were kept on purpose.
Delete branches manually only after merge or explicit abandonment.
EOF
