import os
import sys
import time
import platform
from fastapi import FastAPI

from manus2.config import settings
from manus2.utils.logger import get_logger
from manus2.utils.schemas import HealthResponse, StatusResponse
start_ts = time.time()
log = get_logger("manus2", settings.log_level)
api = FastAPI(title=settings.app_name, version=settings.version)

@api.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse()

@api.get("/status", response_model=StatusResponse)
async def status() -> StatusResponse:
    return StatusResponse(
        name=settings.app_name,
        version=settings.version,
        pid=os.getpid(),
        python=sys.version.split()[0],
        platform=f"{platform.system()} {platform.release()}",
        uptime_seconds=max(0.0, time.time() - start_ts),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("manus2.app:api", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
