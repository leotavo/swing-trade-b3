from __future__ import annotations

from fastapi import FastAPI

from .routers import health

app = FastAPI()
health.setup(app)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"status": "ok"}
