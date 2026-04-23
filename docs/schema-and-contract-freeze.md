# 全新项目 Schema 与 Contract 冻结清单

更新日期：2026-04-23
状态：Draft v0.1

## 1. 目的

这份文档只做一件事：

把当前阶段最不应该漂移的结构先写死。

只要后续实现会改动这些结构，就必须先更新这份文档或补 ADR，而不是边写边改。

## 2. 当前冻结级别

### Level A：当前冻结

必须保持稳定，改动需要 review pass：

- `Project` 核心字段
- `AnalysisRun` 核心字段
- `WorkflowDraft` 核心字段
- `RenderRun` 核心字段
- `RunStep` 状态结构
- `StoryboardDraftSchema`
- provider capability naming
- 状态枚举

### Level B：当前半冻结

可以补充，但不应轻易重命名：

- 分析结果里的 insight 字段细节
- 结果页 DTO
- 历史列表字段

### Level C：尚未冻结

后续再定：

- 计费相关 schema
- 多团队 / 权限
- 模板市场
- 批量生成

## 3. 领域对象冻结

### 3.1 Project

当前冻结字段：

- `id`
- `title`
- `sourceType`
- `sourceUrl`
- `currentStage`
- `updatedAt`
- `createdAt`
- `latestAnalysisRunId`
- `latestWorkflowDraftId`
- `latestRenderRunId`

### 3.2 AnalysisRun

当前冻结字段：

- `id`
- `projectId`
- `status`
- `createdAt`
- `completedAt`
- `errorMessage`

说明：

中间产物可以继续增，但 run 的身份字段和状态字段先不要随意变。

### 3.3 WorkflowDraft

当前冻结字段：

- `id`
- `projectId`
- `version`
- `meta`
- `segments`
- `cta`
- `lowCodeGraph`

### 3.4 RenderRun

当前冻结字段：

- `id`
- `projectId`
- `workflowDraftId`
- `status`
- `provider`
- `createdAt`
- `completedAt`
- `errorMessage`

### 3.5 RunStep

当前冻结字段：

- `name`
- `status`
- `startedAt`
- `finishedAt`
- `errorMessage`

## 4. 状态枚举冻结

### 4.1 ProjectStage

当前冻结值：

- `draft`
- `analysis_pending`
- `analysis_ready`
- `workflow_ready`
- `render_pending`
- `result_ready`
- `failed`

### 4.2 Run Status

当前统一建议：

- `queued`
- `running`
- `succeeded`
- `failed`

说明：

当前 `contracts` 与 `technical architecture` 里曾出现过 `pending` 和 `queued` 两套词。  
从现在开始，运行态统一优先使用 `queued/running/succeeded/failed`。  
如果后面确实要引入 `pending` 或 `canceled`，必须统一补一次 contract。

## 5. Provider Capability 冻结

业务层只认能力，不认厂商。

当前冻结能力名：

- `analysis`
- `transcript`
- `ocr`
- `render`
- `tts`

禁止直接把下面这些名字暴露成业务层 contract：

- `openai`
- `anthropic`
- `fal`
- `gemini`

这些名字只能存在于 adapter 或 registry 层。

## 6. StoryboardDraftSchema 冻结

当前冻结顶层结构：

```json
{
  "meta": {},
  "segments": [],
  "cta": {},
  "lowCodeGraph": {}
}
```

### 6.1 meta

当前冻结字段：

- `ratio`
- `language`
- `tone`
- `style`

### 6.2 segments

每个 segment 当前冻结字段：

- `id`
- `goal`
- `script`
- `durationSec`
- `shots`

### 6.3 shots

每个 shot 当前冻结字段：

- `id`
- `visual`
- `subtitle`
- `durationSec`

### 6.4 cta

当前冻结字段：

- `text`

### 6.5 lowCodeGraph

当前冻结字段：

- `schemaVersion`
- `nodes`
- `edges`

## 7. 首批 API Contract 冻结

### 7.1 已确认接口组

- `POST /api/projects`
- `GET /api/projects/:projectId`
- `GET /api/projects/:projectId/analysis`
- `GET /api/projects/:projectId/workflow`
- `POST /api/projects/:projectId/renders`
- `GET /api/projects/:projectId/runs/:runId`
- `GET /api/projects/:projectId/result`
- `GET /api/history`

### 7.2 首批 DTO 名称冻结

- `CreateProjectRequest`
- `ProjectSummary`
- `ProjectDetailResponse`
- `ProjectListResponse`
- `AnalysisResultResponse`
- `WorkflowDraftResponse`
- `RenderRunDetailResponse`
- `ProjectResultResponse`
- `ProjectHistoryResponse`

## 8. 改动规则

触碰下面任一项时，必须额外 review pass：

- 状态枚举
- provider capability name
- workflow schema 顶层结构
- DTO 名称
- 共享 contract 导出路径

## 9. 当前推荐动作

接下来所有实现，都应该先服从这份冻结清单。

如果实现过程发现这份清单不合理，不是直接改代码，而是：

1. 先更新文档或 ADR
2. 再改 contract / schema
3. 最后改实现
