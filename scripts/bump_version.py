#!/usr/bin/env python3
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
version_file = root / "VERSION"
app_file = root / "manus2" / "app.py"

if not version_file.exists():
    version_file.write_text("0.1.1\n", encoding="utf-8")

cur = version_file.read_text(encoding="utf-8").strip()
m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", cur)
if not m:
    print(f"Invalid VERSION: {cur}", file=sys.stderr)
    sys.exit(1)
major, minor, patch = map(int, m.groups())
new = f"{major}.{minor}.{patch+1}"
version_file.write_text(new + "\n", encoding="utf-8")

app_src = app_file.read_text(encoding="utf-8")
app_src = re.sub(r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"',
                 f'version="{new}"', app_src, count=1)
app_file.write_text(app_src, encoding="utf-8")
print(new)
