"use server";

import { redirect } from "next/navigation";

import { createRenderRun } from "../../../lib/api";

export async function createRenderRunAction(projectId: string, workflowDraftId: string) {
  try {
    await createRenderRun(projectId, {
      projectId,
      workflowDraftId
    });
    redirect(`/projects/${projectId}`);
  } catch {
    redirect(`/projects/${projectId}?error=render_failed`);
  }
}
