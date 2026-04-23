export type ISODateTime = string;

export type RunStatus = "queued" | "running" | "succeeded" | "failed";

export type ProviderCapability = "analysis" | "transcript" | "ocr" | "render" | "tts";

export type TraceContext = {
  traceId: string;
  requestId: string;
  actorId: string;
  orgId: string;
};

export type AuditEventCategory = "config" | "run" | "security" | "data";

export type AuditEvent = {
  id: string;
  category: AuditEventCategory;
  action: string;
  actorId: string;
  orgId: string;
  projectId?: string;
  runId?: string;
  occurredAt: ISODateTime;
  metadata: Record<string, string | number | boolean | null>;
};

export type PromptRegistryEntry = {
  id: string;
  capability: ProviderCapability;
  version: string;
  status: "draft" | "active" | "retired";
  modelFamily: "openai" | "anthropic" | "provider-agnostic";
  updatedAt: ISODateTime;
};

export type MoneyUsage = {
  inputTokens?: number;
  outputTokens?: number;
  estimatedCostUsd?: number;
};
