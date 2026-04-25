from __future__ import annotations

from typing import Protocol

from app.providers.registry import ProviderConfig
from app.schemas import (
    AnalysisResultResponse,
    CreateProjectRequest,
    CreateRenderRunRequest,
    OutputAssetSummary,
    ObservabilitySummaryResponse,
    ProjectDetailResponse,
    ProjectHistoryResponse,
    RenderRunDetailResponse,
    TraceContext,
    WorkflowDraftResponse,
)


class ProjectRepository(Protocol):
    def create_project(self, payload: CreateProjectRequest) -> ProjectDetailResponse: ...

    def get_project(self, project_id: str) -> ProjectDetailResponse: ...

    def get_analysis(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> AnalysisResultResponse: ...

    def get_workflow(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> WorkflowDraftResponse: ...

    def create_render_run(self, payload: CreateRenderRunRequest, provider: ProviderConfig) -> RenderRunDetailResponse: ...

    def process_render_run(self, project_id: str, run_id: str, provider: ProviderConfig) -> RenderRunDetailResponse: ...

    def fail_render_run(
        self,
        project_id: str,
        run_id: str,
        provider: ProviderConfig,
        error_message: str,
    ) -> RenderRunDetailResponse: ...

    def get_run_detail(self, project_id: str, run_id: str) -> RenderRunDetailResponse: ...

    def get_result(self, project_id: str) -> OutputAssetSummary | None: ...

    def get_history(self, limit: int | None = None) -> ProjectHistoryResponse: ...

    def get_observability_summary(self) -> ObservabilitySummaryResponse: ...
