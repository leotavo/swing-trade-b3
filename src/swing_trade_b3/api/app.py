from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from swing_trade_b3 import __version__


class HealthResponse(BaseModel):
    status: str
    version: str


def create_app() -> FastAPI:
    app = FastAPI(title="swing-trade-b3 API", version=__version__)

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:  # noqa: ANN202 - FastAPI infers
        return RedirectResponse(url="/docs", status_code=307)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    def health() -> HealthResponse:  # noqa: ANN202 - FastAPI infers
        return HealthResponse(status="ok", version=__version__)

    return app
