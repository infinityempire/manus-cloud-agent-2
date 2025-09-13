# GitHub CLI Examples

# Cancel queued runs
gh run list -R infinityempire/manus-cloud-agent-2 --status queued --json databaseId -q '.[].databaseId' \
| xargs -r -n1 gh run cancel -R infinityempire/manus-cloud-agent-2

# Cancel in-progress runs
gh run list -R infinityempire/manus-cloud-agent-2 --status in_progress --json databaseId -q '.[].databaseId' \
| xargs -r -n1 gh run cancel -R infinityempire/manus-cloud-agent-2

# Delete completed runs older than 30 days
CUTOFF=$(date -u -d "30 days ago" +%s)
gh run list -R infinityempire/manus-cloud-agent-2 --status completed --limit 200 --json databaseId,createdAt -q \
  ".[] | select((.createdAt|fromdateiso8601) < $CUTOFF) | .databaseId" \
| xargs -r -n1 gh run delete -R infinityempire/manus-cloud-agent-2

# List & delete old/expired artifacts
gh api -X GET "/repos/infinityempire/manus-cloud-agent-2/actions/artifacts?per_page=100" -q \
  ".artifacts[] | {id, name, expired, created_at}"

gh api -X GET "/repos/infinityempire/manus-cloud-agent-2/actions/artifacts?per_page=100" -q \
  ".artifacts[] | select(.expired==true) | .id" \
| xargs -r -n1 -I{} gh api -X DELETE "/repos/infinityempire/manus-cloud-agent-2/actions/artifacts/{}"
