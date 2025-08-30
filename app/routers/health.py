from __future__ import annotations

import time
import psutil
from fastapi import APIRouter, FastAPI, Request
from typing import Awaitable, Callable
from fastapi.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    Histogram,
    generate_latest,
)

router = APIRouter()
registry = CollectorRegistry()
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    registry=registry,
)
CPU_USAGE = Gauge(
    "process_cpu_percent",
    "Process CPU usage percent",
    registry=registry,
)
MEMORY_USAGE = Gauge(
    "process_memory_bytes",
    "Process memory usage in bytes",
    registry=registry,
)

_process = psutil.Process()


async def metrics_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - start_time
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(latency)
    CPU_USAGE.set(_process.cpu_percent())
    MEMORY_USAGE.set(_process.memory_info().rss)
    return response


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.head("/healthz")
async def healthz_head() -> Response:
    return Response(status_code=200)


@router.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


@router.head("/metrics")
async def metrics_head() -> Response:
    return Response(media_type=CONTENT_TYPE_LATEST)


def setup(app: FastAPI) -> None:
    app.middleware("http")(metrics_middleware)
    app.include_router(router)
