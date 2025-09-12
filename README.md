# Android Debug APK via GitHub Actions

This repository builds a **debug APK** and publishes it as an artifact in GitHub Actions.

## How to trigger
1. Push any commit to `main`, `master`, or a branch starting with `ci/apk`, **or**
2. Trigger manually: GitHub → **Actions** → **Android APK (Debug)** → **Run workflow**.

## Where to download
- GitHub → **Actions** → open the latest successful run of **Android APK (Debug)** → **Artifacts** → `app-debug-apk`.

## Requirements
- Android project includes a module (typically `app`) with a working Gradle wrapper.
- Uses **JDK 17** and Gradle cache. Produces a **debug** APK (not signed for release).

## Local build (optional)
```bash
chmod +x gradlew
./gradlew clean assembleDebug --stacktrace --no-daemon
```

Result will usually be at app/build/outputs/apk/debug/app-debug.apk.
