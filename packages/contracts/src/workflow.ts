import type { ISODateTime, TraceContext } from "./common.js";

export type WorkflowNodeKind = "analysis" | "script" | "shot_plan" | "render" | "approval";

export type WorkflowNode = {
  id: string;
  kind: WorkflowNodeKind;
  label: string;
  config: Record<string, string | number | boolean | null>;
};

export type WorkflowEdge = {
  id: string;
  from: string;
  to: string;
};

export type WorkflowLowCodeGraph = {
  schemaVersion: "2026-04-23";
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
};

export type WorkflowDraftSegment = {
  id: string;
  goal: "hook" | "body" | "cta";
  script: string;
  durationSec: number;
  shots: Array<{
    id: string;
    visual: string;
    subtitle: string;
    durationSec: number;
  }>;
};

export type WorkflowDraft = {
  id: string;
  projectId: string;
  version: number;
  meta: {
    ratio: "9:16";
    language: "zh-CN";
    tone: string;
    style: string;
  };
  segments: WorkflowDraftSegment[];
  cta: {
    text: string;
  };
  lowCodeGraph: WorkflowLowCodeGraph;
  updatedAt: ISODateTime;
};

export type UpdateWorkflowDraftRequest = {
  meta?: Partial<WorkflowDraft["meta"]>;
  segments?: WorkflowDraftSegment[];
  cta?: Partial<WorkflowDraft["cta"]>;
  lowCodeGraph?: WorkflowLowCodeGraph;
  trace?: TraceContext;
};

export type WorkflowDraftResponse = {
  ok: true;
  workflow: WorkflowDraft;
};
