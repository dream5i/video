from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request

from app.errors import api_error
from app.domain.interfaces import ProjectRepository
from app.domain.repository import get_project_repository
from app.observability import log_event, log_run_detail, trace_context_from_request
from app.providers.registry import provider_registry
from app.schemas import (
    AnalysisResultResponse,
    CreateProjectRequest,
    CreateRenderRunRequest,
    ObservabilitySummaryResponse,
    ProjectDetailResponse,
    ProjectHistoryResponse,
    ProjectResultResponse,
    RenderRunDetailResponse,
    WorkflowDraftResponse,
)

router = APIRouter(prefix="/api")
ProjectRepositoryDependency = Annotated[ProjectRepository, Depends(get_project_repository)]


def _process_render_run_in_background(
    repository: ProjectRepository,
    project_id: str,
    run_id: str,
    request_id: str,
    trace_id: str,
) -> None:
    render_provider = provider_registry.get("render")
    try:
        log_event(
            "run.background.started",
            request_id=request_id,
            trace_id=trace_id,
            project_id=project_id,
            run_id=run_id,
            provider=render_provider.primary,
        )
        response = repository.process_render_run(project_id, run_id, render_provider)
        log_event(
            "run.background.completed",
            request_id=request_id,
            trace_id=response.run.trace_id,
            project_id=project_id,
            run_id=run_id,
            provider=render_provider.primary,
            run_status=response.run.status,
            step_statuses={step.name: step.status for step in response.steps},
        )
    except Exception as exc:  # pragma: no cover
        try:
            response = repository.fail_render_run(project_id, run_id, render_provider, str(exc))
            log_event(
                "run.background.failed",
                request_id=request_id,
                trace_id=response.run.trace_id,
                project_id=project_id,
                run_id=run_id,
                provider=render_provider.primary,
                run_status=response.run.status,
                error_message=str(exc),
            )
        except Exception:
            return


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/observability/summary", response_model=ObservabilitySummaryResponse)
async def get_observability_summary(repository: ProjectRepositoryDependency) -> ObservabilitySummaryResponse:
    return repository.get_observability_summary()


@router.post("/projects", response_model=ProjectDetailResponse)
async def create_project(
    request: Request,
    input_data: CreateProjectRequest,
    repository: ProjectRepositoryDependency,
) -> ProjectDetailResponse:
    payload = input_data.model_copy(update={"trace": trace_context_from_request(request, input_data.trace)})
    return repository.create_project(payload)


@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
async def get_project(request: Request, project_id: str, repository: ProjectRepositoryDependency) -> ProjectDetailResponse:
    try:
        return repository.get_project(project_id)
    except KeyError as exc:
        raise api_error(request, status_code=404, error_code="project_not_found", message="project not found") from exc


@router.get("/projects/{project_id}/analysis", response_model=AnalysisResultResponse)
async def get_analysis(request: Request, project_id: str, repository: ProjectRepositoryDependency) -> AnalysisResultResponse:
    analysis_provider = provider_registry.get("analysis")
    try:
        return repository.get_analysis(project_id, analysis_provider, trace=trace_context_from_request(request))
    except KeyError as exc:
        raise api_error(request, status_code=404, error_code="project_not_found", message="project not found") from exc


@router.get("/projects/{project_id}/workflow", response_model=WorkflowDraftResponse)
async def get_workflow(request: Request, project_id: str, repository: ProjectRepositoryDependency) -> WorkflowDraftResponse:
    analysis_provider = provider_registry.get("analysis")
    try:
        return repository.get_workflow(project_id, analysis_provider, trace=trace_context_from_request(request))
    except KeyError as exc:
        raise api_error(request, status_code=404, error_code="project_not_found", message="project not found") from exc


@router.post("/projects/{project_id}/renders", response_model=RenderRunDetailResponse)
async def create_render_run(
    request: Request,
    project_id: str,
    input_data: CreateRenderRunRequest,
    background_tasks: BackgroundTasks,
    repository: ProjectRepositoryDependency,
) -> RenderRunDetailResponse:
    if input_data.project_id != project_id:
        raise api_error(request, status_code=400, error_code="project_id_mismatch", message="project id mismatch")
    render_provider = provider_registry.get("render")
    try:
        payload = input_data.model_copy(update={"trace": trace_context_from_request(request, input_data.trace)})
        response = repository.create_render_run(payload, render_provider)
        log_run_detail("run.created", request, response, project_id=project_id)
        background_tasks.add_task(
            _process_render_run_in_background,
            repository,
            project_id,
            response.run.id,
            payload.trace.request_id if payload.trace else None,
            response.run.trace_id,
        )
        return response
    except KeyError as exc:
        raise api_error(
            request,
            status_code=404,
            error_code="project_or_workflow_not_found",
            message="project or workflow not found",
        ) from exc


@router.get("/projects/{project_id}/runs/{run_id}", response_model=RenderRunDetailResponse)
async def get_render_run(
    request: Request,
    project_id: str,
    run_id: str,
    repository: ProjectRepositoryDependency,
) -> RenderRunDetailResponse:
    try:
        return repository.get_run_detail(project_id, run_id)
    except KeyError as exc:
        raise api_error(request, status_code=404, error_code="run_not_found", message="run not found") from exc


@router.get("/projects/{project_id}/result", response_model=ProjectResultResponse)
async def get_result(request: Request, project_id: str, repository: ProjectRepositoryDependency) -> ProjectResultResponse:
    try:
        asset = repository.get_result(project_id)
    except KeyError as exc:
        raise api_error(request, status_code=404, error_code="project_not_found", message="project not found") from exc
    return ProjectResultResponse(asset=asset)


@router.get("/history", response_model=ProjectHistoryResponse)
async def get_history(
    repository: ProjectRepositoryDependency,
    limit: int | None = Query(default=None, ge=1, le=100),
) -> ProjectHistoryResponse:
    return repository.get_history(limit=limit)
