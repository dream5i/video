"use server";

import type { CreateProjectRequest } from "@new-project/contracts";
import { redirect } from "next/navigation";

import { createProject } from "../../../lib/api";

function readField(formData: FormData, key: string) {
  const value = formData.get(key);
  return typeof value === "string" ? value.trim() : "";
}

function parseSellingPoints(input: string) {
  return input
    .split(/[\n,，]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export async function createProjectAction(formData: FormData) {
  const sourceType = readField(formData, "sourceType") === "product_brief" ? "product_brief" : "video_url";
  const title = readField(formData, "title");

  const payload: CreateProjectRequest = {
    sourceType,
    ratio: "9:16",
    ...(title ? { title } : {})
  };

  if (sourceType === "video_url") {
    const sourceUrl = readField(formData, "sourceUrl");

    if (sourceUrl) {
      payload.sourceUrl = sourceUrl;
    }
  } else {
    const productName = readField(formData, "productName") || "待补充商品";
    const targetAudience = readField(formData, "targetAudience") || "待补充目标人群";
    const sellingPoints = parseSellingPoints(readField(formData, "sellingPoints"));

    payload.productBrief = {
      productName,
      targetAudience,
      sellingPoints: sellingPoints.length > 0 ? sellingPoints : ["待补充核心卖点"]
    };
  }

  try {
    const response = await createProject(payload);
    redirect(`/projects/${response.project.id}`);
  } catch {
    redirect(`/projects/new?error=${sourceType === "video_url" ? "video_create_failed" : "brief_create_failed"}`);
  }
}
