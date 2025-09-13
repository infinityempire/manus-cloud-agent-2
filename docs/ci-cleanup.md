# CI Cleanup: Cancel & Delete Stale Workflow Runs and Artifacts

This repo includes a script to keep GitHub Actions tidy.

## Quick start
```bash
# Authenticate once
gh auth login

# Cancel queued/in-progress runs and delete old ones (>30 days) in repo infinityempire/manus-cloud-agent-2
./scripts/cleanup-workflows.sh infinityempire manus-cloud-agent-2 30
```

Notes

Requires GitHub CLI (gh) with repo+workflow scopes.

Adjust the 30 days parameter as needed (e.g., 14, 7).

Combine with retention settings (below) for best results.
