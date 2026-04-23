import type { ISODateTime, MoneyUsage, ProviderCapability, RunStatus, TraceContext } from "./common.js";

export type AnalysisRunStatus = RunStatus;

export type StartAnalysisRequest = {
  projectId: string;
  regenerate?: boolean;
  trace?: TraceContext;
};

export type AnalysisRunSummary = {
  id: string;
  projectId: string;
  status: AnalysisRunStatus;
  capability: ProviderCapability;
  provider: string;
  promptVersion: string;
  traceId: string;
  usage: MoneyUsage;
  createdAt: ISODateTime;
  completedAt: ISODateTime | null;
  errorMessage: string | null;
};

export type AnalysisInsight = {
  targetAudience: string[];
  sellingPoints: string[];
  hooks: string[];
  cta: string;
};

export type AnalysisOutput = {
  sourceSummary: {
    platform: string | null;
    sourceType: "video_url" | "product_brief";
    title: string;
  };
  insights: AnalysisInsight;
  scriptDraft: {
    opening: string;
    body: string[];
    ending: string;
  };
  shotPlan: {
    segments: Array<{
      id: string;
      visual: string;
      subtitle: string;
      durationSec: number;
    }>;
  };
};

export type AnalysisResultResponse = {
  ok: true;
  run: AnalysisRunSummary;
  sourceSummary: AnalysisOutput["sourceSummary"];
  insights: AnalysisInsight;
};
