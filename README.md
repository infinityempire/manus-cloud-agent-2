# manus-cloud-agent-2

[![Build & Artifact](https://github.com/infinityempire/manus-cloud-agent-2/actions/workflows/build-and-artifacts.yml/badge.svg)](../../actions/workflows/build-and-artifacts.yml)
[![Deploy to Railway](https://github.com/infinityempire/manus-cloud-agent-2/actions/workflows/deploy.yml/badge.svg)](../../actions/workflows/deploy.yml)
[![Post-Deploy Smoke](https://github.com/infinityempire/manus-cloud-agent-2/actions/workflows/smoke.yml/badge.svg)](../../actions/workflows/smoke.yml)

Minimal FastAPI service with `/health` and `/status`, CI that packages an APK-like artifact (zip of `manus2/`), Railway deployment, post-deploy smoke checks, and auto version bump on successful deploy.

## Endpoints
- `GET /health` → `{ "ok": true }`
- `GET /status` → service metadata

## Local run
```bash
pip install -r requirements.txt
uvicorn manus2.app:api --host 0.0.0.0 --port 8000
```

## Tests
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
```

### Android client (APK)
A minimal Flutter client lives in `client_flutter/`. The `flutter-android` workflow builds a debug APK and uploads it as the `client-apk` artifact (`app-debug.apk`). Set the `API_BASE_URL` secret to point the app at your server (defaults to `http://10.0.2.2:8000`).

## CI
- **Build & Artifact**: `.github/workflows/build-and-artifacts.yml`
- **Deploy to Railway**: `.github/workflows/deploy.yml`
- **Post-Deploy Smoke**: `.github/workflows/smoke.yml`
- **Version bump**: `.github/workflows/version-bump.yml`

### Secrets (GitHub → Settings → Secrets → Actions)
- `RAILWAY_TOKEN` (required)
- `RAILWAY_PUBLIC_URL` (required for smoke)
- `RAILWAY_PROJECT_ID` (optional)
- `RAILWAY_ENVIRONMENT` (optional)

## Versioning
Version lives in `VERSION` and is bumped automatically after a successful deploy; the app’s reported version is kept in sync.
