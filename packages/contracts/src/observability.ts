import type { ISODateTime, ProviderCapability, RunStatus } from "./common.js";
import type { RunType } from "./run.js";

export type RunStatusCount = {
  status: RunStatus;
  count: number;
};

export type MainChainHealthSummary = {
  projectsTotal: number;
  analysisRunsTotal: number;
  analysisSuccessRate: number | null;
  workflowDraftsTotal: number;
  renderRunsTotal: number;
  renderSuccessRate: number | null;
  resultAssetsTotal: number;
  runStatusCounts: RunStatusCount[];
};

export type AsyncTaskHealthSummary = {
  queuedRuns: number;
  runningRuns: number;
  activeRuns: number;
  stuckRuns: number;
  latestRunUpdatedAt: ISODateTime | null;
};

export type ProviderHealthSummary = {
  provider: string;
  capability: ProviderCapability;
  totalRuns: number;
  succeededRuns: number;
  failedRuns: number;
  averageLatencyMs: number | null;
  estimatedCostUsd: number | null;
  lastEventAt: ISODateTime | null;
};

export type ObservabilityFailureItem = {
  projectId: string;
  projectTitle: string;
  runId: string;
  runType: RunType;
  provider: string;
  status: "failed";
  traceId: string;
  errorCode: string;
  errorMessage: string | null;
  updatedAt: ISODateTime;
};

export type ObservabilitySignal = {
  id: string;
  label: string;
  status: "ok" | "partial" | "missing" | "attention";
  detail: string;
  evidence: string | null;
};

export type ObservabilitySummaryResponse = {
  ok: true;
  generatedAt: ISODateTime;
  mainChain: MainChainHealthSummary;
  asyncTasks: AsyncTaskHealthSummary;
  providers: ProviderHealthSummary[];
  recentFailures: ObservabilityFailureItem[];
  signals: ObservabilitySignal[];
};
