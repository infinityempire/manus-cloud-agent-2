#!/usr/bin/env bash
set -euo pipefail

NEED_SCOPES=(repo workflow)
# Prefer GH CLI auth if present; otherwise use $GITHUB_TOKEN
HAS_GH=$(command -v gh >/dev/null 2>&1 && echo yes || echo no)

if [ "$HAS_GH" = "yes" ]; then
  if gh auth status >/dev/null 2>&1; then
    echo "[ok] gh is authenticated"
    exit 0
  fi
fi

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "[warn] gh not authenticated; falling back to GITHUB_TOKEN env var"
  exit 0
fi

echo "[error] No valid auth found. Please create a Personal Access Token (classic) with 'repo' and 'workflow' scopes and set it via:\n\n  gh auth login --with-token < <(echo YOUR_TOKEN)\n  # or\n  # export GITHUB_TOKEN=YOUR_TOKEN\n" >&2
exit 1
