import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from manus2.config import settings


@retry(wait=wait_exponential(multiplier=0.5, max=8), stop=stop_after_attempt(3))
async def trigger_workflow(workflow: str, ref: str = "main") -> str:
    token = settings.github_token
    owner = settings.repo_owner
    name = settings.repo_name
    if not token or not owner or not name:
        return "חסר טוקן או פרטי מאגר"
    repo = f"{owner}/{name}"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, json={"ref": ref}, headers=headers)
            if r.status_code >= 400:
                raise httpx.HTTPStatusError("server error", request=r.request, response=r)
    except httpx.HTTPStatusError:
        return "לא ניתן להפעיל את ה-Workflow, נסה שוב."
    except httpx.RequestError:
        return "בעיית חיבור ל-GitHub."
    return "ה-Workflow הופעל בהצלחה."
