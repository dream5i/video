from __future__ import annotations

from dataclasses import dataclass

from worker.adapters.anthropic_analysis import AnthropicAnalysisAdapter
from worker.adapters.openai_analysis import OpenAIAnalysisAdapter


@dataclass(frozen=True)
class ProviderConfig:
    capability: str
    primary: str
    fallback: str | None
    prompt_version: str


class WorkerProviderRegistry:
    def __init__(self) -> None:
        self.analysis_config = ProviderConfig(
            capability="analysis",
            primary="openai_analysis",
            fallback="anthropic_analysis",
            prompt_version="analysis.v1",
        )
        self.analysis_primary = OpenAIAnalysisAdapter()
        self.analysis_fallback = AnthropicAnalysisAdapter()


provider_registry = WorkerProviderRegistry()
