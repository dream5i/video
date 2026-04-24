import { expect, test } from "@playwright/test";

test("user can create a project, run render, and see it in history", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("link", { name: "新建一个项目" }).click();
  await expect(page).toHaveURL(/\/projects\/new/);

  const projectTitle = `E2E 主链项目 ${Date.now()}`;

  await page.locator("#video-title").fill(projectTitle);
  await page.locator("#source-url").fill("https://example.com/e2e-main-flow");
  await page.getByRole("button", { name: "以爆款链接创建项目" }).click();

  await expect(page).toHaveURL(/\/projects\/proj_/);
  await expect(page.getByRole("heading", { name: projectTitle })).toBeVisible();
  await expect(page.getByText("结构化分析结果")).toBeVisible();
  await expect(page.getByText("预填充工作流与低代码图")).toBeVisible();

  await page.getByRole("button", { name: "发起一次渲染运行" }).click();
  await expect(page).toHaveURL(/\/projects\/proj_/);
  await expect(page.getByText("运行状态、步骤和产出锚点")).toBeVisible();

  await expect
    .poll(
      async () => {
        await page.reload();
        return (await page.locator("main").textContent()) ?? "";
      },
      {
        message: "waiting for render result asset to appear"
      }
    )
    .toContain("结果锚点：projects/");

  await page.goto("/history");
  await expect(page.getByRole("heading", { name: "最近运行" })).toBeVisible();
  await expect(page.getByText(projectTitle)).toBeVisible();
});
