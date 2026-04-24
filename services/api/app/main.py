from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors import http_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.observability import configure_logging, log_request_lifecycle
from app.routes import router


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="全新项目 API", version="0.1.0")
    app.middleware("http")(log_request_lifecycle)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(router)
    return app


app = create_app()
