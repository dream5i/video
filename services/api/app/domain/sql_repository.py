from __future__ import annotations

from sqlalchemy import Select, desc, select

from app.config import get_api_settings
from app.db.base import Base
from app.db.models import (
    AnalysisOutputRecord,
    AnalysisRunRecord,
    AuditEventRecord,
    OutputAssetRecord,
    ProjectRecord,
    PromptRegistryRecord,
    RenderRunRecord,
    RunStepRecord,
    WorkflowDraftRecord,
)
from app.db.session import get_engine, get_session_factory
from app.domain.interfaces import ProjectRepository
from app.domain.scaffold import (
    build_analysis_output,
    build_output_asset_summary,
    build_render_run_steps,
    build_workflow_from_analysis,
    default_trace_context,
    make_id,
    parse_iso_datetime,
    to_iso_datetime,
    utc_now_datetime,
)
from app.observability import log_event
from app.providers.registry import ProviderConfig
from app.schemas import (
    AnalysisOutput,
    AnalysisResultResponse,
    AnalysisRunSummary,
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
    TraceContext,
    WorkflowDraft,
    WorkflowDraftResponse,
)


class SqlProjectRepository(ProjectRepository):
    def __init__(self, *, database_url: str | None = None) -> None:
        settings = get_api_settings()
        self._database_url = database_url or settings.database_url
        self._session_factory = get_session_factory(self._database_url)
        if self._database_url.startswith("sqlite"):
            Base.metadata.create_all(bind=get_engine(self._database_url))
        self._ensure_seed_data()

    def _record_audit(
        self,
        session,
        category: str,
        action: str,
        trace: TraceContext,
        *,
        project_id: str | None = None,
        run_id: str | None = None,
        metadata: dict[str, str | int | float | bool | None] | None = None,
    ) -> None:
        session.add(
            AuditEventRecord(
                id=make_id("audit"),
                category=category,
                action=action,
                actor_id=trace.actor_id,
                org_id=trace.org_id,
                project_id=project_id,
                run_id=run_id,
                occurred_at=utc_now_datetime(),
                metadata_json=metadata or {},
            )
        )

    def _seed_prompt_registry(self, session) -> None:
        existing_ids = {
            item[0]
            for item in session.execute(select(PromptRegistryRecord.id).where(PromptRegistryRecord.id.in_(["prompt_analysis_active", "prompt_render_active"])))
        }

        if "prompt_analysis_active" not in existing_ids:
            session.add(
                PromptRegistryRecord(
                    id="prompt_analysis_active",
                    capability="analysis",
                    version="analysis.v1",
                    status="active",
                    model_family="openai",
                    updated_at=utc_now_datetime(),
                )
            )

        if "prompt_render_active" not in existing_ids:
            session.add(
                PromptRegistryRecord(
                    id="prompt_render_active",
                    capability="render",
                    version="render.v1",
                    status="active",
                    model_family="provider-agnostic",
                    updated_at=utc_now_datetime(),
                )
            )

    def _ensure_seed_data(self) -> None:
        with self._session_factory() as session:
            self._seed_prompt_registry(session)
            existing_demo = session.get(ProjectRecord, "proj_demo")
            if existing_demo is not None:
                session.commit()
                return

            trace = default_trace_context()
            now = utc_now_datetime()
            project = ProjectRecord(
                id="proj_demo",
                org_id=trace.org_id,
                owner_id=trace.actor_id,
                title="纯粹计划小吊梨汤演示项目",
                source_type="video_url",
                source_url="https://example.com/demo",
                source_payload_json=None,
                current_stage="result_ready",
                latest_analysis_run_id=None,
                latest_workflow_draft_id=None,
                latest_render_run_id=None,
                created_at=now,
                updated_at=now,
            )
            session.add(project)
            session.flush()

            analysis_provider = ProviderConfig(
                capability="analysis",
                primary="openai_analysis",
                fallback="anthropic_analysis",
                prompt_version="analysis.v1",
            )
            render_provider = ProviderConfig(
                capability="render",
                primary="render_primary",
                fallback=None,
                prompt_version="render.v1",
            )
            self._ensure_analysis(session, project.id, analysis_provider)
            workflow_record = self._ensure_workflow(session, project.id)
            self._create_render_run(
                session,
                CreateRenderRunRequest(project_id=project.id, workflow_draft_id=workflow_record.id, trace=trace),
                render_provider,
                completed=True,
            )
            session.commit()

    def _project_record_to_detail(self, record: ProjectRecord) -> ProjectDetail:
        return ProjectDetail(
            id=record.id,
            org_id=record.org_id,
            owner_id=record.owner_id,
            title=record.title,
            source_type=record.source_type,
            current_stage=record.current_stage,
            updated_at=to_iso_datetime(record.updated_at) or "",
            created_at=to_iso_datetime(record.created_at) or "",
            latest_analysis_run_id=record.latest_analysis_run_id,
            latest_workflow_draft_id=record.latest_workflow_draft_id,
            latest_render_run_id=record.latest_render_run_id,
        )

    def _analysis_run_to_summary(self, record: AnalysisRunRecord) -> AnalysisRunSummary:
        return AnalysisRunSummary(
            id=record.id,
            project_id=record.project_id,
            status=record.status,
            capability=record.capability,
            provider=record.provider,
            prompt_version=record.prompt_version,
            trace_id=record.trace_id,
            usage=MoneyUsage(**(record.usage_json or {})),
            created_at=to_iso_datetime(record.created_at) or "",
            completed_at=to_iso_datetime(record.completed_at),
            error_message=record.error_message,
        )

    def _analysis_output_to_schema(self, record: AnalysisOutputRecord) -> AnalysisOutput:
        return AnalysisOutput(
            source_summary=record.source_summary_json,
            insights=record.insights_json,
            script_draft=record.script_draft_json,
            shot_plan=record.shot_plan_json,
        )

    def _workflow_record_to_schema(self, record: WorkflowDraftRecord) -> WorkflowDraft:
        return WorkflowDraft(
            id=record.id,
            project_id=record.project_id,
            version=record.version,
            meta=record.meta_json,
            segments=record.segments_json,
            cta=record.cta_json,
            low_code_graph=record.low_code_graph_json,
            updated_at=to_iso_datetime(record.updated_at) or "",
        )

    def _render_run_to_summary(self, record: RenderRunRecord) -> RenderRunSummary:
        return RenderRunSummary(
            id=record.id,
            project_id=record.project_id,
            workflow_draft_id=record.workflow_draft_id,
            status=record.status,
            provider=record.provider,
            trace_id=record.trace_id,
            usage=MoneyUsage(**(record.usage_json or {})),
            created_at=to_iso_datetime(record.created_at) or "",
            completed_at=to_iso_datetime(record.completed_at),
            error_message=record.error_message,
        )

    def _run_step_to_summary(self, record: RunStepRecord) -> RunStepSummary:
        return RunStepSummary(
            name=record.name,
            status=record.status,
            capability=record.capability,
            provider=record.provider,
            started_at=to_iso_datetime(record.started_at),
            finished_at=to_iso_datetime(record.finished_at),
            error_message=record.error_message,
        )

    def _output_asset_to_summary(self, record: OutputAssetRecord) -> OutputAssetSummary:
        return OutputAssetSummary(
            id=record.id,
            asset_type=record.asset_type,
            storage_key=record.storage_key,
            preview_storage_key=record.preview_storage_key,
        )

    def _trace_for_project(self, project: ProjectRecord, trace_id: str | None = None) -> TraceContext:
        return TraceContext(
            trace_id=trace_id or make_id("trace"),
            request_id=make_id("req"),
            actor_id=project.owner_id,
            org_id=project.org_id,
        )

    def _get_project_record_or_raise(self, session, project_id: str) -> ProjectRecord:
        project = session.get(ProjectRecord, project_id)
        if project is None:
            raise KeyError(project_id)
        return project

    def _get_render_run_record_or_raise(self, session, project_id: str, run_id: str) -> RenderRunRecord:
        run_record = session.get(RenderRunRecord, run_id)
        if run_record is None or run_record.project_id != project_id:
            raise KeyError(run_id)
        return run_record

    def _first_or_none(self, session, statement: Select):
        return session.execute(statement).scalar_one_or_none()

    def _get_render_step_records(self, session, run_id: str) -> list[RunStepRecord]:
        return list(
            session.execute(select(RunStepRecord).where(RunStepRecord.run_id == run_id).order_by(RunStepRecord.name)).scalars()
        )

    def _apply_render_step_updates(self, step_records: list[RunStepRecord], step_summaries: list[RunStepSummary]) -> None:
        step_record_by_name = {record.name: record for record in step_records}
        for step_summary in step_summaries:
            step_record = step_record_by_name[step_summary.name]
            step_record.status = step_summary.status
            step_record.started_at = parse_iso_datetime(step_summary.started_at)
            step_record.finished_at = parse_iso_datetime(step_summary.finished_at)
            step_record.error_message = step_summary.error_message

    def _render_detail_response(self, run_record: RenderRunRecord, step_records: list[RunStepRecord]) -> RenderRunDetailResponse:
        return RenderRunDetailResponse(
            run=self._render_run_to_summary(run_record),
            steps=[self._run_step_to_summary(step_record) for step_record in step_records],
        )

    def _ensure_analysis(
        self,
        session,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> tuple[AnalysisRunRecord, AnalysisOutputRecord]:
        project = self._get_project_record_or_raise(session, project_id)

        if project.latest_analysis_run_id:
            run_record = session.get(AnalysisRunRecord, project.latest_analysis_run_id)
            output_record = self._first_or_none(
                session,
                select(AnalysisOutputRecord).where(AnalysisOutputRecord.analysis_run_id == project.latest_analysis_run_id),
            )
            if run_record is not None and output_record is not None:
                return run_record, output_record

        trace = trace or default_trace_context()
        now = utc_now_datetime()
        usage = MoneyUsage(input_tokens=980, output_tokens=240, estimated_cost_usd=0.021)
        run_record = AnalysisRunRecord(
            id=make_id("analysis"),
            project_id=project_id,
            status="succeeded",
            capability="analysis",
            provider=provider.primary,
            prompt_version=provider.prompt_version,
            trace_id=trace.trace_id,
            usage_json=usage.model_dump(mode="json"),
            error_message=None,
            created_at=now,
            completed_at=now,
        )
        session.add(run_record)
        session.flush()

        analysis_output = build_analysis_output(project.title, project.source_type)
        output_record = AnalysisOutputRecord(
            id=make_id("analysis_output"),
            project_id=project_id,
            analysis_run_id=run_record.id,
            source_summary_json=analysis_output.source_summary.model_dump(mode="json"),
            insights_json=analysis_output.insights.model_dump(mode="json"),
            script_draft_json=analysis_output.script_draft.model_dump(mode="json"),
            shot_plan_json=analysis_output.shot_plan.model_dump(mode="json"),
            created_at=now,
        )
        session.add(output_record)

        project.latest_analysis_run_id = run_record.id
        project.current_stage = "analysis_ready"
        project.updated_at = now
        self._record_audit(
            session,
            "run",
            "analysis.completed",
            trace,
            project_id=project_id,
            run_id=run_record.id,
            metadata={"provider": provider.primary},
        )
        session.flush()
        return run_record, output_record

    def _ensure_workflow(self, session, project_id: str, trace: TraceContext | None = None) -> WorkflowDraftRecord:
        project = self._get_project_record_or_raise(session, project_id)

        if project.latest_workflow_draft_id:
            workflow_record = session.get(WorkflowDraftRecord, project.latest_workflow_draft_id)
            if workflow_record is not None:
                return workflow_record

        if not project.latest_analysis_run_id:
            raise KeyError(project_id)

        analysis_output_record = self._first_or_none(
            session,
            select(AnalysisOutputRecord).where(AnalysisOutputRecord.analysis_run_id == project.latest_analysis_run_id),
        )
        if analysis_output_record is None:
            raise KeyError(project.latest_analysis_run_id)

        analysis_output = self._analysis_output_to_schema(analysis_output_record)
        workflow = build_workflow_from_analysis(project_id, analysis_output)
        workflow_record = WorkflowDraftRecord(
            id=workflow.id,
            project_id=workflow.project_id,
            version=workflow.version,
            meta_json=workflow.meta.model_dump(mode="json"),
            segments_json=[segment.model_dump(mode="json") for segment in workflow.segments],
            cta_json=workflow.cta.model_dump(mode="json"),
            low_code_graph_json=workflow.low_code_graph.model_dump(mode="json", by_alias=True),
            created_from_analysis_run_id=project.latest_analysis_run_id,
            created_at=parse_iso_datetime(workflow.updated_at) or utc_now_datetime(),
            updated_at=parse_iso_datetime(workflow.updated_at) or utc_now_datetime(),
        )
        session.add(workflow_record)

        project.latest_workflow_draft_id = workflow_record.id
        project.current_stage = "workflow_ready"
        project.updated_at = workflow_record.updated_at
        self._record_audit(
            session,
            "run",
            "workflow.prefilled",
            trace or default_trace_context(),
            project_id=project_id,
            metadata={"workflowVersion": workflow.version},
        )
        session.flush()
        return workflow_record

    def _create_render_run(
        self,
        session,
        payload: CreateRenderRunRequest,
        provider: ProviderConfig,
        *,
        completed: bool,
    ) -> RenderRunDetailResponse:
        project = self._get_project_record_or_raise(session, payload.project_id)
        workflow = session.get(WorkflowDraftRecord, payload.workflow_draft_id)
        if workflow is None or workflow.project_id != payload.project_id:
            raise KeyError(payload.workflow_draft_id)

        trace = payload.trace or default_trace_context()
        now = utc_now_datetime()
        status = "succeeded" if completed else "queued"
        usage = MoneyUsage(input_tokens=120, output_tokens=0, estimated_cost_usd=0.18 if completed else 0.0)
        run_record = RenderRunRecord(
            id=make_id("render"),
            project_id=payload.project_id,
            workflow_draft_id=payload.workflow_draft_id,
            status=status,
            provider=provider.primary,
            trace_id=trace.trace_id,
            usage_json=usage.model_dump(mode="json"),
            error_message=None,
            created_at=now,
            completed_at=now if completed else None,
        )
        session.add(run_record)
        session.flush()

        step_records: list[RunStepRecord] = []
        for step in build_render_run_steps(
            provider.primary,
            status,
            started_at=to_iso_datetime(now) if completed else None,
            finished_at=to_iso_datetime(now) if completed else None,
        ):
            step_record = RunStepRecord(
                id=make_id("step"),
                run_id=run_record.id,
                run_type="render",
                name=step.name,
                status=step.status,
                capability=step.capability,
                provider=step.provider,
                started_at=parse_iso_datetime(step.started_at),
                finished_at=parse_iso_datetime(step.finished_at),
                error_message=step.error_message,
                step_payload_json=None,
            )
            session.add(step_record)
            step_records.append(step_record)

        project.latest_render_run_id = run_record.id
        project.current_stage = "result_ready" if completed else "render_pending"
        project.updated_at = now

        if completed:
            asset_summary = build_output_asset_summary(payload.project_id, run_record.id)
            session.add(
                OutputAssetRecord(
                    id=asset_summary.id,
                    project_id=payload.project_id,
                    render_run_id=run_record.id,
                    asset_type=asset_summary.asset_type,
                    storage_key=asset_summary.storage_key,
                    preview_storage_key=asset_summary.preview_storage_key,
                    created_at=now,
                )
            )

        self._record_audit(
            session,
            "run",
            "render.created",
            trace,
            project_id=payload.project_id,
            run_id=run_record.id,
            metadata={"provider": provider.primary, "completed": completed},
        )
        session.flush()
        return RenderRunDetailResponse(
            run=self._render_run_to_summary(run_record),
            steps=[self._run_step_to_summary(step_record) for step_record in step_records],
        )

    def create_project(self, payload: CreateProjectRequest) -> ProjectDetailResponse:
        with self._session_factory() as session:
            trace = payload.trace or default_trace_context()
            now = utc_now_datetime()
            record = ProjectRecord(
                id=make_id("proj"),
                org_id=trace.org_id,
                owner_id=trace.actor_id,
                title=payload.title or ("爆款链接项目" if payload.source_type == "video_url" else "商品信息项目"),
                source_type=payload.source_type,
                source_url=payload.source_url,
                source_payload_json=payload.product_brief.model_dump(mode="json") if payload.product_brief else None,
                current_stage="draft",
                latest_analysis_run_id=None,
                latest_workflow_draft_id=None,
                latest_render_run_id=None,
                created_at=now,
                updated_at=now,
            )
            session.add(record)
            self._record_audit(
                session,
                "config",
                "project.created",
                trace,
                project_id=record.id,
                metadata={"sourceType": payload.source_type},
            )
            session.commit()
            return ProjectDetailResponse(project=self._project_record_to_detail(record))

    def get_project(self, project_id: str) -> ProjectDetailResponse:
        with self._session_factory() as session:
            return ProjectDetailResponse(project=self._project_record_to_detail(self._get_project_record_or_raise(session, project_id)))

    def get_analysis(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> AnalysisResultResponse:
        with self._session_factory() as session:
            run_record, output_record = self._ensure_analysis(session, project_id, provider, trace=trace)
            session.commit()
            output = self._analysis_output_to_schema(output_record)
            return AnalysisResultResponse(
                run=self._analysis_run_to_summary(run_record),
                source_summary=output.source_summary,
                insights=output.insights,
            )

    def get_workflow(
        self,
        project_id: str,
        provider: ProviderConfig,
        trace: TraceContext | None = None,
    ) -> WorkflowDraftResponse:
        with self._session_factory() as session:
            self._ensure_analysis(session, project_id, provider, trace=trace)
            workflow_record = self._ensure_workflow(session, project_id, trace=trace)
            session.commit()
            return WorkflowDraftResponse(workflow=self._workflow_record_to_schema(workflow_record))

    def create_render_run(self, payload: CreateRenderRunRequest, provider: ProviderConfig) -> RenderRunDetailResponse:
        with self._session_factory() as session:
            response = self._create_render_run(session, payload, provider, completed=False)
            session.commit()
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
        with self._session_factory() as session:
            project = self._get_project_record_or_raise(session, project_id)
            run_record = self._get_render_run_record_or_raise(session, project_id, run_id)
            step_records = self._get_render_step_records(session, run_id)

            if run_record.status == "failed":
                return self._render_detail_response(run_record, step_records)

            existing_asset_record = self._first_or_none(
                session,
                select(OutputAssetRecord).where(OutputAssetRecord.render_run_id == run_id),
            )

            if run_record.status == "succeeded":
                if existing_asset_record is None:
                    asset_summary = build_output_asset_summary(project_id, run_id)
                    session.add(
                        OutputAssetRecord(
                            id=asset_summary.id,
                            project_id=project_id,
                            render_run_id=run_id,
                            asset_type=asset_summary.asset_type,
                            storage_key=asset_summary.storage_key,
                            preview_storage_key=asset_summary.preview_storage_key,
                            created_at=run_record.completed_at or utc_now_datetime(),
                        )
                    )
                    session.commit()
                return self._render_detail_response(run_record, step_records)

            finished_at = utc_now_datetime()
            run_record.status = "succeeded"
            run_record.completed_at = finished_at
            run_record.error_message = None
            run_record.usage_json = MoneyUsage(
                input_tokens=120,
                output_tokens=0,
                estimated_cost_usd=0.18,
            ).model_dump(mode="json")
            self._apply_render_step_updates(
                step_records,
                build_render_run_steps(
                    provider.primary,
                    "succeeded",
                    started_at=to_iso_datetime(run_record.created_at),
                    finished_at=to_iso_datetime(finished_at),
                ),
            )

            if existing_asset_record is None:
                asset_summary = build_output_asset_summary(project_id, run_id)
                session.add(
                    OutputAssetRecord(
                        id=asset_summary.id,
                        project_id=project_id,
                        render_run_id=run_id,
                        asset_type=asset_summary.asset_type,
                        storage_key=asset_summary.storage_key,
                        preview_storage_key=asset_summary.preview_storage_key,
                        created_at=finished_at,
                    )
                )

            if project.latest_render_run_id == run_id:
                project.current_stage = "result_ready"
                project.updated_at = finished_at

            self._record_audit(
                session,
                "run",
                "render.completed",
                self._trace_for_project(project, run_record.trace_id),
                project_id=project_id,
                run_id=run_id,
                metadata={"provider": provider.primary},
            )
            session.commit()
            log_event(
                "run.step.snapshot",
                trace_id=run_record.trace_id,
                project_id=project_id,
                run_id=run_id,
                run_status="succeeded",
                step_statuses={step.name: step.status for step in self._render_detail_response(run_record, step_records).steps},
            )
            return self._render_detail_response(run_record, step_records)

    def fail_render_run(
        self,
        project_id: str,
        run_id: str,
        provider: ProviderConfig,
        error_message: str,
    ) -> RenderRunDetailResponse:
        with self._session_factory() as session:
            project = self._get_project_record_or_raise(session, project_id)
            run_record = self._get_render_run_record_or_raise(session, project_id, run_id)
            step_records = self._get_render_step_records(session, run_id)

            if run_record.status == "succeeded":
                return self._render_detail_response(run_record, step_records)

            finished_at = utc_now_datetime()
            run_record.status = "failed"
            run_record.completed_at = finished_at
            run_record.error_message = error_message
            run_record.usage_json = MoneyUsage(
                input_tokens=120,
                output_tokens=0,
                estimated_cost_usd=0.0,
            ).model_dump(mode="json")
            self._apply_render_step_updates(
                step_records,
                build_render_run_steps(
                    provider.primary,
                    "failed",
                    started_at=to_iso_datetime(run_record.created_at),
                    finished_at=to_iso_datetime(finished_at),
                    error_message=error_message,
                ),
            )

            if project.latest_render_run_id == run_id:
                project.current_stage = "failed"
                project.updated_at = finished_at

            self._record_audit(
                session,
                "run",
                "render.failed",
                self._trace_for_project(project, run_record.trace_id),
                project_id=project_id,
                run_id=run_id,
                metadata={"provider": provider.primary, "errorMessage": error_message},
            )
            session.commit()
            log_event(
                "run.step.snapshot",
                trace_id=run_record.trace_id,
                project_id=project_id,
                run_id=run_id,
                run_status="failed",
                step_statuses={step.name: step.status for step in self._render_detail_response(run_record, step_records).steps},
                error_message=error_message,
            )
            return self._render_detail_response(run_record, step_records)

    def get_run_detail(self, project_id: str, run_id: str) -> RenderRunDetailResponse:
        with self._session_factory() as session:
            run_record = self._get_render_run_record_or_raise(session, project_id, run_id)
            step_records = self._get_render_step_records(session, run_id)
            return self._render_detail_response(run_record, step_records)

    def get_result(self, project_id: str) -> OutputAssetSummary | None:
        with self._session_factory() as session:
            project = self._get_project_record_or_raise(session, project_id)
            if project.latest_render_run_id is None:
                return None
            asset_record = self._first_or_none(
                session,
                select(OutputAssetRecord)
                .where(OutputAssetRecord.render_run_id == project.latest_render_run_id)
                .order_by(desc(OutputAssetRecord.created_at)),
            )
            if asset_record is None:
                return None
            return self._output_asset_to_summary(asset_record)

    def get_history(self, limit: int | None = None) -> ProjectHistoryResponse:
        with self._session_factory() as session:
            statement = select(RenderRunRecord).order_by(desc(RenderRunRecord.created_at))
            if limit is not None:
                statement = statement.limit(limit)
            runs = list(session.execute(statement).scalars())
            projects = {
                project.id: project.title
                for project in session.execute(select(ProjectRecord.id, ProjectRecord.title)).all()
            }
            items = [
                ProjectHistoryItem(
                    project_id=run.project_id,
                    project_title=projects.get(run.project_id, run.project_id),
                    run_id=run.id,
                    run_type="render",
                    status=run.status,
                    updated_at=to_iso_datetime(run.completed_at or run.created_at) or "",
                )
                for run in runs
            ]
            return ProjectHistoryResponse(items=items)
