from __future__ import annotations

import json
import logging
import os
from time import perf_counter
from typing import Callable

from worker.providers.interfaces import AnalysisProviderRequest, AnalysisProviderResult

LOGGER_NAME = "new_project.worker"

def configure_logging() -> None:
    if logging.getLogger().handlers:
        return

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level_name, logging.INFO), format="%(message)s")


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def log_event(event: str, **fields: object) -> None:
    payload = {"event": event, **fields}
    get_logger().info(json.dumps(payload, ensure_ascii=False, default=str))


def error_code_for_capability(capability: str) -> str:
    return {
        "analysis": "ANALYSIS_ERROR",
        "transcript": "TRANSCRIPT_ERROR",
        "ocr": "OCR_ERROR",
        "render": "RENDER_ERROR",
        "tts": "INTERNAL_ERROR",
    }.get(capability, "INTERNAL_ERROR")


def _analysis_trace_fields(
    *,
    request: AnalysisProviderRequest,
    provider: str,
    capability: str,
    model_name: str,
    status: str,
    latency_ms: float | None = None,
    retry_count: int = 0,
    estimated_cost_usd: float | None = None,
    error_code: str | None = None,
) -> dict[str, object]:
    return {
        "request_id": request.context.request_id,
        "trace_id": request.context.trace_id,
        "project_id": request.project_id,
        "analysis_run_id": request.context.run_id,
        "run_step_id": request.context.run_step_id,
        "provider": provider,
        "capability": capability,
        "model_name": model_name,
        "prompt_version": request.prompt_version,
        "status": status,
        "latency_ms": latency_ms,
        "retry_count": retry_count,
        "estimated_cost_usd": estimated_cost_usd,
        "error_code": error_code,
    }


def trace_analysis_provider_call(
    *,
    request: AnalysisProviderRequest,
    provider: str,
    model_name: str,
    operation: Callable[[], AnalysisProviderResult],
    retry_count: int = 0,
) -> AnalysisProviderResult:
    capability = "analysis"
    log_event(
        "provider.call.started",
        **_analysis_trace_fields(
            request=request,
            provider=provider,
            capability=capability,
            model_name=model_name,
            status="running",
            retry_count=retry_count,
        ),
    )

    started_at = perf_counter()
    try:
        result = operation()
    except Exception:
        latency_ms = round((perf_counter() - started_at) * 1000, 2)
        log_event(
            "provider.call.failed",
            **_analysis_trace_fields(
                request=request,
                provider=provider,
                capability=capability,
                model_name=model_name,
                status="failed",
                latency_ms=latency_ms,
                retry_count=retry_count,
                error_code=error_code_for_capability(capability),
            ),
        )
        raise

    latency_ms = round((perf_counter() - started_at) * 1000, 2)
    estimated_cost = result.usage.get("estimated_cost_usd")
    log_event(
        "provider.call.completed",
        **_analysis_trace_fields(
            request=request,
            provider=result.provider,
            capability=capability,
            model_name=model_name,
            status=result.status,
            latency_ms=latency_ms,
            retry_count=retry_count,
            estimated_cost_usd=float(estimated_cost) if estimated_cost is not None else None,
        ),
    )
    return result
