#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if [[ "${1:-}" == "--" ]]; then
  shift
fi

if [[ "$#" -eq 0 ]]; then
  cat <<'EOF'
Usage:
  bash scripts/worktree/bootstrap_worktree.sh <worktree-path> [more-worktree-paths...]

What this does:
1. Link the repository root `.venv` into each worktree when available
2. Run `pnpm install --frozen-lockfile` inside each worktree unless SKIP_NODE_INSTALL=1
EOF
  exit 1
fi

bootstrap_one() {
  local raw_path="$1"
  local target_path=""
  local exclude_path=""

  if [[ ! -d "$raw_path" ]]; then
    echo "Worktree path not found: $raw_path" >&2
    exit 1
  fi

  target_path="$(cd "$raw_path" && pwd)"

  if [[ ! -f "$target_path/package.json" ]]; then
    echo "Not a repository checkout with package.json: $target_path" >&2
    exit 1
  fi

  echo "Bootstrapping worktree: $target_path"

  exclude_path="$(git -C "$target_path" rev-parse --git-path info/exclude)"
  if [[ -n "$exclude_path" ]]; then
    mkdir -p "$(dirname "$exclude_path")"
    if ! grep -qxF ".venv" "$exclude_path" 2>/dev/null; then
      printf "\n.venv\n" >> "$exclude_path"
      echo "  Registered local ignore: .venv"
    fi
  fi

  if [[ -e "$ROOT_DIR/.venv" ]]; then
    if [[ -L "$target_path/.venv" ]]; then
      rm "$target_path/.venv"
    fi

    if [[ ! -e "$target_path/.venv" ]]; then
      ln -s "$ROOT_DIR/.venv" "$target_path/.venv"
      echo "  Linked Python env: $target_path/.venv -> $ROOT_DIR/.venv"
    else
      echo "  Skip Python env link: target already has its own .venv"
    fi
  else
    echo "  Skip Python env link: root .venv not found at $ROOT_DIR/.venv"
    echo "  Hint: see docs/local-development-runbook.md to create the root .venv first."
  fi

  if [[ "${SKIP_NODE_INSTALL:-0}" = "1" ]]; then
    echo "  Skip Node install: SKIP_NODE_INSTALL=1"
  else
    (
      cd "$target_path"
      CI=1 pnpm install --frozen-lockfile
    )
  fi
}

for worktree_path in "$@"; do
  bootstrap_one "$worktree_path"
done
