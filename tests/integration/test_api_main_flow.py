from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import unittest
from urllib import error, request

ROOT_DIR = Path(__file__).resolve().parents[2]
API_ROOT = ROOT_DIR / "services" / "api"


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json_response(method: str, url: str, payload: dict | None = None) -> tuple[int, dict, dict[str, str]]:
    encoded_payload = None
    headers: dict[str, str] = {}
    if payload is not None:
        encoded_payload = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    http_request = request.Request(url, data=encoded_payload, headers=headers, method=method)
    try:
        with request.urlopen(http_request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body), dict(response.headers.items())
    except error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
            return exc.code, json.loads(body), dict(exc.headers.items())
        finally:
            exc.close()


def request_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    status, payload_body, _ = request_json_response(method, url, payload)
    return status, payload_body


class ApiMainFlowIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.port = find_free_port()
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.database_url = f"sqlite+pysqlite:///{Path(self.temp_dir.name) / 'api-flow.db'}"

        env = os.environ.copy()
        python_path = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(API_ROOT) if not python_path else f"{API_ROOT}{os.pathsep}{python_path}"
        env.pop("NEW_PROJECT_REPOSITORY_BACKEND", None)
        env["DATABASE_URL"] = self.database_url
        env["API_HOST"] = "127.0.0.1"
        env["API_PORT"] = str(self.port)

        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(self.port),
            ],
            cwd=ROOT_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        self._wait_until_ready()

    def tearDown(self) -> None:
        if hasattr(self, "process") and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)

        if hasattr(self, "temp_dir"):
            self.temp_dir.cleanup()

    def _wait_until_ready(self) -> None:
        deadline = time.time() + 20
        last_error: Exception | None = None

        while time.time() < deadline:
            if self.process.poll() is not None:
                output = ""
                if self.process.stdout is not None:
                    output = self.process.stdout.read()
                self.fail(f"API server exited before becoming ready.\n{output}")

            try:
                status, payload, headers = request_json_response("GET", f"{self.base_url}/api/health")
                if status == 200 and payload.get("status") == "ok":
                    self.assertIn("x-request-id", {key.lower(): value for key, value in headers.items()})
                    self.assertIn("x-trace-id", {key.lower(): value for key, value in headers.items()})
                    return
            except (OSError, error.URLError, json.JSONDecodeError) as exc:
                last_error = exc

            time.sleep(0.25)

        self.fail(f"API server did not become ready in time: {last_error}")

    def _create_project(self, title: str, source_url: str) -> tuple[str, dict]:
        create_status, create_payload, create_headers = request_json_response(
            "POST",
            f"{self.base_url}/api/projects",
            payload={
                "sourceType": "video_url",
                "sourceUrl": source_url,
                "title": title,
                "ratio": "9:16",
            },
        )
        self.assertEqual(create_status, 200)
        normalized_headers = {key.lower(): value for key, value in create_headers.items()}
        self.assertIn("x-request-id", normalized_headers)
        self.assertIn("x-trace-id", normalized_headers)
        return create_payload["project"]["id"], create_payload

    def _wait_for_run_status(self, project_id: str, run_id: str, expected_status: str) -> dict:
        deadline = time.time() + 10
        last_payload: dict | None = None

        while time.time() < deadline:
            run_status, run_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/runs/{run_id}")
            self.assertEqual(run_status, 200)
            last_payload = run_payload
            current_status = run_payload["run"]["status"]
            if current_status == expected_status:
                return run_payload
            if current_status == "failed" and expected_status != "failed":
                self.fail(f"render run ended in failed unexpectedly: {run_payload}")
            time.sleep(0.2)

        self.fail(f"render run did not reach {expected_status} in time: {last_payload}")

    def _wait_for_result_asset(self, project_id: str) -> dict:
        deadline = time.time() + 10
        last_payload: dict | None = None

        while time.time() < deadline:
            result_status, result_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/result")
            self.assertEqual(result_status, 200)
            last_payload = result_payload
            if result_payload["asset"] is not None:
                return result_payload
            time.sleep(0.2)

        self.fail(f"result asset did not become available in time: {last_payload}")

    def test_http_api_supports_mvp_main_flow(self) -> None:
        project_id, create_payload = self._create_project(
            title="HTTP 主链测试项目",
            source_url="https://example.com/douyin/http-flow",
        )
        self.assertEqual(create_payload["project"]["currentStage"], "draft")

        project_status, project_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}")
        self.assertEqual(project_status, 200)
        self.assertEqual(project_payload["project"]["id"], project_id)

        analysis_status, analysis_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/analysis")
        self.assertEqual(analysis_status, 200)
        self.assertEqual(analysis_payload["run"]["status"], "succeeded")
        self.assertEqual(analysis_payload["sourceSummary"]["sourceType"], "video_url")
        self.assertTrue(analysis_payload["run"]["traceId"].startswith("trace_"))

        workflow_status, workflow_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/workflow")
        self.assertEqual(workflow_status, 200)
        self.assertGreater(len(workflow_payload["workflow"]["segments"]), 0)

        workflow_draft_id = workflow_payload["workflow"]["id"]
        render_status, render_payload = request_json(
            "POST",
            f"{self.base_url}/api/projects/{project_id}/renders",
            payload={
                "projectId": project_id,
                "workflowDraftId": workflow_draft_id,
            },
        )
        self.assertEqual(render_status, 200)
        self.assertIn(render_payload["run"]["status"], {"queued", "succeeded"})
        self.assertGreater(len(render_payload["steps"]), 0)

        run_id = render_payload["run"]["id"]
        run_payload = self._wait_for_run_status(project_id, run_id, "succeeded")
        self.assertEqual(run_payload["run"]["id"], run_id)
        self.assertEqual(run_payload["run"]["status"], "succeeded")

        result_payload = self._wait_for_result_asset(project_id)
        self.assertIsNotNone(result_payload["asset"])
        self.assertEqual(result_payload["asset"]["storageKey"], f"projects/{project_id}/runs/{run_id}/output.mp4")

        history_status, history_payload = request_json("GET", f"{self.base_url}/api/history")
        self.assertEqual(history_status, 200)
        matched_items = [item for item in history_payload["items"] if item["runId"] == run_id]
        self.assertEqual(len(matched_items), 1)
        self.assertEqual(matched_items[0]["status"], "succeeded")

    def test_http_api_returns_expected_errors_for_missing_or_mismatched_resources(self) -> None:
        missing_project_status, missing_project_payload = request_json(
            "GET",
            f"{self.base_url}/api/projects/proj_missing",
        )
        self.assertEqual(missing_project_status, 404)
        self.assertEqual(missing_project_payload["detail"]["message"], "project not found")
        self.assertEqual(missing_project_payload["detail"]["errorCode"], "project_not_found")

        project_id, _ = self._create_project(
            title="HTTP 异常测试项目",
            source_url="https://example.com/douyin/http-error-flow",
        )

        workflow_status, workflow_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/workflow")
        self.assertEqual(workflow_status, 200)

        render_status, render_payload = request_json(
            "POST",
            f"{self.base_url}/api/projects/{project_id}/renders",
            payload={
                "projectId": "proj_other",
                "workflowDraftId": workflow_payload["workflow"]["id"],
            },
        )
        self.assertEqual(render_status, 400)
        self.assertEqual(render_payload["detail"]["message"], "project id mismatch")
        self.assertEqual(render_payload["detail"]["errorCode"], "project_id_mismatch")

    def test_http_api_returns_not_found_for_missing_run_and_missing_result_project(self) -> None:
        project_id, _ = self._create_project(
            title="HTTP 丢失资源测试项目",
            source_url="https://example.com/douyin/http-missing-resources",
        )

        missing_run_status, missing_run_payload = request_json(
            "GET",
            f"{self.base_url}/api/projects/{project_id}/runs/run_missing",
        )
        self.assertEqual(missing_run_status, 404)
        self.assertEqual(missing_run_payload["detail"]["message"], "run not found")
        self.assertEqual(missing_run_payload["detail"]["errorCode"], "run_not_found")

        missing_result_status, missing_result_payload = request_json(
            "GET",
            f"{self.base_url}/api/projects/proj_missing/result",
        )
        self.assertEqual(missing_result_status, 404)
        self.assertEqual(missing_result_payload["detail"]["message"], "project not found")
        self.assertEqual(missing_result_payload["detail"]["errorCode"], "project_not_found")

    def test_http_api_returns_not_found_when_workflow_draft_does_not_belong_to_project(self) -> None:
        project_a_id, _ = self._create_project(
            title="HTTP 工作流归属测试项目A",
            source_url="https://example.com/douyin/http-workflow-project-a",
        )
        project_b_id, _ = self._create_project(
            title="HTTP 工作流归属测试项目B",
            source_url="https://example.com/douyin/http-workflow-project-b",
        )

        workflow_status, workflow_payload = request_json("GET", f"{self.base_url}/api/projects/{project_a_id}/workflow")
        self.assertEqual(workflow_status, 200)

        render_status, render_payload = request_json(
            "POST",
            f"{self.base_url}/api/projects/{project_b_id}/renders",
            payload={
                "projectId": project_b_id,
                "workflowDraftId": workflow_payload["workflow"]["id"],
            },
        )
        self.assertEqual(render_status, 404)
        self.assertEqual(render_payload["detail"]["message"], "project or workflow not found")
        self.assertEqual(render_payload["detail"]["errorCode"], "project_or_workflow_not_found")

    def test_http_api_history_supports_limit_query(self) -> None:
        project_id, _ = self._create_project(
            title="HTTP 历史 limit 测试项目",
            source_url="https://example.com/douyin/http-history-limit",
        )

        workflow_status, workflow_payload = request_json("GET", f"{self.base_url}/api/projects/{project_id}/workflow")
        self.assertEqual(workflow_status, 200)

        render_status, render_payload = request_json(
            "POST",
            f"{self.base_url}/api/projects/{project_id}/renders",
            payload={
                "projectId": project_id,
                "workflowDraftId": workflow_payload["workflow"]["id"],
            },
        )
        self.assertEqual(render_status, 200)
        latest_run_id = render_payload["run"]["id"]

        history_status, history_payload = request_json("GET", f"{self.base_url}/api/history?limit=1")
        self.assertEqual(history_status, 200)
        self.assertEqual(len(history_payload["items"]), 1)
        self.assertEqual(history_payload["items"][0]["runId"], latest_run_id)

    def test_http_api_history_rejects_invalid_limit(self) -> None:
        history_status, history_payload = request_json("GET", f"{self.base_url}/api/history?limit=0")
        self.assertEqual(history_status, 422)
        self.assertEqual(history_payload["detail"]["errorCode"], "validation_error")
        self.assertEqual(history_payload["detail"]["validationErrors"][0]["loc"], ["query", "limit"])

    def test_http_api_exposes_observability_summary(self) -> None:
        status, payload, headers = request_json_response("GET", f"{self.base_url}/api/observability/summary")
        self.assertEqual(status, 200)
        normalized_headers = {key.lower(): value for key, value in headers.items()}
        self.assertIn("x-request-id", normalized_headers)
        self.assertIn("x-trace-id", normalized_headers)

        self.assertTrue(payload["ok"])
        self.assertGreaterEqual(payload["mainChain"]["projectsTotal"], 1)
        self.assertGreaterEqual(payload["mainChain"]["renderRunsTotal"], 1)
        self.assertIn("activeRuns", payload["asyncTasks"])
        self.assertGreaterEqual(len(payload["providers"]), 1)

        signals_by_id = {item["id"]: item for item in payload["signals"]}
        self.assertEqual(signals_by_id["api-trace-headers"]["status"], "ok")
        self.assertEqual(signals_by_id["external-alerting"]["status"], "missing")
