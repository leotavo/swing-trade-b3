from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import CollectorRegistry, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import psutil
import time

app = FastAPI()
registry = CollectorRegistry()

# Metrics
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds",
    ["method", "endpoint"], registry=registry
)
CPU_USAGE = Gauge(
    "process_cpu_percent", "Process CPU usage percent", registry=registry
)
MEMORY_USAGE = Gauge(
    "process_memory_bytes", "Process memory usage in bytes", registry=registry
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - start_time
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(latency)
    # Update CPU and memory after each request
    process = psutil.Process()
    CPU_USAGE.set(process.cpu_percent())
    MEMORY_USAGE.set(process.memory_info().rss)
    return response

@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def read_root():
    return {"status": "ok"}
