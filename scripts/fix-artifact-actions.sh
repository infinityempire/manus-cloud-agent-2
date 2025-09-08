#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob
for f in .github/workflows/*.yml .github/workflows/*.yaml; do
  tmp="${f}.tmp"
  sed -E \
    -e 's|(actions/upload-artifact)@v[0-9]+|\1@v4|g' \
    -e 's|(actions/download-artifact)@v[0-9]+|\1@v4|g' \
    "$f" > "$tmp"
  mv "$tmp" "$f"
  echo "Updated: $f"
done
echo "✅ All artifact actions bumped to v4."
