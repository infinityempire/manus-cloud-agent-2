#!/usr/bin/env bash
# Cancel queued/in-progress runs; delete completed runs older than N days; remove old/expired artifacts.
# Usage: ./scripts/cleanup-workflows.sh infinityempire manus-cloud-agent-2 30
set -euo pipefail
OWNER=${1:?owner}
REPO=${2:?repo}
DAYS=${3:-30}
CUTOFF=$(date -u -d "$DAYS days ago" +%s)

for S in queued in_progress; do
  gh run list -R "$OWNER/$REPO" --status "$S" --json databaseId -q '.[].databaseId' \
    | xargs -r -n1 gh run cancel -R "$OWNER/$REPO"
done

gh run list -R "$OWNER/$REPO" --status completed --limit 200 --json databaseId,createdAt -q \
  ".[] | select((.createdAt|fromdateiso8601) < $CUTOFF) | .databaseId" \
  | xargs -r -n1 gh run delete -R "$OWNER/$REPO"

gh api -X GET "/repos/$OWNER/$REPO/actions/artifacts?per_page=100" -q \
  ".artifacts[] | select(.expired==true) | .id" \
  | xargs -r -n1 -I{} gh api -X DELETE "/repos/$OWNER/$REPO/actions/artifacts/{}"
