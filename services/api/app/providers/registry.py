from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 2
    base_backoff_seconds: int = 5


@dataclass(frozen=True)
class ProviderConfig:
    capability: str
    primary: str
    fallback: str | None = None
    prompt_version: str = "v1"
    soft_budget_usd: float = 5.0
    hard_budget_usd: float = 15.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderConfig] = {
            "analysis": ProviderConfig(
                capability="analysis",
                primary="openai_analysis",
                fallback="anthropic_analysis",
                prompt_version="analysis.v1",
                soft_budget_usd=1.5,
                hard_budget_usd=4.0,
            ),
            "transcript": ProviderConfig(capability="transcript", primary="whisper_primary", prompt_version="transcript.v1"),
            "ocr": ProviderConfig(capability="ocr", primary="vision_ocr_primary", prompt_version="ocr.v1"),
            "render": ProviderConfig(
                capability="render",
                primary="render_primary",
                prompt_version="render.v1",
                soft_budget_usd=3.0,
                hard_budget_usd=10.0,
            ),
        }

    def get(self, capability: str) -> ProviderConfig:
        return self._providers[capability]


provider_registry = ProviderRegistry()
