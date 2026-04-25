from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest

ROOT_DIR = Path(__file__).resolve().parents[2]
WORKER_ROOT = ROOT_DIR / "services" / "worker"

if str(WORKER_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKER_ROOT))

from worker.adapters.openai_analysis import OpenAIAnalysisAdapter
from worker.observability import trace_analysis_provider_call
from worker.providers.interfaces import AnalysisProviderRequest, AnalysisProviderResult, ProviderExecutionContext


def make_request() -> AnalysisProviderRequest:
    return AnalysisProviderRequest(
        project_id="proj_trace_test",
        source_type="video_url",
        source_value="https://example.com/trace-test",
        prompt_version="analysis.v1",
        context=ProviderExecutionContext(
            trace_id="trace_test",
            request_id="req_test",
            actor_id="user_test",
            org_id="org_test",
            run_id="analysis_test",
            run_step_id="analysis_step_test",
        ),
    )


def parse_log_messages(records) -> list[dict]:
    return [json.loads(record.getMessage()) for record in records]


class WorkerProviderTraceIntegrationTest(unittest.TestCase):
    def test_analysis_adapter_emits_provider_trace_events(self) -> None:
        request = make_request()

        with self.assertLogs("new_project.worker", level="INFO") as captured:
            result = OpenAIAnalysisAdapter().generate(request)

        self.assertEqual(result.status, "stubbed")
        events = parse_log_messages(captured.records)
        started_event = next(item for item in events if item["event"] == "provider.call.started")
        completed_event = next(item for item in events if item["event"] == "provider.call.completed")

        self.assertEqual(started_event["request_id"], "req_test")
        self.assertEqual(started_event["trace_id"], "trace_test")
        self.assertEqual(started_event["project_id"], "proj_trace_test")
        self.assertEqual(started_event["analysis_run_id"], "analysis_test")
        self.assertEqual(started_event["run_step_id"], "analysis_step_test")
        self.assertEqual(started_event["capability"], "analysis")
        self.assertEqual(started_event["provider"], "openai")
        self.assertEqual(completed_event["status"], "stubbed")
        self.assertEqual(completed_event["estimated_cost_usd"], 0.014)
        self.assertIsInstance(completed_event["latency_ms"], float)

    def test_provider_trace_emits_failure_event_with_error_code(self) -> None:
        request = make_request()

        def operation() -> AnalysisProviderResult:
            raise RuntimeError("provider unavailable")

        with self.assertLogs("new_project.worker", level="INFO") as captured:
            with self.assertRaises(RuntimeError):
                trace_analysis_provider_call(
                    request=request,
                    provider="openai",
                    model_name="openai_analysis_stub",
                    operation=operation,
                )

        events = parse_log_messages(captured.records)
        failed_event = next(item for item in events if item["event"] == "provider.call.failed")
        self.assertEqual(failed_event["status"], "failed")
        self.assertEqual(failed_event["error_code"], "ANALYSIS_ERROR")
        self.assertEqual(failed_event["request_id"], "req_test")
        self.assertEqual(failed_event["trace_id"], "trace_test")
        self.assertIsInstance(failed_event["latency_ms"], float)


if __name__ == "__main__":
    unittest.main()
