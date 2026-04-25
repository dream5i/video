from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.domain.scaffold import parse_iso_datetime, utc_now
from app.schemas import (
    AsyncTaskHealthSummary,
    MainChainHealthSummary,
    MoneyUsage,
    ObservabilityFailureItem,
    ObservabilitySignal,
    ObservabilitySummaryResponse,
    ProviderHealthSummary,
    RunStatusCount,
)

RunStatus = Literal["queued", "running", "succeeded", "failed"]
RunType = Literal["analysis", "render"]
ProviderCapability = Literal["analysis", "transcript", "ocr", "render", "tts"]

RUN_STATUSES: tuple[RunStatus, ...] = ("queued", "running", "succeeded", "failed")


@dataclass(frozen=True)
class ObservabilityRunSnapshot:
    id: str
    project_id: str
    project_title: str
    run_type: RunType
    status: RunStatus
    capability: ProviderCapability
    provider: str
    trace_id: str
    usage: MoneyUsage
    created_at: str
    completed_at: str | None = None
    error_message: str | None = None


def _success_rate(succeeded_count: int, total_count: int) -> float | None:
    if total_count == 0:
        return None
    return round(succeeded_count / total_count, 4)


def _latency_ms(created_at: str, completed_at: str | None) -> float | None:
    started = parse_iso_datetime(created_at)
    finished = parse_iso_datetime(completed_at)
    if started is None or finished is None:
        return None
    return round((finished - started).total_seconds() * 1000, 2)


def _build_signals(step_snapshot_evidence: str) -> list[ObservabilitySignal]:
    return [
        ObservabilitySignal(
            id="api-trace-headers",
            label="API 请求追踪头",
            status="ok",
            detail="API 会生成并回传 x-request-id / x-trace-id。",
            evidence="services/api/app/observability.py",
        ),
        ObservabilitySignal(
            id="structured-error-contract",
            label="统一错误契约",
            status="ok",
            detail="错误响应包含 message、errorCode、requestId、traceId。",
            evidence="services/api/app/errors.py",
        ),
        ObservabilitySignal(
            id="render-step-snapshots",
            label="运行步骤快照日志",
            status="ok",
            detail="render run 创建、完成、失败时会写结构化 step 状态。",
            evidence=step_snapshot_evidence,
        ),
        ObservabilitySignal(
            id="worker-provider-trace",
            label="Worker / Provider trace",
            status="partial",
            detail="当前已有 provider 抽象和 run trace，但 worker/provider 侧还没完整串到外部追踪平台。",
            evidence="docs/observability-and-alerting-baseline.md",
        ),
        ObservabilitySignal(
            id="external-alerting",
            label="外部告警平台",
            status="missing",
            detail="本轮先完成内部 API 与页面接线，Prometheus/Grafana 或云告警仍在后续 Gate。",
            evidence="docs/parallel-and-launch-gates.md",
        ),
    ]


def build_observability_summary(
    *,
    projects_total: int,
    workflow_drafts_total: int,
    result_assets_total: int,
    runs: list[ObservabilityRunSnapshot],
    step_snapshot_evidence: str,
) -> ObservabilitySummaryResponse:
    analysis_runs = [run for run in runs if run.run_type == "analysis"]
    render_runs = [run for run in runs if run.run_type == "render"]
    all_statuses = [run.status for run in runs]
    queued_runs = sum(1 for run in render_runs if run.status == "queued")
    running_runs = sum(1 for run in render_runs if run.status == "running")
    latest_run_updated_at = max((run.completed_at or run.created_at for run in render_runs), default=None)

    providers: dict[tuple[str, ProviderCapability], dict[str, object]] = {}
    for run in runs:
        key = (run.provider, run.capability)
        summary = providers.setdefault(
            key,
            {
                "total_runs": 0,
                "succeeded_runs": 0,
                "failed_runs": 0,
                "latencies": [],
                "estimated_cost_usd": 0.0,
                "last_event_at": None,
            },
        )
        summary["total_runs"] = int(summary["total_runs"]) + 1
        if run.status == "succeeded":
            summary["succeeded_runs"] = int(summary["succeeded_runs"]) + 1
        if run.status == "failed":
            summary["failed_runs"] = int(summary["failed_runs"]) + 1

        latency = _latency_ms(run.created_at, run.completed_at)
        if latency is not None:
            latencies = summary["latencies"]
            if isinstance(latencies, list):
                latencies.append(latency)

        summary["estimated_cost_usd"] = float(summary["estimated_cost_usd"]) + float(run.usage.estimated_cost_usd or 0)
        event_at = run.completed_at or run.created_at
        if summary["last_event_at"] is None or event_at > str(summary["last_event_at"]):
            summary["last_event_at"] = event_at

    provider_summaries = []
    for (provider, capability), summary in sorted(providers.items()):
        latencies = summary["latencies"] if isinstance(summary["latencies"], list) else []
        provider_summaries.append(
            ProviderHealthSummary(
                provider=provider,
                capability=capability,
                total_runs=int(summary["total_runs"]),
                succeeded_runs=int(summary["succeeded_runs"]),
                failed_runs=int(summary["failed_runs"]),
                average_latency_ms=round(sum(latencies) / len(latencies), 2) if latencies else None,
                estimated_cost_usd=round(float(summary["estimated_cost_usd"]), 6),
                last_event_at=str(summary["last_event_at"]) if summary["last_event_at"] else None,
            )
        )

    failures = [
        ObservabilityFailureItem(
            project_id=run.project_id,
            project_title=run.project_title,
            run_id=run.id,
            run_type=run.run_type,
            provider=run.provider,
            status="failed",
            trace_id=run.trace_id,
            error_code="ANALYSIS_ERROR" if run.run_type == "analysis" else "RENDER_ERROR",
            error_message=run.error_message,
            updated_at=run.completed_at or run.created_at,
        )
        for run in runs
        if run.status == "failed"
    ]
    failures.sort(key=lambda item: item.updated_at, reverse=True)

    return ObservabilitySummaryResponse(
        generated_at=utc_now(),
        main_chain=MainChainHealthSummary(
            projects_total=projects_total,
            analysis_runs_total=len(analysis_runs),
            analysis_success_rate=_success_rate(sum(1 for run in analysis_runs if run.status == "succeeded"), len(analysis_runs)),
            workflow_drafts_total=workflow_drafts_total,
            render_runs_total=len(render_runs),
            render_success_rate=_success_rate(sum(1 for run in render_runs if run.status == "succeeded"), len(render_runs)),
            result_assets_total=result_assets_total,
            run_status_counts=[RunStatusCount(status=status, count=all_statuses.count(status)) for status in RUN_STATUSES],
        ),
        async_tasks=AsyncTaskHealthSummary(
            queued_runs=queued_runs,
            running_runs=running_runs,
            active_runs=queued_runs + running_runs,
            stuck_runs=0,
            latest_run_updated_at=latest_run_updated_at,
        ),
        providers=provider_summaries,
        recent_failures=failures[:8],
        signals=_build_signals(step_snapshot_evidence),
    )
