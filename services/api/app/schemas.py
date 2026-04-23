from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MoneyUsage(CamelModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost_usd: float | None = None


class ActorContext(CamelModel):
    actor_id: str
    org_id: str
    role: Literal["owner", "member", "service_account"]


class TraceContext(CamelModel):
    trace_id: str
    request_id: str
    actor_id: str
    org_id: str


class AuditEvent(CamelModel):
    id: str
    category: Literal["config", "run", "security", "data"]
    action: str
    actor_id: str
    org_id: str
    project_id: str | None = None
    run_id: str | None = None
    occurred_at: str
    metadata: dict[str, str | int | float | bool | None]


class PromptRegistryEntry(CamelModel):
    id: str
    capability: Literal["analysis", "transcript", "ocr", "render", "tts"]
    version: str
    status: Literal["draft", "active", "retired"]
    model_family: Literal["openai", "anthropic", "provider-agnostic"]
    updated_at: str


class ProductBrief(CamelModel):
    product_name: str
    target_audience: str
    selling_points: list[str]


class CreateProjectRequest(CamelModel):
    source_type: Literal["video_url", "product_brief"]
    source_url: str | None = None
    title: str | None = None
    ratio: Literal["9:16"]
    product_brief: ProductBrief | None = None
    trace: TraceContext | None = None


class ProjectSummary(CamelModel):
    id: str
    org_id: str
    owner_id: str
    title: str
    source_type: Literal["video_url", "product_brief"]
    current_stage: str
    updated_at: str


class ProjectDetail(ProjectSummary):
    created_at: str
    latest_analysis_run_id: str | None = None
    latest_workflow_draft_id: str | None = None
    latest_render_run_id: str | None = None


class ProjectDetailResponse(CamelModel):
    ok: bool = True
    project: ProjectDetail


class ProjectHistoryItem(CamelModel):
    project_id: str
    project_title: str
    run_id: str
    run_type: Literal["analysis", "render"]
    status: Literal["queued", "running", "succeeded", "failed"]
    updated_at: str


class ProjectHistoryResponse(CamelModel):
    ok: bool = True
    items: list[ProjectHistoryItem]


class AnalysisRunSummary(CamelModel):
    id: str
    project_id: str
    status: Literal["queued", "running", "succeeded", "failed"]
    capability: Literal["analysis", "transcript", "ocr", "render", "tts"]
    provider: str
    prompt_version: str
    trace_id: str
    usage: MoneyUsage
    created_at: str
    completed_at: str | None = None
    error_message: str | None = None


class AnalysisSourceSummary(CamelModel):
    platform: str | None = None
    source_type: Literal["video_url", "product_brief"]
    title: str


class AnalysisInsight(CamelModel):
    target_audience: list[str]
    selling_points: list[str]
    hooks: list[str]
    cta: str


class ScriptDraft(CamelModel):
    opening: str
    body: list[str]
    ending: str


class ShotPlanSegment(CamelModel):
    id: str
    visual: str
    subtitle: str
    duration_sec: int


class ShotPlan(CamelModel):
    segments: list[ShotPlanSegment]


class AnalysisOutput(CamelModel):
    source_summary: AnalysisSourceSummary
    insights: AnalysisInsight
    script_draft: ScriptDraft
    shot_plan: ShotPlan


class AnalysisResultResponse(CamelModel):
    ok: bool = True
    run: AnalysisRunSummary
    source_summary: AnalysisSourceSummary
    insights: AnalysisInsight


class WorkflowShot(CamelModel):
    id: str
    visual: str
    subtitle: str
    duration_sec: int


class WorkflowDraftSegment(CamelModel):
    id: str
    goal: Literal["hook", "body", "cta"]
    script: str
    duration_sec: int
    shots: list[WorkflowShot]


class WorkflowMeta(CamelModel):
    ratio: Literal["9:16"]
    language: Literal["zh-CN"]
    tone: str
    style: str


class WorkflowCTA(CamelModel):
    text: str


class WorkflowNode(CamelModel):
    id: str
    kind: Literal["analysis", "script", "shot_plan", "render", "approval"]
    label: str
    config: dict[str, str | int | float | bool | None]


class WorkflowEdge(CamelModel):
    id: str
    from_: str
    to: str

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class WorkflowLowCodeGraph(CamelModel):
    schema_version: Literal["2026-04-23"]
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]


class WorkflowDraft(CamelModel):
    id: str
    project_id: str
    version: int
    meta: WorkflowMeta
    segments: list[WorkflowDraftSegment]
    cta: WorkflowCTA
    low_code_graph: WorkflowLowCodeGraph
    updated_at: str


class WorkflowDraftResponse(CamelModel):
    ok: bool = True
    workflow: WorkflowDraft


class RunStepSummary(CamelModel):
    name: str
    status: Literal["queued", "running", "succeeded", "failed"]
    capability: Literal["analysis", "transcript", "ocr", "render", "tts"]
    provider: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    error_message: str | None = None


class CreateRenderRunRequest(CamelModel):
    project_id: str
    workflow_draft_id: str
    trace: TraceContext | None = None


class RenderRunSummary(CamelModel):
    id: str
    project_id: str
    workflow_draft_id: str
    status: Literal["queued", "running", "succeeded", "failed"]
    provider: str
    trace_id: str
    usage: MoneyUsage
    created_at: str
    completed_at: str | None = None
    error_message: str | None = None


class OutputAssetSummary(CamelModel):
    id: str
    asset_type: Literal["video", "image", "json"]
    storage_key: str
    preview_storage_key: str | None = None


class RenderRunDetailResponse(CamelModel):
    ok: bool = True
    run: RenderRunSummary
    steps: list[RunStepSummary]


class ProjectResultResponse(CamelModel):
    ok: bool = True
    asset: OutputAssetSummary | None = None
