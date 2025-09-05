
import os, requests, mimetypes

OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")
TOKEN = os.getenv("GITHUB_TOKEN")

def create_release_and_upload(tag, name, asset_path):
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"
    data = {"tag_name": tag, "name": name}
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    release = r.json()
    upload_url = release["upload_url"].split("{")[0]
    filename = os.path.basename(asset_path)
    mime = mimetypes.guess_type(filename)[0] or "application/zip"
    with open(asset_path, "rb") as f:
        up = requests.post(f"{upload_url}?name={filename}", headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": mime}, data=f)
    up.raise_for_status()
    return up.json()["browser_download_url"]
