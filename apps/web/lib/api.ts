import type {
  AnalysisResultResponse,
  CreateProjectRequest,
  CreateRenderRunRequest,
  ProjectDetailResponse,
  ProjectHistoryResponse,
  ProjectResultResponse,
  RenderRunDetailResponse,
  WorkflowDraftResponse
} from "@new-project/contracts";

const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getApiBaseUrl() {
  return process.env.API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;
}

function buildUrl(path: string) {
  return new URL(path, getApiBaseUrl()).toString();
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(buildUrl(path), {
    cache: "no-store",
    ...init,
    headers: {
      ...(init?.body ? { "content-type": "application/json" } : {}),
      ...init?.headers
    }
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

async function safeRequest<T>(path: string) {
  try {
    return await requestJson<T>(path);
  } catch {
    return null;
  }
}

export function getProject(projectId: string) {
  return safeRequest<ProjectDetailResponse>(`/api/projects/${projectId}`);
}

export function getProjectAnalysis(projectId: string) {
  return safeRequest<AnalysisResultResponse>(`/api/projects/${projectId}/analysis`);
}

export function getProjectWorkflow(projectId: string) {
  return safeRequest<WorkflowDraftResponse>(`/api/projects/${projectId}/workflow`);
}

export function getProjectResult(projectId: string) {
  return safeRequest<ProjectResultResponse>(`/api/projects/${projectId}/result`);
}

export function getRenderRun(projectId: string, runId: string) {
  return safeRequest<RenderRunDetailResponse>(`/api/projects/${projectId}/runs/${runId}`);
}

export function getHistory() {
  return safeRequest<ProjectHistoryResponse>("/api/history");
}

export function createProject(payload: CreateProjectRequest) {
  return requestJson<ProjectDetailResponse>("/api/projects", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function createRenderRun(projectId: string, payload: CreateRenderRunRequest) {
  return requestJson<RenderRunDetailResponse>(`/api/projects/${projectId}/renders`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
