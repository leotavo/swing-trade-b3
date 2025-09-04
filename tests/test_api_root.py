from __future__ import annotations

from fastapi.testclient import TestClient

from swing_trade_b3.api.app import create_app


def test_root_redirects_to_docs() -> None:
    client = TestClient(create_app())
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location", "").endswith("/docs")
