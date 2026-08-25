from fastapi.testclient import TestClient

from src.main import MAX_BATCH, app

client = TestClient(app)


def test_health_and_readiness():
    assert client.get("/healthz").status_code == 200
    readiness = client.get("/readyz")
    assert readiness.status_code == 200
    assert readiness.json()["max_batch"] == MAX_BATCH


def test_analyze_is_deterministic():
    response = client.post(
        "/v1/analyze",
        json={
            "logs": [
                {"level": "INFO", "message": "started", "source": "api"},
                {"level": "ERROR", "message": "failed", "source": "worker"},
                {"level": "CRITICAL", "message": "stopped", "source": "worker"},
            ]
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["severe_count"] == 2
    assert payload["severe_rate"] == 2 / 3
    assert payload["levels"] == {"CRITICAL": 1, "ERROR": 1, "INFO": 1}
    assert payload["sources"] == {"api": 1, "worker": 2}


def test_rejects_invalid_or_unbounded_batches():
    assert client.post("/v1/analyze", json={"logs": []}).status_code == 422
    assert client.post(
        "/v1/analyze", json={"logs": [{"level": "TRACE", "message": "x"}]}
    ).status_code == 422
    assert client.post(
        "/v1/analyze", json={"logs": [{"level": "INFO", "message": "   "}]}
    ).status_code == 422
    too_many = [{"level": "INFO", "message": "x"}] * (MAX_BATCH + 1)
    assert client.post("/v1/analyze", json={"logs": too_many}).status_code == 422
