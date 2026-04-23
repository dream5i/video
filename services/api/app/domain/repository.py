from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

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


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def default_trace_context() -> TraceContext:
    return TraceContext(
        trace_id=make_id("trace"),
        request_id=make_id("req"),
        actor_id="user_demo",
        org_id="org_demo",
    )


def build_low_code_graph() -> WorkflowLowCodeGraph:
    return WorkflowLowCodeGraph(
        schema_version="2026-04-23",
        nodes=[
            WorkflowNode(id="node_analysis", kind="analysis", label="素材分析", config={"mode": "auto"}),
            WorkflowNode(id="node_script", kind="script", label="脚本生成", config={"tone": "friendly"}),
            WorkflowNode(id="node_shot_plan", kind="shot_plan", label="镜头规划", config={"segments": 3}),
            WorkflowNode(id="node_render", kind="render", label="结果运行", config={"provider": "render_primary"}),
        ],
        edges=[
            WorkflowEdge(id="edge_analysis_script", from_="node_analysis", to="node_script"),
            WorkflowEdge(id="edge_script_shot", from_="node_script", to="node_shot_plan"),
            WorkflowEdge(id="edge_shot_render", from_="node_shot_plan", to="node_render"),
        ],
    )


def build_analysis_output(project: ProjectDetail) -> AnalysisOutput:
    selling_points = (
        ["梨香清甜", "配料干净", "适合家庭场景"]
        if project.source_type == "video_url"
        else ["信息更结构化", "适合低代码编排", "便于快速生成方案"]
    )
    opening = "前三秒先把核心记忆点打出去。"
    body = [
        "用一段真实场景，把产品优势和使用时刻绑在一起。",
        "第二段把差异点说人话，避免技术术语堆砌。",
    ]
    ending = "最后用轻 CTA 把用户引到下一步。"

    return AnalysisOutput(
        source_summary=AnalysisSourceSummary(
            platform="douyin" if project.source_type == "video_url" else None,
            source_type=project.source_type,
            title=project.title,
        ),
        insights=AnalysisInsight(
            target_audience=["宝妈", "家庭囤货人群"],
            selling_points=selling_points,
            hooks=["前三秒抓住真实使用场景", "突出干净、放心、好喝"],
            cta="引导继续生成完整工作流或直接发起运行。",
        ),
        script_draft=ScriptDraft(opening=opening, body=body, ending=ending),
        shot_plan=ShotPlan(
            segments=[
                ShotPlanSegment(id="shot_hook", visual="手持产品近景", subtitle="梨香浓郁清甜好喝", duration_sec=3),
                ShotPlanSegment(id="shot_body", visual="家庭分享场景", subtitle="配料表干净，给小孩喝更放心", duration_sec=6),
                ShotPlanSegment(id="shot_cta", visual="产品包装与桌面陈列", subtitle="先生成可执行草稿，再决定是否直接运行", duration_sec=3),
            ]
        ),
    )


def build_workflow_from_analysis(project_id: str, analysis_output: AnalysisOutput) -> WorkflowDraft:
    now = utc_now()
    shots = analysis_output.shot_plan.segments
    return WorkflowDraft(
        id=make_id("wf"),
        project_id=project_id,
        version=1,
        meta=WorkflowMeta(ratio="9:16", language="zh-CN", tone="friendly", style="clean-realistic"),
        segments=[
            WorkflowDraftSegment(
                id="seg_hook",
                goal="hook",
                script=analysis_output.script_draft.opening,
                duration_sec=3,
                shots=[WorkflowShot(id=shots[0].id, visual=shots[0].visual, subtitle=shots[0].subtitle, duration_sec=shots[0].duration_sec)],
            ),
            WorkflowDraftSegment(
                id="seg_body",
                goal="body",
                script=analysis_output.script_draft.body[0],
                duration_sec=6,
                shots=[WorkflowShot(id=shots[1].id, visual=shots[1].visual, subtitle=shots[1].subtitle, duration_sec=shots[1].duration_sec)],
            ),
            WorkflowDraftSegment(
                id="seg_cta",
                goal="cta",
                script=analysis_output.script_draft.ending,
                duration_sec=3,
                shots=[WorkflowShot(id=shots[2].id, visual=shots[2].visual, subtitle=shots[2].subtitle, duration_sec=shots[2].duration_sec)],
            ),
        ],
        cta=WorkflowCTA(text=analysis_output.insights.cta),
        low_code_graph=build_low_code_graph(),
        updated_at=now,
    )


def build_run_steps(provider: str, status: str) -> list[RunStepSummary]:
    step_status = "succeeded" if status == "succeeded" else status
    now = utc_now() if status == "succeeded" else None
    return [
        RunStepSummary(
            name="prepare_workflow",
            status=step_status,
            capability="render",
            provider=provider,
            started_at=now,
            finished_at=now,
            error_message=None,
        ),
        RunStepSummary(
            name="submit_render",
            status=step_status,
            capability="render",
            provider=provider,
            started_at=now,
            finished_at=now,
            error_message=None,
        ),
    ]


class InMemoryProjectRepository:
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
        analysis_output = build_analysis_output(project)
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

    def get_history(self) -> ProjectHistoryResponse:
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
        return ProjectHistoryResponse(items=items)


project_repository = InMemoryProjectRepository()
