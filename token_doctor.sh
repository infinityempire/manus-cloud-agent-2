# token_doctor.sh — Diagnose & fix GH token issues
# Usage: export GH_TOKEN=xxxxxxxx && bash token_doctor.sh
set -euo pipefail

OWNER=${OWNER:-infinityempire}
REPO=${REPO:-manus-cloud-agent-2}
HOST=${HOST:-github.com}

# 0) Pick up token
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
if [ -z "$TOKEN" ]; then
  echo "[ERROR] No GH_TOKEN/GITHUB_TOKEN in env."
  echo "Fix: export GH_TOKEN='your_token_here'  (use printf, not echo when piping to gh)"
  exit 1
fi

# 1) Obvious string pitfalls
LEN=$(printf "%s" "$TOKEN" | wc -c | tr -d ' ')
if [ "$LEN" -lt 30 ]; then
  echo "[ERROR] Token looks too short ($LEN chars). Copy it again completely."
  exit 1
fi
if printf "%s" "$TOKEN" | tr -d '[:print:]' | grep -q .; then
  echo "[ERROR] Token contains non-printable chars (maybe copied with newline). Re-copy."
  exit 1
fi
if printf "%s" "$TOKEN" | grep -q "[\"']"; then
  echo "[WARN] Token contains quotes. Remove any surrounding quotes."
fi

# 2) Basic API check (should be 200)
echo "[info] Checking /user..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.${HOST}/user")
if [ "$STATUS" != "200" ]; then
  echo "[ERROR] /user returned $STATUS (expected 200)."
  echo "Common causes: expired/revoked token, missing SSO authorization, wrong host."
  echo "If your org uses SSO: open token page and 'Enable SSO' for the org."
  exit 1
fi
echo "[ok] /user auth working."

# 3) Repo access check
echo "[info] Checking repo access for $OWNER/$REPO..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.${HOST}/repos/$OWNER/$REPO")
if [ "$STATUS" != "200" ]; then
  echo "[ERROR] Repo access check failed ($STATUS)."
  echo "Fix: Ensure the token has access to this repo:"
  echo " - Classic PAT: scope 'repo' (and 'workflow' if you dispatch workflows)."
  echo " - Fine-grained PAT: repository '$OWNER/$REPO' must be selected, Permissions:"
  echo "     Actions: Write, Contents: Read (and Write if pushing), Metadata: Read."
  echo " - If org enforces SSO/IP allow-list: authorize token for the org / allow IP."
  exit 1
fi
echo "[ok] Repo reachable with this token."

# 4) Workflow permission dry-run (no-op GET)
echo "[info] Checking Actions/Workflow API visibility..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.${HOST}/repos/$OWNER/$REPO/actions/workflows")
if [ "$STATUS" != "200" ]; then
  echo "[ERROR] Actions list returned $STATUS."
  echo "Fix: add Actions: Read (fine-grained) or 'repo' scope on classic PAT."
  exit 1
fi
echo "[ok] Actions API accessible."

# 5) gh CLI hookup (optional but recommended)
if command -v gh >/dev/null 2>&1; then
  printf "%s" "$TOKEN" | gh auth login --with-token || true
  gh auth status -h "$HOST" || true
else
  echo "[info] gh CLI not installed. You can use REST-only flow."
  echo "Install if needed: apt/brew/winget (see manual block below)."
fi

cat <<EOF
===============================================
[SUCCESS] Token looks valid & authorized for $OWNER/$REPO.
Next:

- To dispatch a workflow via REST:
  curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
    https://api.${HOST}/repos/$OWNER/$REPO/actions/workflows/android-apk.yml/dispatches \
    -d '{"ref":"main"}'

- If default branch != main, use the correct ref.
EOF
