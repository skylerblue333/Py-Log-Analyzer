from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze():
    r = client.post("/api/v1/analyze", json=[
        {"level": "INFO", "message": "started"},
        {"level": "ERROR", "message": "failed"}
    ])
    assert r.status_code == 200
    assert r.json()["error_count"] == 1
    assert r.json()["error_rate"] == 0.5

