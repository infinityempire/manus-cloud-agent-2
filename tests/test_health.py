import os, sys
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from manus2.app import api

client = TestClient(api)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

def test_status():
    r = client.get("/status")
    assert r.status_code == 200
    data = r.json()
    assert data.get("name") == "manus2"
    assert "python" in data
    assert "uptime_seconds" in data
