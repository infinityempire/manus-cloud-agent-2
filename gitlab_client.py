
import os, requests, time

HOST = os.getenv("GITLAB_HOST", "https://gitlab.com")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
BRANCH = os.getenv("GITLAB_BRANCH", "main")
TOKEN = os.getenv("GITLAB_TOKEN")
JOB_NAME = os.getenv("GITLAB_BUILD_JOB", "build_debug_apk")

HEADERS = {"PRIVATE-TOKEN": TOKEN}

def trigger_pipeline():
    url = f"{HOST}/api/v4/projects/{PROJECT_ID}/pipeline?ref={BRANCH}"
    r = requests.post(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["id"]

def wait_pipeline(pid, timeout=1800):
    end = time.time() + timeout
    while time.time() < end:
        r = requests.get(f"{HOST}/api/v4/projects/{PROJECT_ID}/pipelines/{pid}", headers=HEADERS)
        r.raise_for_status()
        status = r.json().get("status")
        if status in ["success", "failed", "canceled"]:
            return status
        time.sleep(10)
    raise TimeoutError("Pipeline timeout")

def download_artifact():
    url = f"{HOST}/api/v4/projects/{PROJECT_ID}/jobs/artifacts/{BRANCH}/download?job={JOB_NAME}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    path = f"/tmp/{JOB_NAME}.zip"
    with open(path, "wb") as f:
        f.write(r.content)
    return path
