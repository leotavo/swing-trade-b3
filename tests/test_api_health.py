from __future__ import annotations

from fastapi.testclient import TestClient

from swing_trade_b3.api.app import create_app


def test_health_endpoint_ok() -> None:
    client = TestClient(create_app())
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert isinstance(data.get("version"), str)
    assert data["version"]
