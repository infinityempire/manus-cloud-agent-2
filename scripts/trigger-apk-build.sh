#!/usr/bin/env bash
set -euo pipefail
BRANCH=${1:-ci/apk/trigger}

git checkout -B "$BRANCH"
: > .ci-touch
git add .ci-touch
git commit -m "ci: trigger APK build"
git push -u origin "$BRANCH"

echo "Pushed $BRANCH. Open a PR or check Actions for the run."
