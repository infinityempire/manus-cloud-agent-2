#!/usr/bin/env bash
# Trigger the Android APK workflow, wait for completion, and download the artifact.
# Requires: gh auth login (token with repo+workflow) or GITHUB_TOKEN env var.
# Usage: OWNER=infinityempire REPO=manus-cloud-agent-2 ./scripts/build_and_fetch_apk.sh
set -euo pipefail
OWNER=${OWNER:?set OWNER}
REPO=${REPO:?set REPO}
WF="Android APK (Debug)"

# Trigger workflow (workflow_dispatch) on provided ref (default: ci/apk)
REF=${REF:-ci/apk}
gh workflow run "$WF" -R "$OWNER/$REPO" --ref "$REF"

# Get latest run id for this workflow
sleep 2
RUN_ID=$(gh run list -R "$OWNER/$REPO" --workflow "$WF" --limit 1 --json databaseId -q '.[0].databaseId')
echo "[info] Watching run $RUN_ID"

gh run watch "$RUN_ID" -R "$OWNER/$REPO"

# Download artifact
mkdir -p artifacts/apk
gh run download "$RUN_ID" -R "$OWNER/$REPO" -n app-debug-apk -D artifacts/apk

APK_PATH=$(ls -1 artifacts/apk/*.apk 2>/dev/null | head -n1 || true)
if [ -n "$APK_PATH" ]; then
  echo "[ok] APK downloaded: $APK_PATH"
else
  echo "[warn] Artifact downloaded but APK file not found in artifacts/apk/"
  ls -la artifacts/apk || true
fi
