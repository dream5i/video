from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.domain.repository import project_repository
from app.providers.registry import provider_registry
from app.schemas import (
    AnalysisResultResponse,
    CreateProjectRequest,
    CreateRenderRunRequest,
    ProjectDetailResponse,
    ProjectHistoryResponse,
    ProjectResultResponse,
    RenderRunDetailResponse,
    WorkflowDraftResponse,
)

router = APIRouter(prefix="/api")


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/projects", response_model=ProjectDetailResponse)
async def create_project(input_data: CreateProjectRequest) -> ProjectDetailResponse:
    return project_repository.create_project(input_data)


@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
async def get_project(project_id: str) -> ProjectDetailResponse:
    try:
        return project_repository.get_project(project_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="project not found") from exc


@router.get("/projects/{project_id}/analysis", response_model=AnalysisResultResponse)
async def get_analysis(project_id: str) -> AnalysisResultResponse:
    analysis_provider = provider_registry.get("analysis")
    try:
        return project_repository.get_analysis(project_id, analysis_provider)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="project not found") from exc


@router.get("/projects/{project_id}/workflow", response_model=WorkflowDraftResponse)
async def get_workflow(project_id: str) -> WorkflowDraftResponse:
    analysis_provider = provider_registry.get("analysis")
    try:
        return project_repository.get_workflow(project_id, analysis_provider)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="project not found") from exc


@router.post("/projects/{project_id}/renders", response_model=RenderRunDetailResponse)
async def create_render_run(project_id: str, input_data: CreateRenderRunRequest) -> RenderRunDetailResponse:
    if input_data.project_id != project_id:
        raise HTTPException(status_code=400, detail="project id mismatch")
    render_provider = provider_registry.get("render")
    try:
        return project_repository.create_render_run(input_data, render_provider)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="project or workflow not found") from exc


@router.get("/projects/{project_id}/runs/{run_id}", response_model=RenderRunDetailResponse)
async def get_render_run(project_id: str, run_id: str) -> RenderRunDetailResponse:
    try:
        return project_repository.get_run_detail(project_id, run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="run not found") from exc


@router.get("/projects/{project_id}/result", response_model=ProjectResultResponse)
async def get_result(project_id: str) -> ProjectResultResponse:
    try:
        asset = project_repository.get_result(project_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="project not found") from exc
    return ProjectResultResponse(asset=asset)


@router.get("/history", response_model=ProjectHistoryResponse)
async def get_history() -> ProjectHistoryResponse:
    return project_repository.get_history()
