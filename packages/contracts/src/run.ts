import type { ISODateTime, MoneyUsage, ProviderCapability, RunStatus, TraceContext } from "./common.js";

export type RunType = "analysis" | "render";

export type RunStepSummary = {
  name: string;
  status: RunStatus;
  capability: ProviderCapability;
  provider: string | null;
  startedAt: ISODateTime | null;
  finishedAt: ISODateTime | null;
  errorMessage: string | null;
};

export type CreateRenderRunRequest = {
  projectId: string;
  workflowDraftId: string;
  trace?: TraceContext;
};

export type RenderRunSummary = {
  id: string;
  projectId: string;
  workflowDraftId: string;
  status: RunStatus;
  provider: string;
  traceId: string;
  usage: MoneyUsage;
  createdAt: ISODateTime;
  completedAt: ISODateTime | null;
  errorMessage: string | null;
};

export type OutputAssetSummary = {
  id: string;
  assetType: "video" | "image" | "json";
  storageKey: string;
  previewStorageKey: string | null;
};

export type RenderRunDetailResponse = {
  ok: true;
  run: RenderRunSummary;
  steps: RunStepSummary[];
};

export type ProjectResultResponse = {
  ok: true;
  asset: OutputAssetSummary | null;
};
