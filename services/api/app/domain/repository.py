from __future__ import annotations

from threading import Lock

from app.config import get_api_settings
from app.domain.interfaces import ProjectRepository
from app.domain.observability_summary import ObservabilityRunSnapshot, build_observability_summary
from app.domain.scaffold import (
    build_analysis_output,
    build_output_asset_summary,
    build_render_run_steps,
    build_workflow_from_analysis,
    default_trace_context,
    make_id,
    utc_now,
)
from app.observability import log_event
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
    ObservabilitySummaryResponse,
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

    def _trace_for_project(self, project: ProjectDetail, trace_id: str | None = None) -> TraceContext:
        return TraceContext(
            trace_id=trace_id or make_id("trace"),
            request_id=make_id("req"),
            actor_id=project.owner_id,
            org_id=project.org_id,
        )

    def _project_title(self, project_id: str) -> str:
        project = self.projects.get(project_id)
        return project.title if project is not None else project_id

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

    def _ensure_analysis(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> AnalysisRunSummary:
        project = self.projects[project_id]
        if project.latest_analysis_run_id and project.latest_analysis_run_id in self.analysis_runs:
            return self.analysis_runs[project.latest_analysis_run_id]

        trace = trace or default_trace_context()
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

    def get_analysis(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> AnalysisResultResponse:
        run = self._ensure_analysis(project_id, provider, trace=trace)
        output = self.analysis_outputs[project_id]
        return AnalysisResultResponse(run=run, source_summary=output.source_summary, insights=output.insights)

    def _ensure_workflow(self, project_id: str, trace: TraceContext | None = None) -> WorkflowDraft:
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
        self._record_audit(
            "run",
            "workflow.prefilled",
            trace or default_trace_context(),
            project_id=project_id,
            metadata={"workflowVersion": workflow.version},
        )
        return workflow

    def get_workflow(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> WorkflowDraftResponse:
        self._ensure_analysis(project_id, provider, trace=trace)
        workflow = self._ensure_workflow(project_id, trace=trace)
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
        usage = MoneyUsage(input_tokens=120, output_tokens=0, estimated_cost_usd=0.18 if completed else 0.0)
        run = RenderRunSummary(
            id=make_id("render"),
            project_id=payload.project_id,
            workflow_draft_id=payload.workflow_draft_id,
            status=status,
            provider=provider.primary,
            trace_id=trace.trace_id,
            usage=usage,
            created_at=now,
            completed_at=completed_at,
            error_message=None,
        )
        steps = build_render_run_steps(
            provider.primary,
            status,
            started_at=now if completed else None,
            finished_at=completed_at,
        )
        self.render_runs[run.id] = run
        self.run_steps[run.id] = steps
        project.latest_render_run_id = run.id
        project.current_stage = "result_ready" if completed else "render_pending"
        project.updated_at = now
        self.projects[payload.project_id] = project
        if completed:
            self.output_assets[run.id] = build_output_asset_summary(payload.project_id, run.id)
        self._record_audit("run", "render.created", trace, project_id=payload.project_id, run_id=run.id, metadata={"provider": provider.primary, "completed": completed})
        return RenderRunDetailResponse(run=run, steps=steps)

    def create_render_run(self, payload: CreateRenderRunRequest, provider: ProviderConfig) -> RenderRunDetailResponse:
        response = self._create_render_run(payload, provider, completed=False)
        log_event(
            "run.step.snapshot",
            trace_id=response.run.trace_id,
            project_id=payload.project_id,
            run_id=response.run.id,
            run_status=response.run.status,
            step_statuses={step.name: step.status for step in response.steps},
        )
        return response

    def process_render_run(self, project_id: str, run_id: str, provider: ProviderConfig) -> RenderRunDetailResponse:
        project = self.projects[project_id]
        run = self.render_runs[run_id]
        if run.project_id != project_id:
            raise KeyError(run_id)
        if run.status == "failed":
            return self.get_run_detail(project_id, run_id)
        if run.status == "succeeded":
            if run_id not in self.output_assets:
                self.output_assets[run_id] = build_output_asset_summary(project_id, run_id)
            return self.get_run_detail(project_id, run_id)

        finished_at = utc_now()
        self.render_runs[run_id] = run.model_copy(
            update={
                "status": "succeeded",
                "completed_at": finished_at,
                "error_message": None,
                "usage": MoneyUsage(input_tokens=120, output_tokens=0, estimated_cost_usd=0.18),
            }
        )
        self.run_steps[run_id] = build_render_run_steps(
            provider.primary,
            "succeeded",
            started_at=run.created_at,
            finished_at=finished_at,
        )
        self.output_assets[run_id] = build_output_asset_summary(project_id, run_id)

        if project.latest_render_run_id == run_id:
            project.current_stage = "result_ready"
            project.updated_at = finished_at
            self.projects[project_id] = project

        self._record_audit(
            "run",
            "render.completed",
            self._trace_for_project(project, run.trace_id),
            project_id=project_id,
            run_id=run_id,
            metadata={"provider": provider.primary},
        )
        log_event(
            "run.step.snapshot",
            trace_id=run.trace_id,
            project_id=project_id,
            run_id=run_id,
            run_status="succeeded",
            step_statuses={step.name: step.status for step in self.run_steps[run_id]},
        )
        return self.get_run_detail(project_id, run_id)

    def fail_render_run(
        self,
        project_id: str,
        run_id: str,
        provider: ProviderConfig,
        error_message: str,
    ) -> RenderRunDetailResponse:
        project = self.projects[project_id]
        run = self.render_runs[run_id]
        if run.project_id != project_id:
            raise KeyError(run_id)
        if run.status == "succeeded":
            return self.get_run_detail(project_id, run_id)

        finished_at = utc_now()
        self.render_runs[run_id] = run.model_copy(
            update={
                "status": "failed",
                "completed_at": finished_at,
                "error_message": error_message,
                "usage": MoneyUsage(input_tokens=120, output_tokens=0, estimated_cost_usd=0.0),
            }
        )
        self.run_steps[run_id] = build_render_run_steps(
            provider.primary,
            "failed",
            started_at=run.created_at,
            finished_at=finished_at,
            error_message=error_message,
        )

        if project.latest_render_run_id == run_id:
            project.current_stage = "failed"
            project.updated_at = finished_at
            self.projects[project_id] = project

        self._record_audit(
            "run",
            "render.failed",
            self._trace_for_project(project, run.trace_id),
            project_id=project_id,
            run_id=run_id,
            metadata={"provider": provider.primary, "errorMessage": error_message},
        )
        log_event(
            "run.step.snapshot",
            trace_id=run.trace_id,
            project_id=project_id,
            run_id=run_id,
            run_status="failed",
            step_statuses={step.name: step.status for step in self.run_steps[run_id]},
            error_message=error_message,
        )
        return self.get_run_detail(project_id, run_id)

    def get_run_detail(self, project_id: str, run_id: str) -> RenderRunDetailResponse:
        run = self.render_runs[run_id]
        if run.project_id != project_id:
            raise KeyError(run_id)
        return RenderRunDetailResponse(run=run, steps=self.run_steps[run_id])

    def get_result(self, project_id: str) -> OutputAssetSummary | None:
        project = self.projects.get(project_id)
        if project is None:
            raise KeyError(project_id)
        if project.latest_render_run_id is None:
            return None
        return self.output_assets.get(project.latest_render_run_id)

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

    def get_observability_summary(self) -> ObservabilitySummaryResponse:
        analysis_runs = [
            ObservabilityRunSnapshot(
                id=run.id,
                project_id=run.project_id,
                project_title=self._project_title(run.project_id),
                run_type="analysis",
                status=run.status,
                capability=run.capability,
                provider=run.provider,
                trace_id=run.trace_id,
                usage=run.usage,
                created_at=run.created_at,
                completed_at=run.completed_at,
                error_message=run.error_message,
            )
            for run in self.analysis_runs.values()
        ]
        render_runs = [
            ObservabilityRunSnapshot(
                id=run.id,
                project_id=run.project_id,
                project_title=self._project_title(run.project_id),
                run_type="render",
                status=run.status,
                capability="render",
                provider=run.provider,
                trace_id=run.trace_id,
                usage=run.usage,
                created_at=run.created_at,
                completed_at=run.completed_at,
                error_message=run.error_message,
            )
            for run in self.render_runs.values()
        ]
        return build_observability_summary(
            projects_total=len(self.projects),
            workflow_drafts_total=len(self.workflow_drafts),
            result_assets_total=len(self.output_assets),
            runs=[*analysis_runs, *render_runs],
            step_snapshot_evidence="services/api/app/domain/repository.py",
        )


def build_project_repository() -> ProjectRepository:
    backend = get_api_settings().repository_backend
    if backend == "database":
        from app.domain.sql_repository import SqlProjectRepository

        return SqlProjectRepository()
    if backend == "memory":
        return InMemoryProjectRepository()
    raise ValueError(f"Unsupported repository backend: {backend}")


_repository_instance: ProjectRepository | None = None
_repository_lock = Lock()


def get_project_repository() -> ProjectRepository:
    global _repository_instance

    if _repository_instance is not None:
        return _repository_instance

    with _repository_lock:
        if _repository_instance is None:
            _repository_instance = build_project_repository()
        return _repository_instance


def reset_project_repository() -> None:
    global _repository_instance

    with _repository_lock:
        _repository_instance = None
