# CI Best Practices

## Concurrency
Add to each workflow to auto-cancel older runs for the same branch/workflow:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Retention

Repository → Settings → Actions → General → set Artifact and log retention (e.g., 7–14 days).

## Triggers

Prefer selective triggers, e.g.:

```yaml
on:
  push:
    branches: [ main, ci/* ]
    paths:
      - 'app/**'
      - '.github/workflows/android-apk.yml'
  workflow_dispatch:
```

## Secrets

For debug builds no extra secrets are needed beyond the default GITHUB_TOKEN. For release signing, create keystore secrets and a separate release workflow.
