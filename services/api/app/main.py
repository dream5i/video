from __future__ import annotations

from fastapi import FastAPI

from app.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="全新项目 API", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()
