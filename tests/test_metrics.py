import re

import psutil
from fastapi.testclient import TestClient
from prometheus_client import CONTENT_TYPE_LATEST

from app.main import app

client = TestClient(app)


def test_metrics_report_process_info() -> None:
    client.get("/healthz")
    expected_mem = psutil.Process().memory_info().rss

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    assert metrics_response.headers["content-type"] == CONTENT_TYPE_LATEST
    metrics_text = metrics_response.text

    assert metrics_text.startswith("# HELP")
    assert "# HELP process_cpu_percent" in metrics_text
    assert "# TYPE process_cpu_percent gauge" in metrics_text
    assert "# HELP process_memory_bytes" in metrics_text
    assert "# TYPE process_memory_bytes gauge" in metrics_text

    mem_match = re.search(
        r"^process_memory_bytes\s+([0-9.e+-]+)", metrics_text, re.MULTILINE
    )
    cpu_match = re.search(
        r"^process_cpu_percent\s+([0-9.e+-]+)", metrics_text, re.MULTILINE
    )

    assert mem_match is not None
    assert cpu_match is not None

    memory_metric = float(mem_match.group(1))
    cpu_metric = float(cpu_match.group(1))

    assert abs(memory_metric - expected_mem) < 10_000_000  # 10 MB tolerance
    assert cpu_metric >= 0


def test_metrics_head() -> None:
    response = client.head("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == CONTENT_TYPE_LATEST
