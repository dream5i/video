import type {
  AnalysisResultResponse,
  CreateProjectRequest,
  CreateRenderRunRequest,
  ObservabilitySummaryResponse,
  ProjectDetailResponse,
  ProjectHistoryResponse,
  ProjectResultResponse,
  RenderRunDetailResponse,
  WorkflowDraftResponse
} from "@new-project/contracts";

const DEFAULT_API_BASE_URL = "http://localhost:8000";

type ErrorPayload = {
  detail?: {
    message?: string;
    errorCode?: string;
    requestId?: string;
    traceId?: string;
  };
};

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
    const responseText = await response.text();
    const traceId = response.headers.get("x-trace-id");
    const requestId = response.headers.get("x-request-id");
    let payload: ErrorPayload | null = null;

    try {
      payload = JSON.parse(responseText) as ErrorPayload;
    } catch {
      payload = null;
    }

    if (payload?.detail) {
      const message = payload.detail?.message || `Request failed with status ${response.status}`;
      const errorCode = payload.detail?.errorCode ? ` (${payload.detail.errorCode})` : "";
      const traceSuffix = payload.detail?.traceId || traceId ? ` [trace:${payload.detail?.traceId || traceId}]` : "";
      const requestSuffix = payload.detail?.requestId || requestId ? ` [request:${payload.detail?.requestId || requestId}]` : "";
      throw new Error(`${message}${errorCode}${traceSuffix}${requestSuffix}`);
    }

    throw new Error(responseText || `Request failed with status ${response.status}`);
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

export function getObservabilitySummary() {
  return safeRequest<ObservabilitySummaryResponse>("/api/observability/summary");
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
