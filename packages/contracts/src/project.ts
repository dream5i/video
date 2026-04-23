import type { ISODateTime, TraceContext } from "./common.js";

export type ProjectSourceType = "video_url" | "product_brief";
export type ProjectStage =
  | "draft"
  | "analysis_pending"
  | "analysis_ready"
  | "workflow_ready"
  | "render_pending"
  | "result_ready"
  | "failed";

export type ProductBrief = {
  productName: string;
  targetAudience: string;
  sellingPoints: string[];
};

export type CreateProjectRequest = {
  sourceType: ProjectSourceType;
  sourceUrl?: string;
  title?: string;
  ratio: "9:16";
  productBrief?: ProductBrief;
  trace?: TraceContext;
};

export type ProjectSummary = {
  id: string;
  orgId: string;
  ownerId: string;
  title: string;
  sourceType: ProjectSourceType;
  currentStage: ProjectStage;
  updatedAt: ISODateTime;
};

export type ProjectDetailResponse = {
  ok: true;
  project: ProjectSummary & {
    createdAt: ISODateTime;
    latestAnalysisRunId: string | null;
    latestWorkflowDraftId: string | null;
    latestRenderRunId: string | null;
  };
};

export type ProjectListResponse = {
  ok: true;
  items: ProjectSummary[];
};
