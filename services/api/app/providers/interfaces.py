from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderExecutionContext:
    trace_id: str
    request_id: str
    actor_id: str
    org_id: str


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


@dataclass(frozen=True)
class RenderProviderRequest:
    project_id: str
    workflow_draft_id: str
    provider: str
    context: ProviderExecutionContext


@dataclass(frozen=True)
class RenderProviderResult:
    provider: str
    status: str
    job_id: str
    metadata: dict[str, Any]


class AnalysisProvider(Protocol):
    async def generate_insight(self, request: AnalysisProviderRequest) -> AnalysisProviderResult:
        """Return normalized analysis output."""


class TranscriptProvider(Protocol):
    async def transcribe(self, request: dict[str, Any]) -> dict[str, Any]:
        """Return normalized transcript segments."""


class RenderProvider(Protocol):
    async def submit(self, request: RenderProviderRequest) -> RenderProviderResult:
        """Submit a render job and return normalized job metadata."""
