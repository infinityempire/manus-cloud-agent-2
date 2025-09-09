import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from manus2.config import settings


@retry(wait=wait_exponential(multiplier=0.5, max=8), stop=stop_after_attempt(3))
async def call_flow(path: str, payload: dict) -> dict:
    base = settings.n8n_base_url
    if not base:
        return {"error": "חסר N8N_BASE_URL"}
    url = f"{base.rstrip('/')}/{path.lstrip('/') }"
    headers = {}
    if settings.n8n_api_key:
        headers["X-N8N-API-Key"] = settings.n8n_api_key
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, json=payload, headers=headers)
            if r.status_code in {429,500,502,503,504}:
                raise httpx.HTTPStatusError("server error", request=r.request, response=r)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError:
        return {"error": "שגיאת שרת, נסה שוב"}
    except httpx.RequestError:
        return {"error": "אין תגובה מהשרת"}
