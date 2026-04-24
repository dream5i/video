"use server";

import { redirect } from "next/navigation";

import { createRenderRun } from "../../../lib/api";

export async function createRenderRunAction(projectId: string, workflowDraftId: string) {
  const response = await createRenderRun(projectId, {
    projectId,
    workflowDraftId
  }).catch(() => null);

  if (response === null) {
    redirect(`/projects/${projectId}?error=render_failed`);
  }

  redirect(`/projects/${projectId}`);
}
