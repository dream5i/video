export type AnalysisOutputSchema = {
  sourceSummary: {
    platform: string | null;
    sourceType: "video_url" | "product_brief";
    title: string;
  };
  insights: {
    targetAudience: string[];
    sellingPoints: string[];
    hooks: string[];
    cta: string;
  };
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

export type StoryboardDraftSchema = {
  schemaVersion: "2026-04-23";
  meta: {
    ratio: "9:16";
    language: "zh-CN";
    tone: string;
    style: string;
  };
  segments: Array<{
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
  }>;
  cta: {
    text: string;
  };
  lowCodeGraph: LowCodeWorkflowGraphSchema;
};

export type LowCodeWorkflowNodeKind = "analysis" | "script" | "shot_plan" | "render" | "approval";

export type LowCodeWorkflowNodeSchema = {
  id: string;
  kind: LowCodeWorkflowNodeKind;
  label: string;
  config: Record<string, string | number | boolean | null>;
};

export type LowCodeWorkflowEdgeSchema = {
  id: string;
  from: string;
  to: string;
};

export type LowCodeWorkflowGraphSchema = {
  schemaVersion: "2026-04-23";
  nodes: LowCodeWorkflowNodeSchema[];
  edges: LowCodeWorkflowEdgeSchema[];
};

export type RenderRequestSnapshotSchema = {
  projectId: string;
  workflowVersion: number;
  ratio: "9:16";
  segments: StoryboardDraftSchema["segments"];
  voiceover: {
    enabled: boolean;
    voiceStyle: string;
  };
  music: {
    mode: "auto" | "manual";
  };
};

export type RunProgressSchema = {
  runId: string;
  status: "queued" | "running" | "succeeded" | "failed";
  currentStep: string | null;
  steps: Array<{
    name: string;
    status: "queued" | "running" | "succeeded" | "failed";
  }>;
};
