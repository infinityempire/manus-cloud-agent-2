import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from manus2.config import settings


@retry(wait=wait_exponential(multiplier=0.5, max=8), stop=stop_after_attempt(3))
async def generate(prompt: str) -> str:
    """Generate text using the configured Ollama instance."""
    base = settings.ollama_base_url
    url = f"{base.rstrip('/')}/api/generate"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, json={"prompt": prompt})
            if r.status_code in {429,500,502,503,504}:
                raise httpx.HTTPStatusError("server error", request=r.request, response=r)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "")
    except httpx.HTTPStatusError:
        return "שגיאת שרת, נסה שוב מאוחר יותר."
    except httpx.RequestError:
        return "אין תגובה מהשרת."
