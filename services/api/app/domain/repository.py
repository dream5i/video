from __future__ import annotations

from functools import lru_cache

from app.config import get_api_settings
from app.domain.interfaces import ProjectRepository
from app.domain.scaffold import (
    build_analysis_output,
    build_run_steps,
    build_workflow_from_analysis,
    default_trace_context,
    make_id,
    utc_now,
)
from app.providers.registry import ProviderConfig
from app.schemas import (
    AnalysisInsight,
    AnalysisOutput,
    AnalysisResultResponse,
    AnalysisRunSummary,
    AnalysisSourceSummary,
    AuditEvent,
    CreateProjectRequest,
    CreateRenderRunRequest,
    MoneyUsage,
    OutputAssetSummary,
    ProjectDetail,
    ProjectDetailResponse,
    ProjectHistoryItem,
    ProjectHistoryResponse,
    PromptRegistryEntry,
    RenderRunDetailResponse,
    RenderRunSummary,
    RunStepSummary,
    ScriptDraft,
    ShotPlan,
    ShotPlanSegment,
    TraceContext,
    WorkflowCTA,
    WorkflowDraft,
    WorkflowDraftResponse,
    WorkflowDraftSegment,
    WorkflowEdge,
    WorkflowLowCodeGraph,
    WorkflowMeta,
    WorkflowNode,
    WorkflowShot,
)


class InMemoryProjectRepository(ProjectRepository):
    def __init__(self) -> None:
        self.projects: dict[str, ProjectDetail] = {}
        self.analysis_runs: dict[str, AnalysisRunSummary] = {}
        self.analysis_outputs: dict[str, AnalysisOutput] = {}
        self.workflow_drafts: dict[str, WorkflowDraft] = {}
        self.render_runs: dict[str, RenderRunSummary] = {}
        self.run_steps: dict[str, list[RunStepSummary]] = {}
        self.output_assets: dict[str, OutputAssetSummary] = {}
        self.audit_events: list[AuditEvent] = []
        self.prompts: dict[str, PromptRegistryEntry] = {
            "analysis": PromptRegistryEntry(
                id="prompt_analysis_active",
                capability="analysis",
                version="analysis.v1",
                status="active",
                model_family="openai",
                updated_at=utc_now(),
            ),
            "render": PromptRegistryEntry(
                id="prompt_render_active",
                capability="render",
                version="render.v1",
                status="active",
                model_family="provider-agnostic",
                updated_at=utc_now(),
            ),
        }
        self._seed_demo_project()

    def _record_audit(
        self,
        category: str,
        action: str,
        trace: TraceContext,
        project_id: str | None = None,
        run_id: str | None = None,
        metadata: dict[str, str | int | float | bool | None] | None = None,
    ) -> None:
        self.audit_events.append(
            AuditEvent(
                id=make_id("audit"),
                category=category,
                action=action,
                actor_id=trace.actor_id,
                org_id=trace.org_id,
                project_id=project_id,
                run_id=run_id,
                occurred_at=utc_now(),
                metadata=metadata or {},
            )
        )

    def _seed_demo_project(self) -> None:
        trace = default_trace_context()
        now = utc_now()
        project = ProjectDetail(
            id="proj_demo",
            org_id=trace.org_id,
            owner_id=trace.actor_id,
            title="纯粹计划小吊梨汤演示项目",
            source_type="video_url",
            current_stage="result_ready",
            updated_at=now,
            created_at=now,
            latest_analysis_run_id=None,
            latest_workflow_draft_id=None,
            latest_render_run_id=None,
        )
        self.projects[project.id] = project
        self._ensure_analysis(project.id, ProviderConfig(capability="analysis", primary="openai_analysis", fallback="anthropic_analysis", prompt_version="analysis.v1"))
        self._ensure_workflow(project.id)
        workflow = self.workflow_drafts[project.latest_workflow_draft_id or ""]
        self._create_render_run(
            CreateRenderRunRequest(project_id=project.id, workflow_draft_id=workflow.id, trace=trace),
            ProviderConfig(capability="render", primary="render_primary", fallback=None, prompt_version="render.v1"),
            completed=True,
        )

    def create_project(self, payload: CreateProjectRequest) -> ProjectDetailResponse:
        trace = payload.trace or default_trace_context()
        now = utc_now()
        project = ProjectDetail(
            id=make_id("proj"),
            org_id=trace.org_id,
            owner_id=trace.actor_id,
            title=payload.title or ("爆款链接项目" if payload.source_type == "video_url" else "商品信息项目"),
            source_type=payload.source_type,
            current_stage="draft",
            updated_at=now,
            created_at=now,
            latest_analysis_run_id=None,
            latest_workflow_draft_id=None,
            latest_render_run_id=None,
        )
        self.projects[project.id] = project
        self._record_audit("config", "project.created", trace, project_id=project.id, metadata={"sourceType": payload.source_type})
        return ProjectDetailResponse(project=project)

    def get_project(self, project_id: str) -> ProjectDetailResponse:
        return ProjectDetailResponse(project=self.projects[project_id])

    def _ensure_analysis(self, project_id: str, provider: ProviderConfig) -> AnalysisRunSummary:
        project = self.projects[project_id]
        if project.latest_analysis_run_id and project.latest_analysis_run_id in self.analysis_runs:
            return self.analysis_runs[project.latest_analysis_run_id]

        trace = default_trace_context()
        now = utc_now()
        run = AnalysisRunSummary(
            id=make_id("analysis"),
            project_id=project_id,
            status="succeeded",
            capability="analysis",
            provider=provider.primary,
            prompt_version=provider.prompt_version,
            trace_id=trace.trace_id,
            usage=MoneyUsage(input_tokens=980, output_tokens=240, estimated_cost_usd=0.021),
            created_at=now,
            completed_at=now,
            error_message=None,
        )
        analysis_output = build_analysis_output(project.title, project.source_type)
        self.analysis_runs[run.id] = run
        self.analysis_outputs[project_id] = analysis_output
        project.latest_analysis_run_id = run.id
        project.current_stage = "analysis_ready"
        project.updated_at = now
        self.projects[project_id] = project
        self._record_audit("run", "analysis.completed", trace, project_id=project_id, run_id=run.id, metadata={"provider": provider.primary})
        return run

    def get_analysis(self, project_id: str, provider: ProviderConfig) -> AnalysisResultResponse:
        run = self._ensure_analysis(project_id, provider)
        output = self.analysis_outputs[project_id]
        return AnalysisResultResponse(run=run, source_summary=output.source_summary, insights=output.insights)

    def _ensure_workflow(self, project_id: str) -> WorkflowDraft:
        project = self.projects[project_id]
        if project.latest_workflow_draft_id and project.latest_workflow_draft_id in self.workflow_drafts:
            return self.workflow_drafts[project.latest_workflow_draft_id]

        analysis_output = self.analysis_outputs[project_id]
        workflow = build_workflow_from_analysis(project_id, analysis_output)
        self.workflow_drafts[workflow.id] = workflow
        project.latest_workflow_draft_id = workflow.id
        project.current_stage = "workflow_ready"
        project.updated_at = workflow.updated_at
        self.projects[project_id] = project
        self._record_audit("run", "workflow.prefilled", default_trace_context(), project_id=project_id, metadata={"workflowVersion": workflow.version})
        return workflow

    def get_workflow(self, project_id: str, provider: ProviderConfig) -> WorkflowDraftResponse:
        self._ensure_analysis(project_id, provider)
        workflow = self._ensure_workflow(project_id)
        return WorkflowDraftResponse(workflow=workflow)

    def _create_render_run(
        self,
        payload: CreateRenderRunRequest,
        provider: ProviderConfig,
        *,
        completed: bool,
    ) -> RenderRunDetailResponse:
        project = self.projects[payload.project_id]
        workflow = self.workflow_drafts.get(payload.workflow_draft_id)
        if workflow is None or workflow.project_id != payload.project_id:
            raise KeyError(payload.workflow_draft_id)
        trace = payload.trace or default_trace_context()
        now = utc_now()
        status = "succeeded" if completed else "queued"
        completed_at = now if completed else None
        run = RenderRunSummary(
            id=make_id("render"),
            project_id=payload.project_id,
            workflow_draft_id=payload.workflow_draft_id,
            status=status,
            provider=provider.primary,
            trace_id=trace.trace_id,
            usage=MoneyUsage(input_tokens=120, output_tokens=0, estimated_cost_usd=0.18 if completed else 0.0),
            created_at=now,
            completed_at=completed_at,
            error_message=None,
        )
        steps = build_run_steps(provider.primary, status)
        self.render_runs[run.id] = run
        self.run_steps[run.id] = steps
        project.latest_render_run_id = run.id
        project.current_stage = "result_ready" if completed else "render_pending"
        project.updated_at = now
        self.projects[payload.project_id] = project
        if completed:
            self.output_assets[payload.project_id] = OutputAssetSummary(
                id=make_id("asset"),
                asset_type="video",
                storage_key=f"projects/{payload.project_id}/outputs/demo.mp4",
                preview_storage_key=f"projects/{payload.project_id}/outputs/demo-cover.jpg",
            )
        self._record_audit("run", "render.created", trace, project_id=payload.project_id, run_id=run.id, metadata={"provider": provider.primary, "completed": completed})
        return RenderRunDetailResponse(run=run, steps=steps)

    def create_render_run(self, payload: CreateRenderRunRequest, provider: ProviderConfig) -> RenderRunDetailResponse:
        return self._create_render_run(payload, provider, completed=False)

    def get_run_detail(self, project_id: str, run_id: str) -> RenderRunDetailResponse:
        run = self.render_runs[run_id]
        if run.project_id != project_id:
            raise KeyError(run_id)
        return RenderRunDetailResponse(run=run, steps=self.run_steps[run_id])

    def get_result(self, project_id: str) -> OutputAssetSummary | None:
        if project_id not in self.projects:
            raise KeyError(project_id)
        return self.output_assets.get(project_id)

    def get_history(self, limit: int | None = None) -> ProjectHistoryResponse:
        items = [
            ProjectHistoryItem(
                project_id=run.project_id,
                project_title=self.projects[run.project_id].title,
                run_id=run.id,
                run_type="render",
                status=run.status,
                updated_at=run.completed_at or run.created_at,
            )
            for run in sorted(self.render_runs.values(), key=lambda item: item.created_at, reverse=True)
        ]
        if limit is not None:
            items = items[:limit]
        return ProjectHistoryResponse(items=items)


def build_project_repository() -> ProjectRepository:
    backend = get_api_settings().repository_backend
    if backend == "database":
        from app.domain.sql_repository import SqlProjectRepository

        return SqlProjectRepository()
    if backend == "memory":
        return InMemoryProjectRepository()
    raise ValueError(f"Unsupported repository backend: {backend}")


@lru_cache(maxsize=1)
def get_project_repository() -> ProjectRepository:
    return build_project_repository()


def reset_project_repository() -> None:
    get_project_repository.cache_clear()
