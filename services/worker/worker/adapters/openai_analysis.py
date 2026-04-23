from __future__ import annotations

from worker.providers.interfaces import AnalysisProviderRequest, AnalysisProviderResult


class OpenAIAnalysisAdapter:
    def generate(self, request: AnalysisProviderRequest) -> AnalysisProviderResult:
        return AnalysisProviderResult(
            provider="openai",
            status="stubbed",
            output={
                "sourceSummary": {"platform": "douyin", "sourceType": request.source_type, "title": "worker analysis stub"},
                "insights": {
                    "targetAudience": ["宝妈", "家庭用户"],
                    "sellingPoints": ["清甜", "干净", "适合家庭场景"],
                    "hooks": ["前三秒真实场景切入"],
                    "cta": "先回填低代码工作流，再决定是否直接运行。",
                },
            },
            usage={"input_tokens": 512, "output_tokens": 128, "estimated_cost_usd": 0.014},
        )
