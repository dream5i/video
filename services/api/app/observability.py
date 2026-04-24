from __future__ import annotations

import json
import logging
import os
from time import perf_counter
from typing import Any

from fastapi import Request

from app.domain.scaffold import make_id
from app.schemas import RenderRunDetailResponse, TraceContext

LOGGER_NAME = "new_project.api"
REQUEST_ID_HEADER = "x-request-id"
TRACE_ID_HEADER = "x-trace-id"


def configure_logging() -> None:
    if logging.getLogger().handlers:
        return

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level_name, logging.INFO), format="%(message)s")


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def log_event(event: str, **fields: Any) -> None:
    logger = get_logger()
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, ensure_ascii=False, default=str))


def ensure_request_context(request: Request) -> tuple[str, str]:
    request_id = request.headers.get(REQUEST_ID_HEADER) or make_id("req")
    trace_id = request.headers.get(TRACE_ID_HEADER) or make_id("trace")
    request.state.request_id = request_id
    request.state.trace_id = trace_id
    return request_id, trace_id


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", make_id("req"))


def get_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", make_id("trace"))


def trace_context_from_request(
    request: Request,
    existing_trace: TraceContext | None = None,
    *,
    actor_id: str = "user_demo",
    org_id: str = "org_demo",
) -> TraceContext:
    if existing_trace is not None:
        return existing_trace.model_copy(
            update={
                "request_id": get_request_id(request),
                "trace_id": get_trace_id(request),
            }
        )

    return TraceContext(
        trace_id=get_trace_id(request),
        request_id=get_request_id(request),
        actor_id=actor_id,
        org_id=org_id,
    )


def log_run_detail(
    event: str,
    request: Request | None,
    response: RenderRunDetailResponse,
    *,
    project_id: str,
) -> None:
    log_event(
        event,
        request_id=get_request_id(request) if request is not None else None,
        trace_id=response.run.trace_id,
        project_id=project_id,
        run_id=response.run.id,
        run_status=response.run.status,
        provider=response.run.provider,
        step_statuses={step.name: step.status for step in response.steps},
        estimated_cost_usd=response.run.usage.estimated_cost_usd,
    )


async def log_request_lifecycle(request: Request, call_next):
    request_id, trace_id = ensure_request_context(request)
    started_at = perf_counter()
    log_event(
        "api.request.started",
        request_id=request_id,
        trace_id=trace_id,
        method=request.method,
        path=request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        log_event(
            "api.request.failed",
            request_id=request_id,
            trace_id=trace_id,
            method=request.method,
            path=request.url.path,
            duration_ms=duration_ms,
        )
        raise

    duration_ms = round((perf_counter() - started_at) * 1000, 2)
    response.headers[REQUEST_ID_HEADER] = request_id
    response.headers[TRACE_ID_HEADER] = trace_id
    log_event(
        "api.request.completed",
        request_id=request_id,
        trace_id=trace_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms,
        project_id=request.path_params.get("project_id"),
        run_id=request.path_params.get("run_id"),
    )
    return response
