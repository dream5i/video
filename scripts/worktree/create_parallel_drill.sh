#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

DRILL_ID="${1:-parallel-01}"
BASE_REF="${2:-HEAD}"
WORKTREE_ROOT="$ROOT_DIR/.worktrees"
BOOTSTRAP_SCRIPT="$ROOT_DIR/scripts/worktree/bootstrap_worktree.sh"
BOOTSTRAP_WORKTREES="${BOOTSTRAP_WORKTREES:-1}"
created_paths=()

if [[ -n "$(git status --porcelain)" ]]; then
  cat <<'EOF'
Current worktree is dirty.

For the first parallel drill, worktrees must be created from a clean checkpoint.
Why: git worktree branches from a commit, not from your uncommitted local edits.

Recommended next step:
1. Run `pnpm verify`
2. Create a checkpoint commit
3. Re-run `pnpm worktree:drill:create`
EOF
  exit 1
fi

if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  echo "Base ref not found: $BASE_REF" >&2
  exit 1
fi

mkdir -p "$WORKTREE_ROOT"

create_one() {
  local lane="$1"
  local branch="$2"
  local path="$3"

  if git show-ref --verify --quiet "refs/heads/$branch"; then
    echo "Branch already exists: $branch" >&2
    exit 1
  fi

  if [[ -e "$path" ]]; then
    echo "Worktree path already exists: $path" >&2
    exit 1
  fi

  git worktree add "$path" -b "$branch" "$BASE_REF"
  created_paths+=("$path")
  echo "Created $lane -> $branch -> $path"
}

create_one "api-data" "feat/${DRILL_ID}-api-data" "$WORKTREE_ROOT/${DRILL_ID}-api-data"
create_one "web-read" "feat/${DRILL_ID}-web-read" "$WORKTREE_ROOT/${DRILL_ID}-web-read"
create_one "review" "review/${DRILL_ID}-review" "$WORKTREE_ROOT/${DRILL_ID}-review"

if [[ "$BOOTSTRAP_WORKTREES" != "0" ]]; then
  echo
  echo "Bootstrapping worktree runtime dependencies..."
  bash "$BOOTSTRAP_SCRIPT" "${created_paths[@]}"
fi

cat <<EOF

Parallel drill worktrees are ready.

Drill ID: $DRILL_ID
Base ref: $BASE_REF

Suggested ownership:
- api-data: only writer for services/api and tests/integration during this drill
- web-read: only writer for apps/web during this drill
- review: read-only review pass, no feature edits

Bootstrap:
- Python env link: root .venv is linked into each worktree when available
- Node deps: \`CI=1 pnpm install --frozen-lockfile\` runs inside each worktree by default
- Advanced skip: set \`BOOTSTRAP_WORKTREES=0\` before create if you only want the trees without dependency setup

Execution guide:
- docs/parallel-drill-first-wave.md
- docs/worktree-and-branching-runbook.md
EOF
