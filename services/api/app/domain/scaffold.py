from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.schemas import (
    AnalysisInsight,
    AnalysisOutput,
    AnalysisSourceSummary,
    RunStepSummary,
    ScriptDraft,
    ShotPlan,
    ShotPlanSegment,
    TraceContext,
    WorkflowCTA,
    WorkflowDraft,
    WorkflowDraftSegment,
    WorkflowEdge,
    WorkflowLowCodeGraph,
    WorkflowMeta,
    WorkflowNode,
    WorkflowShot,
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def utc_now_datetime() -> datetime:
    return datetime.now(UTC)


def to_iso_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def parse_iso_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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


def build_analysis_output(project_title: str, source_type: str) -> AnalysisOutput:
    selling_points = (
        ["梨香清甜", "配料干净", "适合家庭场景"]
        if source_type == "video_url"
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
            platform="douyin" if source_type == "video_url" else None,
            source_type=source_type,
            title=project_title,
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
