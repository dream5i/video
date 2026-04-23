import type { ISODateTime, RunStatus } from "./common.js";
import type { RunType } from "./run.js";

export type ProjectHistoryItem = {
  projectId: string;
  projectTitle: string;
  runId: string;
  runType: RunType;
  status: RunStatus;
  updatedAt: ISODateTime;
};

export type ProjectHistoryResponse = {
  ok: true;
  items: ProjectHistoryItem[];
};
