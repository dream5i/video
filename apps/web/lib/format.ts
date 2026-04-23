import type { ProjectSourceType, ProjectStage, RunStatus } from "@new-project/contracts";

const sourceTypeLabels: Record<ProjectSourceType, string> = {
  video_url: "爆款链接",
  product_brief: "商品信息"
};

const stageLabels: Record<ProjectStage, string> = {
  draft: "待补充",
  analysis_pending: "分析中",
  analysis_ready: "分析完成",
  workflow_ready: "工作流可执行",
  render_pending: "运行排队中",
  result_ready: "结果已就绪",
  failed: "执行失败"
};

const statusLabels: Record<RunStatus, string> = {
  queued: "已排队",
  running: "运行中",
  succeeded: "成功",
  failed: "失败"
};

export function formatSourceTypeLabel(sourceType: ProjectSourceType) {
  return sourceTypeLabels[sourceType];
}

export function formatStageLabel(stage: ProjectStage) {
  return stageLabels[stage];
}

export function formatRunStatusLabel(status: RunStatus) {
  return statusLabels[status];
}

export function stageToneClass(stage: ProjectStage) {
  if (stage === "result_ready") {
    return "tone-success";
  }

  if (stage === "analysis_ready" || stage === "workflow_ready" || stage === "analysis_pending" || stage === "render_pending") {
    return "tone-progress";
  }

  if (stage === "failed") {
    return "tone-warn";
  }

  return "tone-neutral";
}

export function runToneClass(status: RunStatus) {
  if (status === "succeeded") {
    return "tone-success";
  }

  if (status === "running") {
    return "tone-progress";
  }

  if (status === "failed") {
    return "tone-warn";
  }

  return "tone-neutral";
}

export function formatDateTime(value: string | null | undefined) {
  if (!value) {
    return "未生成";
  }

  return new Intl.DateTimeFormat("zh-CN", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

export function formatCost(value: number | null | undefined) {
  if (value == null) {
    return "-";
  }

  return `$${value.toFixed(3)}`;
}
