from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT_DIR = Path(__file__).resolve().parents[2]
API_ROOT = ROOT_DIR / "services" / "api"

if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.db.session import reset_db_session_state
from app.domain.sql_repository import SqlProjectRepository
from app.providers.registry import provider_registry
from app.schemas import CreateProjectRequest, CreateRenderRunRequest


class SqlRepositoryMainFlowIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.database_url = f"sqlite+pysqlite:///{Path(self.temp_dir.name) / 'integration.db'}"
        reset_db_session_state(self.database_url)
        self.repository = SqlProjectRepository(database_url=self.database_url)
        self.analysis_provider = provider_registry.get("analysis")
        self.render_provider = provider_registry.get("render")

    def tearDown(self) -> None:
        reset_db_session_state(self.database_url)
        self.temp_dir.cleanup()

    def test_database_repository_supports_mvp_main_flow(self) -> None:
        create_response = self.repository.create_project(
            CreateProjectRequest(
                source_type="video_url",
                source_url="https://example.com/douyin/demo",
                title="纯粹计划小吊梨汤测试项目",
                ratio="9:16",
            )
        )
        project_id = create_response.project.id
        self.assertEqual(create_response.project.current_stage, "draft")

        project_response = self.repository.get_project(project_id)
        self.assertEqual(project_response.project.id, project_id)
        self.assertEqual(project_response.project.title, "纯粹计划小吊梨汤测试项目")

        analysis_response = self.repository.get_analysis(project_id, self.analysis_provider)
        self.assertEqual(analysis_response.run.status, "succeeded")
        self.assertEqual(analysis_response.run.project_id, project_id)
        self.assertEqual(analysis_response.source_summary.source_type, "video_url")

        workflow_response = self.repository.get_workflow(project_id, self.analysis_provider)
        self.assertEqual(workflow_response.workflow.project_id, project_id)
        self.assertGreater(len(workflow_response.workflow.segments), 0)

        render_response = self.repository.create_render_run(
            CreateRenderRunRequest(
                project_id=project_id,
                workflow_draft_id=workflow_response.workflow.id,
            ),
            self.render_provider,
        )
        self.assertEqual(render_response.run.status, "queued")
        self.assertEqual(render_response.run.project_id, project_id)
        self.assertGreater(len(render_response.steps), 0)

        run_detail_response = self.repository.get_run_detail(project_id, render_response.run.id)
        self.assertEqual(run_detail_response.run.id, render_response.run.id)
        self.assertEqual(run_detail_response.run.workflow_draft_id, workflow_response.workflow.id)

        completed_render_response = self.repository.process_render_run(
            project_id,
            render_response.run.id,
            self.render_provider,
        )
        self.assertEqual(completed_render_response.run.status, "succeeded")

        latest_project_response = self.repository.get_project(project_id)
        self.assertEqual(latest_project_response.project.current_stage, "result_ready")

        result_asset = self.repository.get_result(project_id)
        self.assertIsNotNone(result_asset)
        if result_asset is None:
            self.fail("result asset should exist after render completion")
        self.assertEqual(result_asset.storage_key, f"projects/{project_id}/runs/{render_response.run.id}/output.mp4")

        history_response = self.repository.get_history()
        matching_items = [
            item
            for item in history_response.items
            if item.project_id == project_id and item.run_id == render_response.run.id
        ]
        self.assertEqual(len(matching_items), 1)
        self.assertEqual(matching_items[0].status, "succeeded")

        limited_history_response = self.repository.get_history(limit=1)
        self.assertEqual(len(limited_history_response.items), 1)
        self.assertEqual(limited_history_response.items[0].run_id, render_response.run.id)

        observability_summary = self.repository.get_observability_summary()
        self.assertGreaterEqual(observability_summary.main_chain.projects_total, 2)
        self.assertGreaterEqual(observability_summary.main_chain.render_runs_total, 2)
        self.assertGreaterEqual(len(observability_summary.providers), 2)
        self.assertTrue(any(signal.id == "api-trace-headers" and signal.status == "ok" for signal in observability_summary.signals))

    def test_database_repository_marks_failed_render_and_keeps_result_empty(self) -> None:
        create_response = self.repository.create_project(
            CreateProjectRequest(
                source_type="video_url",
                source_url="https://example.com/douyin/demo-failed",
                title="失败渲染测试项目",
                ratio="9:16",
            )
        )
        project_id = create_response.project.id

        workflow_response = self.repository.get_workflow(project_id, self.analysis_provider)
        render_response = self.repository.create_render_run(
            CreateRenderRunRequest(
                project_id=project_id,
                workflow_draft_id=workflow_response.workflow.id,
            ),
            self.render_provider,
        )

        failed_response = self.repository.fail_render_run(
            project_id,
            render_response.run.id,
            self.render_provider,
            "stub render failed",
        )
        self.assertEqual(failed_response.run.status, "failed")
        self.assertEqual(failed_response.run.error_message, "stub render failed")
        self.assertTrue(any(step.status == "failed" for step in failed_response.steps))

        latest_project_response = self.repository.get_project(project_id)
        self.assertEqual(latest_project_response.project.current_stage, "failed")
        self.assertIsNone(self.repository.get_result(project_id))

        history_response = self.repository.get_history()
        matching_items = [
            item
            for item in history_response.items
            if item.project_id == project_id and item.run_id == render_response.run.id
        ]
        self.assertEqual(len(matching_items), 1)
        self.assertEqual(matching_items[0].status, "failed")

        observability_summary = self.repository.get_observability_summary()
        matching_failures = [
            item
            for item in observability_summary.recent_failures
            if item.project_id == project_id and item.run_id == render_response.run.id
        ]
        self.assertEqual(len(matching_failures), 1)
        self.assertEqual(matching_failures[0].error_code, "RENDER_ERROR")
