### Summary
- Add Android Debug APK workflow (JDK 17), locate APK, upload as artifact for download.
- Document how to trigger and retrieve APK via GitHub Actions.
- Expand `.gitignore` for Gradle outputs, keystore files, OS artifacts.
- Introduce helper script to trigger a branch commit and kick off the build.
- Add CI cleanup toolkit and docs to cancel/delete stale runs and artifacts.

### Testing
- `python -m py_compile $(git ls-files '*.py')` (if applicable)
- `./gradlew assembleDebug` locally (optional)
- GitHub Actions run is green; artifact `app-debug-apk` is present

### Notes
- Debug build only (no signing). Release signing can be added later.
