import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import re
import psutil
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_report_process_info():
    client.get("/")
    client.get("/")
    expected_mem = psutil.Process().memory_info().rss

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics_text = metrics_response.text

    mem_match = re.search(r"^process_memory_bytes\s+([0-9.e+-]+)", metrics_text, re.MULTILINE)
    cpu_match = re.search(r"^process_cpu_percent\s+([0-9.e+-]+)", metrics_text, re.MULTILINE)

    assert mem_match is not None
    assert cpu_match is not None

    memory_metric = float(mem_match.group(1))
    cpu_metric = float(cpu_match.group(1))

    assert abs(memory_metric - expected_mem) < 10_000_000  # 10 MB tolerance
    assert cpu_metric >= 0
