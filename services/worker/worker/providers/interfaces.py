from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderExecutionContext:
    trace_id: str
    request_id: str
    actor_id: str
    org_id: str
    run_id: str | None = None
    run_step_id: str | None = None


@dataclass(frozen=True)
class AnalysisProviderRequest:
    project_id: str
    source_type: str
    source_value: str | None
    prompt_version: str
    context: ProviderExecutionContext


@dataclass(frozen=True)
class AnalysisProviderResult:
    provider: str
    status: str
    output: dict[str, Any]
    usage: dict[str, int | float | None]


class AnalysisProvider(Protocol):
    def generate(self, request: AnalysisProviderRequest) -> AnalysisProviderResult:
        """Generate normalized analysis output for a project."""
