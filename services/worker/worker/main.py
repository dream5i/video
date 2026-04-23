from __future__ import annotations

from worker.providers.registry import provider_registry
from worker.providers.interfaces import AnalysisProviderRequest, ProviderExecutionContext


def run_demo_analysis(project_id: str) -> dict:
    request = AnalysisProviderRequest(
        project_id=project_id,
        source_type="video_url",
        source_value="https://example.com/demo",
        prompt_version=provider_registry.analysis_config.prompt_version,
        context=ProviderExecutionContext(
            trace_id="trace_demo",
            request_id="req_demo",
            actor_id="user_demo",
            org_id="org_demo",
        ),
    )
    return provider_registry.analysis_primary.generate(request).__dict__


if __name__ == "__main__":
    print(run_demo_analysis("proj_demo"))
