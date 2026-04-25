from __future__ import annotations

from worker.observability import trace_analysis_provider_call
from worker.providers.interfaces import AnalysisProviderRequest, AnalysisProviderResult


class AnthropicAnalysisAdapter:
    def generate(self, request: AnalysisProviderRequest) -> AnalysisProviderResult:
        def operation() -> AnalysisProviderResult:
            return AnalysisProviderResult(
                provider="anthropic",
                status="stubbed",
                output={
                    "sourceSummary": {"platform": "douyin", "sourceType": request.source_type, "title": "worker fallback stub"},
                    "insights": {
                        "targetAudience": ["精细家庭消费人群"],
                        "sellingPoints": ["配料更放心", "场景更真实"],
                        "hooks": ["先讲使用瞬间，再讲产品差异"],
                        "cta": "把分析结果回填到工作流图后，再决定渲染路线。",
                    },
                },
                usage={"input_tokens": 430, "output_tokens": 144, "estimated_cost_usd": 0.019},
            )

        return trace_analysis_provider_call(
            request=request,
            provider="anthropic",
            model_name="anthropic_analysis_stub",
            operation=operation,
        )
