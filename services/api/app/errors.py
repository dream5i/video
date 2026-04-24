from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.observability import get_request_id, get_trace_id, log_event


def build_error_detail(
    request: Request,
    *,
    error_code: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    detail: dict[str, Any] = {
        "message": message,
        "errorCode": error_code,
        "requestId": get_request_id(request),
        "traceId": get_trace_id(request),
    }
    if extra:
        detail.update(extra)
    return detail


def api_error(
    request: Request,
    *,
    status_code: int,
    error_code: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=build_error_detail(request, error_code=error_code, message=message, extra=extra),
    )


def _normalize_detail(request: Request, detail: Any, *, default_error_code: str) -> dict[str, Any]:
    if isinstance(detail, dict) and {"message", "errorCode", "requestId", "traceId"}.issubset(detail.keys()):
        return detail
    if isinstance(detail, str):
        return build_error_detail(request, error_code=default_error_code, message=detail)
    return build_error_detail(request, error_code=default_error_code, message="request failed", extra={"rawDetail": detail})


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = _normalize_detail(request, exc.detail, default_error_code="http_error")
    log_event(
        "api.error.http",
        request_id=detail["requestId"],
        trace_id=detail["traceId"],
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
        error_code=detail["errorCode"],
        message=detail["message"],
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": detail})


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    detail = build_error_detail(
        request,
        error_code="validation_error",
        message="request validation failed",
        extra={"validationErrors": exc.errors()},
    )
    log_event(
        "api.error.validation",
        request_id=detail["requestId"],
        trace_id=detail["traceId"],
        path=request.url.path,
        method=request.method,
        status_code=422,
        error_code=detail["errorCode"],
    )
    return JSONResponse(status_code=422, content={"detail": detail})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    detail = build_error_detail(
        request,
        error_code="internal_error",
        message="internal server error",
    )
    log_event(
        "api.error.unhandled",
        request_id=detail["requestId"],
        trace_id=detail["traceId"],
        path=request.url.path,
        method=request.method,
        status_code=500,
        error_code=detail["errorCode"],
        exception_type=exc.__class__.__name__,
    )
    return JSONResponse(status_code=500, content={"detail": detail})
