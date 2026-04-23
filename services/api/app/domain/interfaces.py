from __future__ import annotations

from typing import Protocol

from app.providers.registry import ProviderConfig
from app.schemas import (
    AnalysisResultResponse,
    CreateProjectRequest,
    CreateRenderRunRequest,
    OutputAssetSummary,
    ProjectDetailResponse,
    ProjectHistoryResponse,
    RenderRunDetailResponse,
    WorkflowDraftResponse,
)


class ProjectRepository(Protocol):
    def create_project(self, payload: CreateProjectRequest) -> ProjectDetailResponse: ...

    def get_project(self, project_id: str) -> ProjectDetailResponse: ...

    def get_analysis(self, project_id: str, provider: ProviderConfig) -> AnalysisResultResponse: ...

    def get_workflow(self, project_id: str, provider: ProviderConfig) -> WorkflowDraftResponse: ...

    def create_render_run(self, payload: CreateRenderRunRequest, provider: ProviderConfig) -> RenderRunDetailResponse: ...

    def get_run_detail(self, project_id: str, run_id: str) -> RenderRunDetailResponse: ...

    def get_result(self, project_id: str) -> OutputAssetSummary | None: ...

    def get_history(self) -> ProjectHistoryResponse: ...
