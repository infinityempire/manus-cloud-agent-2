from pydantic import BaseModel

class HealthResponse(BaseModel):
    ok: bool = True

class StatusResponse(BaseModel):
    name: str
    version: str
    pid: int
    python: str
    platform: str
    uptime_seconds: float
